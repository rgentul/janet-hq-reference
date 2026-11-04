# Janet HQ: coordination, trust, and a useful view of work

Janet HQ is a personal operating system for working with AI agents. Its dashboard is the visible surface; the more interesting product challenge is deciding who can do what, what needs a person's approval, and what evidence makes a status trustworthy.

This repository contains an **offline teaching model**, not the private system. Run a fictional job through assignment, independent review, exact-scope approval, a simulated handoff, and readback. Then see how a status snapshot reports the result and any source gaps. There are no external services, agents, real people, or actions in the demonstration.

```text
Request → assign a worker → review → owner approval → simulated handoff → readback → status snapshot
                    evidence is bound to the proposal's content ↑
```

## Run it

Python 3.9+; standard library only:

```sh
python3 demo.py
python3 -m unittest discover -s tests -v
```

All examples are fictional. The demo prints a staged timeline and a JSON snapshot. The handoff is an in-memory state change: it accepts no action callback and does not send, schedule, purchase, delete, or publish anything. The tests exercise mismatched approvals, rejected review, changed proposals, failed readback, source gaps, and refresh ownership takeover.

## Explore the design

| File | What it shows |
| --- | --- |
| `coordination.py` | Illustrative job lifecycle, content-bound evidence and simulated execution |
| `refresh_lock.py` | Simplified in-memory adaptation of the private refresh lock's owner, heartbeat and takeover logic |
| `snapshot.py` | Fictional dashboard view with explicit source gaps |
| `demo.py` | Complete fictional walkthrough |
| `tests/` | Behavioral tests |
| `docs/design.md` | Source map, real-versus-illustrative boundary and limits |

The private system uses a refresh lock to prevent overlapping runs from writing as the same owner. The adapted example uses the same core ownership, heartbeat, stale takeover and old-owner check ideas, but is in memory only. The lifecycle, fake execution, snapshot, and examples are newly written illustrations of documented operating concepts, not production code. See [design notes](docs/design.md) for exact distinctions.

## Trust boundaries

A review is not owner approval. Approval matches the exact proposal content and does not carry to a changed proposal. Purchase handoff belongs to the owner even when the rest of the model's checks pass. The private system's deletion, sending and other rules have additional human and operational requirements; this model is not a complete policy implementation.

The model cannot authenticate the owner or reviewer, establish reviewer independence, securely store or expire approval, enforce permissions on real tools, coordinate processes, or prove an external action happened. Caller-provided readback is simulated. **Do not use it as an authorization or execution layer.**

No private dashboard, live integrations, messages, personal records, credentials, account identifiers, third-party personal data, or Git history are included.

## License

No license has been selected or granted for this candidate. A repository can be publicly readable without a license; an open-source license would grant reuse permissions under its terms. Attribution and any license choice remain to be resolved.
