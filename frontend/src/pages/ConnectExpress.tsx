import React, { useState, useEffect } from 'react';
import { QrCode, CheckCircle, Loader, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ConnectExpress = () => {
    const [qrCode, setQrCode] = useState<string | null>(null);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [connected, setConnected] = useState(false);
    const [countdown, setCountdown] = useState(60);
    const navigate = useNavigate();

    const generateQR = async () => {
        setLoading(true);
        setConnected(false);
        setCountdown(60);

        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(
                'http://localhost:8000/api/v1/baileys/generate-qr',
                {},
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setQrCode(response.data.qr_code);
            setSessionId(response.data.session_id);
        } catch (error: any) {
            console.error('Error generating QR:', error);
            alert(error.response?.data?.detail || 'Failed to generate QR code');
        } finally {
            setLoading(false);
        }
    };

    const checkConnection = async () => {
        if (!sessionId) return;

        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                'http://localhost:8000/api/v1/baileys/status',
                { headers: { Authorization: `Bearer ${token}` } }
            );

            if (response.data.connected) {
                setConnected(true);
                setTimeout(() => navigate('/dashboard'), 2000);
            }
        } catch (error) {
            console.error('Error checking connection:', error);
        }
    };

    // Countdown timer
    useEffect(() => {
        if (qrCode && countdown > 0 && !connected) {
            const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
            return () => clearTimeout(timer);
        }
    }, [countdown, qrCode, connected]);

    // Poll for connection every 3 seconds
    useEffect(() => {
        if (sessionId && !connected) {
            const interval = setInterval(checkConnection, 3000);
            return () => clearInterval(interval);
        }
    }, [sessionId, connected]);

    // Generate QR on mount
    useEffect(() => {
        generateQR();
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
            <div className="max-w-2xl w-full bg-white rounded-2xl shadow-2xl p-8">

                {/* Header */}
                <div className="text-center mb-8">
                    <div className="flex justify-center mb-4">
                        <div className="bg-green-100 p-4 rounded-full">
                            <QrCode className="w-12 h-12 text-green-600" />
                        </div>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Conecta WhatsApp Express
                    </h1>
                    <p className="text-gray-600">
                        Plan Express - Conexión vía código QR
                    </p>
                </div>

                {/* QR Code Display */}
                {!connected ? (
                    <div className="space-y-6">
                        {loading ? (
                            <div className="flex flex-col items-center justify-center py-16">
                                <Loader className="w-12 h-12 text-green-600 animate-spin mb-4" />
                                <p className="text-gray-600">Generando código QR...</p>
                            </div>
                        ) : qrCode ? (
                            <>
                                {/* QR Code */}
                                <div className="flex justify-center p-6 bg-gray-50 rounded-xl">
                                    <img
                                        src={qrCode}
                                        alt="QR Code"
                                        className="w-64 h-64 border-4 border-green-600 rounded-lg"
                                    />
                                </div>

                                {/* Timer */}
                                <div className="text-center">
                                    <p className="text-sm text-gray-500 mb-2">
                                        Código expira en: <span className="font-bold text-green-600">{countdown}s</span>
                                    </p>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-green-600 h-2 rounded-full transition-all duration-1000"
                                            style={{ width: `${(countdown / 60) * 100}%` }}
                                        />
                                    </div>
                                </div>

                                {/* Instructions */}
                                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                                    <h3 className="font-semibold text-blue-900 mb-2">
                                        Instrucciones:
                                    </h3>
                                    <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                                        <li>Abre WhatsApp en tu teléfono</li>
                                        <li>Ve a Configuración → Dispositivos vinculados</li>
                                        <li>Toca "Vincular un dispositivo"</li>
                                        <li>Escanea este código QR</li>
                                    </ol>
                                </div>

                                {/* Regenerate Button */}
                                {countdown === 0 && (
                                    <button
                                        onClick={generateQR}
                                        className="w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white py-3 px-6 rounded-lg font-semibold transition"
                                    >
                                        <RefreshCw className="w-5 h-5" />
                                        Generar Nuevo Código
                                    </button>
                                )}

                                {/* Checking Status */}
                                <div className="text-center">
                                    <Loader className="w-5 h-5 text-green-600 animate-spin mx-auto mb-2" />
                                    <p className="text-sm text-gray-500">
                                        Esperando que escanees el código...
                                    </p>
                                </div>
                            </>
                        ) : null}
                    </div>
                ) : (
                    /* Success State */
                    <div className="text-center py-12">
                        <CheckCircle className="w-20 h-20 text-green-600 mx-auto mb-4" />
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">
                            ¡Conectado Exitosamente!
                        </h2>
                        <p className="text-gray-600 mb-6">
                            WhatsApp está ahora conectado a WhatsBackup
                        </p>
                        <div className="flex items-center justify-center gap-2">
                            <Loader className="w-5 h-5 text-green-600 animate-spin" />
                            <span className="text-gray-600">Redirigiendo al dashboard...</span>
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
};

export default ConnectExpress;
