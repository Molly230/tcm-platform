from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class InsomniaLevel(str, Enum):
    """失眠等级"""
    NO_TREATMENT = "无需治疗"  # ≥103分
    PRIMARY = "初级失眠"       # 60-102分
    MIDDLE = "中级失眠"        # 45-59分  
    ADVANCED = "高级失眠"      # ≤44分

class SyndromeType(str, Enum):
    """证型组合"""
    LIVER_KIDNEY_DEFICIENCY = "肝郁肾虚"    # 肝肠+骨髓
    LIVER_BRAIN_DEFICIENCY = "肝郁脑虚"     # 肝肠+脑髓
    QI_BLOOD_DEFICIENCY = "气血两虚"        # 血液+骨髓
    QI_BLOOD_STASIS = "气滞血瘀"           # 血液+脑髓
    ESSENCE_DEFICIENCY = "精髓空虚"         # 神内+骨髓
    NEURASTHENIA = "神经衰弱"              # 神内+脑髓

@dataclass
class SyndromeScores:
    """证型得分"""
    liver_intestine: int = 0  # 肝肠
    blood: int = 0           # 血液  
    neural: int = 0          # 神内
    bone_marrow: int = 0     # 骨髓
    brain_marrow: int = 0    # 脑髓

@dataclass
class DiagnosisResult:
    """完整诊断结果"""
    base_score: int                    # 基础分数
    level: InsomniaLevel              # 失眠等级
    syndrome: SyndromeType            # 证型组合
    syndrome_scores: SyndromeScores   # 各证型得分
    treatment_plan: Dict              # 治疗方案
    confidence: float                 # 置信度

