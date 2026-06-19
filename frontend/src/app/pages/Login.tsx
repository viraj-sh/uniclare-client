import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import { Loader2, Github } from "lucide-react";
import { api } from "../lib/api";
import { HealthBanner } from "../components/HealthBanner";

type View = "login" | "forgot-step1" | "forgot-step2";

export function Login() {
  const [view, setView] = useState<View>("login");
  const navigate = useNavigate();

  // Ensure dark theme is active on login page
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  // Login state
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [loginSuccess, setLoginSuccess] = useState("");

  // Forgot password state
  const [forgotMobile, setForgotMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [forgotLoading, setForgotLoading] = useState(false);
  const [forgotError, setForgotError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");
    if (mobile.length !== 10) {
      setLoginError("Please enter a valid 10-digit mobile number");
      return;
    }
    setLoginLoading(true);
    try {
      const { session_id } = await api.login(mobile, password);
      localStorage.setItem("session_token", session_id);
      navigate("/results");
    } catch (err: unknown) {
      setLoginError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setForgotError("");
    if (forgotMobile.length !== 10) {
      setForgotError("Please enter a valid 10-digit mobile number");
      return;
    }
    setForgotLoading(true);
    try {
      await api.sendOtp(forgotMobile);
      setView("forgot-step2");
    } catch (err: unknown) {
      setForgotError(err instanceof Error ? err.message : "Failed to send OTP. Please try again.");
    } finally {
      setForgotLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setForgotError("");
    if (newPassword !== confirmPassword) {
      setForgotError("Passwords do not match");
      return;
    }
    setForgotLoading(true);
    try {
      await api.resetPassword(forgotMobile, otp, newPassword);
      setView("login");
      setLoginSuccess("Password reset successfully. Please sign in.");
    } catch (err: unknown) {
      setForgotError(err instanceof Error ? err.message : "Failed to reset password. Please try again.");
    } finally {
      setForgotLoading(false);
    }
  };

  const inputClass =
    "w-full px-3 py-2 bg-input-background border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary dark:bg-input-background";

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <HealthBanner />
      <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-medium">Uniclare Client</h1>
          <p className="text-sm text-muted-foreground">Sign in to access your academic records</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          {/* Login form */}
          {view === "login" && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="mobile" className="block text-sm">
                  Mobile Number
                </label>
                <input
                  id="mobile"
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]{10}"
                  maxLength={10}
                  value={mobile}
                  onChange={(e) => setMobile(e.target.value.replace(/\D/g, ""))}
                  className={inputClass}
                  placeholder="Enter 10-digit mobile number"
                  disabled={loginLoading}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="block text-sm">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={inputClass}
                  placeholder="Enter your password"
                  disabled={loginLoading}
                />
              </div>

              {loginError && (
                <div className="text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md p-3">
                  {loginError}
                </div>
              )}

              {loginSuccess && (
                <div className="text-sm text-primary bg-primary/10 border border-primary/20 rounded-md p-3">
                  {loginSuccess}
                </div>
              )}

              <button
                type="submit"
                disabled={loginLoading}
                className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loginLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                {loginLoading ? "Signing in..." : "Sign in"}
              </button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={() => { setView("forgot-step1"); setForgotError(""); }}
                  className="text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  Forgot Password?
                </button>
              </div>
            </form>
          )}

          {/* Forgot password step 1 */}
          {view === "forgot-step1" && (
            <form onSubmit={handleSendOtp} className="space-y-4">
              <div className="space-y-1">
                <h2 className="text-base font-medium">Reset Password</h2>
                <p className="text-sm text-muted-foreground">Enter your mobile number to receive an OTP</p>
              </div>

              <div className="space-y-2">
                <label htmlFor="forgot-mobile" className="block text-sm">
                  Mobile Number
                </label>
                <input
                  id="forgot-mobile"
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]{10}"
                  maxLength={10}
                  value={forgotMobile}
                  onChange={(e) => setForgotMobile(e.target.value.replace(/\D/g, ""))}
                  className={inputClass}
                  placeholder="Enter 10-digit mobile number"
                  disabled={forgotLoading}
                />
              </div>

              {forgotError && (
                <div className="text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md p-3">
                  {forgotError}
                </div>
              )}

              <button
                type="submit"
                disabled={forgotLoading}
                className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {forgotLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                {forgotLoading ? "Sending OTP..." : "Send OTP"}
              </button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setView("login")}
                  className="text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  Back to Login
                </button>
              </div>
            </form>
          )}

          {/* Forgot password step 2 */}
          {view === "forgot-step2" && (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <div className="space-y-1">
                <h2 className="text-base font-medium">Enter OTP &amp; New Password</h2>
                <p className="text-sm text-muted-foreground">OTP sent to {forgotMobile}</p>
              </div>

              <div className="space-y-2">
                <label htmlFor="otp" className="block text-sm">
                  OTP
                </label>
                <input
                  id="otp"
                  type="text"
                  inputMode="numeric"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  className={inputClass}
                  placeholder="Enter OTP"
                  disabled={forgotLoading}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="new-password" className="block text-sm">
                  New Password
                </label>
                <input
                  id="new-password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className={inputClass}
                  placeholder="Enter new password"
                  disabled={forgotLoading}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="confirm-password" className="block text-sm">
                  Confirm Password
                </label>
                <input
                  id="confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={inputClass}
                  placeholder="Confirm new password"
                  disabled={forgotLoading}
                />
              </div>

              {forgotError && (
                <div className="text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md p-3">
                  {forgotError}
                </div>
              )}

              <button
                type="submit"
                disabled={forgotLoading}
                className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {forgotLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                {forgotLoading ? "Resetting..." : "Reset Password"}
              </button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setView("login")}
                  className="text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  Back to Login
                </button>
              </div>
            </form>
          )}
        </div>

        <div className="text-center">
          <a
            href="https://github.com/viraj-sh/uniclare-client"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <Github className="h-3.5 w-3.5" />
            github.com/viraj-sh/uniclare-client
          </a>
        </div>
      </div>
      </div>
    </div>
  );
}
