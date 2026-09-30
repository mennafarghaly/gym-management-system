from abc import ABC, abstractmethod
from datetime import date


class Person(ABC):
    def __init__(self, id: str, name: str, email: str, phone: str) -> None:
        self.__id = id
        self.__name = name
        self.__email = email
        self.__phone = phone

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def phone(self):
        return self.__phone

    @abstractmethod
    def get_role(self):
        pass


class Member(Person):
    def __init__(self, id: str, name: str, email: str, phone: str, join_date: str, trainer_id: str = None) -> None:
        super().__init__(id, name, email, phone)
        self.__join_date = join_date
        self.__trainer_id = trainer_id

    @property
    def join_date(self):
        return self.__join_date

    @property
    def trainer_id(self):
        return self.__trainer_id

    def assign_trainer(self, trainer_id: str) -> None:
        self.__trainer_id = trainer_id

    def get_role(self):
        return "Member"


class Trainer(Person):
    def __init__(self, id: str, name: str, email: str, phone: str, specialization: str) -> None:
        super().__init__(id, name, email, phone)
        self.__specialization = specialization

    @property
    def specialization(self):
        return self.__specialization

    def get_role(self):
        return "Trainer"


class Membership:
    def __init__(self, membership_id: str, member_id: str, plan_type: str, start_date: str, end_date: str) -> None:
        try:
            start = date.fromisoformat(str(start_date))
            end = date.fromisoformat(str(end_date))
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format, for example 2026-09-03")

        if end < start:
            raise ValueError("End date cannot be before start date")

        self.__membership_id = membership_id
        self.__member_id = member_id
        self.__plan_type = plan_type
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def membership_id(self):
        return self.__membership_id

    @property
    def member_id(self):
        return self.__member_id

    @property
    def plan_type(self):
        return self.__plan_type

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    def is_active(self) -> bool:
        today = date.today()
        end = self.__end_date
        if isinstance(end, str):
            end = date.fromisoformat(end)
        if end < today:
            return False
        else:
            return True


class Payment:
    def __init__(self, payment_id: str, member_id: str, amount: float, payment_date: str) -> None:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        self.__payment_id = payment_id
        self.__member_id = member_id
        self.__amount = amount
        self.__payment_date = payment_date

    @property
    def payment_id(self):
        return self.__payment_id

    @property
    def member_id(self):
        return self.__member_id

    @property
    def amount(self):
        return self.__amount

    @property
    def payment_date(self):
        return self.__payment_date


class Attendance:
    def __init__(self, attendance_id: str, member_id: str, date: str) -> None:
        self.__attendance_id = attendance_id
        self.__member_id = member_id
        self.__date = date

    @property
    def attendance_id(self):
        return self.__attendance_id

    @property
    def member_id(self):
        return self.__member_id

    @property
    def date(self):
        return self.__date


class Gym:
    def __init__(self, gym_name: str) -> None:
        self.__gym_name = gym_name
        self.__members = []
        self.__trainers = []
        self.__memberships = []
        self.__payments = []
        self.__attendances = []

    @property
    def gym_name(self):
        return self.__gym_name

    @property
    def members(self):
        return self.__members

    @property
    def trainers(self):
        return self.__trainers

    @property
    def memberships(self):
        return self.__memberships

    @property
    def payments(self):
        return self.__payments

    @property
    def attendances(self):
        return self.__attendances

    def add_member(self, member):
        self.__members.append(member)

    def add_trainer(self, trainer):
        self.__trainers.append(trainer)

    def find_member(self, member_id):
        for m in self.__members:
            if str(m.id) == str(member_id):
                return m
        return None

    def find_trainer(self, trainer_id):
        for t in self.__trainers:
            if str(t.id) == str(trainer_id):
                return t
        return None

    def search_members(self, keyword):
        keyword = keyword.lower()
        results = []
        for m in self.__members:
            if keyword in m.name.lower() or keyword in str(m.id).lower():
                results.append(m)
        return results

    def update_member(self, member_id, name, email, phone, join_date):
        for i in range(len(self.__members)):
            if str(self.__members[i].id) == str(member_id):
                self.__members[i] = Member(member_id, name, email, phone, join_date)
                return
        raise ValueError(f"Member {member_id} does not exist")

    def delete_member(self, member_id):
        member = self.find_member(member_id)
        if member is None:
            raise ValueError(f"Member {member_id} does not exist")
        for mb in self.__memberships:
            if str(mb.member_id) == str(member_id) and mb.is_active():
                raise ValueError("Cannot delete a member with an active membership")
        self.__members.remove(member)

    def assign_trainer(self, member_id: str, trainer_id: str) -> None:
        member = self.find_member(member_id)
        if member is None:
            raise ValueError(f"Member {member_id} does not exist")

        trainer = self.find_trainer(trainer_id)
        if trainer is None:
            raise ValueError(f"Trainer {trainer_id} does not exist")

        member.assign_trainer(trainer_id)

    def create_membership(self, membership_id, member_id, plan_type, start_date, end_date):
        for membership in self.__memberships:
            if membership.member_id == member_id and membership.is_active():
                raise ValueError(f"Member {member_id} already has an active membership")
        new_membership = Membership(membership_id, member_id, plan_type, start_date, end_date)
        self.__memberships.append(new_membership)
        return new_membership

    def record_payment(self, payment_id, member_id, amount, payment_date):
        new_payment = Payment(payment_id, member_id, amount, payment_date)
        self.__payments.append(new_payment)
        return new_payment

    def record_attendance(self, attendance_id, member_id, date):
        member_exists = False
        for member in self.__members:
            if member.id == member_id:
                member_exists = True
                break
        if not member_exists:
            raise ValueError(f"Member {member_id} does not exist")

        has_active_membership = False
        for membership in self.__memberships:
            if membership.member_id == member_id and membership.is_active():
                has_active_membership = True
                break
        if not has_active_membership:
            raise ValueError(f"Member {member_id} has no active membership")

        new_attendance = Attendance(attendance_id, member_id, date)
        self.__attendances.append(new_attendance)
        return new_attendance

    def get_active_memberships(self):
        return [mb for mb in self.__memberships if mb.is_active()]

    def get_expired_memberships(self):
        return [mb for mb in self.__memberships if not mb.is_active()]