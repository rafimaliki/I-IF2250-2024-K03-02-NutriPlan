from typing import Any
import datetime, calendar

import flet as ft
from components.NavBar import NavBar
from classes.Jadwal_Makanan import Jadwal_Makanan
from classes.Makanan import Makanan
from database.db import DatabaseManager

Month_Show = datetime.datetime.now().month
Month = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
Month_Day_Map = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
Max_Date = calendar.monthrange(datetime.datetime.now().year, Month_Show)[1]

class Jadwal_Title(ft.Text):
    def __init__(self):
        super().__init__(
            f"Jadwalku ({Month[Month_Show-1]})", 
            color="black", 
            size=25, 
            text_align=ft.TextAlign.CENTER, 
            weight=ft.FontWeight.BOLD, 
            font_family="Kanit"
        )

class Edit_Jadwal_Modal(ft.AlertDialog):
    def __init__(self, Page, Jadwal_Card_Table):
        
        self.db_manager = DatabaseManager()
        self.Page = Page
        self.Reload_Database() 
        self.Submit_Button = self.Submit_Button()
        self.Date = None
        self.Jadwal_Card_Table = Jadwal_Card_Table
        self.Jadwal = None
        self.Makanan_Dropdown = self.Makanan_Dropdown_UI()
        self.Category_Dropdown = self.Category_Dropdown_UI()
        self.Date_Picker_Button = self.Date_Picker_Button_UI()  
        
        super().__init__(
            bgcolor="white",
            content=ft.Container(
                ft.Column([
                    ft.Container(content=ft.Text("Edit Jadwal", color="black", size=20, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, font_family="Kanit"), width=450, height=50, alignment=ft.alignment.center),
                    self.Makanan_Dropdown,
                    self.Category_Dropdown,
                    self.Date_Picker_Button,
                    self.Submit_Button
                ],
                width=450,
                height=400,
                ), 
            )
        )
    def Reload_Database(self):
        self.List_Makanan = self.db_manager.get_all_makanan()
        self.Date_Picker = self.Date_Picker_UI()
        self.Page.overlay.append(self.Date_Picker)
        self.Date_Picker_Button = self.Date_Picker_Button_UI()
        self.Category_Dropdown = self.Category_Dropdown_UI()
        
        #reload makanan names
        
    def Open(self, key):
        # self.Reload_Database()
        db = DatabaseManager()
        list_makanan = db.get_all_makanan()
        makanan_names = [makanan.nama for makanan in list_makanan]
        self.Makanan_Dropdown.content.controls[1].options=[ft.dropdown.Option(makanan) for makanan in makanan_names]
        self.Jadwal = self.db_manager.get_jadwal_by_id(key)
        self.Category_Dropdown.content.controls[1].value = self.Jadwal.kategori
        self.Date_Picker_Button.content.controls[1].content.value = self.Jadwal.hari
        self.Date = self.Jadwal.hari
        self.Makanan_Dropdown.content.controls[1].value = self.Jadwal.makanan.nama
        print(self.Jadwal)
        
        self.Page.dialog = self
        self.open = True
        self.Page.update()
        
    def Category_Dropdown_UI(self):
        return ft.Container(
            content=ft.Row([
                ft.Text("Kategori ", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Dropdown(
                options=[
                    ft.dropdown.Option("Sarapan"),
                    ft.dropdown.Option("Makan Siang"),
                    ft.dropdown.Option("Makan Malam"),
                ],
                bgcolor="white",
                color="black",
                width=150,
                height=30,
                padding=0,
                content_padding=ft.padding.only(top=0, bottom=0, left=10, right=0),
                item_height=30,
                focused_border_color = "#547250",
                )
            ])
        )
        
    def Date_Picker_UI(self):
        return ft.DatePicker(
            first_date=datetime.datetime(2024, 1, 1),
            last_date=datetime.datetime(2026, 10, 1),
            on_change=self.Date_Change_Handler,
        )
        
    def Date_Picker_Button_UI(self):
        return ft.Container(
            content=ft.Row([
                ft.Text("Tanggal   ", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Container(
                    content=ft.Text("Pilih Tanggal", color="black", size=14, text_align=ft.TextAlign.LEFT),
                    height=30,
                    width=150,
                    bgcolor="white",
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.BLACK),
                    on_click=lambda _: self.Date_Picker.pick_date(),
                    alignment=ft.alignment.center_left,
                    padding=ft.padding.only(left=10, right=10),
                )
            ])
        )
        
    def Date_Change_Handler(self, e):
        self.Date = self.Date_Picker.value.strftime("%d-%m-%Y")
        self.Date_Picker_Button.content.controls[1].content.value = self.Date
        self.Page.update()
        
    def Makanan_Dropdown_UI(self):
        db = DatabaseManager()
        list_makanan = db.get_all_makanan()
        makanan_names = [makanan.nama for makanan in list_makanan]
     
        return ft.Container(
            content=ft.Row([
                ft.Text("Makanan", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Dropdown(
                options=[ft.dropdown.Option(makanan) for makanan in makanan_names],
                bgcolor="white",
                color="black",
                width=150,
                height=30,
                padding=0,
                content_padding=ft.padding.only(top=0, bottom=0, left=10, right=0),
                item_height=30,
                focused_border_color = "#547250",
                )
            ])
        )
        
    def Submit_Handler(self, e):
        
        list_makanan = self.db_manager.get_all_makanan()
        Nama_Makanan = self.Makanan_Dropdown.content.controls[1].value
        Id = 0;
        
        for makanan in list_makanan:
            if makanan.nama == Nama_Makanan:
                Id = makanan.id_makanan
                
        Kategori = self.Category_Dropdown.content.controls[1].value
        Tanggal = self.Date
        
        if (Id != 0 and Kategori != None and Tanggal != None):
            
            if ((self.db_manager.jadwal_already_exists(Kategori, Tanggal)) and (self.Jadwal.id_jadwal != self.db_manager.get_jadwal_id_by_kat_tgl(Kategori, Tanggal).id_jadwal)):
                print("Jadwal sudah ada")
                return
            
            # delete old data
            self.db_manager.delete_jadwal(self.Jadwal.id_jadwal)
            self.Jadwal_Card_Table.Delete(self.Jadwal.id_jadwal)
            
            self.db_manager.insert_jadwal_makanan(Id, Kategori, Tanggal)
            self.Jadwal_Card_Table.Set(int(Tanggal.split("-")[0]), ["Sarapan", "Makan Siang", "Makan Malam"].index(Kategori) + 1, Makanan(nama=Nama_Makanan), self.db_manager.get_last_id_jadwal())
            self.Jadwal_Card_Table.Jadwal_Element_List[int(Tanggal.split("-")[0])-1][["Sarapan", "Makan Siang", "Makan Malam"].index(Kategori)].key = self.db_manager.get_last_id_jadwal()-1
            
            self.Page.update()
        
        print(Nama_Makanan, Kategori, Tanggal)
        self.open = False
        self.Page.update()
        
    def Submit_Button(self):
        return ft.Container(
            content=ft.ElevatedButton("Submit", on_click=self.Submit_Handler, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)), 
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                }, 
                bgcolor=
                {ft.MaterialState.FOCUSED: ft.colors.WHITE, "": "#547250"},),
            width=450, height=50, alignment=ft.alignment.center, margin=ft.margin.only(top=175, bottom=10)
        )

