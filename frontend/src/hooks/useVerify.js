/**
 * Verification Hook.
 *
 * Provides convenient access to verification context.
 */

import { useContext } from "react";
import { VerificationContext } from "../contexts/VerificationContext";

export function useVerify() {
    const context = useContext(VerificationContext);

    if (!context) {
        throw new Error("useVerify must be used within a VerificationProvider");
    }

    return context;
}
