#!/usr/bin/env python3
"""Generate summary report for NIEMS อปท. selection programs."""

import json
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    with open(DATA_DIR / "submissions_standard_2569.json", encoding="utf-8") as f:
        submissions = json.load(f)
    with open(DATA_DIR / "status_standard_2569.json", encoding="utf-8") as f:
        status = json.load(f)

    provinces = Counter(s["province"] for s in submissions)
    unit_types = Counter(s["unit_type"] for s in submissions)
    scores = [s["score"] for s in submissions if s["score"] is not None]

    print("=" * 50)
    print("NIEMS อปท.มาตรฐาน พ.ศ. 2569 — สรุปผล")
    print("=" * 50)
    print(f"\n📊 จำนวนรายการทั้งหมด: {len(submissions)}")
    print(f"📍 จำนวนจังหวัด: {len(provinces)}")
    print(f"📝 กรอกฟอร์ม: {status['metrics']['total_form_submissions']} อปท.")
    print(f"✅ ครบทั้งหนังสือ+ฟอร์ม: {status['metrics']['provinces_complete_both']} จังหวัด")
    print(f"⚠️  มีหนังสือแต่ไม่กรอกฟอร์ม: {status['metrics']['provinces_letter_only']} จังหวัด")
    print(f"⚠️  กรอกฟอร์มแต่ไม่ส่งหนังสือ: {status['metrics']['provinces_form_only']} จังหวัด")

    print("\n--- ประเภทหน่วยปฏิบัติการ ---")
    for ut, count in unit_types.most_common():
        print(f"  {ut}: {count}")

    if scores:
        print(f"\n--- คะแนน ---")
        print(f"  เฉลี่ย: {sum(scores)/len(scores):.1f}")
        print(f"  สูงสุด: {max(scores)}")
        print(f"  ต่ำสุด: {min(scores)}")

    print(f"\n--- จังหวัดที่ต้องติดตาม (มีหนังสือ ไม่กรอกฟอร์ม) ---")
    for p in status["provinces_letter_only"]:
        print(f"  • {p}")


if __name__ == "__main__":
    main()
