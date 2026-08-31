import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cfd_design_opt.assets import AssetError, asset_path, verify_assets


class AssetResolverTests(unittest.TestCase):
    def test_resolves_and_verifies_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            payload = b"test asset\n"
            asset_file = temporary_root / "store" / "geometry" / "asset.txt"
            asset_file.parent.mkdir(parents=True)
            asset_file.write_bytes(payload)
            manifest = temporary_root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "storage_subdirectory": "store",
                        "assets": {
                            "example": {
                                "relative_path": "geometry/asset.txt",
                                "sha256": hashlib.sha256(payload).hexdigest(),
                            }
                        },
                    }
                )
            )
            self.assertEqual(asset_path("example", manifest=manifest, assets_root=temporary_root), asset_file)
            self.assertEqual(verify_assets(manifest=manifest, assets_root=temporary_root), [])

    def test_reports_missing_asset(self) -> None:
        with self.assertRaises(AssetError):
            asset_path("crm_ffd", assets_root="/tmp/definitely-missing-cfd-assets")
