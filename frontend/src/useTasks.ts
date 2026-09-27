import { useCallback, useEffect, useState } from "react";
import { Task, tasksApi } from "./api/client";

export type Filter = "all" | "open" | "done";

// State + data-fetching hook: swap for React Query later without touching components.
export function useTasks(filter: Filter) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const done = filter === "all" ? undefined : filter === "done";
      setTasks((await tasksApi.list(done)).items);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { refresh(); }, [refresh]);

  const run = (fn: () => Promise<unknown>) => async () => {
    try { await fn(); await refresh(); } catch (e) { setError((e as Error).message); }
  };

  return {
    tasks, loading, error,
    add: (title: string) => run(() => tasksApi.create(title))(),
    toggle: (t: Task) => run(() => tasksApi.update(t.id, { done: !t.done }))(),
    remove: (id: number) => run(() => tasksApi.remove(id))(),
  };
}
