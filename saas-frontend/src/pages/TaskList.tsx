import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { listTasks, ApiError } from "../lib/api";
import type { Task } from "../lib/api";

export default function TaskList() {
  const { projectId } = useParams<{ projectId: string }>();
  const [tasks, setTasks] = useState<Task[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId) return;
    listTasks(projectId)
      .then(setTasks)
      .catch((err) => {
        setError(
          err instanceof ApiError
            ? `${err.status}: ${err.message}`
            : "Couldn't load tasks."
        );
      });
  }, [projectId]);

  return (
    <div className="min-h-screen bg-[#EEF0F4]">
      <header className="bg-white shadow-[0_1px_2px_rgba(16,24,40,0.06)]">
        <div className="max-w-5xl mx-auto px-6 py-3.5 flex items-center gap-3">
          <Link to="/dashboard" className="text-[13px] text-[#6B7280] hover:text-[#111827] transition-colors">
            ← Projects
          </Link>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <h1 className="text-[22px] font-semibold text-[#111827] tracking-tight mb-7">Tasks</h1>

        {error && (
          <div className="rounded-lg bg-[#FEF2F2] border border-[#FECACA] px-4 py-3 mb-5">
            <p className="text-[13px] text-[#B91C1C]">{error}</p>
          </div>
        )}

        {!tasks && !error && (
          <div className="text-[13px] text-[#6B7280] font-mono">loading tasks…</div>
        )}

        {tasks && tasks.length === 0 && (
          <div className="rounded-xl border border-dashed border-[#D1D5DB] bg-white px-6 py-16 text-center">
            <p className="text-[14px] text-[#374151] font-medium">No tasks yet</p>
          </div>
        )}

        {tasks && tasks.length > 0 && (
          <div className="bg-white rounded-xl overflow-hidden shadow-[0_1px_2px_rgba(16,24,40,0.06),0_1px_3px_rgba(16,24,40,0.05)]">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[#F9FAFB]">
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Task</th>
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Done</th>
                  <th className="px-5 py-3 font-medium text-[#6B7280] text-[11px] uppercase tracking-wide text-left">Due</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((t) => (
                  <tr key={t.id} className="border-t border-[#F1F2F4]">
                    <td className="px-5 py-4">
                      <div className="font-medium text-[#111827] text-[14px]">{t.title}</div>
                      <div className="text-[12px] text-[#6B7280] mt-0.5">{t.description}</div>
                    </td>
                    <td className="px-5 py-4">
                      <span
                        className={`inline-block h-2 w-2 rounded-full ${
                          t.is_done ? "bg-[#16A34A]" : "bg-[#D1D5DB]"
                        }`}
                      />
                    </td>
                    <td className="px-5 py-4 font-mono text-[12px] text-[#6B7280]">
                      {t.due_date ? new Date(t.due_date).toLocaleDateString() : "—"}
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
