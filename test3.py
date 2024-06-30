import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview Example")

# 스타일 정의
style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.map("Treeview", background=[("selected", "blue")])

# Treeview 생성
tree = ttk.Treeview(root, columns=("column1", "column2"), show="headings")
tree.heading("column1", text="Column 1")
tree.heading("column2", text="Column 2")

# 데이터 삽입
for i in range(10):
    tree.insert("", "end", values=(f"Item {i+1}", f"Value {i+1}"))

# Treeview 배치
tree.pack(fill="both", expand=True)

# 열과 행 사이에 선 넣기
tree.tag_configure("evenrow", background="lightblue")
tree.tag_configure("oddrow", background="white")

for i in range(len(tree.get_children())):
    if i % 2 == 0:
        tree.item(tree.get_children()[i], tags=("evenrow",))
    else:
        tree.item(tree.get_children()[i], tags=("oddrow",))

root.mainloop()