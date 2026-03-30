import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown(
    "**PawPal+** helps pet owners plan their day. "
    "Add care tasks, set your available time, and let the scheduler build a priority-ordered plan for you and your pet."
)

st.divider()

# ── Owner & Pet ──────────────────────────────────────────────────────────────
st.subheader("Owner & Pet Info")

col_o, col_p = st.columns(2)
with col_o:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=10, max_value=480, value=60
    )
with col_p:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=2)

st.divider()

# ── Task entry ───────────────────────────────────────────────────────────────
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        category = st.selectbox(
            "Category",
            ["exercise", "feeding", "grooming", "medical", "play", "training", "general"],
        )
    with col5:
        task_time = st.text_input("Preferred time (optional)", placeholder="e.g. 8:00 AM")

    col6, col7 = st.columns(2)
    with col6:
        description = st.text_input("Description (optional)", placeholder="Brief notes")
    with col7:
        frequency = st.text_input("Frequency (optional)", placeholder="e.g. daily")

    submitted = st.form_submit_button("Add task")
    if submitted:  # #TOFIX: task dict was missing "pet_name", causing filter_by_pet to always fall back to the live input value
        st.session_state.tasks.append(
            {
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
                "category": category,
                "time": task_time,
                "description": description,
                "frequency": frequency,
                "completed": False,
                "pet_name": pet_name,  # #FIX: store pet_name so filter_by_pet works correctly
            }
        )

if st.session_state.tasks:
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_pet = st.text_input("Filter by pet name", placeholder="Leave blank for all")
    with filter_col2:
        filter_status = st.selectbox("Filter by status", ["All", "Incomplete", "Completed"])

    status_map = {"All": None, "Incomplete": False, "Completed": True}
    filtered = list(st.session_state.tasks)
    if filter_pet.strip():
        filtered = [t for t in filtered if t.get("pet_name", pet_name).lower() == filter_pet.strip().lower()]  # #FIX: pet_name now stored in task dict so this lookup is correct
    if filter_status != "All":
        filtered = [t for t in filtered if t.get("completed", False) == status_map[filter_status]]

    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None

    st.write(f"**{len(filtered)} of {len(st.session_state.tasks)} task(s) shown:**")
    if filtered:
        for task_dict in filtered:
            original_index = st.session_state.tasks.index(task_dict)
            with st.expander(f"{task_dict['title']} — {task_dict['duration_minutes']} min | {task_dict['priority']} | {task_dict['category']}"):
                st.write(f"Time: {task_dict['time'] or '—'}  |  Freq: {task_dict['frequency'] or '—'}  |  {'✅ Done' if task_dict['completed'] else '⬜ Pending'}")
                if task_dict['description']:
                    st.caption(task_dict['description'])
                if st.button("Edit", key=f"edit_{original_index}"):
                    st.session_state.editing_index = original_index
                    st.rerun()
    else:
        st.info("No tasks match your filters.")

    if st.session_state.editing_index is not None:
        idx = st.session_state.editing_index
        t = st.session_state.tasks[idx]
        st.markdown(f"#### Editing: {t['title']}")
        with st.form("edit_task_form"):
            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                e_title = st.text_input("Task title", value=t["title"])
            with e_col2:
                e_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=t["duration_minutes"])
            with e_col3:
                priority_opts = ["low", "medium", "high"]
                e_priority = st.selectbox("Priority", priority_opts, index=priority_opts.index(t["priority"]))
            e_col4, e_col5 = st.columns(2)
            with e_col4:
                cat_opts = ["exercise", "feeding", "grooming", "medical", "play", "training", "general"]
                e_category = st.selectbox("Category", cat_opts, index=cat_opts.index(t["category"]) if t["category"] in cat_opts else 0)
            with e_col5:
                e_time = st.text_input("Preferred time (optional)", value=t["time"])
            e_col6, e_col7 = st.columns(2)
            with e_col6:
                e_description = st.text_input("Description (optional)", value=t["description"])
            with e_col7:
                e_frequency = st.text_input("Frequency (optional)", value=t["frequency"])
            save_col, cancel_col = st.columns(2)
            with save_col:
                save = st.form_submit_button("Save changes")
            with cancel_col:
                cancel = st.form_submit_button("Cancel")
        if save:
            st.session_state.tasks[idx] = {
                "title": e_title,
                "duration_minutes": int(e_duration),
                "priority": e_priority,
                "category": e_category,
                "time": e_time,
                "description": e_description,
                "frequency": e_frequency,
                "completed": t["completed"],
                "pet_name": t["pet_name"],
            }
            st.session_state.editing_index = None
            st.session_state.pop("schedule", None)
            st.rerun()
        if cancel:
            st.session_state.editing_index = None
            st.rerun()

    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.session_state.pop("schedule", None)
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Schedule generation ──────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet = Pet(pet_name, species, int(pet_age))
        task_objects = [
            Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                category=t["category"],
                pet=pet,
                description=t.get("description", ""),
                time=t.get("time", ""),
                frequency=t.get("frequency", ""),
            )
            for t in st.session_state.tasks
        ]
        owner = Owner(owner_name, int(available_minutes), pet=pet, tasks=task_objects)
        scheduler = Scheduler(owner)
        st.session_state.schedule = scheduler.generate_schedule()
        st.session_state.scheduler = scheduler
        st.session_state.owner = owner
        st.session_state.pet = pet

