/**
 * Login Page Component.
 *
 * Provides Google OAuth authentication interface.
 */

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import GoogleLoginButton from "../components/auth/GoogleLoginButton";
import Card from "../components/common/Card";
import { APP_NAME } from "../constants";

export default function LoginPage() {
    const { isAuthenticated, loading } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (isAuthenticated && !loading) {
            navigate("/dashboard");
        }
    }, [isAuthenticated, loading, navigate]);

    if (loading) {
        return (
            <div className="min-h-[80vh] flex items-center justify-center">
                <div className="animate-spin h-10 w-10 border-4 border-primary-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div className="min-h-[80vh] flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                        <svg
                            className="w-10 h-10 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                            />
                        </svg>
                    </div>
                    <h1 className="text-2xl font-bold text-gray-900 mb-2">
                        Welcome to {APP_NAME}
                    </h1>
                    <p className="text-gray-600">
                        Sign in to start verifying job postings
                    </p>
                </div>

                <Card>
                    <div className="space-y-6">
                        <div className="text-center">
                            <h2 className="text-lg font-semibold text-gray-900 mb-2">
                                Sign In
                            </h2>
                            <p className="text-sm text-gray-500">
                                Use your Google account to get started
                            </p>
                        </div>

                        <GoogleLoginButton />

                        <div className="text-center">
                            <p className="text-xs text-gray-400">
                                By signing in, you agree to our Terms of Service
                                and Privacy Policy. Your data is encrypted and
                                stored securely.
                            </p>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    );
}
