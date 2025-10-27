import { useState } from 'react';
import { Edit2, Trash2, Clock, Calendar } from 'lucide-react';
import type { Task } from '../types/task.types';

interface TaskItemProps {
  task: Task;
  onDelete: (id: string) => void;
  onUpdate: (id: string, updates: Partial<Task>) => void;
}

export function TaskItem({ task, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.title);

  const categoryColors = {
    work: 'bg-blue-100 text-blue-700 border-blue-200',
    personal: 'bg-green-100 text-green-700 border-green-200',
    urgent: 'bg-red-100 text-red-700 border-red-200',
  };

  const handleSave = () => {
    if (editedTitle.trim() && editedTitle !== task.title) {
      onUpdate(task.id, { title: editedTitle.trim() });
    }
    setIsEditing(false);
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow animate-fade-in">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <input
              type="text"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
              onBlur={handleSave}
              onKeyDown={(e) => e.key === 'Enter' && handleSave()}
              className="w-full px-2 py-1 border border-primary-500 rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
              autoFocus
            />
          ) : (
            <h3 className="text-lg font-medium text-gray-900 mb-1 break-words">
              {task.title}
            </h3>
          )}

          {task.description && (
            <p className="text-sm text-gray-600 mb-2 break-words">{task.description}</p>
          )}

          <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500">
            <span className={`px-2 py-1 rounded-full border font-medium ${categoryColors[task.category]}`}>
              {task.category}
            </span>

            {task.estimated_time && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {task.estimated_time}m
              </span>
            )}

            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {formatDate(task.created_at)}
            </span>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
            title="Edit task"
          >
            <Edit2 className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            title="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
