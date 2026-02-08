import React, { useState } from 'react';
import { Check, Zap, Shield, TrendingUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Pricing = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSelectPlan = async (planType: 'express' | 'pro') => {
        setLoading(true);

        try {
            const token = localStorage.getItem('token');
            await axios.post(
                'http://localhost:8000/api/v1/plans/select',
                { plan_type: planType },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            // Redirect to appropriate connection page
            if (planType === 'express') {
                navigate('/dashboard/connect-express');
            } else {
                navigate('/dashboard/connect-pro');
            }
        } catch (error) {
            console.error('Error selecting plan:', error);
            alert('Failed to select plan. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-5xl font-bold text-gray-900 mb-4">
                        Elige tu Plan WhatsBackup
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Protege tus conversaciones de WhatsApp con backups automáticos.
                        Nunca más pierdas mensajes importantes.
                    </p>
                </div>

                {/* Plans Container */}
                <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">

                    {/* Express Plan */}
                    <div className="bg-white rounded-2xl shadow-xl overflow-hidden border-2 border-green-200 hover:border-green-400 transition-all duration-300 transform hover:-translate-y-2">
                        <div className="bg-gradient-to-r from-green-500 to-green-600 px-8 py-6 text-white">
                            <div className="flex items-center gap-3 mb-2">
                                <Zap className="w-8 h-8" />
                                <h2 className="text-3xl font-bold">Plan Express</h2>
                            </div>
                            <p className="text-green-100">Para negocios pequeños</p>
                        </div>

                        <div className="px-8 py-8">
                            {/* Price */}
                            <div className="mb-6">
                                <div className="flex items-baseline gap-2">
                                    <span className="text-5xl font-bold text-gray-900">$18</span>
                                    <span className="text-gray-600">/mes</span>
                                </div>
                                <p className="text-sm text-gray-500 mt-1">Facturación mensual</p>
                            </div>

                            {/* Features */}
                            <ul className="space-y-4 mb-8">
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Conexión vía código QR (sin API)</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Backups automáticos cada 12 horas</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Hasta 5,000 mensajes/mes</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Búsqueda de mensajes</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Exportar a PDF</span>
                                </li>
                            </ul>

                            {/* CTA Button */}
                            <button
                                onClick={() => handleSelectPlan('express')}
                                disabled={loading}
                                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                            >
                                {loading ? 'Procesando...' : 'Elegir Express'}
                            </button>

                            <p className="text-xs text-center text-gray-500 mt-4">
                                7 días de prueba gratis
                            </p>
                        </div>
                    </div>

                    {/* Pro Plan */}
                    <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border-4 border-blue-500 relative transform hover:-translate-y-2 transition-all duration-300">
                        {/* Popular Badge */}
                        <div className="absolute top-4 right-4 bg-yellow-400 text-yellow-900 px-4 py-1 rounded-full text-sm font-bold">
                            Más Popular
                        </div>

                        <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-6 text-white">
                            <div className="flex items-center gap-3 mb-2">
                                <Shield className="w-8 h-8" />
                                <h2 className="text-3xl font-bold">Plan Pro</h2>
                            </div>
                            <p className="text-blue-100">Para negocios establecidos</p>
                        </div>

                        <div className="px-8 py-8">
                            {/* Price */}
                            <div className="mb-6">
                                <div className="flex items-baseline gap-2">
                                    <span className="text-5xl font-bold text-gray-900">$35</span>
                                    <span className="text-gray-600">/mes</span>
                                </div>
                                <p className="text-sm text-gray-500 mt-1">Facturación mensual</p>
                            </div>

                            {/* Features */}
                            <ul className="space-y-4 mb-8">
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700 font-semibold">WhatsApp Business API oficial</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Backups automáticos cada 24 horas</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700 font-semibold">Mensajes ilimitados</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Multi-dispositivo</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Búsqueda avanzada</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <Check className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Exportar a PDF</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <TrendingUp className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">Herramientas de negocio</span>
                                </li>
                            </ul>

                            {/* CTA Button */}
                            <button
                                onClick={() => handleSelectPlan('pro')}
                                disabled={loading}
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                            >
                                {loading ? 'Procesando...' : 'Elegir Pro'}
                            </button>

                            <p className="text-xs text-center text-gray-500 mt-4">
                                14 días de prueba gratis
                            </p>
                        </div>
                    </div>

                </div>

                {/* FAQ/Info Section */}
                <div className="mt-16 text-center">
                    <h3 className="text-2xl font-bold text-gray-900 mb-6">
                        ¿No estás seguro cuál elegir?
                    </h3>
                    <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h4 className="font-semibold text-gray-900 mb-2">Plan Express</h4>
                            <p className="text-sm text-gray-600">
                                Ideal para tiendas pequeñas, emprendedores y negocios que empiezan.
                            </p>
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h4 className="font-semibold text-gray-900 mb-2">Plan Pro</h4>
                            <p className="text-sm text-gray-600">
                                Perfecto para empresas con alto volumen de mensajes y múltiples agentes.
                            </p>
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow-md">
                            <h4 className="font-semibold text-gray-900 mb-2">Fácil Upgrade</h4>
                            <p className="text-sm text-gray-600">
                                Puedes cambiar de Express a Pro en any momento desde Ajustes.
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Pricing;
