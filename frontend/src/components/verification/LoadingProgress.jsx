/**
 * Loading Progress Component.
 *
 * Displays animated progress indicators during verification analysis.
 * Shows the steps being executed in real-time.
 */

import { useState, useEffect } from "react";
import Card from "../common/Card";

const ANALYSIS_STEPS = [
    { id: "nlp", label: "Running NLP Analysis...", pipeline: "ML Pipeline" },
    {
        id: "extraction",
        label: "Extracting Company Information...",
        pipeline: "Agent Pipeline",
    },
    {
        id: "whois",
        label: "Checking Domain Registration...",
        pipeline: "Agent Pipeline",
    },
    {
        id: "website",
        label: "Investigating Company Website...",
        pipeline: "Agent Pipeline",
    },
    {
        id: "online_reputation",
        label: "Searching Online Reputation Sources...",
        pipeline: "Agent Pipeline",
    },
    {
        id: "reasoning",
        label: "AI Reasoning in Progress...",
        pipeline: "Agent Pipeline",
    },
    {
        id: "synthesis",
        label: "Synthesizing Results...",
        pipeline: "Synthesis",
    },
];

export default function LoadingProgress() {
    const [activeStep, setActiveStep] = useState(0);
    const [completedSteps, setCompletedSteps] = useState(new Set());

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveStep((prev) => {
                if (prev < ANALYSIS_STEPS.length - 1) {
                    setCompletedSteps(
                        (completed) => new Set([...completed, prev])
                    );
                    return prev + 1;
                }
                clearInterval(interval);
                return prev;
            });
        }, 4000);

        return () => clearInterval(interval);
    }, []);

    return (
        <Card className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Analyzing Job Posting
                </h3>
                <p className="text-sm text-gray-500">
                    Running parallel ML and Agent-based analysis pipelines
                </p>
            </div>

            <div className="space-y-4">
                {ANALYSIS_STEPS.map((step, index) => {
                    const isActive = index === activeStep;
                    const isCompleted = completedSteps.has(index);

                    return (
                        <div
                            key={step.id}
                            className="flex items-center space-x-3"
                        >
                            <div className="flex-shrink-0">
                                {isCompleted ? (
                                    <div className="w-6 h-6 rounded-full bg-success-500 flex items-center justify-center">
                                        <svg
                                            className="w-4 h-4 text-white"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M5 13l4 4L19 7"
                                            />
                                        </svg>
                                    </div>
                                ) : isActive ? (
                                    <div className="w-6 h-6 rounded-full border-2 border-primary-500 border-t-transparent animate-spin" />
                                ) : (
                                    <div className="w-6 h-6 rounded-full border-2 border-gray-300" />
                                )}
                            </div>

                            <div className="flex-1 min-w-0">
                                <p
                                    className={`text-sm font-medium ${
                                        isCompleted
                                            ? "text-gray-900"
                                            : isActive
                                            ? "text-primary-600"
                                            : "text-gray-400"
                                    }`}
                                >
                                    {step.label}
                                </p>
                                <p className="text-xs text-gray-400">
                                    {step.pipeline}
                                </p>
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="mt-6 text-center">
                <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                        className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                        style={{
                            width: `${
                                ((completedSteps.size +
                                    (activeStep >= 0 ? 1 : 0)) /
                                    ANALYSIS_STEPS.length) *
                                100
                            }%`,
                        }}
                    />
                </div>
                <p className="text-xs text-gray-400 mt-2">
                    Analyzing job posting through multiple verification layers
                </p>
            </div>
        </Card>
    );
}
