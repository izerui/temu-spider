from controller.model.BaseModel import BaseModel


class TaskModel(BaseModel):

    def __init__(self, datas):
        _heads = [{'title': '序号', 'code': 'id', 'hidden': True},
                  {'title': "创建时间", 'code': "create_time", 'hidden': True},
                  {'title': "商品id", 'code': "goods_id"},
                  {'title': "商品名称", 'code': "goods_name"},
                  {'title': "最后更新", 'code': "last_time"},
                  ]
        super().__init__(_heads, datas)
