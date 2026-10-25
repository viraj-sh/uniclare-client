import { AlertCircle } from "lucide-react";

interface ErrorMessageProps {
  title?: string;
  message: string;
  retry?: () => void;
}

export function ErrorMessage({ title = "Error", message, retry }: ErrorMessageProps) {
  return (
    <div className="rounded-lg border border-destructive/20 bg-destructive/10 p-4">
      <div className="flex gap-3">
        <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
        <div className="flex-1 space-y-1">
          <h4 className="font-medium text-destructive">{title}</h4>
          <p className="text-sm text-destructive/80">{message}</p>
          {retry && (
            <button
              onClick={retry}
              className="mt-2 text-sm text-destructive hover:text-destructive/80 underline"
            >
              Try again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
