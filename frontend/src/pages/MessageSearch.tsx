import React, { useState } from 'react';
import { Search, FileText, Download } from 'lucide-react';

interface Message {
    id: string;
    contact_name: string;
    contact_phone: string;
    message_text: string;
    timestamp: string;
    is_from_me: boolean;
}

const MessageSearch: React.FC = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState<Message[]>([]);
    const [searching, setSearching] = useState(false);

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;

        setSearching(true);
        try {
            const response = await fetch(
                `/api/v1/messages/search?q=${encodeURIComponent(searchQuery)}`
            );
            const data = await response.json();
            setResults(data);
        } catch (error) {
            console.error('Error searching messages:', error);
        } finally {
            setSearching(false);
        }
    };

    const exportConversation = async (contactPhone: string) => {
        try {
            const response = await fetch(`/api/v1/messages/export/${contactPhone}`);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `conversacion_${contactPhone}.pdf`;
            a.click();
        } catch (error) {
            console.error('Error exporting conversation:', error);
        }
    };

    return (
        <div className="p-8">
            <div className="max-w-5xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-3">
                        Buscar en Mensajes Respaldados
                    </h1>
                    <p className="text-xl text-gray-600">
                        Encuentra cualquier conversación aunque haya pasado meses
                    </p>
                </div>

                <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6 mb-8">
                    <div className="flex gap-3">
                        <div className="relative flex-1">
                            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                            <input
                                type="text"
                                placeholder="Buscar por nombre, teléfono o contenido del mensaje..."
                                className="w-full pl-12 pr-4 py-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                            />
                        </div>
                        <button
                            onClick={handleSearch}
                            disabled={searching || !searchQuery.trim()}
                            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-8 py-4 rounded-lg font-bold flex items-center gap-2 transition-all shadow-md"
                        >
                            {searching ? (
                                <>⏳ Buscando...</>
                            ) : (
                                <>
                                    <Search size={20} />
                                    Buscar
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {results.length > 0 && (
                    <div className="space-y-4">
                        <p className="text-gray-600 font-medium mb-4">
                            {results.length} resultado{results.length !== 1 && 's'} encontrado{results.length !== 1 && 's'}
                        </p>

                        {results.map((msg) => (
                            <div
                                key={msg.id}
                                className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow"
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <h3 className="font-bold text-lg text-gray-900">
                                            {msg.contact_name}
                                        </h3>
                                        <p className="text-sm text-gray-500">{msg.contact_phone}</p>
                                    </div>
                                    <span className="text-sm text-gray-500">
                                        {new Date(msg.timestamp).toLocaleString('es-ES')}
                                    </span>
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                                    <p className="text-gray-800 leading-relaxed">
                                        {msg.is_from_me && (
                                            <span className="text-blue-600 font-semibold mr-2">Yo:</span>
                                        )}
                                        {msg.message_text}
                                    </p>
                                </div>

                                <button
                                    onClick={() => exportConversation(msg.contact_phone)}
                                    className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center gap-2 transition-colors"
                                >
                                    <Download size={16} />
                                    📄 Exportar conversación completa a PDF
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {results.length === 0 && searchQuery && !searching && (
                    <div className="text-center py-12 text-gray-500">
                        <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                        <p className="text-lg">No se encontraron mensajes</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MessageSearch;
