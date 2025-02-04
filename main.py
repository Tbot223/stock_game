import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

# JSON 파일을 읽습니다.
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# JSON 파일을 저장합니다.
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

class StockApp(tk.Tk):
    def __init__(self, stocks, player):
        super().__init__()

        self.title("주식 정보")
        self.geometry("800x600")

        self.stocks = stocks
        self.player = player

        # 게임 일시정지 플래그
        self.is_paused = False

        # 메뉴바 생성
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 게임 메뉴 생성
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="게임", menu=game_menu)
        game_menu.add_command(label="게임 저장", command=self.save_game)
        game_menu.add_command(label="게임 종료", command=self.quit_game)
        game_menu.add_command(label="게임 일시정지", command=self.stop_prices)
        game_menu.add_command(label="게임 재개", command=self.start_prices)

        # Notebook (탭) 생성
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # 주식 정보 탭
        self.stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stock_frame, text="주식 정보")

        # 내가 산 주식 탭
        self.my_stocks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.my_stocks_frame, text="내가 산 주식")

        # Treeview를 생성합니다.
        self.treeview = ttk.Treeview(self.stock_frame, columns=("name", "price", "change", "pct_change", "abs_change"), show="headings")
        self.treeview.heading("name", text="Name", command=lambda: self.sort_column("name", False))
        self.treeview.heading("price", text="Price", command=lambda: self.sort_column("price", False))
        self.treeview.heading("change", text="Change", command=lambda: self.sort_column("change", False))
        self.treeview.heading("pct_change", text="Pct Change", command=lambda: self.sort_column("pct_change", False))
        self.treeview.heading("abs_change", text="Abs Change", command=lambda: self.sort_column("abs_change", False))


        self.treeview.column("name", width=100, anchor='center')
        self.treeview.column("price", width=100, anchor='center')
        self.treeview.column("change", width=40, anchor='center')
        self.treeview.column("pct_change", width=40, anchor='center')
        self.treeview.column("abs_change", width=40, anchor='center')

        # 각 주식에 대한 정보를 Treeview에 추가합니다.
        for i, stock in enumerate(self.stocks):
            stock_name = stock['name']
            stock_price = stock['price']
            stock_change = stock.get('change', '')

            self.treeview.insert('', 'end', values=(stock_name, stock_price, stock_change))

            # 홀수 번째 항목의 배경색을 변경합니다.
            if i % 2:
                self.treeview.tag_configure('oddrow', background='orange')
                self.treeview.item(self.treeview.get_children()[-1], tags=('oddrow',))

        self.treeview.bind("<Double-1>", self.on_double_click)
        self.treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Treeview 스타일 설정
        style = ttk.Style()
        style.configure("Treeview.Heading", relief="flat", borderwidth=1)
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")
        style.map("Treeview.Heading", relief=[('active', 'flat'), ('pressed', 'flat')])

        # 주식 이름
        self.stock_name_label = tk.Label(self.stock_frame, text="주식 이름", relief="solid", borderwidth=1)
        self.stock_name_label.pack(side=tk.TOP, anchor='w', padx=10, pady=5, fill=tk.X)

        # 주식 가격
        self.stock_price_label = tk.Label(self.stock_frame, text="주식 가격", relief="solid", borderwidth=1)
        self.stock_price_label.pack(side=tk.TOP, anchor='w', padx=10, pady=5, fill=tk.X)

        # 현재 남은 돈
        self.money_label = tk.Label(self.stock_frame, text=f"남은 돈: {self.player['money']:.2f}", relief="solid", borderwidth=1)
        self.money_label.pack(side=tk.TOP, anchor='w', padx=10, pady=5, fill=tk.X)

        # 수량 레이블
        self.quantity_label = tk.Label(self.stock_frame, text="수량", relief="solid", borderwidth=1)
        self.quantity_label.pack(side=tk.LEFT, anchor='e', padx=10, pady=5)

        # 수량 조절 칸 (스핀 박스)
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spinbox = ttk.Spinbox(self.stock_frame, from_=1, to=999, textvariable=self.quantity_var, wrap=True)
        self.quantity_spinbox.pack(side=tk.LEFT, anchor='e', padx=10, pady=5)

        # 구매 버튼
        self.buy_button = tk.Button(self.stock_frame, text="구매", command=self.confirm_purchase)
        self.buy_button.pack(side=tk.LEFT, anchor='e', padx=10, pady=5)

        # 판매 버튼
        self.sell_button = tk.Button(self.stock_frame, text="판매", command=self.confirm_sale)
        self.sell_button.pack(side=tk.LEFT, anchor='e', padx=10, pady=5)

        self.sort_order = {"name": False, "price": False, "change": False}

        # 내가 산 주식 Treeview 생성
        self.my_stocks_treeview = ttk.Treeview(self.my_stocks_frame, columns=("name", "quantity"), show="headings")
        self.my_stocks_treeview.heading("name", text="Name")
        self.my_stocks_treeview.heading("quantity", text="Quantity")

        self.my_stocks_treeview.column("name", width=100, anchor='center')
        self.my_stocks_treeview.column("quantity", width=100, anchor='center')

        self.my_stocks_treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 주식 가격 변동 스레드 시작
        self.update_prices()
        self.update_my_stocks()

    def sort_column(self, col, reverse):
        l = [(self.treeview.set(k, col), k) for k in self.treeview.get_children('')]
        
        # 숫자 열을 정렬할 때는 숫자로 변환
        if col == "pct_change":
            l.sort(key=lambda t: float(t[0].rstrip('%')) if t[0] else 0, reverse=reverse)
        elif col in ["price", "abs_change"]:
            l.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
        else:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.treeview.move(k, '', index)

        self.treeview.heading(col, text=f"{col.capitalize()} {'▲' if reverse else '▼'}", command=lambda: self.sort_column(col, not reverse))
        self.sort_order[col] = not reverse

        # 다른 열의 정렬 상태 초기화
        for other_col in self.sort_order:
            if other_col != col:
                self.treeview.heading(other_col, text=other_col.capitalize(), command=lambda c=other_col: self.sort_column(c, self.sort_order[c]))

    def on_double_click(self, event):
        selected_items = self.treeview.selection()
        if selected_items:
            item = selected_items[0]  # 선택된 항목의 ID를 가져옵니다.
            item_values = self.treeview.item(item, 'values')  # 선택된 항목의 값을 가져옵니다.
            stock_name = item_values[0]
            stock_price = item_values[1]

            # 주식 이름과 가격을 업데이트합니다.
            self.stock_name_label.config(text=f"주식 이름: {stock_name}")
            self.stock_price_label.config(text=f"주식 가격: {stock_price}")

    def confirm_purchase(self):
        quantity = self.quantity_var.get()
        selected_items = self.treeview.selection()
        if selected_items:
            item = selected_items[0]
            item_values = self.treeview.item(item, 'values')
            stock_name = item_values[0]
            stock_price = float(item_values[1])
            total_price = stock_price * quantity

            if self.player['money'] >= total_price:
                if messagebox.askyesno("구매 확인", f"{stock_name} 주식을 {quantity}개 구매하시겠습니까?\n총 가격: {total_price:.2f}"):
                    self.player['money'] -= total_price
                    if stock_name in self.player['stocks']:
                        self.player['stocks'][stock_name] += quantity
                    else:
                        self.player['stocks'][stock_name] = quantity
                    self.money_label.config(text=f"남은 돈: {self.player['money']:.2f}")
                    self.update_my_stocks()
                    messagebox.showinfo("구매 완료", "구매가 완료되었습니다.")
            else:
                messagebox.showwarning("잔액 부족", "잔액이 부족합니다.")

    def confirm_sale(self):
        quantity = self.quantity_var.get()
        selected_items = self.treeview.selection()
        if selected_items:
            item = selected_items[0]
            item_values = self.treeview.item(item, 'values')
            stock_name = item_values[0]
            stock_price = float(item_values[1])
            total_price = stock_price * quantity

            if stock_name in self.player['stocks'] and self.player['stocks'][stock_name] >= quantity:
                if messagebox.askyesno("판매 확인", f"{stock_name} 주식을 {quantity}개 판매하시겠습니까?\n총 가격: {total_price:.2f}"):
                    self.player['money'] += total_price
                    self.player['stocks'][stock_name] -= quantity
                    if self.player['stocks'][stock_name] == 0:
                        del self.player['stocks'][stock_name]
                    self.money_label.config(text=f"남은 돈: {self.player['money']:.2f}")
                    self.update_my_stocks()  # <--- Add this line
                    messagebox.showinfo("판매 완료", "판매가 완료되었습니다.")
            else:
                messagebox.showwarning("주식 부족", "판매할 주식이 부족합니다.")

    def save_game(self):
        os.makedirs('./db/Save', exist_ok=True)
        save_json(self.stocks, './db/Save/stocks.json')
        save_json([self.player], './db/Save/player.json')
        messagebox.showinfo("게임 저장", "게임이 저장되었습니다.")

    def quit_game(self):
        self.quit()

    def stop_prices(self):
        self.is_paused = True

    def start_prices(self):
        self.is_paused = False
        self.update_prices()

    def update_prices(self):
        if not self.is_paused:
            for item in self.treeview.get_children():
                current_price = float(self.treeview.set(item, "price"))
                new_price = current_price * (1 + random.uniform(-0.025, 0.025))  # ±10% variation
                change = "▲" if new_price > current_price else "▼"
                pct_change = f"{(new_price / current_price - 1) * 100:.2f}%"
                abs_change = f"{new_price - current_price:.2f}"
                color = "red" if new_price > current_price else "blue"
                self.treeview.set(item, "price", f"{new_price:.2f}")
                self.treeview.set(item, "change", change)
                self.treeview.set(item, "pct_change", pct_change)
                self.treeview.set(item, "abs_change", abs_change)
                self.treeview.tag_configure(item, foreground=color)
                self.treeview.item(item, tags=(item,))

        self.after(10000, self.update_prices)

        # 5초마다 가격 업데이트
        self.after(5000, self.update_prices)
    
    def update_my_stocks(self):
        self.my_stocks_treeview.delete(*self.my_stocks_treeview.get_children())
        for stock, quantity in self.player['stocks'].items():
            self.my_stocks_treeview.insert('', 'end', values=(stock, quantity))

class StartApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("주식 게임")
        self.geometry("300x200")

        start_button = tk.Button(self, text="게임 시작", command=self.start_game)
        start_button.pack(pady=20)

        new_button = tk.Button(self, text="새로하기", command=self.new_game)
        new_button.pack(pady=20)

    def start_game(self):
        if not os.path.exists('./db/Save'):
            os.makedirs('./db/Save', exist_ok=True)
        if not os.path.exists('./db/Save/stocks.json') or not os.path.exists('./db/Save/player.json'):
            stocks = load_json('./stocks.json')
            player = load_json('./player.json')[0]
            player['stocks'] = {}
        else:
            stocks = load_json('./db/Save/stocks.json')
            player = load_json('./db/Save/player.json')[0]

        self.destroy()
        app = StockApp(stocks, player)
        app.mainloop()

    def new_game(self):
        a = 1

if __name__ == "__main__":
    app = StartApp()
    app.mainloop()