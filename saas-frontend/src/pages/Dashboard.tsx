import { useEffect, useState } from "react";
import { listProjects, logout, ApiError } from "../lib/api";
import type { Project } from "../lib/api";
import { useNavigate, Link } from "react-router-dom";
import ExportButton from "../components/ExportButton";

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    listProjects()
      .then(setProjects)
      .catch((err) => {
        setError(
          err instanceof ApiError
            ? `${err.status}: ${err.message}`
            : "Network error — check the API is running and reachable."
        );
      });
  }, []);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-[#EEF0F4]">
      <header className="bg-white shadow-[0_1px_2px_rgba(16,24,40,0.06)]">
        <div className="max-w-5xl mx-auto px-6 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="h-8 w-8 rounded-lg bg-[#1B2233] flex items-center justify-center">
              <span className="text-[#7C9BFF] text-[11px] font-mono font-semibold">PP</span>
            </div>
            <span className="font-semibold text-[15px] text-[#111827] tracking-tight">ProjectPulse</span>
          </div>
          <button
            onClick={handleLogout}
            className="text-[13px] text-[#6B7280] hover:text-[#111827] transition-colors font-medium"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex items-end justify-between mb-7">
          <div>
            <h1 className="text-[22px] font-semibold text-[#111827] tracking-tight">Projects</h1>
            <p className="text-[13px] text-[#6B7280] mt-1">Every project in your workspace.</p>
          </div>
          <div className="flex items-center gap-3">
            <ExportButton />
            <button
              className="rounded-lg bg-[#3552F0] text-white text-[13px] font-medium px-4 py-2.5
                         shadow-[0_1px_2px_rgba(16,24,40,0.1)] hover:bg-[#2C44D9] transition-colors"
            >
              New project
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-[#FEF2F2] border border-[#FECACA] px-4 py-3 mb-5">
            <p className="text-[13px] text-[#B91C1C]">{error}</p>
          </div>
        )}

        {!projects && !error && (
          <div className="text-[13px] text-[#6B7280] font-mono">loading projects…</div>
        )}

        {projects && projects.length === 0 && (
          <div className="rounded-xl border border-dashed border-[#D1D5DB] bg-white px-6 py-16 text-center">
            <p className="text-[14px] text-[#374151] font-medium">No projects yet</p>
            <p className="text-[13px] text-[#6B7280] mt-1">Create your first one to get started.</p>
          </div>
        )}

        {projects && projects.length > 0 && (
          <div className="bg-white rounded-xl overflow-hidden shadow-[0_1px_2px_rgba(16,24,40,0.06),0_1px_3px_rgba(16,24,40,0.05)]">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[#F9FAFB]">
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Name</th>
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Created by</th>
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Tasks</th>
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Updated</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((p) => (
                  <tr key={p.id} className="border-t border-[#F1F2F4] hover:bg-[#FAFBFC] transition-colors">
                    <td className="px-5 py-4">
                      <div className="font-medium text-[#111827] text-[14px]">{p.title}</div>
                      <div className="text-[12px] text-[#6B7280] mt-0.5">{p.description}</div>
                    </td>
                    <td className="px-5 py-4 text-[13px] text-[#374151]">
                      {p.created_by_username}
                    </td>
                    <td className="px-5 py-4">
                      <Link
                        to={`/projects/${p.id}/tasks`}
                        className="inline-flex items-center rounded-full bg-[#EEF0F4] px-2.5 py-1 text-[11px] font-mono font-medium text-[#374151]
                                   hover:bg-[#E0E3EA] transition-colors"
                      >
                        {p.task_count}
                      </Link>
                    </td>
                    <td className="px-5 py-4 font-mono text-[12px] text-[#6B7280]">
                      {new Date(p.updated_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
