"""Offline model of a coordinated task. Nothing here executes a real action."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib
import json


class Action(str, Enum):
    LOCAL = "local"
    SEND = "send"
    SCHEDULE = "schedule"
    PURCHASE = "purchase"
    DELETE = "permanent_delete"


@dataclass(frozen=True)
class Proposal:
    action: Action
    target: str
    content: str

    def fingerprint(self):
        if not isinstance(self.action, Action) or not self.target.strip() or not self.content.strip():
            raise ValueError("A known action, target, and content are required")
        data = json.dumps([self.action.value, self.target, self.content], ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass(frozen=True)
class Evidence:
    proposal_hash: str
    outcome: str


class Job:
    def __init__(self, proposal: Proposal, review_required: bool = True):
        self.proposal = proposal
        self.proposal_hash = proposal.fingerprint()
        self.review_required = review_required
        self.worker = None
        self.review = None
        self.approval = None
        self.handoff = None
        self.verified = False

    def assign(self, worker: str):
        if not worker.strip() or self.handoff:
            raise ValueError("Worker required before handoff")
        self.worker = worker

    def record_review(self, evidence: Evidence):
        if not self.worker or self.handoff or evidence.proposal_hash != self.proposal_hash:
            raise ValueError("Review must match the assigned proposal")
        if evidence.outcome not in ("pass", "hold"):
            raise ValueError("Unknown review outcome")
        self.review = evidence

    def approve(self, evidence: Evidence):
        if self.handoff or evidence.proposal_hash != self.proposal_hash or evidence.outcome != "approved":
            raise ValueError("Approval must match the proposal")
        self.approval = evidence

    def status(self):
        if self.proposal.fingerprint() != self.proposal_hash:
            return "proposal_changed"
        if self.verified:
            return "verified"
        if self.handoff:
            return "awaiting_readback"
        if not self.worker:
            return "awaiting_assignment"
        if self.review_required and (not self.review or self.review.outcome != "pass"):
            return "awaiting_review" if not self.review else "review_hold"
        if self.proposal.action is not Action.LOCAL and not self.approval:
            return "awaiting_approval"
        if self.proposal.action is Action.PURCHASE:
            return "owner_final_click"
        return "ready_for_simulation"

    def simulate_handoff(self):
        if self.status() != "ready_for_simulation":
            raise ValueError("Job is not ready")
        self.handoff = "simulated"

    def record_readback(self, evidence: Evidence):
        if not self.handoff or evidence.proposal_hash != self.proposal_hash or evidence.outcome != "matches":
            raise ValueError("Matching readback required")
        self.verified = True
