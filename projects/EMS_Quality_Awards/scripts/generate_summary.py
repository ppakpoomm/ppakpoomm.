#!/usr/bin/env python3
"""Generate summary report from master tracker data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    with open(DATA_DIR / "summary.json", encoding="utf-8") as f:
        summary = json.load(f)
    with open(DATA_DIR / "pending_followup.json", encoding="utf-8") as f:
        pending = json.load(f)

    print("=" * 55)
    print("EMS Quality Awards — อปท.มาตรฐาน 2569")
    print(summary["event"])
    print("=" * 55)

    print(f"\n📊 สรุปการตอบรับ (ณ {summary['as_of']})")
    print(f"  อปท. ได้รับรางวัล:     {summary['total_awardees']} แห่ง")
    print(f"  ตอบรับแล้ว:           {summary['responded_count']} แห่ง ({summary['response_rate_pct']}%)")
    print(f"  ยังไม่ตอบรับ:         {summary['pending_count']} แห่ง ⚠️")
    print(f"  แจ้งไม่เข้าร่วม:      {summary['declined_count']} แห่ง")

    print("\n--- ประเภทรางวัล ---")
    for award_type, count in summary.get("by_award_type", {}).items():
        print(f"  {award_type}: {count}")

    print("\n--- รูปแบบการเข้าร่วม (ที่ระบุแล้ว) ---")
    for mode, count in summary.get("by_participation_mode", {}).items():
        label = "โล่ + นิทรรศการ" if mode == "trophy_and_exhibition" else "โล่เท่านั้น"
        print(f"  {label}: {count}")

    print(f"\n📞 มีเบอร์โทร: {summary['with_phone']}/{summary['total_awardees']}")
    print(f"📧 มีอีเมล: {summary['with_email']}/{summary['total_awardees']}")

    print(f"\n⚠️  จังหวัดที่ยังไม่ตอบรับ: {len(summary.get('by_province_pending', {}))} จังหวัด")
    for province, count in sorted(summary.get("by_province_pending", {}).items()):
        print(f"  {province}: {count}")

    no_email = [p for p in pending if not p.get("email")]
    if no_email:
        print(f"\n--- ยังไม่ตอบรับและไม่มีอีเมล ({len(no_email)} แห่ง) ---")
        for p in no_email[:10]:
            print(f"  • #{p.get('code')} {p.get('org_name')} ({p.get('province')})")
        if len(no_email) > 10:
            print(f"  ... และอีก {len(no_email) - 10} แห่ง")


if __name__ == "__main__":
    main()
