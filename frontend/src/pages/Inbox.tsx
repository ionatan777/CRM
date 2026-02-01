import React, { useState } from 'react';
import ConversationList from '../components/inbox/ConversationList';
import ChatWindow from '../components/inbox/ChatWindow';
import ContactSidebar from '../components/inbox/ContactSidebar';

const Inbox: React.FC = () => {
    const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);

    return (
        <div className="flex h-[calc(100vh-theme(spacing.24))] bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <ConversationList onSelectConversation={setSelectedConversationId} selectedId={selectedConversationId} />
            <ChatWindow conversationId={selectedConversationId || undefined} />
            <ContactSidebar conversationId={selectedConversationId || undefined} />
        </div>
    );
};

export default Inbox;
