/**
 * Verify Page Component.
 *
 * Provides the main job posting verification interface.
 * Handles form submission, loading state, and result display.
 */

import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useVerify } from "../hooks/useVerify";
import VerificationForm from "../components/verification/VerificationForm";
import LoadingProgress from "../components/verification/LoadingProgress";
import ResultCard from "../components/verification/ResultCard";

export default function VerifyPage() {
    const { isAuthenticated, loading: authLoading } = useAuth();
    const { verifying, result, error, submitVerification, clearResult } =
        useVerify();
    const navigate = useNavigate();

    if (authLoading) {
        return (
            <div className="min-h-[80vh] flex items-center justify-center">
                <div className="animate-spin h-10 w-10 border-4 border-primary-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    if (!isAuthenticated) {
        navigate("/login");
        return null;
    }

    const handleSubmit = async (formData) => {
        try {
            clearResult();
            await submitVerification(formData);
        } catch {
            // Error is handled by the context
        }
    };

    const handleTryAgain = () => {
        clearResult();
    };

    return (
        <div className="page-container">
            <div className="max-w-3xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-2xl font-bold text-gray-900">
                        Verify Job Posting
                    </h1>
                    <p className="text-gray-600 mt-1">
                        Submit a job posting to analyze it through our dual
                        verification pipelines.
                    </p>
                </div>

                {error && (
                    <div className="mb-6 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg">
                        <p className="text-sm">{error}</p>
                    </div>
                )}

                {result ? (
                    <div className="space-y-6">
                        <ResultCard result={result} />
                        <div className="flex justify-center">
                            <button
                                onClick={handleTryAgain}
                                className="btn-secondary"
                            >
                                Verify Another Job
                            </button>
                        </div>
                    </div>
                ) : verifying ? (
                    <LoadingProgress />
                ) : (
                    <VerificationForm
                        onSubmit={handleSubmit}
                        loading={verifying}
                    />
                )}
            </div>
        </div>
    );
}