class InsomniaDiagnosisEngine:
    """失眠诊断引擎 - 19题问卷系统"""
    
    # 基础评分配置（1-9题）
    BASE_SCORING = {
        1: {  # 睡眠状况
            "A": 20,  # 好
            "B": 10,  # 一般
            "C": 0    # 较差
        },
        2: {  # 入睡时间
            "A": 12,  # 5分钟以内
            "B": 9,   # 6-15分钟
            "C": 6,   # 16-30分钟
            "D": 3,   # 31-60分钟
            "E": 0    # 60分钟以上
        },
        3: {  # 睡眠时长
            "A": 12,  # 8小时及以上
            "B": 9,   # 7-8小时
            "C": 6,   # 6-7小时
            "D": 3,   # 5-6小时
            "E": 0    # 5小时以下
        },
        4: {  # 醒来次数
            "A": 9,   # 几乎不醒来
            "B": 6,   # 1次
            "C": 3,   # 2-3次
            "D": 0    # 4次及以上
        },
        5: {  # 再次入睡时间
            "A": 12,  # 5分钟以内
            "B": 9,   # 6-15分钟
            "C": 6,   # 16-30分钟
            "D": 3,   # 31-60分钟
            "E": 0    # 60分钟以上
        },
        6: {  # 白天嗜睡
            "A": 9,   # 几乎没有
            "B": 6,   # 每周1-2次
            "C": 3,   # 每周3-5次
            "D": 0    # 每天都有
        },
        7: {  # 睡眠困扰（多选，减分制）
            "A": -3,  # 反复清醒
            "B": -3,  # 整夜做梦
            "C": -3,  # 晨起疲倦
            "D": -3,  # 难以入眠
            "E": 0    # 无
        },
        8: {  # 安眠药使用（多选，减分制）
            "A": -5,  # 苯二氮䓬类
            "B": -5,  # 非苯二氮䓬类
            "C": -5,  # 褪黑素受体激动剂
            "D": -5,  # 食欲素受体拮抗剂
            "E": -5,  # 抗抑郁药物
            "F": 0    # 无
        },
        9: {  # 服药时长（第9题）
            "A": 6,   # 1个月以内
            "B": 4,   # 1-3个月
            "C": 2,   # 3个月以上
            "D": 0    # 长期使用
        }
    }
    
    # 证型计分配置（10-19题）
    SYNDROME_SCORING = {
        # 主证型（行）
        "liver_intestine": [10, 15],  # 肝肠：问题10 + 问题15
        "blood": [11, 16],           # 血液：问题11 + 问题16
        "neural": [12, 17],          # 神内：问题12 + 问题17
        
        # 次证型（列）  
        "bone_marrow": [13, 18],     # 骨髓：问题13 + 问题18
        "brain_marrow": [14, 19]     # 脑髓：问题14 + 问题19
    }
    
    # 证型矩阵
    SYNDROME_MATRIX = {
        ("liver_intestine", "bone_marrow"): SyndromeType.LIVER_KIDNEY_DEFICIENCY,
        ("liver_intestine", "brain_marrow"): SyndromeType.LIVER_BRAIN_DEFICIENCY,
        ("blood", "bone_marrow"): SyndromeType.QI_BLOOD_DEFICIENCY,
        ("blood", "brain_marrow"): SyndromeType.QI_BLOOD_STASIS,
        ("neural", "bone_marrow"): SyndromeType.ESSENCE_DEFICIENCY,
        ("neural", "brain_marrow"): SyndromeType.NEURASTHENIA
    }
    
    # 治疗方案配置
    TREATMENT_PLANS = {
        SyndromeType.LIVER_KIDNEY_DEFICIENCY: {
            "products": ["奶粉（养肝）", "坚果（补肾）"],
            "acupoints": ["肝俞", "肾俞", "太冲", "太溪"],
            "diet_therapy": ["枸杞菊花茶", "黑芝麻核桃粉"],
            "lifestyle": ["调节情绪", "适当运动", "规律作息"]
        },
        SyndromeType.LIVER_BRAIN_DEFICIENCY: {
            "products": ["奶粉（养肝）", "鱼油（健脑）"],
            "acupoints": ["肝俞", "百会", "太冲", "神门"],
            "diet_therapy": ["龙眼肉茶", "核桃仁粥"],
            "lifestyle": ["减少用脑", "情绪调节", "按摩头部"]
        },
        SyndromeType.QI_BLOOD_DEFICIENCY: {
            "products": ["奶粉（养血）", "坚果（补气）"],
            "acupoints": ["脾俞", "胃俞", "足三里", "血海"],
            "diet_therapy": ["红枣桂圆汤", "当归生姜羊肉汤"],
            "lifestyle": ["营养均衡", "适量运动", "避免劳累"]
        },
        SyndromeType.QI_BLOOD_STASIS: {
            "products": ["奶粉（活血）", "鱼油（通络）"],
            "acupoints": ["膈俞", "血海", "三阴交", "合谷"],
            "diet_therapy": ["山楂茶", "玫瑰花茶"],
            "lifestyle": ["活动身体", "情绪舒畅", "避免久坐"]
        },
        SyndromeType.ESSENCE_DEFICIENCY: {
            "products": ["奶粉（补精）", "坚果（固髓）"],
            "acupoints": ["肾俞", "命门", "关元", "涌泉"],
            "diet_therapy": ["黑豆汤", "海参粥"],
            "lifestyle": ["充足休息", "节制房事", "保暖防寒"]
        },
        SyndromeType.NEURASTHENIA: {
            "products": ["奶粉（安神）", "鱼油（营养神经）"],
            "acupoints": ["神门", "百会", "印堂", "安眠"],
            "diet_therapy": ["酸枣仁汤", "百合莲子汤"],
            "lifestyle": ["放松训练", "规律作息", "减少刺激"]
        }
    }
    
    @classmethod
    def _check_special_flows(cls, answers: Dict) -> Optional[DiagnosisResult]:
        """检查特殊流程：第1题选很好、第9题选3个月以上"""
        
        # 检查第1题：如果选择"很好"，直接退出
        if "1" in answers:
            answer_1 = answers["1"][0] if isinstance(answers["1"], list) else answers["1"]
            if answer_1 == "A":  # "好"选项
                return DiagnosisResult(
                    base_score=100,
                    level=InsomniaLevel.NO_TREATMENT,
                    syndrome=SyndromeType.LIVER_KIDNEY_DEFICIENCY,  # 占位
                    syndrome_scores=SyndromeScores(),
                    treatment_plan={
                        "level": "睡眠质量很好",
                        "recommendation": "恭喜您！",
                        "message": "您的睡眠质量很好，请继续保持良好的作息习惯。祝您身体健康！",
                        "products": [],
                        "therapy": [],
                        "special": "perfect_sleep"
                    },
                    confidence=1.0
                )
        
        # 检查第9题：如果选择"3个月以上"，建议定制流程
        if "9" in answers:
            answer_9 = answers["9"][0] if isinstance(answers["9"], list) else answers["9"]
            if answer_9 == "C":  # "3个月以上"选项
                return DiagnosisResult(
                    base_score=30,  # 低分表示严重
                    level=InsomniaLevel.ADVANCED,
                    syndrome=SyndromeType.LIVER_KIDNEY_DEFICIENCY,  # 占位
                    syndrome_scores=SyndromeScores(),
                    treatment_plan={
                        "level": "长期用药失眠",
                        "recommendation": "建议咨询专业医师",
                        "message": "您长期使用安眠药物，建议寻求高级咨询师的专业指导，制定个性化的减药和治疗方案。",
                        "products": ["专业咨询服务"],
                        "therapy": ["高级咨询师定制流程"],
                        "special": "long_term_medication"
                    },
                    confidence=1.0
                )
        
        return None
    
    @classmethod
    def analyze_questionnaire(cls, answers: Dict) -> DiagnosisResult:
        """分析19题问卷，返回完整诊断结果"""
        
        # 0. 特殊流程检查
        special_result = cls._check_special_flows(answers)
        if special_result:
            return special_result
        
        # 1. 计算基础分数（1-8题，第9题不参与评分）
        base_score = cls._calculate_base_score(answers)
        
        # 2. 确定失眠等级
        level = cls._determine_insomnia_level(base_score)
        
        # 3. 计算证型分数（10-19题）
        syndrome_scores = cls._calculate_syndrome_scores(answers)
        
        # 4. 确定证型组合
        syndrome = cls._determine_syndrome_type(syndrome_scores)
        
        # 5. 生成治疗方案
        treatment_plan = cls._generate_treatment_plan(base_score, syndrome, syndrome_scores)
        
        # 6. 计算置信度
        confidence = cls._calculate_confidence(base_score, syndrome_scores)
        
        return DiagnosisResult(
            base_score=base_score,
            level=level,
            syndrome=syndrome,
            syndrome_scores=syndrome_scores,
            treatment_plan=treatment_plan,
            confidence=confidence
        )
    
    @classmethod
    def _calculate_base_score(cls, answers: Dict) -> int:
        """计算基础睡眠评分（1-8题，第9题不参与评分）"""
        total_score = 0
        
        # 处理1-6题（单选题）
        for q_id in range(1, 7):
            if str(q_id) in answers and answers[str(q_id)]:
                answer = answers[str(q_id)][0] if isinstance(answers[str(q_id)], list) else answers[str(q_id)]
                score = cls.BASE_SCORING[q_id].get(answer, 0)
                total_score += score
        
        # 处理第7题（睡眠困扰，多选，累加减分）
        if "7" in answers and answers["7"]:
            selected_options = answers["7"] if isinstance(answers["7"], list) else [answers["7"]]
            for opt in selected_options:
                total_score += cls.BASE_SCORING[7].get(opt, 0)
        
        # 处理第8题（安眠药，多选，累加减分）
        if "8" in answers and answers["8"]:
            selected_options = answers["8"] if isinstance(answers["8"], list) else [answers["8"]]
            for opt in selected_options:
                total_score += cls.BASE_SCORING[8].get(opt, 0)
        
        # 第9题（服药时长）不参与基础评分计算，仅用于治疗方案参考
        
        return total_score
    
    @classmethod
    def _determine_insomnia_level(cls, base_score: int) -> InsomniaLevel:
        """根据基础分数确定失眠等级"""
        if base_score >= 103:
            return InsomniaLevel.NO_TREATMENT
        elif base_score >= 60:
            return InsomniaLevel.PRIMARY
        elif base_score >= 45:
            return InsomniaLevel.MIDDLE
        else:
            return InsomniaLevel.ADVANCED
    
    @classmethod
    def _calculate_syndrome_scores(cls, answers: Dict) -> SyndromeScores:
        """计算证型分数（10-19题）"""
        scores = SyndromeScores()
        
        # 肝肠分：问题10 + 问题15
        for q_id in cls.SYNDROME_SCORING["liver_intestine"]:
            if str(q_id) in answers and answers[str(q_id)]:
                if answers[str(q_id)] == "是" or (isinstance(answers[str(q_id)], list) and "是" in answers[str(q_id)]):
                    scores.liver_intestine += 1
                elif isinstance(answers[str(q_id)], list):
                    scores.liver_intestine += len(answers[str(q_id)])  # 多选题按选中项数计分
        
        # 血液分：问题11 + 问题16
        for q_id in cls.SYNDROME_SCORING["blood"]:
            if str(q_id) in answers and answers[str(q_id)]:
                if answers[str(q_id)] == "是" or (isinstance(answers[str(q_id)], list) and "是" in answers[str(q_id)]):
                    scores.blood += 1
                elif isinstance(answers[str(q_id)], list):
                    scores.blood += len(answers[str(q_id)])
        
        # 神内分：问题12 + 问题17
        for q_id in cls.SYNDROME_SCORING["neural"]:
            if str(q_id) in answers and answers[str(q_id)]:
                if answers[str(q_id)] == "是" or (isinstance(answers[str(q_id)], list) and "是" in answers[str(q_id)]):
                    scores.neural += 1
                elif isinstance(answers[str(q_id)], list):
                    scores.neural += len(answers[str(q_id)])
        
        # 骨髓分：问题13 + 问题18
        for q_id in cls.SYNDROME_SCORING["bone_marrow"]:
            if str(q_id) in answers and answers[str(q_id)]:
                if answers[str(q_id)] == "是" or (isinstance(answers[str(q_id)], list) and "是" in answers[str(q_id)]):
                    scores.bone_marrow += 1
                elif isinstance(answers[str(q_id)], list):
                    scores.bone_marrow += len(answers[str(q_id)])
        
        # 脑髓分：问题14 + 问题19
        for q_id in cls.SYNDROME_SCORING["brain_marrow"]:
            if str(q_id) in answers and answers[str(q_id)]:
                if answers[str(q_id)] == "是" or (isinstance(answers[str(q_id)], list) and "是" in answers[str(q_id)]):
                    scores.brain_marrow += 1
                elif isinstance(answers[str(q_id)], list):
                    scores.brain_marrow += len(answers[str(q_id)])
        
        return scores
    
    @classmethod
    def _determine_syndrome_type(cls, scores: SyndromeScores) -> SyndromeType:
        """根据证型分数确定证型组合（矩阵匹配）"""
        
        # 找出行最高分（主证型）
        row_scores = {
            "liver_intestine": scores.liver_intestine,
            "blood": scores.blood,
            "neural": scores.neural
        }
        max_row = max(row_scores.items(), key=lambda x: x[1])[0]
        
        # 找出列最高分（次证型）
        col_scores = {
            "bone_marrow": scores.bone_marrow,
            "brain_marrow": scores.brain_marrow
        }
        max_col = max(col_scores.items(), key=lambda x: x[1])[0]
        
        # 矩阵匹配
        syndrome_key = (max_row, max_col)
        return cls.SYNDROME_MATRIX.get(syndrome_key, SyndromeType.LIVER_KIDNEY_DEFICIENCY)
    
    @classmethod
    def _generate_treatment_plan(cls, base_score: int, syndrome: SyndromeType, syndrome_scores: SyndromeScores) -> Dict:
        """根据分数和证型生成治疗方案"""
        
        # 根据分数等级确定治疗方案
        if base_score >= 103:
            return {
                "level": "无需治疗",
                "recommendation": "保持现状",
                "products": [],
                "therapy": []
            }
        elif base_score == 74:
            return {
                "level": "初级失眠(74分)",
                "recommendation": "保持",
                "products": ["茶包1"],
                "therapy": []
            }
        elif base_score >= 60:
            # 初级失眠 60-73分，茶包3（根据肝血神最高分）+ 奶粉
            syndrome_tea = cls._get_syndrome_tea_for_primary(syndrome_scores)
            return {
                "level": "初级失眠(60-73分)",
                "recommendation": "茶包3 + 奶粉",
                "products": [syndrome_tea, "奶粉"],
                "therapy": []
            }
        elif base_score >= 45:
            # 中级失眠，奶粉 + 坚果/鱼油 + 证型穴位
            syndrome_products, additional_products = cls._get_syndrome_products_with_supplements(syndrome)
            acupoint_therapy = cls._get_syndrome_acupoints(syndrome)
            return {
                "level": "中级失眠(45-59分)", 
                "recommendation": "奶粉+营养补充+理疗",
                "products": syndrome_products + additional_products,
                "therapy": [acupoint_therapy]
            }
        else:
            # 高级失眠 ≤44分，定制流程
            return {
                "level": "高级失眠(≤44分)",
                "recommendation": "定制流程",
                "products": ["②丸剂", "奶粉"],
                "therapy": [],
                "special": "定制流程"
            }
    
    @classmethod
    def _get_syndrome_tea_for_primary(cls, syndrome_scores: SyndromeScores) -> str:
        """初级失眠(60-73分)根据肝血神最高分获取对应的茶包3"""
        # 食疗逻辑：看肝肠、血液、神内哪个最高分
        scores = {
            "肝肠": syndrome_scores.liver_intestine,
            "血液": syndrome_scores.blood,
            "神内": syndrome_scores.neural
        }
        
        max_syndrome = max(scores.items(), key=lambda x: x[1])[0]
        
        tea_map = {
            "肝肠": "茶包3(养肝)",
            "血液": "茶包3(养血)",
            "神内": "茶包3(养神)"
        }
        
        return tea_map.get(max_syndrome, "茶包3(养肝)")
        
    @classmethod
    def _get_syndrome_products_with_supplements(cls, syndrome: SyndromeType) -> Tuple[List[str], List[str]]:
        """中级失眠(45-59分)根据证型获取奶粉产品和营养补充品"""
        # 根据表格：奶粉 + 骨髓坚果 或 脑髓鱼油
        if syndrome in [SyndromeType.LIVER_KIDNEY_DEFICIENCY, SyndromeType.QI_BLOOD_DEFICIENCY, SyndromeType.ESSENCE_DEFICIENCY]:
            # 骨髓类证型：奶粉 + 坚果
            return (["奶粉"], ["坚果"])
        else:
            # 脑髓类证型：奶粉 + 鱼油
            return (["奶粉"], ["鱼油"])
    
    @classmethod
    def _get_syndrome_acupoints(cls, syndrome: SyndromeType) -> str:
        """根据6个证型获取对应的穴位组合"""
        acupoint_map = {
            SyndromeType.LIVER_KIDNEY_DEFICIENCY: "穴位敷贴（肝俞、肾俞、太冲、太溪）",
            SyndromeType.LIVER_BRAIN_DEFICIENCY: "穴位敷贴（肝俞、百会、神门、印堂）",
            SyndromeType.QI_BLOOD_DEFICIENCY: "穴位敷贴（脾俞、胃俞、足三里、血海）",
            SyndromeType.QI_BLOOD_STASIS: "穴位敷贴（心俞、神门、内关、三阴交）",
            SyndromeType.ESSENCE_DEFICIENCY: "穴位敷贴（肾俞、命门、关元、涌泉）",
            SyndromeType.NEURASTHENIA: "穴位敷贴（百会、神庭、安眠、神门）"
        }
        return acupoint_map.get(syndrome, "穴位敷贴（安眠、神门、百会、印堂）")
    
    @classmethod
    def _calculate_confidence(cls, base_score: int, syndrome_scores: SyndromeScores) -> float:
        """计算诊断置信度"""
        
        # 基础分数置信度
        score_confidence = min(base_score / 100.0, 1.0)
        
        # 证型分数置信度
        all_syndrome_scores = [
            syndrome_scores.liver_intestine,
            syndrome_scores.blood,
            syndrome_scores.neural,
            syndrome_scores.bone_marrow,
            syndrome_scores.brain_marrow
        ]
        max_syndrome_score = max(all_syndrome_scores) if all_syndrome_scores else 0
        syndrome_confidence = min(max_syndrome_score / 4.0, 1.0)  # 最高4分
        
        # 综合置信度
        confidence = (score_confidence + syndrome_confidence) / 2.0
        return round(confidence, 2)