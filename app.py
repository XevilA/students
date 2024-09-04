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

        
        self.style = Style(theme="superhero")
        self.configure(bg=self.style.colors.light)
        
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
                "gpa": round(3.5 + (i % 5) * 0.1, 1), 
                "image": f"student{i}.jpg",  
                "courses": ["Course A", "Course B", "Course C"]  
            }
        
        with open("students.json", "w") as f:
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

class StudentSelectionFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)

    
        logo_path = "images/student2.jpg"  
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = logo.resize((150, 150), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo)
            logo_label = ttk.Label(main_frame, image=logo_photo, background=self.master.style.colors.light)
            logo_label.image = logo_photo
            logo_label.pack(pady=10, anchor="n")

        ttk.Label(main_frame, text="Select a Student", font=("Helvetica Neue", 18, "bold")).pack(pady=10)

        student_names = [self.master.students[student_id]["name"] for student_id in self.master.students]
        self.student_listbox = tk.Listbox(main_frame, height=10, font=("Helvetica Neue", 12))
        for name in student_names:
            self.student_listbox.insert(tk.END, name)
        self.student_listbox.pack(pady=10, fill=tk.X, padx=20)

        select_button = ttk.Button(main_frame, text="Select", command=self.select_student, style="Accent.TButton", cursor="hand2", width=10)
        select_button.pack(pady=10)

    def select_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            selected_name = self.student_listbox.get(selected_index)
            student_id = next(key for key, value in self.master.students.items() if value["name"] == selected_name)
            self.master.show_main(student_id)

class MainFrame(ttk.Notebook):
    def __init__(self, master, student_id):
        style = ttk.Style()
        style.configure('lefttab.TNotebook', tabposition='wn')
        super().__init__(master, style='lefttab.TNotebook')
        
        self.student_id = student_id
        self.student_data = master.students[student_id]
        self.create_tabs()

    def create_tabs(self):
        self.add(StudentInfoFrame(self, self.student_data), text="📊 Info")
        self.add(StudyTableFrame(self, self.student_data), text="📅 Schedule")

class StudentInfoFrame(ttk.Frame):
    def __init__(self, master, student_data):
        super().__init__(master, padding=20)
        self.create_widgets(student_data)

    def create_widgets(self, student_data):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Student Information", font=("Helvetica Neue", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        row = 1
        for key, value in student_data.items():
            if key not in ["image", "courses"]:
                ttk.Label(self, text=f"{key.capitalize()}:", font=("Helvetica Neue", 14, "bold")).grid(row=row, column=0, sticky="e", pady=5)
                ttk.Label(self, text=str(value), font=("Helvetica Neue", 14)).grid(row=row, column=1, sticky="w", pady=5)
                row += 1

      
        img_frame = ttk.Frame(self, style="Card.TFrame")
        img_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky="nsew")
        img_frame.columnconfigure(0, weight=1)
        img_frame.rowconfigure(0, weight=1)

        try:
            img = Image.open(student_data["image"])
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = ttk.Label(img_frame, image=photo, background=self.master.master.style.colors.light)
            label.image = photo
            label.grid(pady=20)
        except FileNotFoundError:
            ttk.Label(img_frame, text="Image not found", font=("Helvetica Neue", 14)).grid(pady=20)

class StudyTableFrame(ttk.Frame):
    def __init__(self, master, student_data):
        super().__init__(master, padding=20)
        self.student_data = student_data
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Study Schedule", font=("Helvetica Neue", 24, "bold")).grid(row=0, column=0, pady=20)

        schedule_images = {
            "Monday": "images/table.jpg",
            
        }

        for index, (day, image_file) in enumerate(schedule_images.items()):
            ttk.Label(self, text=day, font=("Helvetica Neue", 16)).grid(row=index + 1, column=0, padx=10, pady=5, sticky="w")
            try:
                img = Image.open(image_file)
                img = img.resize((200, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(self, image=photo)
                img_label.image = photo
                img_label.grid(row=index + 1, column=1, padx=10, pady=5)
            except FileNotFoundError:
                ttk.Label(self, text="Image not found", font=("Helvetica Neue", 14)).grid(row=index + 1, column=1, padx=10, pady=5)

if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()
