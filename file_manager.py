import json
from models import Gym, Member, Trainer, Membership, Payment, Attendance


class FileManager:
    def __init__(self, filename: str = "gym_data.json") -> None:
        self.__filename = filename

    def save_data(self, gym):
        data = {
            "members": [],
            "trainers": [],
            "memberships": [],
            "payments": [],
            "attendances": []
        }

        for m in gym.members:
            data["members"].append({
                "id": m.id, "name": m.name, "email": m.email,
                "phone": m.phone, "join_date": str(m.join_date)
            })

        for t in gym.trainers:
            data["trainers"].append({
                "id": t.id, "name": t.name, "email": t.email,
                "phone": t.phone, "specialization": t.specialization
            })

        for mb in gym.memberships:
            data["memberships"].append({
                "membership_id": mb.membership_id, "member_id": mb.member_id,
                "plan_type": mb.plan_type, "start_date": str(mb.start_date),
                "end_date": str(mb.end_date)
            })

        for p in gym.payments:
            data["payments"].append({
                "payment_id": p.payment_id, "member_id": p.member_id,
                "amount": p.amount, "payment_date": str(p.payment_date)
            })

        for a in gym.attendances:
            data["attendances"].append({
                "attendance_id": a.attendance_id, "member_id": a.member_id,
                "date": str(a.date)
            })

        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_gym(self):
        gym = Gym("My Gym")

        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return gym
        except ValueError:
            return gym

        for m in data["members"]:
            gym.add_member(Member(m["id"], m["name"], m["email"], m["phone"], m["join_date"]))

        for t in data["trainers"]:
            gym.add_trainer(Trainer(t["id"], t["name"], t["email"], t["phone"], t["specialization"]))

        for mb in data["memberships"]:
            gym.memberships.append(Membership(
                mb["membership_id"], mb["member_id"], mb["plan_type"],
                mb["start_date"], mb["end_date"]
            ))

        for p in data["payments"]:
            gym.payments.append(Payment(p["payment_id"], p["member_id"], p["amount"], p["payment_date"]))

        for a in data["attendances"]:
            gym.attendances.append(Attendance(a["attendance_id"], a["member_id"], a["date"]))

        return gym