class Detail_Makanan_Modal(ft.AlertDialog):
    def __init__(self, Page, Table):
        self.Page = Page
        self.db_manager = DatabaseManager()
        self.Table = Table
        self.Add_Shopping_Button = self.Add_Shopping_Button_UI()
        self.Edit_Button = self.Edit_Button_UI()
        self.Delete_Button = self.Delete_Button_UI()
        self.Nama_Makanan_Text = ft.Text("", color="black", size=25, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, font_family="Kanit")
        self.Detail_Makanan_Text = ft.Text("", color="black", size=15, text_align=ft.TextAlign.CENTER)
        self.Key = -1
        self.Makanan_Id = -1
        self.Edit_Jadwal_Modal = Edit_Jadwal_Modal(self.Page, self.Table)
        super().__init__(
            bgcolor="white",
            content=ft.Container(
                ft.Column([
                    ft.Container(content=ft.Column(
                        [
                        ft.Container(content=self.Nama_Makanan_Text, width=450, height=50, alignment=ft.alignment.center),
                        ft.Container(content=self.Detail_Makanan_Text, width=450, height=50, alignment=ft.alignment.center),
                        ], alignment=ft.MainAxisAlignment.START
                        ), width=450, height=50, alignment=ft.alignment.center),
                    ft.Container(content=ft.Column(
                        [
                        ft.Container(content=ft.Row(
                            [
                            self.Delete_Button,
                            self.Edit_Button,
                            ], alignment=ft.MainAxisAlignment.CENTER
                        ), width=450, height=35, alignment=ft.alignment.center),
                        self.Add_Shopping_Button
                        ], alignment=ft.MainAxisAlignment.CENTER
                        ), width=450, alignment=ft.alignment.center),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450,
                height=400,
                ), 
            )
        )
        
    def Edit_Handler(self, e):
        # open modal
        print(f"Edit {self.Key}")
        self.Edit_Jadwal_Modal.Open(self.Key)
        
    
    def Edit_Button_UI(self):
        return ft.Container(
            content=ft.ElevatedButton("Edit", on_click=self.Edit_Handler, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)), 
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                }, 
                bgcolor=
                {ft.MaterialState.FOCUSED: ft.colors.WHITE, "": "#547250"},
                width=138),
            height=35, alignment=ft.alignment.center, margin=0
        )
        
    def Delete_Handler(self, e):
        self.db_manager.delete_jadwal(self.Key)
        self.Table.Delete(self.Key)
        self.open = False
        self.Page.update()
        
    def Delete_Button_UI(self):
        return ft.Container(
            content=ft.ElevatedButton("Hapus", on_click=self.Delete_Handler, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)), 
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                }, 
                bgcolor=
                {ft.MaterialState.FOCUSED: ft.colors.WHITE, "": "#FF0000"},),
            height=35, alignment=ft.alignment.center, margin=0
        )
    def Belanja_Handler(self, e):
        print("Menambahkan daftar belanja: ID Makanan=", self.Makanan_Id)
        self.db_manager.insert_daftar_belanja_by_id_makanan(self.Makanan_Id)
        
    def Add_Shopping_Button_UI(self):
        return ft.Container(
            content=ft.ElevatedButton("Tambahkan ke Daftar Belanja", on_click=self.Belanja_Handler, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)), 
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                }, 
                bgcolor=
                {ft.MaterialState.FOCUSED: ft.colors.WHITE, "": "#547250"},),
            height=35, alignment=ft.alignment.center, margin=0
        )    
        
    def Open(self, e):
        if (e.control.key == -1):
            return
        
        Makanan = self.db_manager.get_makanan_by_id_jadwal(e.control.key)
        self.Detail_Makanan_Text.value = f"{Makanan.deskripsi}"
        self.Nama_Makanan_Text.value = f"{Makanan.nama}"
        self.Page.dialog = self
        self.Key = e.control.key
        self.Makanan_Id = Makanan.id_makanan
        
        print(f"Makanan: {Makanan}")
        print(f"Id Jadwal: {e.control.key}")
        
        self.open = True
        self.Page.update()
        
