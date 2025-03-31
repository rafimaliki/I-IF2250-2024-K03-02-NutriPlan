import flet as ft
    
class Page_Loading(ft.View):
    def __init__(self, Page):
        super().__init__(
            "/Loading",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer_start"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="title"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("NutriPlan", font_family="Kanit", size=70, color="white", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("Your daily meal planner", font_family="Open Sans", size=30, color="#E5E4E2", italic=True, key="subtitle"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer", width=1980),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer"),
                        ft.Text("         ", font_family="Kanit", size=70, color="#E5E4E2", weight=ft.FontWeight.BOLD, key="buffer_end"),
                    ], 
                                      alignment=ft.MainAxisAlignment.CENTER, 
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                                      spacing=0,
                                      scroll=ft.ScrollMode.HIDDEN),      
                    
                    width=1920,
                    height=1080,
                    bgcolor="#547250",
                    alignment=ft.alignment.center,
                    
                )
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START,
            bgcolor="#222222",
        )
        
    def scroll_to_start(self):
        self.controls[0].content.scroll_to(key="buffer_start", duration=1000)
        
    def scroll_to_title(self):
        self.controls[0].content.scroll_to(key="title", duration=1000)
        
    def scroll_to_end(self):
        self.controls[0].content.scroll_to(key="buffer_end", duration=1000)