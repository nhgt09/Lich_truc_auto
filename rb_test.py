from tkinter import *
from tkinter import ttk, Menu, LabelFrame, filedialog, messagebox
from docx import Document
import json, os

file_duong_dan = "./setting.json"
file_danh_sach = "./danhsach.json"
file_thu = './thu.json'
duong_dan_export = ''

toor =[]
DANHSACH_HS_TUNG_TO = []
DANHSACH_HS = []

#OUTPUT
DANHSACH_HS_TOOR_TRUC = []
DANHSACH_HS_TRUC= []

class HocSinh:
     def __init__(self,ten:str,gioi_tinh:str):
          self.ten=ten
          self.gioi_tinh=gioi_tinh.lower()
     
     def to_dict(self):
          return {
               "ten": self.ten,
               "gioi_tinh": self.gioi_tinh
          }

#Thai
def check_file(file):
     with open(file, 'r+', encoding='utf-8') as f:
          data=f.read().strip()
          dau=[]
          val={'{':1,'}':-1, '[':2,']':-2,'(':3,')':-3}
          if not data:
               f.write("{}")
               return
          for i in data:
               t=val.get(i,[])
               if not t:continue
               if dau and t<0 and dau[-1]+t==0:
                    dau.pop()
               else:dau+=[t]
          sua = ""
          for t in reversed(dau):
               if t == 1: 
                    sua += "}"
               elif t == 2:
                    sua += "]"
          if dau:
               if data.endswith(','):
                    data = data.strip()[:-1]
               f.write(sua)

def doc_file_duong_dan():
     check_file(file=file_duong_dan)
     if os.path.exists(file_duong_dan):
          try:
               with open(file_duong_dan, "r", encoding="utf-8") as f:
                    return json.load(f)
          except Exception:
               messagebox.showerror("Lỗi","Lỗi 001")
               os._exit(0)
               return {}
     messagebox.showerror("Lỗi!","Lỗi 002")
     os._exit(0)
     return {}

def doc_file_thu():
     check_file(file=file_thu)
     if os.path.exists(file_thu):
          try:
               with open(file_thu, "r", encoding="utf-8") as f:
                    return json.load(f)
          except Exception:
               messagebox.showerror("Lỗi","Lỗi 003")
               os._exit(0)
               return {}
     messagebox.showerror("Lỗi!","Lỗi 004")
     os._exit(0)
     return []

def doc_ghi_file_word():

     DANHSACH_HS_LUU = {}
     duong_dan = filedialog.askopenfilename(title="Chọn file Word", filetypes=[("Word files", "*.docx")])
     if not duong_dan:
          return
     try:
          file = Document(duong_dan)
          danh_sach_to = None

          for dulieu_ch_xl in file.paragraphs:
               dulieu = dulieu_ch_xl.text.strip()
               if not dulieu:
                    continue

               dulieu = dulieu.replace("–", "-").replace("—", "-")

               if dulieu.lower().startswith("tổ"):
                    danh_sach_to = dulieu.upper()
                    DANHSACH_HS_LUU[danh_sach_to] = []
               
               elif danh_sach_to and ("nam" in dulieu.lower() or "nữ" in dulieu.lower()):
                    parts = dulieu.rsplit(" ", 1)
                    if len(parts) == 2:
                         DANHSACH_HS_LUU[danh_sach_to].append(HocSinh(*parts))

          with open(file_danh_sach, "w", encoding="utf-8") as f:
               for to in DANHSACH_HS_LUU:
                    DANHSACH_HS_LUU[to] = [hs.to_dict() for hs in DANHSACH_HS_LUU[to]]
               print(DANHSACH_HS_LUU)
               json.dump(DANHSACH_HS_LUU, f, ensure_ascii=False, indent=2)

     except Exception as n:
          messagebox.showerror("Lỗi", f"Không thể đọc file: \n{n}")

def trich_xuat_file_danhsach():
     check_file(file=file_danh_sach)
     global toor,DANHSACH_HS_TUNG_TO,DANHSACH_HS
     
     with open(file_danh_sach, "r", encoding="utf-8") as f:
          data  = json.load(f)
     toor = list(data.keys())
     data:dict
     for danh_sach_hs in data.values():
          hocsinhs=[HocSinh(**hs) for hs in danh_sach_hs]
          DANHSACH_HS+=hocsinhs
          DANHSACH_HS_TUNG_TO.append(hocsinhs)
               
     

     
