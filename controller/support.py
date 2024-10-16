from PySide6.QtWidgets import QMessageBox


def show_message(message: str, warning: bool = False):
    """
    弹出提示框
    """
    msg: QMessageBox = QMessageBox()
    msg.setText(message)
    if warning:
        msg.setWindowTitle('Warning')
        msg.setIcon(QMessageBox.Icon.Warning)
    else:
        msg.setWindowTitle('Information')
        msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
