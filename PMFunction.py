import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

# --- BIẾN TOÀN CỤC ---
global_tree = None

# --- MÀU SẮC ---
COLOR_NORMAL = "#34414f"  # Màu xám xanh mặc định
COLOR_ERROR = "#990000"  # Màu đỏ báo lỗi


# --- HÀM HỖ TRỢ ---
def parse_product_info(full_string):
    try:
        parts = full_string.split(" - Mã ")
        if len(parts) < 2: return full_string, "", ""
        name_part = parts[0];
        code = parts[1]
        name_size = name_part.rsplit(" size ", 1)
        if len(name_size) < 2: return name_part, "", code
        name = name_size[0];
        size = name_size[1]
        return name, size, code
    except:
        return full_string, "", ""


def reset_colors(*widgets):
    for widget in widgets:
        widget.config(bg=COLOR_NORMAL)


# --- HÀM VALIDATION (KIỂM TRA DỮ LIỆU) ---
def kiem_tra_dau_vao(txt_name, txt_size, txt_code, txt_qty, txt_price):
    # 1. Reset màu về bình thường trước khi kiểm tra
    reset_colors(txt_name, txt_size, txt_code, txt_qty, txt_price)

    # 2. Lấy dữ liệu thô
    val_name = txt_name.get("1.0", "end-1c").strip()
    val_size = txt_size.get("1.0", "end-1c").strip()
    val_code = txt_code.get("1.0", "end-1c").strip()
    val_qty_str = txt_qty.get("1.0", "end-1c").strip()
    val_price_str = txt_price.get("1.0", "end-1c").strip()

    is_valid = True
    error_msg = []

    # 3. Kiểm tra String (Tên, Size, Mã) - Không được để trống
    if not val_name:
        txt_name.config(bg=COLOR_ERROR)
        is_valid = False

    if not val_size:
        txt_size.config(bg=COLOR_ERROR)
        is_valid = False

    if not val_code:
        txt_code.config(bg=COLOR_ERROR)
        is_valid = False

    if not is_valid:
        error_msg.append("- Tên, Size, Mã SP không được để trống.")

    # 4. Kiểm tra Float (Số lượng, Giá) - Phải là số
    val_qty = 0.0
    val_price = 0.0

    # Kiểm tra Số lượng
    try:
        if not val_qty_str: raise ValueError("Empty")
        val_qty = float(val_qty_str)
    except ValueError:
        txt_qty.config(bg=COLOR_ERROR)
        is_valid = False
        error_msg.append("- Số lượng phải là số (Float).")

    # Kiểm tra Giá tiền
    try:
        if not val_price_str: raise ValueError("Empty")
        val_price = float(val_price_str)
    except ValueError:
        txt_price.config(bg=COLOR_ERROR)
        is_valid = False
        error_msg.append("- Giá tiền phải là số (Float).")

    # 5. Tổng kết lỗi
    if not is_valid:
        full_msg = "Dữ liệu không hợp lệ:\n" + "\n".join(error_msg)
        messagebox.showwarning("Lỗi nhập liệu", full_msg)
        return False, None, None, None, None, None

    # Trả về True và các giá trị đã chuẩn hóa
    return True, val_name, val_size, val_code, val_qty, val_price


