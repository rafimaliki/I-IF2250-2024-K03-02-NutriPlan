import flet as ft
from components.NavBar import NavBar
from database.db import DatabaseManager

PAGE = None
db_manager = DatabaseManager()

class Task(ft.UserControl):
    def __init__(self, task_name):
        super().__init__()
        self.task_name = task_name

    def build(self):
        flag = self.task_name[2] == 1
        self.display_task = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Checkbox(
                                value=flag,
                                label=self.task_name[4],
                                check_color=ft.colors.BLACK,
                                adaptive=True,
                                label_style=ft.TextStyle(
                                    color=ft.colors.BLACK,
                                    size=22,
                                    font_family="Kanit",
                                    weight=ft.FontWeight.NORMAL
                                ),
                                on_change=lambda e: checkbox_changed(self.task_name[2], self.task_name[0], e),
                            ),
                            ft.Text(
                                self.task_name[1],
                                style=ft.TextStyle(
                                    color=ft.colors.GREY_600,
                                    size=14,
                                    font_family="Kanit",
                                ),
                            )
                        ],
                        spacing=5,
                    ),
                    ft.Container(
                        content=ft.IconButton(
    
                        icon='delete_outline',
                        icon_size=24,
                        on_click=lambda e: self.delete_task()
                    ),
                        expand=True,
                        alignment=ft.alignment.center_right,
                    ),
                    
                    
                ],
                expand=True
            ),
            padding=15,
            margin=8,
            border_radius=12,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(3, "#547250"),
            shadow=ft.BoxShadow(blur_radius=6, spread_radius=2, color=ft.colors.GREY_300),
            expand=True
        )

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.display_task],
        )

        return ft.Column(controls=[self.display_view])

    def delete_task(self):
        db_manager.delete_daftar_belanja(self.task_name[0])
        reload_data()

class TodoList(ft.UserControl):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks

    def build(self):
        task_controls = [Task(task_name) for task_name in self.tasks]
        return ft.Column(
            controls=task_controls,
            spacing=15,
            scroll='always',
            expand=True,  
        )

    def update_tasks(self, tasks):
        self.tasks = tasks
        self.update()

def reload_data():
    tasks = db_manager.join_two_table('daftar_belanja', 'bahan_baku', 'barang', 'id_bahan')
    global todo_list
    todo_list.update_tasks(tasks)
    PAGE.update()

task = db_manager.join_two_table('daftar_belanja', 'bahan_baku', 'barang', 'id_bahan')
todo_list = TodoList(task)

def checkbox_changed(val, id_bahan, e):
    if val:
        db_manager.update_data_shopping('daftar_belanja', 'sudah_dibeli', id_bahan, 0)
    else:
        db_manager.update_data_shopping('daftar_belanja', 'sudah_dibeli', id_bahan, 1)
    reload_data()



def Page_Belanja(page):
    global PAGE, todo_list
    PAGE = page
    
    return ft.View(
        "/Belanja",
        controls=[
            NavBar("Belanja", page),
            ft.Container(
                padding=30,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREY_100,
                width=1200,
                height=800,
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Daftar Belanja",
                            style=ft.TextStyle(
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                font_family="Kanit",
                                color=ft.colors.GREY_800
                            ),
                        ),
                        ft.Container(
                            content=todo_list,
                            expand=True,
                        ),
                        ft.ElevatedButton(
                            text="Refresh",
                            on_click=lambda e: reload_data()
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    expand=True,  # Ensure the column expands to use available space
                )
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=26,
        bgcolor=ft.LinearGradient(
            colors=[ft.colors.BLUE_50, ft.colors.BLUE_100],
            stops=[0.0, 1.0],
        )
    )
