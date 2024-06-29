import tkinter as tk
from tkinter import messagebox
import json

path = "./infomation.json"

def show_success_message():
    success_window = tk.Tk()
    success_window.title("성공")
    success_label = tk.Label(success_window, text="로그인에 성공했습니다!")
    success_label.pack()
    success_window.mainloop()

def check_credentials():
    with open(path, "r") as json_file:
        json_data = json.load(json_file)

    json_player = json_data["player"]
    
    for i in json_player:
        if username_entry.get() == i["name"] and password_entry.get() == i["password"]:
            messagebox.showinfo("로그인 성공", "환영합니다!")
            root.destroy()  # 로그인 창을 닫습니다.
            show_success_message()
    else:
        messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")

root = tk.Tk()
root.title("로그인 창")

username_label = tk.Label(root, text="사용자 이름:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="비밀번호:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="로그인", command=check_credentials)
login_button.pack()

root.mainloop()