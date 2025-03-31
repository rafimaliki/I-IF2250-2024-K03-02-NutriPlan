import customtkinter as ctk
from db import DatabaseManager  # Import the DatabaseManager class

# Page class
class Page(ctk.CTkFrame):
    def __init__(self, master, title, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.title_label = ctk.CTkLabel(self, text="Page "+title, font=("Helvetica", 18))
        self.title_label.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.1, anchor="center")

       

class MakananPage(Page):
    def __init__(self, master, title, db_manager):
        super().__init__(master, title, db_manager)
        self.create_widgets()

    def create_widgets(self):
        makanan_label = ctk.CTkLabel(self, text="Daftar Makanan", font=("Helvetica", 14))
        makanan_label.place(relx=0.5, rely=0.2, anchor="center")

        # Buat textbox tempat nyimpen list makanan
        makanan_list = ctk.CTkTextbox(self)
        makanan_list.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.6, anchor="center")
        
        # Ambil list of makanan dari database
        makanan_data = self.db_manager.get_makanan_value()
        for makanan in makanan_data:
            makanan_list.insert("end", makanan[1] + "\n")  # Assuming the first column contains makanan names

# Navbar class
class Navbar(ctk.CTkFrame):
    def __init__(self, master, pages, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pages = pages
        self.create_widgets()

    def create_widgets(self):
        for page_name, page_class in self.pages.items():
            button = ctk.CTkButton(self, text=page_name,
                                   command=lambda name=page_name: self.show_page(name))
            button.pack(side="left", padx=10, pady=10)

    def show_page(self, page_name):
        for page in self.pages.values():
            page.place_forget()
        page = self.pages[page_name]
        page.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")
        page.tkraise()

# NutriPlanApp class
class NutriPlanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nutri Plan")
        self.geometry("800x600") 
        self.resizable(False, False)  

        self.db_manager = DatabaseManager('tes.db')  # Initialize DatabaseManager
        #Init table 
        self.db_manager.create_table()
        self.db_manager.create_table_makanan()



        # self.db_manager.insert_user("Halo",32)
        # self.db_manager.insert_makanan("NasiGoreng")
        # self.db_manager.insert_makanan("Sopbuah")

        self.page_frame = ctk.CTkFrame(self)
        self.page_frame.pack(fill="both", expand=True)

        self.pages = {}

        self.pages["Jadwal"] = Page(self.page_frame, "Jadwal", self.db_manager)
        self.pages["Makanan"] = MakananPage(self.page_frame,"Makanan",self.db_manager)
        self.pages["Belanja"] = Page(self.page_frame, "Belanja", self.db_manager)
        self.pages["Riwayat"] = Page(self.page_frame, "Riwayat", self.db_manager)

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")
            
        self.navbar = Navbar(self, self.pages)
        self.navbar.place(relx=0.5, rely=0.0, anchor="n")

        self.pages["Jadwal"].tkraise()

# Run 
if __name__ == "__main__":
    app = NutriPlanApp()
    app.mainloop()
