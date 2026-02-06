---
name: nextjs-app-router-patterns
description: Modern Next.js 16 App Router patterns for Phase 2 frontend. Automatically activates when discussing Next.js pages, server components, client components, API calls, routing, or frontend architecture.
---

# Next.js App Router Patterns Expert

You are the official Next.js Frontend Expert for this Hackathon II Todo project (Phase 2). Your responsibility is to ensure modern, performant Next.js 16 App Router code following React Server Components best practices.

## When to Activate

This skill automatically activates when the user mentions:
- Next.js 16 App Router pages or routing
- Server Components vs Client Components
- Frontend UI components
- API calls to FastAPI backend
- Better Auth integration (frontend)
- Tailwind CSS styling
- Form handling and validation
- Loading states and error handling
- TypeScript types for frontend

## Core Principles

1. **Server Components by Default**: Use 'use client' only when necessary
2. **API Client Abstraction**: Centralized backend communication
3. **Type Safety**: TypeScript for all components and API calls
4. **Authentication First**: Protect routes with Better Auth
5. **Error Boundaries**: Graceful error handling at component level
6. **Loading States**: Skeleton UIs and Suspense for better UX
7. **Accessibility**: Semantic HTML and ARIA attributes
8. **Responsive Design**: Mobile-first with Tailwind CSS

## Phase 2 Frontend Project Structure

```
hackathon-todo-app/
├── frontend/                          # Next.js application
│   ├── app/
│   │   ├── layout.tsx                # Root layout with auth provider
│   │   ├── page.tsx                  # Home page (redirect to /tasks)
│   │   ├── login/
│   │   │   └── page.tsx              # Login page (Better Auth)
│   │   ├── signup/
│   │   │   └── page.tsx              # Signup page (Better Auth)
│   │   ├── tasks/
│   │   │   ├── page.tsx              # Task list (Server Component)
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx          # Task detail page
│   │   │   └── layout.tsx            # Tasks layout (protected)
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/route.ts # Better Auth API routes
│   ├── components/
│   │   ├── ui/                       # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   ├── tasks/
│   │   │   ├── task-list.tsx         # Task list component
│   │   │   ├── task-item.tsx         # Single task card
│   │   │   ├── task-form.tsx         # Create/Edit form (Client Component)
│   │   │   └── task-filters.tsx      # Filter controls
│   │   ├── layout/
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── footer.tsx
│   │   └── auth/
│   │       ├── login-form.tsx        # Better Auth login
│   │       └── signup-form.tsx       # Better Auth signup
│   ├── lib/
│   │   ├── api-client.ts             # Backend API client
│   │   ├── auth.ts                   # Better Auth configuration
│   │   ├── utils.ts                  # Utility functions
│   │   └── types.ts                  # TypeScript types
│   ├── hooks/
│   │   ├── use-tasks.ts              # Custom hook for tasks
│   │   └── use-auth.ts               # Auth hook (Better Auth)
│   ├── public/
│   │   └── ...
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.local
```

## TypeScript Types

```typescript
// frontend/lib/types.ts

/**
 * Task model matching backend SQLModel schema.
 */
export interface Task {
  id: string;  // UUID as string
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;  // ISO 8601 datetime string
  updated_at: string;
}

/**
 * Request schema for creating a task.
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Request schema for updating a task.
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

/**
 * Response from GET /api/tasks endpoint.
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

/**
 * Task statistics from backend.
 */
export interface TaskStats {
  total: number;
  completed: number;
  incomplete: number;
}

/**
 * API error response.
 */
export interface ApiError {
  detail: string;
  error_code?: string;
}
```

## API Client Implementation

```typescript
// frontend/lib/api-client.ts
import { auth } from './auth';  // Better Auth instance

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * API Client for communicating with FastAPI backend.
 * Automatically includes JWT token from Better Auth session.
 */
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get JWT token from Better Auth session.
   */
  private async getAuthToken(): Promise<string | null> {
    const session = await auth.api.getSession();
    return session?.session.token || null;
  }

  /**
   * Make authenticated request to backend.
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken();

    if (!token) {
      throw new Error('Not authenticated');
    }

    const url = `${this.baseURL}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    // Handle authentication errors
    if (response.status === 401) {
      // Token expired or invalid - redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
      throw new Error('Authentication failed');
    }

    // Handle other errors
    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: 'Request failed',
      }));
      throw new Error(error.detail);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  // ==================== TASK ENDPOINTS ====================

  /**
   * Get all tasks for current user.
   * @param completed - Optional filter by completion status
   */
  async getTasks(completed?: boolean): Promise<TaskListResponse> {
    const params = new URLSearchParams();
    if (completed !== undefined) {
      params.append('completed', String(completed));
    }
    const query = params.toString() ? `?${params}` : '';
    return this.request<TaskListResponse>(`/api/tasks${query}`);
  }

  /**
   * Get a single task by ID.
   */
  async getTask(taskId: string): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}`);
  }

  /**
   * Create a new task.
   */
  async createTask(data: TaskCreate): Promise<Task> {
    return this.request<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing task.
   */
  async updateTask(taskId: string, data: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a task.
   */
  async deleteTask(taskId: string): Promise<void> {
    return this.request<void>(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Mark task as completed.
   */
  async completeTask(taskId: string): Promise<Task> {
    return this.request<Task>(`/api/tasks/${taskId}/complete`, {
      method: 'POST',
    });
  }

  /**
   * Get task statistics.
   */
  async getTaskStats(): Promise<TaskStats> {
    return this.request<TaskStats>('/api/tasks/stats/summary');
  }
}

export const apiClient = new ApiClient();
```

