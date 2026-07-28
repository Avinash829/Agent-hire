/**
 * History Page Component.
 *
 * Displays paginated list of all verification history
 * for the authenticated user.
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useHistory } from "../hooks/useHistory";
import VerificationHistoryItem from "../components/dashboard/VerificationHistoryItem";
import Card from "../components/common/Card";
import Spinner from "../components/common/Spinner";
import Button from "../components/common/Button";

export default function HistoryPage() {
    const { isAuthenticated, loading: authLoading } = useAuth();
    const { items, total, loading, loadHistory, loadDetail } = useHistory();
    const [page, setPage] = useState(1);
    const navigate = useNavigate();
    const limit = 20;
    const totalPages = Math.ceil(total / limit);

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            navigate("/login");
        }
    }, [isAuthenticated, authLoading, navigate]);

    useEffect(() => {
        if (isAuthenticated) {
            loadHistory(page, limit);
        }
    }, [isAuthenticated, page, loadHistory]);

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

    return (
        <div className="page-container">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-2xl font-bold text-gray-900">
                        Verification History
                    </h1>
                    <p className="text-gray-600 mt-1">
                        View all your past job posting verifications ({total}{" "}
                        total)
                    </p>
                </div>

                <Card>
                    {loading ? (
                        <Spinner message="Loading history..." />
                    ) : items.length === 0 ? (
                        <div className="text-center py-12">
                            <svg
                                className="w-16 h-16 text-gray-300 mx-auto mb-4"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={1.5}
                                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                                />
                            </svg>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                No Verifications Yet
                            </h3>
                            <p className="text-gray-500 mb-6">
                                Start by verifying your first job posting.
                            </p>
                            <Button onClick={() => navigate("/verify")}>
                                Verify a Job
                            </Button>
                        </div>
                    ) : (
                        <>
                            <div className="space-y-3 mb-6">
                                {items.map((item) => (
                                    <VerificationHistoryItem
                                        key={item.verification_id}
                                        item={item}
                                        onClick={handleViewDetail}
                                    />
                                ))}
                            </div>

                            <div className="flex items-center justify-between border-t border-gray-200 pt-4">
                                <p className="text-sm text-gray-500">
                                    Page {page} of {totalPages || 1}
                                </p>
                                <div className="flex space-x-2">
                                    <button
                                        onClick={() =>
                                            setPage((p) => Math.max(1, p - 1))
                                        }
                                        disabled={page <= 1}
                                        className="btn-secondary text-sm disabled:opacity-50"
                                    >
                                        Previous
                                    </button>
                                    <button
                                        onClick={() =>
                                            setPage((p) =>
                                                Math.min(totalPages, p + 1)
                                            )
                                        }
                                        disabled={page >= totalPages}
                                        className="btn-secondary text-sm disabled:opacity-50"
                                    >
                                        Next
                                    </button>
                                </div>
                            </div>
                        </>
                    )}
                </Card>
            </div>
        </div>
    );
}
