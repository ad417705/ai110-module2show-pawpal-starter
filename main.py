from pawpal_system import Owner, Pet, Task, Scheduler

dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5)

dog_tasks = [
    Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise", pet=dog),
    Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding", pet=dog),
    Task(title="Brush coat", duration_minutes=15, priority="medium", category="grooming", pet=dog),
    Task(title="Play fetch", duration_minutes=20, priority="low", category="play", pet=dog),
]

cat_tasks = [
    Task(title="Clean litter box", duration_minutes=10, priority="high", category="hygiene", pet=cat),
    Task(title="Feed breakfast", duration_minutes=5, priority="high", category="feeding", pet=cat),
    Task(title="Trim nails", duration_minutes=15, priority="medium", category="grooming", pet=cat),
    Task(title="Laser pointer playtime", duration_minutes=20, priority="low", category="play", pet=cat),
]

owner_dog = Owner(name="Alex", available_minutes=60, pet=dog, tasks=dog_tasks)
owner_cat = Owner(name="Alex", available_minutes=60, pet=cat, tasks=cat_tasks)

dog_scheduler = Scheduler(owner=owner_dog)
cat_scheduler = Scheduler(owner=owner_cat)

dog_schedule = dog_scheduler.generate_schedule()
cat_schedule = cat_scheduler.generate_schedule()

print("=" * 40)
print("       Today's Schedule - PawPal+")
print("=" * 40)
print(f"Owner: {owner_dog.name} | Available: {owner_dog.available_minutes} min\n")

print(f"--- {dog.name} the {dog.species} (age {dog.age}) ---")
print(dog_schedule.explain())

print()

print(f"--- {cat.name} the {cat.species} (age {cat.age}) ---")
print(cat_schedule.explain())
print("=" * 40)

# ── Edit task demo ────────────────────────────────────────────────────────────
print()
print("=" * 40)
print("       Edit Task Demo")
print("=" * 40)

# Edit index 2 (Brush coat): bump priority to high and extend duration
updated_brush = Task(
    title="Brush coat",
    duration_minutes=20,
    priority="high",
    category="grooming",
    pet=dog,
)
dog_scheduler.edit_task(2, updated_brush)
print(f"Updated task at index 2: '{updated_brush.title}' — {updated_brush.duration_minutes} min, {updated_brush.priority} priority")

updated_schedule = dog_scheduler.generate_schedule()
print("\nRegenerated schedule after edit:")
print(updated_schedule.explain())
print("=" * 40)
