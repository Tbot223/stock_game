#login system
from main_systems import db
import os
import json

def login():
    db.db_check()
    SaveFilse = ["Player.json"]
    for i in SaveFilse:
        data = [
                    {
                        "name" : "Player",
                        "money" : 100000
                    }
                ]
        if not os.path.isdir("./db/AutoSave/" + i):
            with open("./db/AutoSave/" + i, "w") as f:
                json.dump(data,f)

import tkinter as tk

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
button_login = tk.Button(root, text="로그인", command=check_login)
button_login.pack()

root.mainloop()
    