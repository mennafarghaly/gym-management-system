# Gym Management System

## Team Members
- [Menna Tallah Farghaly] (solo project)
 
## Project Description
A desktop application for managing a gym: members, trainers, memberships, payments and
attendance. It is built with Python and Object-Oriented Programming, stores its data in a
JSON file, and has a graphical interface built with Tkinter.

## Main Features
- Add, update, delete and search members
- Add trainers
- Create memberships (with active / expired status)
- Filter memberships: All / Active only / Expired only
- Record payments
- Record attendance
- Dashboard with live statistics calculated from the real data
- Automatic loading of data on startup and saving when the window is closed

## Classes
| Class | Responsibility |
|---|---|
| `Person` (abstract) | Base class holding the data shared by members and trainers: id, name, email, phone |
| `Member(Person)` | A gym member, adds `join_date` |
| `Trainer(Person)` | A trainer, adds `specialization` |
| `Membership` | A member's subscription: plan, start date, end date, `is_active()` |
| `Payment` | A payment made by a member (amount must be > 0) |
| `Attendance` | A single attendance record of a member |
| `Gym` | Main class: holds all objects and enforces the business rules |
| `FileManager` | Saves/loads all data to/from a JSON file (kept separate from business logic) |

## OOP Concepts Used
- **Classes & Objects / Constructors:** every entity has its own class with `__init__`.
- **Encapsulation:** all attributes are private (`__name`) and are read through `@property`.
- **Inheritance:** `Member` and `Trainer` inherit from `Person` and call `super().__init__()`.
- **Abstraction:** `Person` is an abstract base class (`ABC`) with the abstract method `get_role()`.
- **Polymorphism:** `get_role()` has the same interface but a different result in `Member` ("Member") and `Trainer` ("Trainer").
- **Composition:** `Gym` contains lists of `Member`, `Trainer`, `Membership`, `Payment` and `Attendance` objects.
- **Exception Handling:** the models raise `ValueError` for invalid data; the GUI catches it with `try/except` and shows a clear message. `FileManager` handles a missing or corrupted file.
- **File Handling:** JSON persistence through the `FileManager` class.

## Business Rules
1. A member cannot have two active memberships at the same time.
2. Payment amount must be greater than zero.
3. Attendance can only be recorded for an existing member with an active membership.
4. Membership dates must be in `YYYY-MM-DD` format and the end date cannot be before the start date.
5. A member with an active membership cannot be deleted.
6. Member ID must be unique.
7. Memberships and payments can only be created for an existing member.

## File Storage
Data is stored in `gym_data.json` (created automatically next to the program).
It is loaded when the application starts and saved when the window is closed with the X button.

## GUI Framework
Tkinter (included with Python, no installation needed). The window has six tabs:
Dashboard, Members, Trainers, Memberships, Payments, Attendance.

## How to Run
1. Install Python 3.8 or newer.
2. Put `gym_app.py`, `models.py` and `file_manager.py` in the same folder.
3. Open a terminal in that folder and run:
   ```
   python gym_app.py
   ```

## Project Structure
```
gym_project/
├── gym_app.py          # GUI (Tkinter) + program entry point
├── models.py           # OOP classes: Person, Member, Trainer, Membership, Payment, Attendance, Gym
├── file_manager.py     # FileManager (JSON save/load)
├── gym_data.json       # Data file (auto-created)
├── test_scenarios.txt  # Test scenarios
├── uml_diagram.mermaid # UML class diagram source
└── README.md
```

## Test Scenarios
12 documented scenarios (3 successful, 3 invalid input, 4 business-rule violations,
2 edge cases) are in `test_scenarios.txt`.

## Screenshots
Add your screenshots here, for example:
- Dashboard
- Members tab
- Memberships tab with the Active / Expired filter
- An error message caused by a business rule
