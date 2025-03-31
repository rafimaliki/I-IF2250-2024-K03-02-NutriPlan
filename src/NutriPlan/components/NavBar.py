import flet as ft

def ClickEvent(page, title):
    page.go('/'+title)
    page.update()
    page.title = "NutriPlan: " + title
        
def NavBarItem(title: str, img: ft.icons, isClicked:bool, page:ft.Page)->ft.IconButton:
    
    return ft.IconButton(
            width=60,
            height=45,
            icon=img,
            icon_size=25,
            tooltip=title,
            icon_color= "white" if isClicked else "#C0C0C0",
            hover_color="#547250",
            bgcolor="#435b40",
            on_click=lambda _: ClickEvent(page, title)
            )

pages = ["Jadwal","Makanan","Riwayat","Belanja"]

def NavBar(currPage:str, page:ft.Page)->ft.AppBar:
    return ft.Container(
        width=ft.Page.window_width,
        height=60,
        alignment=ft.alignment.center,
        content=ft.Container(
            content=
                ft.Row([ft.Row([
                                ft.Text("    NutriPlan", size=25, weight=ft.FontWeight.BOLD, color="#242424", font_family="Kanit")],
                               alignment=ft.MainAxisAlignment.START),
                        ft.Row([NavBarItem("Jadwal", ft.icons.CALENDAR_VIEW_MONTH_SHARP, currPage == pages[0], page),
                                NavBarItem("Makanan", ft.icons.DINNER_DINING_SHARP, currPage == pages[1], page),
                                NavBarItem("Riwayat", ft.icons.HISTORY_TOGGLE_OFF_SHARP, currPage == pages[2], page),
                                NavBarItem("Belanja", ft.icons.SHOPPING_CART_CHECKOUT_SHARP, currPage == pages[3], page)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=20,)
                               ],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="white",
            border_radius=30,
            height=60,
            width=500,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color="black",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )
    )