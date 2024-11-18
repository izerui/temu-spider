from PySide6.QtWidgets import QMessageBox

categories = [{
                  'href': '/category.html?opt_id=-13&opt_level=1&title=精选&_x_enter_scene_type=cate_tab&show_search_type=3&child_opt_list=1733,6912,1560,7264,1115,7181,7266,7183,1035,6933,1644,1568,1120,1562,1911,1435,29,1564,1038,1018,2889,1732,1900,7268,1426,1331,1580,1084,6876,1572&leaf_type=son',
                  'text': '精选'}, {'href': '/us-zh-Hans/home-kitchen-o3-36.html', 'text': '家居厨房用品'},
              {'href': '/us-zh-Hans/womens-clothing-o3-28.html', 'text': '女装'},
              {'href': '/us-zh-Hans/womens-curve-clothing-o3-589.html', 'text': '大码女装'},
              {'href': '/us-zh-Hans/womens-shoes-o3-95.html', 'text': '女鞋'},
              {'href': '/us-zh-Hans/womens-lingerie-lounge-o3-1107.html', 'text': '女士内衣和睡衣'},
              {'href': '/us-zh-Hans/mens-clothing-o3-67.html', 'text': '男装'},
              {'href': '/us-zh-Hans/mens-shoes-o3-1536.html', 'text': '男鞋'},
              {'href': '/us-zh-Hans/mens-big-tall-o3-1232.html', 'text': '大码男装'},
              {'href': '/us-zh-Hans/mens-underwear-sleepwear-o3-114.html', 'text': '男士内衣和睡衣'},
              {'href': '/us-zh-Hans/sports-outdoors-o3-178.html', 'text': '运动与户外'},
              {'href': '/us-zh-Hans/jewelry-accessories-o3-352.html', 'text': '珠宝和配饰'},
              {'href': '/us-zh-Hans/beauty-health-o3-25.html', 'text': '美容与健康'},
              {'href': '/us-zh-Hans/toys-games-o3-204.html', 'text': '玩具与游戏'},
              {'href': '/us-zh-Hans/automotive-o3-580.html', 'text': '汽车用品'},
              {'href': '/us-zh-Hans/kids-fashion-o3-218.html', 'text': '童装'},
              {'href': '/us-zh-Hans/kids-shoes-o3-1553.html', 'text': '童鞋'},
              {'href': '/us-zh-Hans/baby-maternity-o3-1167.html', 'text': '母婴用品'},
              {'href': '/us-zh-Hans/bags-luggage-o3-731.html', 'text': '箱包'},
              {'href': '/us-zh-Hans/patio-lawn-garden-o3-885.html', 'text': '庭院、草坪和园艺'},
              {'href': '/us-zh-Hans/arts-crafts-sewing-o3-1493.html', 'text': '手工艺与缝纫制品'},
              {'href': '/us-zh-Hans/electronics-o3-248.html', 'text': '电子产品'},
              {'href': '/us-zh-Hans/business--science-o3-259.html', 'text': '商务、工业与科技'},
              {'href': '/us-zh-Hans/tools-home-improvement-o3-893.html', 'text': '家居装修'},
              {'href': '/us-zh-Hans/appliances-o3-990.html', 'text': '电器'},
              {'href': '/us-zh-Hans/-supplies-o3-202.html', 'text': '办公与学校用品'},
              {'href': '/us-zh-Hans/health-household-o3-871.html', 'text': '健康与家庭用品'},
              {'href': '/us-zh-Hans/pet-supplies-o3-320.html', 'text': '宠物用品'},
              {'href': '/us-zh-Hans/cell-phones-accessories-o3-2640.html', 'text': '手机及配件'},
              {'href': '/us-zh-Hans/-home-o3-1422.html', 'text': '智能家居'},
              {'href': '/us-zh-Hans/musical-instruments-o3-628.html', 'text': '乐器'},
              {'href': '/us-zh-Hans/beachwear-o3-7166.html', 'text': '泳衣'},
              {'href': '/us-zh-Hans/food-grocery-o3-7084.html', 'text': '食品和杂货'},
              {'href': '/us-zh-Hans/books-o3-7085.html', 'text': '图书'}]


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
