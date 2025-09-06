class InsomniaKnowledgeBase:
    """失眠专病知识库"""
    
    # 失眠证型分类及症状特征（基于医师临床经验）
    SYNDROME_PATTERNS = {
        # 虚证类型
        "骨髓空虚": {
            "category": "虚证",
            "primary_symptoms": ["严重失眠", "记忆力下降", "腰膝酸软", "头晕耳鸣"],
            "tongue": "淡红舌苔薄白",
            "pulse": "沉细脉",
            "pathogenesis": "先天不足,后天失养,骨髓空虚"
        },
        "脑髓空虚": {
            "category": "虚证", 
            "primary_symptoms": ["健忘", "精神恍惚", "头部空痛", "思维迟缓"],
            "tongue": "淡胖舌",
            "pulse": "弱脉",
            "pathogenesis": "肾精不足,髓海不充"
        },
        "肝血不足": {
            "category": "虚证",
            "primary_symptoms": ["多梦", "易惊醒", "面色萎黄", "月经量少"],
            "tongue": "淡红舌",
            "pulse": "细脉",
            "pathogenesis": "血虚不能养肝,肝不藏魂"
        },
        "肝阴不足": {
            "category": "虚证",
            "primary_symptoms": ["烦躁不眠", "口干", "眼干", "头晕目眩"],
            "tongue": "红舌少苔",
            "pulse": "弦细脉",
            "pathogenesis": "阴液亏虚,肝阳偏亢"
        },
        "肾阴虚": {
            "category": "虚证",
            "primary_symptoms": ["五心烦热", "盗汗", "腰膝酸软", "耳鸣"],
            "tongue": "红舌少津",
            "pulse": "细数脉", 
            "pathogenesis": "肾阴亏虚,虚火扰神"
        },
        "肾阳虚": {
            "category": "虚证",
            "primary_symptoms": ["畏寒肢冷", "夜尿频多", "精神萎靡", "腰酸"],
            "tongue": "淡胖舌苔白",
            "pulse": "沉迟脉",
            "pathogenesis": "肾阳不足,命门火衰"
        },
        
        # 瘀证类型
        "肝气郁滞": {
            "category": "瘀证",
            "primary_symptoms": ["入睡困难", "易怒", "胸胁胀痛", "善太息"],
            "tongue": "暗红舌或有瘀点",
            "pulse": "弦脉",
            "pathogenesis": "情志不遂,肝气郁结,气滞血瘀"
        },
        "肾内血瘀": {
            "category": "瘀证", 
            "primary_symptoms": ["腰痛固定", "夜间加重", "尿色深", "舌质紫暗"],
            "tongue": "紫暗舌有瘀斑",
            "pulse": "沉涩脉",
            "pathogenesis": "久病入络,血瘀肾络"
        },
        
        # 实证类型  
        "精气衰竭": {
            "category": "实证",
            "primary_symptoms": ["极度疲劳", "精神萎靡", "反应迟钝", "体力严重下降"],
            "tongue": "淡暗舌苔厚腻",
            "pulse": "沉弱脉",
            "pathogenesis": "久病重症,精气大伤"
        }
    }
    
    # 经典方剂库
    CLASSICAL_FORMULAS = {
        "甘麦大枣汤": {
            "ingredients": {
                "甘草": "9g",
                "小麦": "30g", 
                "大枣": "10枚"
            },
            "indications": ["心神不宁", "情志异常"],
            "modifications": {
                "心烦重": "+黄连3g",
                "多梦": "+龙骨15g, 牡蛎15g"
            }
        },
        "安神定志丸": {
            "ingredients": {
                "人参": "6g",
                "茯苓": "9g",
                "远志": "6g",
                "石菖蒲": "6g"
            },
            "indications": ["心神不安", "健忘"],
            "modifications": {
                "心悸重": "+酸枣仁15g",
                "多梦": "+合欢皮12g"
            }
        },
        "黄连阿胶汤": {
            "ingredients": {
                "黄连": "12g",
                "黄芩": "6g",
                "白芍": "6g",
                "阿胶": "9g",
                "鸡子黄": "2枚"
            },
            "indications": ["心火亢盛", "阴液不足"],
            "modifications": {
                "便秘": "+大黄6g",
                "口苦": "+栀子9g"
            }
        }
    }
    
    # 外治法库
    EXTERNAL_TREATMENTS = {
        "耳穴压豆": {
            "acupoints": ["神门", "心", "肾", "皮质下", "交感"],
            "technique": "王不留行籽贴压",
            "frequency": "每日按压3-5次,每次30秒",
            "duration": "留置3-5天更换",
            "effects": ["宁心安神", "调节植物神经"]
        },
        "足浴安神": {
            "formula": {
                "酸枣仁": "30g",
                "夜交藤": "30g", 
                "合欢花": "15g",
                "薰衣草": "10g"
            },
            "method": "煎煮取汁,温度40-42℃",
            "duration": "浸泡20-30分钟",
            "timing": "睡前1小时"
        },
        "穴位按摩": {
            "acupoints": ["百会", "印堂", "神门", "三阴交", "涌泉"],
            "technique": "指腹按揉,力度适中",
            "frequency": "每穴按压1-2分钟",
            "timing": "睡前30分钟进行"
        }
    }
    
    # 食疗方库
    DIET_THERAPY = {
        "百合莲子粥": {
            "ingredients": ["百合30g", "莲子30g", "大米100g"],
            "preparation": "先煮莲子至软,再加百合和大米煮粥",
            "effects": "养心安神,润肺止咳",
            "timing": "晚餐或睡前服用",
            "contraindications": ["脾胃虚寒者慎用"]
        },
        "酸枣仁粥": {
            "ingredients": ["酸枣仁15g", "粳米100g"],
            "preparation": "酸枣仁研末,与粳米同煮粥",
            "effects": "养心安神,敛汗生津", 
            "timing": "早晚各一次",
            "contraindications": ["实热证者不宜"]
        },
        "龙眼肉茶": {
            "ingredients": ["龙眼肉10g", "酸枣仁10g", "芡实10g"],
            "preparation": "开水冲泡,焖10分钟",
            "effects": "补心脾,益气血",
            "timing": "下午或睡前饮用",
            "contraindications": ["痰湿重者少用"]
        }
    }
    
    @classmethod
    def get_syndrome_by_symptoms(cls, symptoms):
        """根据症状判断证型"""
        # 这里可以添加你的诊断逻辑
        pass
    
    @classmethod
    def get_treatment_plan(cls, syndrome_type):
        """根据证型获取治疗方案"""
        # 这里可以添加你的治疗方案逻辑
        pass