import React, { useEffect, useState } from 'react';
import { Database, MessageSquare, Users, Clock, TrendingUp, Shield } from 'lucide-react';

interface BackupStats {
    total_backups: number;
    total_messages: number;
    total_contacts: number;
    last_backup_date: string | null;
}

const DashboardHome: React.FC = () => {
    const [stats, setStats] = useState<BackupStats>({
        total_backups: 0,
        total_messages: 0,
        total_contacts: 0,
        last_backup_date: null
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        try {
            const response = await fetch('/api/v1/backups/stats');
            const data = await response.json();
            setStats(data);
        } catch (error) {
            console.error('Error loading stats:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                    <Shield className="text-green-600" size={40} />
                    WhatsBackup Dashboard
                </h1>
                <p className="text-xl text-gray-600">
                    Protege tus conversaciones de WhatsApp con backups automáticos
                </p>
            </div>

            {/* Key Value Proposition */}
            <div className="bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-500 rounded-2xl p-6 mb-8 shadow-lg">
                <div className="flex items-start gap-4">
                    <Shield className="text-green-600 flex-shrink-0" size={48} />
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">
                            ✅ Tus mensajes están protegidos
                        </h2>
                        <p className="text-lg text-gray-700">
                            {stats.last_backup_date ? (
                                <>
                                    Último backup:{' '}
                                    <strong className="text-green-700">
                                        {new Date(stats.last_backup_date).toLocaleDateString('es-ES', {
                                            year: 'numeric',
                                            month: 'long',
                                            day: 'numeric',
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </strong>
                                </>
                            ) : (
                                <span className="text-yellow-700">
                                    Aún no has creado tu primer backup. ¡Conecta WhatsApp para empezar!
                                </span>
                            )}
                        </p>
                        {stats.total_backups > 0 && (
                            <p className="text-sm text-gray-600 mt-2">
                                💾 {stats.total_messages.toLocaleString()} mensajes respaldados de {stats.total_contacts} contactos
                            </p>
                        )}
                    </div>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 p-6 hover:shadow-xl transition-all">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-1">Total Backups</p>
                            <p className="text-3xl font-bold text-gray-900">
                                {loading ? '...' : stats.total_backups}
                            </p>
                        </div>
                        <div className="p-3 bg-green-100 rounded-lg">
                            <Database className="text-green-600" size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500 flex items-center gap-1">
                        <TrendingUp size={12} className="text-green-600" />
                        Respaldos realizados
                    </p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 p-6 hover:shadow-xl transition-all">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-1">Mensajes</p>
                            <p className="text-3xl font-bold text-gray-900">
                                {loading ? '...' : stats.total_messages.toLocaleString()}
                            </p>
                        </div>
                        <div className="p-3 bg-blue-100 rounded-lg">
                            <MessageSquare className="text-blue-600" size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500">Conversaciones guardadas</p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 p-6 hover:shadow-xl transition-all">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-1">Contactos</p>
                            <p className="text-3xl font-bold text-gray-900">
                                {loading ? '...' : stats.total_contacts}
                            </p>
                        </div>
                        <div className="p-3 bg-purple-100 rounded-lg">
                            <Users className="text-purple-600" size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500">Personas respaldadas</p>
                </div>

                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 p-6 hover:shadow-xl transition-all">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-1">Próximo Backup</p>
                            <p className="text-2xl font-bold text-gray-900">
                                {stats.last_backup_date ? (
                                    <>
                                        {Math.round(
                                            (24 - (Date.now() - new Date(stats.last_backup_date).getTime()) / (1000 * 60 * 60))
                                        )}h
                                    </>
                                ) : (
                                    'Pendiente'
                                )}
                            </p>
                        </div>
                        <div className="p-3 bg-orange-100 rounded-lg">
                            <Clock className="text-orange-600" size={24} />
                        </div>
                    </div>
                    <p className="text-xs text-gray-500">Automático cada 24hrs</p>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <a
                    href="/whatsapp/connect"
                    className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 cursor-pointer"
                >
                    <h3 className="text-xl font-bold mb-2">🔗 Conectar WhatsApp</h3>
                    <p className="text-green-50 text-sm">
                        Conecta tu cuenta de WhatsApp Business para comenzar a respaldar
                    </p>
                </a>

                <a
                    href="/backups"
                    className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 cursor-pointer"
                >
                    <h3 className="text-xl font-bold mb-2">📊 Ver Backups</h3>
                    <p className="text-blue-50 text-sm">
                        Revisa el historial completo de tus respaldos automáticos
                    </p>
                </a>

                <a
                    href="/search"
                    className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 cursor-pointer"
                >
                    <h3 className="text-xl font-bold mb-2">🔍 Buscar Mensajes</h3>
                    <p className="text-purple-50 text-sm">
                        Encuentra cualquier conversación en segundos
                    </p>
                </a>
            </div>

            {/* Features Info */}
            <div className="mt-12 bg-white rounded-xl shadow-lg border border-gray-200 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    ¿Por qué WhatsBackup?
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="flex gap-4">
                        <div className="text-4xl">🔒</div>
                        <div>
                            <h3 className="font-bold text-gray-900 mb-1">Seguridad Total</h3>
                            <p className="text-gray-600 text-sm">
                                Tus mensajes se guardan en TU base de datos. Nadie más tiene acceso.
                            </p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-4xl">⚡</div>
                        <div>
                            <h3 className="font-bold text-gray-900 mb-1">Backups Automáticos</h3>
                            <p className="text-gray-600 text-sm">
                                Respaldo diario sin que tengas que hacer nada. Configura y olvídate.
                            </p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-4xl">📄</div>
                        <div>
                            <h3 className="font-bold text-gray-900 mb-1">Exportación Legal</h3>
                            <p className="text-gray-600 text-sm">
                                Exporta conversaciones a PDF para auditorías, contabilidad o documentación legal.
                            </p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-4xl">🚀</div>
                        <div>
                            <h3 className="font-bold text-gray-900 mb-1">Continuidad Operativa</h3>
                            <p className="text-gray-600 text-sm">
                                Accede a tus mensajes aunque WhatsApp esté caído. Tus ventas nunca paran.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardHome;
