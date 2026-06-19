import { useState } from "react";
import { History as HistoryIcon, TrendingUp, TrendingDown } from "lucide-react";
import { EmptyState } from "../components/EmptyState";

interface Snapshot {
  id: string;
  semester: string;
  sgpa: number;
  cgpa: number;
  date: string;
}

export function History() {
  const [snapshots] = useState<Snapshot[]>([
    { id: "1", semester: "Semester 6", sgpa: 8.75, cgpa: 8.42, date: "2026-03-15" },
    { id: "2", semester: "Semester 5", sgpa: 8.50, cgpa: 8.35, date: "2025-11-20" },
    { id: "3", semester: "Semester 4", sgpa: 8.20, cgpa: 8.28, date: "2025-05-10" },
    { id: "4", semester: "Semester 3", sgpa: 8.35, cgpa: 8.31, date: "2024-12-05" },
    { id: "5", semester: "Semester 2", sgpa: 8.60, cgpa: 8.35, date: "2024-05-15" },
    { id: "6", semester: "Semester 1", sgpa: 8.10, cgpa: 8.10, date: "2023-12-10" },
  ]);

  if (snapshots.length === 0) {
    return (
      <div className="space-y-6">
        <div>
          <h1>History</h1>
          <p className="text-sm text-muted-foreground">View historical academic data</p>
        </div>
        <EmptyState
          icon={HistoryIcon}
          title="No history available"
          description="Historical snapshots will appear here once data is stored locally"
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1>History</h1>
        <p className="text-sm text-muted-foreground">Track your academic progress over time</p>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>CGPA Trend</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {snapshots.map((snapshot, index) => {
              const prevCgpa = snapshots[index + 1]?.cgpa;
              const trend = prevCgpa ? snapshot.cgpa - prevCgpa : 0;

              return (
                <div key={snapshot.id} className="flex items-center justify-between py-3 border-b border-border last:border-0">
                  <div className="space-y-1">
                    <div className="font-medium">{snapshot.semester}</div>
                    <div className="text-sm text-muted-foreground">
                      {new Date(snapshot.date).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </div>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground">SGPA</div>
                      <div className="font-medium">{snapshot.sgpa.toFixed(2)}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground">CGPA</div>
                      <div className="font-medium">{snapshot.cgpa.toFixed(2)}</div>
                    </div>
                    {prevCgpa && (
                      <div className="flex items-center gap-1">
                        {trend > 0 ? (
                          <>
                            <TrendingUp className="h-4 w-4 text-primary" />
                            <span className="text-sm text-primary">+{trend.toFixed(2)}</span>
                          </>
                        ) : trend < 0 ? (
                          <>
                            <TrendingDown className="h-4 w-4 text-destructive" />
                            <span className="text-sm text-destructive">{trend.toFixed(2)}</span>
                          </>
                        ) : (
                          <span className="text-sm text-muted-foreground">—</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-2">Highest SGPA</div>
          <div className="text-2xl font-medium">
            {Math.max(...snapshots.map(s => s.sgpa)).toFixed(2)}
          </div>
          <div className="text-sm text-muted-foreground mt-1">
            {snapshots.find(s => s.sgpa === Math.max(...snapshots.map(x => x.sgpa)))?.semester}
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="text-sm text-muted-foreground mb-2">Current CGPA</div>
          <div className="text-2xl font-medium">{snapshots[0].cgpa.toFixed(2)}</div>
          <div className="text-sm text-muted-foreground mt-1">As of {snapshots[0].semester}</div>
        </div>
      </div>
    </div>
  );
}
