from flet import UserControl, Page, app
from database.db import DatabaseManager
from pages.Jadwal import Page_Jadwal
from pages.Makanan import Page_Makanan
from pages.Riwayat import Page_Riwayat
from pages.Belanja import Page_Belanja
from pages.Loading import Page_Loading
import time

def main(page: Page):
    page.title = "Nutri Plan"
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "fonts/OpenSans-Regular.ttf",
    }
    page.window_maximized = True

    db_manager = DatabaseManager()
    
    page.views.clear()
    
    pages = {
        "/Jadwal": Page_Jadwal(page),
        "/Makanan": Page_Makanan(page),
        "/Riwayat": Page_Riwayat(page),
        "/Belanja": Page_Belanja(page),
        "/Loading": Page_Loading(page)
    }
  
    def route_change(route):
        print("Route change to", route.route) 
        if route.route == "/Riwayat":
            pages["/Riwayat"] = Page_Riwayat(page)
        page.views.clear()
        page.views.append(pages[route.route])
        page.update()
        if route.route == "/Jadwal":
            pages["/Jadwal"].init_scroll()
            pages["/Jadwal"].controls[1].InitDatas()

    page.views.append(pages["/Loading"])
    page.on_route_change = route_change
    page.update()
    
    pages["/Loading"].scroll_to_title()
    time.sleep(1.5)
    pages["/Loading"].scroll_to_end()
    time.sleep(0.6)
    
    page.views.clear()
    page.views.append(pages["/Jadwal"])
    page.update()
    pages["/Jadwal"].init_scroll()
    pages["/Jadwal"].controls[1].InitDatas()

if __name__ == "__main__":        
    app(target=main)
