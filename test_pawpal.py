from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_scheduler_task_count():
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    scheduler = Scheduler(owner=owner, pet=pet, tasks=[])
    assert len(scheduler.tasks) == 0
    scheduler.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding"))
    assert len(scheduler.tasks) == 1
