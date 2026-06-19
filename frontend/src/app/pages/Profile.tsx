import { useEffect, useState } from "react";
import { User, Mail, Phone, Hash, BookOpen, Building2, Tag, CreditCard } from "lucide-react";
import { Loader } from "../components/Loader";
import { ErrorMessage } from "../components/ErrorMessage";
import { api } from "../lib/api";

type ProfileData = Awaited<ReturnType<typeof api.getProfile>>;

export function Profile() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState<ProfileData | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getProfile();
      setProfile(data);
      // Cache reg_no for result detail calls
      if (data.reg_no) {
        localStorage.setItem("reg_no", data.reg_no);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load profile");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader message="Loading profile..." />;
  if (error) return <ErrorMessage message={error} retry={fetchProfile} />;
  if (!profile) return null;

  const fields = [
    { label: "Full Name", value: profile.full_name, icon: User },
    { label: "Registration No", value: profile.reg_no, icon: Hash },
    { label: "Email", value: profile.email, icon: Mail },
    { label: "Mobile No", value: profile.mob_no, icon: Phone },
    { label: "Parent Mobile No", value: profile.parent_mob_no, icon: Phone },
    { label: "College", value: profile.college, icon: Building2 },
    { label: "Degree Code", value: profile.degree, icon: BookOpen },
    { label: "Caste Category", value: profile.category, icon: Tag },
    { label: "Fee Type", value: profile.fee_type, icon: CreditCard },
  ].filter((f) => f.value);

  return (
    <div className="space-y-6">
      <div>
        <h1>Profile</h1>
        <p className="text-sm text-muted-foreground">Your academic profile and personal information</p>
      </div>

      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-center gap-4 mb-6 pb-6 border-b border-border">
          {profile.photo ? (
            <img
              src={profile.photo}
              alt={profile.full_name}
              className="h-16 w-16 rounded-full object-cover"
            />
          ) : (
            <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="h-8 w-8 text-primary" />
            </div>
          )}
          <div>
            <div className="text-xl font-medium">{profile.full_name}</div>
            <div className="text-sm text-muted-foreground">{profile.reg_no}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {fields.map((field) => {
            const Icon = field.icon;
            return (
              <div key={field.label} className="space-y-1">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Icon className="h-4 w-4" />
                  <span>{field.label}</span>
                </div>
                <div className="font-medium">{field.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
