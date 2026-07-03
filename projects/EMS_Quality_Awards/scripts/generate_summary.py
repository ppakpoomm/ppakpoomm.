#!/usr/bin/env python3
"""Generate summary report from RSVP tracking data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    with open(DATA_DIR / "summary.json", encoding="utf-8") as f:
        summary = json.load(f)
    with open(DATA_DIR / "rsvp_responses.json", encoding="utf-8") as f:
        responses = json.load(f)

    print("=" * 55)
    print("EMS Quality Awards — อปท.มาตรฐาน 2569")
    print(summary["event"])
    print("=" * 55)

    print(f"\n📊 สรุปการตอบรับ (ณ {summary['as_of']})")
    print(f"  อปท. ได้รับรางวัล:     {summary['expected_awardees']} แห่ง")
    print(f"  ตอบรับแล้ว:           {summary['awardees_responded']} แห่ง ({summary['response_rate_pct']}%)")
    print(f"  ยังไม่ตอบรับ:         {summary['pending_awardees']} แห่ง ⚠️")
    print(f"  แจ้งไม่เข้าร่วม:      {summary['by_status'].get('declined', 0)} แห่ง")
    print(f"  ออกนิทรรศการ:        {summary['by_status'].get('exhibitor', 0)} แห่ง")

    print("\n--- รูปแบบการเข้าร่วม ---")
    for mode, count in summary.get("by_participation", {}).items():
        label = "โล่ + นิทรรศการ" if mode == "trophy_and_exhibition" else "โล่เท่านั้น"
        print(f"  {label}: {count}")

    print("\n--- ประเภทหน่วยปฏิบัติการ (ผู้ได้รางวัล) ---")
    for ut, count in summary.get("by_unit_type", {}).items():
        print(f"  {ut}: {count}")

    print("\n--- การเดินทาง ---")
    for tm, count in summary.get("by_travel_mode", {}).items():
        print(f"  {tm}: {count}")

    print(f"\n🏨 ขอที่พักจาก อบจ.กระบี่: {summary['accommodation_requests']} รายการ")
    print(f"📍 จังหวัดที่ตอบรับ: {summary['provinces_responded']} จังหวัด")

    declined = [r for r in responses if r["status"] == "declined"]
    if declined:
        print("\n--- ไม่เข้าร่วม ---")
        for r in declined:
            print(f"  • {r.get('declined_org', '—')}: {r.get('declined_reason', '—')}")


if __name__ == "__main__":
    main()
