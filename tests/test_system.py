import unittest
from coordination import Action, Evidence, Job, Proposal
from refresh_lock import RefreshLock
from snapshot import make_snapshot


class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.job = Job(Proposal(Action.SEND, "example recipient", "example content"))
        self.job.assign("worker")

    def test_full_lifecycle_requires_separate_readback(self):
        job = self.job
        self.assertEqual(job.status(), "awaiting_review")
        job.record_review(Evidence(job.proposal_hash, "pass"))
        self.assertEqual(job.status(), "awaiting_approval")
        job.approve(Evidence(job.proposal_hash, "approved"))
        self.assertEqual(job.status(), "ready_for_simulation")
        job.simulate_handoff()
        self.assertEqual(job.status(), "awaiting_readback")
        with self.assertRaises(ValueError):
            job.record_readback(Evidence(job.proposal_hash, "mismatch"))
        self.assertEqual(job.status(), "awaiting_readback")
        job.record_readback(Evidence(job.proposal_hash, "matches"))
        self.assertEqual(job.status(), "verified")

    def test_hold_and_scope_mismatch_block(self):
        job = self.job
        job.record_review(Evidence(job.proposal_hash, "hold"))
        with self.assertRaises(ValueError):
            job.approve(Evidence("wrong hash", "approved"))
        job.approve(Evidence(job.proposal_hash, "approved"))
        self.assertEqual(job.status(), "review_hold")
        with self.assertRaises(ValueError):
            job.simulate_handoff()

    def test_changed_proposal_invalidates_prior_evidence(self):
        job = self.job
        job.record_review(Evidence(job.proposal_hash, "pass"))
        job.approve(Evidence(job.proposal_hash, "approved"))
        job.proposal = Proposal(Action.SEND, "other recipient", "example content")
        self.assertEqual(job.status(), "proposal_changed")
        with self.assertRaises(ValueError):
            job.simulate_handoff()

    def test_purchase_stays_with_owner(self):
        job = Job(Proposal(Action.PURCHASE, "item", "purchase"), False)
        job.assign("worker")
        job.approve(Evidence(job.proposal_hash, "approved"))
        self.assertEqual(job.status(), "owner_final_click")
        with self.assertRaises(ValueError):
            job.simulate_handoff()

    def test_simulation_does_not_accept_a_callback(self):
        with self.assertRaises(TypeError):
            self.job.simulate_handoff(lambda _: self.fail("callback must not run"))

    def test_source_gaps_are_visible(self):
        result = make_snapshot([("example", self.job)], {"source A": False, "source B": True})
        self.assertEqual(result["source_gaps"], ["source A"])
        self.assertEqual(result["jobs"][0]["status"], "awaiting_review")

    def test_refresh_takeover_fences_previous_owner(self):
        lock = RefreshLock(60)
        self.assertTrue(lock.acquire("first", 0))
        self.assertFalse(lock.acquire("second", 59))
        self.assertTrue(lock.acquire("second", 60))
        self.assertFalse(lock.check("first"))
        self.assertFalse(lock.heartbeat("first", 61))
        self.assertFalse(lock.release("first"))
        self.assertTrue(lock.check("second"))
        self.assertTrue(lock.release("second"))


if __name__ == "__main__":
    unittest.main()
