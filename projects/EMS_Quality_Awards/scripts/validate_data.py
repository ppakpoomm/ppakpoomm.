#!/usr/bin/env python3
"""Validate RSVP response data quality."""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def validate_phone(phone: str | None) -> bool:
    if not phone:
        return True
    digits = re.sub(r"\D", "", phone)
    return 9 <= len(digits) <= 10


def main() -> int:
    with open(DATA_DIR / "rsvp_responses.json", encoding="utf-8") as f:
        responses = json.load(f)
    with open(DATA_DIR / "summary.json", encoding="utf-8") as f:
        summary = json.load(f)

    issues: list[dict] = []

    for r in responses:
        if r["status"] == "award_winner":
            if not r.get("org_name"):
                issues.append({"id": r["id"], "field": "org_name", "message": "ไม่ระบุชื่อ อปท."})
            if not r.get("coordinator"):
                issues.append({"id": r["id"], "field": "coordinator", "message": "ไม่ระบุผู้ประสานงาน"})
            if not validate_phone(r.get("coordinator_phone")):
                issues.append({"id": r["id"], "field": "phone", "message": f"เบอร์โทรไม่ถูกต้อง: {r.get('coordinator_phone')}"})
            if not r.get("participation_mode"):
                issues.append({"id": r["id"], "field": "participation", "message": "ไม่ระบุรูปแบบการเข้าร่วม"})

    print(f"ตรวจสอบ {len(responses)} รายการ")
    print(f"อัตราตอบรับ: {summary['response_rate_pct']}% ({summary['awardees_responded']}/59)")
    print(f"พบปัญหาคุณภาฯข้อมูล: {len(issues)} รายการ")

    if issues:
        print("\n--- รายละเอียด ---")
        for issue in issues:
            print(f"  #{issue['id']} [{issue['field']}] {issue['message']}")
        return 1

    print("✅ ไม่พบปัญหาเพิ่มเติม")
    return 0


if __name__ == "__main__":
    sys.exit(main())
