import tkinter as tk
from tkinter import ttk, messagebox
from models import Gym, Member, Trainer
from file_manager import FileManager

file_manager = FileManager("gym_data.json")
gym = file_manager.load_gym()

root = tk.Tk()
root.title("Gym Management System")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

dashboard_tab = ttk.Frame(notebook)
members_tab = ttk.Frame(notebook)
trainers_tab = ttk.Frame(notebook)
memberships_tab = ttk.Frame(notebook)
payments_tab = ttk.Frame(notebook)
attendance_tab = ttk.Frame(notebook)

notebook.add(dashboard_tab, text="Dashboard")
notebook.add(members_tab, text="Members")
notebook.add(trainers_tab, text="Trainers")
notebook.add(memberships_tab, text="Memberships")
notebook.add(payments_tab, text="Payments")
notebook.add(attendance_tab, text="Attendance")


# ================= MEMBERS TAB =================

form = tk.Frame(members_tab)
form.pack(pady=10)

tk.Label(form, text="ID").grid(row=0, column=0)
tk.Label(form, text="Name").grid(row=0, column=1)
tk.Label(form, text="Email").grid(row=0, column=2)
tk.Label(form, text="Phone").grid(row=0, column=3)
tk.Label(form, text="Join Date (YYYY-MM-DD)").grid(row=0, column=4)

m_id = tk.Entry(form, width=10)
m_name = tk.Entry(form, width=15)
m_email = tk.Entry(form, width=15)
m_phone = tk.Entry(form, width=12)
m_join = tk.Entry(form, width=18)

m_id.grid(row=1, column=0)
m_name.grid(row=1, column=1)
m_email.grid(row=1, column=2)
m_phone.grid(row=1, column=3)
m_join.grid(row=1, column=4)

columns = ("ID", "Name", "Email", "Phone", "Join Date")
members_table = ttk.Treeview(members_tab, columns=columns, show="headings", height=12)
for col in columns:
    members_table.heading(col, text=col)


def refresh_members_table():
    for row in members_table.get_children():
        members_table.delete(row)
    for m in gym.members:
        members_table.insert("", "end", values=(m.id, m.name, m.email, m.phone, m.join_date))


def add_member_clicked():
    member_id = m_id.get().strip()
    name = m_name.get().strip()
    email = m_email.get().strip()
    phone = m_phone.get().strip()
    join_date = m_join.get().strip()

    if member_id == "" or name == "":
        messagebox.showerror("Error", "ID and Name are required")
        return

    for m in gym.members:
        if str(m.id) == member_id:
            messagebox.showerror("Error", "A member with this ID already exists")
            return

    member = Member(member_id, name, email, phone, join_date)
    gym.add_member(member)
    refresh_members_table()
    messagebox.showinfo("Success", "Member added successfully")

    m_id.delete(0, tk.END)
    m_name.delete(0, tk.END)
    m_email.delete(0, tk.END)
    m_phone.delete(0, tk.END)
    m_join.delete(0, tk.END)


tk.Button(form, text="Add Member", command=add_member_clicked).grid(row=1, column=5, padx=10)


# ---------- Members: Search / Update / Delete / Assign Trainer ----------

def clear_member_form():
    m_id.delete(0, tk.END)
    m_name.delete(0, tk.END)
    m_email.delete(0, tk.END)
    m_phone.delete(0, tk.END)
    m_join.delete(0, tk.END)


def on_member_select(event):
    selected = members_table.selection()
    if not selected:
        return
    member_id = members_table.item(selected[0])["values"][0]
    member = gym.find_member(member_id)
    if member is None:
        return
    clear_member_form()
    m_id.insert(0, member.id)
    m_name.insert(0, member.name)
    m_email.insert(0, member.email)
    m_phone.insert(0, member.phone)
    m_join.insert(0, member.join_date)


members_table.bind("<<TreeviewSelect>>", on_member_select)


def update_member_clicked():
    member_id = m_id.get().strip()
    name = m_name.get().strip()

    if member_id == "" or name == "":
        messagebox.showerror("Error", "Select a member from the table first")
        return

    try:
        gym.update_member(member_id, name, m_email.get().strip(),
                          m_phone.get().strip(), m_join.get().strip())
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    refresh_members_table()
    clear_member_form()
    messagebox.showinfo("Success", "Member updated successfully")


def delete_member_clicked():
    member_id = m_id.get().strip()

    if member_id == "":
        messagebox.showerror("Error", "Select a member from the table first")
        return

    if not messagebox.askyesno("Confirm", f"Delete member {member_id}?"):
        return

    try:
        gym.delete_member(member_id)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    refresh_members_table()
    clear_member_form()
    messagebox.showinfo("Success", "Member deleted successfully")


