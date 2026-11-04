"""Run only fictional jobs against an in-memory fake executor."""
import json
from coordination import Action, Evidence, Job, Proposal
from refresh_lock import RefreshLock
from snapshot import make_snapshot


def show(label, job):
    print(f"{label}: {job.status()}")


def main():
    proposal = Proposal(Action.SEND, "fictional recipient", "fictional update")
    job = Job(proposal)
    show("New proposal", job)
    job.assign("example worker")
    show("Assigned", job)
    job.record_review(Evidence(job.proposal_hash, "pass"))
    show("Reviewed", job)
    job.approve(Evidence(job.proposal_hash, "approved"))
    show("Approved", job)
    job.simulate_handoff()
    show("Simulated handoff", job)
    job.record_readback(Evidence(job.proposal_hash, "matches"))
    show("Simulated readback", job)
    purchase = Job(Proposal(Action.PURCHASE, "fictional item", "fictional purchase"), review_required=False)
    purchase.assign("example worker")
    purchase.approve(Evidence(purchase.proposal_hash, "approved"))
    show("Purchase", purchase)
    lock = RefreshLock(stale_after=60)
    print("Refresh owner acquired:", lock.acquire("example-run", 0))
    print("Snapshot (all fictional):")
    print(json.dumps(make_snapshot([("Update", job), ("Purchase", purchase)],
                                   {"example source": False}), indent=2))


if __name__ == "__main__":
    main()
