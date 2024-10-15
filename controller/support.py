from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMessageBox
from sqlalchemy import create_engine, text

set_conf: QSettings = QSettings('settings.ini', QSettings.Format.IniFormat)
set_conf.setFallbacksEnabled(False)


class Context(object):
    """
    数据库配置
    """

    @staticmethod
    def get_settings() -> dict:
        db_type = set_conf.value('database/type', 'PostgreSQL')
        db_host = set_conf.value('database/host', '127.0.0.1')
        db_port = set_conf.value('database/port', '5432')
        db_user = set_conf.value('database/user', 'postgres')
        db_password = set_conf.value('database/password', 'postgres')
        db_database = set_conf.value('database/database', 'v8')
        return {
            'db_type': db_type,
            'db_host': db_host,
            'db_port': db_port,
            'db_user': db_user,
            'db_password': db_password,
            'db_database': db_database,
        }

    @staticmethod
    def save_settings(settings: dict):
        set_conf.setValue('database/type', settings['db_type'])
        set_conf.setValue('database/host', settings['db_host'])
        set_conf.setValue('database/port', settings['db_port'])
        set_conf.setValue('database/user', settings['db_user'])
        set_conf.setValue('database/password', settings['db_password'])
        set_conf.setValue('database/database', settings['db_database'])

    @staticmethod
    def get_db_engine(settings: dict) -> str:
        database_url = None
        if settings['db_type'] == 'PostgreSQL':
            database_url = f"postgresql+psycopg2://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
        elif settings['db_type'] == 'MySQL':
            database_url = f"mysql+pymysql://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
        # 创建数据库引擎
        engine = create_engine(database_url)
        return engine

    @staticmethod
    def test_connection(settings: dict) -> tuple[bool, str]:
        engine = Context.get_db_engine(settings)
        # 测试连接并执行查询
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("查询结果: ", result.fetchone())
                print("连接成功并执行查询成功!")
                return True, ""
        except Exception as e:
            print(f"连接失败: {e}")
            return False, f'连接失败: {str(e)}'

    @staticmethod
    def show_message(message: str, warning: bool = False):
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
