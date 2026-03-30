from pawpal_system import Owner, Pet, Task, Scheduler, parse_time, detect_conflicts


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_scheduler_task_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    owner = Owner(name="Alex", available_minutes=60, pet=pet)
    scheduler = Scheduler(owner=owner)
    assert len(scheduler.tasks) == 0
    scheduler.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding", pet=pet))
    assert len(scheduler.tasks) == 1


# --- parse_time tests ---

def test_parse_time_valid_am():
    t = parse_time("8:00 AM")
    assert t is not None
    assert t.hour == 8 and t.minute == 0


def test_parse_time_valid_24h():
    t = parse_time("14:30")
    assert t is not None
    assert t.hour == 14 and t.minute == 30


def test_parse_time_empty_returns_none():
    assert parse_time("") is None
    assert parse_time("   ") is None


def test_parse_time_invalid_returns_none():
    assert parse_time("morning") is None
    assert parse_time("soon") is None


# --- Sorting tests ---

def test_generate_schedule_secondary_sort_by_time():
    pet = Pet("Buddy", "dog", 3)
    t1 = Task("Late Walk", 10, "high", "exercise", time="2:00 PM")
    t2 = Task("Early Walk", 10, "high", "exercise", time="8:00 AM")
    owner = Owner("Alex", 60, pet=pet, tasks=[t1, t2])
    schedule = Scheduler(owner).generate_schedule()
    assert schedule.scheduled_tasks[0].title == "Early Walk"
    assert schedule.scheduled_tasks[1].title == "Late Walk"


# --- Filter tests ---

def test_filter_by_status_incomplete():
    pet = Pet("Mochi", "cat", 2)
    t1 = Task("Feed", 10, "high", "feeding", pet=pet)
    t2 = Task("Walk", 20, "medium", "exercise", pet=pet)
    t2.mark_complete()
    owner = Owner("Jordan", 60, pet=pet, tasks=[t1, t2])
    result = Scheduler(owner).filter_by_status(completed=False)
    assert len(result) == 1
    assert result[0].title == "Feed"


def test_filter_by_status_none_returns_all():
    pet = Pet("Mochi", "cat", 2)
    t1 = Task("Feed", 10, "high", "feeding", pet=pet)
    t2 = Task("Walk", 20, "medium", "exercise", pet=pet)
    owner = Owner("Jordan", 60, pet=pet, tasks=[t1, t2])
    assert len(Scheduler(owner).filter_by_status(None)) == 2


def test_filter_by_pet_name():
    dog = Pet("Buddy", "dog", 3)
    cat = Pet("Mochi", "cat", 2)
    t1 = Task("Walk", 20, "medium", "exercise", pet=dog)
    t2 = Task("Feed cat", 5, "high", "feeding", pet=cat)
    owner = Owner("Alex", 60, pet=dog, tasks=[t1, t2])
    result = Scheduler(owner).filter_by_pet("Mochi")
    assert len(result) == 1
    assert result[0].title == "Feed cat"


# --- Conflict detection tests ---

def test_detect_conflicts_overlapping_tasks():
    t1 = Task("Walk", 30, "high", "exercise", time="8:00 AM")
    t2 = Task("Feed", 20, "high", "feeding", time="8:15 AM")
    conflicts = detect_conflicts([t1, t2])
    assert len(conflicts) == 1
    assert (t1, t2) in conflicts


def test_detect_conflicts_non_overlapping_tasks():
    t1 = Task("Walk", 30, "high", "exercise", time="8:00 AM")
    t2 = Task("Feed", 20, "high", "feeding", time="8:30 AM")
    assert detect_conflicts([t1, t2]) == []


def test_detect_conflicts_no_time_no_conflict():
    t1 = Task("Walk", 30, "high", "exercise", time="")
    t2 = Task("Feed", 20, "high", "feeding", time="")
    assert detect_conflicts([t1, t2]) == []


def test_detect_conflicts_mixed_timed_and_untimed():
    t1 = Task("Walk", 30, "high", "exercise", time="8:00 AM")
    t2 = Task("Feed", 20, "high", "feeding", time="")
    assert detect_conflicts([t1, t2]) == []


def test_schedule_has_conflicts_field():
    pet = Pet("Buddy", "dog", 3)
    t1 = Task("Walk", 60, "high", "exercise", time="8:00 AM")
    t2 = Task("Feed", 30, "high", "feeding", time="8:15 AM")
    owner = Owner("Alex", 120, pet=pet, tasks=[t1, t2])
    schedule = Scheduler(owner).generate_schedule()
    assert hasattr(schedule, "conflicts")
    assert len(schedule.conflicts) == 1
