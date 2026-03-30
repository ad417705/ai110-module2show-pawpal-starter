# PawPal+

**PawPal+** is a Streamlit app that helps a pet owner plan and track daily care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The following features were added to make the scheduler more capable and the UI more useful:

### Priority + time-aware sorting
Tasks are sorted by priority score (high → medium → low) first, then by their preferred start time within the same priority tier. Tasks without a time are treated as last in the order.

### Filter by pet and status
The task list can be filtered by pet name (case-insensitive, stored per-task so it survives owner name edits) and by completion status (All / Incomplete / Completed).

### Recurring task support
Each task has an optional `frequency` field (e.g. `daily`, `weekly`). When a `daily` task is marked complete, a fresh copy is automatically appended for the next occurrence.

### Conflict detection
After building the schedule, the app runs a sweep-line algorithm over all scheduled tasks that have a start time. Any pair whose time windows overlap is reported in a "Conflict Check" section, showing both task names and their times.

### Inline task editing
Each task in the list has an Edit button that opens an inline form pre-populated with the task's current values. Saving updates the task in place and clears the cached schedule so the next run reflects the change.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run tests

```bash
pytest
```
