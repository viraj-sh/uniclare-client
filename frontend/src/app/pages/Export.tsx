import { useState } from "react";
import { Download, FileJson, FileSpreadsheet } from "lucide-react";

export function Export() {
  const [format, setFormat] = useState<"json" | "csv">("json");
  const [scope, setScope] = useState<"all" | "semester" | "subject">("all");
  const [selectedSemester, setSelectedSemester] = useState("");

  const handleExport = () => {
    // Mock export logic
    const filename = `academic-data-${Date.now()}.${format}`;
    alert(`Exporting as ${format.toUpperCase()}: ${filename}`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1>Export Data</h1>
        <p className="text-sm text-muted-foreground">Download your academic data in various formats</p>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Export Format</h2>
        </div>
        <div className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => setFormat("json")}
              className={`flex items-center gap-3 p-4 border rounded-lg transition-colors ${
                format === "json"
                  ? "border-primary bg-primary/5"
                  : "border-border hover:border-primary/50"
              }`}
            >
              <FileJson className="h-6 w-6" />
              <div className="text-left">
                <div className="font-medium">JSON</div>
                <div className="text-sm text-muted-foreground">Structured data format</div>
              </div>
            </button>

            <button
              onClick={() => setFormat("csv")}
              className={`flex items-center gap-3 p-4 border rounded-lg transition-colors ${
                format === "csv"
                  ? "border-primary bg-primary/5"
                  : "border-border hover:border-primary/50"
              }`}
            >
              <FileSpreadsheet className="h-6 w-6" />
              <div className="text-left">
                <div className="font-medium">CSV</div>
                <div className="text-sm text-muted-foreground">Spreadsheet compatible</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-6 border-b border-border">
          <h2>Data Scope</h2>
        </div>
        <div className="p-6 space-y-4">
          <div className="space-y-3">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="radio"
                name="scope"
                value="all"
                checked={scope === "all"}
                onChange={(e) => setScope(e.target.value as any)}
                className="w-4 h-4 text-primary"
              />
              <div>
                <div className="font-medium">All Results</div>
                <div className="text-sm text-muted-foreground">Export complete academic record</div>
              </div>
            </label>

            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="radio"
                name="scope"
                value="semester"
                checked={scope === "semester"}
                onChange={(e) => setScope(e.target.value as any)}
                className="w-4 h-4 text-primary"
              />
              <div>
                <div className="font-medium">Specific Semester</div>
                <div className="text-sm text-muted-foreground">Export results from selected semester</div>
              </div>
            </label>

            {scope === "semester" && (
              <div className="ml-7">
                <select
                  value={selectedSemester}
                  onChange={(e) => setSelectedSemester(e.target.value)}
                  className="w-full max-w-xs px-3 py-2 bg-input-background border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary dark:bg-input-background"
                >
                  <option value="">Select semester</option>
                  <option value="1">Semester 1</option>
                  <option value="2">Semester 2</option>
                  <option value="3">Semester 3</option>
                  <option value="4">Semester 4</option>
                  <option value="5">Semester 5</option>
                  <option value="6">Semester 6</option>
                </select>
              </div>
            )}

            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="radio"
                name="scope"
                value="subject"
                checked={scope === "subject"}
                onChange={(e) => setScope(e.target.value as any)}
                className="w-4 h-4 text-primary"
              />
              <div>
                <div className="font-medium">Subject Level</div>
                <div className="text-sm text-muted-foreground">Export individual subject details</div>
              </div>
            </label>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-6 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        >
          <Download className="h-4 w-4" />
          Export Data
        </button>
      </div>
    </div>
  );
}
