import tkinter as tk
from tkinter import scrolledtext
import random

# ================== MENU DATA (Categorized) ==================
menu = {
    "Fast Food": {
        "pizza": 150,
        "burger": 100,
        "pasta": 120,
        "sandwich": 80,
        "fries": 60,
        "momos": 90,
        "noodles": 110
    },
    "Indian Dishes": {
        "paneer butter masala": 180,
        "chole bhature": 140,
        "rajma rice": 130,
        "biryani": 160,
        "dal makhani": 150,
        "butter naan": 30,
        "roti": 15,
        "veg thali": 200,
        "chicken curry": 190,
        "fish fry": 220
    },
    "Beverages": {
        "coffee": 50,
        "tea": 30,
        "cold coffee": 70,
        "milkshake": 90,
        "lemonade": 40,
        "soft drink": 45,
        "lassi": 60
    },
    "Desserts": {
        "ice cream": 70,
        "brownie": 100,
        "gulab jamun": 50,
        "rasgulla": 50,
        "cake": 120,
        "pastry": 80,
        "kheer": 90
    }
}

order = {}

# ================== HELPER FUNCTION ==================
def calculate_total():
    total = 0
    for item, qty in order.items():
        for cat in menu.values():
            if item in cat:
                total += cat[item] * qty
                break
    return total

# ================== SHOW TOTAL BILL ==================
def show_total_bill():
    chat_window.config(state=tk.NORMAL)

    if not order:
        chat_window.insert(tk.END, "FoodBot: You haven't ordered anything yet.\n\n")
    else:
        total = calculate_total()
        summary = "FoodBot: Here’s your order summary:\n\n"
        for item, qty in order.items():
            for cat in menu.values():
                if item in cat:
                    price = cat[item]
                    summary += f"{item.title()} x{qty} = ₹{price * qty}\n"
                    break
        summary += f"\nTotal Bill: ₹{total}\n\n"
        chat_window.insert(tk.END, summary)

    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# ================== CHATBOT LOGIC ==================
def get_response(user_input):
    user_input = user_input.lower()

    if "menu" in user_input:
        msg = "📋 Here’s our menu:\n\n"
        for category, items in menu.items():
            msg += f"🍽️ {category}:\n"
            for item, price in items.items():
                msg += f"  • {item.title()} - ₹{price}\n"
            msg += "\n"
        msg += "Type 'order pizza' or 'add biryani' to start ordering."
        return msg

    for category, items in menu.items():
        for item, price in items.items():
            if item in user_input:
                order[item] = order.get(item, 0) + 1
                total = calculate_total()
                return f"{item.title()} added to your order.\nCurrent Total: ₹{total}"

    if "total" in user_input or "bill" in user_input:
        if not order:
            return "You haven’t ordered anything yet."
        total = calculate_total()
        summary = "🧾 Here’s your order summary:\n\n"
        for item, qty in order.items():
            for cat in menu.values():
                if item in cat:
                    price = cat[item]
                    summary += f"{item.title()} x{qty} = ₹{price * qty}\n"
                    break
        summary += f"\n💰 Total Bill: ₹{total}\n\nThank you for ordering!"
        return summary

    if "clear" in user_input or "cancel" in user_input:
        order.clear()
        return "Your order has been cleared."

    if "bye" in user_input or "exit" in user_input:
        return "Thanks for visiting. Have a great day."

    responses = [
        "Type 'menu' to see our categories.",
        "You can order something like 'order pizza' or 'add biryani'.",
        "Ask me for your 'total' anytime."
    ]
    return random.choice(responses)

# ================== MESSAGE HANDLER ==================
def send_message():
    user_message = user_input.get().strip()
    if user_message == "":
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_message}\n")

    response = get_response(user_message)
    chat_window.insert(tk.END, f"FoodBot: {response}\n\n")

    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    user_input.set("")

# ================== GUI SETUP ==================
root = tk.Tk()
root.title("🍔 Food Ordering Chatbot")
root.geometry("600x650")
root.resizable(False, False)
root.config(bg="#FFF3E0")

# ================== CHAT DISPLAY ==================
chat_window = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Helvetica", 12),
    bg="white",
    fg="black"
)
chat_window.place(x=20, y=20, width=560, height=470)
chat_window.config(state=tk.DISABLED)

# ================== INPUT FIELD ==================
user_input = tk.StringVar()
entry_box = tk.Entry(
    root,
    textvariable=user_input,
    font=("Helvetica", 12),
    width=32,
    bg="#FFF8E1"
)
entry_box.place(x=20, y=510, height=40)

# ================== BUTTONS ==================
tk.Button(
    root,
    text="Send",
    command=send_message,
    font=("Helvetica", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    width=10
).place(x=470, y=510, height=40)

tk.Button(
    root,
    text="Clear Chat",
    command=lambda: chat_window.config(state=tk.NORMAL) or chat_window.delete("1.0", tk.END) or chat_window.config(state=tk.DISABLED),
    font=("Helvetica", 11, "bold"),
    bg="#f44336",
    fg="white",
    width=12
).place(x=230, y=560, height=30)

tk.Button(
    root,
    text="Total Bill",
    command=show_total_bill,
    font=("Helvetica", 11, "bold"),
    bg="#2196F3",
    fg="white",
    width=12
).place(x=20, y=560, height=30)

# ================== WELCOME MESSAGE ==================
chat_window.config(state=tk.NORMAL)
chat_window.insert(
    tk.END,
    "FoodBot: Hello. I'm your food ordering assistant.\n"
    "Type 'menu' to see our food categories and prices.\n\n"
)
chat_window.config(state=tk.DISABLED)

# ================== RUN APP ==================
root.mainloop()
