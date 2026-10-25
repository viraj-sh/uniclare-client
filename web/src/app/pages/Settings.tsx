export function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1>Settings</h1>
        <p className="text-sm text-muted-foreground">Manage your application preferences</p>
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