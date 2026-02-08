# Baileys WhatsApp Server

Express plan backend for WhatsBackup - handles WhatsApp Web connections via QR

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

Server runs on port 3000 by default.

## Endpoints

- `POST /generate-qr` - Generate QR code for connection
- `GET /status/:session_id` - Check connection status
- `POST /fetch-messages` - Fetch messages from session
- `POST /disconnect/:session_id` - Disconnect session
- `GET /health` - Health check

## Sessions

Sessions are stored in `./sessions/` directory.
