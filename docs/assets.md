# External asset setup

Code and manifests live in this repository. CFD meshes, training data, model checkpoints, and generated outputs live outside Git.

## Default storage location

The default external root is:

```text
/mnt/data2/aobo/CFD-Design-Optimization/assets
```

The tracked [`crm-v1.json`](../assets/manifests/crm-v1.json) manifest resolves each asset below that root. The initial `crm-v1` installation contains `crm_ffd`, `crm_modes`, `crm_bounds_standard`, and `crm_bounds_multifidelity`.

## Portable configuration

Use one of these mechanisms, in priority order:

```bash
# One command invocation
cfd-do-assets --assets-root /scratch/my-assets verify

# Shell/session setting
export CFD_DO_ASSETS_ROOT=/scratch/my-assets
cfd-do-assets verify
```

Python code must request an asset ID rather than construct a filesystem path:

```python
from cfd_design_opt.assets import asset_path

ffd_file = asset_path("crm_ffd")
```

## Integrity checks

Run the following before a CFD, training, or optimization workflow:

```bash
cfd-do-assets verify
cfd-do-assets path crm_ffd
```

`verify` checks both presence and SHA-256. Add a new asset by first placing it under the external root, calculating its checksum, and then adding its ID, relative path, provenance, and checksum to a manifest. Never commit machine-specific absolute paths to a case configuration.
