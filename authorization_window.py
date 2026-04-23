import tkinter as tk
from tkinter import messagebox
import re
import json
import os

class AuthorizationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Окно авторизации")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        
        self.setup_data_folder()
        
       
        self.load_users()
        
        
        self.current_user = None
        
        
        self.create_auth_interface()
    
    def setup_data_folder(self):
       
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        
        self.data_dir = os.path.join(script_dir, "data")
        
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Создана папка для данных: {self.data_dir}")
        
        
        self.users_file = os.path.join(self.data_dir, "users.json")
        print(f"Файл пользователей: {self.users_file}")
    
    def load_users(self):
       
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
                print(f"Загружено пользователей: {len(self.users)}")
            else:
                self.users = {}
                print("Файл users.json не найден, создаем новую базу данных")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            self.users = {}
    
    def save_users(self):
       
        try:
            
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=4)
            
            print(f"Сохранено пользователей: {len(self.users)}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
            return False
    
    def validate_email(self, email):
       
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_auth_interface(self):
       
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        
        tk.Label(self.root, text="Авторизация", font=("Arial", 20, "bold")).pack(pady=20)
        
        
        tk.Label(self.root, text="Логин:", font=("Arial", 12)).pack(pady=(10, 0))
        self.login_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.login_entry.pack(pady=5)
        
       
        tk.Label(self.root, text="Пароль:", font=("Arial", 12)).pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)
        
       
        tk.Label(self.root, text="Email:", font=("Arial", 12)).pack(pady=(10, 0))
        self.email_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.email_entry.pack(pady=5)
        
        
        tk.Button(self.root, text="Войти", font=("Arial", 12), 
                 command=self.login, bg="#4CAF50", fg="white", width=20).pack(pady=20)
        
        tk.Button(self.root, text="Зарегистрироваться", font=("Arial", 10),
                 command=self.register, bg="#2196F3", fg="white", width=20).pack(pady=5)
        
        
        path_label = tk.Label(self.root, text=f"Данные сохраняются в:\n{self.users_file}", 
                             font=("Arial", 8), fg="gray")
        path_label.pack(side=tk.BOTTOM, pady=10)
    
    def login(self):
       
        login = self.login_entry.get().strip()
        password = self.password_entry.get()
        email = self.email_entry.get().strip()
        
        
        if not login or not password or not email:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
       
        if login in self.users:
            user_data = self.users[login]
            if user_data["password"] == password and user_data["email"] == email:
                self.current_user = login
                messagebox.showinfo("Успех", f"Добро пожаловать, {login}!")
                self.create_personal_page()
            else:
                messagebox.showerror("Ошибка", "Неверный пароль или email!")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
    
    def register(self):
        
        login = self.login_entry.get().strip()
        password = self.password_entry.get()
        email = self.email_entry.get().strip()
        
       
        if not login or not password or not email:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        
        if len(login) < 3:
            messagebox.showerror("Ошибка", "Логин должен содержать минимум 3 символа!")
            return
        
        
        if len(password) < 4:
            messagebox.showerror("Ошибка", "Пароль должен содержать минимум 4 символа!")
            return
        
        
        if not self.validate_email(email):
            messagebox.showerror("Ошибка", "Введите корректный email!")
            return
        
        
        if login in self.users:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
            return
        
        
        self.users[login] = {
            "password": password,
            "email": email
        }
        
        
        if self.save_users():
            messagebox.showinfo("Успех", "Регистрация прошла успешно! Теперь вы можете войти.")
           
            self.login_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            
            del self.users[login]
    
    def create_personal_page(self):
       
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        
        tk.Label(self.root, text=f"Личная страница", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Добро пожаловать, {self.current_user}!", 
                font=("Arial", 16)).pack(pady=10)
        
       
        user_info = self.users[self.current_user]
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=20)
        
        tk.Label(info_frame, text="Информация о пользователе:", 
                font=("Arial", 14, "bold")).pack()
        tk.Label(info_frame, text=f"Логин: {self.current_user}", 
                font=("Arial", 12)).pack(pady=5)
        tk.Label(info_frame, text=f"Email: {user_info['email']}", 
                font=("Arial", 12)).pack(pady=5)
        
        
        tk.Button(self.root, text="Редактировать профиль", font=("Arial", 12),
                 command=self.edit_profile, bg="#FF9800", fg="white", width=20).pack(pady=10)
        
        tk.Button(self.root, text="Выйти из аккаунта", font=("Arial", 12),
                 command=self.logout, bg="#f44336", fg="white", width=20).pack(pady=5)
        
        
        path_label = tk.Label(self.root, text=f"Данные сохранены в:\n{self.users_file}", 
                             font=("Arial", 8), fg="gray")
        path_label.pack(side=tk.BOTTOM, pady=10)
    
    def edit_profile(self):
       
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование профиля")
        edit_window.geometry("350x300")
        edit_window.resizable(False, False)
        
        tk.Label(edit_window, text="Редактирование профиля", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        
        tk.Label(edit_window, text="Текущий пароль:", font=("Arial", 12)).pack()
        current_pass = tk.Entry(edit_window, font=("Arial", 12), width=25, show="*")
        current_pass.pack(pady=5)
        
        
        tk.Label(edit_window, text="Новый пароль:", font=("Arial", 12)).pack()
        new_pass = tk.Entry(edit_window, font=("Arial", 12), width=25, show="*")
        new_pass.pack(pady=5)
        
        
        tk.Label(edit_window, text="Новый email:", font=("Arial", 12)).pack()
        new_email = tk.Entry(edit_window, font=("Arial", 12), width=25)
        new_email.insert(0, self.users[self.current_user]["email"])
        new_email.pack(pady=5)
        
        def save_changes():
            
            if current_pass.get() != self.users[self.current_user]["password"]:
                messagebox.showerror("Ошибка", "Неверный текущий пароль!")
                return
            
            changes_made = False
            
            
            if new_pass.get():
                if len(new_pass.get()) < 4:
                    messagebox.showerror("Ошибка", "Новый пароль должен содержать минимум 4 символа!")
                    return
                self.users[self.current_user]["password"] = new_pass.get()
                changes_made = True
            
            
            if new_email.get() != self.users[self.current_user]["email"]:
                if not self.validate_email(new_email.get()):
                    messagebox.showerror("Ошибка", "Введите корректный email!")
                    return
                self.users[self.current_user]["email"] = new_email.get()
                changes_made = True
            
            if changes_made:
                if self.save_users():
                    messagebox.showinfo("Успех", "Профиль успешно обновлен!")
                    edit_window.destroy()
                    self.create_personal_page()  # Обновляем личную страницу
                else:
                    messagebox.showerror("Ошибка", "Не удалось сохранить изменения!")
            else:
                messagebox.showinfo("Информация", "Изменения не были внесены")
        
        tk.Button(edit_window, text="Сохранить изменения", font=("Arial", 12),
                 command=save_changes, bg="#4CAF50", fg="white", width=20).pack(pady=20)
        
        tk.Button(edit_window, text="Отмена", font=("Arial", 12),
                 command=edit_window.destroy, bg="#f44336", fg="white", width=20).pack()
    
    def logout(self):
       
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.current_user = None
            self.create_auth_interface()


def main():
    root = tk.Tk()
    app = AuthorizationWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
