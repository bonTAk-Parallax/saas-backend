import { useState, useRef, useEffect } from "react";
import { triggerExport, getExportStatus, resolveMediaUrl } from "../lib/api";
import type { ExportJob } from "../lib/api";

const LAST_JOB_KEY = "last_export_job_id";

function makeIdempotencyKey() {
  return crypto.randomUUID();
}

function isTerminal(status: string) {
  const s = status.toUpperCase();
  return s.includes("FAIL") || s.includes("COMPLET") || s.includes("DONE");
}

function isFailed(status: string) {
  return status.toUpperCase().includes("FAIL");
}

export default function ExportButton() {
  const [job, setJob] = useState<ExportJob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [triggering, setTriggering] = useState(false);
  const [checking, setChecking] = useState(false);
  const keyRef = useRef(makeIdempotencyKey());
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Recover the last job on page load/reload, so a refresh doesn't lose status.
  useEffect(() => {
    const lastId = localStorage.getItem(LAST_JOB_KEY);
    if (lastId) {
      getExportStatus(lastId)
        .then((j) => {
          setJob(j);
          if (!isTerminal(j.status)) startPolling(lastId);
        })
        .catch(() => localStorage.removeItem(LAST_JOB_KEY));
    }
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function startPolling(jobId: string) {
    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      try {
        const updated = await getExportStatus(jobId);
        setJob(updated);
        if (isTerminal(updated.status) && pollRef.current) {
          clearInterval(pollRef.current);
        }
      } catch {
        if (pollRef.current) clearInterval(pollRef.current);
      }
    }, 2000);
  }

  async function handleTrigger() {
    setError(null);
    setTriggering(true);
    try {
      const created = await triggerExport(keyRef.current);
      setJob(created);
      localStorage.setItem(LAST_JOB_KEY, created.id);
      if (!isTerminal(created.status)) startPolling(created.id);
      keyRef.current = makeIdempotencyKey(); // fresh key for next trigger
    } catch {
      setError("Export couldn't start. Try again.");
    } finally {
      setTriggering(false);
    }
  }

  async function handleRefresh() {
    if (!job) return;
    setChecking(true);
    try {
      const updated = await getExportStatus(job.id);
      setJob(updated);
      if (isTerminal(updated.status) && pollRef.current) {
        clearInterval(pollRef.current);
      }
    } catch {
      setError("Couldn't check status.");
    } finally {
      setChecking(false);
    }
  }

  const inProgress = job ? !isTerminal(job.status) : false;

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={handleTrigger}
        disabled={triggering || inProgress}
        className="rounded-lg border border-[#D1D5DB] bg-white px-3.5 py-2.5 text-[13px] font-medium text-[#111827]
                   shadow-sm hover:bg-[#F9FAFB] disabled:opacity-60 disabled:cursor-not-allowed transition-colors
                   focus:outline-none focus:ring-4 focus:ring-[#3552F0]/10"
      >
        {triggering ? "Starting…" : "Export CSV"}
      </button>

      {job && (
        <>
          <div className="flex items-center gap-1.5 text-[12px] font-mono text-[#6B7280]">
            <StatusDot status={job.status} />
            <span>{job.status.toLowerCase()}</span>
          </div>

          {inProgress && (
            <button
              onClick={handleRefresh}
              disabled={checking}
              title="Check status"
              className="rounded-md p-1.5 text-[#6B7280] hover:bg-[#F3F4F6] hover:text-[#111827]
                         disabled:opacity-50 transition-colors"
            >
              <RefreshIcon spinning={checking} />
            </button>
          )}

          {job.file_url && (
            <a
              href={resolveMediaUrl(job.file_url)}
              className="rounded-lg bg-[#3552F0] text-white text-[13px] font-medium px-3.5 py-2.5
                         shadow-sm hover:bg-[#2C44D9] transition-colors"
            >
              Download CSV
            </a>
          )}

          {isFailed(job.status) && (
            <span className="text-[12px] text-[#B91C1C]">Export failed — try again.</span>
          )}
        </>
      )}

      {error && <span className="text-[12px] text-[#B91C1C]">{error}</span>}
    </div>
  );
}

function StatusDot({ status }: { status: string }) {
  const s = status.toUpperCase();
  let color = "bg-[#9CA3AF]"; // default / pending
  if (s.includes("FAIL")) color = "bg-[#DC2626]";
  else if (s.includes("COMPLET") || s.includes("DONE")) color = "bg-[#16A34A]";
  else if (s.includes("PROCESS") || s.includes("RUN")) color = "bg-[#D97B29] animate-pulse";
  return <span className={`inline-block h-1.5 w-1.5 rounded-full ${color}`} />;
}

function RefreshIcon({ spinning }: { spinning: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={`h-4 w-4 ${spinning ? "animate-spin" : ""}`}
    >
      <path d="M21 12a9 9 0 1 1-2.64-6.36" />
      <path d="M21 3v6h-6" />
    </svg>
  );
}
