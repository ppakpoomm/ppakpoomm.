#!/usr/bin/env python3
"""
Sync RSVP data from Google Spreadsheet export (xlsx).

Usage:
  python3 scripts/sync_from_sheet.py /path/to/export.xlsx

Or set SHEET_URL and download via gdown first:
  gdown "https://drive.google.com/uc?id=1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo" -O /tmp/tracker.xlsx
  python3 scripts/sync_from_sheet.py /tmp/tracker.xlsx
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SHEET_NAME = "Form Responses 3"
SPREADSHEET_ID = "1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo"

COLS = {
    "timestamp": "Timestamp",
    "respondent_type": "ประเภทผู้ตอบรับ",
    "participation_mode": "รูปแบบการเข้าร่วม",
    "org_select": "ชื่อองค์กรปกครองส่วนท้องถิ่น (เลือกจากรายชื่อ ๕๙ แห่ง)",
    "unit_type": "ประเภทหน่วยปฏิบัติการที่ได้รับรางวัล",
    "coordinator": "ชื่อ-สกุล ผู้ประสานงาน",
    "coordinator_phone": "เบอร์โทรศัพท์มือถือผู้ประสานงาน",
    "trophy_recipient": "ชื่อ-สกุล ผู้รับมอบโล่รางวัล",
    "province": "จังหวัด",
    "org_name_free": "ชื่อหน่วยงาน",
    "travel_mode": "รูปแบบการเดินทาง",
    "travel_detail": "รายละเอียดการเดินทาง / ต้นทาง",
    "accommodation": "ความต้องการที่พักจาก อบจ.กระบี่",
    "declined_org": "ชื่อ อปท. ที่แจ้งไม่เข้าร่วม",
    "declined_reason": "เหตุผลที่ไม่สามารถเข้าร่วมได้ (โดยสังเขป)",
    "declined_contact": "ชื่อ-สกุล ผู้ประสานงาน และเบอร์โทรศัพท์",
    "booth_staff_1": "ชื่อ-สกุล เจ้าหน้าที่ประจำบูธนิทรรศการ คนที่ 1",
    "booth_staff_2": "ชื่อ-สกุล เจ้าหน้าที่ประจำบูธนิทรรศการ คนที่ 2",
}


def parse_org(value: object) -> tuple[str | None, str | None, str | None]:
    if pd.isna(value) or not str(value).strip():
        return None, None, None
    text = str(value).strip()
    match = re.match(r"(\d+)\s*\|\s*(.+?)\s*\|\s*(.+)", text)
    if match:
        return match.group(1), match.group(2).strip(), match.group(3).strip()
    return None, text, None


def classify_status(row: pd.Series) -> str:
    declined_org = str(row.get(COLS["declined_org"], "") or "").strip()
    if declined_org:
        return "declined"

    respondent_type = str(row.get(COLS["respondent_type"], "") or "")
    if "ไม่เข้าร่วม" in respondent_type:
        return "declined"
    if "ไม่ได้รับรางวัล" in respondent_type or "ออกนิทรรศการ" in respondent_type:
        return "exhibitor"
    if "ได้รับรางวัล" in respondent_type:
        return "award_winner"
    return "unknown"


def classify_participation(row: pd.Series) -> str | None:
    mode = str(row.get(COLS["participation_mode"], "") or "")
    if "ไม่จัดนิทรรศการ" in mode or "โล่รางวัลเท่านั้น" in mode:
        return "trophy_only"
    if "จัดแสดงนิทรรศการ" in mode or "นิทรรศการ" in mode:
        return "trophy_and_exhibition"
    return None


def simplify_unit_type(unit_type: str | None) -> str | None:
    if not unit_type:
        return None
    if "พื้นฐาน" in unit_type:
        return "ระดับพื้นฐาน"
    if "สูง" in unit_type:
        return "ระดับสูง"
    if "อำนวยการ" in unit_type:
        return "อำนวยการดีเด่น"
    return unit_type


def cell_str(row: pd.Series, key: str) -> str | None:
    value = row.get(COLS[key])
    if pd.isna(value):
        return None
    return str(value).strip()


def parse_records(df: pd.DataFrame) -> list[dict]:
    records: list[dict] = []
    seen: set[tuple] = set()

    for _, row in df.iterrows():
        if pd.isna(row.get(COLS["timestamp"])):
            continue

        code, org_name, province = parse_org(row.get(COLS["org_select"]))
        if not org_name:
            org_name = cell_str(row, "org_name_free")
        if not province:
            province = cell_str(row, "province")

        status = classify_status(row)
        timestamp = str(row.get(COLS["timestamp"]))
        dedupe_key = (timestamp, org_name, status)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        records.append({
            "id": len(records) + 1,
            "timestamp": timestamp,
            "status": status,
            "participation_mode": classify_participation(row),
            "org_code": code,
            "org_name": org_name,
            "province": province,
            "unit_type": simplify_unit_type(cell_str(row, "unit_type")),
            "coordinator": cell_str(row, "coordinator"),
            "coordinator_phone": cell_str(row, "coordinator_phone"),
            "trophy_recipient": cell_str(row, "trophy_recipient"),
            "travel_mode": cell_str(row, "travel_mode"),
            "travel_detail": cell_str(row, "travel_detail"),
            "accommodation_request": "อบจ.กระบี่" in str(row.get(COLS["accommodation"], "") or ""),
            "declined_org": cell_str(row, "declined_org"),
            "declined_reason": cell_str(row, "declined_reason"),
            "declined_contact": cell_str(row, "declined_contact"),
            "booth_staff_1": cell_str(row, "booth_staff_1"),
            "booth_staff_2": cell_str(row, "booth_staff_2"),
        })

    return records


def build_summary(records: list[dict]) -> dict:
    expected_awardees = 59
    award_winners = [r for r in records if r["status"] == "award_winner"]
    unique_codes = {r["org_code"] for r in award_winners if r["org_code"]}
    responded = len(unique_codes)

    return {
        "program": "อปท.มาตรฐาน พ.ศ. 2569",
        "event": "ประชุมวิชาการการแพทย์ฉุกเฉินในองค์กรปกครองส่วนท้องถิ่นระดับชาติ ครั้งที่ 10",
        "as_of": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "total_form_submissions": len(records),
        "expected_awardees": expected_awardees,
        "awardees_responded": responded,
        "response_rate_pct": round(responded / expected_awardees * 100, 1),
        "by_status": dict(Counter(r["status"] for r in records)),
        "by_participation": dict(Counter(r["participation_mode"] for r in records if r["participation_mode"])),
        "by_unit_type": dict(Counter(r["unit_type"] for r in award_winners if r["unit_type"])),
        "by_travel_mode": dict(Counter(r["travel_mode"] for r in records if r["travel_mode"])),
        "provinces_responded": len({r["province"] for r in records if r["province"]}),
        "accommodation_requests": sum(1 for r in records if r["accommodation_request"]),
        "pending_awardees": expected_awardees - responded,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: sync_from_sheet.py <path-to-xlsx>")
        print(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
        return 1

    xlsx_path = Path(sys.argv[1])
    if not xlsx_path.exists():
        print(f"File not found: {xlsx_path}")
        return 1

    df = pd.read_excel(xlsx_path, sheet_name=SHEET_NAME).dropna(how="all")
    records = parse_records(df)
    summary = build_summary(records)

    (DATA_DIR / "rsvp_responses.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    expected = summary.get("expected_awardees", 59)
    print(f"✅ Synced {len(records)} records from {SHEET_NAME}")
    print(f"   อัตราตอบรับ: {summary['response_rate_pct']}% ({summary['awardees_responded']}/{expected})")


if __name__ == "__main__":
    sys.exit(main())
