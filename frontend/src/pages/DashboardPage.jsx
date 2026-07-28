/**
 * Dashboard Page Component.
 *
 * Displays user's verification statistics and summary overview.
 */

import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useHistory } from "../hooks/useHistory";
import ScoreCard from "../components/dashboard/ScoreCard";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import VerificationHistoryItem from "../components/dashboard/VerificationHistoryItem";

export default function DashboardPage() {
    const { isAuthenticated, loading: authLoading, user } = useAuth();
    const {
        items,
        total,
        loading: historyLoading,
        loadHistory,
        loadDetail,
    } = useHistory();
    const navigate = useNavigate();

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            navigate("/login");
        }
    }, [isAuthenticated, authLoading, navigate]);

    useEffect(() => {
        if (isAuthenticated) {
            loadHistory(1, 5);
        }
    }, [isAuthenticated, loadHistory]);

    if (authLoading) {
        return (
            <div className="min-h-[80vh] flex items-center justify-center">
                <div className="animate-spin h-10 w-10 border-4 border-primary-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    const handleViewDetail = (verificationId) => {
        navigate(`/history/${verificationId}`);
    };

    const recentItems = items.slice(0, 5);
    const averageScore = items.length
        ? items.reduce((acc, item) => acc + (item.overall_score || 0), 0) /
          items.length
        : null;

    const fraudulentCount = items.filter(
        (item) => item.verdict?.toLowerCase() === "fraudulent"
    ).length;

    const suspiciousCount = items.filter(
        (item) => item.verdict?.toLowerCase() === "suspicious"
    ).length;

    return (
        <div className="page-container">
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600 mt-1">
                    Welcome back, {user?.name || "User"}
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <p className="text-sm font-medium text-gray-500 mb-2">
                        Total Verifications
                    </p>
                    <p className="text-3xl font-bold text-gray-900">{total}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <p className="text-sm font-medium text-gray-500 mb-2">
                        Suspicious
                    </p>
                    <p className="text-3xl font-bold text-warning-600">
                        {suspiciousCount}
                    </p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <p className="text-sm font-medium text-gray-500 mb-2">
                        Fraudulent
                    </p>
                    <p className="text-3xl font-bold text-danger-600">
                        {fraudulentCount}
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2">
                    <Card>
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold text-gray-900">
                                Recent Verifications
                            </h2>
                            <Link
                                to="/history"
                                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                            >
                                View All
                            </Link>
                        </div>
                        {historyLoading ? (
                            <div className="space-y-4">
                                {[1, 2, 3].map((i) => (
                                    <div
                                        key={i}
                                        className="animate-pulse bg-gray-100 rounded-lg h-24"
                                    />
                                ))}
                            </div>
                        ) : recentItems.length > 0 ? (
                            <div className="space-y-3">
                                {recentItems.map((item) => (
                                    <VerificationHistoryItem
                                        key={item.verification_id}
                                        item={item}
                                        onClick={handleViewDetail}
                                    />
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-8">
                                <p className="text-gray-500 mb-4">
                                    No verifications yet
                                </p>
                                <Link to="/verify">
                                    <Button>Verify Your First Job</Button>
                                </Link>
                            </div>
                        )}
                    </Card>
                </div>

                <div>
                    <Card>
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">
                            Quick Actions
                        </h2>
                        <div className="space-y-3">
                            <Link to="/verify">
                                <Button className="w-full justify-center">
                                    Verify New Job
                                </Button>
                            </Link>
                            <Link to="/history">
                                <Button
                                    variant="secondary"
                                    className="w-full justify-center"
                                >
                                    View History
                                </Button>
                            </Link>
                        </div>
                    </Card>

                    {averageScore !== null && (
                        <Card className="mt-6">
                            <h2 className="text-lg font-semibold text-gray-900 mb-4">
                                Average Risk Score
                            </h2>
                            <p className="text-3xl font-bold text-gray-900">
                                {(averageScore * 100).toFixed(0)}%
                            </p>
                            <p className="text-sm text-gray-500 mt-1">
                                Across {total} verification
                                {total !== 1 ? "s" : ""}
                            </p>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}
