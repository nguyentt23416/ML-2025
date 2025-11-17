import os
import sys
import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
import DashboardFunction as dbf
import subprocess


def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)


# --- HÀM CẬP NHẬT BẢNG ---
def update_table(func_logic):
    data = func_logic()

    if isinstance(data, str):
        print(data)
        return

    # Xóa dữ liệu cũ
    for item in tree.get_children():
        tree.delete(item)

    # Cập nhật cột
    columns = list(data.columns)
    tree["columns"] = columns

    # --- TÍNH TOÁN ĐỘ RỘNG CỘT (Tổng chiều rộng ~ 885px) ---
    # Kiểm tra xem có cột Giá hay không để chia lại đất cho cột Mô tả
    has_price = "Giá/Sản phẩm" in columns

    for col in columns:
        tree.heading(col, text=col)

        if "Tên" in col:
            # Tên sản phẩm: 220px (Đủ dài)
            tree.column(col, width=220, minwidth=150, anchor="w")

        elif "Mã" in col:
            # Mã SP: 70px
            tree.column(col, width=70, minwidth=50, anchor="center")

        elif "Size" in col:
            # Size: 50px
            tree.column(col, width=50, minwidth=40, anchor="center")

        elif col in ["Tồn Kho", "SL đã bán", "Hàng hóa sắp hết"]:
            # Cột Số lượng: 120px (Mở rộng để chứa đủ chữ "Hàng hóa sắp hết")
            tree.column(col, width=120, minwidth=80, anchor="center")

        elif "Giá" in col:
            # Giá: 100px (Chỉ hiện khi bấm nút Xanh Dương)
            tree.column(col, width=100, minwidth=80, anchor="center")

        elif "Mô Tả" in col:
            # Mô tả: Tự động co giãn
            # Nếu có Giá: 885 - (220+70+50+120+100) = 325px
            # Nếu ko Giá: 885 - (220+70+50+120) = 425px
            desc_width = 325 if has_price else 425
            tree.column(col, width=desc_width, minwidth=200, anchor="w")

    # Đổ dữ liệu vào bảng
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))


# Wrapper functions
def on_click_blue():
    threading.Thread(target=lambda: update_table(dbf.get_total_products_df)).start()


def on_click_green():
    threading.Thread(target=lambda: update_table(dbf.get_sold_products_df)).start()


def on_click_red():
    threading.Thread(target=lambda: update_table(dbf.get_running_out_products_df)).start()


# Navigation functions
def open_management():
    window.destroy()
    subprocess.Popen([sys.executable, "management.py"])


def open_prediction():
    window.destroy()
    subprocess.Popen([sys.executable, "prediction.py"])


def open_login():
    window.destroy()
    subprocess.Popen([sys.executable, "login.py"])


def open_statistic():
    # Already in statistic, do nothing or refresh
    pass


# --- GIAO DIỆN CHÍNH ---
window = tk.Tk()
window.geometry("1280x720")
window.configure(bg="#ffffff")
window.title("Machine Learning UI - Statistic")

canvas = tk.Canvas(
    window,
    bg="#ffffff",
    width=1280,
    height=720,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load nền
try:
    image_1 = tk.PhotoImage(file=load_asset("frame_3/1.png"))
    canvas.create_image(640, 360, image=image_1)
except:
    pass

# =================================================================
# TIÊU ĐỀ "STATISTIC" TRÊN NÚT SỐ 2
# =================================================================
canvas.create_text(
    750, 75,  # Thẳng hàng nút giữa
    text="STATISTIC",
    fill="#ffffff",
    font=("Arial", 54, "bold"),
    anchor="center"
)

# --- CẤU HÌNH BẢNG ---
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#2c2c2c",
                foreground="white",
                fieldbackground="#2c2c2c",
                rowheight=30,
                font=("Arial", 11))

style.configure("Treeview.Heading",
                font=("Arial", 11, "bold"),
                background="#4a4a4a",
                foreground="white")

table_frame = tk.Frame(window)
table_frame.place(x=308, y=263, width=885, height=427)

scrollbar_y = tk.Scrollbar(table_frame)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(table_frame, orient='horizontal')
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

tree = ttk.Treeview(table_frame,
                    yscrollcommand=scrollbar_y.set,
                    xscrollcommand=scrollbar_x.set,
                    show="headings")
tree.pack(fill=tk.BOTH, expand=True)

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)

# --- CÁC NÚT BẤM ---
try:
    button_1_image = tk.PhotoImage(file=load_asset("frame_3/2.png"))
    button_1 = tk.Button(
        image=button_1_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        command=on_click_red
    )
    button_1.place(x=930, y=143, width=262, height=79)
except:
    pass

try:
    button_2_image = tk.PhotoImage(file=load_asset("frame_3/3.png"))
    button_2 = tk.Button(
        image=button_2_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        command=on_click_green
    )
    button_2.place(x=619, y=144, width=262, height=76)
except:
    pass

try:
    button_3_image = tk.PhotoImage(file=load_asset("frame_3/4.png"))
    button_3 = tk.Button(
        image=button_3_image,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        command=on_click_blue
    )
    button_3.place(x=308, y=143, width=262, height=79)
except:
    pass

# --- SIDEBAR ---
sidebar_configs = [
    ("frame_2/2.png", 538, open_login, "Log Out"),
    ("frame_2/3.png", 372, open_prediction, "ML Prediction"),
    ("frame_2/4.png", 210, open_management, "Product Management"),
    ("frame_2/5.png", 44, open_statistic, "Dashboard")
]

sidebar_buttons = []
sidebar_images = []

for img_path, y, command, text in sidebar_configs:
    try:
        img = tk.PhotoImage(file=load_asset(img_path))
        btn = tk.Button(
            image=img,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=command
        )
        btn.image = img
        btn.place(x=37, y=y, width=116, height=116)
        sidebar_buttons.append(btn)
        sidebar_images.append(img)  # Keep reference to prevent garbage collection
    except Exception as e:
        print(f"Error loading {img_path}: {e}")

# LABELS
texts = [
    (666, "Log Out"),
    (499, "ML Prediction"),
    (338, "Product Management"),
    (171, "Dashboard")
]
for y, t in texts:
    canvas.create_text(41, y, anchor="nw", text=t, fill="#ffffff", font=("Roboto", 14 * -1))

window.resizable(False, False)
window.mainloop()
