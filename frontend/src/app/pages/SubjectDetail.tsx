import { useEffect, useState } from "react";
import { useParams, Link } from "react-router";
import { ArrowLeft } from "lucide-react";
import { Loader } from "../components/Loader";
import { ErrorMessage } from "../components/ErrorMessage";

interface Component {
  name: string;
  maxMarks: number;
  obtained: number;
  percentage: number;
}

interface SubjectDetail {
  id: string;
  code: string;
  name: string;
  credits: number;
  grade: string;
  gradePoints: number;
  semester: string;
  components: Component[];
}

export function SubjectDetail() {
  const { subjectId } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [subject, setSubject] = useState<SubjectDetail | null>(null);

  useEffect(() => {
    fetchSubjectDetail();
  }, [subjectId]);

  const fetchSubjectDetail = () => {
    setLoading(true);
    setError("");

    setTimeout(() => {
      setSubject({
        id: subjectId || "1",
        code: "CS601",
        name: "Machine Learning",
        credits: 4,
        grade: "A+",
        gradePoints: 10,
        semester: "Semester 6",
        components: [
          { name: "End Semester Exam (ESE)", maxMarks: 100, obtained: 85, percentage: 85 },
          { name: "Internal Assessment 1", maxMarks: 20, obtained: 18, percentage: 90 },
          { name: "Internal Assessment 2", maxMarks: 20, obtained: 20, percentage: 100 },
          { name: "Practical", maxMarks: 25, obtained: 23, percentage: 92 },
          { name: "Assignments", maxMarks: 15, obtained: 13, percentage: 86.67 },
        ],
      });
      setLoading(false);
    }, 500);
  };

  if (loading) return <Loader message="Loading subject details..." />;
  if (error) return <ErrorMessage message={error} retry={fetchSubjectDetail} />;
  if (!subject) return null;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/results" className="inline-flex items-center gap-1 text-sm text-primary hover:text-primary/80 transition-colors mb-4">
          <ArrowLeft className="h-4 w-4" />
          Back to results
        </Link>
        <h1>{subject.name}</h1>
        <p className="text-sm text-muted-foreground">{subject.code} • {subject.semester}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card border border-border rounded-lg p-4">
          <div className="text-sm text-muted-foreground mb-1">Grade</div>
          <div className="text-2xl font-medium">{subject.grade}</div>
        </div>
        <div className="bg-card border border-border rounded-lg p-4">
          <div className="text-sm text-muted-foreground mb-1">Grade Points</div>
          <div className="text-2xl font-medium">{subject.gradePoints}</div>
        </div>
        <div className="bg-card border border-border rounded-lg p-4">
          <div className="text-sm text-muted-foreground mb-1">Credits</div>
          <div className="text-2xl font-medium">{subject.credits}</div>
        </div>
        <div className="bg-card border border-border rounded-lg p-4">
          <div className="text-sm text-muted-foreground mb-1">Components</div>
          <div className="text-2xl font-medium">{subject.components.length}</div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Evaluation Breakdown</h2>
        </div>
        <div className="divide-y divide-border">
          {subject.components.map((component, index) => (
            <div key={index} className="p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium">{component.name}</div>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-muted-foreground">
                    {component.obtained} / {component.maxMarks}
                  </span>
                  <span className="font-medium">{component.percentage.toFixed(1)}%</span>
                </div>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-primary rounded-full h-2 transition-all"
                  style={{ width: `${component.percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
