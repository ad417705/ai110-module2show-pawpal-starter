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

    def priority_score(self) -> int:
        """Convert priority label to a numeric score for sorting."""
        pass


@dataclass
class Schedule:
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0

    def explain(self) -> str:
        """Return a human-readable explanation of what was scheduled and why."""
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def generate_schedule(self) -> Schedule:
        """Build and return a Schedule based on priority and available time."""
        pass
