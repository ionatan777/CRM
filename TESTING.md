# Local Testing Checklist - WhatsBackup MVP

## ✅ Pre-Flight Checks

### 1. Environment Setup
- [ ] PostgreSQL running
- [ ] Database `whatsbackup_db` exists
- [ ] All .env files configured
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Node dependencies installed (baileys-server: `npm install`)
- [ ] Frontend dependencies installed (`npm install`)

---

## 🚀 Start All Servers

**Terminal 1 - Backend:**
```bash
cd c:\CRM
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Baileys Server:**
```bash
cd c:\CRM\baileys-server
npm start
```

**Terminal 3 - Frontend:**
```bash
cd c:\CRM\frontend
npm run dev
```

**Expected:**
- Backend: http://localhost:8000
- Baileys: http://localhost:3000
- Frontend: http://localhost:5173

---

## 🧪 Automated Quick Check

```bash
# Run quick test (if on Linux/Mac)
bash scripts/test_local.sh

# Manual checks:
curl http://localhost:8000/health
curl http://localhost:3000/health
curl http://localhost:5173
```

---

## 📋 Manual Testing Flow

### Test 1: User Registration & Login
- [ ] Open http://localhost:5173
- [ ] Click "Register" or navigate to register page
- [ ] Fill form: 
  - Email: test@whatsbackup.com
  - Password: Test123456
  - Name: Test User
- [ ] Submit and verify redirects to dashboard
- [ ] Logout
- [ ] Login again with same credentials
- [ ] ✅ **PASS** if login successful

---

### Test 2: Pricing Page
- [ ] Navigate to /dashboard/pricing
- [ ] Verify both plans displayed (Express $18, Pro $35)
- [ ] Verify features listed correctly
- [ ] Click "Choose Express"
- [ ] Verify redirects to /dashboard/connect-express
- [ ] Go back, click "Choose Pro"
- [ ] Verify redirects to /dashboard/connect-pro
- [ ] ✅ **PASS** if all redirects work

---

### Test 3: Express Plan Flow (QR Code)

**Prerequisites:**
- Have WhatsApp installed on phone
- Phone has internet connection

**Steps:**
- [ ] Select Express plan from Pricing
- [ ] Verify QR code displays on ConnectExpress page
- [ ] Verify countdown timer shows (60 seconds)
- [ ] Open WhatsApp on phone
- [ ] Go to Settings → Linked Devices
- [ ] Tap "Link a Device"
- [ ] Scan the QR code
- [ ] Wait for connection (polling happens automatically)
- [ ] Verify success message appears
- [ ] Verify redirects to dashboard
- [ ] ✅ **PASS** if connection successful

**Backend Verification:**
- [ ] Check backend logs for QR generation
- [ ] Check Baileys server logs for connection
- [ ] Verify user.baileys_session_id is set in database

---

### Test 4: Express Plan - Create Backup

**Prerequisites:**
- Express plan connected (Test 3 completed)

**Steps:**
- [ ] On dashboard, click "Create Backup" button
- [ ] Wait for backup to complete
- [ ] Verify success message
- [ ] Navigate to "Mis Backups"
- [ ] Verify backup appears in history
- [ ] Verify message count is realistic
- [ ] ✅ **PASS** if backup created

**Database Verification:**
```sql
SELECT * FROM backups WHERE backup_source = 'baileys' ORDER BY backup_date DESC LIMIT 1;
SELECT COUNT(*) FROM messages WHERE source = 'baileys';
```

---

### Test 5: Pro Plan Flow (API Credentials)

**Prerequisites:**
- WhatsApp Business API credentials (get from Meta)
- Phone Number ID
- Access Token

**Steps:**
- [ ] Logout (or use different user)
- [ ] Register new user: pro-test@whatsbackup.com
- [ ] Select Pro plan from Pricing
- [ ] On ConnectPro page, enter:
  - Phone Number ID: [your-id]
  - Access Token: [your-token]
- [ ] Click "Connect WhatsApp Business API"
- [ ] Verify success message
- [ ] Verify redirects to dashboard
- [ ] ✅ **PASS** if connection successful

**Backend Verification:**
- [ ] Check backend logs for API connection
- [ ] Verify user.whatsapp_phone_id is set
- [ ] Verify user.whatsapp_access_token is set

---

### Test 6: Pro Plan - Create Backup

**Prerequisites:**
- Pro plan connected (Test 5 completed)

**Steps:**
- [ ] On dashboard, click "Create Backup"
- [ ] Wait for backup to complete (may take longer than Express)
- [ ] Verify success message
- [ ] Navigate to "Mis Backups"
- [ ] Verify backup appears in history
- [ ] ✅ **PASS** if backup created

**Database Verification:**
```sql
SELECT * FROM backups WHERE backup_source = 'api' ORDER BY backup_date DESC LIMIT 1;
SELECT COUNT(*) FROM messages WHERE source = 'api';
```

---

### Test 7: Message Search

**Prerequisites:**
- At least one backup completed (Test 4 or 6)

**Steps:**
- [ ] Navigate to "Buscar Mensajes"
- [ ] Enter search term (word from your messages)
- [ ] Click "Search"
- [ ] Verify results appear
- [ ] Verify results contain search term
- [ ] Try empty search (should show all)
- [ ] ✅ **PASS** if search works

---

### Test 8: PDF Export

**Prerequisites:**
- Messages in database

**Steps:**
- [ ] From Message Search results, identify a contact
- [ ] Click "Export to PDF" for that contact
- [ ] Verify PDF downloads
- [ ] Open PDF
- [ ] Verify messages are formatted correctly
- [ ] ✅ **PASS** if PDF generates

---

### Test 9: Plan Limits (Express)

**Prerequisites:**
- Express user with active subscription

**Steps:**
- [ ] Get current message count for user
- [ ] Manually update subscription.messages_this_period to 4999
- [ ] Try to create backup
- [ ] Should succeed (under limit)
- [ ] Update subscription.messages_this_period to 5001
- [ ] Try to create backup again
- [ ] Should fail with "Message limit reached" error
- [ ] ✅ **PASS** if limit enforcement works

---

### Test 10: Plan Upgrade

**Prerequisites:**
- Express user logged in

**Steps:**
- [ ] Navigate to Settings or Pricing
- [ ] Click "Upgrade to Pro"
- [ ] Verify confirmation message
- [ ] Verify plan_type changes to 'pro'
- [ ] Verify can now use Pro features
- [ ] ✅ **PASS** if upgrade works

---

## 🐛 Common Issues & Fixes

**Issue: Backend won't start**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <pid> /F

# Verify Python dependencies
pip install -r requirements.txt
```

