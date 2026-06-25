import { ChevronRight, FileText, Search } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { EmptyState } from "../components/EmptyState";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { api } from "../lib/api";

type ResultItem = Awaited<ReturnType<typeof api.getResults>>[number];

function statusBadgeClass(status: string): string {
  if (status === "Pass") {
    return "bg-green-500/10 text-green-600 dark:text-green-400";
  }
  if (status.includes("Fail, Promoted") || status.includes("Fail,Promoted")) {
    return "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400";
  }
  if (status.includes("Fail")) {
    return "bg-destructive/10 text-destructive";
  }
  return "bg-primary/10 text-primary";
}

export function ResultsList() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [results, setResults] = useState<ResultItem[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getResults();
      setResults(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load results");
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = results.filter((r) => {
    const q = searchQuery.toLowerCase();
    return (
      r.exam_name.toLowerCase().includes(q) ||
      r.exam_date.toLowerCase().includes(q) ||
      r.status.toLowerCase().includes(q)
    );
  });

  if (loading) return <Loader message="Loading results..." />;
  if (error) return <ErrorMessage message={error} retry={fetchResults} />;

  return (
    <div className="space-y-6">
      <div>
        <h1>Results</h1>
        <p className="text-sm text-muted-foreground">View all your academic results</p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search results..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-input-background border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary dark:bg-input-background"
        />
      </div>

      {filteredResults.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No results found"
          description={searchQuery ? "Try adjusting your search query" : "No academic results available yet"}
        />
      ) : (
        <div className="bg-card border border-border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted/50 border-b border-border">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-medium">Exam</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Exam Date</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Result Date</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Status</th>
                  <th className="px-4 py-3"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {filteredResults.map((result) => (
                  <tr key={result.year} className="hover:bg-muted/30 transition-colors">
                    <td className="px-4 py-3 font-medium">{result.exam_name}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{result.exam_date}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{result.result_date || "—"}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${statusBadgeClass(result.status)}`}>
                        {result.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <Link
                        to={`/results/${encodeURIComponent(result.year)}?reg_no=${encodeURIComponent(result.reg_no)}`}
                        className="inline-flex items-center gap-1 text-sm text-primary hover:text-primary/80 transition-colors"
                      >
                        View
                        <ChevronRight className="h-4 w-4" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
