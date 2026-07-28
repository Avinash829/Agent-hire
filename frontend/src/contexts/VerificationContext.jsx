/**
 * Verification Context Provider.
 *
 * Manages the state of job posting verification operations,
 * including loading states, results, and error handling.
 */

import { createContext, useState, useCallback } from "react";
import {
    verifyJobPosting,
    getVerificationHistory,
    getVerificationDetail,
} from "../api/endpoints";

export const VerificationContext = createContext(null);

export function VerificationProvider({ children }) {
    const [verifying, setVerifying] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState({
        items: [],
        total: 0,
        loading: false,
    });

    const submitVerification = useCallback(
        async ({ jobDescription, sourceLink, applicationLink }) => {
            try {
                setVerifying(true);
                setError(null);
                setResult(null);

                const response = await verifyJobPosting({
                    jobDescription,
                    sourceLink,
                    applicationLink,
                });

                setResult(response);
                return response;
            } catch (verificationError) {
                const errorMessage =
                    verificationError.customMessage || "Verification failed";
                setError(errorMessage);
                throw verificationError;
            } finally {
                setVerifying(false);
            }
        },
        []
    );

    const fetchHistory = useCallback(async (page = 1, limit = 20) => {
        try {
            setHistory((prev) => ({ ...prev, loading: true }));
            const response = await getVerificationHistory(page, limit);
            setHistory({
                items: response.items || [],
                total: response.total || 0,
                loading: false,
            });
            return response;
        } catch (historyError) {
            setHistory((prev) => ({ ...prev, loading: false }));
            throw historyError;
        }
    }, []);

    const fetchDetail = useCallback(async (verificationId) => {
        try {
            const response = await getVerificationDetail(verificationId);
            return response.data;
        } catch (detailError) {
            throw detailError;
        }
    }, []);

    const clearResult = useCallback(() => {
        setResult(null);
        setError(null);
    }, []);

    const value = {
        verifying,
        result,
        error,
        history,
        submitVerification,
        fetchHistory,
        fetchDetail,
        clearResult,
    };

    return (
        <VerificationContext.Provider value={value}>
            {children}
        </VerificationContext.Provider>
    );
}