if "schedule" in st.session_state:
    schedule: Schedule = st.session_state.schedule
    scheduler: Scheduler = st.session_state.scheduler
    owner = st.session_state.owner
    pet = st.session_state.pet

    st.success(
        f"Schedule for **{owner.name}** & **{pet.name}** "
        f"({pet.species}, age {pet.age}) — "
        f"{schedule.total_duration} of {owner.available_minutes} min used"
    )

    if schedule.scheduled_tasks:
        st.markdown("#### Scheduled tasks")
        for i, task in enumerate(schedule.scheduled_tasks):
            col_label, col_btn = st.columns([5, 1])
            with col_label:
                status_icon = "✅" if task.completed else "⬜"
                label = f"{status_icon} **{task.title}** — {task.duration_minutes} min | {task.priority} | {task.category}"
                if task.time:
                    label += f" | {task.time}"
                if task.frequency:
                    label += f" | 🔁 {task.frequency}"
                if task.description:
                    label += f"  \n_{task.description}_"
                st.markdown(label)
            with col_btn:
                if not task.completed and st.button("Done", key=f"done_{i}"):
                        scheduler.mark_complete(task)
                        # Sync Task objects back to session_state.tasks dicts
                        st.session_state.tasks = [
                            {
                                "title": t.title,
                                "duration_minutes": t.duration_minutes,
                                "priority": t.priority,
                                "category": t.category,
                                "time": t.time,
                                "description": t.description,
                                "frequency": t.frequency,
                                "completed": t.completed,
                                "pet_name": t.pet.name if t.pet else pet.name,
                            }
                            for t in scheduler.owner.tasks
                        ]
                        st.session_state.pop("schedule", None)
                        st.rerun()

    if schedule.skipped_tasks:
        st.markdown("#### Skipped (not enough time)")
        for task in schedule.skipped_tasks:
            st.markdown(
                f"- ~~{task.title}~~ — {task.duration_minutes} min needed, {task.priority} priority"
            )

    st.markdown("#### Conflict Check")
    if schedule.conflicts:
        st.warning(f"{len(schedule.conflicts)} conflict(s) detected among scheduled tasks.")
        for task_a, task_b in schedule.conflicts:
            st.markdown(
                f"- **{task_a.title}** ({task_a.time}, {task_a.duration_minutes} min) "
                f"overlaps with **{task_b.title}** ({task_b.time}, {task_b.duration_minutes} min)"
            )
    else:
        st.info("No scheduling conflicts detected.")
