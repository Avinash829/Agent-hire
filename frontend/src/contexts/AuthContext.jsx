/**
 * Authentication Context Provider.
 *
 * Manages authentication state across the application using Firebase.
 * Provides login, logout, and user state to all child components.
 */

import { createContext, useState, useEffect, useCallback } from "react";
import { signInWithPopup, signOut, onAuthStateChanged } from "firebase/auth";
import { auth, googleProvider } from "../firebase/firebase";
import { STORAGE_KEYS } from "../constants";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
            if (firebaseUser) {
                const userData = {
                    uid: firebaseUser.uid,
                    email: firebaseUser.email,
                    name: firebaseUser.displayName,
                    picture: firebaseUser.photoURL,
                };
                setUser(userData);
                localStorage.setItem(
                    STORAGE_KEYS.userData,
                    JSON.stringify(userData)
                );
            } else {
                setUser(null);
                localStorage.removeItem(STORAGE_KEYS.authToken);
                localStorage.removeItem(STORAGE_KEYS.userData);
            }
            setLoading(false);
        });

        return () => unsubscribe();
    }, []);

    const loginWithGoogle = useCallback(async () => {
        try {
            setError(null);
            const result = await signInWithPopup(auth, googleProvider);
            const token = await result.user.getIdToken();
            localStorage.setItem(STORAGE_KEYS.authToken, token);

            const userData = {
                uid: result.user.uid,
                email: result.user.email,
                name: result.user.displayName,
                picture: result.user.photoURL,
            };
            setUser(userData);
            localStorage.setItem(
                STORAGE_KEYS.userData,
                JSON.stringify(userData)
            );

            return userData;
        } catch (loginError) {
            const errorMessage =
                loginError.code === "auth/popup-closed-by-user"
                    ? "Login cancelled"
                    : "Failed to login with Google";
            setError(errorMessage);
            throw loginError;
        }
    }, []);

    const logout = useCallback(async () => {
        try {
            await signOut(auth);
            setUser(null);
            localStorage.removeItem(STORAGE_KEYS.authToken);
            localStorage.removeItem(STORAGE_KEYS.userData);
        } catch (logoutError) {
            setError("Failed to logout");
            throw logoutError;
        }
    }, []);

    const getToken = useCallback(async () => {
        if (auth.currentUser) {
            return await auth.currentUser.getIdToken();
        }
        return null;
    }, []);

    const value = {
        user,
        loading,
        error,
        isAuthenticated: !!user,
        loginWithGoogle,
        logout,
        getToken,
    };

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
}
