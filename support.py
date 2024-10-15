from PySide6.QtCore import QSettings

set_conf: QSettings = QSettings('settings.ini', QSettings.IniFormat)
set_conf.setFallbacksEnabled(False)


class Settings(object):
    """
    数据库配置
    """

    @staticmethod
    def get_settings() -> dict:
        db_type = set_conf.value('database/type', 'PostgreSQL')
        db_host = set_conf.value('database/host', '127.0.0.1')
        db_port = set_conf.value('database/port', 5432)
        db_user = set_conf.value('database/user', 'postgres')
        db_password = set_conf.value('database/password', 'postgres')
        return {
            'db_type': db_type,
            'db_host': db_host,
            'db_port': db_port,
            'db_user': db_user,
            'db_password': db_password,
        }

    @staticmethod
    def save_settings(settings: dict):
        set_conf.setValue('database/type', settings['db_type'])
        set_conf.setValue('database/host', settings['db_host'])
        set_conf.setValue('database/port', settings['db_port'])
        set_conf.setValue('database/user', settings['db_user'])
        set_conf.setValue('database/password', settings['db_password'])
