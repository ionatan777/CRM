import React, { useState, useEffect } from 'react';
import { Search, MoreHorizontal, UserPlus, Phone } from 'lucide-react';
import { contactsApi } from '../api/services';
import type { Contact } from '../api/services';

const Contacts: React.FC = () => {
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchContacts();
    }, []);

    const fetchContacts = async () => {
        try {
            const data = await contactsApi.list();
            setContacts(data);
        } catch (error) {
            console.error('Error al cargar contactos', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredContacts = contacts.filter(contact =>
        contact.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) return (
        <div className="h-full flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
    );

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 h-full flex flex-col overflow-hidden animate-fade-in">
            {/* Header */}
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-white">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">Contactos</h1>
                    <p className="text-sm text-gray-500 mt-1">Gestiona tus relaciones y clientes potenciales.</p>
                </div>
                <button className="flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl transition-all shadow-md hover:shadow-lg font-medium">
                    <UserPlus className="w-5 h-5 mr-2" />
                    Nuevo Contacto
                </button>
            </div>

            {/* Toolbar */}
            <div className="p-4 bg-gray-50 border-b border-gray-100 flex items-center justify-between">
                <div className="relative w-full max-w-md">
                    <input
                        type="text"
                        placeholder="Buscar por nombre, teléfono..."
                        className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white transition-all hover:border-blue-300"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <Search className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                </div>
            </div>

            {/* Table */}
            <div className="flex-1 overflow-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider sticky top-0 z-10 font-semibold">
                            <th className="p-4 border-b border-gray-100">Nombre</th>
                            <th className="p-4 border-b border-gray-100">Contacto</th>
                            <th className="p-4 border-b border-gray-100">Etiquetas</th>
                            <th className="p-4 border-b border-gray-100 text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                        {filteredContacts.map((contact) => (
                            <tr key={contact.id} className="hover:bg-blue-50/50 transition-colors group">
                                <td className="p-4">
                                    <div className="flex items-center">
                                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-blue-600 font-bold mr-3 text-sm border border-blue-200">
                                            {contact.name.split(' ').map(n => n[0]).join('')}
                                        </div>
                                        <div>
                                            <div className="font-semibold text-gray-900 group-hover:text-blue-700 transition-colors">{contact.name}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="p-4">
                                    <div className="flex flex-col text-sm">
                                        <div className="flex items-center text-gray-600 bg-gray-100 w-fit px-2 py-1 rounded-lg">
                                            <Phone className="w-3 h-3 mr-2" />
                                            {contact.phone}
                                        </div>
                                    </div>
                                </td>
                                <td className="p-4">
                                    <div className="flex flex-wrap gap-2">
                                        {contact.tags && contact.tags.map(tag => (
                                            <span
                                                key={tag.id}
                                                className="px-2.5 py-0.5 rounded-md text-xs font-bold border"
                                                style={{
                                                    backgroundColor: `${tag.color}15`,
                                                    color: tag.color,
                                                    borderColor: `${tag.color}30`
                                                }}
                                            >
                                                {tag.name}
                                            </span>
                                        ))}
                                        {(!contact.tags || contact.tags.length === 0) && (
                                            <span className="text-gray-400 text-xs italic">Sin etiquetas</span>
                                        )}
                                    </div>
                                </td>
                                <td className="p-4 text-right">
                                    <button className="text-gray-400 hover:text-blue-600 p-2 rounded-full hover:bg-blue-50 transition-colors">
                                        <MoreHorizontal className="w-5 h-5" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {filteredContacts.length === 0 && (
                            <tr>
                                <td colSpan={4} className="p-12 text-center text-gray-400">
                                    No se encontraron contactos.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Contacts;
