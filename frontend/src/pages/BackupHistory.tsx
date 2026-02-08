import React, { useState, useEffect } from 'react';
import { Database, Download, RefreshCw, Clock } from 'lucide-react';

interface Backup {
    id: string;
    backup_date: string;
    total_messages: number;
    total_contacts: number;
    status: 'completed' | 'in_progress' | 'failed';
}

const BackupHistory: React.FC = () => {
    const [backups, setBackups] = useState<Backup[]>([]);
    const [creating, setCreating] = useState(false);
    const [stats, setStats] = useState({
        lastBackup: '',
        totalMessages: 0,
        totalContacts: 0
    });

    useEffect(() => {
        loadBackups();
        loadStats();
    }, []);

    const loadBackups = async () => {
        try {
            const response = await fetch('/api/v1/backups/history');
            const data = await response.json();
            setBackups(data);
        } catch (error) {
            console.error('Error loading backups:', error);
        }
    };

    const loadStats = async () => {
        try {
            const response = await fetch('/api/v1/backups/stats');
            const data = await response.json();
            setStats({
                lastBackup: data.last_backup_date || '',
                totalMessages: data.total_messages || 0,
                totalContacts: data.total_contacts || 0
            });
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    };

    const createBackupNow = async () => {
        setCreating(true);
        try {
            await fetch('/api/v1/backups/create', { method: 'POST' });
            await loadBackups();
            await loadStats();
        } catch (error) {
            console.error('Error creating backup:', error);
        } finally {
            setCreating(false);
        }
    };

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Historial de Backups
                    </h1>
                    <p className="text-gray-600">
                        Tus conversaciones están respaldadas y seguras
                    </p>
                </div>
                <button
                    onClick={createBackupNow}
                    disabled={creating}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-bold flex items-center gap-2 shadow-lg transition-all transform hover:scale-105 active:scale-95"
                >
                    {creating ? (
                        <>
                            <RefreshCw className="animate-spin" size={20} />
                            Creando...
                        </>
                    ) : (
                        <>
                            <Database size={20} />
                            Crear Backup Ahora
                        </>
                    )}
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-500 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-3">
                        <Clock className="text-green-600" size={32} />
                    </div>
                    <p className="text-sm text-green-800 font-medium mb-1">Último Backup</p>
                    <p className="text-2xl font-bold text-green-900">
                        {stats.lastBackup ? new Date(stats.lastBackup).toLocaleDateString('es-ES') : 'N/A'}
                    </p>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-500 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-3">
                        <Database className="text-blue-600" size={32} />
                    </div>
                    <p className="text-sm text-blue-800 font-medium mb-1">Mensajes Respaldados</p>
                    <p className="text-2xl font-bold text-blue-900">
                        {stats.totalMessages.toLocaleString()}
                    </p>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-500 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-3">
                        <Download className="text-purple-600" size={32} />
                    </div>
                    <p className="text-sm text-purple-800 font-medium mb-1">Contactos</p>
                    <p className="text-2xl font-bold text-purple-900">
                        {stats.totalContacts}
                    </p>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-50 border-b border-gray-200">
                        <tr>
                            <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Fecha</th>
                            <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Mensajes</th>
                            <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Contactos</th>
                            <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Estado</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {backups.length === 0 ? (
                            <tr>
                                <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                                    No hay backups aún. Crea tu primer backup ahora.
                                </td>
                            </tr>
                        ) : (
                            backups.map((backup) => (
                                <tr key={backup.id} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-6 py-4">
                                        {new Date(backup.backup_date).toLocaleString('es-ES')}
                                    </td>
                                    <td className="px-6 py-4 font-semibold">
                                        {backup.total_messages.toLocaleString()}
                                    </td>
                                    <td className="px-6 py-4 font-semibold">
                                        {backup.total_contacts}
                                    </td>
                                    <td className="px-6 py-4">
                                        {backup.status === 'completed' && (
                                            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-bold">
                                                ✅ Completado
                                            </span>
                                        )}
                                        {backup.status === 'in_progress' && (
                                            <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-bold">
                                                ⏳ En proceso
                                            </span>
                                        )}
                                        {backup.status === 'failed' && (
                                            <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-bold">
                                                ❌ Fallido
                                            </span>
                                        )}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default BackupHistory;
