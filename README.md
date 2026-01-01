# 🧮 LINE Math Solver Bot

บอท LINE สำหรับหาสมการคณิตศาสตร์ (Summation) จากตัวเลขที่กำหนด

## 📋 Features

- รับโจทย์ในรูปแบบ `ตัวเลข=ผลลัพธ์` (เช่น `24056=901`)
- ค้นหาสมการ Σ (Summation) ที่ใช้ตัวเลขครบทุกตัว
- รองรับ patterns: `i`, `i+i`, `i*i`, `i!`, `(i+i)!`, `(i!)!`

## 🚀 Deploy to Railway

### ขั้นตอนที่ 1: เตรียม GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/line-math-bot.git
git push -u origin main
```

### ขั้นตอนที่ 2: Deploy บน Railway

1. ไปที่ [railway.app](https://railway.app) และ Sign in ด้วย GitHub
2. คลิก **New Project** → **Deploy from GitHub repo**
3. เลือก repository ที่สร้างไว้
4. รอให้ deploy เสร็จ

### ขั้นตอนที่ 3: ตั้งค่า Environment Variables

ใน Railway Dashboard:
1. ไปที่ **Variables** tab
2. เพิ่ม:
   - `LINE_CHANNEL_ACCESS_TOKEN` = (จาก LINE Developers Console)
   - `LINE_CHANNEL_SECRET` = (จาก LINE Developers Console)

### ขั้นตอนที่ 4: Generate Domain

1. ไปที่ **Settings** → **Networking**
2. คลิก **Generate Domain**
3. คุณจะได้ URL เช่น `your-app.up.railway.app`

### ขั้นตอนที่ 5: ตั้งค่า LINE Webhook

1. ไปที่ [LINE Developers Console](https://developers.line.biz/console/)
2. เลือก Channel ของคุณ → **Messaging API** tab
3. ตั้ง **Webhook URL** เป็น: `https://your-app.up.railway.app/callback`
4. เปิดใช้งาน **Use webhook**
5. ปิด **Auto-reply messages** (ถ้าต้องการ)

## 🔧 Deploy to Render (ทางเลือก)

1. ไปที่ [render.com](https://render.com)
2. **New** → **Web Service**
3. เชื่อมต่อ GitHub repository
4. ตั้งค่า:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. เพิ่ม Environment Variables
6. Deploy และใช้ URL `xxx.onrender.com/callback`

## 💬 วิธีใช้งาน

ส่งข้อความไปที่ LINE Bot:

```
24056=901
```

Bot จะตอบกลับสมการ เช่น:
```
Σ_{i=2}^{9+3} (i*i) + 7 - 2 = 654
```

## 📁 โครงสร้างไฟล์

```
line-math-bot/
├── app.py              # Flask app + LINE webhook handler
├── smart_solver.py     # Logic แก้โจทย์คณิตศาสตร์
├── sum_library.json    # ฐานข้อมูล Summation patterns
├── requirements.txt    # Python dependencies
├── Procfile           # สำหรับ Railway/Render
└── README.md
```

## 🔑 การขอ LINE Credentials

1. ไปที่ [LINE Developers Console](https://developers.line.biz/console/)
2. สร้าง **Provider** (ถ้ายังไม่มี)
3. สร้าง **Messaging API Channel**
4. ใน **Basic settings**: คัดลอก **Channel secret**
5. ใน **Messaging API**: คลิก **Issue** เพื่อสร้าง **Channel access token**

## 📝 License

MIT License
