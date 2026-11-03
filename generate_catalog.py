# -*- coding: utf-8 -*-
"""
SimReady 3D 资产库汉化选型目录生成器 (左右分栏布局 · 无Emoji简约工程版 · 明暗主题)
包含：
1. 经典左右工程分栏布局 (左侧导航与控制面板，右侧内容网格与表格)
2. 去除全部小图标与Emoji，采用纯粹专业的工业工程视觉风格
3. 10 大产业与仿真领域纵向分类导航与数量角标
4. 覆盖全部 192 个主分类的中英双语对照与 300+ 核心词汇翻译
5. 完备的明暗主题切换与本地记忆 (Light / Dark Mode)
6. 实时中英双语检索、关节过滤、多维排序与 CSV 导出功能
"""

import json
import re
import os

# 1. 10 大核心产业与仿真领域划分（去除Emoji）
DOMAINS = {
    'auto': {'name': '汽车与汽修部件', 'desc': '车身构件、发动机动力、底盘悬挂、制动转向、举升支撑与专业维保设备'},
    'tool': {'name': '工具与工业设备', 'desc': '手动工具、电动/气动切削、检测诊断仪器、工业机械、紧固件与登高设施'},
    'logistics': {'name': '仓储物流与包装', 'desc': '托盘栈板、瓦楞纸箱周转筐、工业储桶/吨桶、搬运地牛、货架立柱与流水线'},
    'food': {'name': '食品生鲜与酒水', 'desc': '生鲜果蔬、肉类海鲜、快餐熟食、面包烘焙、饮料酒水与预包装罐头'},
    'kitchen': {'name': '餐饮厨具与日用', 'desc': '烹饪锅具、餐盘碗碟、西餐餐具、厨房小家电（洗碗机/抽油烟机/冰箱等）'},
    'medical': {'name': '医疗器械与健康', 'desc': '手术器械、X光/CT/超声设备、麻醉透析机、病床轮椅、输液注射与医用耗材'},
    'office': {'name': '办公家具与设施', 'desc': '办公桌椅、文件防爆柜、电脑主机显示器、百叶窗、建筑钢梁、照明与卫浴'},
    'safety': {'name': '安全消防与环保', 'desc': '劳保护具(PPE)、洗眼器/急救箱、灭火器、安全警示牌、吸油棉与分类垃圾桶'},
    'robotics': {'name': '机器人与自动化', 'desc': '工业机械臂、自动化传感器、电气控制与通用物理仿真测试件'},
    'misc': {'name': '装饰与杂项物资', 'desc': '室内摆件、仿真玩具、配饰与各类通用三维道具'}
}

