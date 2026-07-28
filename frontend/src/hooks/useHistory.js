/**
 * History Hook.
 *
 * Provides convenient access to verification history
 * from the VerificationContext.
 */

import { useCallback } from "react";
import { useVerify } from "./useVerify";

export function useHistory() {
    const { history, fetchHistory, fetchDetail, error } = useVerify();

    const loadHistory = useCallback(
        (page = 1, limit = 20) => {
            return fetchHistory(page, limit);
        },
        [fetchHistory]
    );

    const loadDetail = useCallback(
        (verificationId) => {
            return fetchDetail(verificationId);
        },
        [fetchDetail]
    );

    return {
        items: history.items,
        total: history.total,
        loading: history.loading,
        error,
        loadHistory,
        loadDetail,
    };
}
