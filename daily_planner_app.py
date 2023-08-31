import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class DailyPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Planner")
        self.tasks = {"Daily": [], "Weekly": [], "Monthly": []}
        self.goals = {"Week": [], "Month": [], "Year": []}

        # Save plans when the program is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_gui()

    def on_closing(self):
        # Check if there are any tasks or goals before saving
        if not self.tasks_empty() or not self.goals_empty():
            # Save plans when the program is closed
            self.save_as_pdf()
        self.root.destroy()

    def tasks_empty(self):
        for frequency, tasks in self.tasks.items():
            if tasks:
                return False
        return True

    def goals_empty(self):
        for goals_list in self.goals.values():
            if goals_list:
                return False
        return True

    def create_gui(self):
        self.create_task_frame()
        self.create_goal_frame()
        self.create_pdf_frame()
        self.create_task_table()
        self.update_goal_table()
        self.update_task_table()

    def create_task_frame(self):
        task_frame = ttk.LabelFrame(self.root, text="Add Task")
        task_frame.pack(padx=10, pady=10, fill="both", expand="True", side="left")

        task_name_label = ttk.Label(task_frame, text="Task Name:")
        task_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.task_entry = ttk.Entry(task_frame)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        due_date_label = ttk.Label(task_frame, text="Due Date:")
        due_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.due_date_entry = ttk.Entry(task_frame)
        self.due_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.frequency_var = tk.StringVar()
        self.frequency_var.set("Daily")

        frequency_label = ttk.Label(task_frame, text="Frequency:")
        frequency_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.frequency_menu = ttk.OptionMenu(
            task_frame, self.frequency_var, "Daily", "Daily", "Weekly", "Monthly"
        )
        self.frequency_menu.config(width=15)  # Adjust the width as needed
        self.frequency_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.schedule_label = ttk.Label(task_frame, text="Daily Schedule:")
        self.schedule_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.schedule_entry = ttk.Entry(task_frame)
        self.schedule_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        importance_label = ttk.Label(task_frame, text="Importance:")
        importance_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.importance_var = tk.StringVar()
        self.importance_var.set("Low")

        importance_menu = ttk.OptionMenu(
            task_frame, self.importance_var, "Low", "Low", "Medium", "High"
        )
        importance_menu.config(width=15)
        importance_menu.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.add_button = ttk.Button(task_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = ttk.Button(
            task_frame, text="Delete Task", command=self.delete_task
        )
        self.delete_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def create_pdf_frame(self):
        pdf_frame = ttk.LabelFrame(self.root, text="PDF Actions")
        pdf_frame.pack(padx=10, pady=10, fill="both", expand="True")

        self.save_pdf_button = ttk.Button(
            pdf_frame, text="Save as PDF", command=self.save_as_pdf
        )
        self.save_pdf_button.pack(padx=10, pady=10)

    def create_task_table(self):
        table_frame = ttk.LabelFrame(self.root, text="Task List")
        table_frame.pack(padx=5, pady=5, fill="both", expand=True, side="right")

        self.task_table = ttk.Treeview(
            table_frame,
            columns=("Frequency", "Task", "Due Date", "Schedule", "Importance"),
            show="headings",
        )

        self.task_table.heading("Frequency", text="Frequency")
        self.task_table.heading("Task", text="Task")
        self.task_table.heading("Due Date", text="Due Date")
        self.task_table.heading("Schedule", text="Schedule")
        self.task_table.heading("Importance", text="Importance")

        self.task_table.column("Frequency", width=75)
        self.task_table.column("Task", width=150)
        self.task_table.column("Due Date", width=100)
        self.task_table.column("Schedule", width=100)
        self.task_table.column("Importance", width=60, anchor="center")

        self.task_table.pack(padx=5, pady=5, expand=True, fill="both")
        # Additional options to expand the LabelFrame
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

    def update_task_table(self):
        self.task_table.delete(*self.task_table.get_children())
        sorted_tasks = []

        for frequency, tasks in self.tasks.items():
            sorted_tasks.extend(tasks)

        sorted_tasks.sort(
            key=lambda task: (
                {"Low": 0, "Medium": 1, "High": 2}[task["importance"]],
                task["due_date"],
            )
        )

        for task_info in sorted_tasks:
            importance = task_info["importance"]
            importance_color = {"Low": "green", "Medium": "yellow", "High": "red"}.get(
                importance, ""
            )

            self.task_table.insert(
                "",
                "end",
                values=(
                    frequency,
                    task_info["task"],
                    task_info["due_date"],
                    task_info.get("schedule"),
                ),
                tags=(importance_color,),
            )
            self.task_table.tag_configure(
                importance_color, background=importance_color, foreground="Black"
            )

    def delete_task(self):
        selected_item = self.task_table.selection()
        if not selected_item:
            messagebox.showwarning(
                "No Task Selected", "Please select a task to delete."
            )
            return

        item = self.task_table.item(selected_item)
        frequency = item["values"][2]
        task = item["values"][0]

        for task_info in self.tasks[frequency]:
            if task_info["task"] == task:
                self.tasks[frequency].remove(task_info)
                self.update_task_table()
                return

    def delete_goal(self):
        selected_item = self.goal_table.selection()
        if not selected_item:
            messagebox.showwarning(
                "No Goal Selected", "Please select a goal to delete."
            )
            return

        item = self.goal_table.item(selected_item)
        goal_type = item["values"][0]
        goal = item["values"][1]

        if goal in self.goals[goal_type]:
            self.goals[goal_type].remove(goal)
            self.update_goal_table()

    def add_task(self):
        task = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        frequency = self.frequency_var.get()
        schedule = self.schedule_entry.get().strip()
        importance = self.importance_var.get()

        if not task:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")
            return

        for existing_task in self.tasks[frequency]:
            if existing_task["task"] == task:
                messagebox.showinfo(
                    "Task Already Added", f"The task '{task}' has already been added."
                )
                return

        self.tasks[frequency].append(
            {
                "task": task,
                "due_date": due_date,
                "schedule": schedule,
                "importance": importance,
                "frequency": frequency,
            }
        )
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.schedule_entry.delete(0, tk.END)
        self.update_task_table()

    def save_as_pdf(self):
        if self.tasks_empty() and self.goals_empty():
            messagebox.showinfo("Nothing to Save", "No tasks or goals to save.")
            return

        file_name = f"DailyPlanner_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        pdf_path = os.path.join(os.getcwd(), file_name)

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []

        # Explanation Table
        data = [["Importance", "Color"], ["Low", "•"], ["Medium", "•"], ["High", "•"]]

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 20),
                    ("TEXTCOLOR", (1, 1), (1, 1), colors.green),
                    ("TEXTCOLOR", (1, 2), (1, 2), colors.yellow),
                    ("TEXTCOLOR", (1, 3), (1, 3), colors.red),
                    ("FONTSIZE", (1, 1), (1, -1), 15),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ]
            )
        )

        # Create a two-column grid for the header section (day and explanation table)
        header_grid = [
            [
                Paragraph(
                    f"Daily Planner: {datetime.now().strftime('%Y-%m-%d')}",
                    getSampleStyleSheet()["Title"],
                ),
                table,
            ]
        ]
        header_table = Table(header_grid, colWidths=[3 * inch, 2 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )
        story.append(header_table)

        # Spacer
        story.append(Spacer(1, 20))

        # Sort tasks by importance (High first, Low last) and then by due date
        sorted_tasks = []
        for frequency, tasks in self.tasks.items():
            sorted_tasks.extend(
                sorted(
                    tasks,
                    key=lambda x: ("High", "Medium", "Low").index(x["importance"]),
                )
            )

        # Print tasks in separate tables for daily, weekly, and monthly
        for frequency in ["Daily", "Weekly", "Monthly"]:
            frequency_tasks = [
                task for task in sorted_tasks if task["frequency"] == frequency
            ]
            if frequency_tasks:
                # Create a table header
                task_data = [
                    ["Frequency", "Task", "Due Date", "Schedule", "Importance"]
                ]
                for task_info in frequency_tasks:
                    importance = task_info["importance"]
                    importance_color = {
                        "Low": "green",
                        "Medium": "yellow",
                        "High": "red",
                    }.get(importance, "")

                    dot = f"<font color='{importance_color}'>\u25CF</font>"
                    task_data.append(
                        [
                            frequency,
                            Paragraph(
                                task_info["task"], getSampleStyleSheet()["Normal"]
                            ),
                            task_info["due_date"],
                            task_info.get("schedule", ""),
                            Paragraph(
                                dot, getSampleStyleSheet()["Normal"]
                            ),  # Insert the colored dot
                        ]
                    )

                # Create the tasks table
                tasks_table = Table(
                    task_data,
                    colWidths=[
                        1.5 * inch,
                        2.5 * inch,
                        1 * inch,
                        1.5 * inch,
                        1.5 * inch,
                    ],
                )  # Adjust column widths
                tasks_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                story.append(
                    Paragraph(frequency, getSampleStyleSheet()["Heading1"])
                )  # Add frequency as a heading
                story.append(tasks_table)
                story.append(Spacer(1, 20))  # Add space between tables

        # Spacer
        story.append(Spacer(1, 20))  # Adds 20 units of vertical space

        # Goals Table
        goal_data = [["Goal Type", "Goal"]]
        for goal_type, goals_list in self.goals.items():
            for goal in goals_list:
                goal_data.append(
                    [
                        goal_type,
                        Paragraph(
                            goal, getSampleStyleSheet()["Normal"]
                        ),  # Wrap goal in a Paragraph
                    ]
                )

        goals_table = Table(goal_data, colWidths=[1.5 * inch, 4 * inch])
        goals_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(goals_table)

        # Prayer Schedule Table
        prayer_names = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        prayer_times = ["5:00 AM", "1:00 PM", "4:30 PM", "7:19 PM", "8:39 PM"]
        Nwafel = ["2 before", "4 before and 2 after", "-", "2 after", "2 after"]

        prayer_schedule_data = [
            ["prayer Name", "prayer Time", "Nwafel", "Done", "Nwafel Done?"]
        ]
        for name, time, _ in zip(prayer_names, prayer_times, Nwafel):
            prayer_schedule_data.append([name, time, _])

        prayer_schedule_table = Table(
            prayer_schedule_data,
            colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch],
        )
        prayer_schedule_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(Paragraph("prayer Schedule", getSampleStyleSheet()["Heading1"]))
        story.append(prayer_schedule_table)

        # Spacer
        story.append(Spacer(1, 20))

        # Sunnah Prayers
        sunnah_prayers = [
            {"name": "Duha", "scheduled_time": "8:00 AM"},
            {"name": "Tahajjud", "scheduled_time": "4:00 AM"},
            {"name": "Ishraq", "scheduled_time": "7:30 AM"},
        ]
        sunnah_data = [["Sunnah prayer", "Scheduled Time", "Done"]]
        for prayer in sunnah_prayers:
            sunnah_data.append([prayer["name"], prayer["scheduled_time"], ""])

        sunnah_table = Table(sunnah_data, colWidths=[2 * inch, 2 * inch, 1 * inch])
        sunnah_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(Paragraph("Sunnah Prayers", getSampleStyleSheet()["Heading1"]))
        story.append(sunnah_table)

        doc.build(story)

        messagebox.showinfo("PDF Saved", f"Planner saved as {file_name}")

    def create_goal_frame(self):
        goal_frame = ttk.LabelFrame(self.root, text="Set Goal")
        goal_frame.pack(padx=10, pady=10, fill="both", expand="True")

        goal_type_label = ttk.Label(goal_frame, text="Goal:")
        goal_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.goal_entry = ttk.Entry(goal_frame)
        self.goal_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        goal_type_label = ttk.Label(goal_frame, text="Goal Type:")
        goal_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.goal_type_var = tk.StringVar()
        self.goal_type_var.set("Week")

        self.goal_type_menu = ttk.OptionMenu(
            goal_frame, self.goal_type_var, "Week", "Week", "Month", "Year"
        )
        self.goal_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.set_goal_button = ttk.Button(
            goal_frame, text="Set Goal", command=self.set_goal
        )
        self.set_goal_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Goal Table
        self.goal_table = ttk.Treeview(
            goal_frame, columns=("Goal Type", "Goal"), show="headings"
        )

        self.goal_table.heading("Goal Type", text="Goal Type")
        self.goal_table.heading("Goal", text="Goal")
        self.goal_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.delete_goal_button = ttk.Button(
            goal_frame, text="Delete Goal", command=self.delete_goal
        )
        self.delete_goal_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def update_goal_table(self):
        self.goal_table.delete(*self.goal_table.get_children())
        for goal_type, goals_list in self.goals.items():
            for goal in goals_list:
                delete_button = ttk.Button(
                    self.goal_table, text="Delete", command=self.delete_goal
                )
                self.goal_table.insert(
                    "", "end", values=(goal_type, goal), tags=("delete_button",)
                )

    def set_goal(self):
        goal_type = self.goal_type_var.get()
        goal = self.goal_entry.get().strip()

        if not goal:
            messagebox.showwarning("Empty Goal", "Please enter a goal before setting.")
            return
        # Check if the goal already exists
        if goal in self.goals[goal_type]:
            messagebox.showinfo(
                "Goal Already Added",
                f"The goal '{goal}' for '{goal_type}' has already been set.",
            )
            return
        self.goals[goal_type].append(goal)
        self.goal_entry.delete(0, tk.END)
        self.update_goal_table()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")  # Adjust the dimensions as needed
    app = DailyPlannerApp(root)
    root.mainloop()
