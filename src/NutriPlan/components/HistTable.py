import flet as ft
from database.db import DatabaseManager
db = DatabaseManager()

class HistTableEntry(ft.UserControl):
    def __init__(self,page:ft.Page,id,tanggal,makanan)->None:
        global db
        super().__init__()
        if (id%2==0):
            self.bgcolor = "#6A8C65"
        else:
            self.bgcolor = "#9DDE8B"
        self.id = db.get_all_data("daftar_riwayat")[id][0]
        self.tanggalteks = tanggal
        self.makanan = makanan
        self.listRiwayat = db.get_all_data("daftar_riwayat")
        self.listRiwayat = sortDaftarRiwayat(self.listRiwayat,db.get_all_data("jadwal_makanan"))
        self.page = page
        self.dlg : ft.AlertDialog = ft.AlertDialog()
        self.e = ft.ControlEvent
        self.teks = ft.Text(self.listRiwayat[id][1],text_align="center",width=450,size=25,font_family="RobotoSlab",color=ft.colors.BLACK,overflow="elipsis")
        self.textbox = ft.TextField(label="Comment",text_align="center",width=900,height=200, min_lines=4, max_lines=4)
        self.textbox.value = self.teks.value
        self.tanggal = ft.Container(content=ft.Text(self.tanggalteks,size=25,font_family="RobotoSlab",
                                                    text_align="center",overflow="elipsis",color=ft.colors.BLACK ),
                                    height=50,width=300,bgcolor=ft.colors.WHITE70,border_radius=10)
        
        self.makanan = ft.Container(content=ft.Text(self.makanan,size=25,font_family="RobotoSlab",
                                                    text_align="center",overflow="elipsis",color=ft.colors.BLACK),
                                    height=50, width=300,border_radius=10,bgcolor=ft.colors.WHITE70)
        
        self.catatan = ft.Container(content=ft.Row(controls=[self.teks,
                                                             ft.IconButton(icon=ft.icons.EDIT_NOTE_ROUNDED,
                                                                               on_click= self.open,icon_size=30)
                                                            ]
                                                    ),
                                            width=500,height=50,bgcolor=ft.colors.WHITE70,
                                            border_radius=10,
                                            alignment=ft.alignment.Alignment(1,-1)
                                    )
       
    def openDialog(self,e:ft.ControlEvent):
        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Update History Commment"),
            content=ft.Text("Tulis komentar di dalam teks di bawah ini"),
            actions=[self.textbox,
                    ft.Row(
                        controls=[ft.TextButton("Simpan",on_click=self.save),
                                 ft.TextButton("Buang",on_click=self.discard)],  
                    )
                ],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )
        self.page.update()
        self.update()

    def discard(self,e:ft.ControlEvent):
        self.dlg.open = False
        self.textbox.value = self.teks.value
        self.page.update()
        self.update()

    def save(self,e:ft.ControlEvent):
        db.update_daftar_riwayat('daftar_riwayat','catatan',self.id,self.textbox.value)
        self.teks.value = self.textbox.value
        self.textbox.value = self.teks.value
        self.dlg.open = False
        self.page.update()
        self.update()

    def open(self,e:ft.ControlEvent):
        self.openDialog(e)
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()
        self.update()

    
    def build(self):
        return ft.Container(

            content=  ft.Row(
                controls=[
                    self.tanggal,
                    self.makanan,
                    self.catatan,
                  ],
                  alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=30
            ),
            bgcolor=self.bgcolor,
            padding=15,
            margin=0,
            alignment=ft.alignment.center_left,
            width=1200,
            
        )
def getTableName():
    return ft.Container(
        content=
            ft.Row(
                controls=[
                    ft.Container(content=ft.Text("Tanggal",size=30,font_family="RobotoSlab",text_align="center",
                                                 overflow="elipsis", weight=ft.FontWeight.BOLD,color=ft.colors.WHITE),
                                height=50,width=300,border_radius=10),

                    ft.Container(content=ft.Text("Makanan",size=30,font_family="RobotoSlab",text_align="center",
                                                 overflow="elipsis",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE),
                                height=50, width=300,border_radius=10),

                    ft.Container(content=ft.Text("Komentar",size=30,font_family="RobotoSlab",text_align="center",
                                                 overflow="elipsis",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE),
                                width=500,height=50,border_radius=10)
                    
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=30
            )
        ,
        bgcolor="#547250",
        padding=10,
        margin=0,
        alignment=ft.alignment.center_left,
        border_radius = ft.border_radius.vertical(10,0),
        width=1200,

    )
def PastThan(day1, day2):
    day1d = int(day1[0:2])
    day1m = int(day1[3:5])
    day1y = int(day1[6:10])
    day2d = int(day2[0:2])
    day2m = int(day2[3:5])
    day2y = int(day2[6:10])
    return day2d >= day1d and day2m>=day1m and day2y >= day1y

def sortDaftarRiwayat(listHist,listJadwal):
    result = []
    print(listHist)
    print(listJadwal)
    while (len(listHist)>0):
        min = 0
        for i in range(0,len(listHist)):
            if (PastThan(listJadwal[int(listHist[i][0])-100][3],listJadwal[int(listHist[min][0])-100][3])):
                min = i
        result.append(listHist[min])
        listHist.remove(listHist[min])
    return result
def HistTable(page:ft.Page):
    db.auto_update_daftar_riwayat()
    listHist = db.get_all_data("daftar_riwayat")    
    listJadwal = db.get_all_data("jadwal_makanan")
    listMakanan = db.get_all_data("makanan")
    listMakanan.pop(0)
    column = ft.Column(
        controls=[ft.Text("My History",weight=ft.FontWeight.BOLD,font_family="Kanit",
                          color=ft.colors.BLACK,size=30),
                    ft.Text("\n"),
                    getTableName()],  
        spacing=0,
        scroll=ft.ScrollMode.AUTO 
    )
    listHist = sortDaftarRiwayat(listHist,listJadwal)
    for i in range(len(listHist)-1,-1,-1):
        column.controls.append(HistTableEntry(page,i,listJadwal[int(listHist[i][0])-100][3],listMakanan[int(listJadwal[int(listHist[i][0])-100][1])-1][1]))
    # "#006769"
    #"#40A578"
    return ft.Container(
        content=column,
        expand=True,
        bgcolor=ft.colors.GREY_200,
        width=1440,
        padding=30,
        margin=30,
        border_radius=10,
        alignment=ft.alignment.top_center,
        shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color="black",
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER),
    )

