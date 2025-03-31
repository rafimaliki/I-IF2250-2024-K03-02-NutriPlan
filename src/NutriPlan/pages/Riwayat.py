import flet as ft
# from components.NavBar import BoxIconNavBar
from components.NavBar import NavBar
from components.HistTable import *

def Page_Riwayat(page):
    return ft.View(
        "/Riwayat",
        controls=[
            NavBar("Riwayat", page),
            HistTable(page)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=26,
        bgcolor="#222222"
    )
