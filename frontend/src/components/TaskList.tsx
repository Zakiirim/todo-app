import { ClipboardList } from 'lucide-react';
import { TaskItem } from './TaskItem';
import type { Task } from '../types/task.types';

interface TaskListProps {
  tasks: Task[];
  onDelete: (id: string) => void;
  onUpdate: (id: string, updates: Partial<Task>) => void;
}

export function TaskList({ tasks, onDelete, onUpdate }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <ClipboardList className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks yet</h3>
        <p className="text-gray-600">Create your first task to get started!</p>
      </div>
    );
  }

  const groupedTasks = {
    urgent: tasks.filter((t) => t.category === 'urgent'),
    work: tasks.filter((t) => t.category === 'work'),
    personal: tasks.filter((t) => t.category === 'personal'),
  };

  const renderGroup = (title: string, items: Task[], count: number) => {
    if (items.length === 0) return null;

    return (
      <div key={title} className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3 flex items-center gap-2">
          {title}
          <span className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded-full">
            {count}
          </span>
        </h3>
        <div className="space-y-3">
          {items.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onDelete={onDelete}
              onUpdate={onUpdate}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div>
      {renderGroup('Urgent', groupedTasks.urgent, groupedTasks.urgent.length)}
      {renderGroup('Work', groupedTasks.work, groupedTasks.work.length)}
      {renderGroup('Personal', groupedTasks.personal, groupedTasks.personal.length)}
    </div>
  );
}
