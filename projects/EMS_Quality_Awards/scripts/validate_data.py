#!/usr/bin/env python3
"""Validate master tracker data quality."""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def validate_phone(phone: str | None) -> bool:
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    return 9 <= len(digits) <= 10


def main() -> int:
    with open(DATA_DIR / "awardees.json", encoding="utf-8") as f:
        awardees = json.load(f)
    with open(DATA_DIR / "summary.json", encoding="utf-8") as f:
        summary = json.load(f)

    issues: list[dict] = []

    for a in awardees:
        code = a.get("code", "?")
        if not a.get("org_name"):
            issues.append({"code": code, "field": "org_name", "message": "ไม่ระบุชื่อ อปท."})
        if a["form_status"] == "pending" and not validate_phone(a.get("phone")):
            issues.append({"code": code, "field": "phone", "message": f"ไม่มีเบอร์โทร: {a.get('phone')}"})
        if a["form_status"] == "responded" and not a.get("participation_mode"):
            issues.append({"code": code, "field": "participation", "message": "ตอบรับแล้วแต่ยังไม่ระบุรูปแบบการเข้าร่วม"})

    print(f"ตรวจสอบ {len(awardees)} อปท.")
    print(
        f"อัตราตอบรับ: {summary['response_rate_pct']}% "
        f"({summary['responded_count']}/{summary['total_awardees']})"
    )
    print(f"ยังไม่ตอบรับ: {summary['pending_count']} แห่ง")
    print(f"พบปัญหาคุณภาพข้อมูล: {len(issues)} รายการ")

    if issues:
        print("\n--- รายละเอียด (สูงสุด 20) ---")
        for issue in issues[:20]:
            print(f"  #{issue['code']} [{issue['field']}] {issue['message']}")
        if len(issues) > 20:
            print(f"  ... และอีก {len(issues) - 20} รายการ")
        return 1

    print("✅ ไม่พบปัญหาเพิ่มเติม")
    return 0


if __name__ == "__main__":
    sys.exit(main())
