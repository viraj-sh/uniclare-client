import { useEffect, useState } from "react";
import { Bell } from "lucide-react";
import { Loader } from "../components/Loader";
import { ErrorMessage } from "../components/ErrorMessage";
import { EmptyState } from "../components/EmptyState";
import { api } from "../lib/api";

type Notification = Awaited<ReturnType<typeof api.getNotifications>>[number];

export function Notifications() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getNotifications();
      setNotifications(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load notifications");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader message="Loading notifications..." />;
  if (error) return <ErrorMessage message={error} retry={fetchNotifications} />;

  return (
    <div className="space-y-6">
      <div>
        <h1>Notifications</h1>
        <p className="text-sm text-muted-foreground">Updates and alerts from your institution</p>
      </div>

      {notifications.length === 0 ? (
        <EmptyState
          icon={Bell}
          title="No notifications"
          description="You have no notifications at this time"
        />
      ) : (
        <div className="space-y-3">
          {notifications.map((n, idx) => (
            <div key={idx} className="bg-card border border-border rounded-lg p-4 space-y-1">
              <div className="flex items-start justify-between gap-4">
                <div className="font-medium">{n.title}</div>
                {n.date && (
                  <div className="text-xs text-muted-foreground whitespace-nowrap shrink-0">
                    {n.date}
                  </div>
                )}
              </div>
              {n.body && <p className="text-sm text-muted-foreground">{n.body}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
