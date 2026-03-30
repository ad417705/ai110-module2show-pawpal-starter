from dataclasses import dataclass, field
from typing import Literal

PriorityLevel = Literal["low", "medium", "high"]


@dataclass
class Pet:
    name: str
    species: str
    age: int


@dataclass
class Owner:
    name: str
    available_minutes: int


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: PriorityLevel
    category: str
    description: str = ""
    time: str = ""
    frequency: str = ""
    completed: bool = False

    def priority_score(self) -> int:
        """Convert priority label to a numeric score for sorting."""
        scores = {"high": 3, "medium": 2, "low": 1}
        return scores[self.priority]

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Schedule:
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0

    def explain(self) -> str:
        """Return a human-readable explanation of what was scheduled and why."""
        lines = []
        lines.append(f"Scheduled {len(self.scheduled_tasks)} task(s) totaling {self.total_duration} minutes:")
        for task in self.scheduled_tasks:
            lines.append(f"  [✓] {task.title} ({task.duration_minutes} min, {task.priority} priority, {task.category})")
        if self.skipped_tasks:
            lines.append(f"Skipped {len(self.skipped_tasks)} task(s) due to insufficient time:")
            for task in self.skipped_tasks:
                lines.append(f"  [✗] {task.title} ({task.duration_minutes} min, {task.priority} priority)")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def add_task(self, task: Task) -> None:
        """Append a task to the scheduler's task list."""
        self.tasks.append(task)

    def generate_schedule(self) -> Schedule:
        """Build and return a Schedule based on priority and available time."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority_score(), reverse=True)
        schedule = Schedule()
        remaining = self.owner.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                schedule.scheduled_tasks.append(task)
                schedule.total_duration += task.duration_minutes
                remaining -= task.duration_minutes
            else:
                schedule.skipped_tasks.append(task)
        return schedule
