from PySide6.QtCore import QThread, Signal

from controller.support import Context


class ConnectTestWorkThread(QThread):

    result = Signal(tuple)

    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings

    def run(self):
        _reulst = Context.test_connection(self.settings)
        self.result.emit(_reulst)



