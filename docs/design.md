# Design notes and provenance

## Source map

| Concept | Private source inspected | This repository |
| --- | --- | --- |
| Refresh ownership | Private refresh coordination: owner run ID, heartbeat, stale takeover, ownership checks, guarded file writes | `refresh_lock.py` adapts the same decision pattern into an in-memory object; mode, JSON output, persistent files, file locks, atomic writes and ID generation are removed. Callers provide time and run ID. |
| Snapshot and visibility | Earlier dashboard documentation: collected data, gaps, status, versioned write and readback | `snapshot.py` is newly written and projects only fictional job states and named source gaps. It does not collect or publish data, deduplicate entries, use versions, or establish freshness. |
| Review and approval | Private review and coordination rules: separate review from action approval, preserve review evidence and bind final decisions | `coordination.py` is newly written. Its content hash and state transitions are a teaching design, not a claim that all private workflows implement these exact types or states. |
| Test approach | Private HQ test README: mock connectors and refuse unexpected tool calls or network egress | Tests here use only local in-memory fakes. They do not reproduce the browser harness or test network interception. |

The source descriptions identify the concepts without disclosing private file locations. No code or assets from third parties were included. The owner/heartbeat/takeover code is an adaptation of first-party source, substantially reduced and rewritten for a single process. No other code is copied from the private system. Licensing and attribution remain a release decision.

## Walkthrough and limits

A proposal identifies an action, target and content. Its deterministic fingerprint binds illustrative review, approval and readback records to the content. A changed proposal stops progress. An assigned worker and passing review are required when configured. Non-local actions need matching approval; purchases end at the owner's final click. A local state change records a simulated handoff without invoking a callback, then a separate matching readback changes the displayed state to verified. The snapshot shows job status and unavailable sources; it is a projection, not proof that a real source was checked.

The private lock actually uses a filesystem guard and ownership token. The sample's lock has neither cross-process synchronization nor persistence, and its caller-supplied clock and identifiers are untrusted. Checks are not atomic with any write. It illustrates stale-owner fencing only, and cannot protect real work. The demo does not implement actual independent review, human approval provenance, revocation, authentication, tamper resistance, source retrieval, timestamps, reconciliation, recovery, or real readback. Its `verified` status means only the sample accepted a simulated matching record. All example text and identities are fictional.

No live dashboard or data, private paths, IDs, connector settings, accounts, messages, personal details, credentials, third-party personal information, or Git history are packaged.