class Tambah_Jadwal_Modal(ft.AlertDialog):
    def __init__(self, Page, Jadwal_Card_Table):
        
        self.db_manager = DatabaseManager()
        self.Page = Page
        self.Reload_Database() 
        self.Submit_Button = self.Submit_Button()
        self.Date = None
        self.Jadwal_Card_Table = Jadwal_Card_Table
        
        super().__init__(
            bgcolor="white",
            content=ft.Container(
                ft.Column([
                    ft.Container(content=ft.Text("Tambah Jadwal", color="black", size=20, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, font_family="Kanit"), width=450, height=50, alignment=ft.alignment.center),
                    self.Makanan_Dropdown,
                    self.Category_Dropdown,
                    self.Date_Picker_Button,
                    self.Submit_Button
                ],
                width=450,
                height=400,
                ), 
            )
        )
    def Reload_Database(self):
        self.List_Makanan = self.db_manager.get_all_makanan()
        self.Date_Picker = self.Date_Picker_UI()
        self.Page.overlay.append(self.Date_Picker)
        self.Date_Picker_Button = self.Date_Picker_Button_UI()
        self.Makanan_Dropdown = self.Makanan_Dropdown_UI()
        self.Category_Dropdown = self.Category_Dropdown_UI()
        
    def Open(self, e):
        # self.Reload_Database()
        db = DatabaseManager()
        list_makanan = db.get_all_makanan()
        makanan_names = [makanan.nama for makanan in list_makanan]
        self.Makanan_Dropdown.content.controls[1].options=[ft.dropdown.Option(makanan) for makanan in makanan_names]
        self.Page.dialog = self
        self.open = True
        self.Page.update()
        
    def Category_Dropdown_UI(self):
        return ft.Container(
            content=ft.Row([
                ft.Text("Kategori ", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Dropdown(
                options=[
                    ft.dropdown.Option("Sarapan"),
                    ft.dropdown.Option("Makan Siang"),
                    ft.dropdown.Option("Makan Malam"),
                ],
                bgcolor="white",
                color="black",
                width=150,
                height=30,
                padding=0,
                content_padding=ft.padding.only(top=0, bottom=0, left=10, right=0),
                item_height=30,
                focused_border_color = "#547250",
                )
            ])
        )
        
    def Date_Picker_UI(self):
        return ft.DatePicker(
            first_date=datetime.datetime(2024, 1, 1),
            last_date=datetime.datetime(2026, 10, 1),
            on_change=self.Date_Change_Handler,
        )
        
    def Date_Picker_Button_UI(self):
        return ft.Container(
            content=ft.Row([
                ft.Text("Tanggal   ", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Container(
                    content=ft.Text("Pilih Tanggal", color="black", size=14, text_align=ft.TextAlign.LEFT),
                    height=30,
                    width=150,
                    bgcolor="white",
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.BLACK),
                    on_click=lambda _: self.Date_Picker.pick_date(),
                    alignment=ft.alignment.center_left,
                    padding=ft.padding.only(left=10, right=10),
                )
            ])
        )
        
    def Date_Change_Handler(self, e):
        self.Date = self.Date_Picker.value.strftime("%d-%m-%Y")
        self.Date_Picker_Button.content.controls[1].content.value = self.Date
        self.Page.update()
        
    def Makanan_Dropdown_UI(self):
        db = DatabaseManager()
        list_makanan = db.get_all_makanan()
        makanan_names = [makanan.nama for makanan in list_makanan]
     
        return ft.Container(
            content=ft.Row([
                ft.Text("Makanan", color="black", size=15, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Dropdown(
                options=[ft.dropdown.Option(makanan) for makanan in makanan_names],
                bgcolor="white",
                color="black",
                width=150,
                height=30,
                padding=0,
                content_padding=ft.padding.only(top=0, bottom=0, left=10, right=0),
                item_height=30,
                focused_border_color = "#547250",
                )
            ])
        )
        
    def Submit_Handler(self, e):
        
        list_makanan = self.db_manager.get_all_makanan()
        Nama_Makanan = self.Makanan_Dropdown.content.controls[1].value
        Id = 0;
        
        for makanan in list_makanan:
            if makanan.nama == Nama_Makanan:
                Id = makanan.id_makanan
                
        Kategori = self.Category_Dropdown.content.controls[1].value
        Tanggal = self.Date
        
        if (Id != 0 and Kategori != None and Tanggal != None and self.db_manager.jadwal_already_exists(Kategori, Tanggal) == False):
            
            self.db_manager.insert_jadwal_makanan(Id, Kategori, Tanggal)
            self.Jadwal_Card_Table.Set(int(Tanggal.split("-")[0]), ["Sarapan", "Makan Siang", "Makan Malam"].index(Kategori) + 1, Makanan(nama=Nama_Makanan), self.db_manager.get_last_id_jadwal()-1)
            # self.Jadwal_Card_Table.Jadwal_Element_List[int(Tanggal.split("-")[0])-1][["Sarapan", "Makan Siang", "Makan Malam"].index(Kategori)].key = self.db_manager.get_last_id_jadwal()-1
            
            self.Page.update()
        
        print(Nama_Makanan, Kategori, Tanggal)
        self.open = False
        self.Page.update()
        
    def Submit_Button(self):
        return ft.Container(
            content=ft.ElevatedButton("Submit", on_click=self.Submit_Handler, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)), 
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                }, 
                bgcolor=
                {ft.MaterialState.FOCUSED: ft.colors.WHITE, "": "#547250"},),
            width=450, height=50, alignment=ft.alignment.center, margin=ft.margin.only(top=175, bottom=10)
        )

