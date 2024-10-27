import json

from PySide6.QtCore import QSettings
from sqlalchemy import create_engine, text, Column, String, BigInteger, Engine, JSON, Boolean, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

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
    init_engine()


def get_db_engine(settings: dict) -> Engine:
    """
    获取数据库引擎操作对象
    """
    database_url = None
    connect_args = {}
    if settings['db_type'] == 'PostgreSQL':
        database_url = f"postgresql+psycopg2://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
    elif settings['db_type'] == 'MySQL':
        database_url = f"mysql+pymysql://{settings['db_user']}:{settings['db_password']}@{settings['db_host']}:{settings['db_port']}/{settings['db_database']}"
        connect_args = {
            "init_command": "SET time_zone = '+08:00'"
        }
    # 创建数据库引擎
    engine = create_engine(
        database_url,
        echo_pool=True,
        pool_size=200,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args=connect_args
    )
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


# 创建基类
Base = declarative_base()
engine = None
Session = None

def init_engine():
    global engine
    engine = get_db_engine(get_db_settings())
    # 创建表（如果尚未创建）
    Base.metadata.create_all(engine)
    global Session
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    pass


# 动态创建引擎和会话的函数
def get_session():
    if not engine:
        init_engine()
    return Session()


# 定义模型
class TemuSku(Base):
    __tablename__ = 'temu_sku'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    opt_list = Column(JSON)
    thumb_url = Column(String)
    ware_house_type = Column(BigInteger)
    benefit_text = Column(JSON)
    item_type = Column(BigInteger)
    page_alt = Column(String)
    current_sku_id = Column(String)
    tags_info = Column(JSON)
    title = Column(String)
    sales_tip_text_list = Column(JSON)
    display_end_time_percent = Column(BigInteger)
    sold_quantity_percent = Column(BigInteger)
    p_rec = Column(JSON)
    activity_type = Column(BigInteger)
    mall_id = Column(BigInteger)
    sales_num = Column(String)
    link_url = Column(String)
    extend_fields = Column(JSON)
    goods_tags = Column(JSON)
    show_index = Column(BigInteger)
    all_location_data_dict_map = Column(JSON)
    price_info = Column(JSON)
    image = Column(JSON)
    sales_tip = Column(String)
    visible = Column(Boolean)
    goods_id = Column(BigInteger)
    opt_id = Column(BigInteger)
    display_end_time = Column(BigInteger)
    seo_link_url = Column(String)
    query_rele_score = Column(Numeric(24, 8))
    sales_tip_text = Column(JSON)
    opt_type = Column(BigInteger)
    adult_goods = Column(Boolean)


# 过滤字典，只保留模型定义的字段，并为缺失字段提供默认值
def filter_dict_for_model(model, data):
    model_columns = {c.name for c in model.__table__.columns}
    return {c: data.get(c, None) for c in model_columns}


def add_temu_sku(r):
    data = r['result']['data']
    opt_list = data['opt_list']
    goods = data['goods_list']
    try:
        session = get_session()
        for good in goods:
            good['opt_list'] = opt_list
            _good = filter_dict_for_model(TemuSku, good)
            temuSku = TemuSku(**_good)
            session.add(temuSku)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error committing session: {e}")
        raise e
    finally:
        session.close()