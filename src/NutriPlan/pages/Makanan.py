import flet as ft
from components.NavBar import NavBar
from database.db import DatabaseManager
import time

PAGE = None
isOnEdit = None
lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
db_manager = DatabaseManager()
edit_container = None
ijo = "#547250"
black = "#000000"  




def handle_empty_textfield(textfield, warning_message):
    """
    Check if the TextField is empty and display a warning if it is.
    
    Parameters:
        textfield (ft.TextField): The TextField to check.
        warning_message (str): The warning message to display.
    """
    if textfield.value.strip() == "":
        # Display a warning message
        PAGE.snack_bar = ft.SnackBar(ft.Text(warning_message))
        PAGE.snack_bar.open = True
        PAGE.update()
        return True  # Indicates that the TextField is empty
    else:
        return False  # Indicates that the TextField is not empty
#=========================EDIT CONTAINER SEGMENT============================
def build_bb_edit_field(nama_bahan):
    return ft.Container(width=175,content =ft.TextField(
    label="Bahan baku  ",value= nama_bahan))
def build_qq_edit_field(kuantitas):
    return ft.Container(width=90,content =ft.TextField(
        label="Kuantitas ",value = kuantitas))








def insert_makanan_value(e):
    nama_makanan = makanan_field.value
    deskripsi = deskripsi_field.value
    cara_buat = field_cara_buat.value
    if(handle_empty_textfield(makanan_field,"Nama Makanan tak boleh kosong!")):
        return

    max_id = db_manager.get_max_makanan_id() + 1
    db_manager.insert_resep(cara_buat)  
    db_manager.insert_makanan(nama_makanan, deskripsi, max_id) #resepid + 1
    
    process_bahan_lv(lv_bahan,max_id )
    

    lv.controls.clear()
    close_dlg(e)
    get_makanandb_list(lv)

    PAGE.snack_bar = ft.SnackBar(ft.Text(f"{nama_makanan} Berhasil disimpan!"))
    PAGE.snack_bar.open = True
    PAGE.update()

def show_edit_container(val,desk,cara,id_makanan,e):
    global edit_container,isOnEdit,lv_bahan_edit
    if isOnEdit is not None:
        temp = e.control
        if not isOnEdit == temp:
            isOnEdit.selected = False
        
    e.control.selected = not e.control.selected

    edit_container.content = build_edit_container(val,desk,cara,id_makanan).content
    if(e.control.selected == True):
        edit_container.visible = False
        e.control.selected = False
        
    else:
        edit_container.visible = True
        e.control.selected = True
        isOnEdit = e.control

    PAGE.update()



    

