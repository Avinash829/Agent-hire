/**
 * Root Application Component.
 *
 * Sets up providers and routing for the entire application.
 */

import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { VerificationProvider } from "./contexts/VerificationContext";
import AppRoutes from "./routes/AppRoutes";

export default function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <VerificationProvider>
                    <AppRoutes />
                </VerificationProvider>
            </AuthProvider>
        </BrowserRouter>
    );
}
