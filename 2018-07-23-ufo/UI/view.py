import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._btnPercorso = None
        self._btn_graph = None
        self.ddShape = None
        self._btnSelezionaAnno = None
        self.txtInYear = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Esame 23-07-2018 Turno A", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1
        self.txtInYear = ft.TextField(label="Anno (da 1919 a 2014, estremi inclusi)", width=500)
        self._btnSelezionaAnno = ft.ElevatedButton(text="Seleziona Anno", on_click=self._controller.fillDD)
        row1 = ft.Row([self.txtInYear, self._btnSelezionaAnno],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # ROW 2
        self.ddShape = b = ft.Dropdown(label="Forma", width=500)
        self._btn_graph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handle_graph,
                                            disabled=True)
        row2 = ft.Row([self.ddShape, self._btn_graph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # ROW 3
        self._btnPercorso = ft.ElevatedButton(text="Calcola Percorso", on_click=self._controller.handleSimula)
        row3 = ft.Row([self._btnPercorso], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