class Tambah_Jadwal_Button(ft.IconButton):
    def __init__(self, Page, Jadwal_Card_Table):
        self.Page = Page
        self.Tambah_Jadwal_Modal = Tambah_Jadwal_Modal(self.Page, Jadwal_Card_Table)
        super().__init__(
            icon=ft.icons.ADD,
            icon_size=25,
            bgcolor="#547250",
            icon_color="white",
            tooltip="Tambah Jadwal",
            on_click=self.Tambah_Jadwal_Modal.Open,
        )
        
class Scroll_Button(ft.Row):
    def __init__(self, Jadwal_Card_Table, parent):
        self.Jadwal_Card_Table = Jadwal_Card_Table
        self.Table = parent
        super().__init__(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK_ROUNDED,
                    icon_size=25,
                    bgcolor="#547250",
                    icon_color = "white",
                    tooltip="Kiri",
                    on_click=self.Scroll_Left,
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_FORWARD_ROUNDED,
                    icon_size=25,
                    bgcolor="#547250",
                    icon_color = "white",
                    tooltip="Kanan",
                    on_click=self.Scroll_Right,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        
    def Scroll_Left(self, e):
        
        global Month_Show
        Max_Date = Month_Day_Map[Month_Show]
        
        if (self.Jadwal_Card_Table.Scroll_Idx == 1):
            Month_Show -= 1
            if (Month_Show == 0):
                Month_Show = 12
            self.Jadwal_Card_Table.Scroll_Idx = Month_Day_Map[Month_Show]-4
            self.Table.InitDatas()
        elif (self.Jadwal_Card_Table.Scroll_Idx - 5 >= 1):
            self.Jadwal_Card_Table.Scroll_Idx -= 5
        else:
            self.Jadwal_Card_Table.Scroll_Idx = 1
        # print(self.Jadwal_Card_Table.Scroll_Idx)
        self.Jadwal_Card_Table.scroll_to(key=f"{self.Jadwal_Card_Table.Scroll_Idx}", duration=700)

    def Scroll_Right(self, e):
        
        global Month_Show
        Max_Date = Month_Day_Map[Month_Show]
        
        if (self.Jadwal_Card_Table.Scroll_Idx == Max_Date-4):
            self.Jadwal_Card_Table.Scroll_Idx = 1
            Month_Show += 1
            if (Month_Show == 13):
                Month_Show = 1
            self.Table.InitDatas()
        elif (self.Jadwal_Card_Table.Scroll_Idx + 5 <= Max_Date):
            self.Jadwal_Card_Table.Scroll_Idx += 5
            if (self.Jadwal_Card_Table.Scroll_Idx > Max_Date-4):
                self.Jadwal_Card_Table.Scroll_Idx = Max_Date-4
        else:
            self.Jadwal_Card_Table.Scroll_Idx = Max_Date-4
        # print(self.Jadwal_Card_Table.Scroll_Idx)
        self.Jadwal_Card_Table.scroll_to(key=f"{self.Jadwal_Card_Table.Scroll_Idx}", duration=700)

class Jadwal_Element(ft.Container):
    def __init__(self, color, key, Page, Table, Id = -1):
        
        self.Page = Page
        self.Detail_Makanan_Modal = Detail_Makanan_Modal(self.Page, Table)
        
        super().__init__(
            content=ft.Column(
                [
                    ft.Text(" ",
                    size=20, 
                    text_align=ft.TextAlign.CENTER, 
                    weight=ft.FontWeight.BOLD, 
                    font_family="Kanit",
                    color="white"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor=color,
            width=170,
            height=150,
            margin=0,
            key=Id,
            on_click=self.Detail_Makanan_Modal.Open,
            padding=ft.padding.only(top=10, bottom=10, left=10, right=10)
        )
    
    def Set_Jadwal(self, makanan: Jadwal_Makanan):
        self.content.controls[0].value = makanan.nama
    
class Jadwal_Card(ft.Container):
    def __init__(self, key, elements):
        super().__init__(
            content=ft.Column(
            [   
                ft.Text(f"{key}", color="black", size=20, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, font_family="Kanit"),
                ft.Container(content=ft.Column(elements,
                          alignment=ft.MainAxisAlignment.END,spacing=0,
                          horizontal_alignment=ft.MainAxisAlignment.CENTER,
                          ), height=450, border_radius=15, padding=ft.padding.only(bottom=10)),
            ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.MainAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(5,5,5,10),
            alignment=ft.alignment.center,
            bgcolor="white",
            width=200,
            height=500,
            border_radius=10,
            key = key,
        )

class Jadwal_Card_Table(ft.Row):
    def __init__(self, Page):
        
        self.Page = Page
        
        self.Jadwal_Element_List = []
        self.Jadwal_Card_List = [] 
        
        self.Scroll_Idx = datetime.date.today().day
        
        # New_Jadwal_Element = [
        #         Jadwal_Element("#6a8c65", f"{-1}", self.Page, self), 
        #         Jadwal_Element("#547250", f"{-1}", self.Page, self), 
        #         Jadwal_Element("#6a8c65", f"{-1}", self.Page, self)
        #         ]
        # New_Jadwal_Card = Jadwal_Card(f"{-2}", New_Jadwal_Element)
        # self.Jadwal_Card_List.append(New_Jadwal_Card)
        # New_Jadwal_Card = Jadwal_Card(f"{-1}", New_Jadwal_Element)
        # self.Jadwal_Card_List.append(New_Jadwal_Card)
        # New_Jadwal_Card = Jadwal_Card(f"{0}", New_Jadwal_Element)
        # self.Jadwal_Card_List.append(New_Jadwal_Card)
            
    
        for i in range(1, Max_Date+1):
            
            New_Jadwal_Element = [
                Jadwal_Element("#6a8c65", f"{(i-1)*3 + 1}", self.Page, self), 
                Jadwal_Element("#547250", f"{(i-1)*3 + 2}", self.Page, self), 
                Jadwal_Element("#6a8c65", f"{(i-1)*3 + 3}", self.Page, self)
                ]
            
            New_Jadwal_Card = Jadwal_Card(f"{i}", New_Jadwal_Element)
            
            self.Jadwal_Element_List.append(New_Jadwal_Element)
            self.Jadwal_Card_List.append(New_Jadwal_Card)
        
        super().__init__(
            self.Jadwal_Card_List, 
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                scroll=ft.ScrollMode.ALWAYS
        )
        
    def Set(self, tgl, waktu, makanan, id_jadwal):
        self.Jadwal_Element_List[tgl-1][waktu-1].Set_Jadwal(makanan)
        self.Jadwal_Element_List[tgl-1][waktu-1].key = str(id_jadwal)
        
    
    
    def Delete(self, Id):
        
        for i in range(Max_Date):
            for j in range(3):
                # print(self.Jadwal_Element_List[i][j].key)
                # print(Id, self.Jadwal_Element_List[i][j].key)
                if (int(self.Jadwal_Element_List[i][j].key) == int(Id)):
                    # print("Ketemu!")
                    self.Jadwal_Element_List[i][j].Set_Jadwal(Makanan(" "))
                    self.Jadwal_Element_List[i][j].key = -1
                    self.Page.update()
                    return

    
    def DeleteAll(self):
        for i in range(Max_Date):
            for j in range(3):
                self.Jadwal_Element_List[i][j].Set_Jadwal(Makanan("Bebek"))
                self.Jadwal_Element_List[i][j].key = -1
        self.Page.update()
        
    def SetAll(self):
        for i in range(Max_Date):
            for j in range(3):
                self.Jadwal_Element_List[i][j].Set_Jadwal(Makanan("Ayam"))
                print(self.Jadwal_Element_List[i][j])
                self.Jadwal_Element_List[i][j].key = 1000
        self.Page.update()

class Jadwal(ft.Container):
    def __init__(self, Page):
        
        self.Page = Page
        self.Jadwal_Title = Jadwal_Title()
        self.Jadwal_Card_Table = Jadwal_Card_Table(self.Page)
        self.Tambah_Jadwal_Button = Tambah_Jadwal_Button(self.Page, self.Jadwal_Card_Table)
        self.Scroll_Button = Scroll_Button(self.Jadwal_Card_Table, self)
        
        super().__init__(
            width=ft.Page.window_width,
            alignment=ft.alignment.center,
            content=(ft.Container(
                content=ft.Column(
                            [ft.Row(
                                [ft.Container(
                                    content=self.Jadwal_Title, 
                                    margin=ft.Margin(15,0,0,0), width=300, alignment=ft.alignment.center_left), 
                                ft.Container(
                                    content=self.Scroll_Button, 
                                    width=200, alignment=ft.alignment.center),  
                                ft.Container(content=
                                    ft.Row([self.Tambah_Jadwal_Button], width=300, alignment=ft.MainAxisAlignment.END), 
                                    margin=ft.Margin(0,0,15,0), width=300, alignment=ft.alignment.center_right)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=1050, height=50), 
                            self.Jadwal_Card_Table
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                padding=0,
                margin=ft.margin.only(0,10,0,5),
                alignment=ft.alignment.Alignment(0, 1),
                bgcolor=ft.colors.GREY_200,
                width=1050,
                height=600,
                border_radius=10,
                shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color="black",
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER),
                )
            )
        )
        
        self.db_manager = DatabaseManager()
        
    def InitDatas(self):
        
        self.Jadwal_Title.value = f"Jadwalku ({Month[Month_Show-1]})"
        self.Jadwal_Card_Table.DeleteAll()
        self.list_jadwal = self.db_manager.get_jadwal_bulan("{:02}".format(Month_Show))
        self.list_makanan = self.db_manager.get_all_makanan()
        # self.Jadwal_Card_Table.SetAll()
        
        for jadwal in self.list_jadwal:
            if (jadwal.id_jadwal < 101):
                continue
            print(jadwal)
            self.Jadwal_Card_Table.Set(jadwal.getHari(), jadwal.getKategori(), jadwal.makanan, jadwal.id_jadwal)
        

        
        # self.Jadwal_Card_Table.Set(19, 2, Makanan(nama="Gado-gado"), 2)
            

        
        self.Page.update()
            
class Page_Jadwal(ft.View):
    def __init__(self, Page):
        super().__init__(
            "/Jadwal",
            controls=[
                NavBar("Jadwal", Page), Jadwal(Page)
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START,
            bgcolor="#222222",
        )
    
    def init_scroll(self):
        self.controls[1].Jadwal_Card_Table.scroll_to(key=f"{self.controls[1].Jadwal_Card_Table.Scroll_Idx}", duration=1000)
