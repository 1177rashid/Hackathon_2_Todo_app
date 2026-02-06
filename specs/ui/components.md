# UI Components and Pages

**Feature Branch**: `002-web-auth-specs`
**Created**: 2026-01-05
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Overview
Phase II introduces a responsive, authenticated web experience built on Next.js 16+ with Tailwind CSS. The UI must implement the user stories in @specs/features/task-crud-web.md while integrating seamlessly with authentication (@specs/features/authentication.md) and REST APIs (@specs/api/rest-endpoints.md).

## Pages

### Login Page
- Displays email/password form with validation and error messaging.
- Calls `/auth/login` endpoint and stores JWT via secure storage (httpOnly cookie or memory + CSRF mitigation).
- Redirects authenticated users to `/dashboard`.

### Signup Page
- Mirrors login UI but performs account creation.
- Shows password policy hints and success confirmation instructing users to log in.

### Dashboard Page
- Main task list view after authentication.
- Contains filters, sorting controls, and "Add Task" button.
- Uses Suspense/loading states while fetching data.

### TaskForm Modal/Page
- Reusable form for create/edit operations.
- Includes title input, description textarea, optional due date picker.
- Performs client-side validation before submitting to API.

## Components

### Layout/Header
- Persistent navigation with app name and Logout button.
- Displays current user email fetched from auth context.

### TaskList
- Receives `tasks: TaskViewModel[]` and `onToggle`, `onEdit`, `onDelete` callbacks.
- Responsible for empty state and virtualization if list grows large.

### TaskItem
- Individual row showing title, status pill, created date, optional due date.
- Contains action buttons (edit, delete) and completion toggle.

### TaskForm
- Controlled component used by modal/page.
- Emits `onSubmit(TaskFormValues)` and handles inline error display.

### Toast/Alert System
- Global feedback mechanism for success/failure states.
- Central store to avoid duplicate implementations.

## State Management Approach
- Use React Server Components for data fetching where possible; client components handle interactions.
- API client hook (e.g., `useTasksApi`) encapsulates fetch logic with SWR or React Query for caching/invalidation.
- Auth context provider stores token and user metadata, refreshing as needed.
- Filters persisted via URL query parameters for shareable state.

## Responsive Design
- Tailwind breakpoints ensure layout adapts from mobile → desktop (stacked list on small screens, table-like view on large).
- Touch targets sized appropriately for mobile interactions.
- Dark mode uses Tailwind’s `dark:` variants, toggled via user preference stored in local storage.

## Accessibility
- All interactive elements must provide keyboard access and ARIA labels.
- Color choices must meet WCAG AA contrast.
- Toasts and modals must announce via ARIA live regions.

## Error Handling & Feedback
- Form-level validation errors displayed inline with actionable text.
- Global error boundary for unexpected failures routes users to a friendly fallback screen.
- Unauthorized (401) responses trigger logout flow and redirect to login with preserved intent path.

## Dependencies
- Tailwind CSS for utility-first styling.
- Headless UI (or similar) for accessible modals/dropdowns.
- Date picker library compliant with accessibility guidelines.
