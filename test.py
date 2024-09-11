import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
import pickle
import cv2
import numpy as np
from ttkbootstrap import Style
import face_recognition

class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Information System with Face Recognition")
        self.geometry("1024x768")
        self.minsize(1000, 900)

        self.style = Style(theme="darkly")
        self.configure(bg=self.style.colors.dark)
        
        self.load_database()
        self.current_frame = None
        self.show_student_selection()

    def load_database(self):

        if not os.path.exists("user.json"):
            self.create_sample_database()
        with open("user.json", "r") as f:
            self.students = json.load(f)

       
        if not os.path.exists("face_encodings.pkl") or not os.path.exists("face_labels.pkl"):
            raise FileNotFoundError("Face encodings or labels not found. Please provide 'face_encodings.pkl' and 'face_labels.pkl'.")

        with open("student_face_model.pkl", "rb") as f:
            self.known_face_encodings = pickle.load(f)

        with open("student_labels.pkl", "rb") as f:
            self.known_face_labels = pickle.load(f)

    def create_sample_database(self):
  
        students = {}
        for i in range(1, 34):
            student_id = f"student{i}"
            students[student_id] = {
                "name": f"Student Name {i}",
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

    def recognize_face(self, image_path):
    
        input_image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(input_image)
        
   
        if len(face_encodings) == 0:
            return None

       
        input_encoding = face_encodings[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, input_encoding)
        face_distances = face_recognition.face_distance(self.known_face_encodings, input_encoding)
        
   
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            matched_student_id = self.known_face_labels[best_match_index]
            return matched_student_id
        return None


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

        ttk.Label(main_frame, text="Select a Student or Recognize via Face", font=("Helvetica Neue", 22, "bold"), background=self.master.style.colors.dark, foreground=self.master.style.colors.primary).pack(pady=20)

        self.student_names = {value["name"]: student_id for student_id, value in self.master.students.items()}
        
        self.student_listbox = tk.Listbox(main_frame, height=10, font=("Helvetica Neue", 14), bg=self.master.style.colors.light, selectmode=tk.SINGLE, bd=0, highlightthickness=0)
        self.student_listbox.pack(pady=20, fill=tk.X, padx=20)
        for name in self.student_names.keys():
            self.student_listbox.insert(tk.END, name)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        select_button = ttk.Button(button_frame, text="Select", command=self.select_student, style="Success.TButton", cursor="hand2", width=12)
        select_button.pack(side=tk.LEFT, padx=10)

        face_rec_button = ttk.Button(button_frame, text="Recognize Face", command=self.recognize_face, style="Primary.TButton", cursor="hand2", width=15)
        face_rec_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.master.exit_application, style="Danger.TButton", cursor="hand2", width=12)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def select_student(self):
        selected_index = self.student_listbox.curselection()
        if selected_index:
            selected_name = self.student_listbox.get(selected_index)
            student_id = self.student_names[selected_name]
            self.master.show_main(student_id)

    def recognize_face(self):
        image_path = filedialog.askopenfilename(title="Select an Image for Face Recognition", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if image_path:
            matched_student_id = self.master.recognize_face(image_path)
            if matched_student_id:
                self.master.show_main(matched_student_id)
            else:
                messagebox.showerror("Error", "No matching student found for the provided face image.")


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
            ttk.Label(img_frame, text="No Image Available", font=("Helvetica Neue", 16), background=self.master.master.style.colors.dark).grid(pady=20)


class StudyTableFrame(ttk.Frame):
    def __init__(self, master, student_data):
        super().__init__(master, padding=20, style="Card.TFrame")
        self.create_widgets(student_data)

    def create_widgets(self, student_data):
        ttk.Label(self, text="Courses", font=("Helvetica Neue", 26, "bold"), background=self.master.master.style.colors.dark, foreground=self.master.master.style.colors.primary).pack(pady=20)

        courses_frame = ttk.Frame(self)
        courses_frame.pack(fill=tk.BOTH, expand=True)

        for course in student_data["courses"]:
            ttk.Label(courses_frame, text=course, font=("Helvetica Neue", 18), style="Card.TLabel").pack(pady=10)


if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()
