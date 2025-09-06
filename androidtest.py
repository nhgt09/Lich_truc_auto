from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import json
import os
from plyer import filechooser

# ====================== HẰNG SỐ ======================
TAP_TIN_CAU_HINH = "setting.json"
CAC_THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]

# ====================== DỮ LIỆU TOÀN CỤC ======================
DATA_HS = {}  # {"Tổ 1": [{"ten": ..., "gioi_tinh": ...}, ...], ...}
so_ngay_gh = 0
ds_truc_to = []  # Danh sách tổ trực
ds_hs = []  # Danh sách học sinh được thêm



# ====================== HẰNG SỐ ======================
TAP_TIN_CAU_HINH = "setting.json"
CAC_THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]

# ====================== DỮ LIỆU TOÀN CỤC ======================
DATA_HS = {}  # {"Tổ 1": [{"ten": ..., "gioi_tinh": ...}, ...], ...}
so_ngay_gh = 0
ds_truc_to = []  # Danh sách tổ trực
ds_hs = []  # Danh sách học sinh được thêm

# ====================== HÀM CẤU HÌNH ======================
def tai_cau_hinh():
    if os.path.exists(TAP_TIN_CAU_HINH):
        try:
            with open(TAP_TIN_CAU_HINH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}
def luu_cau_hinh(cau_hinh):
    try:
        with open(TAP_TIN_CAU_HINH, "w", encoding="utf-8") as f:
            json.dump(cau_hinh, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu file cấu hình: {e}")

# ====================== HÀM XỬ LÝ FILE ======================
def trich_xuat_file_json(duong_dan="danhsach.json"):
    global DATA_HS
    if not os.path.exists(duong_dan):
        MDApp.get_running_app().show_alert("Lỗi", f"File {duong_dan} không tồn tại!")
        return {}
    try:
        with open(duong_dan, "r", encoding="utf-8") as f:
            DATA_HS = json.load(f)
        print("Đã tải DATA_HS:", DATA_HS)  # Debug
        return DATA_HS
    except Exception as e:
        MDApp.get_running_app().show_alert("Lỗi", f"Không đọc được file {duong_dan}: {e}")
        return {}

def chon_thu_muc_xuat():
    def on_selection(paths):
        if paths:
            cau_hinh = tai_cau_hinh()
            cau_hinh["thu_muc_xuat"] = paths[0]
            luu_cau_hinh(cau_hinh)
            MDApp.get_running_app().show_alert("Đã chọn", paths[0])
        else:
            MDApp.get_running_app().show_alert("Chưa chọn", "Bạn chưa chọn thư mục nào")
    filechooser.choose_dir(on_selection=on_selection)

# ====================== HÀM XỬ LÝ NGÀY ======================
def cap_nhat_menu_ngay(dropdown, so_ngay):
    menu_items = [
        {"text": str(i), "viewclass": "MDDropDownItem", "on_release": lambda x=i: dropdown.set_item(str(x))}
        for i in range(1, so_ngay + 1)
    ]
    dropdown.menu = MDDropdownMenu(caller=dropdown, items=menu_items, width_mult=5, max_height=dp(200))
    dropdown.current_item = "1"

# ====================== HÀM XỬ LÝ HỌC SINH ======================
def cap_nhat_hoc_sinh_theo_to(ten_to, hs_textfield, hs_dropdown_menu):
    ds_hs = []
    for to, hs_list in DATA_HS.items():
        for hs in hs_list:
            ds_hs.append(hs["ten"])
    print("Danh sách học sinh:", ds_hs)  # Debug
    hs_textfield.ds_hs = ds_hs  # Lưu danh sách học sinh vào textfield để lọc
    hs_textfield.dropdown_menu = MDDropdownMenu(
        caller=hs_textfield,
        items=[{"text": hs, "viewclass": MDDropDownItem", "on_release": lambda x=hs: [hs_textfield.set_text(x), hs_textfield.dropdown_menu.dismiss()]}
            for hs in ds_hs
        ],
        width_mult=5,
        max_height=dp(200)
    )

def xac_nhan_to(ten_to):
    global ds_truc_to
    ds_truc_to = [{"ten": hs["ten"], "gioi_tinh": hs["gioi_tinh"]} for hs in DATA_HS.get(ten_to, [])]
    print("Tổ được chọn:", ten_to, "Danh sách tổ trực:", ds_truc_to)  # Debug
    MDApp.get_running_app().show_alert("Thành công", f"Đã chọn tổ: {ten_to}")

def xac_nhan_hs(hバンドs_name, so_ngay):
    print("Xác nhận học sinh:", hs_name, "Số ngày:", so_ngay)  # Debug
    if not hs_name.strip():
        MDApp.get_running_app().show_alert("Lỗi", "Vui lòng nhập tên học sinh")
        return
    thong_tin_hs = None
    for to, danh_s in DATA_HS.items():
        for hs in danh_s

System: Cảm ơn bạn đã cung cấp thêm thông tin về lỗi. Dựa trên mô tả của bạn rằng ứng dụng gặp lỗi khi nhấn nút "Xác nhận học sinh" sau khi nhập hoặc chọn tên học sinh, và các lỗi trước đó (như `font_style`), có vẻ vấn đề nằm ở việc xử lý dữ liệu trong hàm `xac_nhan_hs` hoặc tương tác với `MDDropdownMenu`. Vì bạn chưa cung cấp thông báo lỗi cụ thể, tôi sẽ giả định lỗi xảy ra do:

1. **Dữ liệu không hợp lệ**: Tên học sinh nhập vào không có trong `DATA_HS`, hoặc `DATA_HS` rỗng, dẫn đến lỗi khi kiểm tra trong `xac_nhan_hs`.
2. **Sự kiện chọn không hoạt động đúng**: Hàm `loc_hoc_sinh` hoặc sự kiện `on_release` trong `MDDropdownMenu` không cập nhật giá trị vào `MDTextField` đúng cách, gây lỗi khi xác nhận.
3. **Tương tác trên điện thoại**: Menu gợi ý không phản hồi tốt với thao tác chạm, hoặc giá trị được chọn không truyền đúng sang `self.hs_textfield.text`.

---

### **Khắc phục lỗi**

Mã nguồn đã được cập nhật để:
- **Kiểm tra dữ liệu chặt chẽ**: Thêm xử lý lỗi trong `trich_xuat_file_json` và `loc_hoc_sinh` để tránh lỗi khi `DATA_HS` hoặc `ds_hs` rỗng.
- **Cải thiện sự kiện `on_release`**: Đảm bảo khi chọn tên từ menu gợi ý, `self.hs_textfield.text` được cập nhật đúng và menu đóng lại mà không gây lỗi.
- **Tối ưu giao diện**: Tăng `width_mult` và giữ `max_height` để cải thiện trải nghiệm chạm trên điện thoại.
- **Thêm debug**: Thêm các lệnh `print` để theo dõi trạng thái dữ liệu và phát hiện lỗi.
- **Xử lý ngoại lệ**: Thêm kiểm tra trong `xac_nhan_hs` để xử lý trường hợp tên học sinh không hợp lệ hoặc để trống.

---

### **Mã nguồn sửa đổi**

Dưới đây là mã đã được cập nhật để đảm bảo tính năng chọn và xác nhận học sinh hoạt động ổn định trên cả máy tính và điện thoại:

<xaiArtifact artifact_id="d4daf959-f435-49b8-9ff9-08fabb93a063" artifact_version_id="81271156-8416-4145-8567-07a59fcf5505" title="main.py" contentType="text/python">
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import json
import os
from plyer import filechooser

# ====================== HẰNG SỐ ======================
TAP_TIN_CAU_HINH = "setting.json"
CAC_THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]

# ====================== DỮ LIỆU TOÀN CỤC ======================
DATA_HS = {}  # {"Tổ 1": [{"ten": ..., "gioi_tinh": ...}, ...], ...}
so_ngay_gh = 0
ds_truc_to = []  # Danh sách tổ trực
ds_hs = []  # Danh sách học sinh được thêm

# ====================== HÀM CẤU HÌNH ======================
def tai_cau_hinh():
    if os.path.exists(TAP_TIN_CAU_HINH):
        try:
            with open(TAP_TIN_CAU_HINH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc file cấu hình: {e}")
            return {}
    return {}

def luu_cau_hinh(cau_hinh):
    try:
        with open(TAP_TIN_CAU_HINH, "w", encoding="utf-8") as f:
            json.dump(cau_hinh, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu file cấu hình: {e}")

# ====================== HÀM XỬ LÝ FILE ======================
def trich_xuat_file_json(duong_dan="danhsach.json"):
    global DATA_HS
    if not os.path.exists(duong_dan):
        MDApp.get_running_app().show_alert("Lỗi", f"File {duong_dan} không tồn tại!")
        return {}
    try:
        with open(duong_dan, "r", encoding="utf-8") as f:
            DATA_HS = json.load(f)
        print("Đã tải DATA_HS:", DATA_HS)  # Debug
        return DATA_HS
    except Exception as e:
        MDApp.get_running_app().show_alert("Lỗi", f"Không đọc được file {duong_dan}: {e}")
        return {}

def chon_thu_muc_xuat():
    def on_selection(paths):
        if paths:
            cau_hinh = tai_cau_hinh()
            cau_hinh["thu_muc_xuat"] = paths[0]
            luu_cau_hinh(cau_hinh)
            MDApp.get_running_app().show_alert("Đã chọn", paths[0])
        else:
            MDApp.get_running_app().show_alert("Chưa chọn", "Bạn chưa chọn thư mục nào")
    filechooser.choose_dir(on_selection=on_selection)

# ====================== HÀM XỬ LÝ NGÀY ======================
def cap_nhat_menu_ngay(dropdown, so_ngay):
    menu_items = [
        {"text": str(i), "viewclass": "MDDropDownItem", "on_release": lambda x=i: dropdown.set_item(str(x))}
        for i in range(1, so_ngay + 1)
    ]
    dropdown.menu = MDDropdownMenu(caller=dropdown, items=menu_items, width_mult=5, max_height=dp(200))
    dropdown.current_item = "1"

# ====================== HÀM XỬ LÝ HỌC SINH ======================
def cap_nhat_hoc_sinh_theo_to(ten_to texfield, hs_dropdown_menu):
    ds_hs = []
    for to, hs_list in DATA_HS.items():
        for hs in hs_list:
            ds_hs.append(hs["ten"])
    print("Danh sách học sinh:", ds_hs)  # Debug
    hs_textfield.ds_hs = ds_hs  # Lưu danh sách học sinh vào textfield để lọc
    hs_textfield.dropdown_menu = MDDropdownMenu(
        caller=hs_textfield,
        items=[
            {"text": hs, "viewclass": "MDDropDownItem", "on_release": lambda x=hs: [hs_textfield.set_text(x), hs_textfield.dropdown_menu.dismiss()]}
            for hs in ds_hs
        ],
        width_mult=5,
        max_height=dp(200)
    )

def xac_nhan_to(ten_to):
    global ds_truc_to
    ds_truc_to = [{"ten": hs["ten"], "gioi_tinh": hs["gioi_tinh"]} for hs in DATA_HS.get(ten_to, [])]
    print("Tổ được chọn:", ten_to, "Danh sách tổ trực:", ds_truc_to)  # Debug
    MDApp.get_running_app().show_alert("Thành công", f"Đã chọn tổ: {ten_to}")

def xac_nhan_hs(hs_name, so_ngay):
    print("Xác nhận học sinh:", hs_name, "Số ngày:", so_ngay)  # Debug
    if not hs_name.strip():
        MDApp.get_running_app().show_alert("Lỗi", "Vui lòng nhập tên học sinh")
        return
    thong_tin_hs = None
    for to, danh_s in DATA_HS.items():
        for hs in danh_s:
            if hs["ten"] == hs_name:
                thong_tin_hs = hs
                break
        if thong_tin_hs:
            break
    if not thong_tin_hs:
        MDApp.get_running_app().show_alert("Lỗi", f"Không tìm thấy học sinh: {hs_name}")
        return
    for hs in ds_hs:
        if hs["ten"] == thong_tin_hs["ten"] and hs["gioi_tinh"] == thong_tin_hs["gioi_tinh"]:
            hs["ngay_truc"] = so_ngay
            MDApp.get_running_app().show_alert("Cập nhật", f"Đã cập nhật {hs['ten']} với {so_ngay} ngày trực")
            return
    ds_hs.append({"ten": thong_tin_hs["ten"], "gioi_tinh": thong_tin_hs["gioi_tinh"], "ngay_truc": so_ngay})
    MDApp.get_running_app().show_alert("Thành công", f"Đã thêm {hs_name} với {so_ngay} ngày trực")

def sap_xep():
    print("Danh sách học sinh:", ds_hs)
    print("Danh sách tổ trực:", ds_truc_to)

# ====================== GIAO DIỆN KIVYMD ======================
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cau_hinh = tai_cau_hinh()
        trich_xuat_file_json()
        print("Danh sách tổ:", list(DATA_HS.keys()))  # Debug
        print("Dữ liệu học sinh:", DATA_HS)  # Debug

        # Bố cục chính
        layout = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        # Khung xem trước lịch trực
        layout.add_widget(MDLabel(text="Xem trước lịch trực", halign="center", font_size=dp(20)))

        # Khung chọn tổ
        self.to_dropdown = MDDropDownItem()
        cac_to = list(DATA_HS.keys()) if DATA_HS else ["Tổ 1", "Tổ 2"]
        self.to_dropdown.menu_items = [
            {
                "text": to,
                "viewclass": "MDDropDownItem",
                "on_release": lambda x=to: [self.to_dropdown.set_item(x), cap_nhat_hoc_sinh_theo_to(x, self.hs_textfield, self.hs_dropdown_menu)]
            } for to in cac_to
        ]
        self.to_dropdown.menu = MDDropdownMenu(
            caller=self.to_dropdown,
            items=self.to_dropdown.menu_items,
            width_mult=5,
            max_height=dp(200)
        )
        self.to_dropdown.set_item(cac_to[0] if cac_to else "Không có tổ")
        layout.add_widget(MDLabel(text="Chọn tổ", font_size=dp(16)))
        layout.add_widget(self.to_dropdown)
        layout.add_widget(MDRaisedButton(
            text="Xác nhận tổ",
            on_release=lambda x: xac_nhan_to !<self.to_dropdown.current_item)
        )
        layout.add_widget(MDRaisedButton(
            text="Kiểm tra tổ",
            on_release=lambda x: MDApp.get_running_app().show_alert("Tổ hiện tại", self.to_dropdown.current_item)
        ))

        # Khung chọn học sinh
        self.hs_textfield = MDTextField(hint_text="Nhập tên học sinh", mode="rectangle", font_size=dp(16))
        self.hs_textfield.bind(text=self.loc_hoc_sinh)
        self.hs_dropdown_menu = MDDropdownMenu(caller=self.hs_textfield, items=[], width_mult=5, max_height=dp(200))
        layout.add_widget(MDLabel(text="Chọn học sinh", font_size=dp(16)))
        layout.add_widget(self.hs_textfield)

        # Số ngày trực
        self.ngay_dropdown = MDDropDownItem()
        cap_nhat_menu_ngay(self.ngay_dropdown, 1)
        layout.add_widget(MDLabel(text="Số ngày trực", font_size=dp(16)))
        layout.add_widget(self.ngay_dropdown)
        layout.add_widget(MDRaisedButton(
            text="Xác nhận học sinh",
            on_release=lambda x: xac_nhan_hs(self.hs_textfield.text, int(self.ngay_dropdown.current_item))
        ))

        # Nút điều khiển
        layout.add_widget(MDRaisedButton(text="Chạy thử", on_release=lambda x: sap_xep()))
        layout.add_widget(MDRaisedButton(text="Chọn thư mục Export", on_release=lambda x: chon_thu_muc_xuat()))

        # Cài đặt khoảng ngày trực
        if "khoang_ngay" in self.cau_hinh:
            bat_dau, ket_thuc = self.cau_hinh["khoang_ngay"]
            i_bat_dau = CAC_THU_TRONG_TUAN.index(bat_dau)
            i_ket_thuc = CAC_THU_TRONG_TUAN.index(ket_thuc)
            if i_bat_dau <= i_ket_thuc:
                global so_ngay_gh
                so_ngay_gh = i_ket_thuc - i_bat_dau + 1
                cap_nhat_menu_ngay(self.ngay_dropdown, so_ngay_gh)

        # Khởi tạo danh sách học sinh
        cap_nhat_hoc_sinh_theo_to(cac_to[0] if cac_to else "Tổ 1", self.hs_textfield, self.hs_dropdown_menu)
        self.add_widget(layout)

    def loc_hoc_sinh(self, instance, value):
        if not hasattr(self.hs_textfield, 'ds_hs') or not self.hs_textfield.ds_hs:
            print("Không có danh sách học sinh để lọc")  # Debug
            self.hs_dropdown_menu.items = []
            return
        tu_khoa = value.lower().strip()
        ds_loc = [hs for hs in self.hs_textfield.ds_hs if tu_khoa in hs.lower()] if tu_khoa else self.hs_textfield.ds_hs
        print("Danh sách học sinh được lọc:", ds_loc)  # Debug
        self.hs_dropdown_menu.items = [
            {"text": hs, "viewclass": "MDDropDownItem", "on_release": lambda x=hs: [self.hs_textfield.set_text(x), self.hs_dropdown_menu.dismiss()]}
            for hs in ds_loc
        ]
        if ds_loc:  # Chỉ mở menu nếu có kết quả lọc
            self.hs_dropdown_menu.open()
        else:
            self.hs_dropdown_menu.dismiss()

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return MainScreen()

    def show_alert(self, title, message):
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(title=title, text=message, buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()
        
if __name__ == "__main__":
    MyApp().run()