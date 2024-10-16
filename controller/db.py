from PySide6.QtCore import QSettings
from sqlalchemy import create_engine, text

set_conf: QSettings = QSettings('settings.ini', QSettings.Format.IniFormat)
set_conf.setFallbacksEnabled(False)


def get_db_settings() -> dict:
    """
    获取数据库的配置信息
    """
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


def save_db_settings(settings: dict):
    """
    保存配置信息
    """
    set_conf.setValue('database/type', settings['db_type'])
    set_conf.setValue('database/host', settings['db_host'])
    set_conf.setValue('database/port', settings['db_port'])
    set_conf.setValue('database/user', settings['db_user'])
    set_conf.setValue('database/password', settings['db_password'])
    set_conf.setValue('database/database', settings['db_database'])


def get_db_engine(settings: dict) -> str:
    """
    获取数据库引擎操作对象
    """
    database_url = None
    if settings['db_type'] == 'PostgreSQL':
        database_url = f"postgresql+psycopg2://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
    elif settings['db_type'] == 'MySQL':
        database_url = f"mysql+pymysql://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
    # 创建数据库引擎
    engine = create_engine(database_url)
    return engine


def test_connection(settings: dict) -> tuple[bool, str]:
    """
    根据配置信息，测试数据库连接
    """
    engine = get_db_engine(settings)
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
