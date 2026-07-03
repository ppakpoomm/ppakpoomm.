# NIEMS Activities Tracker

ระบบติดตามกิจกรรมการคัดเลือก **องค์กรปกครองส่วนท้องถิ่น (อปท.)** ด้านการแพทย์ฉุกเฉิน  
สถาบันการแพทย์ฉุกเฉินแห่งชาติ (NIEMS / สพฉ.)

## โปรแกรมที่ติดตาม

| โปรแกรม | ปี | สถานะ | คำอธิบาย |
|---------|-----|--------|----------|
| **อปท.มาตรฐาน** | 2569 | 🟢 Active | คัดเลือก อปท. ที่มีการบริหารการแพทย์ฉุกเฉินให้มีมาตรฐาน |
| **อปท.คุณภาพ** | 2568 | ✅ Completed | คัดเลือก อปท. ที่มีการบริหารการแพทย์ฉุกเฉินให้มีคุณภาพ |
| **อปท.คุณภาพ** | 2567 | 📦 Archived | ข้อมูลย้อนหลัง |

### ประเภทหน่วยปฏิบัติการ (อปท.มาตรฐาน 2569)

- **ระดับพื้นฐาน** — หน่วยปฏิบัติการแพทย์ฉุกเฉินระดับพื้นฐาน
- **ระดับสูง** — หน่วยปฏิบัติการแพทย์ฉุกเฉินระดับสูง
- **อำนวยการ** — หน่วยปฏิบัติการอำนวยการดีเด่น

## โครงสร้างโปรเจกต์

```
niems-activities/
├── data/                          # ข้อมูล JSON (จาก Google Drive + Google Form)
│   ├── programs.json              # นิยามโปรแกรม
│   ├── submissions_standard_2569.json
│   ├── comparison_standard_2569.json
│   ├── status_standard_2569.json
│   └── quality_issues.json
├── dashboard/                     # Web Dashboard
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── scripts/                       # Python utilities
│   ├── validate_data.py
│   └── generate_summary.py
└── docs/
    └── DATA_DICTIONARY.md
```

## Quick Start

### ดู Dashboard

```bash
# รัน local server แล้วเปิด dashboard
python3 -m http.server 8080
# เปิด http://localhost:8080/dashboard/
```

### สรุปผล

```bash
python3 scripts/generate_summary.py
```

### ตรวจสอบคุณภาพข้อมูล

```bash
python3 scripts/validate_data.py
```

## สถานะปัจจุบัน (อปท.มาตรฐาน 2569)

| รายการ | จำนวน |
|--------|--------|
| อปท. ที่กรอกแบบฟอร์ม | 41 |
| จังหวัดที่มีโฟลเดอร์ใน Drive | 32 |
| จังหวัดครบถ้วน (หนังสือ + ฟอร์ม) | 17 |
| จังหวัดมีหนังสือแต่ไม่กรอกฟอร์ม | 15 ⚠️ |
| จังหวัดกรอกฟอร์มแต่ไม่ส่งหนังสือ | 10 ⚠️ |
| ปัญหาคุณภาพข้อมูล | 6 |

## แหล่งข้อมูล

- **Google Drive:** [โฟลเดอร์หลัก](https://drive.google.com/drive/folders/1CzZo6jDwKO_mU0utRP5nUnb5PopefWiR)
- **Google Form:** แบบเสนอผลงานเพื่อคัดเลือก อปท.มาตรฐาน 2569
- **Hub:** [ppakpoomm/ppakpoomm.](https://github.com/ppakpoomm/ppakpoomm.)

## ที่เกี่ยวข้อง

- [niems-strategic-system](https://github.com/ppakpoomm/niems-strategic-system) — ระบบวางแผนยุทธศาสตร์
- [AI-for-Thai-EMS](https://github.com/ppakpoomm/AI-for-Thai-EMS) — แอป AI สำหรับ EMS

---

*NIEMS · Monitoring & Evaluation · อัปเดต กรกฎาคม 2026*
