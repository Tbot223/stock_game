import tkinter as tk
from tkinter import ttk

def check_login():
    # 사용자 이름과 비밀번호를 하드코딩하여 비교
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "password":
        print("로그인 성공!")
    else:
        print("로그인 실패!")

# Tkinter 창 생성
root = tk.Tk()
style = ttk.Style()
style.configure('My.TButton', font=('Helvetica', 12, 'bold'), foreground='blue')
root.title("로그인")

# 사용자 이름 입력 필드
label_username = tk.Label(root, text="사용자 이름:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# 비밀번호 입력 필드
label_password = tk.Label(root, text="비밀번호:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# 로그인 버튼
button_login = ttk.Button(root, text="로그인", command=check_login, style='My.TButton')
button_login.pack()
button_sing_up = tk.Button(root, text="가입")
button_login.grid(row = 0,column=1)
button_sing_up.pack()

root.mainloop()
