import React from 'react';
import { Users, MessageSquare, Archive, Activity, DollarSign, TrendingUp, Briefcase } from 'lucide-react';

const StatCard: React.FC<{ title: string; value: string; icon: React.ReactNode; color: string; trend?: string }> = ({ title, value, icon, color, trend }) => (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center hover:shadow-md transition-shadow">
        <div className={`p-4 rounded-xl ${color} text-white mr-5 shadow-sm`}>
            {icon}
        </div>
        <div>
            <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
            <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
            {trend && <p className="text-xs text-green-600 font-medium mt-1 flex items-center"><TrendingUp className="w-3 h-3 mr-1" /> {trend}</p>}
        </div>
    </div>
);

const DashboardHome: React.FC = () => {
    return (
        <div className="space-y-8 animate-fade-in">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Panel de Control</h1>
                <p className="text-gray-500 mt-2">Bienvenido de nuevo, Administrador. Aquí tienes el resumen de hoy.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Ingresos Totales"
                    value="$45,231.89"
                    icon={<DollarSign className="w-6 h-6" />}
                    color="bg-gradient-to-br from-green-400 to-green-600"
                    trend="+20.1% este mes"
                />
                <StatCard
                    title="Nuevos Clientes"
                    value="125"
                    icon={<Users className="w-6 h-6" />}
                    color="bg-gradient-to-br from-blue-400 to-blue-600"
                    trend="+12 nuevos hoy"
                />
                <StatCard
                    title="Chats Activos"
                    value="42"
                    icon={<MessageSquare className="w-6 h-6" />}
                    color="bg-gradient-to-br from-purple-400 to-purple-600"
                    trend="5 requieren atención"
                />
                <StatCard
                    title="Tasa de Cierre"
                    value="28%"
                    icon={<Briefcase className="w-6 h-6" />}
                    color="bg-gradient-to-br from-orange-400 to-orange-600"
                    trend="+2.4% vs semana pasada"
                />
            </div>

            {/* Main Dashboard Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column (Activities) */}
                <div className="lg:col-span-2 space-y-8">
                    {/* Recent Activity */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="font-bold text-lg text-gray-800">Mensajes Recientes</h3>
                            <button className="text-blue-600 text-sm font-medium hover:text-blue-700 hover:underline">Ver Todos</button>
                        </div>
                        <div className="space-y-4">
                            {[
                                { name: "María García", msg: "Hola, me interesa la cotización...", time: "Hace 2 min", initial: "M", color: "bg-pink-100 text-pink-600" },
                                { name: "Juan Pérez", msg: "¿Tienen soporte técnico hoy?", time: "Hace 15 min", initial: "J", color: "bg-blue-100 text-blue-600" },
                                { name: "Empresa Tech SA", msg: "Confirmamos la orden de compra.", time: "Hace 1 hora", initial: "E", color: "bg-purple-100 text-purple-600" },
                            ].map((item, i) => (
                                <div key={i} className="flex items-center p-3 hover:bg-gray-50 rounded-xl transition-colors cursor-pointer group">
                                    <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg mr-4 ${item.color}`}>
                                        {item.initial}
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex justify-between">
                                            <p className="font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{item.name}</p>
                                            <span className="text-xs text-gray-400">{item.time}</span>
                                        </div>
                                        <p className="text-sm text-gray-500 truncate">{item.msg}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Sales Pipeline (Mock) */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <h3 className="font-bold text-lg text-gray-800 mb-6">Embudo de Ventas (Pipeline)</h3>
                        <div className="flex justify-between space-x-4 overflow-x-auto pb-2">
                            {[
                                { label: "Prospecto", count: 15, amt: "$10k", color: "border-gray-200" },
                                { label: "Contactado", count: 8, amt: "$15k", color: "border-blue-400" },
                                { label: "Propuesta", count: 12, amt: "$45k", color: "border-yellow-400" },
                                { label: "Negociación", count: 4, amt: "$20k", color: "border-orange-400" },
                                { label: "Cerrado", count: 25, amt: "$120k", color: "border-green-400" },
                            ].map((stage, i) => (
                                <div key={i} className={`flex-1 min-w-[120px] border-t-4 ${stage.color} bg-gray-50 p-4 rounded-b-xl`}>
                                    <p className="text-xs text-gray-500 uppercase font-bold tracking-wider mb-1">{stage.label}</p>
                                    <p className="text-2xl font-bold text-gray-800">{stage.count}</p>
                                    <p className="text-xs text-gray-400">{stage.amt}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column (Status & Tasks) */}
                <div className="space-y-8">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <h3 className="font-bold text-lg text-gray-800 mb-6">Estado del Sistema</h3>
                        <div className="space-y-6">
                            <div>
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-sm text-gray-600 flex items-center"><Activity className="w-4 h-4 mr-2 text-green-500" /> API Server</span>
                                    <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded">Normal</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-1.5">
                                    <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '98%' }}></div>
                                </div>
                            </div>
                            <div>
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-sm text-gray-600 flex items-center"><Archive className="w-4 h-4 mr-2 text-blue-500" /> Database</span>
                                    <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">Respaldo hace 2h</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-1.5">
                                    <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '100%' }}></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-2xl shadow-lg p-6 text-white text-center">
                        <h3 className="font-bold text-xl mb-2">Plan Pro</h3>
                        <p className="text-indigo-100 text-sm mb-6">Desbloquea análisis avanzados y usuarios ilimitados.</p>
                        <button className="bg-white text-indigo-600 px-6 py-2 rounded-lg font-bold hover:bg-indigo-50 transition-colors w-full">
                            Actualizar Ahora
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardHome;
