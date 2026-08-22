const API_BASE = import.meta.env.VITE_API_BASE ?? "/api/v1";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function getToken() {
  return localStorage.getItem("access_token");
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(body.detail ?? `Request failed (${res.status})`, res.status);
  }

  // 204 No Content etc.
  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function login(email: string, password: string) {
  const data = await apiFetch<{ access: string; refresh: string }>("/token/", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

export interface Project {
  id: string;
  title: string;
  description: string;
  created_by: string;
  created_by_username: string;
  organization: string;
  created_at: string;
  updated_at: string;
  task_count: number;
}

// file_url from the backend is a relative path (served by Django's MEDIA_URL,
// e.g. /media/exports/x.csv) — resolve it against the API's origin, not the
// frontend's, or the browser tries to navigate within the React app instead.
const BACKEND_ORIGIN = import.meta.env.VITE_BACKEND_ORIGIN ?? "http://localhost:8000";
export function resolveMediaUrl(path: string) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${BACKEND_ORIGIN}${path}`;
}

export function listProjects() {
  return apiFetch<Project[]>("/projects/");
}

export interface ExportJob {
  id: string;
  status: string;
  file_url: string;
  created_at: string;
  completed_at: string | null;
}

export interface Task {
  id: string;
  project: string;
  title: string;
  description: string;
  assigned_to: string | null;
  is_done: boolean;
  due_date: string | null;
}

export function listTasks(projectId: string) {
  return apiFetch<Task[]>(`/tasks/?project=${projectId}`);
}

export interface ExportJob {
  id: string;
  status: string; // PENDING / PROCESSING / COMPLETED / FAILED
  file_url: string;
  created_at: string;
  completed_at: string | null;
}


export function triggerExport(idempotencyKey: string) {
  return apiFetch<ExportJob>("/projects/export/", {
    method: "POST",
    headers: { "Idempotency-Key": idempotencyKey },
  });
}

export function getExportStatus(jobId: string) {
  return apiFetch<ExportJob>(`/export-jobs/${jobId}/`);
}