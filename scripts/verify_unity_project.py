#!/usr/bin/env python3
"""Mechanical Unity project/package integrity check; does not launch the Unity Editor."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNITY = ROOT / "unity"
CORE = ROOT / "src" / "core"
checks: dict[str, bool] = {}

def require(name: str, condition: bool) -> None:
    checks[name] = bool(condition)
    if not condition:
        print(f"FAIL {name}")

version_text = (UNITY / "ProjectSettings" / "ProjectVersion.txt").read_text(encoding="utf-8")
require("unity_editor_is_security_patched_6000_3", "m_EditorVersion: 6000.3.27f2" in version_text)
require("unity_revision_matches_editor", "m_EditorVersionWithRevision: 6000.3.27f2 (22188f149405)" in version_text)

manifest = json.loads((UNITY / "Packages" / "manifest.json").read_text(encoding="utf-8"))
dependencies = manifest.get("dependencies", {})
require("urp_dependency_pinned", dependencies.get("com.unity.render-pipelines.universal") == "17.3.0")
local_core = dependencies.get("com.d1traverser.game-core", "")
require("core_package_uses_local_path", local_core == "file:../src/core")
resolved_core = (UNITY / local_core.removeprefix("file:")).resolve()
require("local_core_path_resolves", resolved_core == CORE.resolve())

package = json.loads((CORE / "package.json").read_text(encoding="utf-8"))
require("local_package_name_matches_manifest", package.get("name") == "com.d1traverser.game-core")
require("local_package_targets_unity_6000_3", package.get("unity") == "6000.3")

asmdef = json.loads((CORE / "Runtime" / "Game.Core.asmdef").read_text(encoding="utf-8"))
require("core_assembly_is_engine_independent", asmdef.get("noEngineReferences") is True)
require("core_assembly_name_matches", asmdef.get("name") == "Game.Core")

project = ET.parse(CORE / "Game.Core.csproj").getroot()
target_framework = project.findtext("./PropertyGroup/TargetFramework")
require("core_targets_netstandard_2_1", target_framework == "netstandard2.1")

runtime_sources = list((CORE / "Runtime").rglob("*.cs"))
require("core_runtime_sources_present", len(runtime_sources) >= 7)
uses_unity = any("using UnityEngine" in p.read_text(encoding="utf-8") for p in runtime_sources)
require("core_runtime_has_no_unityengine_dependency", not uses_unity)

assets_readme = UNITY / "Assets" / "README.md"
require("unity_assets_root_present", assets_readme.exists())
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
for name, pattern in (
    ("Library", "[Ll]ibrary/"),
    ("Temp", "[Tt]emp/"),
    ("Obj", "[Oo]bj/"),
    ("Builds", "[Bb]uilds/"),
):
    require(f"gitignore_{name}", pattern in gitignore)

result = {
    "pass": all(checks.values()),
    "passed": sum(1 for ok in checks.values() if ok),
    "total": len(checks),
    "checks": checks,
    "limitations": [
        "Does not launch Unity Editor or prove package resolution.",
        "Does not verify generated URP pipeline assets, scenes, native build, runtime, multiplayer, art/audio, or performance."
    ]
}
print(json.dumps(result, indent=2))
sys.exit(0 if result["pass"] else 1)