# --- 1. HIỂN THỊ DỮ LIỆU ---
def hien_thi_du_lieu(window, txt_name, txt_size, txt_code, txt_qty, txt_price):
    global global_tree
    try:
        df = pd.read_csv("dataset/data_1000_fashion_price.csv")
        processed_data = []
        for index, row in df.iterrows():
            p_name, p_size, p_code = parse_product_info(row['Name'])
            processed_data.append({
                "Name": p_name, "Size": p_size, "Code": p_code,
                "Qty": row['quantity'], "Price": row['Price']
            })

        df_new = pd.DataFrame(processed_data)
        cols = ("Name", "Size", "Code", "Qty", "Price")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=30,
                        font=('Roboto', 10))
        style.configure("Treeview.Heading", background="#444444", foreground="white", font=('Roboto', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#0078D7')])

        frame_table = tk.Frame(window, bg="#2b2b2b")
        frame_table.place(x=650, y=160, width=570, height=420)

        scrollbar = tk.Scrollbar(frame_table)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(frame_table, columns=cols, show='headings', yscrollcommand=scrollbar.set)
        global_tree = tree
        scrollbar.config(command=tree.yview)

        tree.heading("Name", text="Tên SP");
        tree.column("Name", width=200, anchor="w")
        tree.heading("Size", text="Size");
        tree.column("Size", width=50, anchor="center")
        tree.heading("Code", text="Mã SP");
        tree.column("Code", width=80, anchor="center")
        tree.heading("Qty", text="SL");
        tree.column("Qty", width=60, anchor="center")
        tree.heading("Price", text="Giá");
        tree.column("Price", width=110, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)

        for item in tree.get_children(): tree.delete(item)
        for index, row in df_new.iterrows():
            formatted_price = "{:,.0f}".format(row['Price'])
            tree.insert("", tk.END, values=(row['Name'], row['Size'], row['Code'], row['Qty'], formatted_price))

    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi: {e}")


# --- 2. ĐỌC DỮ LIỆU (READ) ---
def doc_du_lieu(txt_name, txt_size, txt_code, txt_qty, txt_price):
    global global_tree
    if global_tree is None: return

    try:
        selected_items = global_tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng trong bảng!")
            return

        item = selected_items[0]
        values = global_tree.item(item, "values")

        reset_colors(txt_name, txt_size, txt_code, txt_qty, txt_price)

        txt_name.delete("1.0", tk.END);
        txt_name.insert(tk.END, values[0])
        txt_size.delete("1.0", tk.END);
        txt_size.insert(tk.END, values[1])
        txt_code.delete("1.0", tk.END);
        txt_code.insert(tk.END, values[2])
        txt_qty.delete("1.0", tk.END);
        txt_qty.insert(tk.END, values[3])
        txt_price.delete("1.0", tk.END);
        txt_price.insert(tk.END, str(values[4]).replace(",", ""))

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi đọc: {e}")


# --- 3. THÊM SẢN PHẨM (CREATE) ---
def them_san_pham(window, txt_name, txt_size, txt_code, txt_qty, txt_price):
    # GỌI HÀM KIỂM TRA
    is_valid, val_name, val_size, val_code, val_qty, val_price = kiem_tra_dau_vao(
        txt_name, txt_size, txt_code, txt_qty, txt_price
    )

    if not is_valid: return  # Dừng nếu lỗi

    try:
        df = pd.read_csv("dataset/data_1000_fashion_price.csv")
        for full_name_db in df['Name']:
            _, _, code_db = parse_product_info(full_name_db)
            if code_db == val_code:
                txt_code.config(bg=COLOR_ERROR)
                messagebox.showwarning("Trùng lặp", "Mã SP bị trùng!")
                return

        full_name_new = f"{val_name} size {val_size} - Mã {val_code}"
        new_row = pd.DataFrame({
            'Name': [full_name_new], 'quantity': [val_qty],
            'Price': [val_price], 'avg_monthly_quantity': [0]
        })
        df_updated = pd.concat([df, new_row], ignore_index=True)
        df_updated.to_csv("dataset/data_1000_fashion_price.csv", index=False)

        messagebox.showinfo("Thành công", "Đã thêm sản phẩm mới!")
        hien_thi_du_lieu(window, txt_name, txt_size, txt_code, txt_qty, txt_price)
        for w in [txt_name, txt_size, txt_code, txt_qty, txt_price]: w.delete("1.0", tk.END)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {e}")


# --- 4. XÓA SẢN PHẨM (DELETE) ---
def xoa_san_pham(txt_name, txt_size, txt_code, txt_qty, txt_price):
    global global_tree
    if global_tree is None: return
    selected_items = global_tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
        return

    if not messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa không?"): return

    try:
        item = selected_items[0]
        values = global_tree.item(item, "values")
        target_code = values[2]

        df = pd.read_csv("dataset/data_1000_fashion_price.csv")
        indices_to_drop = []
        for index, row in df.iterrows():
            _, _, code_db = parse_product_info(row['Name'])
            if code_db == target_code:
                indices_to_drop.append(index)

        if indices_to_drop:
            df.drop(indices_to_drop, inplace=True)
            df.to_csv("dataset/data_1000_fashion_price.csv", index=False)
            global_tree.delete(item)
            for w in [txt_name, txt_size, txt_code, txt_qty, txt_price]: w.delete("1.0", tk.END)
            reset_colors(txt_name, txt_size, txt_code, txt_qty, txt_price)
            messagebox.showinfo("Thành công", "Đã xóa!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {e}")


# --- 5. CẬP NHẬT SẢN PHẨM (UPDATE) ---
def cap_nhat_san_pham(window, txt_name, txt_size, txt_code, txt_qty, txt_price):
    global global_tree
    if global_tree is None: return
    selected_items = global_tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật!")
        return

    # GỌI HÀM KIỂM TRA DỮ LIỆU MỚI
    is_valid, new_name, new_size, new_code, new_qty, new_price = kiem_tra_dau_vao(
        txt_name, txt_size, txt_code, txt_qty, txt_price
    )

    if not is_valid: return  # Dừng nếu lỗi

    # Lấy Mã Code CŨ
    item = selected_items[0]
    old_values = global_tree.item(item, "values")
    old_code = old_values[2]

    if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn cập nhật không?"): return

    try:
        df = pd.read_csv("dataset/data_1000_fashion_price.csv")

        # Kiểm tra trùng mã (Trừ chính nó)
        is_duplicate = False
        for index, row in df.iterrows():
            _, _, code_db = parse_product_info(row['Name'])
            if code_db == new_code and code_db != old_code:
                is_duplicate = True
                break

        if is_duplicate:
            if not messagebox.askyesno("Cảnh báo trùng mã",
                                       f"Mã '{new_code}' đã tồn tại.\nTiếp tục giữ nguyên mã này?"):
                txt_code.config(bg=COLOR_ERROR)
                return

        updated_count = 0
        for index, row in df.iterrows():
            _, _, code_db = parse_product_info(row['Name'])
            if code_db == old_code:
                full_name_updated = f"{new_name} size {new_size} - Mã {new_code}"
                df.at[index, 'Name'] = full_name_updated
                df.at[index, 'quantity'] = new_qty
                df.at[index, 'Price'] = new_price
                updated_count += 1

        if updated_count > 0:
            df.to_csv("dataset/data_1000_fashion_price.csv", index=False)
            messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")
            hien_thi_du_lieu(window, txt_name, txt_size, txt_code, txt_qty, txt_price)
            for w in [txt_name, txt_size, txt_code, txt_qty, txt_price]: w.delete("1.0", tk.END)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm gốc!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}")