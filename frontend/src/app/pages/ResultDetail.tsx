import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { api } from "../lib/api";

type ResultData = Awaited<ReturnType<typeof api.getResult>>;

function resultBadgeClass(result: string): string {
  if (result === "Pass") return "bg-green-500/10 text-green-600 dark:text-green-400";
  if (result.includes("Fail Promoted") || result.includes("Fail, Promoted")) {
    return "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400";
  }
  if (result.includes("Fail")) return "bg-destructive/10 text-destructive";
  return "bg-primary/10 text-primary";
}

function val(v: string | number | null | undefined): string {
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}

export function ResultDetail() {
  const { resultId } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ResultData | null>(null);
   const [searchParams] = useSearchParams();

  useEffect(() => {
    fetchResultDetail();
  }, [resultId, searchParams]);

  const fetchResultDetail = async () => {
    setLoading(true);
    setError("");
    try {
      const year = decodeURIComponent(resultId || "");
      const regNo = searchParams.get("reg_no") || "";
      const data = await api.getResult(year, regNo);
      setResult(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load result details");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader message="Loading result details..." />;
  if (error) return <ErrorMessage message={error} retry={fetchResultDetail} />;
  if (!result) return null;

  const { student_details, result: summary, subjects } = result;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/results" className="inline-flex items-center gap-1 text-sm text-primary hover:text-primary/80 transition-colors mb-4">
          <ArrowLeft className="h-4 w-4" />
          Back to results
        </Link>
        <h1>{student_details.full_sem || student_details.sem}</h1>
        <p className="text-sm text-muted-foreground">{student_details.exam_date}</p>
      </div>

      {/* Section A — Student/Exam Info */}
      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Exam Info</h2>
        </div>
        <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="space-y-1">
            <div className="text-sm text-muted-foreground">Semester</div>
            <div className="font-medium">{val(student_details.sem)}</div>
          </div>
          <div className="space-y-1">
            <div className="text-sm text-muted-foreground">Full Semester</div>
            <div className="font-medium">{val(student_details.full_sem)}</div>
          </div>
          <div className="space-y-1">
            <div className="text-sm text-muted-foreground">Exam Date</div>
            <div className="font-medium">{val(student_details.exam_date)}</div>
          </div>
          <div className="space-y-1">
            <div className="text-sm text-muted-foreground">Exam No</div>
            <div className="font-medium">{val(student_details.exam_no)}</div>
          </div>
        </div>
      </div>

      {/* Section B — Result Summary */}
      {summary && (
        <div className="bg-card border border-border rounded-lg">
          <div className="p-6 border-b border-border">
            <h2>Result Summary</h2>
          </div>
          <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="space-y-1">
              <div className="text-sm text-muted-foreground">Result</div>
              <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${resultBadgeClass(val(summary.result))}`}>
                {val(summary.result)}
              </span>
            </div>
            <div className="space-y-1">
              <div className="text-sm text-muted-foreground">CGPA</div>
              <div className="text-xl font-medium">{val(summary.cgpa)}</div>
            </div>
            <div className="space-y-1">
              <div className="text-sm text-muted-foreground">SGPA</div>
              <div className="text-xl font-medium">{val(summary.sgpa)}</div>
            </div>
            <div className="space-y-1">
              <div className="text-sm text-muted-foreground">Percentage</div>
              <div className="text-xl font-medium">{val(summary.percentage)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Section C — Subjects Table */}
      {subjects.length > 0 && (
        <div className="bg-card border border-border rounded-lg">
          <div className="p-6 border-b border-border">
            <h2>Subject Details</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted/50 border-b border-border">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-medium">Subject</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Type</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">ESE</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">IA</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Viva</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Total</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Credits</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Grade</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Grade Points</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Credit Points</th>
                  <th className="px-4 py-3 text-left text-sm font-medium">Remarks</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {subjects.map((subject) => (
                  <tr key={subject.id} className="hover:bg-muted/30 transition-colors">
                    <td className="px-4 py-3 font-medium text-sm">{val(subject.sub)}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{val(subject.exam_type)}</td>
                    <td className="px-4 py-3 text-sm">{val(subject.ese_marks)}</td>
                    <td className="px-4 py-3 text-sm">{val(subject.ia_marks)}</td>
                    <td className="px-4 py-3 text-sm">{val(subject.viva_marks)}</td>
                    <td className="px-4 py-3 font-medium">{val(subject.total_marks)}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{val(subject.credits)}</td>
                    <td className="px-4 py-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-md bg-primary/10 text-primary text-sm font-medium">
                        {val(subject.grade)}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{val(subject.grade_points)}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{val(subject.credit_points)}</td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">{val(subject.remarks)}</td>
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
