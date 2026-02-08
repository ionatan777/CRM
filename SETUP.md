# WhatsBackup Setup Guide

## 🚀 Quick Start Guide

Follow these steps to get WhatsBackup up and running:

### 1. Install Backend Dependencies

```bash
cd c:\CRM
pip install reportlab
pip install httpx
pip install sqlalchemy
pip install fastapi
```

### 2. Configure Database

The `.env` file has been updated with WhatsBackup settings. Review and customize if needed:

```bash
# Database
POSTGRES_DB=whatsbackup_db
PROJECT_NAME=WhatsBackup

# WhatsApp Business API (IMPORTANT!)
WHATSAPP_WEBHOOK_VERIFY_TOKEN=change_this_to_your_verify_token
WHATSAPP_APP_SECRET=change_this_to_your_app_secret
```

### 3. Run Database Migration

**⚠️ IMPORTANT: Backup your database first!**

```bash
cd c:\CRM
python scripts/migrate_to_whatsbackup.py
```

This will:
- Drop old CRM tables (tenants, contacts, conversations, etc.)
- Modify users table (add WhatsApp fields)
- Create new tables (backups, messages)
- Create indexes for performance

### 4. Test Models

Verify everything works:

```bash
python scripts/test_models.py
```

This creates test data and validates:
- User model with WhatsApp credentials
- Backup model
- Message model
- Search functionality

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### 6. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:5174`

### 7. Get WhatsApp Credentials

1. Go to [Meta for Developers](https://developers.facebook.com)
2. Create/select a WhatsApp Business App
3. Navigate to WhatsApp > Getting Started
4. Get your:
   - **Phone Number ID** (looks like: 123456789012345)
   - **Access Token** (starts with: EAA...)
5. Save these for the connection step

### 8. Connect WhatsApp

1. Login to WhatsBackup
2. Go to "Conectar WhatsApp"
3. Paste your credentials
4. Click "Conectar WhatsApp Ahora"

### 9. Create First Backup

Two ways to create backups:

**Manual:**
1. Go to "Mis Backups"
2. Click "Crear Backup Ahora"
3. Wait for completion

**Automatic (Scheduler):**
```bash
# Run in background
python scripts/auto_backup_scheduler.py
```

This will backup all users every 24 hours automatically.

---

## 📊 Features Available

### ✅ Connect WhatsApp
- `/dashboard/connect` - Connect WhatsApp Business account
- Saves credentials securely in database

### ✅ View Backups
- `/dashboard/backups` - See all backup history
- Statistics: total messages, contacts, last backup date

### ✅ Search Messages
- `/dashboard/search` - Search through all backed-up messages
- Full-text search across all conversations

### ✅ Export to PDF
- Export any conversation to PDF
- Legal documentation ready

---

## 🔧 Configuration Options

### Auto-Backup Settings (in `.env`)

```bash
AUTO_BACKUP_ENABLED=true          # Enable auto-backups
BACKUP_FREQUENCY_HOURS=24         # How often to backup
BACKUP_RETENTION_DAYS=365         # How long to keep backups
```

### Per-User Settings (in database)

Each user can customize:
- `auto_backup_enabled` - Enable/disable for this user
- `backup_frequency_hours` - Custom frequency (24, 12, 48 hours, etc.)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if all deps are installed
pip install -r requirements.txt
pip install reportlab

# Verify database connection
# Check .env DATABASE_URL
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Database errors
```bash
# Re-run migration
python scripts/migrate_to_whatsbackup.py

# Test models
python scripts/test_models.py
```

### WhatsApp connection fails
- Verify your Phone Number ID is correct
- Verify Access Token hasn't expired
- Check Meta Business Manager settings
- Ensure WhatsApp Business API is enabled

---

## 📝 Next Steps After Setup

1. **Create test backup** - Verify integration works
2. **Set up scheduler** - For automatic daily backups
3. **Configure webhooks** (optional) - For real-time message sync
4. **Customize branding** - Update colors, logos if needed

---

## 🎯 Production Deployment Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env` to a strong random string
- [ ] Update `WHATSAPP_WEBHOOK_VERIFY_TOKEN` 
- [ ] Update `WHATSAPP_APP_SECRET`
- [ ] Set up SSL/HTTPS
- [ ] Configure CORS for your domain
- [ ] Set up monitoring/alerts
- [ ] Configure backup retention policy
- [ ] Test PDF export on server
- [ ] Set up auto-backup scheduler as system service

---

## 🆘 Support

If you encounter issues:
1. Check logs in the terminal
2. Verify all environment variables
3. Test with `test_models.py`
4. Check WhatsApp Business API status
5. Review Meta Developer Console for API errors

---

*Setup guide for WhatsBackup v1.0*
