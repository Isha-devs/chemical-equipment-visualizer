import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


plt.style.use("seaborn-v0_8")


class ChartCanvas(FigureCanvas):
    def __init__(self, width=5, height=4):
        self.figure = Figure(figsize=(width, height))
        super().__init__(self.figure)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history = []
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(900, 700)

        # ===== Global Styling =====
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f5f7fa;
        }
        QGroupBox {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            font-size: 14px;
        }
        QPushButton {
            background-color: #4f46e5;
            color: white;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #4338ca;
        }
        QLabel {
            font-size: 13px;
        }
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ===== Upload Button =====
        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)
        main_layout.addWidget(upload_btn, alignment=Qt.AlignCenter)


        # ===== Export Button =====
        export_btn = QPushButton("Export Charts as Images")
        export_btn.clicked.connect(self.export_charts)
        main_layout.addWidget(export_btn, alignment=Qt.AlignCenter)

        # ===== Summary Card =====
        self.summary_box = QGroupBox("Summary")
        self.summary_layout = QVBoxLayout()

        self.total_label = QLabel("Total Equipment: -")
        self.flow_label = QLabel("Avg Flowrate: -")
        self.pressure_label = QLabel("Avg Pressure: -")
        self.temp_label = QLabel("Avg Temperature: -")

        self.summary_layout.addWidget(self.total_label)
        self.summary_layout.addWidget(self.flow_label)
        self.summary_layout.addWidget(self.pressure_label)
        self.summary_layout.addWidget(self.temp_label)

        self.summary_box.setLayout(self.summary_layout)
        main_layout.addWidget(self.summary_box)


        # ===== Upload History =====
        self.history_box = QGroupBox("Last 5 Uploads")
        history_layout = QVBoxLayout()

        self.history_layout = QVBoxLayout()
        history_layout.addLayout(self.history_layout)

        self.history_box.setLayout(history_layout)
        main_layout.addWidget(self.history_box)

        # ===== Pie Chart =====
        self.pie_box = QGroupBox("Equipment Distribution")
        pie_layout = QVBoxLayout()

        self.pie_canvas = ChartCanvas()
        pie_layout.addWidget(self.pie_canvas, alignment=Qt.AlignCenter)

        self.pie_box.setLayout(pie_layout)
        main_layout.addWidget(self.pie_box)

        # ===== Bar Chart =====
        self.bar_box = QGroupBox("Equipment Count")
        bar_layout = QVBoxLayout()

        self.bar_canvas = ChartCanvas(width=7, height = 5)
        bar_layout.addWidget(self.bar_canvas)

        self.bar_box.setLayout(bar_layout)
        main_layout.addWidget(self.bar_box)

        # ===== Scroll Area =====
        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        self.setCentralWidget(scroll)


    def generate_data_quality_report(self, df):
        report = {}

        report["Total Rows"] = len(df)
        report["Total Columns"] = len(df.columns)

        missing = df.isnull().sum()
        report["Missing Values"] = missing.to_dict()

        numeric_cols = df.select_dtypes(include="number")
        report["Statistics"] = numeric_cols.describe().to_dict()

        outliers = {}

        for col in numeric_cols.columns:
            q1 = numeric_cols[col].quantile(0.25)
            q3 = numeric_cols[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5*iqr
            upper = q3 + 1.5*iqr
            outliers[col] = int(
                ((numeric_cols[col] < lower) | 
                 (numeric_cols[col] > upper)).sum()
            )
        
        report["Outliers"] = outliers
        return report


    def validate_csv_schema(self, df):
        required_columns = {
            "Equipment Name",
            "Flowrate",
            "Pressure",
            "Temperature"
        }

        if df.empty:
            raise ValueError("Uploaded CSV file is empty")
        
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )
        

        numeric_columns = ["Flowrate", "Pressure", "Temperature"]
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(
                    f"Column '{col}' must contain numeric values."
                )
            

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return
        

        try:
            df = pd.read_csv(file_path)
            self.validate_csv_schema(df)
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Invalid CSV File",
                str(e)
            )
            return

        quality_report = self.generate_data_quality_report(df)
        self.show_data_quality_report(quality_report)
        

        self.save_to_history(file_path, df.copy())
        self.process_dataframe(df)

       
    
    def process_dataframe(self, df):
        # ===== Summary =====
        total = len(df)
        avg_flow = df["Flowrate"].mean()
        avg_pressure = df["Pressure"].mean()
        avg_temp = df["Temperature"].mean()

        self.total_label.setText(f"<b>Total Equipment:</b> {total}")
        self.flow_label.setText(f"<b>Avg Flowrate:</b> {avg_flow:.2f}")
        self.pressure_label.setText(f"<b>Avg Pressure:</b> {avg_pressure:.2f}")
        self.temp_label.setText(f"<b>Avg Temperature:</b> {avg_temp:.2f}")

        # ===== Equipment Distribution =====
        df["Equipment Name"] = df["Equipment Name"].str.strip()
        df["Type"] = df["Equipment Name"].str.split("-").str[0]

        distribution = df["Type"].value_counts().sort_index()

        self.chart_colors = cm.Set3(range(len(distribution)))

        self.draw_pie_chart(distribution)
        self.draw_bar_chart(distribution)


    def draw_pie_chart(self, distribution):
        self.pie_canvas.figure.clear()
        ax = self.pie_canvas.figure.add_subplot(111)


        wedges, _, _ = ax.pie(
            distribution.values,
            # labels=distribution.index,
            autopct="%1.1f%%",
            startangle=90,
            colors = self.chart_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1},
            textprops={"fontsize": 10}
            
        )
        ax.set_title("Equipment Distribution by Type", fontsize=14)


        ax.legend(
            wedges,
            distribution.index,
            title="Equipment Type",
            loc = "center left",
            bbox_to_anchor = (1, 0.5),
            frameon= False
        )

        self.pie_canvas.draw()

    def draw_bar_chart(self, distribution):
        self.bar_canvas.figure.clear()

        self.bar_canvas.figure.set_size_inches(12, 6)

        ax = self.bar_canvas.figure.add_subplot(111)

        x_pos = range(len(distribution))

        bars = ax.bar(
            x_pos,
            distribution.values,
            color=self.chart_colors
        )

        ax.set_xlabel("Equipment Type", fontsize=12, labelpad=10)
        ax.set_ylabel("Number of Equipments", fontsize=12)
        ax.set_title("Equipment Count by Type", fontsize=14)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(distribution.index, rotation=30, ha="right")

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.5,
                int(height),
                ha = "center",
                va = "bottom",
                fontsize=10
            )

        self.bar_canvas.figure.tight_layout()

        self.bar_canvas.draw()

    
    def show_data_quality_report(self, report):
        text = "DATA QUALITY REPORT\n\n"
        text += f"Rows: {report['Total Rows']}\n"
        text += f"Columns: {report['Total Columns']}\n\n"

        text += "Missing Values:\n"
        for k, v in report["Missing Values"].items():
            text += f"  {k}: {v}\n"

        text += "\nOutliers:\n"
        for k, v in report["Outliers"].items():
            text += f"  {k}: {v}\n"

        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Data Quality Report", text)

    
    def export_charts(self):
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Folder to Save Charts"
        )

        if not folder:
            return
        
        self.pie_canvas.figure.savefig(
            f"{folder}/equipment_count_pie.png",
            dpi=300,
            bbox_inches="tight"
        )

        self.bar_canvas.figure.savefig(
            f"{folder}/equipment_count_bar.png",
            dpi=300,
            bbox_inches="tight"
        )

    
    def save_to_history(self, file_path, df):
        from datetime import datetime
        import os

        entry = {
            "name": os.path.basename(file_path),
            "time": datetime.now().strftime("%H:%M:%S"),
            "data": df
        }

        self.history.insert(0, entry)
        self.history = self.history[:5]  # keep only last 5

        self.update_history_ui()


    def update_history_ui(self):
        # clear old buttons
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for idx, entry in enumerate(self.history):
            btn = QPushButton(f"{entry['name']}  ({entry['time']})")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #eef2ff;
                    color: #1e1b4b;
                    text-align: left;
                    padding: 6px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e7ff;
                }
            """)
            btn.clicked.connect(lambda _, i=idx: self.load_from_history(i))
            self.history_layout.addWidget(btn)

    
    def load_from_history(self, index):
        df = self.history[index]["data"]
        self.process_dataframe(df)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())