#!/usr/bin/env python3
"""Proton-Apex Qt6 GUI draft.

Install PySide6, then run: python3 apex-gui.py
The GUI is intentionally read-only for profiles and uses the existing CLI for
settings changes, keeping the Proton launcher untouched.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication, QComboBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
        QListWidget, QListWidgetItem, QMainWindow, QPushButton, QTextEdit,
        QVBoxLayout, QWidget,
    )
except ImportError as exc:
    raise SystemExit("PySide6 is required: pip install PySide6") from exc

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from game_profiles import GAME_PROFILES  # noqa: E402


class ApexWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Proton-Apex Control Center")
        self.resize(980, 620)
        self.profile_list = QListWidget()
        self.details = QTextEdit(readOnly=True)
        self.preset = QComboBox()
        self.preset.addItems(["balanced", "diagnostic"])
        self.status = QLabel("Ready")
        self._build_ui()
        self._populate_profiles()
        self.profile_list.currentItemChanged.connect(self._show_profile)

    def _build_ui(self) -> None:
        root = QWidget()
        outer = QHBoxLayout(root)
        left = QVBoxLayout()
        left.addWidget(QLabel("Game profiles"))
        left.addWidget(self.profile_list)
        outer.addLayout(left, 1)
        right = QVBoxLayout()
        right.addWidget(QLabel("Profile details"))
        right.addWidget(self.details, 1)
        settings = QGroupBox("Configuration")
        form = QFormLayout(settings)
        form.addRow("Preset", self.preset)
        apply_button = QPushButton("Apply preset")
        apply_button.clicked.connect(self._apply_preset)
        form.addRow(apply_button)
        cache_button = QPushButton("Inspect shader cache")
        cache_button.clicked.connect(self._inspect_cache)
        form.addRow(cache_button)
        right.addWidget(settings)
        right.addWidget(self.status)
        outer.addLayout(right, 2)
        self.setCentralWidget(root)

    def _populate_profiles(self) -> None:
        for app_id, profile in GAME_PROFILES.items():
            item = QListWidgetItem(f"{profile['name']}  [{app_id}]")
            item.setData(Qt.UserRole, app_id)
            self.profile_list.addItem(item)
        self.profile_list.setCurrentRow(0)

    def _show_profile(self, current, _previous) -> None:
        if not current:
            return
        profile = GAME_PROFILES[current.data(Qt.UserRole)]
        self.details.setPlainText(json.dumps(profile, indent=2, ensure_ascii=False))

    def _apply_preset(self) -> None:
        result = subprocess.run([str(ROOT / "apex-config"), "preset", self.preset.currentText()], text=True, capture_output=True)
        self.status.setText((result.stdout or result.stderr).strip())

    def _inspect_cache(self) -> None:
        result = subprocess.run([str(ROOT / "apex-shader-optimizer"), "--prepare", "--print-env"], text=True, capture_output=True)
        self.details.setPlainText(result.stdout or result.stderr)
        self.status.setText("Cache inspection complete")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApexWindow()
    window.show()
    sys.exit(app.exec())
