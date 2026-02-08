import React, { useState } from 'react';
import { Shield, Key, CheckCircle, AlertCircle, ExternalLink } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ConnectPro = () => {
    const [formData, setFormData] = useState({
        phoneNumberId: '',
        accessToken: ''
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            await axios.post(
                'http://localhost:8000/api/v1/whatsapp/connect',
                {
                    phone_number_id: formData.phoneNumberId,
                    access_token: formData.accessToken
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setSuccess(true);
            setTimeout(() => navigate('/dashboard'), 2000);
        } catch (err: any) {
            console.error('Error connecting:', err);
            setError(err.response?.data?.detail || 'Failed to connect WhatsApp Business API');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
            <div className="max-w-2xl w-full bg-white rounded-2xl shadow-2xl p-8">

                {/* Header */}
                <div className="text-center mb-8">
                    <div className="flex justify-center mb-4">
                        <div className="bg-blue-100 p-4 rounded-full">
                            <Shield className="w-12 h-12 text-blue-600" />
                        </div>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Conecta WhatsApp Pro
                    </h1>
                    <p className="text-gray-600">
                        Plan Pro - WhatsApp Business API oficial
                    </p>
                </div>

                {!success ? (
                    <div className="space-y-6">

                        {/* Help Banner */}
                        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                            <div className="flex items-start gap-3">
                                <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                <div>
                                    <h3 className="font-semibold text-blue-900 mb-1">
                                        ¿Necesitas ayuda para obtener las credenciales?
                                    </h3>
                                    <p className="text-sm text-blue-800 mb-2">
                                        Sigue nuestra guía paso a paso para configurar WhatsApp Business API
                                    </p>
                                    <a
                                        href="https://developers.facebook.com/docs/whatsapp/business-management-api/get-started"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="inline-flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800 font-semibold"
                                    >
                                        Ver Guía de Meta
                                        <ExternalLink className="w-4 h-4" />
                                    </a>
                                </div>
                            </div>
                        </div>

                        {/* Form */}
                        <form onSubmit={handleSubmit} className="space-y-6">

                            {/* Phone Number ID */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
                                    <Key className="w-4 h-4" />
                                    Phone Number ID
                                </label>
                                <input
                                    type="text"
                                    value={formData.phoneNumberId}
                                    onChange={(e) => setFormData({ ...formData, phoneNumberId: e.target.value })}
                                    placeholder="123456789012345"
                                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition"
                                    required
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Lo encuentras en Meta Business Manager → WhatsApp → Empezar
                                </p>
                            </div>

                            {/* Access Token */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
                                    <Shield className="w-4 h-4" />
                                    Access Token
                                </label>
                                <textarea
                                    value={formData.accessToken}
                                    onChange={(e) => setFormData({ ...formData, accessToken: e.target.value })}
                                    placeholder="EAAxxxxxxxxxxxxxxxxxxxx..."
                                    rows={4}
                                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none transition font-mono text-sm"
                                    required
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Token temporal o permanente de tu aplicación de WhatsApp Business
                                </p>
                            </div>

                            {/* Error Message */}
                            {error && (
                                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                                    <div className="flex items-start gap-3">
                                        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                                        <p className="text-sm text-red-800">{error}</p>
                                    </div>
                                </div>
                            )}

                            {/* Submit Button */}
                            <button
                                type="submit"
                                disabled={loading || !formData.phoneNumberId || !formData.accessToken}
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                        Conectando...
                                    </>
                                ) : (
                                    <>
                                        <Shield className="w-5 h-5" />
                                        Conectar WhatsApp Business API
                                    </>
                                )}
                            </button>

                        </form>

                        {/* Info Sections */}
                        <div className="grid md:grid-cols-2 gap-4 pt-6 border-t">
                            <div>
                                <h4 className="font-semibold text-gray-900 mb-2 text-sm">
                                    ✓ Conexión Segura
                                </h4>
                                <p className="text-xs text-gray-600">
                                    Tus credenciales se encriptan y guardan de forma segura
                                </p>
                            </div>
                            <div>
                                <h4 className="font-semibold text-gray-900 mb-2 text-sm">
                                    ✓ Verificación Automática
                                </h4>
                                <p className="text-xs text-gray-600">
                                    Probamos la conexión antes de guardar
                                </p>
                            </div>
                        </div>

                    </div>
                ) : (
                    /* Success State */
                    <div className="text-center py-12">
                        <CheckCircle className="w-20 h-20 text-green-600 mx-auto mb-4" />
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">
                            ¡Conectado Exitosamente!
                        </h2>
                        <p className="text-gray-600 mb-6">
                            WhatsApp Business API está ahora conectado
                        </p>
                        <div className="flex items-center justify-center gap-2">
                            <div className="w-5 h-5 border-2 border-green-600 border-t-transparent rounded-full animate-spin" />
                            <span className="text-gray-600">Redirigiendo al dashboard...</span>
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
};

export default ConnectPro;
