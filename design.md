# PawPal+ — System Design

## Class Diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +int available_minutes
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
        +priority_score() int
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +list~Task~ tasks
        +generate_schedule() Schedule
    }

    class Schedule {
        +list~Task~ scheduled_tasks
        +list~Task~ skipped_tasks
        +int total_duration
        +explain() str
    }

    Owner "1" --> "1" Pet : owns
    Scheduler --> Owner : uses
    Scheduler --> Pet : uses
    Scheduler --> "0..*" Task : takes in
    Scheduler --> Schedule : produces
    Schedule --> "0..*" Task : contains
```
