import React from 'react';

const ContactSidebar: React.FC<{ conversationId?: string }> = ({ conversationId }) => {
    if (!conversationId) return <div className="w-80 bg-white border-l border-gray-200 hidden md:block" />;

    return (
        <div className="w-80 bg-white border-l border-gray-200 flex flex-col h-full overflow-y-auto">
            <div className="p-6 text-center">
                <p className="text-gray-500">Contact details for {conversationId}</p>
            </div>
        </div>
    );
};

export default ContactSidebar;
