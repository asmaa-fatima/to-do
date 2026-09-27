import { Task } from "../api/client";

interface Props { task: Task; onToggle: (t: Task) => void; onDelete: (id: number) => void; }

export function TaskItem({ task, onToggle, onDelete }: Props) {
  return (
    <li className={task.done ? "item done" : "item"}>
      <label>
        <input type="checkbox" checked={task.done} onChange={() => onToggle(task)} />
        <span>{task.title}</span>
      </label>
      <button className="ghost" onClick={() => onDelete(task.id)} aria-label="Delete">✕</button>
    </li>
  );
}