# 2. 全部 192 个主分类的中英双语对照与所属领域
CATEGORIES = {
    # 汽车与汽修 (auto)
    'bodyPart': ('车身外观构件', 'auto'),
    'engineComponent': ('发动机零部件', 'auto'),
    'engineAssembly': ('发动机总成装配', 'auto'),
    'engine': ('发动机总成', 'auto'),
    'drivetrain': ('动力传动系统', 'auto'),
    'suspension': ('底盘悬挂系统', 'auto'),
    'brakeSystem': ('刹车制动系统', 'auto'),
    'steeringSystem': ('转向操纵系统', 'auto'),
    'steering': ('转向机构部件', 'auto'),
    'coolingSystem': ('引擎冷却系统', 'auto'),
    'exhaustSystem': ('废气排气系统', 'auto'),
    'fuelSystem': ('燃油供给系统', 'auto'),
    'airSystem': ('进气与气动系统', 'auto'),
    'wheelAssembly': ('轮胎与车轮总成', 'auto'),
    'interiorPart': ('汽车座舱内饰', 'auto'),
    'vehicleSupport': ('车辆举升支撑设备', 'auto'),
    'tireTool': ('轮胎拆装检修工具', 'auto'),
    'serviceTool': ('汽修维保专业设备', 'auto'),
    'carFrame': ('汽车车架与底盘', 'auto'),
    'headlight': ('汽车前大灯总成', 'auto'),
    'vehicle': ('特种车辆与设施', 'auto'),

    # 工具与工业设备 (tool)
    'handTool': ('手动工具', 'tool'),
    'powerTool': ('电动与气动工具', 'tool'),
    'testingTool': ('测试与检测仪器', 'tool'),
    'tool': ('常用综合工具', 'tool'),
    'tools': ('专业工具组', 'tool'),
    'equipment': ('工业生产机械设备', 'tool'),
    'machine': ('机械设备与动力单元', 'tool'),
    'machineGuard': ('机床安全防护网格', 'tool'),
    'hardware': ('工业标准五金件', 'tool'),
    'screw': ('标准紧固螺钉螺栓', 'tool'),
    'factory': ('工厂装配标准紧固件', 'tool'),
    'ladder': ('登高梯与便携梯', 'tool'),
    'scaffold': ('建筑装配脚手架', 'tool'),
    'measurement': ('精密测量与量规工具', 'tool'),
    'socket': ('套筒与棘轮配件', 'tool'),
    'workshopSystem': ('车间排程看板系统', 'tool'),
    'workstation': ('工厂流水线操作工位台', 'tool'),
    'extractor': ('工业抽提机与抽风机', 'tool'),
    'extrusion': ('工业铝型材挤出件', 'tool'),
    'pump': ('工业流体输送泵', 'tool'),
    'power': ('电源动力配电装置', 'tool'),
    'construction': ('施工建造结构部件', 'tool'),

    # 仓储物流与包装 (logistics)
    'box': ('包装箱与周转纸箱', 'logistics'),
    'pallet': ('标准物流托盘栈板', 'logistics'),
    'palletJack': ('手动/电动托盘搬运地牛', 'logistics'),
    'crate': ('塑料周转筐与网格箱', 'logistics'),
    'container': ('工业容器与储料罐', 'logistics'),
    'drum': ('大容量工业桶/油桶', 'logistics'),
    'ibcTank': ('IBC复合中型散装吨桶', 'logistics'),
    'pail': ('工业手提桶与涂料桶', 'logistics'),
    'bucket': ('通用手提水桶与储料桶', 'logistics'),
    'rack': ('高位仓储货架与物料架', 'logistics'),
    'storage': ('储物整理架与收纳篮', 'logistics'),
    'storageSystem': ('自动化立体仓储系统', 'logistics'),
    'shelve': ('货架置物层板', 'logistics'),
    'cart': ('手推板车与平板物流车', 'logistics'),
    'trolley': ('多层台车与工具推车', 'logistics'),
    'handTruck': ('两轮直立搬运推车', 'logistics'),
    'tiltTruck': ('可倾卸式大容量推车', 'logistics'),
    'conveyor': ('输送机与传送带单元', 'logistics'),
    'hopper': ('储料斗与下料斗', 'logistics'),
    'tape': ('封箱胶带与台式胶带切割座', 'logistics'),
    'paperbag': ('牛皮纸包装袋', 'logistics'),
    'pack': ('打包耗材与软包装', 'logistics'),
    'warehouse': ('大型钢构仓储立柱与角件', 'logistics'),
    'case': ('工业防护仪器箱与周转箱', 'logistics'),

    # 食品与生鲜 (food)
    'food': ('食品、生鲜、料理与酒水', 'food'),

    # 厨房餐饮与日用 (kitchen)
    'kitchenware': ('厨房烹饪锅具与餐厨用品', 'kitchen'),
    'dishware': ('餐盘、餐碗与杯具', 'kitchen'),
    'utensil': ('烹饪铲勺与硅胶厨具', 'kitchen'),
    'utensils': ('餐厨剪刀与削皮小工具', 'kitchen'),
    'appliance': ('厨房家电（洗碗机/油烟机/烤箱等）', 'kitchen'),
    'refrigerator': ('商用与家用保鲜冰箱冷柜', 'kitchen'),
    'water': ('饮水机与水处理水具', 'kitchen'),
    'bottle': ('调味瓶、水壶与日用储瓶', 'kitchen'),
    'tray': ('备餐托盘与 Serving 盘', 'kitchen'),

    # 医疗器械与健康 (medical)
    'instrument': ('医疗手术精细器械（钳/镊/刀）', 'medical'),
    'device': ('医疗检测与监护诊断设备', 'medical'),
    'anesthesia': ('麻醉机系统与呼吸面罩', 'medical'),
    'Xray': ('数字化 X 射线摄影机系统', 'medical'),
    'CT': ('计算机断层扫描 CT 诊断机', 'medical'),
    'hemodialysis': ('血液透析机系统', 'medical'),
    'ultrasound': ('超声多普勒成像诊断仪', 'medical'),
    'defibrillator': ('自动体外除颤仪(AED)', 'medical'),
    'blood': ('血液采集、化验与导管耗材', 'medical'),
    'syringe': ('医用一次性注射器', 'medical'),
    'needle': ('无菌注射针头与穿刺针', 'medical'),
    'catheter': ('医用介入导管系统', 'medical'),
    'cannulae': ('静脉留置针与套管针', 'medical'),
    'bandage': ('医用无菌弹性绷带', 'medical'),
    'drape': ('无菌手术洞巾与隔离铺单', 'medical'),
    'medicine': ('药品、西药药盒与口服液', 'medical'),
    'bed': ('多功能医用护理病床', 'medical'),
    'bedding': ('医用病床床垫与床单被套', 'medical'),
    'wheelChair': ('医用与康复护理轮椅', 'medical'),
    'screen': ('病房医用折叠隔断屏风', 'medical'),
    'oximeter': ('指夹式脉搏血氧饱和度仪', 'medical'),
    'thermometer': ('红外电子体温计', 'medical'),
    'stethoscope': ('医用双头听诊器', 'medical'),
    'warmer': ('恒温输液加温仪', 'medical'),
    'medical': ('综合医疗耗材与护理用品', 'medical'),
    'IV': ('输液架与重力输液管路系统', 'medical'),
    'lung': ('人工模拟呼吸测试肺囊', 'medical'),
    'tube': ('医用硅胶软管与导流管', 'medical'),
    'clogs': ('洁净室手术专用防滑洞洞鞋', 'medical'),

    # 安全环保劳保 (safety)
    'ppe': ('个人安全防护装备(PPE)', 'safety'),
    'mask': ('防护防尘防烟口罩', 'safety'),
    'facemask': ('医用透明防飞沫面罩', 'safety'),
    'safety': ('紧急洗眼器与安全急救设施', 'safety'),
    'safetyBoard': ('工厂安全生产告示看板', 'safety'),
    'security': ('安保监控与出入口控制设施', 'safety'),
    'fireProtection': ('消防栓箱与火警警报按钮', 'safety'),
    'fireExtinguisher': ('ABC干粉与二氧化碳灭火器', 'safety'),
    'sign': ('立式安全警示牌与指示牌', 'safety'),
    'cleaning': ('保洁洗涤用品与去污研磨粉', 'safety'),
    'disinfectant': ('医用消毒洗手液与壁挂分配机', 'safety'),
    'consumable': ('工业吸油棉垫与泄漏处理卷纸', 'safety'),
    'wasteManagement': ('固废分类回收箱与防火垃圾桶', 'safety'),
    'waste': ('工业废料桶与环保回收容器', 'safety'),
    'bin': ('脚踏式卫生垃圾桶', 'safety'),
    'trashCan': ('大容量圆形塑料垃圾桶', 'safety'),
    'trash': ('废弃物收集桶', 'safety'),
    'barrier': ('工业安全防护栏与伸缩门', 'safety'),
    'wire': ('机床安全围栏与防盗铁丝网', 'safety'),
    'paint': ('调色漆桶与工业喷漆罐', 'safety'),

    # 办公家具与设施 (office)
    'cabinet': ('办公文件柜与易燃品防爆柜', 'office'),
    'desk': ('办公桌与电脑工位桌', 'office'),
    'table': ('会议桌与多功能台桌', 'office'),
    'chair': ('人体工学办公转椅与就诊椅', 'office'),
    'stool': ('实验升降圆凳与垫脚凳', 'office'),
    'sofa': ('接待休闲沙发', 'office'),
    'computer': ('台式电脑主机与键盘外设', 'office'),
    'monitor': ('办公液晶显示器', 'office'),
    'stationery': ('办公文具用品与粉笔', 'office'),
    'stationary': ('桌面办公文具用品', 'office'),
    'stapler': ('办公省力订书机', 'office'),
    'paper': ('复印纸与办公用纸', 'office'),
    'book': ('精装书与参考书籍', 'office'),
    'magazines': ('报刊杂志摆件', 'office'),
    'phone': ('按键式办公固定电话机', 'office'),
    'TV': ('壁挂式液晶智能电视屏', 'office'),
    'video': ('多媒体视频会议终端一体机', 'office'),
    'lighting': ('天花板嵌入式荧光灯与LED灯', 'office'),
    'lamp': ('现代吸顶灯与矩形吊灯', 'office'),
    'light': ('车间与办公室照明灯具', 'office'),
    'blinds': ('2米/4米 开闭式百叶窗帘', 'office'),
    'structure': ('重型建筑工字钢梁与框架柱', 'office'),
    'panel': ('建筑装饰板与墙体板件', 'office'),
    'pipe': ('给排水管道与PVC接头', 'office'),
    'drainage': ('不锈钢地漏与地面排水槽', 'office'),
    'sanitary': ('现代卫浴洁具设施', 'office'),
    'sink': ('不锈钢水槽与洗涤洗手池', 'office'),
    'toilet': ('陶瓷节水抽水马桶', 'office'),
    'washBasin': ('陶瓷洗脸盆与多联洗手台', 'office'),
    'fauset': ('冷热水龙头', 'office'),
    'climate': ('智能温控器与暖通调节面板', 'office'),
    'hvac': ('暖通新风风口与空调管路', 'office'),
    'ventilation': ('工业级 HVLS 大风量吊扇', 'office'),
    'purifier': ('空气净化器', 'office'),
    'humidifier': ('超声波静音加湿器', 'office'),
    'furniture': ('室内商用与办公家具', 'office'),
    'fixture': ('室内固定橱柜与隔板', 'office'),
    'facilityEquipment': ('楼宇后勤设施设备', 'office'),
    'facilityFurniture': ('后勤公共家具设施', 'office'),
    'facilitySystem': ('楼宇公用设施控制系统', 'office'),
    'dispenser': ('洗手液机与自动出纸盒', 'office'),
    'mirror': ('梳妆卫浴玻璃镜', 'office'),

    # 机器人与自动化 (robotics)
    'robotic': ('工业机器人机械臂总成', 'robotics'),
    'robot': ('工业自动化机器人', 'robotics'),
    'robotics': ('机器人运动控制系统', 'robotics'),
    'arm': ('铰接多轴支撑机械臂', 'robotics'),
    'electrical': ('工业电气控制元器件', 'robotics'),
    'electricalSystem': ('车用交流发电机电气系统', 'robotics'),
    'digitalSystem': ('落地式数控触摸终端机', 'robotics'),
    'detector': ('自动化工控传感器检测仪', 'robotics'),
    'laser': ('工业激光标线校准设备', 'robotics'),

    # 装饰与杂项 (misc)
    'decor': ('香薰蜡烛与室内艺术摆件', 'misc'),
    'toy': ('物理碰撞测试玻璃弹珠', 'misc'),
    'accessory': ('防蓝光近视眼镜与服饰配饰', 'misc'),
    'misc': ('通用木板堆、塑料杂物筐等', 'misc'),
    'modular': ('工业模块化组合装配件', 'misc'),
    'grid': ('工业防滑地栅格网板', 'misc'),
    'rail': ('滑动导轨与滑移支撑', 'misc'),
    'ramp': ('无障碍轮椅与装卸斜坡台', 'misc'),
    'unit': ('功能组合模块单元', 'misc'),
    'set': ('工具配件成套组合', 'misc'),
    'supply': ('车间消耗备件与物资', 'misc'),
    'pad': ('防撞防震工业衬垫', 'misc'),
    'pendant': ('天花板悬吊吊挂构件', 'misc'),
    'prop': ('场景物理仿真道具模型', 'misc'),
    'environment': ('仿真场景周边辅助资产', 'misc'),
}

