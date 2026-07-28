/**
 * History Detail Page Component.
 *
 * Displays detailed verification results for a single record.
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { useHistory } from "../hooks/useHistory";

import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Spinner from "../components/common/Spinner";

import HistoryHeader from "../components/history/HistoryHeader";
import ScoreSection from "../components/history/ScoreSection";
import ReasonsSection from "../components/history/ReasonsSection";
import RecommendationsSection from "../components/history/RecommendationsSection";
import EvidenceSection from "../components/history/EvidenceSection";
import MetadataSection from "../components/history/MetadataSection";

import { getVerdictColor } from "../utils/formatters";

export default function HistoryDetailPage() {
    const navigate = useNavigate();

    const { id } = useParams();

    const { isAuthenticated, loading: authLoading } = useAuth();

    const { loading, loadDetail } = useHistory();

    const [detail, setDetail] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            navigate("/login");
        }
    }, [authLoading, isAuthenticated, navigate]);

    useEffect(() => {
        if (!isAuthenticated || !id) {
            return;
        }

        async function fetchHistoryDetail() {
            try {
                const response = await loadDetail(id);
                setDetail(response);
            } catch (err) {
                setError(
                    err?.customMessage || "Failed to load verification details."
                );
            }
        }

        fetchHistoryDetail();
    }, [id, isAuthenticated, loadDetail]);

    if (authLoading) {
        return (
            <div className="page-container">
                <Spinner message="Checking authentication..." />
            </div>
        );
    }

    if (loading || !detail) {
        return (
            <div className="page-container">
                <Spinner message="Loading verification details..." />
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-container">
                <div className="max-w-3xl mx-auto">
                    <Card>
                        <div className="py-10 text-center">
                            <svg
                                className="mx-auto mb-4 h-16 w-16 text-red-400"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={1.5}
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                                />
                            </svg>

                            <h2 className="mb-2 text-xl font-semibold text-gray-900">
                                Verification Not Found
                            </h2>

                            <p className="mb-6 text-gray-500">{error}</p>

                            <Button onClick={() => navigate("/history")}>
                                Back to History
                            </Button>
                        </div>
                    </Card>
                </div>
            </div>
        );
    }

    const verdictColor = getVerdictColor(detail?.verdict);

    return (
        <div className="page-container">
            <div className="mx-auto max-w-4xl">
                <Card>
                    <HistoryHeader
                        verdict={detail?.verdict}
                        verdictColor={verdictColor}
                    />

                    <ScoreSection
                        finalScore={detail?.final_score}
                        mlScore={detail?.ml_score}
                        agentScore={detail?.agent_score}
                    />

                    <ReasonsSection reasons={detail?.reasons} />

                    <RecommendationsSection
                        recommendations={detail?.recommendations}
                    />

                    <EvidenceSection evidence={detail?.evidence} />

                    <MetadataSection
                        id={detail?._id}
                        timestamp={detail?.timestamp}
                    />
                </Card>
            </div>
        </div>
    );
}
