#!/usr/bin/env python3
"""
Sync EMS Quality Awards tracker from master Google Spreadsheet (xlsx).

Usage:
  python3 scripts/sync_from_sheet.py /path/to/export.xlsx

Or download first:
  gdown "https://drive.google.com/uc?id=1MqAI8v3dkFFzlTIQnkEDLT_zGQFHrt9u" -O /tmp/ems-tracker.xlsx
  python3 scripts/sync_from_sheet.py /tmp/ems-tracker.xlsx
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MASTER_SPREADSHEET_ID = "1MqAI8v3dkFFzlTIQnkEDLT_zGQFHrt9u"
FORM_SPREADSHEET_ID = "1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo"

SHEETS = {
    "all": "สรุปทั้งหมด",
    "pending": "ยังไม่ตอบรับ",
    "responded": "ตอบรับแล้ว",
    "form_raw": "จากฟอร์มดิบ",
}

COLS = {
    "code": "ลำดับ",
    "org_name": "ชื่ออปท",
    "province": "จังหวัด",
    "award_type": "ประเภทรางวัล",
    "coordinator": "ผู้ประสานงาน",
    "phone": "โทร",
    "email": "อีเมล",
    "form_status_label": "สถานะฟอร์ม",
    "participation_route": "เส้นทาง",
    "trophy_recipient": "ผู้รับโล่",
    "booth_staff_1": "บูธ1",
    "booth_staff_2": "บูธ2",
    "follow_up_by": "ผู้ติดตาม",
    "notes": "หมายเหตุ",
    "data_source": "แหล่งข้อมูล",
}


def cell_str(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def normalize_code(value: object) -> str | None:
    text = cell_str(value)
    if not text:
        return None
    digits = re.sub(r"\D", "", text)
    return digits.zfill(3) if digits else text


def classify_form_status(label: str | None) -> str:
    if not label:
        return "unknown"
    if "ยังไม่ตอบรับ" in label:
        return "pending"
    if "ไม่เข้าร่วม" in label:
        return "declined"
    if "ตอบรับแล้ว" in label:
        return "responded"
    return "unknown"


def classify_participation_mode(route: str | None) -> str | None:
    if not route:
        return None
    upper = route.upper()
    if "WINNER_FULL" in upper:
        return "trophy_and_exhibition"
    if "WINNER_AWARD_ONLY" in upper or "AWARD-ONLY" in upper:
        return "trophy_only"
    return None


def row_to_record(row: pd.Series) -> dict:
    label = cell_str(row.get(COLS["form_status_label"]))
    route = cell_str(row.get(COLS["participation_route"])) or ""

    return {
        "code": normalize_code(row.get(COLS["code"])),
        "org_name": cell_str(row.get(COLS["org_name"])),
        "province": cell_str(row.get(COLS["province"])),
        "award_type": cell_str(row.get(COLS["award_type"])),
        "coordinator": cell_str(row.get(COLS["coordinator"])),
        "phone": cell_str(row.get(COLS["phone"])),
        "email": cell_str(row.get(COLS["email"])),
        "form_status": classify_form_status(label),
        "form_status_label": label,
        "participation_route": route,
        "participation_mode": classify_participation_mode(route),
        "trophy_recipient": cell_str(row.get(COLS["trophy_recipient"])),
        "booth_staff_1": cell_str(row.get(COLS["booth_staff_1"])),
        "booth_staff_2": cell_str(row.get(COLS["booth_staff_2"])),
        "follow_up_by": cell_str(row.get(COLS["follow_up_by"])),
        "notes": cell_str(row.get(COLS["notes"])),
        "data_source": cell_str(row.get(COLS["data_source"])),
    }


def parse_sheet(xlsx_path: Path, sheet_name: str) -> list[dict]:
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name).dropna(how="all")
    return [row_to_record(row) for _, row in df.iterrows() if cell_str(row.get(COLS["org_name"]))]


def build_summary(awardees: list[dict]) -> dict:
    pending = [a for a in awardees if a["form_status"] == "pending"]
    responded = [a for a in awardees if a["form_status"] == "responded"]
    declined = [a for a in awardees if a["form_status"] == "declined"]
    total = len(awardees)
    responded_count = len(responded)

    return {
        "program": "อปท.มาตรฐาน พ.ศ. 2569",
        "event": "ประชุมวิชาการการแพทย์ฉุกเฉินในองค์กรปกครองส่วนท้องถิ่นระดับชาติ ครั้งที่ 10",
        "as_of": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "total_awardees": total,
        "responded_count": responded_count,
        "pending_count": len(pending),
        "declined_count": len(declined),
        "response_rate_pct": round(responded_count / total * 100, 1) if total else 0,
        "by_award_type": dict(Counter(a["award_type"] for a in awardees if a["award_type"])),
        "by_province_pending": dict(Counter(a["province"] for a in pending if a["province"])),
        "by_form_status_label": dict(Counter(a["form_status_label"] for a in awardees if a["form_status_label"])),
        "by_participation_mode": dict(
            Counter(a["participation_mode"] for a in awardees if a["participation_mode"])
        ),
        "with_email": sum(1 for a in awardees if a.get("email")),
        "with_phone": sum(1 for a in awardees if a.get("phone")),
        "spreadsheet_id": MASTER_SPREADSHEET_ID,
    }


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: sync_from_sheet.py <path-to-xlsx>")
        print(f"Master spreadsheet: https://docs.google.com/spreadsheets/d/{MASTER_SPREADSHEET_ID}/edit")
        return 1

    xlsx_path = Path(sys.argv[1])
    if not xlsx_path.exists():
        print(f"File not found: {xlsx_path}")
        return 1

    awardees = parse_sheet(xlsx_path, SHEETS["all"])
    pending = parse_sheet(xlsx_path, SHEETS["pending"])
    responded = parse_sheet(xlsx_path, SHEETS["responded"])
    summary = build_summary(awardees)

    write_json(DATA_DIR / "awardees.json", awardees)
    write_json(DATA_DIR / "pending_followup.json", pending)
    write_json(DATA_DIR / "responded.json", responded)
    write_json(DATA_DIR / "summary.json", summary)

    try:
        form_df = pd.read_excel(xlsx_path, sheet_name=SHEETS["form_raw"]).dropna(how="all")
        write_json(
            DATA_DIR / "form_raw.json",
            json.loads(form_df.to_json(orient="records", force_ascii=False, date_format="iso")),
        )
    except ValueError:
        pass

    print(f"✅ Synced {len(awardees)} awardees from master spreadsheet")
    print(
        f"   ตอบรับแล้ว: {summary['responded_count']}/{summary['total_awardees']} "
        f"({summary['response_rate_pct']}%)"
    )
    print(f"   ยังไม่ตอบรับ: {summary['pending_count']} · ไม่เข้าร่วม: {summary['declined_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