def build_edit_container(val,desk,cara,id_makanan):
    global isOnEdit
    lv_bahan_edit = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
    
    def build_container_bb_qq_edit(nama_bahan,kuantitas):

        container_bb_qq = ft.Container(
            content = ft.Row([
                build_bb_edit_field(nama_bahan),
                build_qq_edit_field(kuantitas)

            ],spacing=10)
        )
        return container_bb_qq
    def build_lv_bahan_edit():
        bbqq_value = db_manager.get_detail_resep_from_id(id_makanan)
        valid_value = len(bbqq_value)
        for i in range(10):
            if(i < valid_value):
                lv_bahan_edit.controls.append(build_container_bb_qq_edit(bbqq_value[i][0],bbqq_value[i][1]))
            else:
                lv_bahan_edit.controls.append(build_container_bb_qq_edit("",""))
    build_lv_bahan_edit()
    


    def process_bahan_lv_edit(lv):
        
        list_bb_qq = []
        for control in lv.controls:
            valuebbqq = []
            i = 0
            bb = ""
            qq = ""
            for sub_control in control.content.controls:
                value = sub_control.content.value
                if value != "":
                    if i == 0:
                        # #print("Bahan baku : ", value)
                        bb = value
                    else:
                        # #print("Kuantitas : ", value)
                        qq = value
                i += 1

            if bb != "" and qq != "":   
                db_manager.insert_if_not_exists('bahan_baku', 'nama_bahan', bb)
                valuebbqq.append(bb)
                valuebbqq.append(qq)

            list_bb_qq.append(valuebbqq)
                
        db_manager.update_detail_resep(id_makanan,list_bb_qq)

    

    

    container_title_makanan = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Text(value=val, font_family="Kanit", color="black")
        
    )
    container_gambar_makanan = ft.Container(
        bgcolor= ft.colors.WHITE,
        height= 200,
        width= 310,
        border_radius= 5,
        alignment=ft.alignment.center,
        border= ft.border.all(1,ft.colors.BLACK),
        content = lv_bahan_edit
    )
    def update_makanan(e):
        updated_nama_makanan = field_nama_makanan.value
        updated_deskripsi_makanan = field_deskripsi_makanan.value
        updated_cara_membuat = field_cara_buat.value

        # print("Updating makanan with ID:", id_makanan)
        # print("Nama Makanan:", updated_nama_makanan)
        # print("Deskripsi:", updated_deskripsi_makanan)
        # print("Cara Membuat:", updated_cara_membuat)

        db_manager.update_table_by_id('makanan', 'id_makanan', id_makanan, 'nama', updated_nama_makanan)
        db_manager.update_table_by_id('makanan', 'id_makanan', id_makanan, 'deskripsi', updated_deskripsi_makanan)
        db_manager.update_table_by_id('resep', 'id_resep', id_makanan, 'cara_membuat', updated_cara_membuat)
        process_bahan_lv_edit(lv_bahan_edit)
        # Update page
        lv.controls.clear()
        get_makanandb_list(lv)
        PAGE.snack_bar = ft.SnackBar(ft.Text(f"Informasi makanan berhasil disimpan! :D "))
        PAGE.snack_bar.open = True
        PAGE.update()

    def delete_makanan(e):
        global isOnEdit
        db_manager.delete_element_by_id('makanan','id_makanan',id_makanan)
        #Harusnya udah cascade di table db, cuma gk tau kenapa gk work, jadi gini dulu aja, didelete manual
        db_manager.delete_element_by_id('resep','id_resep',id_makanan)
        db_manager.delete_element_by_id('detail_resep','id_resep',id_makanan)


        lv.controls.clear()
        get_makanandb_list(lv)
        isOnEdit = None
        edit_container.visible = False
        PAGE.snack_bar = ft.SnackBar(ft.Text(f" Makanan berhasil dihapus!"))
        PAGE.snack_bar.open = True
        PAGE.update()


        
              
    field_nama_makanan = ft.TextField(value=val,label="Nama Makanan",icon=ft.icons.DINNER_DINING,border=ft.InputBorder.UNDERLINE, color="black")
    field_deskripsi_makanan= ft.TextField(value=desk,label="Deskripsi",icon = ft.icons.EDIT_OUTLINED,border=ft.InputBorder.UNDERLINE, color="black")
    field_cara_buat= ft.TextField(value = cara,hint_text="Cara membuat...",label="Cara buat",multiline=True,min_lines=5,max_lines=5, color="black")

    simpan_button = ft.Container(
                    padding=10,
                    alignment=ft.alignment.center,
                    height=40,
                    width=100,
                    border_radius=10,
                    bgcolor=ijo,
                    on_click=update_makanan,
                    content=ft.Text(value="Simpan", color=ft.colors.BLACK,font_family="Kanit"),
                )
    hapus_button =  ft.Container(
                    padding=10,
                    alignment=ft.alignment.center,
                    height=40,
                    width=100,
                    border_radius=10,
                    on_click=delete_makanan,
                    bgcolor= ft.colors.RED,
                    content=ft.Text(value="Hapus", color=ft.colors.BLACK,font_family="Kanit"),
                )
    container_button_option_makanan =  ft.Container(content = 
        ft.Row([
            simpan_button,
            hapus_button

        ],
        alignment=ft.MainAxisAlignment.CENTER,spacing=20)
    )
    container_edit_makanan = ft.Container(border_radius=10, height=400, width=400, bgcolor=ft.colors.WHITE,padding= 15,
                                          content = ft.Column([
                                              field_nama_makanan,
                                              field_deskripsi_makanan,
                                              field_cara_buat,
                                              container_button_option_makanan
                                              
                                              
                                          ],
                                          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                          spacing= 20
                                          ))
    
    return ft.Container(
        bgcolor=ft.colors.GREY_200, width=400, height=700,
        border_radius=10,
        padding=20,
        content=ft.Column([
            ft.Container(border_radius=10, height=250, width=400, bgcolor=ft.colors.GREY_100,padding=10,
                         content=ft.Column([
                             container_title_makanan,
                             container_gambar_makanan,
                         ],horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
            container_edit_makanan
        ])
    )




#================================PER DLG AN======================================
def open_dlg(e):
    PAGE.dialog = dlg
    lv_bahan.controls.clear()
    build_bahan_baku()
    dlg.open = True
    PAGE.update()
    

def close_dlg(e):
    dlg.open = False
    PAGE.update()

makanan_field = ft.TextField(
    label="Makanan: ",icon = ft.icons.DINNER_DINING,border=ft.InputBorder.UNDERLINE, color="black"
)
deskripsi_field = ft.TextField(
    label="Deskripsi: ",icon= ft.icons.EDIT_OUTLINED,border=ft.InputBorder.UNDERLINE, color="black"
)

def build_bb_field():
    return ft.Container(width=300,content =ft.TextField(
    label="Bahan baku  ",color="black"))
def build_qq_field():
    return ft.Container(width=100,content =ft.TextField(
        label="Kuantitas " ,color="black"))
field_cara_buat= ft.TextField(hint_text="Cara membuat...",label="Cara buat",multiline=True,min_lines=15,max_lines=15,color="black")
lv_bahan = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)



def build_container_bb_qq():

    container_bb_qq = ft.Container(
        content = ft.Row([
            build_bb_field(),
            build_qq_field()

        ],spacing=10)
    )
    return container_bb_qq

listbbqq =[]
for i in range(10):
    listbbqq.append(build_container_bb_qq())


def build_bahan_baku():
    lv_bahan.controls.clear()
    for i in range(10):
        lv_bahan.controls.append(listbbqq[i])

        

row_bahan_cara_buat = ft.Container(content =
                                   ft.Row([
                                       field_cara_buat,
                                       ft.Container(content = lv_bahan,height= 400,width=450,
                                                    bgcolor=ft.colors.GREY_100,
                                                    padding= 10,
                                                    border_radius=10),

                                   ]))

add_food_container = ft.Container(
    content=ft.Column([
        ft.Container(
            padding=20,
            bgcolor=ft.colors.GREY_200,
            height=600,
            width=800,
            border_radius=10,
            content=ft.Column([
                makanan_field,
                deskripsi_field,
                row_bahan_cara_buat
            ],spacing = 10)
        ),
        ft.Container(
            padding=10,
            alignment=ft.alignment.bottom_right,
            content=ft.Row([
                ft.Container(
                    padding=10,
                    alignment=ft.alignment.center,
                    height=40,
                    width=150,
                    border_radius=10,
                    bgcolor=ijo,
                    content=ft.Text(value="Tambah", color=ft.colors.WHITE),
                    on_click=insert_makanan_value
                ),
                ft.Container(
                    padding=10,
                    alignment=ft.alignment.center,
                    height=40,
                    width=150,
                    border_radius=10,
                    bgcolor=ijo,
                    on_click=close_dlg,
                    content=ft.Text(value="Tutup", color=ft.colors.WHITE),
                )
            ],alignment = ft.MainAxisAlignment.CENTER)
        )
    ])
)
dlg = ft.AlertDialog(
    on_dismiss=lambda e: print("Dialog dismissed!"),
    content=add_food_container,
    surface_tint_color = ft.colors.GREY_200,
)

def process_bahan_lv(lv,sum_food):
    for control in lv.controls:
        i = 0
        bb = ""
        qq = ""
        for sub_control in control.content.controls:
            value = sub_control.content.value
            if value != "":
                if i == 0:
                    bb = value
                else:
                    qq = value
            i += 1
        
        if bb != "" and qq != "":
            if db_manager.insert_if_not_exists('bahan_baku', 'nama_bahan', bb):
                id_bahan = db_manager.get_id_from_bahan(bb)
                if id_bahan is not None:
                    db_manager.insert_detail_resep(sum_food, id_bahan, qq)
                else:
                    print(f"Error: Bahan baku '{bb}' tidak ditemukan setelah insert.")




            





# =======================================MAIN SEGMENT=================================================
def get_makanandb_list(lv):
    global isOnEdit
    food_list = db_manager.join_tables("makanan","resep","makanan.cara_buat = resep.id_resep","id_makanan, nama, deskripsi, cara_membuat")
    plus_button = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ADD_BOX,
            icon_color="#547250",
            icon_size=50,
            tooltip="Tambah Makanan",
            on_click=open_dlg
        ),
        bgcolor=ft.colors.GREY_100,
        border_radius=5,
        padding=10
    )
    def create_edit_button(val,desk,cara,id_makanan):
        def on_click_handler(e):
            e.control.selected = not e.control.selected
            e.control.update()
            show_edit_container(val, desk,cara,id_makanan, e)

        
        edit_button = ft.Container(
            content=ft.IconButton(
                icon=ft.icons.EDIT,
                icon_color=ft.colors.WHITE,
                selected_icon= ft.icons.EDIT,
                selected_icon_color= ft.colors.GREEN,
                bgcolor= "#547250",
                icon_size=30,
                tooltip="Edit Makanan",
                on_click=on_click_handler,
                highlight_color= ft.colors.GREEN_200,
                selected= False,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=5,
            padding=10
        )
        return edit_button
    
    def create_delete_button():
        delete_button = ft.Container(
            content=ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.WHITE,
                icon_size=30,
                tooltip="Hapus Makanan Makanan",
                bgcolor= ft.colors.RED_100,
                alignment=  ft.alignment.center_right,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=5,
            padding=10
        )
        return delete_button

    

    i = 0
    for makanan in food_list:
        if (i > 0):
            food_container = ft.Container(
                content=ft.Row([
                    create_edit_button(makanan[1],makanan[2],makanan[3],makanan[0]), #dapetin nama makanan sama deskripsi buat edit button
                    ft.Column([
                        ft.Text(
                            makanan[1],
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            text_align=ft.TextAlign.CENTER,
                            font_family="Kanit",
                            color="black",
                        ),
                        ft.Text(
                            makanan[2],
                            theme_style=ft.TextThemeStyle.BODY_SMALL,
                            text_align=ft.TextAlign.CENTER,
                            color="black",
                        ),
                    ], alignment=ft.alignment.center),
                ]),
                bgcolor=ft.colors.WHITE,
                border_radius=5,
                padding=10
            )
            lv.controls.append(food_container)
        i += 1

    lv.controls.append(plus_button)
    PAGE.update()

def click_edit_makanan(edit_container):
    if edit_container.visible:
        edit_container.visible = True
    else:
        edit_container.visible = False

makanan_list_container = ft.Container(
                    margin=0,
                    padding=20,
                    bgcolor=ft.colors.GREY_200,
                    width=960,
                    height=700,
                    border_radius=10,
                    content=lv,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color="black",
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER
                    )
                )

def Page_Makanan(page):
    global PAGE, lv, edit_container,isOnEdit,lv_bahan
    PAGE = page

    get_makanandb_list(lv)
    PAGE.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )

    

    edit_container = ft.Container(
        bgcolor=ft.colors.GREY_200, width=400, height=700,
        border_radius=10,
        padding=20,
        visible=False,  
        content=ft.Column([
            ft.Container(border_radius=10, height=200, width=400, bgcolor=ft.colors.GREY_100,
                         content=ft.Text(value='Tes')),
            ft.Container(border_radius=10, height=500, width=400, bgcolor=ft.colors.WHITE)
        ])
    )

    return ft.View(
        "/Makanan",
        controls=[
            NavBar("Makanan", page),
            ft.Container(
                content = ft.Row(
                [
                    makanan_list_container,
                    edit_container
                ]
                ,alignment=ft.MainAxisAlignment.CENTER)
            )
            
        ],
        
        spacing=26,
        bgcolor="#222222"
    )   