## Server Component Pattern (Default)

```tsx
// app/tasks/page.tsx
import { Suspense } from 'react';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskListSkeleton } from '@/components/tasks/task-list-skeleton';

/**
 * Tasks page - Server Component (default).
 * No 'use client' needed unless interactive state required.
 */
export default async function TasksPage({
  searchParams,
}: {
  searchParams: { completed?: string };
}) {
  // Server-side logic here (if needed)
  const completedFilter = searchParams.completed === 'true' ? true
    : searchParams.completed === 'false' ? false
    : undefined;

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">My Tasks</h1>
        <TaskForm />
      </div>

      <TaskFilters />

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList completedFilter={completedFilter} />
      </Suspense>
    </div>
  );
}
```

## Client Component Pattern (Interactive)

```tsx
// components/tasks/task-form.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { apiClient } from '@/lib/api-client';
import { TaskCreate } from '@/lib/types';

/**
 * Task form - Client Component (needs interactivity).
 * Uses 'use client' directive at the top.
 */
export function TaskForm() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await apiClient.createTask(formData);

      // Reset form and close modal
      setFormData({ title: '', description: '' });
      setIsOpen(false);

      // Refresh the page to show new task
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>
        + New Task
      </Button>

      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Create New Task</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium mb-1">
                  Title *
                </label>
                <Input
                  id="title"
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  maxLength={200}
                  required
                  placeholder="Enter task title"
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium mb-1">
                  Description
                </label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  maxLength={1000}
                  placeholder="Optional description"
                  rows={4}
                />
              </div>

              {error && (
                <div className="bg-red-50 text-red-600 p-3 rounded">
                  {error}
                </div>
              )}

              <div className="flex gap-3">
                <Button type="submit" disabled={isLoading || !formData.title.trim()}>
                  {isLoading ? 'Creating...' : 'Create Task'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsOpen(false)}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
```

## Custom Hook for Data Fetching

```typescript
// hooks/use-tasks.ts
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { Task, TaskListResponse } from '@/lib/types';

/**
 * Custom hook for fetching tasks.
 * Use in Client Components that need real-time updates.
 */
export function useTasks(completedFilter?: boolean) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.getTasks(completedFilter);
      setTasks(response.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [completedFilter]);

  const refresh = () => {
    fetchTasks();
  };

  return { tasks, isLoading, error, refresh };
}

// Usage in component:
// const { tasks, isLoading, error, refresh } = useTasks();
```

## Better Auth Integration

```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth/react';

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
  // Configure Better Auth with your settings
});

export const { signIn, signUp, signOut, useSession } = auth;
```

```tsx
// app/layout.tsx
import { SessionProvider } from '@/lib/auth';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
```

## Protected Route Pattern

```tsx
// app/tasks/layout.tsx
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';

/**
 * Tasks layout - Server Component that protects all task routes.
 * Redirects to login if not authenticated.
 */
export default async function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth.api.getSession();

  if (!session) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="container mx-auto p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Todo App</h1>
          <div>
            <span className="mr-4">{session.user.email}</span>
            <button onClick={() => auth.signOut()}>Logout</button>
          </div>
        </div>
      </header>

      <main>{children}</main>
    </div>
  );
}
```

## Task List Component

```tsx
// components/tasks/task-list.tsx
'use client';

import { useTasks } from '@/hooks/use-tasks';
import { TaskItem } from './task-item';
import { TaskListSkeleton } from './task-list-skeleton';

interface TaskListProps {
  completedFilter?: boolean;
}

export function TaskList({ completedFilter }: TaskListProps) {
  const { tasks, isLoading, error, refresh } = useTasks(completedFilter);

  if (isLoading) {
    return <TaskListSkeleton />;
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-600 p-4 rounded">
        <p>Error: {error}</p>
        <button onClick={refresh} className="underline mt-2">
          Try again
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-12">
        <p className="text-xl">No tasks found</p>
        <p className="mt-2">Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onUpdate={refresh} />
      ))}
    </div>
  );
}
```

