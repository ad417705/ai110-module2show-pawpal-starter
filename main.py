from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Alex", available_minutes=60)

dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5)

dog_tasks = [
    Task(title="Morning walk", duration_minutes=30, priority="high", category="exercise"),
    Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding"),
    Task(title="Brush coat", duration_minutes=15, priority="medium", category="grooming"),
    Task(title="Play fetch", duration_minutes=20, priority="low", category="play"),
]

cat_tasks = [
    Task(title="Clean litter box", duration_minutes=10, priority="high", category="hygiene"),
    Task(title="Feed breakfast", duration_minutes=5, priority="high", category="feeding"),
    Task(title="Trim nails", duration_minutes=15, priority="medium", category="grooming"),
    Task(title="Laser pointer playtime", duration_minutes=20, priority="low", category="play"),
]

dog_schedule = Scheduler(owner=owner, pet=dog, tasks=dog_tasks).generate_schedule()
cat_schedule = Scheduler(owner=owner, pet=cat, tasks=cat_tasks).generate_schedule()

print("=" * 40)
print("       Today's Schedule - PawPal+")
print("=" * 40)
print(f"Owner: {owner.name} | Available: {owner.available_minutes} min\n")

print(f"--- {dog.name} the {dog.species} (age {dog.age}) ---")
print(dog_schedule.explain())

print()

print(f"--- {cat.name} the {cat.species} (age {cat.age}) ---")
print(cat_schedule.explain())
print("=" * 40)
