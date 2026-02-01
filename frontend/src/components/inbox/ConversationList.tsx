import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { inboxApi } from '../../api/services';
import type { Conversation } from '../../api/services';

interface Props {
    onSelectConversation: (id: string) => void;
    selectedId: string | null;
}

const ConversationList: React.FC<Props> = ({ onSelectConversation, selectedId }) => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadConversations();
    }, []);

    const loadConversations = async () => {
        try {
            const data = await inboxApi.listConversations();
            setConversations(data);
        } catch (error) {
            console.error('Error cargando conversaciones', error);
        }
    };

    const filteredConversations = conversations.filter(c =>
        c.contact.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex flex-col h-full bg-white border-r border-gray-200 w-80">
            <div className="p-4 border-b border-gray-200 bg-gray-50/50">
                <h2 className="text-xl font-bold mb-4 text-gray-800">Mensajes</h2>
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Buscar chats..."
                        className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white shadow-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <Search className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                </div>
            </div>

            <div className="flex-1 overflow-y-auto">
                {filteredConversations.map((conv) => (
                    <div
                        key={conv.id}
                        onClick={() => onSelectConversation(conv.id)}
                        className={`flex items-center p-4 cursor-pointer hover:bg-gray-50 transition-all border-b border-gray-50 ${selectedId === conv.id ? 'bg-blue-50 border-blue-100' : ''}`}
                    >
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold mr-3 shrink-0 shadow-sm border border-white ${selectedId === conv.id ? 'bg-blue-200 text-blue-700' : 'bg-gray-100 text-gray-500'}`}>
                            {conv.contact.name.charAt(0)}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex justify-between items-baseline mb-1">
                                <h3 className={`text-sm font-semibold truncate ${selectedId === conv.id ? 'text-blue-900' : 'text-gray-900'}`}>
                                    {conv.contact.name}
                                </h3>
                                <span className="text-xs text-gray-400 font-medium whitespace-nowrap ml-2">
                                    {new Date(conv.last_message_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className={`text-sm truncate mr-2 ${selectedId === conv.id ? 'text-blue-700/80' : 'text-gray-500'}`}>
                                    {conv.last_message || <span className="italic opacity-75">Imagen o Archivo adjunto</span>}
                                </p>
                                {conv.unread_count > 0 && (
                                    <span className="bg-blue-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full shadow-sm min-w-[1.25rem] text-center">
                                        {conv.unread_count}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                {filteredConversations.length === 0 && (
                    <div className="p-8 text-center text-gray-400 text-sm">
                        No se encontraron chats recientes.
                    </div>
                )}
            </div>
        </div>
    );
};

export default ConversationList;
