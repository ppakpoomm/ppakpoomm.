# พื้นที่ทำงานกลาง — Central Workspace Guide

> คู่มือนี้อธิบายโครงสร้างและวิธีใช้งานรีโป `ppakpoomm/ppakpoomm.` ในฐานะศูนย์กลางจัดการโปรเจกต์ทั้งหมด

**เจ้าของ:** Pakpoom Thanudtee (@ppakpoomm)  
**องค์กร:** สถาบันการแพทย์ฉุกเฉินแห่งชาติ (NIEMS)  
**สำรวจล่าสุด:** 3 กรกฎาคม 2026

---

## ภาพรวม

รีโปนี้ทำหน้าที่ 3 อย่าง:

1. **GitHub Profile README** — แสดงบนหน้าโปรไฟล์ [github.com/ppakpoomm](https://github.com/ppakpoomm)
2. **Central Hub** — จุดเชื่อมโยงไปยังรีโปทั้งหมด 10 รายการ
3. **Workspace Catalog** — เก็บ `repos.json` สำหรับ agent/tool อ่านได้

---

## แผนผังรีโปทั้งหมด (10 รายการ)

### หมวด 1: NIEMS — งานหลัก (3 รีโป)

โปรเจกต์ที่สร้างเองและเกี่ยวข้องกับงาน M&E ที่ NIEMS โดยตรง

#### 1.1 niems-strategic-system ⭐ ลำดับความสำคัญสูง

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/niems-strategic-system |
| ภาษา | Python |
| สถานะ | Active — Phase A เสร็จ, Phase B กำลังดำเนินการ |
| คำอธิบาย | Reverse engineering ระบบ Excel macro (NIEMSMART_original.xlsm) และสร้าง Blueprint สำหรับ modernization |

**เนื้อหาสำคัญ:**
- Forensic analysis ของ XLSM (60 worksheets, 2.1 MB VBA)
- 8 Strategic Frameworks: SWOT, TOWS, BSC, OKR, Logical Framework
- Python scripts: `analyze_xlsm.py`, `extract_vba.py`, `setup_database.py`
- โฟลเดอร์ `comprehensive_system_blueprint/` และ `xlsm_extracted/`

**ขั้นตอนถัดไป:** ดำเนิน Phase B — สร้าง deliverables ที่เหลือ (74/78)

---

#### 1.2 AI-for-Thai-EMS ⭐ ลำดับความสำคัญสูง

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/AI-for-Thai-EMS |
| ภาษา | TypeScript (Vite + React) |
| สถานะ | Active |
| คำอธิบาย | แอป AI สำหรับระบบการแพทย์ฉุกเฉินไทย (NIEMS_2569) |

**วิธีรัน:**
```bash
git clone https://github.com/ppakpoomm/AI-for-Thai-EMS.git
cd AI-for-Thai-EMS
npm install
# ตั้งค่า GEMINI_API_KEY ใน .env.local
npm run dev
```

**AI Studio:** https://ai.studio/apps/drive/1o3q_hCN3PFul0_za4Sn9F_vitxWP35tV

---

#### 1.3 niems-activities ✅ พัฒนาแล้ว

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/niems-activities |
| ภาษา | Python + HTML/JS Dashboard |
| สถานะ | Active — สร้างจากข้อมูล Google Drive |
| คำอธิบาย | ติดตามการคัดเลือก อปท.มาตรฐาน พ.ศ. 2569 และ อปท.คุณภาพ |

**ข้อมูลจาก Google Drive:**
- 44 รายการส่งฟอร์ม อปท.มาตรฐาน 2569
- 17 จังหวัดครบถ้วน (หนังสือ + ฟอร์ม)
- 15 จังหวัดมีหนังสือแต่ไม่กรอกฟอร์ม
- 10 จังหวัดกรอกฟอร์มแต่ไม่ส่งหนังสือ

**โค้ดชั่วคราวอยู่ที่:** [projects/niems-activities/](../projects/niems-activities/) (รอ push ไปรีโปจริง)

**วิธีรัน:**
```bash
cd projects/niems-activities
make serve
# เปิด http://localhost:8080/dashboard/
make summary    # สรุปผล CLI
make validate   # ตรวจสอบคุณภาพข้อมูล
```

---

### หมวด 2: การเรียนรู้ (3 รีโป)

#### 2.1 ML-For-Beginners

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/ML-For-Beginners |
| ประเภท | Fork จาก microsoft/ML-For-Beginners |
| ภาษา | Jupyter Notebook |
| สถานะ | Active — อัปเดตล่าสุด 2 ก.ค. 2026 |

12 สัปดาห์, 26 บทเรียน, 52 แบบทดสอบ — เรียน ML พื้นฐาน

---

#### 2.2 introduction-to-github ✅ เสร็จแล้ว

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/introduction-to-github |
| ประเภท | Fork (GitHub Skills template) |
| สถานะ | Completed — ก.ย. 2025 |

---

#### 2.3 skills-communicate-using-markdown

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/skills-communicate-using-markdown |
| สถานะ | In Progress — มี open issue 1 รายการ |

---

### หมวด 3: เครื่องมือ AI (3 รีโป)

#### 3.1 openclaw

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/openclaw |
| ประเภท | Fork จาก openclaw/openclaw |
| ภาษา | TypeScript |
| สถานะ | Active — sync ล่าสุด 2 ก.ค. 2026 |

Personal AI assistant ที่รองรับทุก OS และ Platform

---

#### 3.2 anthropic-quickstarts

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/anthropic-quickstarts |
| ประเภท | Fork จาก anthropics/anthropic-quickstarts |
| สถานะ | Reference |

โปรเจกต์ตัวอย่างสำหรับสร้างแอปด้วย Anthropic API

---

#### 3.3 system_prompts_leaks

| รายการ | รายละเอียด |
|--------|------------|
| URL | https://github.com/ppakpoomm/system_prompts_leaks |
| ประเภท | Fork |
| สถานะ | Reference — อัปเดตล่าสุด 3 ก.ค. 2026 |

คอลเลกชัน System Prompts สำหรับศึกษา prompt engineering

---

## โครงสร้างไฟล์ใน Hub นี้

```
ppakpoomm./
├── README.md              # Profile + Dashboard (แสดงบน GitHub profile)
├── repos.json             # แคตตาล็อกรีโปแบบ machine-readable
├── docs/
│   └── WORKSPACE.md       # คู่มือนี้
└── .github/
    └── ISSUE_TEMPLATE/
        ├── workspace-task.yml
        └── repo-request.yml
```

---

## วิธีใช้งาน Hub

### สำหรับมนุษย์

1. เปิด [README.md](../README.md) เพื่อดูภาพรวมและลิงก์ด่วน
2. อ่านคู่มือนี้เมื่อต้องการรายละเอียดแต่ละรีโป
3. ใช้ Quick Start table ใน README เพื่อไปยังรีโปที่ต้องการ

### สำหรับ AI Agent / Cursor

1. อ่าน `repos.json` เพื่อเข้าใจโครงสร้างรีโปทั้งหมด
2. ใช้ `category` และ `priority` เพื่อเลือกรีโปที่เกี่ยวข้อง
3. ดู `status` และ `notes` สำหรับ context ล่าสุด

### การอัปเดต Hub

เมื่อมีรีโปใหม่หรือสถานะเปลี่ยน:

1. อัปเดต `repos.json`
2. อัปเดตตารางใน `README.md`
3. เพิ่มรายละเอียดใน `docs/WORKSPACE.md` (ถ้าจำเป็น)
4. เปลี่ยน `last_surveyed` ใน repos.json

---

## ลำดับความสำคัญแนะนำ

| ลำดับ | รีโป | เหตุผล |
|-------|------|--------|
| 1 | niems-strategic-system | งานหลัก NIEMS, Phase B รอดำเนินการ |
| 2 | AI-for-Thai-EMS | โปรเจกต์ AI สำหรับ EMS ไทย |
| 3 | niems-activities | ควรเริ่มโปรเจกต์ — รีโปว่าง |
| 4 | ML-For-Beginners | กำลังเรียนอยู่ |
| 5 | openclaw | เครื่องมือ AI ส่วนตัว |

---

## สรุปสถิติ

| หมวด | จำนวน | Original | Fork |
|------|--------|----------|------|
| NIEMS Work | 3 | 3 | 0 |
| Learning | 3 | 1 | 2 |
| AI Tools | 3 | 0 | 3 |
| **รวม** | **9** (+ hub นี้ = 10) | **4** | **5** |

---

*สร้างโดย Cursor Cloud Agent · สำรวจจาก GitHub API วันที่ 3 กรกฎาคม 2026*