def search_members_clicked():
    results = gym.search_members(member_search.get().strip())
    for row in members_table.get_children():
        members_table.delete(row)
    for m in results:
        members_table.insert("", "end", values=(m.id, m.name, m.email, m.phone, m.join_date))


btn_frame = tk.Frame(members_tab)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Update Selected", command=update_member_clicked).pack(side="left", padx=5)
tk.Button(btn_frame, text="Delete Selected", command=delete_member_clicked).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear Form", command=clear_member_form).pack(side="left", padx=5)

tk.Label(btn_frame, text="  Trainer ID:").pack(side="left", padx=(15, 0))
trainer_id_entry = tk.Entry(btn_frame, width=10)
trainer_id_entry.pack(side="left", padx=5)


def assign_trainer_clicked():
    member_id = m_id.get().strip()
    trainer_id = trainer_id_entry.get().strip()

    if member_id == "" or trainer_id == "":
        messagebox.showerror("Error", "Select a member and enter a Trainer ID")
        return

    try:
        gym.assign_trainer(member_id, trainer_id)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    messagebox.showinfo("Success", f"Trainer {trainer_id} assigned to member {member_id}")
    trainer_id_entry.delete(0, tk.END)


tk.Button(btn_frame, text="Assign Trainer", command=assign_trainer_clicked).pack(side="left", padx=5)

search_frame = tk.Frame(members_tab)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search (name or ID):").pack(side="left")
member_search = tk.Entry(search_frame, width=20)
member_search.pack(side="left", padx=5)
tk.Button(search_frame, text="Search", command=search_members_clicked).pack(side="left")
tk.Button(search_frame, text="Show All", command=refresh_members_table).pack(side="left", padx=5)

members_table.pack(fill="both", expand=True, padx=10, pady=10)


# ================= TRAINERS TAB =================

t_form = tk.Frame(trainers_tab)
t_form.pack(pady=10)

tk.Label(t_form, text="ID").grid(row=0, column=0)
tk.Label(t_form, text="Name").grid(row=0, column=1)
tk.Label(t_form, text="Email").grid(row=0, column=2)
tk.Label(t_form, text="Phone").grid(row=0, column=3)
tk.Label(t_form, text="Specialization").grid(row=0, column=4)

t_id = tk.Entry(t_form, width=10)
t_name = tk.Entry(t_form, width=15)
t_email = tk.Entry(t_form, width=15)
t_phone = tk.Entry(t_form, width=12)
t_spec = tk.Entry(t_form, width=18)

t_id.grid(row=1, column=0)
t_name.grid(row=1, column=1)
t_email.grid(row=1, column=2)
t_phone.grid(row=1, column=3)
t_spec.grid(row=1, column=4)

t_columns = ("ID", "Name", "Email", "Phone", "Specialization")
trainers_table = ttk.Treeview(trainers_tab, columns=t_columns, show="headings", height=12)
for col in t_columns:
    trainers_table.heading(col, text=col)
trainers_table.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_trainers_table():
    for row in trainers_table.get_children():
        trainers_table.delete(row)
    for t in gym.trainers:
        trainers_table.insert("", "end", values=(t.id, t.name, t.email, t.phone, t.specialization))


def add_trainer_clicked():
    trainer_id = t_id.get().strip()
    name = t_name.get().strip()
    email = t_email.get().strip()
    phone = t_phone.get().strip()
    spec = t_spec.get().strip()

    if trainer_id == "" or name == "":
        messagebox.showerror("Error", "ID and Name are required")
        return

    for t in gym.trainers:
        if str(t.id) == trainer_id:
            messagebox.showerror("Error", "A trainer with this ID already exists")
            return

    trainer = Trainer(trainer_id, name, email, phone, spec)
    gym.add_trainer(trainer)
    refresh_trainers_table()
    messagebox.showinfo("Success", "Trainer added successfully")

    t_id.delete(0, tk.END)
    t_name.delete(0, tk.END)
    t_email.delete(0, tk.END)
    t_phone.delete(0, tk.END)
    t_spec.delete(0, tk.END)


tk.Button(t_form, text="Add Trainer", command=add_trainer_clicked).grid(row=1, column=5, padx=10)


# ================= MEMBERSHIPS TAB =================

mb_form = tk.Frame(memberships_tab)
mb_form.pack(pady=10)

