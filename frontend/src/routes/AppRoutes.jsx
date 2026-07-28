/**
 * Application Routes Configuration.
 *
 * Defines all application routes with lazy loading for code splitting.
 */

import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import Spinner from "../components/common/Spinner";

const LandingPage = lazy(() => import("../pages/LandingPage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const VerifyPage = lazy(() => import("../pages/VerifyPage"));
const DashboardPage = lazy(() => import("../pages/DashboardPage"));
const HistoryPage = lazy(() => import("../pages/HistoryPage"));
const HistoryDetailPage = lazy(() => import("../pages/HistoryDetailPage"));
const NotFoundPage = lazy(() => import("../pages/NotFoundPage"));

function LazyFallback() {
    return (
        <div className="min-h-[80vh] flex items-center justify-center">
            <Spinner message="Loading..." />
        </div>
    );
}

export default function AppRoutes() {
    return (
        <Suspense fallback={<LazyFallback />}>
            <Routes>
                <Route element={<MainLayout />}>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/verify" element={<VerifyPage />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/history" element={<HistoryPage />} />
                    <Route
                        path="/history/:id"
                        element={<HistoryDetailPage />}
                    />
                    <Route path="*" element={<NotFoundPage />} />
                </Route>
            </Routes>
        </Suspense>
    );
}
