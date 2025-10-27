import { useState, useEffect } from 'react';
import { CheckSquare } from 'lucide-react';
import { TaskForm } from './components/TaskForm';
import { TaskList } from './components/TaskList';
import { ToastContainer } from './components/Toast';
import { Modal } from './components/Modal';
import { LoadingSkeleton } from './components/LoadingSkeleton';
import { useToast } from './hooks/useToast';
import { taskApi } from './services/api';
import { sanitizeInput } from './utils/validators';
import type { Task, CreateTaskInput } from './types/task.types';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deleteModalId, setDeleteModalId] = useState<string | null>(null);
  const { toasts, showToast, removeToast } = useToast();

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const data = await taskApi.getAllTasks();
      setTasks(data);
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to load tasks', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTask = async (input: CreateTaskInput) => {
    try {
      // Sanitize inputs before sending
      const sanitized = {
        ...input,
        title: sanitizeInput(input.title),
        description: input.description ? sanitizeInput(input.description) : undefined,
      };

      const newTask = await taskApi.createTask(sanitized);

      // Optimistic update
      setTasks((prev) => [newTask, ...prev]);
      showToast('Task created successfully!', 'success');
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to create task', 'error');
    }
  };

  const handleUpdateTask = async (id: string, updates: Partial<Task>) => {
    try {
      const sanitized = {
        ...updates,
        title: updates.title ? sanitizeInput(updates.title) : undefined,
        description: updates.description ? sanitizeInput(updates.description) : undefined,
      };

      const updatedTask = await taskApi.updateTask(id, sanitized);

      setTasks((prev) =>
        prev.map((task) => (task.id === id ? updatedTask : task))
      );
      showToast('Task updated successfully!', 'success');
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to update task', 'error');
    }
  };

  const handleDeleteTask = async (id: string) => {
    setDeleteModalId(id);
  };

  const confirmDelete = async () => {
    if (!deleteModalId) return;

    try {
      await taskApi.deleteTask(deleteModalId);

      // Optimistic update
      setTasks((prev) => prev.filter((task) => task.id !== deleteModalId));
      showToast('Task deleted successfully!', 'success');
    } catch (error: any) {
      showToast(error.response?.data?.detail || 'Failed to delete task', 'error');
    } finally {
      setDeleteModalId(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <div className="flex items-center justify-center gap-3 mb-2">
            <CheckSquare className="w-10 h-10 text-primary-600" />
            <h1 className="text-4xl font-bold text-gray-900">Smart Todo List</h1>
          </div>
          <p className="text-gray-600">Organize your tasks with automatic categorization</p>
        </header>

        <TaskForm onSubmit={handleCreateTask} />

        {isLoading ? (
          <LoadingSkeleton />
        ) : (
          <TaskList
            tasks={tasks}
            onDelete={handleDeleteTask}
            onUpdate={handleUpdateTask}
          />
        )}

        <ToastContainer toasts={toasts} onClose={removeToast} />

        <Modal
          isOpen={deleteModalId !== null}
          onClose={() => setDeleteModalId(null)}
          onConfirm={confirmDelete}
          title="Delete Task"
        >
          Are you sure you want to delete this task? This action cannot be undone.
        </Modal>
      </div>
    </div>
  );
}

export default App;
