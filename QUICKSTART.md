# Quick Start Guide - WhatsBackup MVP

## 🎯 For Developers

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- npm/yarn

### Local Development Setup (5 minutes)

**1. Clone & Install:**
```bash
# Backend
cd c:\CRM
pip install -r requirements.txt

# Baileys Server
cd baileys-server
npm install

# Frontend
cd frontend
npm install
```

**2. Configure .env:**
```bash
# Copy templates
cp .env.example .env
cp baileys-server/.env.example baileys-server/.env
cp frontend/.env.example frontend/.env

# Edit with your values
```

**3. Database:**
```bash
# Create database
createdb whatsbackup_db

# Create tables
python -c "from app.db.session import engine, Base; from app.models.user import User; from app.models.message import Message; from app.models.backup import Backup; from app.models.subscription import Subscription; Base.metadata.create_all(bind=engine)"
```

**4. Run Everything:**
```bash
# Terminal 1: Backend
uvicorn app.main:app --reload

# Terminal 2: Baileys Server
cd baileys-server
npm start

# Terminal 3: Frontend
cd frontend
npm run dev
```

**5. Open Browser:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs
- Baileys Health: http://localhost:3000/health

---

## 🧪 Quick Test

1. **Register:** Create account at http://localhost:5173/login
2. **Select Plan:** Go to Pricing, choose Express
3. **Connect:** Scan QR with WhatsApp
4. **Backup:** Click "Create Backup" on dashboard
5. **Search:** Search your messages

---

## 📁 Project Structure

```
CRM/
├── app/                    # Backend (FastAPI)
│   ├── api/v1/endpoints/  # API routes
│   ├── models/            # SQLAlchemy models
│   ├── services/          # Business logic
│   ├── integrations/      # WhatsApp API & Baileys
│   └── schedulers/        # Auto-backup jobs
├── baileys-server/        # Node.js Baileys server
│   └── index.js           # Express server
├── frontend/              # React frontend
│   └── src/pages/         # UI pages
├── alembic/               # DB migrations
└── scripts/               # Utility scripts
```

---

## 🏗️ Architecture

```
┌─────────────┐
│   React     │ ← User Interface
│  Frontend   │
└─────┬───────┘
      │ REST API
┌─────▼────────────────┐
│  FastAPI Backend     │
├───────────────────────┤
│ Plans │ Auth │ Backup│
└─┬────────────────┬───┘
  │                │
  ▼                ▼
┌────────────┐  ┌──────────────┐
│ WhatsApp   │  │   Baileys    │
│ Business   │  │   Node.js    │
│ API (Pro)  │  │   (Express)  │
└────────────┘  └──────────────┘
```

---

## 🎨 Key Features

✅ **Dual Plan System**
- Express: QR code, 5K msgs, $18/mo
- Pro: Business API, unlimited, $35/mo

✅ **Auto Backups**
- Express: Every 12 hours
- Pro: Every 24 hours

✅ **Message Management**
- Full search
- PDF export
- Backup history

---

## 🚀 Next Steps

1. **Deploy** (see DEPLOYMENT.md)
2. **Configure Payment** (Stripe)
3. **Set up Monitoring**
4. **Launch Marketing**

---

## 📞 Support

Issues? Check:
- DEPLOYMENT.md (troubleshooting)
- Backend logs
- Baileys server logs
- Browser console

---

**Built with ❤️ for WhatsBackup MVP**