**Issue: Baileys server won't start**
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Reinstall dependencies
cd baileys-server
rm -rf node_modules package-lock.json
npm install
```

**Issue: QR not generating**
- Check Baileys server is running: http://localhost:3000/health
- Check backend can reach Baileys: verify BAILEYS_SERVER_URL in .env
- Check backend logs for connection errors

**Issue: Database connection fails**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Create database: `createdb whatsbackup_db`
- Run migration or create tables manually

**Issue: Frontend can't connect to backend**
- Check VITE_API_URL in frontend/.env
- Verify backend is running on correct port
- Check CORS settings in backend

---

## ✅ Testing Complete Checklist

- [ ] All 3 servers start successfully
- [ ] User registration works
- [ ] User login works
- [ ] Pricing page displays correctly
- [ ] Express: QR generation works
- [ ] Express: WhatsApp connection works
- [ ] Express: Backup creation works
- [ ] Pro: API connection works
- [ ] Pro: Backup creation works
- [ ] Message search works
- [ ] PDF export works
- [ ] Plan limits enforced (Express)
- [ ] Plan upgrade works (Express → Pro)

**If all checked: ✅ READY FOR DEPLOYMENT**

---

## 📊 Database Verification Queries

```sql
-- Check users and their plans
SELECT email, plan_type, plan_status, auto_backup_enabled FROM users;

-- Check backups
SELECT user_id, backup_date, status, backup_source, total_messages FROM backups ORDER BY backup_date DESC LIMIT 10;

-- Check messages by source
SELECT source, COUNT(*) as count FROM messages GROUP BY source;

-- Check subscriptions
SELECT user_id, plan_type, status, messages_this_period, max_messages FROM subscriptions;
```

---

**Time Estimate:** 30-45 minutes for full testing
**Next Step:** If all tests pass → Proceed to DEPLOYMENT.md
