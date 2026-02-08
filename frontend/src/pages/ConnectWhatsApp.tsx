import React, { useState } from 'react';
import { Shield, CheckCircle } from 'lucide-react';

const ConnectWhatsApp: React.FC = () => {
    const [phoneId, setPhoneId] = useState('');
    const [accessToken, setAccessToken] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleConnect = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/v1/whatsapp/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone_number_id: phoneId,
                    access_token: accessToken
                })
            });

            if (response.ok) {
                setSuccess(true);
            }
        } catch (error) {
            console.error('Error connecting WhatsApp:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-8">
            <div className="text-center mb-8">
                <Shield className="w-16 h-16 text-green-600 mx-auto mb-4" />
                <h1 className="text-4xl font-bold text-gray-900 mb-3">
                    Conecta tu WhatsApp Business
                </h1>
                <p className="text-xl text-gray-600">
                    Protección automática de tus conversaciones en segundos
                </p>
            </div>

            {!success ? (
                <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
                    <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded-lg mb-8">
                        <div className="flex items-start">
                            <CheckCircle className="w-6 h-6 text-blue-600 mr-3 flex-shrink-0 mt-1" />
                            <div>
                                <h3 className="font-bold text-blue-900 mb-2">
                                    🔒 A partir de ahora estás protegido
                                </h3>
                                <p className="text-blue-800">
                                    Todas tus conversaciones se respaldarán automáticamente cada 24 horas.
                                    Aunque WhatsApp se caiga, tus mensajes de venta estarán seguros.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-bold text-gray-700 mb-2">
                                Phone Number ID (Meta Business)
                            </label>
                            <input
                                type="text"
                                className="w-full border-2 border-gray-300 rounded-lg p-3 focus:border-green-500 focus:outline-none transition-colors"
                                placeholder="123456789012345"
                                value={phoneId}
                                onChange={(e) => setPhoneId(e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-bold text-gray-700 mb-2">
                                Access Token
                            </label>
                            <input
                                type="password"
                                className="w-full border-2 border-gray-300 rounded-lg p-3 focus:border-green-500 focus:outline-none transition-colors"
                                placeholder="EAAxxxxxxxxxxxxxxx"
                                value={accessToken}
                                onChange={(e) => setAccessToken(e.target.value)}
                            />
                        </div>

                        <button
                            onClick={handleConnect}
                            disabled={loading || !phoneId || !accessToken}
                            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 text-white font-bold py-4 px-6 rounded-lg text-lg transition-all transform hover:scale-105 active:scale-95 shadow-lg"
                        >
                            {loading ? '⏳ Conectando...' : '🔗 Conectar WhatsApp Ahora'}
                        </button>
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-200">
                        <p className="text-sm text-gray-600 mb-2">
                            📖 ¿Cómo obtener estas credenciales?
                        </p>
                        <a href="/docs/setup" className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                            Ver guía paso a paso →
                        </a>
                    </div>
                </div>
            ) : (
                <div className="bg-green-50 border-2 border-green-500 rounded-2xl p-8 text-center">
                    <CheckCircle className="w-20 h-20 text-green-600 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-green-900 mb-3">
                        ✅ WhatsApp Conectado Exitosamente
                    </h2>
                    <p className="text-green-800 mb-6">
                        Tu primer backup se creará automáticamente en las próximas horas.
                    </p>
                    <button
                        onClick={() => window.location.href = '/backups'}
                        className="bg-green-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-700 transition-colors"
                    >
                        Ver Panel de Backups →
                    </button>
                </div>
            )}
        </div>
    );
};

export default ConnectWhatsApp;
