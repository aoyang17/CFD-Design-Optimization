"""Portable lookup and integrity checking for external research assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_ASSETS_ROOT = Path("/mnt/data2/aobo/CFD-Design-Optimization/assets")


class AssetError(RuntimeError):
    """Raised when an asset manifest or its requested asset is invalid."""


@dataclass(frozen=True)
class AssetRecord:
    """A single asset entry resolved against an external asset root."""

    asset_id: str
    path: Path
    sha256: str
    description: str


def repository_root() -> Path:
    """Return the root of the checked-out source repository."""
    return Path(__file__).resolve().parents[2]


def resolve_assets_root(assets_root: str | Path | None = None) -> Path:
    """Resolve the asset root using argument, environment, then project default."""
    if assets_root is not None:
        return Path(assets_root).expanduser().resolve()
    configured = os.environ.get("CFD_DO_ASSETS_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return DEFAULT_ASSETS_ROOT


def load_manifest(manifest: str | Path = "crm-v1") -> dict:
    """Load a tracked JSON manifest by name or explicit path."""
    candidate = Path(manifest)
    if not candidate.exists():
        candidate = repository_root() / "assets" / "manifests" / f"{manifest}.json"
    try:
        with candidate.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise AssetError(f"Asset manifest not found: {candidate}") from exc
    except json.JSONDecodeError as exc:
        raise AssetError(f"Invalid JSON manifest {candidate}: {exc}") from exc

    if data.get("schema_version") != 1 or not data.get("storage_subdirectory"):
        raise AssetError(f"Unsupported asset manifest schema: {candidate}")
    if not isinstance(data.get("assets"), dict):
        raise AssetError(f"Manifest has no assets mapping: {candidate}")
    return data


def asset_record(
    asset_id: str,
    *,
    manifest: str | Path = "crm-v1",
    assets_root: str | Path | None = None,
) -> AssetRecord:
    """Resolve an asset ID to its expected external filesystem location."""
    data = load_manifest(manifest)
    try:
        entry = data["assets"][asset_id]
    except KeyError as exc:
        choices = ", ".join(sorted(data["assets"]))
        raise AssetError(f"Unknown asset ID '{asset_id}'. Available: {choices}") from exc

    relative_path = Path(entry["relative_path"])
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise AssetError(f"Unsafe relative path for '{asset_id}': {relative_path}")
    expected = resolve_assets_root(assets_root) / data["storage_subdirectory"] / relative_path
    return AssetRecord(
        asset_id=asset_id,
        path=expected,
        sha256=entry["sha256"],
        description=entry.get("description", ""),
    )


def asset_path(asset_id: str, **kwargs: object) -> Path:
    """Return an existing asset path or raise a useful error."""
    record = asset_record(asset_id, **kwargs)
    if not record.path.is_file():
        raise AssetError(
            f"Asset '{asset_id}' is unavailable at {record.path}. "
            "Set CFD_DO_ASSETS_ROOT or pass --assets-root."
        )
    return record.path


def sha256sum(path: Path) -> str:
    """Calculate a file SHA-256 without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_assets(
    asset_ids: Iterable[str] | None = None,
    *,
    manifest: str | Path = "crm-v1",
    assets_root: str | Path | None = None,
) -> list[str]:
    """Return integrity errors; an empty list means every requested asset matches."""
    data = load_manifest(manifest)
    requested = list(asset_ids) if asset_ids else sorted(data["assets"])
    errors: list[str] = []
    for asset_id in requested:
        try:
            record = asset_record(asset_id, manifest=manifest, assets_root=assets_root)
        except AssetError as exc:
            errors.append(str(exc))
            continue
        if not record.path.is_file():
            errors.append(f"{asset_id}: missing ({record.path})")
        elif sha256sum(record.path) != record.sha256:
            errors.append(f"{asset_id}: SHA-256 mismatch ({record.path})")
    return errors


def main(argv: list[str] | None = None) -> int:
    """Run the asset lookup and verification command-line interface."""
    parser = argparse.ArgumentParser(description="Resolve CFD Design Optimization assets")
    parser.add_argument("--assets-root", help="override CFD_DO_ASSETS_ROOT")
    parser.add_argument("--manifest", default="crm-v1", help="manifest name or JSON path")
    subparsers = parser.add_subparsers(dest="command", required=True)
    path_parser = subparsers.add_parser("path", help="print an asset path")
    path_parser.add_argument("asset_id")
    verify_parser = subparsers.add_parser("verify", help="validate files against manifest checksums")
    verify_parser.add_argument("asset_ids", nargs="*")
    subparsers.add_parser("list", help="list manifest asset IDs")
    args = parser.parse_args(argv)

    try:
        if args.command == "path":
            print(asset_path(args.asset_id, manifest=args.manifest, assets_root=args.assets_root))
        elif args.command == "list":
            for asset_id in sorted(load_manifest(args.manifest)["assets"]):
                print(asset_id)
        else:
            errors = verify_assets(args.asset_ids, manifest=args.manifest, assets_root=args.assets_root)
            if errors:
                print("\n".join(errors))
                return 1
            print("All requested assets passed verification.")
    except AssetError as exc:
        print(f"error: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
