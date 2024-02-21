import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import json
import os

class WordcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("词汇卡片学习工具")
        self.root.geometry("600x400+300+200")

        self.cards = self.load_cards()  # Load cards before UI setup to ensure card data is available
        self.current_card_index = 0
        self.showing_front = True  # Track the current side being displayed
        
        self.setup_ui()

    def setup_ui(self):
        self.card_selector = ttk.Combobox(self.root, state="readonly")
        self.card_selector.grid(row=0, column=0, padx=10, pady=10)
        self.card_selector['values'] = [card['front'] for card in self.cards] if self.cards else []

        self.card_display = tk.Label(self.root, text="", width=20, height=10, bg="white", font=("Arial", 16))
        self.card_display.grid(row=1, column=1, padx=10, pady=10)

        self.prev_button = tk.Button(self.root, text="上一个", command=self.show_prev_card)
        self.prev_button.grid(row=2, column=0, padx=10, pady=10)

        self.next_button = tk.Button(self.root, text="下一个", command=self.show_next_card)
        self.next_button.grid(row=2, column=2, padx=10, pady=10)

        self.add_card_button = tk.Button(self.root, text="添加新卡片", command=self.add_new_card)
        self.add_card_button.grid(row=0, column=2, padx=10, pady=10)

        self.card_selector.bind("<<ComboboxSelected>>", self.on_card_selected)
        self.card_display.bind("<Button-1>", self.flip_card)
        
        # 添加显示卡片背面的按钮
        self.flip_button = tk.Button(self.root, text="显示背面", command=self.flip_card)
        self.flip_button.grid(row=3, column=1, padx=10, pady=10)

    def flip_card(self, event=None):
        if self.cards:
            self.showing_front = not self.showing_front
            self.update_card_display(show_front=self.showing_front)

    def update_card_display(self, show_front=True):
        if self.cards:
            card = self.cards[self.current_card_index]
            self.card_display['text'] = card['front'] if show_front else card['back']
            # Update the button text based on the side of the card being displayed
            self.flip_button['text'] = "显示正面" if not show_front else "显示背面"

    def show_prev_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index - 1) % len(self.cards)
            self.update_card_display()

    def show_next_card(self):
        if self.cards:
            self.current_card_index = (self.current_card_index + 1) % len(self.cards)
            self.update_card_display()

    def add_new_card(self):
        front = simpledialog.askstring("新卡片正面", "请输入卡片正面内容:")
        back = simpledialog.askstring("新卡片反面", "请输入卡片反面内容:")
        if front and back:
            new_card = {"front": front, "back": back}
            self.cards.append(new_card)
            self.save_cards()
            messagebox.showinfo("成功", "卡片添加成功！")
            self.card_selector['values'] = [card['front'] for card in self.cards]

    def on_card_selected(self, event):
        self.current_card_index = self.card_selector.current()
        self.update_card_display()

    def load_cards(self):
        try:
            if os.path.exists("./wordcards.json"):
                with open("./wordcards.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return data.get("cards", [])
            else:
                return []
        except Exception as e:
            messagebox.showerror("错误", f"加载卡片失败: {e}")
            return []

    def save_cards(self):
        try:
            with open("./wordcards.json", "w", encoding="utf-8") as file:
                json.dump({"cards": self.cards}, file, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存卡片失败: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordcardApp(root)
    app.run()
