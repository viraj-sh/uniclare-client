import { useEffect, useState } from "react";
import { Link } from "react-router";
import { TrendingUp, Award, Calendar, ChevronRight } from "lucide-react";
import { Loader } from "../components/Loader";
import { ErrorMessage } from "../components/ErrorMessage";

interface DashboardData {
  overview: {
    totalResults: number;
    averageScore: number;
    latestSemester: string;
  };
  recentResults: Array<{
    id: string;
    semester: string;
    examType: string;
    score: number;
    date: string;
  }>;
}

export function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = () => {
    setLoading(true);
    setError("");

    // Simulate API call
    setTimeout(() => {
      setData({
        overview: {
          totalResults: 8,
          averageScore: 8.42,
          latestSemester: "Semester 6",
        },
        recentResults: [
          { id: "1", semester: "Semester 6", examType: "Regular", score: 8.75, date: "2026-03-15" },
          { id: "2", semester: "Semester 5", examType: "Regular", score: 8.50, date: "2025-11-20" },
          { id: "3", semester: "Semester 4", examType: "Regular", score: 8.20, date: "2025-05-10" },
        ],
      });
      setLoading(false);
    }, 800);
  };

  if (loading) return <Loader message="Loading dashboard..." />;
  if (error) return <ErrorMessage message={error} retry={fetchDashboard} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1>Dashboard</h1>
        <p className="text-sm text-muted-foreground">Overview of your academic performance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-6 space-y-2">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Calendar className="h-4 w-4" />
            <span className="text-sm">Latest Semester</span>
          </div>
          <div className="text-2xl font-medium">{data.overview.latestSemester}</div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 space-y-2">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Award className="h-4 w-4" />
            <span className="text-sm">Total Results</span>
          </div>
          <div className="text-2xl font-medium">{data.overview.totalResults}</div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 space-y-2">
          <div className="flex items-center gap-2 text-muted-foreground">
            <TrendingUp className="h-4 w-4" />
            <span className="text-sm">Average CGPA</span>
          </div>
          <div className="text-2xl font-medium">{data.overview.averageScore.toFixed(2)}</div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Recent Results</h2>
        </div>
        <div className="divide-y divide-border">
          {data.recentResults.map((result) => (
            <Link
              key={result.id}
              to={`/results/${result.id}`}
              className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors group"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-3">
                  <span className="font-medium">{result.semester}</span>
                  <span className="text-sm text-muted-foreground">{result.examType}</span>
                </div>
                <div className="text-sm text-muted-foreground">
                  {new Date(result.date).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric"
                  })}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="font-medium">SGPA: {result.score.toFixed(2)}</div>
                </div>
                <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-foreground transition-colors" />
              </div>
            </Link>
          ))}
        </div>
        <div className="p-4 border-t border-border">
          <Link
            to="/results"
            className="text-sm text-primary hover:text-primary/80 transition-colors"
          >
            View all results →
          </Link>
        </div>
      </div>
    </div>
  );
}
