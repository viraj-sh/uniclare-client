import { useEffect, useState } from "react";
import { api } from "../lib/api";

export function HealthBanner() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    api.healthCheck()
      .then((data) => {
        if (data?.status !== "healthy") {
          setShow(true);
          timer = setTimeout(() => setShow(false), 5000);
        }
      })
      .catch(() => {
        setShow(true);
        timer = setTimeout(() => setShow(false), 5000);
      });
    return () => clearTimeout(timer);
  }, []);

  if (!show) return null;

  return (
    <div
      className="bg-destructive/10 border-b border-destructive/20 text-destructive px-4 py-2 text-sm flex items-center justify-between cursor-pointer"
      onClick={() => setShow(false)}
    >
      <span>Service unavailable. Some features may not work.</span>
      <span className="text-xs opacity-70 ml-4">Tap to dismiss</span>
    </div>
  );
}
