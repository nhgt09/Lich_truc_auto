import tkinter as tk
from tkinter import ttk, Menu, LabelFrame, filedialog, messagebox
from docx import Document
import json, os

# ====================== HẰNG SỐ ======================
TAP_TIN_CAU_HINH = "setting.json"
CAC_THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]

# ====================== DỮ LIỆU TOÀN CỤC ======================
DATA_HS = {}   # {"Tổ 1": [{"ten": ..., "gioi_tinh": ...}, ...], ...}
WIDGETS = {}   # để lưu các widget cần cập nhật (combobox học sinh,...)

bien_to = None
bien_ngay = None
menu_ngay = None
combobox_hs = None
hs_truc_to= None

so_ngay_gh = 0

ds_truc_to= [] #này là tổ trực
ds_hs = []# này là học sinh thêm 

# ====================== HÀM CẤU HÌNH ======================
def tai_cau_hinh():
    """Đọc file cấu hình JSON."""
    if os.path.exists(TAP_TIN_CAU_HINH):
        try:
            with open(TAP_TIN_CAU_HINH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def luu_cau_hinh(cau_hinh):
    """Lưu cấu hình ra file JSON."""
    with open(TAP_TIN_CAU_HINH, "w", encoding="utf-8") as f:
        json.dump(cau_hinh, f, ensure_ascii=False, indent=2)

# ====================== HÀM LÀM VIỆC VỚI FILE ======================
def trich_xuat_file_json(duong_dan="danhsach.json"):
    """Đọc dữ liệu từ file JSON (giả sử đã được tạo từ Word)."""
    global DATA_HS
    if not os.path.exists(duong_dan):
        return {}
    with open(duong_dan, "r", encoding="utf-8") as f:
        DATA_HS = json.load(f)
    return DATA_HS

def mo_file_word():
    """Chọn và đọc nội dung file Word."""
    duong_dan = filedialog.askopenfilename(
        title="Chọn file Word", filetypes=[("Word files", "*.docx")]
    )
    if not duong_dan:
        return
    try:
        doc = Document(duong_dan)
        _ = [para.text for para in doc.paragraphs]  # chỉ đọc, chưa dùng
        messagebox.showinfo("Thành công", "Đọc file Word thành công")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không đọc được file:\n{e}")

def chon_thu_muc_xuat(cau_hinh):
    """Chọn thư mục để lưu file export."""
    thu_muc = filedialog.askdirectory(title="Chọn thư mục xuất file")
    if thu_muc:
        messagebox.showinfo("Đã chọn", thu_muc)
        cau_hinh["thu_muc_xuat"] = thu_muc
        luu_cau_hinh(cau_hinh)
        return thu_muc
    else:
        messagebox.showwarning("Chưa chọn", "Bạn chưa chọn thư mục nào")
        return None

# ====================== HÀM XỬ LÝ NGÀY ======================
def cap_nhat_menu_ngay(menu_ngay, bien_ngay, so_ngay):
    """Cập nhật OptionMenu số ngày trực dựa theo khoảng ngày đã chọn."""
    menu = menu_ngay["menu"]
    menu.delete(0, "end")
    for i in range(1, so_ngay + 1):
        menu.add_command(label=str(i), command=lambda v=i: bien_ngay.set(str(v)))
    bien_ngay.set("1")

def cua_so_chon_khoang_ngay(root, menu_ngay, bien_ngay, cau_hinh):
    """Hiển thị cửa sổ chọn khoảng ngày trực."""
    top = tk.Toplevel(root)
    top.title("Chọn khoảng ngày trực")
    top.geometry("300x250")

    # Lấy giá trị đã lưu
    if "khoang_ngay" in cau_hinh:
        ngay_bat_dau, ngay_ket_thuc = cau_hinh["khoang_ngay"]
    else:
        ngay_bat_dau, ngay_ket_thuc = CAC_THU_TRONG_TUAN[0], CAC_THU_TRONG_TUAN[-1]

    bien_ngay_bat_dau = tk.StringVar(value=ngay_bat_dau)
    bien_ngay_ket_thuc = tk.StringVar(value=ngay_ket_thuc)

    tk.Label(top, text="Từ:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.OptionMenu(top, bien_ngay_bat_dau, ngay_bat_dau, *CAC_THU_TRONG_TUAN).grid(
        row=0, column=1, padx=10, pady=10, sticky="ew"
    )

    tk.Label(top, text="Đến:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ttk.OptionMenu(top, bien_ngay_ket_thuc, ngay_ket_thuc, *CAC_THU_TRONG_TUAN).grid(
        row=1, column=1, padx=10, pady=10, sticky="ew"
    )

    def xac_nhan():
        bat_dau = bien_ngay_bat_dau.get()
        ket_thuc = bien_ngay_ket_thuc.get()
        i_bat_dau = CAC_THU_TRONG_TUAN.index(bat_dau)
        i_ket_thuc = CAC_THU_TRONG_TUAN.index(ket_thuc)

        if i_bat_dau <= i_ket_thuc:
            global so_ngay_gh
            so_ngay_gh = i_ket_thuc - i_bat_dau + 1
            messagebox.showinfo("Khoảng ngày trực", f"Từ {bat_dau} đến {ket_thuc}\n=> {so_ngay_gh} ngày")
            cap_nhat_menu_ngay(menu_ngay, bien_ngay, so_ngay_gh)
            cau_hinh["khoang_ngay"] = [bat_dau, ket_thuc]
            luu_cau_hinh(cau_hinh)
            top.destroy()
        else:
            messagebox.showwarning("Không hợp lệ", "Ngày bắt đầu phải trước hoặc bằng ngày kết thúc!")

    ttk.Button(top, text="Xác nhận", command=xac_nhan).grid(row=2, column=0, columnspan=2, pady=15)
    top.grid_columnconfigure(1, weight=1)

# ====================== HÀM XỬ LÍ HỌC SINH ======================
def cap_nhat_hoc_sinh_theo_to(ten_to):
    """Cập nhật danh sách học sinh = toàn bộ học sinh của tất cả tổ."""
    if not DATA_HS:
        trich_xuat_file_json()  # load dữ liệu từ test.json nếu chưa có
    # gom toàn bộ học sinh của tất cả tổ
    ds_hs = []
    for to, hs_list in DATA_HS.items():
        for hs in hs_list:
            ds_hs.append(hs["ten"])
    if "combobox_hs" in WIDGETS:
        WIDGETS["combobox_hs"].lua_chon = ds_hs
        WIDGETS["combobox_hs"].cap_nhat_listbox(ds_hs)
def xac_nhan_to():
    global bien_to,ds_truc_to
    to= bien_to.get()
    for hs in DATA_HS.get(to,[]):
        ds_truc_to.append({'ten':hs['ten'],'gioi_tinh': hs['gioi_tinh']})
def xac_nhan_hs():
    global bien_ngay, combobox_hs,ds_hs,so_ngay_gh,WIDGETS
    hs_dc_chon = WIDGETS["combobox_hs"].o_nhap.get().strip()
    so_ngay = int(bien_ngay.get())

    thong_tin_hs = None
    if len(hs_dc_chon) == 0:
        messagebox.showerror("Lỗi!",f"Vui lòng nhập hoặc để trống phần chọn học sinh")
        return
    for to, danh_s in DATA_HS.items():
        for hs in danh_s:
            if hs['ten'] == hs_dc_chon:
                thong_tin_hs = hs
                break
        if thong_tin_hs:
            break
    if not thong_tin_hs:
        messagebox.showerror("Lỗi!",f"Không tìm thấy tên:{thong_tin_hs}")
        return
    for hs in ds_hs:
        if hs["ten"] == thong_tin_hs["ten"] and hs["gioi_tinh"] == thong_tin_hs["gioi_tinh"]:
            hs["ngay_truc"] = so_ngay
            messagebox.showinfo("Cập nhật thêm ngày trực",f"Đã cập nhật ngày trực của {hs['ten']} thành {hs['ngay_truc']} ngày")
            return
    ds_hs.append({"ten": thong_tin_hs["ten"], "gioi_tinh": thong_tin_hs["gioi_tinh"], "ngay_truc": so_ngay})

def sap_xep():
    print(ds_hs)
    print(ds_truc_to)



# ====================== COMBOBOX TÌM KIẾM ======================
class HopChonCoTimKiem(tk.Frame):
    """Combobox có ô tìm kiếm (custom)."""

    def __init__(self, master, lua_chon, **kwargs):
        super().__init__(master, **kwargs)
        self.lua_chon = lua_chon
        self.dropdown_visible = False

        # Ô nhập + nút
        khung_tren = tk.Frame(self)
        khung_tren.pack(fill="x")

        self.o_nhap = tk.Entry(khung_tren, width=24)
        self.o_nhap.pack(side=tk.LEFT, fill="x", expand=True)
        self.o_nhap.bind("<KeyRelease>", self.loc_danh_sach)
        self.o_nhap.bind("<FocusIn>", self.hien_dropdown)

        tk.Button(khung_tren, text="▼", command=self.chuyen_trang_thai, width=2).pack(side=tk.LEFT)

        # Listbox
        self.khung_listbox = tk.Frame(self)
        self.listbox = tk.Listbox(self.khung_listbox, height=5, width=24)
        self.listbox.pack(fill="x")
        self.listbox.bind("<<ListboxSelect>>", self.chon_item)

        self.cap_nhat_listbox(self.lua_chon)

    def cap_nhat_listbox(self, data):
        self.listbox.delete(0, tk.END)
        for item in data:
            self.listbox.insert(tk.END, item)

    def loc_danh_sach(self, event=None):
        tu_khoa = self.o_nhap.get().lower()
        data = [item for item in self.lua_chon if tu_khoa in item.lower()] if tu_khoa else self.lua_chon
        self.cap_nhat_listbox(data)
        self.hien_dropdown()

    def chon_item(self, event=None):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        gia_tri = self.listbox.get(index)
        self.o_nhap.delete(0, tk.END)
        self.o_nhap.insert(0, gia_tri)
        self.an_dropdown()

    def hien_dropdown(self, event=None):
        if not self.dropdown_visible:
            self.khung_listbox.pack(fill="x", pady=2)
            self.dropdown_visible = True

    def an_dropdown(self):
        if self.dropdown_visible:
            self.khung_listbox.pack_forget()
            self.dropdown_visible = False

    def chuyen_trang_thai(self):
        if self.dropdown_visible:
            self.an_dropdown()
        else:
            self.hien_dropdown()

# ====================== MAIN ======================
def main():
    global bien_to, bien_ngay, menu_ngay, combobox_hs

    root = tk.Tk()
    root.title("Phần mềm phân công lịch trực")
    root.state("zoomed")

    # Load config
    cau_hinh = tai_cau_hinh()
    thu_muc_xuat = cau_hinh.get("thu_muc_xuat", "")

    # Load dữ liệu học sinh từ JSON
    trich_xuat_file_json()

    # Khung chính
    khung_chinh = tk.Frame(root)
    khung_chinh.pack(fill="both", expand=True)

    # ===== Khung lịch trực =====
    khung_lich = tk.Frame(khung_chinh, bg="#f0f0f0", relief="sunken", bd=2)
    khung_lich.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(khung_lich, text="Xem trước lịch trực", bg="#f0f0f0").pack(expand=True)

    # ===== Khung điều khiển =====
    khung_dieu_khien = tk.Frame(khung_chinh, relief="groove", bd=2)
    khung_dieu_khien.pack(side="right", fill="y", padx=10, pady=10)

    # ---- Chọn tổ ----
    khung_to = LabelFrame(khung_dieu_khien, text="Chọn tổ", padx=10, pady=10)
    khung_to.pack(fill="x", pady=10)

    cac_to = list(DATA_HS.keys()) if DATA_HS else ["Tổ 1", "Tổ 2"]
    bien_to = tk.StringVar(value=cac_to[0])
    ttk.OptionMenu(khung_to, bien_to, "Chọn tổ", *cac_to,
                   command=lambda v: cap_nhat_hoc_sinh_theo_to(v)).pack(fill="x", pady=5)
    tk.Button(khung_to, text="Xác nhận tổ",command=xac_nhan_to).pack(fill="x", pady=5)

    # ---- Chọn học sinh ----
    khung_hs = LabelFrame(khung_dieu_khien, text="Chọn học sinh", padx=10, pady=10)
    khung_hs.pack(fill="x", pady=10)

    combobox_hs = HopChonCoTimKiem(khung_hs, lua_chon=[])
    combobox_hs.pack(fill="x", pady=5)
    WIDGETS["combobox_hs"] = combobox_hs

    tk.Label(khung_hs, text="Số ngày trực:").pack(anchor="w", pady=5)
    bien_ngay = tk.StringVar(value="1")
    menu_ngay = ttk.OptionMenu(khung_hs, bien_ngay, "1", "1")
    menu_ngay.pack(fill="x", pady=5)
    tk.Button(khung_hs, text="Xác nhận học sinh",command=xac_nhan_hs).pack(fill="x", pady=5)

    # ---- Các nút dưới ----
    khung_duoi = tk.Frame(khung_dieu_khien)
    khung_duoi.pack(side="bottom", fill="x", pady=10)
    tk.Button(khung_duoi, text="Chạy thử",command=sap_xep).pack(fill="x", pady=5)
    tk.Button(khung_duoi, text="Chỉnh sửa").pack(fill="x", pady=5)
    tk.Button(khung_duoi, text="Xác nhận Export").pack(fill="x", pady=5)

    # ===== MENU =====
    menubar = Menu(root)

    # File
    menu_file = Menu(menubar, tearoff=0)
    menu_file.add_command(label="Đọc file Word…", command=mo_file_word)
    menu_file.add_command(label="Chọn thư mục Export…", command=lambda: chon_thu_muc_xuat(cau_hinh))
    menubar.add_cascade(label="File", menu=menu_file)

    # Cài đặt
    menu_caidat = Menu(menubar, tearoff=0)
    menu_caidat.add_command(
        label="Khoảng ngày trực",
        command=lambda: cua_so_chon_khoang_ngay(root, menu_ngay, bien_ngay, cau_hinh),
    )
    menubar.add_cascade(label="Cài đặt", menu=menu_caidat)

    # Hướng dẫn
    menu_huongdan = Menu(menubar, tearoff=0)
    menu_huongdan.add_command(label="Xem hướng dẫn…")
    menubar.add_cascade(label="Hướng dẫn", menu=menu_huongdan)

    # About
    menu_about = Menu(menubar, tearoff=0)
    menu_about.add_command(label="Thông tin phần mềm")
    menubar.add_cascade(label="About", menu=menu_about)

    root.config(menu=menubar)
    
    # ---- Load khoảng ngày từ config ----
    if "khoang_ngay" in cau_hinh:
        bat_dau, ket_thuc = cau_hinh["khoang_ngay"]
        i_bat_dau = CAC_THU_TRONG_TUAN.index(bat_dau)
        i_ket_thuc = CAC_THU_TRONG_TUAN.index(ket_thuc)
        if i_bat_dau <= i_ket_thuc:
            cap_nhat_menu_ngay(menu_ngay, bien_ngay, i_ket_thuc - i_bat_dau + 1)

    # Cập nhật học sinh lần đầu theo tổ mặc định
    cap_nhat_hoc_sinh_theo_to(bien_to.get())

    root.mainloop()

if __name__ == "__main__":
    main()
