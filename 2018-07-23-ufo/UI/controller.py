import flet as ft # 1
from geopy.distance import distance


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self, e):
        anno = self._view.txtInYear.value
        try:
            anno = int(anno)
        except ValueError:
            self._view.create_alert("Attenzione! Inserire un numero intero tra 1910 e 2014, estremi inclusi")
            self._view.update_page()
            return
        if anno is None:
            self._view.create_alert("Inserire un anno nel campo Anno!")
            self._view.update_page()
            return
        else:
            if int(anno) < 1910 or int(anno) > 2014:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(
                    ft.Text("l'anno deve essere compreso tra 1910 e 2014, estremi inclusi"))
                self._view.update_page()
                return
            else:
                forme = self._model.getShapes(anno)
                for f in forme:
                    self._view.ddShape.options.append(ft.dropdown.Option(f))
                    self._view._btn_graph.disabled = False
                self._view.update_page()

    def handle_graph(self, e):
        year = self._view.txtInYear.value
        shape = self._view.ddShape.value
        if shape is None:
            self._view.create_alert("Seleziona una forma")
            self._view.update_page()
            return
        else:
            grafo = self._model.buildGraph(shape, year)
            if grafo:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!", color='green'))
                self._view.txt_result.controls.append(ft.Text(self._model.printGraphDetails()))
                sWN = self._model.sumWeightNeighbours()
                for k, v in sWN:
                    self._view.txt_result.controls.append(ft.Text(f"Nodo {k}, somma pesi su archi = {v}"))
                self._view.update_page()
            else:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo", color='red'))
                self._view.update_page()
                return

    def handleSimula(self, e):
        cammino = self._model.getPath()
        self._view.txt_result.controls.append(ft.Text(f"Peso cammino massimo :{cammino[1]}"))
        self._view.update_page()
        for i in range(0, len(cammino[0]) - 1):
            self._view.txt_result.controls.append(
                ft.Text(f"{cammino[0][i].id}-->{cammino[0][i + 1].id}, peso: {self._model._grafo[cammino[0][i]][cammino[0][i + 1]]["weight"]}, distance: {distance((cammino[0][i].Lat, cammino[0][i].Lng), (cammino[0][i + 1].Lat, cammino[0][i + 1].Lng))}"))
            self._view.update_page()
