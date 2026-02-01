import client from './client';

// Types
export interface Contact {
    id: string;
    name: string;
    phone: string;
    tags: Tag[];
    notes: Note[];
    // ... other fields
}

export interface Tag {
    id: string;
    name: string;
    color: string;
}

export interface Note {
    id: string;
    content: string;
    created_at: string;
}

export interface Conversation {
    id: string;
    contact: Contact;
    last_message: string;
    last_message_at: string;
    unread_count: number;
    status: string;
}

export interface Message {
    id: string;
    content: string;
    direction: 'INBOUND' | 'OUTBOUND';
    created_at: string;
    is_read: boolean;
}

// Contacts Service
export const contactsApi = {
    list: async (skip = 0, limit = 100) => {
        const response = await client.get<Contact[]>('/contacts/', { params: { skip, limit } });
        return response.data;
    },
    create: async (data: { name: string; phone: string; metadata?: any }) => {
        const response = await client.post<Contact>('/contacts/', data);
        return response.data;
    },
    addTag: async (contactId: string, tag: { name: string; color?: string }) => {
        const response = await client.post<Tag>(`/contacts/${contactId}/tags`, tag);
        return response.data;
    },
    addNote: async (contactId: string, content: string) => {
        const response = await client.post<Note>(`/contacts/${contactId}/notes`, { content });
        return response.data;
    }
};

// Inbox/Conversations Service
export const inboxApi = {
    listConversations: async (skip = 0, limit = 50) => {
        const response = await client.get<Conversation[]>('/conversations/', { params: { skip, limit } });
        return response.data;
    },
    listMessages: async (conversationId: string, skip = 0, limit = 50) => {
        const response = await client.get<Message[]>(`/conversations/${conversationId}/messages`, { params: { skip, limit } });
        return response.data;
    },
    sendMessage: async (contactId: string, content: string) => {
        const response = await client.post<{ id: string; status: string }>('/messages/', { contact_id: contactId, content });
        return response.data;
    },
    markRead: async (conversationId: string) => {
        const response = await client.post(`/conversations/${conversationId}/read`);
        return response.data;
    }
};

// Backups Service
export const backupsApi = {
    trigger: async () => {
        const response = await client.post<{ job_id: string; status: string }>('/backups/');
        return response.data;
    },
    getStatus: async (jobId: string) => {
        const response = await client.get(`/backups/${jobId}`);
        // If it returns file, handling might be different, but for status check:
        return response.data;
    }
};
