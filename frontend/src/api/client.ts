// Single place for HTTP concerns (base URL, errors, JSON). Components never call fetch directly.
export interface Task {
  id: number;
  title: string;
  description: string | null;
  done: boolean;
  created_at: string;
  updated_at: string;
}
export interface Page<T> { items: T[]; total: number; limit: number; offset: number; }

const BASE = import.meta.env.VITE_API_URL ?? "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : `HTTP ${res.status}`);
  }
  return (res.status === 204 ? undefined : await res.json()) as T;
}

export const tasksApi = {
  list: (done?: boolean) =>
    request<Page<Task>>(`/tasks?limit=100${done === undefined ? "" : `&done=${done}`}`),
  create: (title: string, description?: string) =>
    request<Task>("/tasks", { method: "POST", body: JSON.stringify({ title, description }) }),
  update: (id: number, patch: Partial<Pick<Task, "title" | "description" | "done">>) =>
    request<Task>(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(patch) }),
  remove: (id: number) => request<void>(`/tasks/${id}`, { method: "DELETE" }),
};
