#!/usr/bin/env python3
"""Validate submission data quality for NIEMS อปท. programs."""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(name: str) -> list | dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def validate_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return len(digits) in (9, 10)


def validate_submissions(submissions: list) -> list[dict]:
    issues = []
    for s in submissions:
        if not s.get("province") or "ไม่ระบุ" in s["province"]:
            issues.append({"id": s["id"], "field": "province", "message": "ไม่ระบุจังหวัด"})
        if s.get("phone") and not validate_phone(s["phone"]):
            issues.append({"id": s["id"], "field": "phone", "message": f"เบอร์โทรไม่ถูกต้อง: {s['phone']}"})
        if "โรงพยาบาล" in s.get("org_name", "") and s.get("unit_type") != "ระดับสูง":
            issues.append({"id": s["id"], "field": "org_name", "message": "โรงพยาบาลไม่ใช่ อปท."})
        if s.get("score") is None and s.get("unit_type") != "อำนวยการ":
            issues.append({"id": s["id"], "field": "score", "message": "ไม่ระบุคะแนน"})
    return issues


def main() -> int:
    submissions = load_json("submissions_standard_2569.json")
    known_issues = load_json("quality_issues.json")
    found = validate_submissions(submissions)

    print(f"ตรวจสอบ {len(submissions)} รายการ")
    print(f"พบปัญหาใหม่: {len(found)} รายการ")
    print(f"ปัญหาที่บันทึกไว้: {len(known_issues)} รายการ")

    if found:
        print("\n--- รายละเอียด ---")
        for issue in found:
            print(f"  #{issue['id']} [{issue['field']}] {issue['message']}")
        return 1

    print("✅ ไม่พบปัญหาเพิ่มเติม")
    return 0


if __name__ == "__main__":
    sys.exit(main())
