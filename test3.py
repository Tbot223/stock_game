import tkinter as tk
from tkinter import ttk, messagebox
import json

# JSON 파일을 읽습니다.
with open('stocks.json', 'r') as f:
    stocks = json.load(f)

root = tk.Tk()
tree = ttk.Treeview(root)
root.title("주식 정보")

# Treeview를 생성합니다.
treeview = ttk.Treeview(root, columns=("name", "price", "change"), show="headings")
treeview.heading("name", text="Name")
treeview.heading("price", text="Price")
treeview.heading("change", text="change")

treeview.column("name", width=100, anchor='center')
treeview.column("price", width=100, anchor='center')
treeview.column("change", width=50, anchor='center')

# 각 주식에 대한 정보를 Treeview에 추가합니다.
for i, stock in enumerate(stocks):
    stock_name = stock['name']
    stock_price = stock['price']
    treeview.insert('', 'end', values=(stock_name, stock_price))

    # 홀수 번째 항목의 배경색을 변경합니다.
    if i % 2:
        treeview.tag_configure('oddrow', background='orange')
        treeview.item(treeview.get_children()[-1], tags=('oddrow',))

def on_double_click(event):
    item = treeview.selection()[0]  # 선택된 항목의 ID를 가져옵니다.
    item_text = treeview.item(item, 'values')[0]  # 선택된 항목의 'name' 값을 가져옵니다.
    messagebox.showinfo("Item Selected", item_text)  # 메시지 박스에 선택된 항목의 텍스트를 표시합니다.

treeview.bind("<Double-1>", on_double_click)  # 더블 클릭 이벤트를 바인드합니다.

treeview.pack()

root.mainloop()
