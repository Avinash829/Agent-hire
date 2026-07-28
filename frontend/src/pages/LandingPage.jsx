/**
 * Landing Page Component.
 *
 * The public landing page showcasing the application's features
 * and providing a call-to-action for authentication.
 */

import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Button from "../components/common/Button";
import { APP_NAME } from "../constants";

export default function LandingPage() {
    const { isAuthenticated } = useAuth();

    const features = [
        {
            title: "ML-Powered Analysis",
            description:
                "Advanced machine learning algorithm analyzes job posting text for suspicious patterns, keywords, and fraud indicators.",
            icon: (
                <svg
                    className="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                    />
                </svg>
            ),
        },
        {
            title: "AI Investigation",
            description:
                "Autonomous AI agent investigates company domains, career pages, and social media for verification evidence.",
            icon: (
                <svg
                    className="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                </svg>
            ),
        },
        {
            title: "Hybrid Scoring",
            description:
                "Combines traditional ML and AI investigation results into a unified, explainable fraud risk score.",
            icon: (
                <svg
                    className="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                </svg>
            ),
        },
        {
            title: "Detailed Reports",
            description:
                "Get comprehensive reports with evidence, risk factors, and actionable recommendations for each job posting.",
            icon: (
                <svg
                    className="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                </svg>
            ),
        },
    ];

    return (
        <div className="min-h-[calc(100vh-4rem)]">
            {/* Hero Section */}
            <section className="py-20 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto text-center">
                    <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary-50 text-primary-700 text-sm font-medium mb-6">
                        Powered by ML + Agentic AI
                    </div>
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                        Detect Fake Job Postings with{" "}
                        <span className="text-primary-600">
                            Hybrid Intelligence
                        </span>
                    </h1>
                    <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
                        {APP_NAME} uses a dual-pipeline approach combining
                        traditional machine learning with autonomous AI agents
                        to identify fraudulent job postings with high accuracy.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        {isAuthenticated ? (
                            <Link to="/verify">
                                <Button size="lg">Start Verification</Button>
                            </Link>
                        ) : (
                            <Link to="/login">
                                <Button size="lg">Get Started Free</Button>
                            </Link>
                        )}
                        <Link to="/login">
                            <Button variant="secondary" size="lg">
                                Learn More
                            </Button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">
                            How It Works
                        </h2>
                        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                            Two independent verification pipelines working
                            together to protect you from job scams.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {features.map((feature) => (
                            <div
                                key={feature.title}
                                className="text-center p-6 rounded-xl hover:bg-gray-50 transition-colors"
                            >
                                <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                                    {feature.icon}
                                </div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                    {feature.title}
                                </h3>
                                <p className="text-sm text-gray-600">
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="py-16 bg-primary-600 text-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
                        <div>
                            <p className="text-4xl font-bold mb-2">2</p>
                            <p className="text-primary-100">
                                Independent Pipelines
                            </p>
                        </div>
                        <div>
                            <p className="text-4xl font-bold mb-2">Real-time</p>
                            <p className="text-primary-100">
                                Analysis & Results
                            </p>
                        </div>
                        <div>
                            <p className="text-4xl font-bold mb-2">100%</p>
                            <p className="text-primary-100">
                                Explainable Reports
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
