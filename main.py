import os
import sys
import random
import pandas as pd

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
)

# ---------------- CONFIG ---------------- #

FLIP_MS = 3000

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

WORDS_TO_LEARN = os.path.join(DATA_DIR, "words_to_learn.csv")
GERMAN_WORDS = os.path.join(DATA_DIR, "german_words.csv")


# ---------------- MAIN WINDOW ---------------- #


class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("German Flashcards")
        self.resize(1000, 700)

        self.cards = []
        self.current_card = None
        self.showing_back = False

        self.setup_ui()
        self.load_data()
        self.next_card()

    def setup_ui(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #1E1E1E;
        }

        QLabel {
            color: white;
        }

        QPushButton {
            background-color: #3A7AFE;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
        }

        QPushButton:hover {
            background-color: #5A92FF;
        }

        QPushButton:pressed {
            background-color: #2F66D6;
        }
    """)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Segoe UI", 12))

        layout.addWidget(self.progress_label)

        # CARD

        self.card = QFrame()
        self.card.setObjectName("card")

        self.card.setStyleSheet("""
        QFrame#card {
            background-color: #2D2D2D;
                border-radius: 20px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)

        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)

        self.language_label = QLabel()
        self.language_label.setAlignment(Qt.AlignCenter)
        self.language_label.setFont(QFont("Segoe UI", 18))

        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setWordWrap(True)
        self.word_label.setFont(QFont("Segoe UI", 42, QFont.Bold))

        card_layout.addStretch()
        card_layout.addWidget(self.language_label)
        card_layout.addWidget(self.word_label)
        card_layout.addStretch()

        layout.addWidget(self.card, stretch=1)

        # BUTTONS

        buttons = QHBoxLayout()

        self.known_btn = QPushButton("✓ Known")
        self.flip_btn = QPushButton("↻ Flip")
        self.next_btn = QPushButton("→ Next")

        buttons.addStretch()
        buttons.addWidget(self.known_btn)
        buttons.addWidget(self.flip_btn)
        buttons.addWidget(self.next_btn)
        buttons.addStretch()

        layout.addLayout(buttons)

        # SIGNALS

        self.known_btn.clicked.connect(self.mark_known)
        self.flip_btn.clicked.connect(self.flip_card)
        self.next_btn.clicked.connect(self.next_card)

        # SHORTCUTS

        QShortcut(QKeySequence(Qt.Key_Right), self).activated.connect(self.mark_known)

        QShortcut(QKeySequence(Qt.Key_Left), self).activated.connect(self.next_card)
        QShortcut(QKeySequence(Qt.Key_Space), self).activated.connect(self.flip_card)

        # TIMER

        self.flip_timer = QTimer(self)
        self.flip_timer.setSingleShot(True)
        self.flip_timer.timeout.connect(self.flip_card)

    # ---------- DATA ---------- #

    def load_data(self):
        df = None
        src = None

        # try user's progress file
        if os.path.exists(WORDS_TO_LEARN):
            try:
                df = pd.read_csv(WORDS_TO_LEARN)
                if df.empty:
                    df = None
                else:
                    src = WORDS_TO_LEARN
            except Exception:
                df = None

        # fallback to original list
        if df is None:
            if not os.path.exists(GERMAN_WORDS):
                QMessageBox.critical(self, "Error", "No vocabulary file found.")
                return
            df = pd.read_csv(GERMAN_WORDS)
            src = GERMAN_WORDS

        # normalize and build
        df.columns = [c.strip().lower() for c in df.columns]
        german_col = df.columns[0]
        english_col = df.columns[1]
        self.cards = [
            {"German": row[german_col], "English": row[english_col]}
            for _, row in df.iterrows()
        ]

        # debug
        try:
            print(f"[Flashcard] Loaded {len(self.cards)} cards from: {src}")
            if self.cards:
                print(f"[Flashcard] First card: {self.cards[0]}")
        except Exception:
            pass

        self.update_progress()

    def save_progress(self):
        pd.DataFrame(self.cards).to_csv(WORDS_TO_LEARN, index=False)

    # ---------- CARD ---------- #

    def show_front(self):
        self.showing_back = False
        if not self.current_card:
            self.language_label.setText("")
            self.word_label.setText("")
            return

        self.language_label.setText("German")
        self.word_label.setText(str(self.current_card["German"]))

    def show_back(self):
        self.showing_back = True
        if not self.current_card:
            self.language_label.setText("")
            self.word_label.setText("")
            return

        self.language_label.setText("English")
        self.word_label.setText(str(self.current_card["English"]))

    def flip_card(self):
        if not self.current_card:
            return
        if self.showing_back:
            self.show_front()
        else:
            self.show_back()

    def next_card(self):
        if self.flip_timer.isActive():
            self.flip_timer.stop()

        if not self.cards:
            QMessageBox.information(self, "Finished", "You learned all cards 🎉")
            return

        self.current_card = random.choice(self.cards)
        try:
            print(f"[Flashcard] Selected card: {self.current_card}")
        except Exception:
            pass
        self.show_front()
        self.flip_timer.start(FLIP_MS)
        self.update_progress()

    def mark_known(self):
        if not self.current_card:
            return

        try:
            self.cards.remove(self.current_card)
        except ValueError:
            pass

        self.save_progress()
        self.next_card()

    # ---------- UTIL ---------- #

    def update_progress(self):
        self.progress_label.setText(f"Remaining Words: {len(self.cards)}")


# ---------------- ENTRY ---------------- #


def main():

    app = QApplication(sys.argv)

    window = FlashcardApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
