# EMS Quality Awards — NIEMS อปท. มาตรฐาน/คุณภาพ

ระบบติดตามและวางแผนการดำเนินงาน **รางวัลคุณภาพการแพทย์ฉุกเฉิน อปท.**  
สถาบันการแพทย์ฉุกเฉินแห่งชาติ (NIEMS / สพฉ.)

## โปรแกรมที่กำลังดำเนินการ

**อปท.มาตรฐาน พ.ศ. 2569** — ประชุมวิชาการการแพทย์ฉุกเฉินในองค์กรปกครองส่วนท้องถิ่นระดับชาติ **ครั้งที่ 10**

| ประเภทรางวัล | โฟลเดอร์ Drive |
|-------------|----------------|
| หน่วยปฏิบัติการแพทย์ระดับพื้นฐาน | [Drive](https://drive.google.com/drive/folders/1XybA5aj7ADdyVz5lLlxhOmVpAmjE-u3_) |
| หน่วยปฏิบัติการแพทย์ระดับสูง | ↑ |
| หน่วยปฏิบัติการอำนวยการดีเด่น | ↑ |

## แหล่งข้อมูลหลัก

| แหล่ง | ลิงก์ | บทบาท |
|-------|------|--------|
| **Spreadsheet ติดตาม** | [Google Sheet](https://docs.google.com/spreadsheets/d/1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo/edit) | ตอบรับเข้าร่วมงาน + นิทรรศการ (ชีต `Form Responses 3`) |
| **Drive งานปัจจุบัน** | [โฟลเดอร์หลัก](https://drive.google.com/drive/folders/1XybA5aj7ADdyVz5lLlxhOmVpAmjE-u3_) | เอกสารประกาศ หนังสือเชิญ แบบฟอร์ม |

## สถานะล่าสุด (ณ 26 มิ.ย. 2569)

| รายการ | จำนวน |
|--------|--------|
| อปท. ได้รับรางวัล (เป้าหมาย) | **59** แห่ง |
| ตอบรับแล้ว (ไม่ซ้ำ) | **16** แห่ง (27.1%) |
| ยังไม่ตอบรับ | **43** แห่ง ⚠️ |
| แจ้งไม่เข้าร่วม | 1 แห่ง |
| หน่วยออกนิทรรศการ (ไม่ได้รับรางวัล) | 4 แห่ง |
| ขอที่พักจาก อบจ.กระบี่ | 17 รายการ |

## โครงสร้างโปรเจกต์

```
EMS_Quality_Awards/
├── data/
│   ├── programs.json           # นิยามโปรแกรม + แหล่งข้อมูล
│   ├── rsvp_responses.json     # คำตอบฟอร์มตอบรับ (จาก Spreadsheet)
│   ├── summary.json            # สรุปสถิติ
│   └── tracking_plan.json      # แผนติดตาม 4 ระยะ
├── dashboard/                  # Web Dashboard
├── scripts/
│   ├── sync_from_sheet.py      # ดึงข้อมูลจาก Google Sheet
│   ├── generate_summary.py
│   └── validate_data.py
└── docs/
    ├── DATA_DICTIONARY.md
    └── TRACKING_PLAN.md
```

## Quick Start

```bash
# ดู Dashboard
make serve
# เปิด http://localhost:8080/dashboard/

# สรุปผล CLI
make summary

# ตรวจสอบข้อมูล
make validate

# อัปเดตจาก Google Sheet (ต้องมีไฟล์ xlsx)
make sync
```

## แผนติดตาม 4 ระยะ

1. **ติดตามการตอบรับ** — ติดตาม 43 อปท. ที่ยังไม่ตอบรับ
2. **การเดินทางและที่พัก** — สรุปรูปแบบเดินทาง ประสาน อบจ.กระบี่
3. **นิทรรศการ** — ยืนยันเจ้าหน้าที่บูธ ค่าสนับสนุน 600 บาท/คน/วัน
4. **พิธีมอบโล่** — ยืนยันผู้รับมอบ จัดลำดับการมอบรางวัล

ดูรายละเอียด: [docs/TRACKING_PLAN.md](docs/TRACKING_PLAN.md)

## Deploy ไป GitHub

```bash
./deploy.sh
# เป้าหมาย: ppakpoomm/EMS_Quality_Awards
```

> หมายเหตุ: เปลี่ยนชื่อรีโปจาก `niems-activities` เป็น `EMS_Quality_Awards` บน GitHub ก่อน deploy

---

*NIEMS · M&E · อัปเดต กรกฎาคม 2026*
