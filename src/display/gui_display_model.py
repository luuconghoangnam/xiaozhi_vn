# -*- coding: utf-8 -*-
"""
GUI display model - bridge dữ liệu từ Python sang QML.
"""

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


class GuiDisplayModel(QObject):
    statusTextChanged = pyqtSignal()
    emotionPathChanged = pyqtSignal()
    emotionNameChanged = pyqtSignal()
    ttsTextChanged = pyqtSignal()
    buttonTextChanged = pyqtSignal()
    modeTextChanged = pyqtSignal()
    autoModeChanged = pyqtSignal()
    detailTextChanged = pyqtSignal()
    logsTextChanged = pyqtSignal()

    manualButtonPressed = pyqtSignal()
    manualButtonReleased = pyqtSignal()
    autoButtonClicked = pyqtSignal()
    abortButtonClicked = pyqtSignal()
    modeButtonClicked = pyqtSignal()
    sendButtonClicked = pyqtSignal(str)
    settingsButtonClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status_text = "Trạng thái: Chưa kết nối"
        self._emotion_path = ""
        self._emotion_name = "neutral"
        self._tts_text = "Sẵn sàng"
        self._button_text = "Bắt đầu"
        self._mode_text = "Thủ công"
        self._auto_mode = False
        self._is_connected = False
        self._detail_text = "Coonie đang chờ anh gọi..."
        self._logs_text = "--- Coonie Logs ---"

    @pyqtProperty(str, notify=statusTextChanged)
    def statusText(self):
        return self._status_text

    @statusText.setter
    def statusText(self, value):
        if self._status_text != value:
            self._status_text = value
            self.statusTextChanged.emit()

    @pyqtProperty(str, notify=emotionPathChanged)
    def emotionPath(self):
        return self._emotion_path

    @emotionPath.setter
    def emotionPath(self, value):
        if self._emotion_path != value:
            self._emotion_path = value
            self.emotionPathChanged.emit()

    @pyqtProperty(str, notify=emotionNameChanged)
    def emotionName(self):
        return self._emotion_name

    @emotionName.setter
    def emotionName(self, value):
        if self._emotion_name != value:
            self._emotion_name = value
            self.emotionNameChanged.emit()

    @pyqtProperty(str, notify=ttsTextChanged)
    def ttsText(self):
        return self._tts_text


    @ttsText.setter
    def ttsText(self, value):
        if self._tts_text != value:
            self._tts_text = value
            self.ttsTextChanged.emit()

    @pyqtProperty(str, notify=buttonTextChanged)
    def buttonText(self):
        return self._button_text

    @buttonText.setter
    def buttonText(self, value):
        if self._button_text != value:
            self._button_text = value
            self.buttonTextChanged.emit()

    @pyqtProperty(str, notify=modeTextChanged)
    def modeText(self):
        return self._mode_text

    @modeText.setter
    def modeText(self, value):
        if self._mode_text != value:
            self._mode_text = value
            self.modeTextChanged.emit()

    @pyqtProperty(bool, notify=autoModeChanged)
    def autoMode(self):
        return self._auto_mode

    @autoMode.setter
    def autoMode(self, value):
        if self._auto_mode != value:
            self._auto_mode = value
            self.autoModeChanged.emit()

    @pyqtProperty(str, notify=detailTextChanged)
    def detailText(self):
        return self._detail_text

    @detailText.setter
    def detailText(self, value):
        if self._detail_text != value:
            self._detail_text = value
            self.detailTextChanged.emit()

    @pyqtProperty(str, notify=logsTextChanged)
    def logsText(self):
        return self._logs_text

    @logsText.setter
    def logsText(self, value):
        if self._logs_text != value:
            self._logs_text = value
            self.logsTextChanged.emit()

    def append_log(self, log_msg: str):
        lines = self._logs_text.split("\n")
        lines.append(log_msg)
        # Keep last 100 lines
        self.logsText = "\n".join(lines[-100:])

    def update_status(self, status: str, connected: bool):
        self.statusText = f"Trạng thái: {status}"
        self._is_connected = connected

    def update_text(self, text: str):
        self.ttsText = text or "Sẵn sàng"

    def update_emotion(self, emotion_path: str, emotion_name: str = "neutral"):
        self.emotionPath = emotion_path
        self.emotionName = emotion_name

    def update_button_text(self, text: str):
        self.buttonText = text or "Bắt đầu"

    def update_mode_text(self, text: str):
        self.modeText = text or "Thủ công"

    def set_auto_mode(self, is_auto: bool):
        self.autoMode = is_auto
        self.modeText = "Tự động" if is_auto else "Thủ công"

    def update_details(self, status: str, task: str, response: str, meta: str):
        parts = []
        if status:
            parts.append(f"• Trạng thái: {status}")
        if task:
            parts.append(f"• Tác vụ: {task}")
        if response:
            parts.append(f"• Phản hồi: {response}")
        if meta:
            parts.append(f"• Ghi chú: {meta}")
        self.detailText = "\n".join(parts) if parts else "Coonie đang chờ anh gọi..."
