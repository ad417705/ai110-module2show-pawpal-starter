# PawPal+ Project Reflection

## 1. System Design

Core features:

- Adding pets
- Add/Editing task
- Generate daily schedule/plans

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

--- a. So the classes I chose are Pet, Owner, Task, Schedule, and Scheduler. The first 4 are mainly data containers and scheduler is a regular class that which uses and owns other objects. It's pretty intuitive in terms of what owns, uses, produces, etc... what, for example, owner owns pet.

--- b. The design did change during implementation. Initially, the Scheduler held the task list directly, but it made more sense for Owner to own the tasks since they belong to the owner's day — not the scheduler. So tasks moved to Owner, and the Scheduler just references owner.tasks. Task also grew a few fields (description, time, frequency, completed, pet) that weren't in the original UML once I realized the UI needed them.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

--- a. The scheduler considers two constraints: available time (owner.available_minutes) and task priority (high / medium / low). Within the same priority tier, tasks are also sorted by preferred start time so earlier tasks are scheduled first. Priority came first because a missed high-priority task (medication, feeding) is more costly than a missed low-priority one. Time-of-day is a secondary sort — useful but not a hard constraint.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

--- b. The scheduler uses a greedy first-fit approach: it works through tasks in priority + time order and adds each one if it fits in the remaining time. A task that is too long gets skipped entirely rather than partially done or swapped for a shorter one. This means a single long high-priority task can leave a lot of time unused even if several shorter lower-priority tasks could fill it. That tradeoff is reasonable here because partial pet-care tasks (a half-walk, half-dose of medication) don't make sense — the task either happens fully or not at all.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

--- a. AI was most useful for debugging and fleshing out logic I had a rough plan for. For example, I described the conflict-detection requirement and asked for help implementing an efficient sweep-line approach. I also used it to help fix a bug where filter_by_pet wasn't working correctly because tasks weren't storing pet_name at creation time. The most helpful prompts were specific ones that included the existing code and described exactly what was broken or what behavior I wanted — vague prompts gave vague answers.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

--- b. When AI first suggested the conflict detection implementation, it used a plain list as the active set instead of a heap, which would have been O(n²) in the worst case. I questioned it and asked for a more efficient approach, which led to the heapq-based sweep-line solution. I verified it by tracing through a few manual examples (two overlapping tasks, two non-overlapping, same start time) before writing the tests that confirmed the behavior.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

--- a. Tests covered: task completion status toggling, adding a task to the scheduler, time string parsing (valid AM/PM, 24h, blank, and unrecognized formats), schedule sorting by priority and then by time within a tier, pet and status filtering, conflict detection (overlapping, non-overlapping, untimed, same start), and daily recurrence creating a new task copy. These were important because they cover the core correctness guarantees — if sorting, filtering, or conflict detection is wrong, the schedule output is wrong regardless of how the UI looks.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

--- b. Fairly confident for the happy-path cases. The tests cover the main scenarios and they all pass. Edge cases I'd test next: owner's who purposely have scheduled two things at the same time, wouldn't really be considered a conflict, so testing that feature.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

--- a. The conflict detection came out cleaner than expected. The sweep-line algorithm with a min-heap keeps it at O(n log n) rather than the naive O(n²) pairwise check, and the logic ended up being readable. The tests for it are also precise — they check the exact pair, not just the count.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

--- b. I'd improve the UI, more specifically when creating the owner it would be more of a hub vs a type in your name, so more personalized. I would also use dropdowns for time instead of manually entering time because it can lead to complications.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

--- c. Lol, it is important to start on time!!! but I think I learned a lot about UML design, git, and taking ownership of a project, takes a lot.
