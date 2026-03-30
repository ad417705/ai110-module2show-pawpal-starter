from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal, Optional

PriorityLevel = Literal["low", "medium", "high"]


def parse_time(time_str: str) -> Optional[datetime.time]:
    """Turn '8:00 AM', '8:00AM', or '14:30' into a time object. Returns None if blank or unrecognized."""
    if not time_str or not time_str.strip():
        return None
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M"):
        try:
            return datetime.strptime(time_str.strip(), fmt).time()
        except ValueError:
            continue
    return None


def detect_conflicts(tasks: list) -> list:
    """Find pairs of tasks whose time windows overlap using a sort + sweep line algorithm.

    Complexity: O(n log n + k) where k is the number of conflict pairs.
    Tasks without a parseable time are ignored.
    """
    import heapq
    today = datetime.today()

    timed = []
    for t in tasks:
        start = parse_time(t.time)
        if start is not None:
            start_dt = datetime.combine(today, start)
            end_dt = start_dt + timedelta(minutes=t.duration_minutes)
            timed.append((start_dt, end_dt, t))

    timed.sort(key=lambda x: x[0])

    conflicts = []
    # heap entries: (end_dt, index, task) — index breaks ties so datetime comparison never falls through to task
    heap = []
    for i, (start_dt, end_dt, task) in enumerate(timed):
        # evict tasks that ended at or before this task starts — no overlap possible
        while heap and heap[0][0] <= start_dt:
            heapq.heappop(heap)
        # every task still in the heap overlaps with the current task
        for entry in heap:
            conflicts.append((entry[2], task))
        heapq.heappush(heap, (end_dt, i, task))

    return conflicts


@dataclass
class Pet:
    """Represents a pet with basic identifying information."""

    name: str
    species: str
    age: int


@dataclass
class Owner:
    """Represents a pet owner with a time budget and a list of tasks to schedule."""

    name: str
    available_minutes: int
    pet: Pet
    tasks: list = field(default_factory=list)


@dataclass
class Task:
    """A single pet-care task with scheduling metadata such as time, priority, and recurrence frequency."""

    title: str
    duration_minutes: int
    priority: PriorityLevel
    category: str
    pet: Optional[Pet] = None
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
    """The result of a scheduling run: tasks that fit within available time, tasks that were skipped, and any detected conflicts."""

    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    conflicts: list = field(default_factory=list)
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
        if self.conflicts:
            lines.append(f"Conflicts detected ({len(self.conflicts)}):")
            for a, b in self.conflicts:
                lines.append(f"  [!] '{a.title}' overlaps with '{b.title}'")
        return "\n".join(lines)


class Scheduler:
    """Manages task scheduling for an owner: sorting by time/priority, filtering by pet or status, and conflict detection."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with the given owner and their associated pet and tasks."""
        self.owner = owner
        self.pet = owner.pet
        self.tasks = owner.tasks

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks for a specific pet (case-insensitive). Returns all tasks if pet_name is blank."""
        if not pet_name or not pet_name.strip():
            return list(self.owner.tasks)
        name_lower = pet_name.strip().lower()
        return [t for t in self.owner.tasks if t.pet and t.pet.name.lower() == name_lower]

    def filter_by_status(self, completed: Optional[bool]) -> list[Task]:
        """Return tasks by completion status. Pass None to get all tasks."""
        if completed is None:
            return list(self.owner.tasks)
        return [t for t in self.owner.tasks if t.completed == completed]

    def add_task(self, task: Task) -> None:
        """Append a task to the scheduler's task list."""
        self.owner.tasks.append(task)

    def edit_task(self, task_index: int, updated_task: Task) -> None:
        """Replace the task at task_index with updated_task."""
        self.owner.tasks[task_index] = updated_task

    def mark_complete(self, task: Task) -> None:
        """Mark a task complete. If it has frequency='daily', append a new incomplete copy for the next occurrence."""
        task.mark_complete()
        if task.frequency == "daily":
            import copy
            next_task = copy.copy(task)
            next_task.completed = False
            self.owner.tasks.append(next_task)

    def generate_schedule(self) -> Schedule:
        """Build and return a Schedule based on priority and available time."""
        _LATEST = datetime.strptime("23:59", "%H:%M").time()
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (-t.priority_score(), parse_time(t.time) or _LATEST)
        )
        schedule = Schedule()
        remaining = self.owner.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                schedule.scheduled_tasks.append(task)
                schedule.total_duration += task.duration_minutes
                remaining -= task.duration_minutes
            else:
                schedule.skipped_tasks.append(task)
        schedule.conflicts = detect_conflicts(schedule.scheduled_tasks)
        return schedule