# 3. 词汇翻译映射表
WORD_MAP = {
    # 颜色
    'blue': '蓝色', 'black': '黑色', 'white': '白色', 'red': '红色', 'green': '绿色',
    'yellow': '黄色', 'orange': '橙色', 'gray': '灰色', 'grey': '灰色', 'brown': '棕色',
    
    # 材质
    'plastic': '塑料', 'metal': '金属', 'steel': '钢制', 'wooden': '实木', 'wood': '木质',
    'glass': '玻璃', 'rubber': '橡胶', 'silicone': '硅胶', 'cardboard': '瓦楞纸',
    'corrugated': '瓦楞', 'fiberglass': '玻璃钢', 'fiber': '纤维', 'ceramic': '陶瓷',
    
    # 方位与修饰
    'front': '前', 'rear': '后', 'left': '左', 'right': '右', 'upper': '上', 'lower': '下',
    'center': '中间', 'inner': '内', 'outer': '外', 'side': '侧', 'standing': '立式',
    'portable': '便携式', 'modular': '模块化', 'automatic': '自动感应', 'manual': '手动',
    'large': '大号', 'small': '小号', 'mini': '迷你', 'heavy': '重型', 'multidepth': '多深可调',
    'cube': '正方体', 'round': '圆形', 'square': '方形', 'rectangle': '矩形', 'rectangular': '矩形',
    'closed': '闭合', 'open': '开启', 'folded': '折叠', 'stacked': '叠放', 'loose': '松脱', 'tight': '紧固',
    
    # 汽车与动力系统
    'bumper': '保险杠', 'door': '车门', 'boot': '后备箱盖', 'trunk': '后备箱盖', 'lid': '盖',
    'hood': '引擎盖', 'fender': '翼子板', 'spoiler': '扰流尾翼', 'skirt': '侧裙板',
    'mirror': '后视镜', 'taillight': '尾灯', 'headlight': '前大灯', 'quarter': '后侧围',
    'window': '车窗', 'windshield': '挡风玻璃', 'frame': '车架', 'chassis': '底盘', 'roof': '车顶',
    'camshaft': '凸轮轴', 'crankshaft': '曲轴', 'piston': '活塞', 'cylinder': '气缸体',
    'flywheel': '飞轮', 'belt': '传动皮带', 'serpentine': '多楔带', 'tensioner': '张紧轮',
    'timing': '正时', 'chain': '链条', 'sprocket': '链轮', 'intersprocket': '中间链轮',
    'pulley': '皮带轮', 'sparkplug': '火花塞', 'spark': '火花', 'plug': '插头',
    'manifold': '歧管', 'intake': '进气', 'exhaust': '排气', 'dipstick': '机油标尺',
    'axle': '车轴', 'shaft': '传动轴', 'differential': '差速器', 'transmission': '变速箱',
    'clutch': '离合器', 'gear': '齿轮', 'suspension': '悬挂', 'coilover': '绞牙避震器',
    'shock': '减震器', 'absorber': '避震筒', 'strut': '减震支柱', 'spring': '弹簧',
    'controlarm': '控制臂', 'link': '连杆', 'swaybar': '防倾杆', 'brake': '制动刹车',
    'caliper': '刹车制动钳', 'rotor': '刹车盘', 'booster': '真空助力器', 'master': '主缸',
    'steering': '转向机构', 'powersteering': '动力转向', 'radiator': '散热水箱',
    'coolant': '防冻液', 'reservoir': '储液罐', 'catalytic': '三元催化', 'converter': '转化器',
    'muffler': '消声器', 'fuelinjector': '喷油嘴', 'carburetor': '化油器', 'airfilter': '空气滤清器',
    'compressor': '压缩机/空压机', 'tire': '轮胎', 'rim': '轮毂', 'wheelchock': '轮档三角木',
    'armrest': '扶手箱', 'seat': '座椅', 'jack': '千斤顶', 'scissor': '剪式',
    'lathe': '刹车盘车削机', 'spraygunholder': '喷枪挂架', 'straightening': '校正机',
    'bottlehydraulic': '立式液压', 'chock': '轮档木',
    
    # 工具与五金
    'ratchet': '棘轮扳手', 'wrench': '扳手', 'combination': '梅花开口两用', 'hammer': '手锤',
    'pliers': '钳子', 'groove': '水泵钳', 'joint': '活动关节', 'screwdriver': '螺丝刀',
    'hex': '内六角', 'socket': '套筒', 'pry': '撬动', 'bar': '撬棍', 'hook': '弯钩',
    'drill': '电钻', 'impact': '冲击式', 'grinder': '角磨机', 'cutter': '切刀', 'saw': '手锯',
    'clamp': '固定夹', 'vise': '台虎钳', 'multimeter': '万用表', 'codereader': '故障诊断仪',
    'code': '故障码', 'reader': '诊断仪', 'gauge': '压力表', 'bolt': '螺栓', 'nut': '螺母',
    'washer': '平垫圈', 'ladder': '登高梯', 'stepstool': '登高脚踏凳', 'workbench': '工作台',
    'tape': '卷尺/胶带', 'dispenser': '胶带切割座', 'tap': '丝锥', 'scanner': '扫描枪',
    'barcode': '条码', 'brush': '毛刷', 'supplies': '耗材', 'paint': '涂料/油漆',
    
    # 仓储物流与包装
    'pallet': '托盘栈板', 'palletjack': '地牛搬运车', 'crate': '周转筐', 'box': '包装箱',
    'drum': '工业圆桶', 'ibctank': 'IBC散装吨桶', 'pail': '工业提桶', 'bucket': '手提水桶',
    'rack': '仓储货架', 'cart': '推车', 'trolley': '双层推车', 'handtruck': '拉货小推车',
    'conveyor': '输送带单元', 'hopper': '漏斗', 'jar': '储物罐', 'bottle': '瓶', 'tank': '储液罐',
    'waste': '废弃物/废液', 'oil': '机油', 'fireresistant': '阻燃防火', 'fire': '防火/消防',
    'resistant': '耐受型', 'cubebox': '正方体箱',
    
    # 食品与生鲜酒水
    'produce': '生鲜', 'beverage': '酒水饮料', 'prepared': '熟食料理', 'processed': '预包装',
    'apple': '苹果', 'honeycrisp': '蜜脆', 'grannysmith': '青苹果', 'gala': '嘎啦果',
    'banana': '香蕉', 'orange': '橙子', 'lemon': '柠檬', 'lime': '青柠', 'pear': '雪梨',
    'peach': '水蜜桃', 'strawberry': '草莓', 'grape': '葡萄', 'watermelon': '西瓜',
    'tomato': '番茄', 'potato': '土豆', 'onion': '洋葱', 'carrot': '胡萝卜', 'cucumber': '黄瓜',
    'lettuce': '生菜', 'cabbage': '卷心菜', 'pepper': '甜椒', 'broccoli': '西兰花',
    'mushroom': '蘑菇', 'beer': '啤酒', 'beerbottle': '啤酒瓶', 'can': '易拉罐',
    'soda': '碳酸汽水', 'juice': '果汁', 'milk': '纯牛奶', 'wine': '葡萄酒', 'bottledwater': '瓶装饮用水',
    'burger': '汉堡包', 'sandwich': '三明治', 'pizza': '披萨', 'hotdog': '热狗',
    'donut': '甜甜圈', 'bread': '烘焙面包', 'baguette': '法棍面包', 'croissant': '牛角面包',
    'toast': '吐司', 'chips': '薯片', 'cannedfood': '罐头食品', 'boxedfood': '盒装快餐',
    'chocolate': '巧克力', 'ketchup': '番茄酱', 'egg': '鲜鸡蛋', 'chicken': '生鲜鸡肉',
    'beef': '牛肉', 'pork': '猪肉', 'fish': '鱼肉', 'mango': '芒果',
    
    # 厨房日用与家电
    'cuttingboard': '切菜砧板', 'pot': '烹饪锅', 'saucepan': '单柄奶锅', 'stockpot': '双耳深汤锅',
    'frypan': '平底煎锅', 'wok': '炒锅', 'kettle': '水壶', 'mug': '马克杯', 'cup': '水杯',
    'coffeecup': '咖啡杯', 'bowl': '餐碗', 'plate': '浅餐盘', 'dish': '餐碟',
    'spatula': '锅铲', 'spoon': '汤勺', 'fork': '西餐叉', 'knife': '餐刀', 'scissors': '剪刀',
    'whisk': '打蛋器', 'tongs': '食物夹', 'dishwasher': '嵌入式洗碗机', 'refrigerator': '保鲜冰箱',
    'toaster': '烤面包机', 'handdryer': '干手烘手机', 'extractor': '强劲抽油烟机',
    
    # 医疗器械与健康
    'forceps': '止血钳', 'artery': '止血', 'curved': '弯头', 'scalpel': '手术刀柄',
    'retractor': '创口拉钩', 'tamper': '充填压实器', 'endoscope': '电子内窥镜', 'catheter': '介入导管',
    'anesthesiamachine': '多功能麻醉机', 'xraymachine': '数字化医用X光机', 'buckystand': '立式胸片架',
    'buckytable': '电动摄影床', 'hemodialysis': '血液透析机', 'ultrasound': '超声探头诊断仪',
    'defibrillator': '急救AED除颤仪', 'glucosemeter': '血糖仪', 'bloodbag': '采血储血袋',
    'bloodline': '透析体外循环管路', 'syringe': '一次性无菌注射器', 'needle': '注射针头', 'cannulae': '静脉留置套管针',
    'bandage': '医用无菌弹性绷带', 'drape': '外科手术铺单', 'medicine': '处方药品', 'hospitalbed': '多功能医用病床',
    'wheelchair': '康复护理轮椅', 'oximeter': '指夹血氧仪', 'thermometer': '电子体温计', 'stethoscope': '心肺双头听诊器',
    'infusionwarmer': '恒温输液加温仪', 'clogs': '洁净室手术防滑洞洞鞋', 'pen': '签字笔', 'soapdispenser': '自动感应皂液器',
    
    # 劳保与安防
    'ppe': '劳保防护装备', 'helmet': '安全头盔', 'hardhat': '安全帽', 'faceshield': '透明防护面屏',
    'goggles': '宽边防冲击护目镜', 'safetyglasses': '护目安全眼镜', 'gloves': '耐磨防护手套',
    'eyewashstation': '紧急冲淋洗眼器', 'firstaidcabinet': '金属急救药箱', 'fireextinguisher': '手提式灭火器',
    'absorbentpad': '工业吸油吸液棉垫', 'absorbentroll': '车间擦拭吸液卷纸', 'oilywastecan': '防火含油抹布脚踏安全桶',
    'trashbin': '分类滚轮垃圾桶', 'fence': '金属隔离网护栏', 'gate': '车间联动安全门',
    
    # 办公设施与家具
    'filecabinet': '铁皮文件资料柜', 'chair': '人体工学办公椅', 'desk': '办公电脑桌', 'keyboard': '电脑键盘',
    'monitor': '办公液晶显示器', 'blinds': '室内遮光百叶窗', 'overheadled': '吊顶LED平板灯', 'beam': '重型工字钢梁',
    'sink': '不锈钢洗手水槽', 'toilet': '抽水坐便马桶', 'washbasin': '连体洗手面盆', 'ceilingfan': '工业节能大吊扇',
    'printer': '3D/办公打印机', 'eyeglasses': '护目近视眼镜', 'touchterminal': '数控触控终端机'
}