tk.Label(mb_form, text="Membership ID").grid(row=0, column=0)
tk.Label(mb_form, text="Member ID").grid(row=0, column=1)
tk.Label(mb_form, text="Plan Type").grid(row=0, column=2)
tk.Label(mb_form, text="Start (YYYY-MM-DD)").grid(row=0, column=3)
tk.Label(mb_form, text="End (YYYY-MM-DD)").grid(row=0, column=4)

mb_id = tk.Entry(mb_form, width=12)
mb_member_id = tk.Entry(mb_form, width=10)
mb_plan = tk.Entry(mb_form, width=12)
mb_start = tk.Entry(mb_form, width=16)
mb_end = tk.Entry(mb_form, width=16)

mb_id.grid(row=1, column=0)
mb_member_id.grid(row=1, column=1)
mb_plan.grid(row=1, column=2)
mb_start.grid(row=1, column=3)
mb_end.grid(row=1, column=4)

mb_columns = ("Membership ID", "Member ID", "Plan", "Start", "End", "Status")
memberships_table = ttk.Treeview(memberships_tab, columns=mb_columns, show="headings", height=12)
for col in mb_columns:
    memberships_table.heading(col, text=col)


def refresh_memberships_table(filter_type="all"):
    for row in memberships_table.get_children():
        memberships_table.delete(row)
    for mb in gym.memberships:
        if filter_type == "active" and not mb.is_active():
            continue
        if filter_type == "expired" and mb.is_active():
            continue
        status = "Active" if mb.is_active() else "Expired"
        memberships_table.insert("", "end", values=(mb.membership_id, mb.member_id, mb.plan_type, mb.start_date, mb.end_date, status))


def add_membership_clicked():
    membership_id = mb_id.get().strip()
    member_id = mb_member_id.get().strip()
    plan = mb_plan.get().strip()
    start = mb_start.get().strip()
    end = mb_end.get().strip()

    if membership_id == "" or member_id == "" or plan == "" or start == "" or end == "":
        messagebox.showerror("Error", "All fields are required")
        return

    member_exists = False
    for m in gym.members:
        if str(m.id) == member_id:
            member_exists = True
    if not member_exists:
        messagebox.showerror("Error", "This member does not exist")
        return

    try:
        gym.create_membership(membership_id, member_id, plan, start, end)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    refresh_memberships_table()
    messagebox.showinfo("Success", "Membership created successfully")

    mb_id.delete(0, tk.END)
    mb_member_id.delete(0, tk.END)
    mb_plan.delete(0, tk.END)
    mb_start.delete(0, tk.END)
    mb_end.delete(0, tk.END)


tk.Button(mb_form, text="Create Membership", command=add_membership_clicked).grid(row=1, column=5, padx=10)

filter_frame = tk.Frame(memberships_tab)
filter_frame.pack(pady=5)
tk.Button(filter_frame, text="Show All", command=lambda: refresh_memberships_table("all")).pack(side="left", padx=5)
tk.Button(filter_frame, text="Active Only", command=lambda: refresh_memberships_table("active")).pack(side="left", padx=5)
tk.Button(filter_frame, text="Expired Only", command=lambda: refresh_memberships_table("expired")).pack(side="left", padx=5)

memberships_table.pack(fill="both", expand=True, padx=10, pady=10)


# ================= PAYMENTS TAB =================

p_form = tk.Frame(payments_tab)
p_form.pack(pady=10)

tk.Label(p_form, text="Payment ID").grid(row=0, column=0)
tk.Label(p_form, text="Member ID").grid(row=0, column=1)
tk.Label(p_form, text="Amount").grid(row=0, column=2)
tk.Label(p_form, text="Date (YYYY-MM-DD)").grid(row=0, column=3)

p_id = tk.Entry(p_form, width=12)
p_member_id = tk.Entry(p_form, width=10)
p_amount = tk.Entry(p_form, width=10)
p_date = tk.Entry(p_form, width=16)

p_id.grid(row=1, column=0)
p_member_id.grid(row=1, column=1)
p_amount.grid(row=1, column=2)
p_date.grid(row=1, column=3)

p_columns = ("Payment ID", "Member ID", "Amount", "Date")
payments_table = ttk.Treeview(payments_tab, columns=p_columns, show="headings", height=12)
for col in p_columns:
    payments_table.heading(col, text=col)
payments_table.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_payments_table():
    for row in payments_table.get_children():
        payments_table.delete(row)
    for p in gym.payments:
        payments_table.insert("", "end", values=(p.payment_id, p.member_id, p.amount, p.payment_date))


