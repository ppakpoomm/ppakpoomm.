# Data Dictionary — NIEMS Activities

## programs.json

นิยามโปรแกรมการคัดเลือก อปท.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | รหัสโปรแกรม เช่น `apt-standard-2569` |
| `name` | string | ชื่อโปรแกรมภาษาไทย |
| `fiscal_year` | number | ปี พ.ศ. |
| `status` | enum | `active`, `completed`, `archived` |
| `unit_types` | string[] | ประเภทหน่วยปฏิบัติการที่รับสมัคร |

## submissions_standard_2569.json

รายการ อปท. ที่ส่งแบบฟอร์ม Google Form

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | ลำดับรายการ |
| `program_id` | string | อ้างอิงโปรแกรม |
| `submitted_at` | string | วันที่ส่ง (DD/M/YYYY HH:mm) |
| `province` | string | จังหวัด |
| `unit_type` | string | ประเภทหน่วยปฏิบัติการ |
| `submission_order` | number | ลำดับที่เสนอ (1, 2, ...) |
| `org_name` | string | ชื่อ อปท. |
| `coordinator` | string | ชื่อผู้ประสานงาน |
| `phone` | string | เบอร์โทรศัพท์ |
| `score` | number\|null | คะแนน |
| `notes` | string\|null | หมายเหตุ/ปัญหา |
| `has_issue` | boolean | มีปัญหาข้อมูลหรือไม่ |

## comparison_standard_2569.json

เปรียบเทียบหนังสือนำส่ง (Google Drive) vs แบบฟอร์ม (Google Form) รายจังหวัด

| Field | Type | Description |
|-------|------|-------------|
| `province` | string | จังหวัด |
| `has_letter` | boolean | มีโฟลเดอร์หนังสือใน Drive |
| `has_form` | boolean | มีการกรอก Google Form |
| `form_status` | string | สถานะฟอร์ม (✅ หรือ ❌ ยังไม่กรอกฟอร์ม) |

## status_standard_2569.json

สรุปสถานะภาพรวมและรายชื่อจังหวัดที่ต้องติดตาม

## quality_issues.json

รายการปัญหาคุณภาพข้อมูลที่ต้องแก้ไข

| Field | Type | Description |
|-------|------|-------------|
| `province` | string | จังหวัด |
| `org_name` | string | ชื่อองค์กร |
| `issue` | string | รายละเอียดปัญหา |
| `severity` | enum | `high`, `medium`, `low` |

## การอัปเดตข้อมูล

1. Export ข้อมูลจาก Google Form เป็น CSV
2. อัปเดตโฟลเดอร์ Google Drive
3. รัน script แปลง CSV → JSON (หรืออัปเดต JSON โดยตรง)
4. รัน `python3 scripts/validate_data.py` เพื่อตรวจสอบ
5. Commit และ push
