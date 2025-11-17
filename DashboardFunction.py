import os
import pandas as pd
import threading
import re

# =================================================================================
# CẤU HÌNH ĐƯỜNG DẪN FILE DỮ LIỆU CSV
# =================================================================================
CSV_PATH = 'dataset/data_1000_fashion_price.csv'

df_global = None


# =================================================================================
# HÀM LOAD VÀ XỬ LÝ DỮ LIỆU (TÁCH CỘT)
# =================================================================================
def load_data_if_needed():
    global df_global
    if df_global is not None:
        return None, True

    try:
        if not os.path.exists(CSV_PATH):
            return f"LỖI: Không tìm thấy file '{CSV_PATH}'", False

        # Đọc file CSV
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        df.columns = df.columns.str.strip()

        # --- TÁCH CỘT NAME THÀNH 3 PHẦN ---
        name_col = 'Name' if 'Name' in df.columns else 'name'

        if name_col in df.columns:
            # Regex tách: Tên - Size - Mã
            split_data = df[name_col].str.extract(r'^(.*?) size (.*?) - Mã (.*)$', flags=re.IGNORECASE)

            df['RealName'] = split_data[0].fillna(df[name_col])
            df['Size'] = split_data[1].fillna('-')
            df['Code'] = split_data[2].fillna('-')
        else:
            return "Lỗi: Không tìm thấy cột 'Name'", False

        df_global = df
        return "Thành công", True
    except Exception as e:
        return f"Lỗi: {str(e)}", False


# =================================================================================
# HÀM BỔ TRỢ FORMAT
# =================================================================================
def format_data(df_input, qty_label="Tồn Kho", show_price=False):
    """
    Hàm này dùng để chọn cột và đặt tên cột linh hoạt
    qty_label: Tên hiển thị của cột số lượng (Tồn kho / SL đã bán / Hàng sắp hết)
    show_price: Có hiển thị cột giá hay không
    """
    qty_col = 'Quantity' if 'Quantity' in df_input.columns else 'quantity'
    desc_col = 'Description' if 'Description' in df_input.columns else 'description'
    price_col = 'Price' if 'Price' in df_input.columns else 'price'

    # Danh sách cột cơ bản
    cols = ['RealName', 'Code', 'Size', qty_col, desc_col]

    # Nếu cần hiện giá thì thêm vào cuối
    if show_price:
        cols.append(price_col)

    # Lọc các cột tồn tại
    valid_cols = [c for c in cols if c in df_input.columns]
    final_df = df_input[valid_cols].copy()

    # Map tên cột sang tiếng Việt
    rename_map = {
        'RealName': 'Tên Sản Phẩm',
        'Code': 'Mã SP',
        'Size': 'Size',
        qty_col: qty_label,  # Tên cột số lượng thay đổi theo nút bấm
        desc_col: 'Mô Tả',
        price_col: 'Giá/Sản phẩm'
    }

    return final_df.rename(columns=rename_map)


# =================================================================================
# CÁC HÀM XỬ LÝ LOGIC CHO TỪNG NÚT
# =================================================================================

# 1. NÚT XANH DA TRỜI: TỔNG SỐ (HIỆN GIÁ, TÊN CỘT LÀ TỒN KHO)
def get_total_products_df():
    err, success = load_data_if_needed()
    if not success: return err

    # Hiển thị giá = True, Tên cột = "Tồn Kho"
    return format_data(df_global, qty_label="Tồn Kho", show_price=True)


# 2. NÚT XANH LÁ: ĐÃ BÁN (ẨN GIÁ, TÊN CỘT LÀ SL ĐÃ BÁN)
def get_sold_products_df():
    err, success = load_data_if_needed()
    if not success: return err

    df = df_global.copy()
    qty_col = 'Quantity' if 'Quantity' in df.columns else 'quantity'

    # Lọc hàng > 50 (Giả lập hàng bán chạy)
    filtered_df = df[df[qty_col] > 50].sort_values(by=qty_col, ascending=False)

    # Hiển thị giá = False, Tên cột = "SL đã bán"
    return format_data(filtered_df, qty_label="SL đã bán", show_price=False)


# 3. NÚT ĐỎ: SẮP HẾT (ẨN GIÁ, TÊN CỘT LÀ HÀNG HÓA SẮP HẾT)
def get_running_out_products_df():
    err, success = load_data_if_needed()
    if not success: return err

    df = df_global.copy()
    qty_col = 'Quantity' if 'Quantity' in df.columns else 'quantity'

    # Lọc hàng từ 0 đến 100
    filtered_df = df[(df[qty_col] >= 0) & (df[qty_col] <= 100)]
    sorted_df = filtered_df.sort_values(by=qty_col, ascending=True)

    # Hiển thị giá = False, Tên cột = "Hàng hóa sắp hết"
    return format_data(sorted_df, qty_label="Hàng hóa sắp hết", show_price=False)