def translate_asset_name_improved(name, cat_zh):
    parts = name.split('_')
    subparts = parts[1:]
    
    tag = ''
    tokens = []
    
    if len(subparts) == 1 and re.match(r'^[a-z]\d+$', subparts[0], re.I):
        tag = subparts[0].upper()
        clean_cat = cat_zh.split('（')[0].split('与')[0].split('/')[0].strip()
        return f'{clean_cat} ({tag})'
        
    for p in subparts:
        if re.match(r'^[a-z]\d+$', p, re.I):
            tag = p.upper()
        else:
            tokens.extend(re.findall(r'[A-Za-z]+|\d+', p))
            
    zh_words = []
    for t in tokens:
        tl = t.lower()
        if tl in WORD_MAP:
            translated = WORD_MAP[tl]
            if translated not in zh_words:
                zh_words.append(translated)
        elif tl.isdigit():
            zh_words.append(tl)
            
    if not zh_words:
        title = ' '.join(tokens).title()
    else:
        title = ' '.join(zh_words)
        
    if len(zh_words) <= 2 and any(w in ['塑料', '钢制', '金属', '实木', '蓝色', '黑色', '白色', '红色', '黄色'] for w in zh_words):
        clean_cat = cat_zh.split('（')[0].split('与')[0].split('/')[0].strip()
        if clean_cat not in title:
            title = f'{title} {clean_cat}'
            
    if tag:
        title = f'{title} ({tag})'
        
    return title

def format_bytes(b):
    if b >= 1e9:
        return f"{b / 1e9:.1f} GB"
    if b >= 1e6:
        return f"{b / 1e6:.1f} MB"
    return f"{round(b / 1e3)} KB"

