from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class PieChartCanvas(FigureCanvasQTAgg):
    def __init__(self, distribution):
        fig = Figure(figsize=(4, 4))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)

        labels = distribution.keys()
        sizes = distribution.values()

        self.ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        self.ax.set_title("Equipment Distribution")

class BarChartCanvas(FigureCanvasQTAgg):
    def __init__(self, distribution):
        fig = Figure(figsize=(5, 4))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)

        labels = list(distribution.keys())
        values = list(distribution.values())

        self.ax.bar(labels, values)
        self.ax.set_title("Equipment Count")
        self.ax.tick_params(axis='x', rotation=30)
