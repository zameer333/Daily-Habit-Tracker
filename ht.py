import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
import os

DATA_FILE = "habits.json"

ACTIVITIES = ["Exercise", "Meditation", "Designing", "Coding", "Exploring"]

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Habit Tracker")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#d4e7f3")

        self.activity_vars = {}
        self.data = self.load_data()

        self.create_ui()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return {activity: {} for activity in ACTIVITIES}

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    def create_ui(self):
        title_bar = tk.Frame(self.root, bg="#1b1b1b", height=70)
        title_bar.pack(fill="x")

        title_label = tk.Label(
            title_bar,
            text="Daily Habit Tracker",
            font=("Arial", 24, "bold"),
            fg="#00ffcc",
            bg="#1b1b1b",
        )
        title_label.pack(pady=10)

        # Activities Section
        activities_frame = tk.Frame(self.root, bg="#d4e7f3", padx=20, pady=20)
        activities_frame.pack(fill="both", expand=True)

        activities_title = tk.Label(
            activities_frame,
            text="Today's Activities",
            font=("Arial", 18, "bold"),
            fg="#000",
            bg="#d4e7f3",
        )
        activities_title.pack(anchor="w", pady=10)

        for activity in ACTIVITIES:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                activities_frame,
                text=f"  {activity}",
                font=("Arial", 14, "bold"),
                variable=var,
                onvalue=True,
                offvalue=False,
                fg="#000",
                bg="#d4e7f3",
                activebackground="#d4e7f3",
                activeforeground="#00aaff",
                selectcolor="#d4e7f3",
            )
            checkbox.pack(anchor="w", pady=5)
            self.activity_vars[activity] = var

        buttons_frame = tk.Frame(self.root, bg="#d4e7f3", pady=20)
        buttons_frame.pack()

        submit_btn = tk.Button(
            buttons_frame,
            text="Submit",
            font=("Arial", 14, "bold"),
            fg="#fff",
            bg="#1b1b1b",
            activebackground="#333333",
            activeforeground="#fff",
            padx=20,
            pady=10,
            command=self.submit_progress,
        )
        submit_btn.grid(row=0, column=0, padx=20)

        report_btn = tk.Button(
            buttons_frame,
            text="Check Weekly Report",
            font=("Arial", 14, "bold"),
            fg="#fff",
            bg="#1b1b1b",
            activebackground="#333333",
            activeforeground="#fff",
            padx=20,
            pady=10,
            command=self.view_report,
        )
        report_btn.grid(row=0, column=1, padx=20)

        date_history_btn = tk.Button(
            buttons_frame,
            text="View Specific Date History",
            font=("Arial", 14, "bold"),
            fg="#fff",
            bg="#1b1b1b",
            activebackground="#333333",
            activeforeground="#fff",
            padx=20,
            pady=10,
            command=self.view_date_history,
        )
        date_history_btn.grid(row=0, column=2, padx=20)

    def submit_progress(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for activity, var in self.activity_vars.items():
            if activity not in self.data:
                self.data[activity] = {}
            self.data[activity][today] = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": var.get(),
            }
        self.save_data()
        messagebox.showinfo("Success", "Today's progress has been saved!")

    def view_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Weekly Report")
        report_window.geometry("800x500")
        report_window.configure(bg="#d4e7f3")
        report_window.resizable(False, False)

        tk.Label(
            report_window,
            text="Weekly Report",
            font=("Arial", 20, "bold"),
            bg="#d4e7f3",
            fg="#1b1b1b",
        ).pack(pady=20)

        report_frame = tk.Frame(report_window, bg="#d4e7f3")
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)

        report_text = tk.Text(
            report_frame,
            wrap="word",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#000",
            padx=10,
            pady=10,
            relief="flat",
        )
        report_text.pack(expand=True, fill="both")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)

        report_text.insert(
            "1.0",
            f"Weekly Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})\n\n",
        )

        for activity, records in self.data.items():
            streak = 0
            weekly_count = 0

            for i in range(7):
                day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                if day in records and records[day]["status"]:
                    weekly_count += 1
                    streak += 1
                else:
                    streak = 0

            percentage = (weekly_count / 7) * 100
            report_text.insert("end", f"{activity}:\n")
            report_text.insert("end", f"  Weekly Completion: {weekly_count}/7 days ({percentage:.2f}%)\n")
            report_text.insert("end", f"  Current Streak: {streak} days\n\n")

        report_text.config(state="disabled")

    def view_date_history(self):
        date_window = tk.Toplevel(self.root)
        date_window.title("View Specific Date History")
        date_window.geometry("400x300")
        date_window.configure(bg="#d4e7f3")
        date_window.resizable(False, False)

        tk.Label(
            date_window,
            text="View Activity History by Date",
            font=("Arial", 16, "bold"),
            bg="#d4e7f3",
            fg="#1b1b1b",
        ).pack(pady=10)

        tk.Label(
            date_window,
            text="Enter Date (YYYY-MM-DD):",
            font=("Arial", 12),
            bg="#d4e7f3",
        ).pack(pady=5)

        date_entry = tk.Entry(date_window, font=("Arial", 12), width=15)
        date_entry.pack(pady=5)

        def fetch_history():
            selected_date = date_entry.get()
            if not selected_date:
                messagebox.showerror("Error", "Please enter a valid date!")
                return

            try:
                datetime.strptime(selected_date, "%Y-%m-%d")  # Validate date format
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
                return

            history_text.delete("1.0", tk.END)
            history_text.insert("1.0", f"Activity History for {selected_date}:\n\n")

            found_data = False
            for activity, records in self.data.items():
                if selected_date in records:
                    status = "Completed" if records[selected_date]["status"] else "Not Completed"
                    time = records[selected_date]["time"]
                    history_text.insert("end", f"{activity}:\n  Status: {status}\n  Time: {time}\n\n")
                    found_data = True

            if not found_data:
                history_text.insert("end", "No records found for the selected date.")

        search_btn = tk.Button(
            date_window,
            text="Search",
            font=("Arial", 12, "bold"),
            fg="#fff",
            bg="#1b1b1b",
            activebackground="#333333",
            activeforeground="#fff",
            padx=15,
            pady=5,
            command=fetch_history,
        )
        search_btn.pack(pady=10)

        history_text = tk.Text(
            date_window,
            wrap="word",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#000",
            padx=10,
            pady=10,
            relief="flat",
        )
        history_text.pack(expand=True, fill="both", padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()