def xac_nhan_to(to):
     global DANHSACH_HS_TOOR_TRUC
     
     DANHSACH_HS_TOOR_TRUC = DANHSACH_HS_TUNG_TO[toor.index(to)]








def chon_duong_dan_export():
     global duong_dan_export
     duong_dan_chon = filedialog.askdirectory(title="Chọn đường dẫn cho export")
     
     if duong_dan_chon:
          duong_dan_export = duong_dan_chon
          with open(file_duong_dan, "w", encoding="utf-8") as f:
               json.dump({"duong_dan": duong_dan_export}, f, ensure_ascii=False, indent=2)
          messagebox.showinfo("",f"Đường dẫn được chọn là {duong_dan_export}")
          return
     else:
          messagebox.showwarning("Cảnh báo","Chưa chọn đường dẫn")
          return

def chon_ngay_sep_lich(man_hinh):
     
     man_hinh_phu = Toplevel(man_hinh)
     man_hinh_phu.title("")
     man_hinh_phu.geometry("200x400")
     thu_list = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]

     thu_duoc_chon_save = doc_file_thu()

     luu_thu = {}
     for thu in thu_list:
          luu_thu[thu] = BooleanVar(value=(thu in thu_duoc_chon_save))
     for thu in thu_list:
        cb = Checkbutton(man_hinh_phu, text=thu, variable=luu_thu[thu],font=("Arial",20))
        cb.pack(anchor="n") 

     def xac_nhan():
          thu_dc_chon = []
          for thu, gia_tri in luu_thu.items():
               if gia_tri.get():
                    thu_dc_chon.append(thu)

          if not thu_dc_chon:
               messagebox.showerror("Lỗi", "Chưa chọn bất kì thứ nào")
               return
          
          with open(file_thu, "w", encoding="utf-8") as f:
               json.dump(thu_dc_chon, f, ensure_ascii=False, indent=4)
          man_hinh_phu.destroy()

     xac_nhan_but = Button(man_hinh_phu,text=("Xác nhận"), font=("Arial", 20),command=xac_nhan)
     xac_nhan_but.pack(pady=20)

     man_hinh_phu.mainloop()






def chinh_sua_danh_sach(man_hinh):
     man_hinh_cs = Toplevel(man_hinh)
     man_hinh_cs.grab_set()
     man_hinh_cs.title("Chỉnh sửa danh sách trực")
     man_hinh_cs.geometry("500x500")

     
     man_hinh_cs.mainloop()







class HopChonCoTimKiem(Frame):
    """Combobox có ô tìm kiếm (custom)."""

    def __init__(self, master, lua_chon, **kwargs):
        super().__init__(master, **kwargs)
        self.lua_chon = lua_chon
        self.dropdown_visible = False

        # Ô nhập + nút
        khung_tren = Frame(self)
        khung_tren.pack(fill="x")

        self.o_nhap = Entry(khung_tren, width=24)
        self.o_nhap.pack(side=LEFT, fill="x", expand=True)
        self.o_nhap.bind("<KeyRelease>", self.loc_danh_sach)
        self.o_nhap.bind("<FocusIn>", self.hien_dropdown)

        Button(khung_tren, text="▼", command=self.chuyen_trang_thai, width=2).pack(side=LEFT)

        # Listbox
        self.khung_listbox = Frame(self)
        self.listbox = Listbox(self.khung_listbox, height=5, width=24)
        self.listbox.pack(fill="x")
        self.listbox.bind("<<ListboxSelect>>", self.chon_item)

        self.cap_nhat_listbox(self.lua_chon)

    def cap_nhat_listbox(self, data):
        self.listbox.delete(0, END)
        for item in data:
            item:HocSinh
            self.listbox.insert(END, item.ten)

    def loc_danh_sach(self, event=None):
        tu_khoa = self.o_nhap.get().lower()
        data = [item for item in self.lua_chon if tu_khoa in item.ten.lower()] if tu_khoa else self.lua_chon
        self.cap_nhat_listbox(data)
        self.hien_dropdown()

    def chon_item(self, event=None):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        gia_tri = self.listbox.get(index)
        self.o_nhap.delete(0, END)
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

