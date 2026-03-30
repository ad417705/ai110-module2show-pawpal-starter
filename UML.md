# PawPal+ — System Design

## Class Diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +int available_minutes
        +Pet pet
        +list~Task~ tasks
    }

    class Pet {
        +str name
        +str species
        +int age
    }

    class Task {
        +str title
        +int duration_minutes
        +str priority
        +str category
        +Pet pet
        +str description
        +str time
        +str frequency
        +bool completed
        +priority_score() int
        +mark_complete() None
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +list~Task~ tasks
        +filter_by_pet(pet_name str) list~Task~
        +filter_by_status(completed bool) list~Task~
        +add_task(task Task) None
        +edit_task(task_index int, updated_task Task) None
        +mark_complete(task Task) None
        +generate_schedule() Schedule
    }

    class Schedule {
        +list~Task~ scheduled_tasks
        +list~Task~ skipped_tasks
        +list conflicts
        +int total_duration
        +explain() str
    }

    Owner "1" --> "1" Pet : owns
    Owner "1" --> "0..*" Task : has
    Task "0..*" --> "0..1" Pet : for
    Scheduler --> Owner : uses
    Scheduler --> Schedule : produces
    Schedule --> "0..*" Task : contains
```