def build_catalog():
    print("开始加载数据并构建左右布局 + 纯净工程风格目录...")
    
    with open('assets_cache.json', 'r', encoding='utf-8') as f:
        raw_assets = json.load(f)
        
    processed_assets = []
    domain_counts = {k: 0 for k in DOMAINS}
    cat_counts = {}
    
    total_blender_bytes = 0
    total_glb_bytes = 0
    moving_models_count = 0
    
    for idx, row in enumerate(raw_assets):
        name = row[0]
        blender_bytes = row[1]
        glb_bytes = row[2]
        blender_triangles = row[3]
        triangles = row[4]
        blender_draw_calls = row[5]
        draw_calls = row[6]
        textures = row[7]
        tex_edge = row[8]
        joints = row[9] if len(row) > 9 else 0
        
        total_blender_bytes += blender_bytes
        total_glb_bytes += glb_bytes
        if joints > 0:
            moving_models_count += 1
        
        cat_key = name.split('_')[0]
        cat_info = CATEGORIES.get(cat_key, (cat_key, 'misc'))
        cat_zh = cat_info[0]
        domain_key = cat_info[1]
        
        domain_counts[domain_key] = domain_counts.get(domain_key, 0) + 1
        cat_counts[cat_key] = cat_counts.get(cat_key, 0) + 1
        
        name_zh = translate_asset_name_improved(name, cat_zh)
        compression_ratio = round(blender_bytes / max(1, glb_bytes))
        
        processed_assets.append({
            'id': idx,
            'name': name,
            'nameZh': name_zh,
            'category': cat_key,
            'categoryZh': cat_zh,
            'domain': domain_key,
            'domainName': DOMAINS[domain_key]['name'],
            'bytes': glb_bytes,
            'bytesFormatted': format_bytes(glb_bytes),
            'blenderBytes': blender_bytes,
            'blenderBytesFormatted': format_bytes(blender_bytes),
            'ratio': compression_ratio,
            'triangles': triangles,
            'blenderTriangles': blender_triangles,
            'drawCalls': draw_calls,
            'textures': textures,
            'texEdge': tex_edge,
            'joints': joints,
            'thumb': f"https://huggingface.co/datasets/codepawl/simready-glb/resolve/main/thumbs/{name}.webp",
            'glbUrl': f"https://huggingface.co/datasets/codepawl/simready-glb/resolve/main/glb/{name}.glb",
            'viewerUrl': f"https://huggingface.co/spaces/codepawl/simready-glb-viewer#/m/{name}",
            'sourceUrl': f"https://huggingface.co/datasets/nvidia/simready-assets/tree/main/{name}"
        })
        
    print(f"数据索引成功: 共 {len(processed_assets)} 个模型，含物理关节模型 {moving_models_count} 个。")
    print(f"原始大小: {format_bytes(total_blender_bytes)} -> 压缩后大小: {format_bytes(total_glb_bytes)} (平均节省 ~{round(total_blender_bytes/total_glb_bytes)}倍)")
    
    assets_json_str = json.dumps(processed_assets, ensure_ascii=False)
    domains_json_str = json.dumps(DOMAINS, ensure_ascii=False)
    categories_json_str = json.dumps(CATEGORIES, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NVIDIA SimReady 3D 资产库 · 选型目录</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    /* =========================================================
       明暗主题 CSS 变量系统 (纯净工程配色，无Emoji装饰)
       ========================================================= */
    :root {{
      /* 默认深色主题 (Dark Theme) */
      --bg-main: #0b0f19;
      --bg-sidebar: #111827;
      --bg-surface: #111827;
      --bg-card: #172033;
      --bg-card-hover: #1f2b42;
      --border-color: #273549;
      --border-light: rgba(255, 255, 255, 0.07);
      
      --accent: #10b981;
      --accent-hover: #059669;
      --accent-glow: rgba(16, 185, 129, 0.15);
      --accent-blue: #38bdf8;
      --accent-purple: #a78bfa;
      
      --text-main: #f9fafb;
      --text-sub: #94a3b8;
      --text-muted: #64748b;
      
      --top-nav-bg: rgba(17, 24, 39, 0.95);
      --thumb-bg: radial-gradient(circle at 50% 50%, #202b3d 0%, #0f172a 100%);
      --modal-bg: #111827;
      --table-header-bg: #141d2e;
      --spec-box-bg: rgba(0, 0, 0, 0.25);
      --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
      --nav-hover-bg: #1e293b;
      --nav-active-bg: #1e293b;
      
      --btn-secondary-bg: #1e293b;
      --btn-secondary-text: #cbd5e1;
      --btn-secondary-hover: #334155;

      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --font-family: 'Inter', 'Noto Sans SC', system-ui, -apple-system, sans-serif;
    }}

    /* 亮色主题 (Light Theme) */
    [data-theme="light"] {{
      --bg-main: #f8fafc;
      --bg-sidebar: #ffffff;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f5f9;
      --border-color: #e2e8f0;
      --border-light: rgba(0, 0, 0, 0.05);
      
      --accent: #059669;
      --accent-hover: #047857;
      --accent-glow: rgba(5, 150, 105, 0.12);
      --accent-blue: #0284c7;
      --accent-purple: #7c3aed;
      
      --text-main: #0f172a;
      --text-sub: #475569;
      --text-muted: #94a3b8;
      
      --top-nav-bg: rgba(255, 255, 255, 0.95);
      --thumb-bg: radial-gradient(circle at 50% 50%, #f8fafc 0%, #e2e8f0 100%);
      --modal-bg: #ffffff;
      --table-header-bg: #f8fafc;
      --spec-box-bg: rgba(0, 0, 0, 0.03);
      --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      --nav-hover-bg: #f1f5f9;
      --nav-active-bg: #f0fdf4;
      
      --btn-secondary-bg: #f1f5f9;
      --btn-secondary-text: #334155;
      --btn-secondary-hover: #e2e8f0;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: var(--font-family);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.2s ease, color 0.2s ease;
    }}

    /* 滚动条 */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}

    /* =========================================================
       顶部精炼导航栏
       ========================================================= */
    header.top-nav {{
      height: 58px;
      background: var(--top-nav-bg);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-title {{
      font-size: 1.05rem;
      font-weight: 700;
      letter-spacing: -0.3px;
      color: var(--text-main);
    }}

    .brand-badge {{
      font-size: 0.72rem;
      font-weight: 600;
      background: var(--accent-glow);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--accent);
      letter-spacing: 0.5px;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    /* 通用按钮 */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      font-size: 0.8rem;
      font-weight: 500;
      padding: 0.45rem 0.85rem;
      border-radius: var(--radius-sm);
      text-decoration: none;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}

    .btn-primary {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }}
    .btn-primary:hover {{
      background: var(--accent-hover);
      border-color: var(--accent-hover);
    }}

    .btn-secondary {{
      background: var(--btn-secondary-bg);
      color: var(--btn-secondary-text);
      border-color: var(--border-color);
    }}
    .btn-secondary:hover {{
      background: var(--btn-secondary-hover);
      color: var(--text-main);
    }}

    .btn-outline {{
      background: transparent;
      border-color: var(--border-color);
      color: var(--text-sub);
    }}
    .btn-outline:hover {{
      border-color: var(--accent);
      color: var(--text-main);
    }}

    /* =========================================================
       左右分栏布局系统
       ========================================================= */
    .app-layout {{
      display: flex;
      flex: 1;
      min-height: calc(100vh - 58px);
    }}

    /* 左侧控制与导航侧边栏 */
    aside.sidebar {{
      width: 320px;
      min-width: 320px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      position: sticky;
      top: 58px;
      height: calc(100vh - 58px);
      overflow-y: auto;
      padding: 1.25rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 1.4rem;
    }}

    .sidebar-section {{
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }}

    .sidebar-label {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      padding: 0 0.4rem;
    }}

    /* 搜索框 */
    .search-box {{
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-size: 0.85rem;
      padding: 0.6rem 0.85rem;
      border-radius: var(--radius-sm);
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-glow);
    }}

    /* 侧边栏过滤器 */
    .filter-item {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .filter-item-label {{
      font-size: 0.75rem;
      color: var(--text-sub);
    }}

    .select-input {{
      width: 100%;
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.5rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      outline: none;
      cursor: pointer;
    }}
    .select-input:focus {{
      border-color: var(--accent);
    }}

    .switch-filter-btn {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 0.55rem 0.85rem;
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      color: var(--text-sub);
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .switch-filter-btn:hover {{
      color: var(--text-main);
      border-color: var(--accent);
    }}
    .switch-filter-btn.active {{
      background: var(--accent-glow);
      border-color: var(--accent);
      color: var(--accent);
      font-weight: 600;
    }}

    /* 垂直领域导航菜单 */
    .domain-nav-list {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .domain-nav-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.55rem 0.75rem;
      border-radius: var(--radius-sm);
      color: var(--text-sub);
      font-size: 0.84rem;
      font-weight: 500;
      cursor: pointer;
      border: 1px solid transparent;
      background: transparent;
      text-align: left;
      transition: all 0.15s;
    }}
    .domain-nav-item:hover {{
      background: var(--nav-hover-bg);
      color: var(--text-main);
    }}
    .domain-nav-item.active {{
      background: var(--nav-active-bg);
      color: var(--accent);
      font-weight: 600;
      border-color: var(--accent);
    }}

    .domain-count-badge {{
      font-size: 0.72rem;
      padding: 1px 6px;
      border-radius: 9999px;
      background: rgba(148, 163, 184, 0.15);
      color: var(--text-muted);
      font-weight: normal;
    }}
    .domain-nav-item.active .domain-count-badge {{
      background: var(--accent);
      color: #ffffff;
      font-weight: 600;
    }}

    /* 右侧主内容展示区 */
    main.main-content {{
      flex: 1;
      min-width: 0;
      padding: 1.5rem 2rem 3rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    /* 主内容区头部工具条 */
    .content-header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border-color);
    }}

    .content-header-title {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .current-domain-title {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--text-main);
    }}

    .current-domain-desc {{
      font-size: 0.8rem;
      color: var(--text-sub);
    }}

    .content-header-controls {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .view-mode-tabs {{
      display: flex;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 2px;
      border-radius: var(--radius-sm);
    }}

    .view-mode-btn {{
      padding: 4px 10px;
      font-size: 0.78rem;
      font-weight: 500;
      color: var(--text-muted);
      background: none;
      border: none;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .view-mode-btn.active {{
      background: var(--btn-secondary-bg);
      color: var(--text-main);
      font-weight: 600;
    }}

    /* =========================================================
       模型卡片网格系统
       ========================================================= */
    .model-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 1.25rem;
    }}

    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
      box-shadow: var(--card-shadow);
      position: relative;
    }}

    .card:hover {{
      transform: translateY(-2px);
      border-color: var(--accent);
    }}

    .card-thumb-container {{
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: var(--thumb-bg);
      overflow: hidden;
      cursor: pointer;
    }}

    .card-thumb {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.25s;
    }}

    .card:hover .card-thumb {{
      transform: scale(1.04);
    }}

    .card-tag-joint {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(167, 139, 250, 0.5);
      color: var(--accent-purple);
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 3px;
      backdrop-filter: blur(4px);
    }}

    .card-tag-ratio {{
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(16, 185, 129, 0.5);
      color: var(--accent);
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 3px;
      backdrop-filter: blur(4px);
    }}

    .card-body {{
      padding: 0.85rem;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
      gap: 0.75rem;
    }}

    .card-meta {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .card-category-text {{
      font-size: 0.72rem;
      color: var(--accent-blue);
      font-weight: 600;
    }}

    .card-title-zh {{
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.35;
      cursor: pointer;
    }}
    .card-title-zh:hover {{
      color: var(--accent);
    }}

    .card-title-en {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: monospace;
      word-break: break-all;
    }}

    .card-specs-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px 6px;
      background: var(--spec-box-bg);
      border: 1px solid var(--border-light);
      padding: 6px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.72rem;
      color: var(--text-sub);
    }}

    .card-specs-grid span strong {{
      color: var(--text-main);
    }}

    .card-actions-row {{
      display: flex;
      gap: 6px;
    }}

    .card-actions-row .btn {{
      padding: 0.4rem 0.5rem;
      font-size: 0.75rem;
      flex: 1;
    }}

    /* =========================================================
       详细表格视图
       ========================================================= */
    .table-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      overflow-x: auto;
      display: none;
      box-shadow: var(--card-shadow);
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.82rem;
    }}

    table.data-table th {{
      background: var(--table-header-bg);
      padding: 0.75rem 1rem;
      color: var(--text-sub);
      font-weight: 600;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
    }}

    table.data-table td {{
      padding: 0.65rem 1rem;
      border-bottom: 1px solid var(--border-light);
      color: var(--text-main);
      vertical-align: middle;
    }}

    table.data-table tr:hover td {{
      background: var(--bg-card-hover);
    }}

    .table-thumb {{
      width: 40px;
      height: 40px;
      border-radius: var(--radius-sm);
      object-fit: cover;
      background: var(--thumb-bg);
      vertical-align: middle;
      cursor: pointer;
    }}

    /* 加载更多 */
    .pagination-bar {{
      display: flex;
      justify-content: center;
      margin-top: 1.5rem;
    }}

    /* =========================================================
       详情弹窗 (Modal)
       ========================================================= */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}

    .modal-overlay.open {{
      display: flex;
    }}

    .modal-box {{
      background: var(--modal-bg);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      max-width: 800px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
      position: relative;
      color: var(--text-main);
    }}

    .modal-header {{
      padding: 1.2rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}

    .modal-close {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.4rem;
      cursor: pointer;
      padding: 0 4px;
    }}
    .modal-close:hover {{ color: var(--text-main); }}

    .modal-content {{
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    .modal-preview-grid {{
      display: grid;
      grid-template-columns: 260px 1fr;
      gap: 1.5rem;
    }}

    @media (max-width: 768px) {{
      .modal-preview-grid {{ grid-template-columns: 1fr; }}
    }}

    .modal-img {{
      width: 100%;
      aspect-ratio: 1/1;
      border-radius: var(--radius-md);
      object-fit: cover;
      background: var(--thumb-bg);
      border: 1px solid var(--border-color);
    }}

    .detail-spec-list dt {{
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 6px;
    }}

    .detail-spec-list dd {{
      font-size: 0.88rem;
      color: var(--text-main);
      font-weight: 600;
    }}

    .code-tabs {{
      display: flex;
      gap: 4px;
      margin-top: 1.2rem;
      margin-bottom: 0.4rem;
    }}

    .code-tab-btn {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-sub);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.78rem;
      cursor: pointer;
    }}

    .code-tab-btn.active {{
      background: var(--btn-secondary-bg);
      color: var(--text-main);
      font-weight: 600;
      border-color: var(--border-color);
    }}

    .code-block {{
      background: #0b0f19;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 0.8rem 1rem;
      font-family: monospace;
      font-size: 0.76rem;
      color: #a7f3d0;
      position: relative;
      overflow-x: auto;
      min-height: 85px;
    }}

    .code-copy-btn {{
      position: absolute;
      top: 6px;
      right: 6px;
      background: #1f2937;
      border: 1px solid #374151;
      color: #e5e7eb;
      font-size: 0.7rem;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
    }}
    .code-copy-btn:hover {{ background: #374151; }}

    /* 回到顶部 */
    .back-to-top {{
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      width: 40px;
      height: 40px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      transition: all 0.2s;
      z-index: 90;
      opacity: 0;
      pointer-events: none;
      font-size: 0.8rem;
      font-weight: 700;
    }}
    .back-to-top.show {{
      opacity: 1;
      pointer-events: auto;
    }}
    .back-to-top:hover {{
      background: var(--accent);
      color: #fff;
    }}

    /* 响应式折叠 */
    @media (max-width: 960px) {{
      aside.sidebar {{
        width: 260px;
        min-width: 260px;
      }}
    }}
    @media (max-width: 768px) {{
      .app-layout {{
        flex-direction: column;
      }}
      aside.sidebar {{
        width: 100%;
        min-width: 100%;
        height: auto;
        position: static;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
      }}
    }}
  </style>
</head>
<body>

  <!-- 顶部精简导航栏 -->
  <header class="top-nav">
    <div class="nav-brand">
      <span class="brand-title">NVIDIA SimReady 3D 资产库</span>
      <span class="brand-badge">汉化选型目录</span>
    </div>
    <div class="nav-actions">
      <button id="export-csv-btn" class="btn btn-secondary" title="导出当前筛选结果为 CSV 表格">导出 CSV</button>
      <button id="theme-toggle-btn" class="btn btn-outline" title="切换明亮 / 暗色模式">
        <span id="theme-text">暗色模式</span>
      </button>
    </div>
  </header>

  <!-- 左右主分栏结构 -->
  <div class="app-layout">
    
    <!-- 左侧固态侧边栏 (导航与参数筛选) -->
    <aside class="sidebar">
      
      <!-- 搜索输入 -->
      <div class="sidebar-section">
        <div class="sidebar-label">关键词检索</div>
        <div class="search-box">
          <input type="text" id="search-input" class="search-input" placeholder="输入中文或英文关键词...">
        </div>
      </div>

      <!-- 快速过滤与排序 -->
      <div class="sidebar-section">
        <div class="sidebar-label">筛选与排序</div>
        
        <div class="filter-item">
          <span class="filter-item-label">细分类别</span>
          <select id="category-select" class="select-input">
            <option value="">全部细分类 (192个)</option>
          </select>
        </div>

        <div class="filter-item">
          <span class="filter-item-label">排序方式</span>
          <select id="sort-select" class="select-input">
            <option value="default">默认排序</option>
            <option value="size-desc">文件体积 (大到小)</option>
            <option value="size-asc">文件体积 (小到大)</option>
            <option value="triangles-desc">面数 (多到少)</option>
            <option value="joints-desc">可动关节数 (多到少)</option>
          </select>
        </div>

        <button id="toggle-joints-btn" class="switch-filter-btn">
          <span>仅显示可动关节</span>
          <span id="joints-count-tag" style="font-size: 0.72rem; color: var(--text-muted);">{moving_models_count}个</span>
        </button>
      </div>

      <!-- 领域导航列表 -->
      <div class="sidebar-section" style="flex: 1;">
        <div class="sidebar-label">产业与仿真领域</div>
        <nav class="domain-nav-list" id="domain-nav-list">
          <button class="domain-nav-item active" data-domain="all">
            <span>全部领域</span>
            <span class="domain-count-badge">2595</span>
          </button>
        </nav>
      </div>

    </aside>

    <!-- 右侧内容展示区 -->
    <main class="main-content">
      
      <!-- 内容头部工具条 -->
      <div class="content-header">
        <div class="content-header-title">
          <div class="current-domain-title" id="domain-header-title">全部领域</div>
          <div class="current-domain-desc" id="domain-header-desc">涵盖全部 10 大产业体系，共 2,595 个优化后 Web 级 SimReady 3D 资产</div>
        </div>
        <div class="content-header-controls">
          <span style="font-size: 0.8rem; color: var(--text-sub); margin-right: 4px;">匹配 <strong id="filter-count" style="color: var(--text-main);">0</strong> 个</span>
          <div class="view-mode-tabs">
            <button id="view-grid-btn" class="view-mode-btn active">网格</button>
            <button id="view-table-btn" class="view-mode-btn">表格</button>
          </div>
        </div>
      </div>

      <!-- 网格视图 -->
      <div class="model-grid" id="grid-view"></div>

      <!-- 表格视图 -->
      <div class="table-container" id="table-view">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 50px;">预览</th>
              <th>中文名称 / 资产标识</th>
              <th>领域 / 分类</th>
              <th>GLB 体积</th>
              <th>面数</th>
              <th>关节</th>
              <th>贴图</th>
              <th style="text-align: right;">操作</th>
            </tr>
          </thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>

      <!-- 加载更多 -->
      <div class="pagination-bar" id="pagination-bar">
        <button class="btn btn-secondary" id="load-more-btn" style="padding: 0.65rem 2rem;">加载更多模型...</button>
      </div>

    </main>

  </div>

  <!-- 详情弹窗 Modal -->
  <div class="modal-overlay" id="detail-modal">
    <div class="modal-box">
      <div class="modal-header">
        <div>
          <h3 id="modal-title-zh" style="color: var(--text-main); font-size: 1.15rem; font-weight: 700;">模型详情</h3>
          <p id="modal-title-en" style="color: var(--text-muted); font-size: 0.78rem; font-family: monospace;"></p>
        </div>
        <button class="modal-close" id="modal-close">&times;</button>
      </div>
      <div class="modal-content">
        <div class="modal-preview-grid">
          <div>
            <img id="modal-img" class="modal-img" src="" alt="3D Model Thumbnail">
            <div style="margin-top: 0.8rem; display: flex; flex-direction: column; gap: 6px;">
              <a id="modal-viewer-link" href="" target="_blank" class="btn btn-primary">在线 3D 预览</a>
              <a id="modal-download-link" href="" target="_blank" class="btn btn-secondary">下载 .GLB 文件</a>
              <a id="modal-source-link" href="" target="_blank" class="btn btn-secondary" style="font-size: 0.72rem;">查看 NVIDIA 原始 USD</a>
            </div>
          </div>
          <div>
            <h4 style="font-size: 0.85rem; color: var(--text-sub); margin-bottom: 0.4rem; font-weight: 600;">工程技术参数</h4>
            <dl class="detail-spec-list" style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px 12px;">
              <div>
                <dt>所属领域</dt>
                <dd id="modal-domain">-</dd>
              </div>
              <div>
                <dt>细分分类</dt>
                <dd id="modal-category">-</dd>
              </div>
              <div>
                <dt>GLB 体积 (优化后)</dt>
                <dd id="modal-size">-</dd>
              </div>
              <div>
                <dt>原始工程体积</dt>
                <dd id="modal-blender-size" style="color: var(--text-muted); font-weight: normal;">-</dd>
              </div>
              <div>
                <dt>多边形三角面数</dt>
                <dd id="modal-triangles">-</dd>
              </div>
              <div>
                <dt>Draw Calls</dt>
                <dd id="modal-drawcalls">-</dd>
              </div>
              <div>
                <dt>物理关节数</dt>
                <dd id="modal-joints" style="color: var(--accent-purple);">-</dd>
              </div>
              <div>
                <dt>贴图最大尺寸</dt>
                <dd id="modal-texture">-</dd>
              </div>
            </dl>

            <!-- 代码调用选项卡 -->
            <div class="code-tabs">
              <button class="code-tab-btn active" data-tab="three">Three.js</button>
              <button class="code-tab-btn" data-tab="python">Python</button>
              <button class="code-tab-btn" data-tab="cli">HF CLI</button>
            </div>
            <div class="code-block">
              <button class="code-copy-btn" id="modal-copy-code">复制代码</button>
              <pre id="modal-code-text"></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 回到顶部 -->
  <button class="back-to-top" id="back-to-top" title="返回顶部">TOP</button>

  <!-- 数据与业务交互脚本 -->
  <script>
    const ASSETS = {assets_json_str};
    const DOMAIN_DEFS = {domains_json_str};
    const CATEGORY_DEFS = {categories_json_str};

    // 状态
    let currentDomain = 'all';
    let currentCategory = '';
    let searchQuery = '';
    let filterJointsOnly = false;
    let currentSort = 'default';
    let currentView = 'grid';
    let currentModalAsset = null;
    let currentCodeTab = 'three';

    let filteredAssets = [];
    let displayedCount = 0;
    const PAGE_SIZE = 60;

    // DOM 元素
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const sortSelect = document.getElementById('sort-select');
    const toggleJointsBtn = document.getElementById('toggle-joints-btn');
    const exportCsvBtn = document.getElementById('export-csv-btn');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeText = document.getElementById('theme-text');
    const domainNavList = document.getElementById('domain-nav-list');
    const domainHeaderTitle = document.getElementById('domain-header-title');
    const domainHeaderDesc = document.getElementById('domain-header-desc');
    const filterCount = document.getElementById('filter-count');
    const gridView = document.getElementById('grid-view');
    const tableView = document.getElementById('table-view');
    const tableBody = document.getElementById('table-body');
    const loadMoreBtn = document.getElementById('load-more-btn');
    const paginationBar = document.getElementById('pagination-bar');
    const viewGridBtn = document.getElementById('view-grid-btn');
    const viewTableBtn = document.getElementById('view-table-btn');
    const backToTopBtn = document.getElementById('back-to-top');

    // Modal
    const modal = document.getElementById('detail-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitleZh = document.getElementById('modal-title-zh');
    const modalTitleEn = document.getElementById('modal-title-en');
    const modalImg = document.getElementById('modal-img');
    const modalViewerLink = document.getElementById('modal-viewer-link');
    const modalDownloadLink = document.getElementById('modal-download-link');
    const modalSourceLink = document.getElementById('modal-source-link');
    const modalDomain = document.getElementById('modal-domain');
    const modalCategory = document.getElementById('modal-category');
    const modalSize = document.getElementById('modal-size');
    const modalBlenderSize = document.getElementById('modal-blender-size');
    const modalTriangles = document.getElementById('modal-triangles');
    const modalDrawcalls = document.getElementById('modal-drawcalls');
    const modalJoints = document.getElementById('modal-joints');
    const modalTexture = document.getElementById('modal-texture');
    const modalCodeText = document.getElementById('modal-code-text');
    const modalCopyCode = document.getElementById('modal-copy-code');
    const codeTabBtns = document.querySelectorAll('.code-tab-btn');

    // ==========================================
    // 明暗主题切换系统
    // ==========================================
    function applyTheme(theme) {{
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('simready_theme', theme);
      themeText.textContent = theme === 'light' ? '亮色模式' : '暗色模式';
    }}

    function initTheme() {{
      const saved = localStorage.getItem('simready_theme');
      if (saved) {{
        applyTheme(saved);
      }} else {{
        const systemPrefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
        applyTheme(systemPrefersLight ? 'light' : 'dark');
      }}

      themeToggleBtn.onclick = () => {{
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        applyTheme(current === 'dark' ? 'light' : 'dark');
      }};
    }}

    // 初始化左侧垂直领域导航
    function initDomainNav() {{
      const fragment = document.createDocumentFragment();
      for (const [key, item] of Object.entries(DOMAIN_DEFS)) {{
        const count = ASSETS.filter(a => a.domain === key).length;
        const btn = document.createElement('button');
        btn.className = 'domain-nav-item';
        btn.dataset.domain = key;
        btn.innerHTML = `<span>${{item.name}}</span><span class="domain-count-badge">${{count}}</span>`;
        btn.onclick = () => selectDomain(key);
        fragment.appendChild(btn);
      }}
      domainNavList.appendChild(fragment);
    }}

    // 更新细分类别下拉选项
    function updateCategoryOptions() {{
      const relevantAssets = currentDomain === 'all' 
        ? ASSETS 
        : ASSETS.filter(a => a.domain === currentDomain);

      const catCounts = new Map();
      for (const a of relevantAssets) {{
        catCounts.set(a.category, (catCounts.get(a.category) || 0) + 1);
      }}

      const sortedCats = [...catCounts.entries()].sort((a, b) => b[1] - a[1]);
      let optionsHtml = `<option value="">全部细分类 (${{catCounts.size}} 个)</option>`;
      for (const [catKey, count] of sortedCats) {{
        const catZh = CATEGORY_DEFS[catKey] ? CATEGORY_DEFS[catKey][0] : catKey;
        optionsHtml += `<option value="${{catKey}}">${{catZh}} (${{catKey}}) · ${{count}}</option>`;
      }}
      categorySelect.innerHTML = optionsHtml;
      categorySelect.value = currentCategory;
    }}

    function selectDomain(domainKey) {{
      currentDomain = domainKey;
      document.querySelectorAll('.domain-nav-item').forEach(item => {{
        item.classList.toggle('active', item.dataset.domain === domainKey);
      }});

      if (domainKey === 'all') {{
        domainHeaderTitle.textContent = '全部领域';
        domainHeaderDesc.textContent = '涵盖全部 10 大产业体系，共 2,595 个 Web 级 SimReady 3D 仿真资产';
      }} else {{
        domainHeaderTitle.textContent = DOMAIN_DEFS[domainKey].name;
        domainHeaderDesc.textContent = DOMAIN_DEFS[domainKey].desc;
      }}

      currentCategory = '';
      updateCategoryOptions();
      applyFilters();
    }}

    // 筛选与排序
    function applyFilters() {{
      const query = searchQuery.trim().toLowerCase();
      const tokens = query.split(/\\s+/).filter(Boolean);

      filteredAssets = ASSETS.filter(asset => {{
        if (currentDomain !== 'all' && asset.domain !== currentDomain) return false;
        if (currentCategory && asset.category !== currentCategory) return false;
        if (filterJointsOnly && asset.joints === 0) return false;

        if (tokens.length > 0) {{
          const searchText = `${{asset.name}} ${{asset.nameZh}} ${{asset.categoryZh}} ${{asset.domainName}}`.toLowerCase();
          for (const t of tokens) {{
            if (!searchText.includes(t)) return false;
          }}
        }}
        return true;
      }});

      // 排序
      if (currentSort === 'size-desc') {{
        filteredAssets.sort((a, b) => b.bytes - a.bytes);
      }} else if (currentSort === 'size-asc') {{
        filteredAssets.sort((a, b) => a.bytes - b.bytes);
      }} else if (currentSort === 'triangles-desc') {{
        filteredAssets.sort((a, b) => b.triangles - a.triangles);
      }} else if (currentSort === 'joints-desc') {{
        filteredAssets.sort((a, b) => b.joints - a.joints);
      }}

      filterCount.textContent = filteredAssets.length.toLocaleString();

      displayedCount = 0;
      gridView.innerHTML = '';
      tableBody.innerHTML = '';
      renderMore();
    }}

    // 渲染卡片
    function createCard(asset) {{
      const card = document.createElement('div');
      card.className = 'card';
      
      const jointsBadge = asset.joints > 0 
        ? `<div class="card-tag-joint">关节: ${{asset.joints}}</div>` 
        : '';

      card.innerHTML = `
        <div class="card-thumb-container" onclick="openDetailModal(${{asset.id}})">
          <img class="card-thumb" src="${{asset.thumb}}" alt="${{asset.nameZh}}" loading="lazy" onerror="this.src='https://placehold.co/400x400/1e293b/94a3b8?text=SimReady'">
          ${{jointsBadge}}
          <div class="card-tag-ratio">${{asset.ratio}}× 压缩</div>
        </div>
        <div class="card-body">
          <div class="card-meta">
            <div class="card-category-text">${{asset.categoryZh}}</div>
            <div class="card-title-zh" onclick="openDetailModal(${{asset.id}})">${{asset.nameZh}}</div>
            <div class="card-title-en">${{asset.name}}</div>
          </div>
          <div>
            <div class="card-specs-grid">
              <span>大小: <strong>${{asset.bytesFormatted}}</strong></span>
              <span>面数: <strong>${{asset.triangles.toLocaleString()}}</strong></span>
              <span>贴图: <strong>${{asset.texEdge}}px</strong></span>
              <span>DrawCall: <strong>${{asset.drawCalls}}</strong></span>
            </div>
            <div class="card-actions-row" style="margin-top: 8px;">
              <a href="${{asset.viewerUrl}}" target="_blank" class="btn btn-primary" title="在官方 3D 视图中查看">3D 预览</a>
              <a href="${{asset.glbUrl}}?download=true" target="_blank" class="btn btn-secondary" title="下载优化后的 GLB 模型文件">下载</a>
              <button class="btn btn-secondary" onclick="openDetailModal(${{asset.id}})" style="flex: 0 0 36px;" title="查看详情参数与调用代码">详情</button>
            </div>
          </div>
        </div>
      `;
      return card;
    }}

    // 渲染表格行
    function createTableRow(asset) {{
      const tr = document.createElement('tr');
      const jointsBadge = asset.joints > 0 ? `<span style="color: var(--accent-purple); font-weight: 600;">${{asset.joints}}</span>` : `<span style="color: var(--text-muted);">-</span>`;
      
      tr.innerHTML = `
        <td>
          <img class="table-thumb" src="${{asset.thumb}}" alt="${{asset.nameZh}}" loading="lazy" onerror="this.src='https://placehold.co/80x80/1e293b/94a3b8?text=GLB'" onclick="openDetailModal(${{asset.id}})">
        </td>
        <td>
          <div style="font-weight: 600; color: var(--text-main); cursor: pointer;" onclick="openDetailModal(${{asset.id}})">${{asset.nameZh}}</div>
          <div style="font-size: 0.72rem; color: var(--text-muted); font-family: monospace;">${{asset.name}}</div>
        </td>
        <td>
          <div style="font-size: 0.78rem; color: var(--accent-blue); font-weight: 500;">${{asset.domainName}}</div>
          <div style="font-size: 0.72rem; color: var(--text-sub);">${{asset.categoryZh}}</div>
        </td>
        <td>
          <span style="font-weight: 600; color: var(--accent);">${{asset.bytesFormatted}}</span>
          <span style="font-size: 0.7rem; color: var(--text-muted);">(${{asset.ratio}}x)</span>
        </td>
        <td>${{asset.triangles.toLocaleString()}}</td>
        <td>${{jointsBadge}}</td>
        <td>${{asset.texEdge}}px</td>
        <td style="text-align: right; white-space: nowrap;">
          <a href="${{asset.viewerUrl}}" target="_blank" class="btn btn-primary" style="padding: 3px 8px; font-size: 0.72rem;">3D 预览</a>
          <a href="${{asset.glbUrl}}?download=true" target="_blank" class="btn btn-secondary" style="padding: 3px 8px; font-size: 0.72rem;">下载</a>
        </td>
      `;
      return tr;
    }}

    function renderMore() {{
      const nextBatch = filteredAssets.slice(displayedCount, displayedCount + PAGE_SIZE);
      if (nextBatch.length === 0 && displayedCount === 0) {{
        gridView.innerHTML = `<div style="grid-column: 1/-1; padding: 4rem; text-align: center; color: var(--text-muted);">暂无匹配的资产，请更换筛选条件。</div>`;
        paginationBar.style.display = 'none';
        return;
      }}

      if (currentView === 'grid') {{
        const fragment = document.createDocumentFragment();
        nextBatch.forEach(asset => fragment.appendChild(createCard(asset)));
        gridView.appendChild(fragment);
      }} else {{
        const fragment = document.createDocumentFragment();
        nextBatch.forEach(asset => fragment.appendChild(createTableRow(asset)));
        tableBody.appendChild(fragment);
      }}

      displayedCount += nextBatch.length;
      paginationBar.style.display = displayedCount < filteredAssets.length ? 'flex' : 'none';
    }}

    // 更新代码片段展示
    function updateModalCode(asset, tabKey) {{
      if (!asset) return;
      currentCodeTab = tabKey;
      codeTabBtns.forEach(b => b.classList.toggle('active', b.dataset.tab === tabKey));

      let codeStr = '';
      if (tabKey === 'three') {{
        codeStr = `import {{ GLTFLoader }} from 'three/addons/loaders/GLTFLoader.js';
import {{ MeshoptDecoder }} from 'three/addons/libs/meshopt_decoder.module.js';

const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
loader.load('${{asset.glbUrl}}', (gltf) => {{
  scene.add(gltf.scene);
}});`;
      }} else if (tabKey === 'python') {{
        codeStr = `from huggingface_hub import hf_hub_download

# 下载单个优化后的 GLB 模型
file_path = hf_hub_download(
    repo_id="codepawl/simready-glb",
    filename="glb/${{asset.name}}.glb",
    repo_type="dataset"
)
print("模型下载到:", file_path)`;
      }} else if (tabKey === 'cli') {{
        codeStr = `hf download codepawl/simready-glb "glb/${{asset.name}}.glb" --repo-type dataset --local-dir ./`;
      }}
      modalCodeText.textContent = codeStr;
    }}

    // 打开详情弹窗
    function openDetailModal(id) {{
      const asset = ASSETS[id];
      if (!asset) return;
      currentModalAsset = asset;

      modalTitleZh.textContent = asset.nameZh;
      modalTitleEn.textContent = asset.name;
      modalImg.src = asset.thumb;
      modalViewerLink.href = asset.viewerUrl;
      modalDownloadLink.href = `${{asset.glbUrl}}?download=true`;
      modalSourceLink.href = asset.sourceUrl;

      modalDomain.textContent = asset.domainName;
      modalCategory.textContent = `${{asset.categoryZh}} (${{asset.category}})`;
      modalSize.textContent = `${{asset.bytesFormatted}} (${{asset.ratio}}× 压缩)`;
      modalBlenderSize.textContent = `${{asset.blenderBytesFormatted}} (USD/Blender)`;
      modalTriangles.textContent = `${{asset.triangles.toLocaleString()}} 面 (原 ${{asset.blenderTriangles.toLocaleString()}})`;
      modalDrawcalls.textContent = `${{asset.drawCalls}} 次 (原 ${{asset.blenderDrawCalls}})`;
      modalJoints.textContent = asset.joints > 0 ? `${{asset.joints}} 个可动关节` : '静态无关节';
      modalTexture.textContent = `${{asset.texEdge}} px (WebP)`;

      updateModalCode(asset, 'three');

      modalCopyCode.onclick = () => {{
        navigator.clipboard.writeText(modalCodeText.textContent);
        modalCopyCode.textContent = '已复制!';
        setTimeout(() => {{ modalCopyCode.textContent = '复制代码'; }}, 1500);
      }};

      modal.classList.add('open');
    }}

    codeTabBtns.forEach(btn => {{
      btn.onclick = () => updateModalCode(currentModalAsset, btn.dataset.tab);
    }});

    modalClose.onclick = () => modal.classList.remove('open');
    modal.onclick = (e) => {{ if (e.target === modal) modal.classList.remove('open'); }};

    // 导出 CSV
    function exportToCsv() {{
      if (filteredAssets.length === 0) {{
        alert('当前无可导出的模型数据');
        return;
      }}
      
      const headers = ['中文名称', '资产唯一ID', '领域', '细分类', 'GLB体积(KB)', '面数', '物理关节数', '贴图边长(px)', 'GLB下载地址', '在线预览地址'];
      const rows = filteredAssets.map(a => [
        `"${{a.nameZh.replace(/"/g, '""')}}"`,
        `"${{a.name}}"`,
        `"${{a.domainName}}"`,
        `"${{a.categoryZh}}"`,
        Math.round(a.bytes / 1024),
        a.triangles,
        a.joints,
        a.texEdge,
        `"${{a.glbUrl}}"`,
        `"${{a.viewerUrl}}"`
      ]);

      const csvContent = "\\uFEFF" + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `SimReady_模型清单_${{filteredAssets.length}}个.csv`;
      link.click();
      URL.revokeObjectURL(url);
    }}

    // 事件绑定
    searchInput.oninput = (e) => {{
      searchQuery = e.target.value;
      applyFilters();
    }};

    categorySelect.onchange = (e) => {{
      currentCategory = e.target.value;
      applyFilters();
    }};

    sortSelect.onchange = (e) => {{
      currentSort = e.target.value;
      applyFilters();
    }};

    toggleJointsBtn.onclick = () => {{
      filterJointsOnly = !filterJointsOnly;
      toggleJointsBtn.classList.toggle('active', filterJointsOnly);
      applyFilters();
    }};

    exportCsvBtn.onclick = exportToCsv;

    loadMoreBtn.onclick = () => renderMore();

    viewGridBtn.onclick = () => {{
      if (currentView === 'grid') return;
      currentView = 'grid';
      viewGridBtn.classList.add('active');
      viewTableBtn.classList.remove('active');
      gridView.style.display = 'grid';
      tableView.style.display = 'none';
      displayedCount = 0;
      gridView.innerHTML = '';
      renderMore();
    }};

    viewTableBtn.onclick = () => {{
      if (currentView === 'table') return;
      currentView = 'table';
      viewTableBtn.classList.add('active');
      viewGridBtn.classList.remove('active');
      gridView.style.display = 'none';
      tableView.style.display = 'block';
      displayedCount = 0;
      tableBody.innerHTML = '';
      renderMore();
    }};

    window.onscroll = () => {{
      backToTopBtn.classList.toggle('show', window.scrollY > 300);
    }};
    backToTopBtn.onclick = () => window.scrollTo({{ top: 0, behavior: 'smooth' }});

    window.onkeydown = (e) => {{
      if (e.key === 'Escape') modal.classList.remove('open');
    }};

    // 启动系统
    initTheme();
    initDomainNav();
    updateCategoryOptions();
    applyFilters();

    console.log("SimReady 左右布局工程目录已就绪，已索引 " + ASSETS.length + " 个模型。");
  </script>
</body>
</html>
"""

    output_path = "SimReady_3D模型汉化选型目录.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"成功生成汉化目录 HTML 文件: {output_path}")
    print(f"文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == '__main__':
    build_catalog()
