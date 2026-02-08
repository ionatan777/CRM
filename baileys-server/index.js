/**
 * Baileys WhatsApp Server (Express Plan)
 * Handles WhatsApp Web connections via QR code
 * Port: 3000
 */

const express = require('express');
const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const QRCode = require('qrcode');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Store active sockets
const activeSockets = new Map();

// Session storage directory
const SESSION_DIR = path.join(__dirname, 'sessions');
if (!fs.existsSync(SESSION_DIR)) {
    fs.mkdirSync(SESSION_DIR, { recursive: true });
}

/**
 * POST /generate-qr
 * Generate QR code for WhatsApp connection
 */
app.post('/generate-qr', async (req, res) => {
    const { session_id } = req.body;

    if (!session_id) {
        return res.status(400).json({ error: 'session_id is required' });
    }

    console.log(`[QR] Generating QR for session: ${session_id}`);

    try {
        const sessionPath = path.join(SESSION_DIR, session_id);

        // If session already exists and is connected, return status
        if (activeSockets.has(session_id)) {
            return res.json({
                session_id,
                status: 'already_connected',
                message: 'WhatsApp is already connected for this session'
            });
        }

        // Create auth state
        const { state, saveCreds } = await useMultiFileAuthState(sessionPath);

        let qrCodeData = null;
        let connectionStatus = 'waiting';

        // Create socket
        const sock = makeWASocket({
            auth: state,
            printQRInTerminal: true
        });

        // Handle QR code generation
        sock.ev.on('connection.update', async (update) => {
            const { connection, lastDisconnect, qr } = update;

            if (qr) {
                qrCodeData = qr;
                console.log(`[QR] QR Code generated for ${session_id}`);
            }

            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error)?.output?.statusCode !== DisconnectReason.loggedOut;
                console.log(`[Connection] Closed for ${session_id}. Reconnect:`, shouldReconnect);

                if (!shouldReconnect) {
                    activeSockets.delete(session_id);
                }
            } else if (connection === 'open') {
                console.log(`[Connection] Opened for ${session_id}`);
                connectionStatus = 'connected';
                activeSockets.set(session_id, sock);
            }
        });

        // Save credentials when updated
        sock.ev.on('creds.update', saveCreds);

        // Wait for QR generation (timeout after 10 seconds)
        let attempts = 0;
        while (!qrCodeData && attempts < 20) {
            await new Promise(resolve => setTimeout(resolve, 500));
            attempts++;
        }

        if (!qrCodeData) {
            return res.status(500).json({ error: 'Failed to generate QR code' });
        }

        // Convert QR to base64 image
        const qrImage = await QRCode.toDataURL(qrCodeData);

        res.json({
            session_id,
            qr_code: qrImage,
            qr_text: qrCodeData,
            status: 'qr_generated',
            message: 'Scan this QR code with WhatsApp',
            expires_in: 60  // QR expires in 60 seconds
        });

    } catch (error) {
        console.error(`[Error] Failed to generate QR:`, error);
        res.status(500).json({ error: error.message });
    }
});

/**
 * GET /status/:session_id
 * Check connection status
 */
app.get('/status/:session_id', (req, res) => {
    const { session_id } = req.params;

    const isConnected = activeSockets.has(session_id);

    res.json({
        session_id,
        connected: isConnected,
        status: isConnected ? 'connected' : 'disconnected'
    });
});

/**
 * POST /fetch-messages
 * Fetch messages from a session
 */
app.post('/fetch-messages', async (req, res) => {
    const { session_id, days_back = 30 } = req.body;

    if (!session_id) {
        return res.status(400).json({ error: 'session_id is required' });
    }

    const sock = activeSockets.get(session_id);
    if (!sock) {
        return res.status(404).json({ error: 'Session not connected' });
    }

    console.log(`[Fetch] Fetching messages for session: ${session_id}`);

    try {
        // Get all chats
        const chats = await sock.store?.chats?.all() || [];

        const messages = [];

        // For each chat, get messages
        for (const chat of chats) {
            try {
                const chatMessages = await sock.store?.messages?.[chat.id]?.all() || [];
                messages.push(...chatMessages);
            } catch (err) {
                console.error(`[Error] Failed to fetch messages for chat ${chat.id}:`, err);
            }
        }

        console.log(`[Fetch] Found ${messages.length} total messages`);

        res.json({
            session_id,
            total_messages: messages.length,
            messages: messages.map(msg => ({
                id: msg.key?.id,
                from: msg.key?.remoteJid,
                text: msg.message?.conversation || msg.message?.extendedTextMessage?.text || '',
                timestamp: msg.messageTimestamp,
                from_me: msg.key?.fromMe || false
            }))
        });

    } catch (error) {
        console.error(`[Error] Failed to fetch messages:`, error);
        res.status(500).json({ error: error.message });
    }
});

/**
 * POST /disconnect/:session_id
 * Disconnect a session
 */
app.post('/disconnect/:session_id', async (req, res) => {
    const { session_id } = req.params;

    const sock = activeSockets.get(session_id);
    if (!sock) {
        return res.status(404).json({ error: 'Session not found' });
    }

    console.log(`[Disconnect] Logging out session: ${session_id}`);

    try {
        await sock.logout();
        activeSockets.delete(session_id);

        // Clean up session files
        const sessionPath = path.join(SESSION_DIR, session_id);
        if (fs.existsSync(sessionPath)) {
            fs.rmSync(sessionPath, { recursive: true });
        }

        res.json({
            session_id,
            status: 'disconnected',
            message: 'Session logged out successfully'
        });

    } catch (error) {
        console.error(`[Error] Failed to disconnect:`, error);
        res.status(500).json({ error: error.message });
    }
});

/**
 * Health check
 */
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        active_sessions: activeSockets.size,
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`\n🚀 Baileys WhatsApp Server running on port ${PORT}`);
    console.log(`📱 Ready to handle WhatsApp connections via QR\n`);
});
