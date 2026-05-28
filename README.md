# SME Retail: Revenue Optimization & Demand Forecasting

โปรเจกต์นี้เป็นส่วนหนึ่งของการทดสอบ Data Science (DS Test) สำหรับโจทย์การเพิ่มรายได้ (Maximize Revenue) ให้กับธุรกิจ SME Retail หรือ Supply Chain

## Business Case & Solution
ปัญหาหลักของธุรกิจ SME คือการจัดการสต็อกสินค้าและโปรโมชั่นที่ไม่สอดคล้องกับความต้องการจริง (Demand) 
โซลูชันที่นำเสนอคือ **AI-Driven Demand Forecasting** โดยใช้ Machine Learning เพื่อพยากรณ์ปริมาณความต้องการสินค้า (`qty`) ล่วงหน้า

**ทำไมถึงเลือก XGBoost?**
โจทย์ต้องการ Maximize Revenue ซึ่งแปรผันตรงกับปริมาณขาย การใช้โมเดล XGBoost Regressor เหมาะสมที่สุดในการจับความสัมพันธ์ที่ซับซ้อนของข้อมูลธุรกิจค้าปลีก (เช่น วันหยุดสุดสัปดาห์, การทำโปรโมชั่นลดราคา) เพื่อให้ร้านค้าสามารถเตรียมสต็อกได้แม่นยำ ลดต้นทุนจม และเพิ่มโอกาสการขายสูงสุด

## Feature Engineering & Mock Data
ในโปรเจกต์นี้ได้ทำการจำลองข้อมูล (Mock Data) อิงจากโครงสร้างที่กำหนด (Sales, Product, Promotion) และมีการเพิ่ม Feature ดังนี้:
- `is_holiday_flag` (ข้อมูลที่จำลองเพิ่ม): เพื่อให้โมเดลแยกแยะพฤติกรรมการซื้อช่วงเทศกาลออกจากช่วงปกติ ลด Error ในการพยากรณ์
- `discount` & `final_price`: คำนวณราคาขายจริงหลังหักโปรโมชั่น เพื่อวิเคราะห์ Price Elasticity
- `lag_1_qty`, `lag_7_qty`: ดึงยอดขายในอดีตมาเพื่อจับ Trend ของความต้องการ

## Project Structure
```text
test projact/
├── src/
│   ├── __init__.py
│   ├── data_prep.py     # Script สำหรับ Mock data และทำ Feature Engineering
│   └── model.py         # Script สำหรับเทรนโมเดล XGBoost และวัดผล
├── main.py              # ไฟล์หลักสำหรับรัน Data Pipeline
└── requirements.txt     # Dependencies