"""
Task Service Layer: Cycle Detection Graph Algorithm & Time Calculations.
"""
from apps.core.exceptions import DependencyCycleException
from .models import Task, TaskDependency, TimeLog
from django.db.models import Sum

def check_for_dependency_cycle(predecessor_id, successor_id):
    """
    Ensures adding predecessor -> successor will not create a circular dependency graph.
    Uses Depth-First Search (DFS) traversal.
    """
    if predecessor_id == successor_id:
        raise DependencyCycleException("A task cannot depend on itself.")

    visited = set()
    
    def dfs(current_id):
        if current_id == predecessor_id:
            return True
        visited.add(current_id)
        
        # Follow outgoing BLOCKS dependencies from current_id
        outgoing_deps = TaskDependency.objects.filter(
            predecessor_id=current_id,
            dependency_type=TaskDependency.DependencyType.BLOCKS
        ).values_list('successor_id', flat=True)
        
        for next_id in outgoing_deps:
            if next_id not in visited:
                if dfs(next_id):
                    return True
        return False

    if dfs(successor_id):
        raise DependencyCycleException(
            "Dependency cycle detected! Adding this dependency would create a circular deadlock."
        )

def recalculate_task_actual_hours(task_id):
    """Recalculates total actual logged hours from TimeLogs."""
    total_minutes = TimeLog.objects.filter(task_id=task_id).aggregate(total=Sum('duration_minutes'))['total'] or 0
    actual_hours = round(total_minutes / 60.0, 2)
    Task.objects.filter(id=task_id).update(actual_hours=actual_hours)
    return actual_hours
