import { useState } from "react";
import { TaskForm } from "./components/TaskForm";
import { TaskItem } from "./components/TaskItem";
import { Filter, useTasks } from "./useTasks";

const FILTERS: Filter[] = ["all", "open", "done"];

export default function App() {
  const [filter, setFilter] = useState<Filter>("all");
  const { tasks, loading, error, add, toggle, remove } = useTasks(filter);

  return (
    <main className="container">
      <h1>Tasks</h1>
      <TaskForm onAdd={add} />
      <nav className="filters">
        {FILTERS.map((f) => (
          <button key={f} className={f === filter ? "active" : ""} onClick={() => setFilter(f)}>{f}</button>
        ))}
      </nav>
      {error && <p className="error">{error}</p>}
      {loading ? <p className="muted">Loading…</p> : tasks.length === 0 ? (
        <p className="muted">Nothing here yet.</p>
      ) : (
        <ul className="list">
          {tasks.map((t) => <TaskItem key={t.id} task={t} onToggle={toggle} onDelete={remove} />)}
        </ul>
      )}
    </main>
  );
}
