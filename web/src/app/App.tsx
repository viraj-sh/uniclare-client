import { useEffect, useState } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router";

import { Layout } from "./components/Layout";
import { api } from "./lib/backend";
import { Login } from "./pages/Login";
import { Notifications } from "./pages/Notifications";
import { Profile } from "./pages/Profile";
import { ResultDetail } from "./pages/ResultDetail";
import { ResultsList } from "./pages/ResultsList";
import { Settings } from "./pages/Settings";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<"checking" | "yes" | "no">("checking");

  useEffect(() => {
    let cancelled = false;
    const token = localStorage.getItem("session_token");
    if (!token) {
      setState("no");
      return;
    }
    api.status()
      .then((loggedIn) => {
        if (cancelled) return;
        if (!loggedIn) localStorage.removeItem("session_token");
        setState(loggedIn ? "yes" : "no");
      })
      .catch(() => {
        if (!cancelled) setState("no");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (state === "checking") return null;
  return state === "yes" ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/results" replace />} />

        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/results" element={<ResultsList />} />
          <Route path="/results/:resultId" element={<ResultDetail />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/settings" element={<Settings />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}