# Model Registry

- `active/`: currently deployed model artifact.
- `archive/`: previous validated versions for rollback.

Rollback policy:
If active model degrades KPI, restore last stable model from archive.