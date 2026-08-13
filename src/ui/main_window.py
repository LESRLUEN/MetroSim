import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QTableWidget, QTableWidgetItem, QHeaderView,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
    QGraphicsLineItem, QGroupBox, QSplitter
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QBrush, QPen, QFont

from core.simulation import Simulation
from core.train import TrainState
from core.incident import Incident


class MetroCanvas(QGraphicsView):
    """Lienzo para renderizar la línea, estaciones y trenes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(self.renderHints())

        # Configuración visual
        self.scene.setBackgroundBrush(QBrush(QColor(240, 242, 245)))
        self.track_length_px = 700  # Ancho de la vía en píxeles
        self.line_y = 120           # Altura vertical de la vía

        self.station_items = {}
        self.train_items = {}

    def setup_network(self, line):
        """Dibuja la vía estática y las estaciones."""
        self.scene.clear()
        self.station_items.clear()
        self.train_items.clear()

        if not line or not line.stations:
            return

        # Determinar longitud total de la línea
        max_pos = max(st.position for st in line.stations) if line.stations else 1.0
        if max_pos == 0:
            max_pos = 1.0

        # Dibujar rieles (línea de vía)
        pen_rail = QPen(QColor(100, 110, 120), 6)
        self.scene.addLine(50, self.line_y, 50 + self.track_length_px, self.line_y, pen_rail)

        # Dibujar estaciones
        for station in line.stations:
            x_pos = 50 + (station.position / max_pos) * self.track_length_px

            # Marcador de estación (círculo / rectángulo)
            rect = self.scene.addRect(x_pos - 12, self.line_y - 12, 24, 24,
                                      QPen(QColor(40, 40, 40), 2),
                                      QBrush(QColor(255, 193, 7)))  # Amarillo Metro

            # Nombre de la estación
            text_name = self.scene.addText(f"{station.name}\n({station.position:.1f} km)")
            text_name.setFont(QFont("Segoe UI", 9, QFont.Bold))
            text_name.setPos(x_pos - 35, self.line_y + 15)

            # Contador de pasajeros
            text_pass = self.scene.addText("👥 0")
            text_pass.setFont(QFont("Segoe UI", 8))
            text_pass.setPos(x_pos - 20, self.line_y - 35)

            self.station_items[station.station_id] = {
                'x': x_pos,
                'pass_item': text_pass
            }

    def update_positions(self, line):
        """Actualiza la ubicación de trenes y contadores de pasajeros."""
        if not line:
            return

        max_pos = max(st.position for st in line.stations) if line.stations else 1.0
        if max_pos == 0:
            max_pos = 1.0

        # Actualizar pasajeros en estaciones
        for station in line.stations:
            if station.station_id in self.station_items:
                pass_item = self.station_items[station.station_id]['pass_item']
                pass_item.setPlainText(f"👥 {station.passengers_waiting}")

        # Actualizar o crear gráfica para cada tren
        for train in line.trains:
            x_pos = 50 + (train.position / max_pos) * self.track_length_px

            # Determinar color según el estado en FSM
            train_color = self._get_train_color(train.state)

            if train.train_id not in self.train_items:
                # Crear representación gráfica del tren (Rectángulo + Etiqueta ID)
                rect_item = self.scene.addRect(-20, -10, 40, 20,
                                               QPen(QColor(0, 0, 0), 2),
                                               QBrush(train_color))
                text_item = self.scene.addText(train.train_id)
                text_item.setFont(QFont("Segoe UI", 8, QFont.Bold))
                text_item.setDefaultTextColor(QColor(255, 255, 255))

                self.train_items[train.train_id] = {
                    'rect': rect_item,
                    'text': text_item
                }

            # Actualizar posición y color del tren existente
            items = self.train_items[train.train_id]
            items['rect'].setBrush(QBrush(train_color))
            items['rect'].setPos(x_pos, self.line_y)
            items['text'].setPos(x_pos - 18, self.line_y - 8)

    def _get_train_color(self, state):
        """Asigna un color según el estado operativo FSM."""
        if state in (TrainState.FALLA, TrainState.EMERGENCIA):
            return QColor(220, 53, 69)      # Rojo (Emergencia/Falla)
        elif state in (TrainState.EN_ESTACION, TrainState.ABRIENDO_PUERTAS,
                       TrainState.PUERTAS_ABIERTAS, TrainState.CERRANDO_PUERTAS):
            return QColor(13, 110, 253)     # Azul (Parada en Estación)
        elif state == TrainState.FRENANDO:
            return QColor(255, 193, 7)      # Naranja (Frenando)
        elif state in (TrainState.ACELERANDO, TrainState.EN_MARCHA):
            return QColor(25, 135, 84)      # Verde (En marcha)
        return QColor(108, 117, 125)        # Gris (Detenido/Esperando)


class MainWindow(QMainWindow):
    """Ventana Principal del Simulador MetroSim."""

    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation
        self.setWindowTitle("MetroSim - Centro de Control Operativo (CCO)")
        self.resize(1100, 700)

        # Timer para el bucle de simulación GUI
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # Actualizar cada 100ms
        self.timer.timeout.connect(self.on_tick)

        self.init_ui()

        # Cargar red inicial
        if self.simulation.lines:
            self.canvas.setup_network(self.simulation.lines[0])

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout_principal = QVBoxLayout(main_widget)

        # --- 1. PANEL SUPERIOR DE CONTROLES ---
        panel_control = QGroupBox("Controles de Simulación")
        layout_control = QHBoxLayout(panel_control)

        self.btn_start = QPushButton("▶ Iniciar")
        self.btn_start.clicked.connect(self.start_sim)
        layout_control.addWidget(self.btn_start)

        self.btn_pause = QPushButton("⏸ Pausar")
        self.btn_pause.clicked.connect(self.pause_sim)
        layout_control.addWidget(self.btn_pause)

        self.btn_step = QPushButton("⏭ Paso (1s)")
        self.btn_step.clicked.connect(self.step_sim)
        layout_control.addWidget(self.btn_step)

        self.btn_incident = QPushButton("🚨 Inyectar Palanca Emergencia")
        self.btn_incident.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")
        self.btn_incident.clicked.connect(self.trigger_incident)
        layout_control.addWidget(self.btn_incident)

        layout_control.addStretch()

        self.lbl_time = QLabel("Tiempo: 0s")
        self.lbl_time.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout_control.addWidget(self.lbl_time)

        layout_principal.addWidget(panel_control)

        # --- 2. LIENZO CENTRAL (CANVAS) ---
        self.canvas = MetroCanvas()
        self.canvas.setMinimumHeight(280)
        layout_principal.addWidget(self.canvas)

        # --- 3. PANEL INFERIOR (TELEMETRÍA) ---
        panel_telemetria = QGroupBox("Telemetría de Trenes en Tiempo Real")
        layout_telemetria = QVBoxLayout(panel_telemetria)

        self.table_trains = QTableWidget()
        self.table_trains.setColumnCount(7)
        self.table_trains.setHorizontalHeaderLabels([
            "Tren", "Sentido", "Velocidad", "Posición", "Destino", "Pasajeros", "Estado FSM"
        ])
        self.table_trains.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout_telemetria.addWidget(self.table_trains)

        layout_principal.addWidget(panel_telemetria)

    def start_sim(self):
        self.timer.start()

    def pause_sim(self):
        self.timer.stop()

    def step_sim(self):
        self.on_tick()

    def trigger_incident(self):
        """Inyecta una falla de palanca de emergencia en el primer tren."""
        if not self.simulation.lines or not self.simulation.lines[0].trains:
            return

        target_train = self.simulation.lines[0].trains[0]
        incident = Incident(
            incident_id="INC-GUI",
            description="Palanca accionada desde GUI CCO",
            train=target_train,
            duration=20,
            state=TrainState.EMERGENCIA
        )
        self.simulation.add_incident(incident)
        incident.trigger()

    def on_tick(self):
        """Actualiza la simulación y refresca la interfaz."""
        self.simulation.update()
        self.lbl_time.setText(f"Tiempo: {self.simulation.current_time:.0f}s")

        if self.simulation.lines:
            line = self.simulation.lines[0]
            # Refrescar elementos visuales
            self.canvas.update_positions(line)
            # Refrescar tabla de telemetría
            self.update_telemetry(line)

    def update_telemetry(self, line):
        """Puebla la tabla de telemetría con los datos actuales."""
        self.table_trains.setRowCount(len(line.trains))

        for row, train in enumerate(line.trains):
            direction_str = "→ Ida" if train.direction == 1 else "← Vuelta"
            next_st = train.next_station.station_id if train.next_station else "N/A"

            self.table_trains.setItem(row, 0, QTableWidgetItem(train.train_id))
            self.table_trains.setItem(row, 1, QTableWidgetItem(direction_str))
            self.table_trains.setItem(row, 2, QTableWidgetItem(f"{train.speed:.1f} km/h"))
            self.table_trains.setItem(row, 3, QTableWidgetItem(f"{train.position:.3f} km"))
            self.table_trains.setItem(row, 4, QTableWidgetItem(next_st))
            self.table_trains.setItem(row, 5, QTableWidgetItem(f"{train.passengers}/{train.capacity}"))
            self.table_trains.setItem(row, 6, QTableWidgetItem(train.state.name))