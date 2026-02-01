import React from 'react';
import { Download, Database, RefreshCw, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const Settings: React.FC = () => {
    const backups = [
        { id: '1', date: 'Hoy 10:00 AM', size: '25 MB', status: 'success', type: 'Auto' },
        { id: '2', date: 'Ayer 10:00 AM', size: '24 MB', status: 'success', type: 'Auto' },
        { id: '3', date: '25/10/2023 04:30 PM', size: '24 MB', status: 'success', type: 'Manual' },
    ];

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">Ajustes</h1>

            {/* Backup Dashboard */}
            <section className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-6 border-b border-gray-200 bg-gray-50/50">
                    <div className="flex items-center space-x-3">
                        <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                            <Database className="w-6 h-6" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-800">Copia de Seguridad</h2>
                            <p className="text-sm text-gray-600">Gestiona los respaldos de la base de datos.</p>
                        </div>
                    </div>
                </div>

                <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Status Card */}
                    <div className="md:col-span-2 space-y-4">
                        <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 flex items-start">
                            <Shield className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
                            <div>
                                <h4 className="text-sm font-semibold text-blue-900">Estado: Saludable</h4>
                                <p className="text-sm text-blue-700 mt-1 leading-relaxed">
                                    Los respaldos automáticos se ejecutan diariamente a las 00:00 UTC. El último respaldo exitoso fue hace 2 horas.
                                </p>
                            </div>
                        </div>

                        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl hover:border-blue-300 transition-colors">
                            <div>
                                <h4 className="font-medium text-gray-800">Respaldo Manual</h4>
                                <p className="text-sm text-gray-500">Generar una copia inmediata de la base de datos.</p>
                            </div>
                            <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium text-sm shadow-sm active:transform active:scale-95">
                                <RefreshCw className="w-4 h-4 mr-2" />
                                Iniciar Ahora
                            </button>
                        </div>
                    </div>

                    {/* Stats */}
                    <div className="bg-gray-50 rounded-xl p-6 border border-gray-200 flex flex-col justify-center space-y-4">
                        <div className="text-center">
                            <span className="text-3xl font-bold text-gray-800 block">12</span>
                            <span className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Total Respaldos</span>
                        </div>
                        <div className="text-center border-t border-gray-200 pt-4">
                            <span className="text-3xl font-bold text-gray-800 block">1.2 GB</span>
                            <span className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Espacio Usado</span>
                        </div>
                    </div>
                </div>

                {/* Backup List */}
                <div className="border-t border-gray-200">
                    <div className="bg-gray-50 px-6 py-3 border-b border-gray-200">
                        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Actividad Reciente</h3>
                    </div>
                    <ul className="divide-y divide-gray-100">
                        {backups.map((backup) => (
                            <li key={backup.id} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors cursor-default">
                                <div className="flex items-center">
                                    {backup.status === 'success' ? (
                                        <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                                    ) : (
                                        <AlertTriangle className="w-5 h-5 text-amber-500 mr-3" />
                                    )}
                                    <div>
                                        <p className="text-sm font-medium text-gray-900">Base de Datos ({backup.type})</p>
                                        <p className="text-xs text-gray-500">{backup.date} • {backup.size}</p>
                                    </div>
                                </div>
                                <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Descargar">
                                    <Download className="w-5 h-5" />
                                </button>
                            </li>
                        ))}
                    </ul>
                    <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 text-center rounded-b-xl">
                        <button className="text-sm text-blue-600 hover:text-blue-800 font-medium hover:underline">Ver Historial Completo</button>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Settings;
