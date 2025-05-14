import sys
import os
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QToolBar, QSpinBox,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QDialog, QLineEdit, QStackedLayout
)
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap, QPainter
from PyQt5.QtCore import Qt
from instrument import MusicPlayer, note_to_frequency

CONFIG_FILE = "config.json"

class RecordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Musical Instruments")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout()

        self.label = QLabel("Enter recording name:")
        self.line_edit = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_name(self):
        return self.line_edit.text()


class InstrumentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Musical Instruments")
        self.setGeometry(100, 100, 1200, 500)

        self.player = MusicPlayer()
        self.current_instrument = "Piano"
        self.octaves = 2
        self.recording = False
        self.recorded_notes = []
        self.record_name = ""

        self.load_config()

        self.create_menu()
        self.create_toolbar()
        self.create_main_ui()
        self.show()

    def create_menu(self):
        menu = self.menuBar().addMenu("Menu")

        # Create shared actions with shortcuts
        self.open_action = QAction(QIcon("open.png"), "Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_score)

        self.record_action = QAction(QIcon("record.png"), "Record", self)
        self.record_action.setShortcut("Ctrl+R")
        self.record_action.triggered.connect(self.record_music)

        self.stop_action = QAction(QIcon("stoprecord.png"), "Stop", self)
        self.stop_action.setShortcut("Ctrl+S")
        self.stop_action.triggered.connect(self.stop_recording)

        self.quit_action = QAction(QIcon("quit.png"), "Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

        # Add to menu
        menu.addAction(self.open_action)
        menu.addAction(self.record_action)
        menu.addAction(self.stop_action)
        menu.addAction(self.quit_action)


    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Reuse shared actions created in create_menu()
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.record_action)
        toolbar.addAction(self.stop_action)

        # Octave selector and instrument buttons
        self.octave_spin = QSpinBox()
        self.octave_spin.setRange(1, 3)
        self.octave_spin.setValue(self.octaves)
        self.octave_spin.valueChanged.connect(self.set_octaves)
        toolbar.addWidget(self.octave_spin)

        self.piano_btn = QPushButton("Piano")
        self.piano_btn.clicked.connect(lambda: self.change_instrument("Piano"))
        toolbar.addWidget(self.piano_btn)

        self.xylophone_btn = QPushButton("Xylophone")
        self.xylophone_btn.clicked.connect(lambda: self.change_instrument("Xylophone"))
        toolbar.addWidget(self.xylophone_btn)

        self.videogame_btn = QPushButton("Video Game")
        self.videogame_btn.clicked.connect(lambda: self.change_instrument("Video Game"))
        toolbar.addWidget(self.videogame_btn)


    def create_main_ui(self):
        self.widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.instrument_area = QWidget()
        self.instrument_stack = QStackedLayout()
        self.instrument_area.setLayout(self.instrument_stack)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.instrument_area)
        center_layout.addStretch()

        self.main_layout.addLayout(center_layout)
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

        self.build_instrument_ui()


    def build_instrument_ui(self):
        while self.instrument_stack.count():
            widget = self.instrument_stack.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        if self.current_instrument == "Piano":
            piano_widget = self.build_piano_keys()
            self.instrument_stack.addWidget(piano_widget)

            # --- Calculate the piano size ---
            key_width = 60
            number_of_white_keys = 7 * self.octaves
            piano_width = number_of_white_keys * key_width
            padding = 100

            total_width = piano_width + padding
            total_height = 400

            # --- Resize the main window ---
            self.setFixedSize(total_width, total_height)

            # --- Resize the instrument area ---
            self.instrument_area.setFixedWidth(piano_width)

        elif self.current_instrument == "Xylophone":
            xylophone_widget = self.build_xylophone_keys()
            self.instrument_stack.addWidget(xylophone_widget)

            # --- Set window size appropriate for xylophone ---
            total_width = 700
            total_height = 400
            self.setFixedSize(total_width, total_height)
            self.instrument_area.setFixedWidth(total_width - 100)

        elif self.current_instrument == "Video Game":
            videogame_widget = self.build_videogame_keys()
            self.instrument_stack.addWidget(videogame_widget)

            # --- Set window size appropriate for video game keys ---
            button_width = 64
            number_of_buttons = 10
            spacing = 10 * (number_of_buttons - 1)
            total_width = number_of_buttons * button_width + spacing + 100
            total_height = 400

            self.setFixedSize(total_width, total_height)
            self.instrument_area.setFixedWidth(total_width - 100)


    def build_piano_keys(self):
        widget = QWidget()
        piano_area = QWidget(widget)
        piano_area.setGeometry(0, 0, 70 * 7 * self.octaves, 250)

        key_width = 60
        key_height = 200
        black_key_width = 40
        black_key_height = 120

        key_map = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]
        black_keys_pos = ["Do#", "Ré#", None, "Fa#", "Sol#", "La#", None]

        self.white_keys = []
        self.black_keys = []

        for o in range(self.octaves):
            for i, note in enumerate(key_map):
                # Create white key
                w_btn = QPushButton(note, piano_area)
                x = (o * 7 + i) * key_width
                w_btn.setGeometry(x, 50, key_width, key_height)
                w_btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        border: 1px solid black;
                        border-bottom-left-radius: 5px;
                        border-bottom-right-radius: 5px;
                    }
                """)
                w_btn.clicked.connect(lambda checked, n=note, oc=o: self.play_note(n, oc))
                w_btn.pressed.connect(lambda btn=w_btn: self.press_key_effect(btn, "white"))
                w_btn.released.connect(lambda btn=w_btn: self.release_key_effect(btn, "white"))
                self.white_keys.append(w_btn)

        for o in range(self.octaves):
            for i, bnote in enumerate(black_keys_pos):
                if bnote:
                    # Create black key
                    b_btn = QPushButton(bnote, piano_area)
                    x = ((o * 7 + i) * key_width) + (key_width - black_key_width // 2)
                    b_btn.setGeometry(x, 50, black_key_width, black_key_height)
                    b_btn.setStyleSheet("background-color: black; color: white; border: 1px solid black;")
                    b_btn.clicked.connect(lambda checked, n=bnote, oc=o: self.play_note(n, oc))
                    b_btn.pressed.connect(lambda btn=b_btn: self.press_key_effect(btn, "black"))
                    b_btn.released.connect(lambda btn=b_btn: self.release_key_effect(btn, "black"))
                    self.black_keys.append(b_btn)

        return widget


    def press_key_effect(self, btn, color):
        if color == "white":
            btn.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        else:  # black key
            btn.setStyleSheet("background-color: #555555; color: white; border: 1px solid black;")
        btn.resize(btn.width()-2, btn.height()-2)

    def release_key_effect(self, btn, color):
        if color == "white":
            btn.setStyleSheet("background-color: white; border: 1px solid black;")
        else:  # black key
            btn.setStyleSheet("background-color: black; color: white; border: 1px solid black;")
        btn.resize(btn.width()+2, btn.height()+2)


    def build_xylophone_keys(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        colors = ["#C71585", "#800080", "#0000FF", "#00FF00", "#FFFF00", "#FFA500", "#FF0000", "#FF69B4"]
        notes = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si", "Do"]
        widths = [60, 60, 55, 55, 50, 50, 45, 45]
        heights = [270, 270, 250, 230, 210, 190, 170, 150]

        self.xylophone_keys = []

        for i, note in enumerate(notes):
            btn = QPushButton(note)
            btn.setFixedSize(widths[i], heights[i])
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors[i]};
                    color: black;
                    font-weight: bold;
                    font-size: 20px;
                    border-radius: 20px;
                    border: 2px solid black;
                }}
            """)
            btn.clicked.connect(lambda checked, n=note, oc=0: self.play_note(n, oc))

            # Add pressed and released effects
            btn.pressed.connect(lambda btn=btn, color=colors[i]: self.press_xylophone_key(btn, color))
            btn.released.connect(lambda btn=btn, color=colors[i]: self.release_xylophone_key(btn, color))

            layout.addWidget(btn)
            self.xylophone_keys.append(btn)

        widget.setLayout(layout)
        return widget
    
    def press_xylophone_key(self, btn, color):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.darken_color(color, 0.5)};
                color: black;
                font-weight: bold;
                font-size: 20px;
                border-radius: 20px;
                border: 2px solid black;
            }}
        """)

    def release_xylophone_key(self, btn, color):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-weight: bold;
                font-size: 20px;
                border-radius: 20px;
                border: 2px solid black;
            }}
        """)

    def darken_color(self, hex_color, factor):
        """Helper to darken a hex color by a factor."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, int(c * factor)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)


    def build_videogame_keys(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # List of notes and corresponding images
        notes = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si", "Do", "Ré", "Mi"]
        images = [
            "super-mario.png",
            "super-mario1.png",
            "plante-carnivore.png",
            "pieces-de-monnaie.png",
            "mario11.png",
            "waluigi.png",
            "plante.png",
            "jeu.png",
            "mario.png",
            "le-manoir-de-luigi.png",
        ]

        for i, note in enumerate(notes):
            btn = QPushButton()
            btn.setFixedSize(64, 64)
            image_dir = os.path.join(os.path.dirname(__file__), "images")
            icon_path = os.path.join(image_dir, images[i])

            icon = QIcon(icon_path)
            btn.setIcon(icon)
            btn.setIconSize(btn.size())
            btn.setStyleSheet("border: none;")

            btn.clicked.connect(lambda checked, n=note: self.play_video_game_note(n))
            btn.pressed.connect(lambda checked=False, b=btn, p=icon_path: self.press_videogame_key(b, p))
            btn.released.connect(lambda checked=False, b=btn, p=icon_path: self.release_videogame_key(b, p))

            layout.addWidget(btn)

        widget.setLayout(layout)
        return widget


    def play_video_game_note(self, note):
        base_frequency = note_to_frequency[note][2]  # Take the base low octave
        #frequency = base_frequency * (2**3)  # Raise octaves (ex: 2^3 = 8 times higher)
        duration = 0.2  # Short punchy sound
        #self.player.play_videoGame_tone(frequency, duration)
        self.player.play_videoGame_tone(base_frequency, duration)
        
        if self.recording:
            self.recorded_notes.append((note, duration))

    def press_videogame_key(self, btn, image_path):
        pixmap = QPixmap(image_path)
        dark_pixmap = QPixmap(pixmap.size())
        dark_pixmap.fill(Qt.transparent)

        painter = QPainter(dark_pixmap)
        painter.setOpacity(0.5)  # 50% darkness
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        btn.setIcon(QIcon(dark_pixmap))

    def release_videogame_key(self, btn, image_path):
        btn.setIcon(QIcon(QPixmap(image_path)))


    def play_note(self, note, octave):
        frequency = note_to_frequency[note][octave]
        duration = 0.5
        if self.current_instrument == "Piano":
            self.player.play_piano_tone(frequency, duration)
        elif self.current_instrument == "Xylophone":
            self.player.play_xylophone_tone(frequency, duration)
        elif self.current_instrument == "Video Game":
            self.player.play_videoGame_tone(frequency, duration)
        if self.recording:
            self.recorded_notes.append((note, 0.5))  # Assuming default duration = 0.5 seconds


    def open_score(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Score", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        note, duration = parts
                        try:
                            duration = float(duration)
                        except ValueError:
                            continue
                        if note == '0' or note == 'Unknown':
                            time.sleep(duration)
                        elif note in note_to_frequency:
                            freq_data = note_to_frequency[note]
                            if isinstance(freq_data, tuple):
                                if self.current_instrument == "Video Game":
                                    frequency = freq_data[2]
                                else:
                                    frequency = freq_data[0]
                            else:
                                frequency = freq_data
                            if self.current_instrument == "Piano":
                                self.player.play_piano_tone(frequency, duration)
                            elif self.current_instrument == "Xylophone":
                                self.player.play_xylophone_tone(frequency, duration)
                            elif self.current_instrument == "Video Game":
                                self.player.play_videoGame_tone(frequency, duration)
                        else:
                            print(f"Note {note} not recognized.")


    def record_music(self):
        dialog = RecordDialog()
        if dialog.exec_():
            self.record_name = dialog.get_name()
            self.recorded_notes = []
            self.recording = True

    def stop_recording(self):
        if self.recording and self.record_name:
            with open(f"{self.record_name}.txt", "w") as f:
                for note, duration in self.recorded_notes:
                    f.write(f"{note} {duration}\n")
        self.recording = False


    def change_instrument(self, instrument):
        self.current_instrument = instrument
        self.build_instrument_ui()
        self.save_config()

    def set_octaves(self, value):
        self.octaves = value
        self.build_instrument_ui()
        self.save_config()

    def save_config(self):
        config = {
            "instrument": self.current_instrument,
            "octaves": self.octaves
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.current_instrument = config.get("instrument", "Piano")
                self.octaves = config.get("octaves", 2)


    def keyPressEvent(self, event):
        key = event.key()

        # Default key map — shared notes for other instruments (one octave only)
        base_key_map = {
            Qt.Key_A: "Do", Qt.Key_Z: "Ré", Qt.Key_E: "Mi",
            Qt.Key_R: "Fa", Qt.Key_T: "Sol", Qt.Key_Y: "La", Qt.Key_U: "Si",
            Qt.Key_1: "Do#", Qt.Key_2: "Ré#", Qt.Key_4: "Fa#", Qt.Key_5: "Sol#", Qt.Key_3: "La#",
        }

        # Extended multi-octave map — only for piano
        piano_key_map = {
            # Octave 1
            Qt.Key_W: ("Do", 0), Qt.Key_X: ("Ré", 0), Qt.Key_C: ("Mi", 0),
            Qt.Key_V: ("Fa", 0), Qt.Key_B: ("Sol", 0), Qt.Key_N: ("La", 0), Qt.Key_Comma: ("Si", 0),
            Qt.Key_Ampersand: ("Do#", 0), Qt.Key_Eacute: ("Ré#", 0),
            Qt.Key_ParenLeft: ("Fa#", 0), Qt.Key_Minus: ("Sol#", 0), Qt.Key_QuoteLeft: ("La#", 0),

            # Octave 2
            Qt.Key_A: ("Do", 1), Qt.Key_Z: ("Ré", 1), Qt.Key_E: ("Mi", 1),
            Qt.Key_R: ("Fa", 1), Qt.Key_T: ("Sol", 1), Qt.Key_Y: ("La", 1), Qt.Key_U: ("Si", 1),
            Qt.Key_1: ("Do#", 1), Qt.Key_2: ("Ré#", 1),
            Qt.Key_4: ("Fa#", 1), Qt.Key_5: ("Sol#", 1), Qt.Key_3: ("La#", 1),

            # Octave 3
            Qt.Key_Q: ("Do", 2), Qt.Key_S: ("Ré", 2), Qt.Key_D: ("Mi", 2),
            Qt.Key_F: ("Fa", 2), Qt.Key_G: ("Sol", 2), Qt.Key_H: ("La", 2), Qt.Key_J: ("Si", 2),
            Qt.Key_6: ("Do#", 2), Qt.Key_7: ("Ré#", 2),
            Qt.Key_9: ("Fa#", 2), Qt.Key_0: ("Sol#", 2), Qt.Key_8: ("La#", 2),
        }

        # Use extended mapping only for piano
        if self.current_instrument == "Piano":
            key_map = piano_key_map
        else:
            key_map = {k: (v, 0) for k, v in base_key_map.items()}  # Default to octave 0

        if key in key_map:
            note, octave = key_map[key]

            if note in note_to_frequency:
                freq_data = note_to_frequency[note]
                if isinstance(freq_data, tuple):
                    frequency = freq_data[octave] if octave < len(freq_data) else freq_data[0]
                else:
                    frequency = freq_data

                if self.current_instrument == "Piano":
                    self.player.play_piano_tone(frequency, 0.5)
                elif self.current_instrument == "Xylophone":
                    self.player.play_xylophone_tone(frequency, 0.5)
                elif self.current_instrument == "Video Game":
                    frequency = freq_data[2] if isinstance(freq_data, tuple) else freq_data
                    self.player.play_videoGame_tone(frequency, 0.2)

                if self.recording:
                    self.recorded_notes.append((note, 0.5))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InstrumentApp()
    sys.exit(app.exec_())