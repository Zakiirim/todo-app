import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters'),
  description: z.string()
    .max(2000, 'Description must be less than 2000 characters')
    .optional(),
  estimated_time: z.number()
    .min(0, 'Estimated time must be positive')
    .max(1440, 'Estimated time cannot exceed 24 hours')
    .optional(),
});

export function sanitizeInput(input: string): string {
  // Remove HTML tags and escape special characters
  return input
    .replace(/<[^>]*>/g, '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .trim();
}
