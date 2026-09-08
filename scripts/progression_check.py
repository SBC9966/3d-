"""Validate planned and delivered L1/L2/L3 building progression records.

This validates ancestry, declared upgrade deltas, budgets and recorded evidence.
It does not inspect GLB geometry or decide visual quality.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

DELTA_GROUPS = {
    "massing", "structure", "facade", "roof", "openings", "interior",
    "furniture", "materials", "props", "animation", "landscape", "performance"
}
ARCH_GROUPS = {"massing", "structure", "facade", "roof", "openings"}
DETAIL_GROUPS = {"interior", "furniture", "materials", "props", "animation", "landscape"}
SAFE_ID = re.compile(r"[a-z][a-z0-9-]{2,99}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive_int(value, name, allow_zero=False):
    minimum_ok = value >= 0 if allow_zero else value > 0
    require(type(value) is int and minimum_ok, name + " must be an integer " + (">= 0" if allow_zero else "> 0"))


def validate_plan(data):
    require(isinstance(data, dict), "progression must be an object")
    require(data.get("schemaVersion") == "1.0", "schemaVersion must be 1.0")
    for field in ("progressionId", "familyId"):
        value = data.get(field)
        require(isinstance(value, str) and SAFE_ID.fullmatch(value), field + " must be a safe lowercase ID")

    identity = data.get("identityLock")
    require(isinstance(identity, dict), "identityLock is required")
    signature = identity.get("signature")
    require(isinstance(signature, list) and len(signature) >= 2 and all(isinstance(x, str) and x.strip() for x in signature),
            "identityLock.signature needs at least two visible identity cues")
    preserve = identity.get("preserve", [])
    require(isinstance(preserve, list) and all(isinstance(x, str) and x.strip() for x in preserve),
            "identityLock.preserve must be a string list")

    policy = data.get("policy", {})
    min_groups = policy.get("minDeltaGroups", 4)
    positive_int(min_groups, "policy.minDeltaGroups")
    require(min_groups <= len(DELTA_GROUPS), "policy.minDeltaGroups is unrealistically high")
    require_arch = policy.get("requireArchitectureDelta", True)
    require_detail = policy.get("requireDetailDelta", True)
    require_growth = policy.get("requireTriangleGrowth", True)
    require(type(require_arch) is bool and type(require_detail) is bool and type(require_growth) is bool,
            "policy booleans are invalid")

    levels = data.get("levels")
    require(isinstance(levels, list) and len(levels) >= 2, "at least two progression levels are required")
    require([x.get("level") for x in levels] == list(range(1, len(levels) + 1)),
            "levels must be ordered and contiguous starting at 1")

    ids = [x.get("id") for x in levels]
    require(all(isinstance(x, str) and SAFE_ID.fullmatch(x) for x in ids), "every level needs a safe lowercase id")
    require(len(ids) == len(set(ids)), "duplicate level id")

    previous = None
    summaries = []
    for item in levels:
        level = item["level"]
        require(isinstance(item.get("role"), str) and item["role"].strip(), "level role is required")
        require(isinstance(item.get("specFile"), str) and item["specFile"].strip(), "specFile is required")
        deltas = item.get("deltas", {})
        require(isinstance(deltas, dict), "deltas must be an object")
        unknown = set(deltas) - DELTA_GROUPS
        require(not unknown, "unknown delta groups: " + ", ".join(sorted(unknown)))
        for group, changes in deltas.items():
            require(isinstance(changes, list) and changes and all(isinstance(x, str) and x.strip() for x in changes),
                    "delta group " + group + " must contain explicit change descriptions")

        budget = item.get("budget", {})
        require(isinstance(budget, dict), "budget must be an object")
        if "triangles" in budget:
            positive_int(budget["triangles"], "budget.triangles")
        if "textureResolution" in budget:
            positive_int(budget["textureResolution"], "budget.textureResolution")

        if level == 1:
            require(item.get("parentId") is None, "L1 parentId must be null")
        else:
            require(item.get("parentId") == previous["id"], "each child must inherit from the immediately previous level")
            groups = set(deltas)
            require(len(groups) >= min_groups,
                    "L" + str(level) + " changes only " + str(len(groups)) + " groups; minimum is " + str(min_groups))
            if require_arch:
                require(bool(groups & ARCH_GROUPS), "L" + str(level) + " needs an architectural delta")
            if require_detail:
                require(bool(groups & DETAIL_GROUPS), "L" + str(level) + " needs a detail/content delta")
            if require_growth and "triangles" in budget and "triangles" in previous.get("budget", {}):
                require(budget["triangles"] > previous["budget"]["triangles"],
                        "L" + str(level) + " triangle budget must exceed its parent when requireTriangleGrowth is true")

        summaries.append({"level": level, "id": item["id"], "deltaGroups": sorted(deltas)})
        previous = item

    return {
        "progressionId": data["progressionId"],
        "familyId": data["familyId"],
        "levels": len(levels),
        "planValid": True,
        "summary": summaries,
        "policy": {
            "minDeltaGroups": min_groups,
            "requireArchitectureDelta": require_arch,
            "requireDetailDelta": require_detail,
            "requireTriangleGrowth": require_growth,
        },
    }


def validate_delivery(data, root=None):
    result = validate_plan(data)
    policy = result["policy"]
    previous = None

    for item in data["levels"]:
        level = item["level"]
        actual = item.get("actual")
        require(isinstance(actual, dict), "L" + str(level) + " needs actual delivery metrics")
        require(isinstance(actual.get("geometrySignature"), str) and actual["geometrySignature"].strip(),
                "L" + str(level) + " geometrySignature is required")
        require(isinstance(actual.get("massingSignature"), str) and actual["massingSignature"].strip(),
                "L" + str(level) + " massingSignature is required")

        for key in ("triangleCount", "namedPartCount", "materialCount"):
            positive_int(actual.get(key), "L" + str(level) + ".actual." + key)
        for key in ("textureCount", "maxTextureResolution", "furnitureCount", "animatablePartCount"):
            positive_int(actual.get(key), "L" + str(level) + ".actual." + key, allow_zero=True)

        evidence = actual.get("previewEvidence")
        require(isinstance(evidence, list) and len(evidence) >= 3 and all(isinstance(x, str) and x.strip() for x in evidence),
                "L" + str(level) + " needs at least three model-render previewEvidence paths")
        if root is not None:
            for rel in evidence:
                path = (root / rel).resolve()
                require(path.is_relative_to(root.resolve()), "preview evidence escapes the job root: " + rel)
                require(path.is_file() and path.stat().st_size > 0, "missing preview evidence: " + rel)

        if level > 1:
            parent = previous["actual"]
            require(actual["geometrySignature"] != parent["geometrySignature"],
                    "L" + str(level) + " has the same geometrySignature as its parent")
            changed = actual.get("changedComponents")
            require(isinstance(changed, list) and changed and all(isinstance(x, str) and x.strip() for x in changed),
                    "L" + str(level) + " needs changedComponents evidence")
            groups = set(item.get("deltas", {}))

            if policy["requireTriangleGrowth"]:
                require(actual["triangleCount"] > parent["triangleCount"],
                        "L" + str(level) + " triangleCount did not grow")
            if "massing" in groups:
                require(actual["massingSignature"] != parent["massingSignature"],
                        "L" + str(level) + " declares massing changes but massingSignature did not change")
            if "furniture" in groups:
                require(actual["furnitureCount"] > parent["furnitureCount"],
                        "L" + str(level) + " declares furniture changes but furnitureCount did not grow")
            if "animation" in groups:
                require(actual["animatablePartCount"] > parent["animatablePartCount"],
                        "L" + str(level) + " declares animation changes but animatablePartCount did not grow")
            if "materials" in groups:
                improved = (
                    actual["materialCount"] > parent["materialCount"]
                    or actual["textureCount"] > parent["textureCount"]
                    or actual["maxTextureResolution"] > parent["maxTextureResolution"]
                )
                require(improved, "L" + str(level) + " declares material changes without recorded material/texture improvement")

        previous = item

    result["deliveryValid"] = True
    result["note"] = "Record/evidence validation only; GLB inspection and matched-camera visual QA remain required."
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("progression", type=Path)
    parser.add_argument("--mode", choices=("plan", "delivery"), default="plan")
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.progression.read_text())
        result = validate_plan(data) if args.mode == "plan" else validate_delivery(data, args.root)
        print(json.dumps(result, indent=2))
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
        sys.exit("Progression invalid: " + str(error) + "\n")


if __name__ == "__main__":
    main()