def add_payment_clicked():
    payment_id = p_id.get().strip()
    member_id = p_member_id.get().strip()
    amount_text = p_amount.get().strip()
    pdate = p_date.get().strip()

    if payment_id == "" or member_id == "" or amount_text == "" or pdate == "":
        messagebox.showerror("Error", "All fields are required")
        return

    member_exists = False
    for m in gym.members:
        if str(m.id) == member_id:
            member_exists = True
    if not member_exists:
        messagebox.showerror("Error", "This member does not exist")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    try:
        gym.record_payment(payment_id, member_id, amount, pdate)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    refresh_payments_table()
    messagebox.showinfo("Success", "Payment recorded successfully")

    p_id.delete(0, tk.END)
    p_member_id.delete(0, tk.END)
    p_amount.delete(0, tk.END)
    p_date.delete(0, tk.END)


tk.Button(p_form, text="Record Payment", command=add_payment_clicked).grid(row=1, column=4, padx=10)


# ================= ATTENDANCE TAB =================

a_form = tk.Frame(attendance_tab)
a_form.pack(pady=10)

tk.Label(a_form, text="Attendance ID").grid(row=0, column=0)
tk.Label(a_form, text="Member ID").grid(row=0, column=1)
tk.Label(a_form, text="Date (YYYY-MM-DD)").grid(row=0, column=2)

a_id = tk.Entry(a_form, width=12)
a_member_id = tk.Entry(a_form, width=10)
a_date = tk.Entry(a_form, width=16)

a_id.grid(row=1, column=0)
a_member_id.grid(row=1, column=1)
a_date.grid(row=1, column=2)

a_columns = ("Attendance ID", "Member ID", "Date")
attendance_table = ttk.Treeview(attendance_tab, columns=a_columns, show="headings", height=12)
for col in a_columns:
    attendance_table.heading(col, text=col)
attendance_table.pack(fill="both", expand=True, padx=10, pady=10)


def refresh_attendance_table():
    for row in attendance_table.get_children():
        attendance_table.delete(row)
    for a in gym.attendances:
        attendance_table.insert("", "end", values=(a.attendance_id, a.member_id, a.date))


def add_attendance_clicked():
    attendance_id = a_id.get().strip()
    member_id = a_member_id.get().strip()
    adate = a_date.get().strip()

    if attendance_id == "" or member_id == "" or adate == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        gym.record_attendance(attendance_id, member_id, adate)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    refresh_attendance_table()
    messagebox.showinfo("Success", "Attendance recorded successfully")

    a_id.delete(0, tk.END)
    a_member_id.delete(0, tk.END)
    a_date.delete(0, tk.END)


tk.Button(a_form, text="Record Attendance", command=add_attendance_clicked).grid(row=1, column=3, padx=10)


# ================= DASHBOARD TAB =================

tk.Label(dashboard_tab, text="Gym Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

lbl_members = tk.Label(dashboard_tab, font=("Arial", 13))
lbl_trainers = tk.Label(dashboard_tab, font=("Arial", 13))
lbl_active = tk.Label(dashboard_tab, font=("Arial", 13))
lbl_expired = tk.Label(dashboard_tab, font=("Arial", 13))
lbl_payments = tk.Label(dashboard_tab, font=("Arial", 13))
lbl_attendance = tk.Label(dashboard_tab, font=("Arial", 13))

for lbl in (lbl_members, lbl_trainers, lbl_active, lbl_expired, lbl_payments, lbl_attendance):
    lbl.pack(pady=5)


def refresh_dashboard():
    active_count = 0
    expired_count = 0
    for mb in gym.memberships:
        if mb.is_active():
            active_count += 1
        else:
            expired_count += 1

    total_paid = 0
    for p in gym.payments:
        total_paid += p.amount

    lbl_members.config(text=f"Total Members: {len(gym.members)}")
    lbl_trainers.config(text=f"Total Trainers: {len(gym.trainers)}")
    lbl_active.config(text=f"Active Memberships: {active_count}")
    lbl_expired.config(text=f"Expired Memberships: {expired_count}")
    lbl_payments.config(text=f"Total Payments Collected: {total_paid}")
    lbl_attendance.config(text=f"Total Attendance Records: {len(gym.attendances)}")


notebook.bind("<<NotebookTabChanged>>", lambda e: refresh_dashboard())
refresh_dashboard()


# ================= STARTUP + SAVE ON CLOSE =================

refresh_members_table()
refresh_trainers_table()
refresh_memberships_table()
refresh_payments_table()
refresh_attendance_table()


def on_close():
    file_manager.save_data(gym)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()