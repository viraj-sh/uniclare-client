import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { useEffect, useState } from "react";

// Inject PWA manifest and mobile viewport meta
(function injectPwaMeta() {
  if (!document.querySelector('link[rel="manifest"]')) {
    const link = document.createElement("link");
    link.rel = "manifest";
    link.href = "/manifest.json";
    document.head.appendChild(link);
  }
  if (!document.querySelector('meta[name="theme-color"]')) {
    const meta = document.createElement("meta");
    meta.name = "theme-color";
    meta.content = "#0f172a";
    document.head.appendChild(meta);
  }
  if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
    const meta = document.createElement("meta");
    meta.name = "apple-mobile-web-app-capable";
    meta.content = "yes";
    document.head.appendChild(meta);
  }
})();

import { Layout } from "./components/Layout";
import { Login } from "./pages/Login";
import { ResultsList } from "./pages/ResultsList";
import { ResultDetail } from "./pages/ResultDetail";
import { SubjectDetail } from "./pages/SubjectDetail";
import { Profile } from "./pages/Profile";
import { Settings } from "./pages/Settings";
import { Notifications } from "./pages/Notifications";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("session_token");
    setIsAuthenticated(!!token);
  }, []);

  if (isAuthenticated === null) {
    return null;
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/results" replace />} />

        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route path="/results" element={<ResultsList />} />
          <Route path="/results/:resultId" element={<ResultDetail />} />
          <Route path="/subjects/:subjectId" element={<SubjectDetail />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
