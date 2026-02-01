import React, { useState, useEffect, useRef } from 'react';
import { Send, Image, Smile, Phone, Video, MoreVertical } from 'lucide-react';
import { inboxApi } from '../../api/services';
import type { Message } from '../../api/services';

interface Props {
    conversationId: string | null;
}

const ChatWindow: React.FC<Props> = ({ conversationId }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [sending, setSending] = useState(false);

    useEffect(() => {
        if (conversationId) {
            loadMessages(conversationId);
            // Poll for messages every 5 seconds (primitive real-time)
            const interval = setInterval(() => loadMessages(conversationId), 5000);
            return () => clearInterval(interval);
        }
    }, [conversationId]);

    const loadMessages = async (id: string) => {
        try {
            const data = await inboxApi.listMessages(id);
            setMessages(data);
            scrollToBottom();
        } catch (error) {
            console.error('Error cargando mensajes', error);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSend = async () => {
        if (!newMessage.trim() || !conversationId) return;
        setSending(true);
        try {
            // Optimistic update could go here
            await inboxApi.sendMessage(conversationId, newMessage); // Note: API needs update to support ID-less send if backend changed
            // Or backend infers contact from conv id.
            setNewMessage('');
            await loadMessages(conversationId);
        } catch (error) {
            console.error('Error enviando mensaje', error);
        } finally {
            setSending(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    if (!conversationId) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center bg-gray-50 h-full text-center p-8">
                <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-sm mb-6">
                    <MessageSquareIcon className="w-10 h-10 text-gray-300" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Selecciona una conversación</h3>
                <p className="text-gray-500 max-w-sm">Elige un contacto de la lista para ver el historial de mensajes o comenzar un chat nuevo.</p>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col h-full bg-[#f0f2f5]">
            {/* Header */}
            <div className="bg-white p-4 border-b border-gray-200 flex justify-between items-center shadow-sm z-10">
                <div className="flex items-center">
                    <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold mr-3">
                        {/* Placeholder for header avatar */}
                        C
                    </div>
                    <div>
                        <h3 className="font-bold text-gray-900">Conversación Activa</h3>
                        <p className="text-xs text-green-500 flex items-center font-medium">
                            <span className="w-2 h-2 rounded-full bg-green-500 mr-1.5 animate-pulse"></span>
                            En línea
                        </p>
                    </div>
                </div>
                <div className="flex items-center space-x-2 text-gray-500">
                    <button className="p-2 hover:bg-gray-100 rounded-full transition-colors"><Phone size={20} /></button>
                    <button className="p-2 hover:bg-gray-100 rounded-full transition-colors"><Video size={20} /></button>
                    <button className="p-2 hover:bg-gray-100 rounded-full transition-colors"><MoreVertical size={20} /></button>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6" style={{ backgroundImage: 'url("https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png")', backgroundRepeat: 'repeat', backgroundSize: '400px' }}>
                {messages.map((msg) => {
                    const isOutbound = msg.direction === 'outbound';
                    return (
                        <div key={msg.id} className={`flex ${isOutbound ? 'justify-end' : 'justify-start'}`}>
                            {!isOutbound && (
                                <div className="w-8 h-8 rounded-full bg-gray-300 mr-2 self-end mb-1"></div>
                            )}
                            <div className={`max-w-[70%] p-3.5 rounded-2xl shadow-sm text-sm relative ${isOutbound
                                    ? 'bg-[#d9fdd3] text-gray-900 rounded-tr-none'
                                    : 'bg-white text-gray-900 rounded-tl-none'
                                }`}>
                                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                                <div className={`text-[10px] mt-1 text-right flex items-center justify-end ${isOutbound ? 'text-green-800/60' : 'text-gray-400'}`}>
                                    {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    {isOutbound && <span className="ml-1 text-blue-500">✓✓</span>}
                                </div>
                            </div>
                        </div>
                    );
                })}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-white p-4 border-t border-gray-200">
                <div className="flex items-center bg-gray-100 rounded-2xl px-4 py-2 border border-transparent focus-within:border-blue-400 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-100 transition-all shadow-inner">
                    <button className="text-gray-500 hover:text-gray-700 p-1 mr-2"><Smile size={24} /></button>
                    <button className="text-gray-500 hover:text-gray-700 p-1 mr-2"><Image size={24} /></button>
                    <input
                        type="text"
                        placeholder="Escribe un mensaje..."
                        className="flex-1 bg-transparent py-2 focus:outline-none text-gray-700"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={sending}
                    />
                    <button
                        onClick={handleSend}
                        disabled={sending || !newMessage.trim()}
                        className={`ml-2 p-2 rounded-full transition-all ${newMessage.trim()
                                ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md transform hover:scale-105 active:scale-95'
                                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            }`}
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
};

// Helper Icon for null state
const MessageSquareIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg>
);

export default ChatWindow;
