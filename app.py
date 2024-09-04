import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import os
from ttkbootstrap import Style

class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Information System")
        self.geometry("1024x768")
        self.minsize(1000, 900)

        self.style = Style(theme="darkly")  # Colorful theme
        self.configure(bg=self.style.colors.dark)
        
        self.load_database()
        self.current_frame = None
        self.show_student_selection()

    def load_database(self):
        if not os.path.exists("user.json"):
            self.create_sample_database()
        with open("user.json", "r") as f:
            self.students = json.load(f)

    def create_sample_database(self):
        students = {}
        for i in range(1, 34):
            student_id = f"student{i}"
            students[student_id] = {
                "name": f"นาย ชื่อ นามสกุล {i}",
                "age": 20 + (i % 5),
                "grade": "12th" if i <= 16 else "11th",
                "image": f"student{i}.jpg",
                "courses": ["Course A", "Course B", "Course C"]
            }
        
        with open("user.json", "w") as f:
            json.dump(students, f, indent=2)

    def show_student_selection(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StudentSelectionFrame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_main(self, student_id):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainFrame(self, student_id)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def exit_application(self):
        self.destroy()

class StudentSelectionFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding=30, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)

        logo_path = "images/facereg.jpg"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = logo.resize((150, 150), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo)
            logo_label = ttk.Label(main_frame, image=logo_photo, background=self.master.style.colors.dark)
            logo_label.image = logo_photo
            logo_label.pack(pady=20, anchor="n")

        ttk.Label(main_frame, text="Select a Student", font=("Helvetica Neue", 22, "bold"), background=self.master.style.colors.dark, foreground=self.master.style.colors.primary).pack(pady=20)

        self.student_names = {value["name"]: student_id for student_id, value in self.master.students.items()}
        
        self.student_listbox = tk.Listbox(main_frame, height=10, font=("Helvetica Neue", 14), bg=self.master.style.colors.light, selectmode=tk.SINGLE, bd=0, highlightthickness=0)
        self.student_listbox.pack(pady=20, fill=tk.X, padx=20)
        for name in self.student_names.keys():
            self.student_listbox.insert(tk.END, name)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        select_button = ttk.Button(button_frame, text="Select", command=self.select_student, style="Success.TButton", cursor="hand2", width=12)
        select_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.master.exit_application, style="Danger.TButton", cursor="hand2", width=12)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def select_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            selected_name = self.student_listbox.get(selected_index)
            student_id = self.student_names[selected_name]
            self.master.show_main(student_id)

class MainFrame(ttk.Notebook):
    def __init__(self, master, student_id):
        style = ttk.Style()
        style.configure('lefttab.TNotebook', tabposition='wn')
        super().__init__(master, style='lefttab.TNotebook', padding=10)
        
        self.student_id = student_id
        self.student_data = master.students[student_id]
        self.create_tabs()

    def create_tabs(self):
        self.add(StudentInfoFrame(self, self.student_data), text="📊 Info")
        self.add(StudyTableFrame(self, self.student_data), text="📅 Schedule")

class StudentInfoFrame(ttk.Frame):
    def __init__(self, master, student_data):
        super().__init__(master, padding=20, style="Card.TFrame")
        self.create_widgets(student_data)

    def create_widgets(self, student_data):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Student Information", font=("Helvetica Neue", 26, "bold"), background=self.master.master.style.colors.dark, foreground=self.master.master.style.colors.primary).grid(row=0, column=0, columnspan=2, pady=20)

        row = 1
        for key, value in student_data.items():
            if key not in ["image", "courses"]:
                ttk.Label(self, text=f"{key.capitalize()}:", font=("Helvetica Neue", 16, "bold")).grid(row=row, column=0, sticky="e", pady=10)
                ttk.Label(self, text=str(value), font=("Helvetica Neue", 16)).grid(row=row, column=1, sticky="w", pady=10)
                row += 1

        img_frame = ttk.Frame(self, style="Card.TFrame")
        img_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="nsew")
        img_frame.columnconfigure(0, weight=1)
        img_frame.rowconfigure(0, weight=1)

        try:
            img = Image.open(student_data["image"])
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = ttk.Label(img_frame, image=photo, background=self.master.master.style.colors.dark)
            label.image = photo
            label.grid(pady=20)
        except FileNotFoundError:
            ttk.Label(img_frame, text="Image not found", font=("Helvetica Neue", 16), foreground="red").grid(pady=20)

class StudyTableFrame(ttk.Frame):
    def __init__(self, master, student_data):
        super().__init__(master, padding=20, style="Card.TFrame")
        self.student_data = student_data
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Study Schedule", font=("Helvetica Neue", 26, "bold"), background=self.master.master.style.colors.dark, foreground=self.master.master.style.colors.primary).grid(row=0, column=0, pady=20)

        schedule_images = {
            "ตารางเรียน": "images/table.jpeg"
        }

        for index, (day, image_file) in enumerate(schedule_images.items()):
            ttk.Label(self, text=day, font=("Helvetica Neue", 18, "bold")).grid(row=index + 1, column=0, padx=10, pady=10, sticky="w")
            try:
                img = Image.open(image_file)
                img = img.resize((600, 400), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(self, image=photo)
                img_label.image = photo
                img_label.grid(row=index + 1, column=1, padx=10, pady=10)
            except FileNotFoundError:
                ttk.Label(self, text="Image not found", font=("Helvetica Neue", 16), foreground="red").grid(row=index + 1, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=index + 2, column=0, columnspan=2, pady=20)

        previous_button = ttk.Button(button_frame, text="Previous", command=self.go_previous, style="Secondary.TButton", cursor="hand2", width=12)
        previous_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.master.master.exit_application, style="Danger.TButton", cursor="hand2", width=12)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def go_previous(self):
        self.master.master.show_student_selection()

if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()
