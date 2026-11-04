"""Build a status projection from supplied fictional state, never from connectors."""


def make_snapshot(jobs, sources):
    """sources maps source names to availability booleans; no source data is fetched."""
    return {
        "jobs": [{"label": label, "status": job.status()} for label, job in jobs],
        "source_gaps": sorted(name for name, available in sources.items() if not available),
    }
