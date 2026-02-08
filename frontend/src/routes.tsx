import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import DashboardLayout from './layouts/DashboardLayout';
import DashboardHome from './pages/DashboardHome';
import Pricing from './pages/Pricing';
import ConnectExpress from './pages/ConnectExpress';
import ConnectPro from './pages/ConnectPro';
import BackupHistory from './pages/BackupHistory';
import MessageSearch from './pages/MessageSearch';
import Settings from './pages/Settings';
import { useAuth, AuthProvider } from './context/AuthContext';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) return <div>Loading...</div>;

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
};

const AppRoutes: React.FC = () => {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    <Route path="/login" element={<Login />} />

                    <Route path="/dashboard" element={
                        <ProtectedRoute>
                            <DashboardLayout />
                        </ProtectedRoute>
                    }>
                        <Route index element={<DashboardHome />} />
                        <Route path="pricing" element={<Pricing />} />
                        <Route path="connect-express" element={<ConnectExpress />} />
                        <Route path="connect-pro" element={<ConnectPro />} />
                        <Route path="backups" element={<BackupHistory />} />
                        <Route path="search" element={<MessageSearch />} />
                        <Route path="settings" element={<Settings />} />
                    </Route>

                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
};

export default AppRoutes;
