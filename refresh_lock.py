"""In-memory teaching adaptation of refresh owner/heartbeat/takeover logic.

The real lock uses a file guard and atomic file replacement; this example is
single-process and has no interprocess exclusion or durable storage.
"""


class RefreshLock:
    def __init__(self, stale_after):
        if stale_after <= 0:
            raise ValueError("stale_after must be positive")
        self.stale_after = stale_after
        self.owner = None
        self.heartbeat_at = None

    def acquire(self, run_id, now):
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("run_id required")
        if self.owner and self.owner != run_id and now - self.heartbeat_at < self.stale_after:
            return False
        self.owner, self.heartbeat_at = run_id, now
        return True

    def check(self, run_id):
        return bool(run_id and self.owner == run_id)

    def heartbeat(self, run_id, now):
        if not self.check(run_id):
            return False
        self.heartbeat_at = now
        return True

    def release(self, run_id):
        if not self.check(run_id):
            return False
        self.owner, self.heartbeat_at = None, None
        return True
