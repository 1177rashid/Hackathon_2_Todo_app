"""
Dashboard Routes - Todo App Phase II
Referencing: @backend/CLAUDE.md, @specs/api/rest-endpoints.md

All endpoints require JWT authentication via Better Auth.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from datetime import datetime

from app.database import get_session
from app.models import Task, User
from app.schemas import DashboardStatsResponse, ActivityItem
from app.auth import get_current_user, verify_user_access

router = APIRouter()

@router.get("/{user_id}/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get dashboard statistics for a user.

    Requires: Bearer JWT token in Authorization header

    Returns:
    - total_tasks: Total number of tasks
    - pending_tasks: Number of incomplete tasks
    - completed_tasks: Number of completed tasks
    - completion_rate: Percentage of completed tasks (0-100)
    - recent_activity: Last 10 task activities
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user)
    # Get total tasks count
    total_tasks = session.exec(
        select(func.count(Task.id)).where(Task.user_id == user_id)
    ).one()

    # Get pending tasks count
    pending_tasks = session.exec(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == False
        )
    ).one()

    # Get completed tasks count
    completed_tasks = session.exec(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True
        )
    ).one()

    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Get recent activity (last 10 tasks ordered by created/updated time)
    # For now, we'll show recently created tasks as "created" actions
    # In a production app, you'd have a separate activity log table
    recent_tasks = session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.updated_at.desc())
        .limit(10)
    ).all()

    # Build activity feed
    recent_activity = []
    for task in recent_tasks:
        # Determine action based on task state
        if task.completed:
            action = "completed"
            timestamp = task.updated_at
        else:
            # If task was just created (created_at ≈ updated_at), show as "created"
            time_diff = (task.updated_at - task.created_at).total_seconds()
            if time_diff < 5:  # Within 5 seconds
                action = "created"
                timestamp = task.created_at
            else:
                action = "updated"
                timestamp = task.updated_at

        recent_activity.append(ActivityItem(
            task_id=task.id,
            task_title=task.title,
            action=action,
            timestamp=timestamp
        ))

    return DashboardStatsResponse(
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        completion_rate=round(completion_rate, 2),
        recent_activity=recent_activity
    )
