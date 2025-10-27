export interface Task {
  id: string;
  title: string;
  description: string | null;
  category: 'work' | 'personal' | 'urgent';
  estimated_time: number | null;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  estimated_time?: number | null;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  category?: 'work' | 'personal' | 'urgent';
  estimated_time?: number | null;
}
