# WhatsBackup MVP - Deployment Guide

## 🚀 Pre-Deployment Checklist

### Environment Variables Required

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/whatsbackup_db

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# WhatsApp Business API (Pro Plan)
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your-verify-token
WHATSAPP_APP_SECRET=your-app-secret

# Baileys Server URL (Express Plan)
BAILEYS_SERVER_URL=http://localhost:3000

# Plan Pricing
EXPRESS_PRICE=18.00
PRO_PRICE=35.00
EXPRESS_MESSAGE_LIMIT=5000

# Optional: Payment (Stripe)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Baileys Server (.env):**
```bash
PORT=3000
SESSION_DIR=./sessions
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
```

---

## 📦 Deployment Steps

### 1. Database Setup (PostgreSQL)

```bash
# Create database
createdb whatsbackup_db

# Run migrations
cd backend
alembic upgrade head

# Or create tables directly
python -c "from app.db.session import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

### 2. Backend Deployment (Railway/Render)

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add PostgreSQL
railway add

# Deploy
railway up
```

**Render:**
1. Connect GitHub repo
2. Choose "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from .env

### 3. Baileys Server Deployment (Railway/Render)

**Separate Service:**
```bash
# Navigate to baileys-server
cd baileys-server

# Deploy to Railway
railway init
railway up

# OR Deploy to Render
# Build command: npm install
# Start command: npm start
```

**Important:** Update `BAILEYS_SERVER_URL` in backend .env with deployed URL.

### 4. Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel --prod

# OR via Vercel Dashboard:
# 1. Import GitHub repo
# 2. Framework: Vite
# 3. Build command: npm run build
# 4. Output directory: dist
# 5. Add VITE_API_URL environment variable
```

---

## 🔧 Running Schedulers

### Option 1: Supervisor (Linux)

**Install Supervisor:**
```bash
sudo apt-get install supervisor
```

**Create config files:**

`/etc/supervisor/conf.d/express-backup.conf`:
```ini
[program:express-backup]
command=/usr/bin/python3 /path/to/app/schedulers/express_backup.py
directory=/path/to/
autostart=true
autorestart=true
stderr_logfile=/var/log/express-backup.err.log
stdout_logfile=/var/log/express-backup.out.log
```

`/etc/supervisor/conf.d/pro-backup.conf`:
```ini
[program:pro-backup]
command=/usr/bin/python3 /path/to/app/schedulers/pro_backup.py
directory=/path/to/
autostart=true
autorestart=true
stderr_logfile=/var/log/pro-backup.err.log
stdout_logfile=/var/log/pro-backup.out.log
```

**Start:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start express-backup
sudo supervisorctl start pro-backup
```

### Option 2: PM2 (Node.js)

```bash
# Install PM2
npm install -g pm2

# Start schedulers
pm2 start app/schedulers/express_backup.py --interpreter python3 --name express-backup
pm2 start app/schedulers/pro_backup.py --interpreter python3 --name pro-backup

# Save and auto-start
pm2 save
pm2 startup
```

### Option 3: systemd (Linux)

Create `/etc/systemd/system/express-backup.service`:
```ini
[Unit]
Description=WhatsBackup Express Plan Scheduler
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/python3 /path/to/app/schedulers/express_backup.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable express-backup
sudo systemctl start express-backup
sudo systemctl status express-backup
```

---

## 🧪 Testing Checklist

### Backend Tests
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] Auth: Register user, login, get token
- [ ] Plans: List plans, select Express plan
- [ ] Baileys: Generate QR (check if Baileys server running)
- [ ] WhatsApp API: Connect with credentials
- [ ] Backups: Create backup, list history
- [ ] Messages: Search messages, export PDF

### Baileys Server Tests
- [ ] Health: `curl http://localhost:3000/health`
- [ ] Generate QR: POST /generate-qr
- [ ] Check status: GET /status/:session_id
- [ ] QR actually displays (test in browser/frontend)

### Frontend Tests
- [ ] Login page works
- [ ] Register new user
- [ ] Navigate to Pricing
- [ ] Select Express plan → redirect to ConnectExpress
- [ ] Select Pro plan → redirect to ConnectPro
- [ ] QR code displays properly
- [ ] Connection polling works
- [ ] Dashboard shows plan badge
- [ ] Backup history loads
- [ ] Message search works

### E2E Tests
- [ ] Express Plan: Full flow (select → QR → scan → backup)
- [ ] Pro Plan: Full flow (select → API → backup)
- [ ] Plan limits: Express hits 5K limit
- [ ] Upgrade: Express → Pro
- [ ] Schedulers: Run manually and verify backups

---

## 📊 Monitoring

### Logs to Watch
```bash
# Backend
tail -f /var/log/whatsbackup/api.log

# Baileys Server
tail -f /var/log/whatsbackup/baileys.log

# Schedulers
tail -f /var/log/express-backup.out.log
tail -f /var/log/pro-backup.out.log
```

### Key Metrics
- Number of active users per plan
- Backup success rate
- Message throughput
- API errors
- Baileys connection stability

---

## 🐛 Common Issues

**Issue: Baileys QR not generating**
- Check Baileys server is running: `curl http://localhost:3000/health`
- Check `BAILEYS_SERVER_URL` in backend .env
- Verify firewall allows port 3000

**Issue: WhatsApp API connection fails**
- Verify Phone Number ID and Access Token
- Check token hasn't expired
- Verify webhook is configured in Meta

**Issue: Schedulers not running**
- Check supervisor/PM2 status
- Verify DATABASE_URL is correct
- Check log files for errors

**Issue: Frontend can't connect to backend**
- Check `VITE_API_URL` matches deployed backend
- Verify CORS is enabled in FastAPI
- Check API is actually running

---

## 🎯 Post-Deployment

### Create First Admin User
```bash
# Via API
curl -X POST http://your-api.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@whatsbackup.com","password":"strong-password","full_name":"Admin"}'
```

### Set Up Payment (Stripe)
1. Create Stripe account
2. Get API keys
3. Add to .env
4. Create webhook for subscription events
5. Test with Stripe test cards

### Marketing Setup
1. Update Pricing page with actual prices
2. Add Terms of Service
3. Add Privacy Policy
4. Set up customer support email

---

## 📈 Scaling Considerations

**When you need to scale:**
- Separate database server
- Load balancer for API
- Multiple Baileys servers (session distribution)
- Redis for session caching
- CDN for frontend
- Professional monitoring (DataDog, New Relic)

---

## ✅ MVP Launch Checklist

- [ ] All environment variables set
- [ ] Database migrated
- [ ] Backend deployed and healthy
- [ ] Baileys server deployed and healthy
- [ ] Frontend deployed
- [ ] Schedulers running
- [ ] Test user can register
- [ ] Test user can select plan
- [ ] Express plan: QR works end-to-end
- [ ] Pro plan: API connection works
- [ ] Backup created successfully
- [ ] Message search works
- [ ] PDF export works
- [ ] Monitoring in place
- [ ] Domain configured
- [ ] SSL certificates
- [ ] Payment processing (if enabled)

**You're ready to launch! 🚀**
