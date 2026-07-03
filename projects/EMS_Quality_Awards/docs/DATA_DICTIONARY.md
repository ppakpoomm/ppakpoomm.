# Data Dictionary — EMS Quality Awards

## แหล่งข้อมูล

| แหล่ง | ID/URL | ชีต/โฟลเดอร์ |
|-------|--------|-------------|
| Spreadsheet หลัก | `1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo` | `Form Responses 3` |
| Drive งานปัจจุบัน | `1XybA5aj7ADdyVz5lLlxhOmVpAmjE-u3_` | อปท.มาตรฐาน 2569 |

## rsvp_responses.json

คำตอบฟอร์มตอบรับเข้าร่วมงาน

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | ลำดับรายการ |
| `timestamp` | string | วันเวลาที่ส่งฟอร์ม |
| `status` | enum | `award_winner`, `declined`, `exhibitor` |
| `participation_mode` | enum | `trophy_and_exhibition`, `trophy_only` |
| `org_code` | string | รหัส อปท. จากรายชื่อ 59 แห่ง |
| `org_name` | string | ชื่อองค์กร |
| `province` | string | จังหวัด |
| `unit_type` | string | ระดับพื้นฐาน / สูง / อำนวยการดีเด่น |
| `coordinator` | string | ผู้ประสานงาน |
| `coordinator_phone` | string | เบอร์โทรผู้ประสานงาน |
| `trophy_recipient` | string | ผู้รับมอบโล่ |
| `travel_mode` | string | รูปแบบการเดินทาง |
| `travel_detail` | string | รายละเอียดเส้นทาง |
| `accommodation_request` | boolean | ขอที่พักจาก อบจ.กระบี่ |
| `booth_staff_1/2` | string | เจ้าหน้าที่บูธนิทรรศการ |
| `declined_org` | string | ชื่อ อปท. ที่ไม่เข้าร่วม |
| `declined_reason` | string | เหตุผลไม่เข้าร่วม |

## summary.json

สรุปสถิติภาพรวม — อัตราตอบรับ, แยกตามสถานะ/ประเภท/การเดินทาง

## tracking_plan.json

แผนติดตาม 4 ระยะ + KPIs + ลิงก์แหล่งข้อมูล

## การอัปเดต

```bash
make sync      # ดาวน์โหลด + แปลงจาก Google Sheet
make validate  # ตรวจสอบคุณภาพข้อมูล
make summary   # แสดงสรุป CLI
```
