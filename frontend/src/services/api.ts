import axios from 'axios';
import type { Task, CreateTaskInput, UpdateTaskInput } from '../types/task.types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const taskApi = {
  async createTask(input: CreateTaskInput): Promise<Task> {
    const response = await api.post<Task>('/api/tasks', input);
    return response.data;
  },

  async getAllTasks(): Promise<Task[]> {
    const response = await api.get<Task[]>('/api/tasks');
    return response.data;
  },

  async updateTask(id: string, input: UpdateTaskInput): Promise<Task> {
    const response = await api.put<Task>(`/api/tasks/${id}`, input);
    return response.data;
  },

  async deleteTask(id: string): Promise<void> {
    await api.delete(`/api/tasks/${id}`);
  },
};