def xac_nhan_hs(hcsinh:HopChonCoTimKiem, ngaytruc):
     hs_duoc_chon = (hcsinh.o_nhap.get())
     print(hs_duoc_chon)
     ngay = ngaytruc.get()
     print(hs_duoc_chon)
     if not hs_duoc_chon and ngay:
          pass
def main():
     
     trich_xuat_file_danhsach()
     mh_chinh = Tk()
     mh_chinh.title("Phần mềm phân công lịch trực")
     mh_chinh.state("zoomed")


#=========================MENU=========================
     #=====Thanh menu setup
     thanhmenu = Menu(mh_chinh)
     thanhmenu_font = ("Arial", 12)

     #=====File
     file_op = Menu(thanhmenu, tearoff=0,font=thanhmenu_font)
     file_op.add_command(label="Đọc file Word…",command=doc_ghi_file_word)
     file_op.add_command(label="Chọn thư mục Export…",command=chon_duong_dan_export)
     thanhmenu.add_cascade(label="File", menu=file_op)

     #=====Cai dat
     caidat_op = Menu(thanhmenu, tearoff=0, font=thanhmenu_font)
     caidat_op.add_command(label="Chọn ngày xếp lịch", command=lambda:chon_ngay_sep_lich(mh_chinh))
     thanhmenu.add_cascade(label="Cài đặt", menu= caidat_op)

#=========================MAIN=========================
     khung_lich_truc = Frame(mh_chinh, bg="#f0f0f0", relief="sunken", bd=2)
     khung_lich_truc.pack(side="left", fill="both", expand=True, padx=10, pady=10)
     Label(khung_lich_truc, text="Xem trước lịch trực", bg="#f0f0f0").pack(expand=True)

     khung_dieu_khien = Frame(mh_chinh, relief="groove", bd=2)
     khung_dieu_khien.pack(side="right", fill="y", padx=10, pady=10)

     #=========== Chọn tổ 
     khung_to = LabelFrame(khung_dieu_khien, text="Chọn tổ",font=('Arial', 15))
     khung_to.pack(side="left",anchor="n",pady=0)

     
     bien_to = StringVar()

     chon_to = ttk.OptionMenu(khung_to,bien_to,"Chọn tổ",*toor,command=lambda val: xac_nhan_to(bien_to.get()))
     style = ttk.Style(mh_chinh)
     style.configure("TMenubutton", font=("Arial", 15)) 
     chon_to.pack(fill="x", pady=5)

     Button(khung_to, text="Xác nhận tổ",font=('Arial', 15)).pack(fill="x", pady=5)

     # ============ Chọn học sinh
     khung_hs = LabelFrame(khung_dieu_khien, text="Chọn học sinh",font=('Arial', 15))
     khung_hs.pack(side="right",anchor="n",pady=0)

     test = [hs for hs in DANHSACH_HS]
     combobox_hs = HopChonCoTimKiem(khung_hs, lua_chon=test)
     combobox_hs.pack(fill="x", pady=5)

     Label(khung_hs, text="Số ngày trực:",font=('Arial', 15)).pack(anchor="w", pady=5)
     bien_ngay = StringVar(value="1")
     
     menu_ngay = ttk.OptionMenu(khung_hs, bien_ngay, "1", *[str(i) for i in range(1, len(doc_file_thu())+1)])
     menu_ngay.pack(fill="x", pady=5)

     
     Button(khung_hs, text="Xác nhận học sinh",font=('Arial', 15),command=lambda: xac_nhan_hs(combobox_hs,bien_ngay)).pack(fill="x", pady=5)

     #========== Các nút dưới
     khung_duoi = Frame(khung_dieu_khien)
     khung_duoi.pack(side="bottom", fill="x", pady=10)
     Button(khung_duoi, text="Chạy thử",font=('Arial', 15)).pack(fill="x", pady=5)
     Button(khung_duoi, text="Chỉnh sửa lịch trực",font=('Arial', 15)).pack(fill="x", pady=5)
     Button(khung_duoi, text="Chỉnh sửa danh sách học sinh",font=('Arial', 15),command=lambda:chinh_sua_danh_sach(mh_chinh)).pack(fill="x", pady=5)
     Button(khung_duoi, text="Xác nhận Export",font=('Arial', 15)).pack(fill="x", pady=5)






     mh_chinh.config(menu=thanhmenu)

     mh_chinh.mainloop()
if __name__ == "__main__":
    main()