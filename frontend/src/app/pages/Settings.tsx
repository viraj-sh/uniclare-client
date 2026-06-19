import { useState } from "react";
import { Loader2 } from "lucide-react";
import { api } from "../lib/api";

export function Settings() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState("");

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError("");
    setPasswordSuccess("");

    if (newPassword !== confirmNewPassword) {
      setPasswordError("New passwords do not match");
      return;
    }
    if (!currentPassword || !newPassword) {
      setPasswordError("All fields are required");
      return;
    }

    setPasswordLoading(true);
    try {
      await api.changePassword(currentPassword, newPassword);
      setPasswordSuccess("Password changed successfully");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
    } catch (err: unknown) {
      setPasswordError(err instanceof Error ? err.message : "Failed to change password. Please try again.");
    } finally {
      setPasswordLoading(false);
    }
  };

  const inputClass =
    "w-full px-3 py-2 bg-input-background border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary dark:bg-input-background";

  return (
    <div className="space-y-6">
      <div>
        <h1>Settings</h1>
        <p className="text-sm text-muted-foreground">Manage your application preferences</p>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Change Password</h2>
        </div>
        <div className="p-6">
          <form onSubmit={handleChangePassword} className="space-y-4 max-w-sm">
            <div className="space-y-2">
              <label htmlFor="current-password" className="block text-sm">
                Current Password
              </label>
              <input
                id="current-password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className={inputClass}
                placeholder="Enter current password"
                disabled={passwordLoading}
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
                disabled={passwordLoading}
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="confirm-new-password" className="block text-sm">
                Confirm New Password
              </label>
              <input
                id="confirm-new-password"
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                className={inputClass}
                placeholder="Confirm new password"
                disabled={passwordLoading}
              />
            </div>

            {passwordError && (
              <div className="text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md p-3">
                {passwordError}
              </div>
            )}

            {passwordSuccess && (
              <div className="text-sm text-primary bg-primary/10 border border-primary/20 rounded-md p-3">
                {passwordSuccess}
              </div>
            )}

            <button
              type="submit"
              disabled={passwordLoading}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {passwordLoading && <Loader2 className="h-4 w-4 animate-spin" />}
              {passwordLoading ? "Updating..." : "Update Password"}
            </button>
          </form>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>About</h2>
        </div>
        <div className="p-6 space-y-2">
          <p className="text-sm text-muted-foreground">
            Uniclare Client is open source. Report bugs, request features, or contribute.
          </p>
          <a
            href="https://github.com/viraj-sh/uniclare-client"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary hover:text-primary/80 transition-colors"
          >
            https://github.com/viraj-sh/uniclare-client
          </a>
        </div>
      </div>
    </div>
  );
}