## Task Item Component

```tsx
// components/tasks/task-item.tsx
'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { Task } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface TaskItemProps {
  task: Task;
  onUpdate: () => void;
}

export function TaskItem({ task, onUpdate }: TaskItemProps) {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleComplete = async () => {
    setIsUpdating(true);
    try {
      await apiClient.updateTask(task.id, {
        is_completed: !task.is_completed,
      });
      onUpdate();  // Refresh parent list
    } catch (err) {
      alert('Failed to update task');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setIsUpdating(true);
    try {
      await apiClient.deleteTask(task.id);
      onUpdate();  // Refresh parent list
    } catch (err) {
      alert('Failed to delete task');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <Card className="p-4">
      <div className="flex items-start gap-4">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={handleToggleComplete}
          disabled={isUpdating}
          className="mt-1 h-5 w-5 rounded border-gray-300"
        />

        <div className="flex-1">
          <h3
            className={`font-medium ${
              task.is_completed ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        <Button
          variant="destructive"
          size="sm"
          onClick={handleDelete}
          disabled={isUpdating}
        >
          Delete
        </Button>
      </div>
    </Card>
  );
}
```

## Loading Skeleton

```tsx
// components/tasks/task-list-skeleton.tsx
import { Card } from '@/components/ui/card';

export function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3, 4, 5].map((i) => (
        <Card key={i} className="p-4">
          <div className="flex items-start gap-4">
            <div className="h-5 w-5 bg-gray-200 rounded animate-pulse" />
            <div className="flex-1 space-y-2">
              <div className="h-5 bg-gray-200 rounded w-3/4 animate-pulse" />
              <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse" />
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
```

## Environment Variables

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Better Auth configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000/api/auth
```

## Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for hackathon theme
        primary: '#3b82f6',  // Blue
        secondary: '#8b5cf6',  // Purple
      },
    },
  },
  plugins: [],
};

export default config;
```

## Error Boundary Pattern

```tsx
// app/error.tsx
'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Error boundary caught:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
        <p className="text-gray-600 mb-4">{error.message}</p>
        <Button onClick={reset}>Try again</Button>
      </div>
    </div>
  );
}
```

## Common Mistakes to Avoid

❌ **Using 'use client' everywhere**: Most components should be Server Components
✅ **Selective 'use client'**: Only for interactivity (forms, hooks, event handlers)

❌ **Direct fetch in components**: `fetch('/api/tasks')` in every component
✅ **Centralized API client**: Use `apiClient.getTasks()` abstraction

❌ **No error handling**: Assuming requests always succeed
✅ **Try-catch blocks**: Handle errors gracefully with user feedback

❌ **No loading states**: Components flash or freeze
✅ **Suspense + skeletons**: Smooth loading experience

❌ **Inline styles**: `style={{ color: 'red' }}`
✅ **Tailwind classes**: `className="text-red-500"`

❌ **Token in localStorage**: `localStorage.setItem('token', token)`
✅ **Better Auth manages tokens**: Let Better Auth handle session storage

## Performance Best Practices

1. **Use Server Components** for static content (reduces JS bundle)
2. **Lazy load modals** with dynamic imports
3. **Optimize images** with Next.js Image component
4. **Debounce search inputs** to reduce API calls
5. **Cache API responses** with SWR or React Query (optional)
6. **Minimize 'use client' boundaries** for better performance

## Judge Evaluation Checklist

For a high-scoring Phase 2 frontend:
- [ ] Server Components used by default
- [ ] Client Components only where necessary ('use client')
- [ ] Centralized API client with proper error handling
- [ ] TypeScript types for all components and API calls
- [ ] Better Auth integration for authentication
- [ ] Protected routes redirect to login
- [ ] Loading states with skeletons
- [ ] Error boundaries for graceful failures
- [ ] Responsive design (mobile-first Tailwind)
- [ ] Accessible forms (labels, ARIA attributes)
- [ ] No console errors in production build

## Integration with Other Skills

- **spec-writing**: UI specs define component hierarchy and interactions
- **fastapi-rest-conventions**: Frontend consumes backend API routes
- **jwt-auth-best-practices**: Frontend sends JWT in Authorization header
- **python-cli-patterns**: Phase 1 console → Phase 2 web UI

Build a frontend that judges will love: fast, accessible, and beautifully designed!
