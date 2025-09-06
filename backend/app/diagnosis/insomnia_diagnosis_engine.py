from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class InsomniaLevel(str, Enum):
    """失眠等级"""
    PRIMARY = "初级失眠"    # 75-90分
    MIDDLE = "中级失眠"     # 60-74分  
    ADVANCED = "高级失眠"   # <60分

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
    """失眠诊断引擎 - 18题问卷系统"""
    
    # 基础评分配置（1-9题）
    BASE_SCORING = {
        1: {  # 睡眠状况
            "A": 20,  # 好
            "B": 10,  # 一般
            "C": 0    # 较差
        },
        2: {  # 入睡时间
            "A": 12,  # 5分钟以内
            "B": 12,  # 6-15分钟
            "C": 9,   # 16-30分钟
            "D": 6,   # 31-60分钟
            "E": 3,   # 60分钟以上
            "F": 0    # 极长时间
        },
        3: {  # 睡眠时长
            "A": 12,  # 8小时及以上
            "B": 12,  # 7-8小时
            "C": 9,   # 6-7小时
            "D": 6,   # 5-6小时
            "E": 3,   # 5小时以下
            "F": 0    # 极少睡眠
        },
        4: {  # 醒来次数
            "A": 9,   # 几乎不醒来
            "B": 9,   # 1次
            "C": 6,   # 2-3次
            "D": 3,   # 4次及以上
            "E": 0    # 频繁醒来
        },
        5: {  # 再次入睡时间
            "A": 12,  # 5分钟以内
            "B": 12,  # 6-15分钟
            "C": 9,   # 16-30分钟
            "D": 6,   # 31-60分钟
            "E": 3,   # 60分钟以上
            "F": 0    # 极长时间
        },
        6: {  # 白天嗜睡
            "A": 9,   # 几乎没有
            "B": 6,   # 每周1-2次
            "C": 3,   # 每周3-5次
            "D": 0    # 每天都有
        },
        7: {  # 睡眠困扰（多选，选1个减3分，基础12分）
            "base": 12,
            "penalty_per_item": 3,
            "A": 9,   # 反复清醒
            "B": 4,   # 整夜做梦
            "C": 2,   # 晨起疲倦
            "D": 0    # 难以入眠
        },
        8: {  # 安眠药使用（多选，选1个减5分，基础20分）
            "base": 20,
            "penalty_per_item": 5,
            "medications": {
                "A": 20,  # 苯二氮䓬类
                "B": 15,  # 非苯二氮䓬类
                "C": 10,  # 褪黑素受体激动剂
                "D": 5,   # 食欲素受体拮抗剂
                "E": 0    # 抗抑郁药物
            }
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
    def analyze_questionnaire(cls, answers: Dict) -> DiagnosisResult:
        """分析18题问卷，返回完整诊断结果"""
        
        # 1. 计算基础分数（1-8题）
        base_score = cls._calculate_base_score(answers)
        
        # 2. 确定失眠等级
        level = cls._determine_insomnia_level(base_score)
        
        # 3. 计算证型分数（9-18题）
        syndrome_scores = cls._calculate_syndrome_scores(answers)
        
        # 4. 确定证型组合
        syndrome = cls._determine_syndrome_type(syndrome_scores)
        
        # 5. 生成治疗方案
        treatment_plan = cls._generate_treatment_plan(base_score, syndrome)
        
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
        """计算基础睡眠评分（1-9题）"""
        total_score = 0
        
        # 处理1-6题（单选题）
        for q_id in range(1, 7):
            if str(q_id) in answers and answers[str(q_id)]:
                answer = answers[str(q_id)][0] if isinstance(answers[str(q_id)], list) else answers[str(q_id)]
                score = cls.BASE_SCORING[q_id].get(answer, 0)
                total_score += score
        
        # 处理第7题（睡眠困扰，多选）
        if "7" in answers and answers["7"]:
            base_7 = cls.BASE_SCORING[7]["base"]
            penalty = cls.BASE_SCORING[7]["penalty_per_item"]
            selected_count = len(answers["7"]) if isinstance(answers["7"], list) else 1
            score_7 = base_7 - (penalty * selected_count)
            total_score += max(score_7, 0)  # 确保不为负
        
        # 处理第8题（安眠药，多选）
        if "8" in answers and answers["8"]:
            base_8 = cls.BASE_SCORING[8]["base"]
            penalty = cls.BASE_SCORING[8]["penalty_per_item"]
            selected_count = len(answers["8"]) if isinstance(answers["8"], list) else 1
            score_8 = base_8 - (penalty * selected_count)
            total_score += max(score_8, 0)  # 确保不为负
        
        # 处理第9题（服药时长）
        if "9" in answers and answers["9"]:
            duration_answer = answers["9"][0] if isinstance(answers["9"], list) else answers["9"]
            duration_score = cls.BASE_SCORING[9].get(duration_answer, 0)
            total_score += duration_score
        
        return total_score
    
    @classmethod
    def _determine_insomnia_level(cls, base_score: int) -> InsomniaLevel:
        """根据基础分数确定失眠等级"""
        if base_score >= 75:
            return InsomniaLevel.PRIMARY
        elif base_score >= 60:
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
    def _generate_treatment_plan(cls, base_score: int, syndrome: SyndromeType) -> Dict:
        """根据分数和证型生成治疗方案"""
        
        # 基础方案
        base_plan = cls.TREATMENT_PLANS[syndrome].copy()
        
        # 根据分数等级调整方案
        if base_score >= 90:
            # 103分以上，无需治疗
            if base_score >= 103:
                return {"level": "无需治疗", "recommendation": "保持现状"}
            else:
                # 90分，优等 - 茶包1
                base_plan["products"] = ["茶包1"]
                base_plan["level"] = "优等"
                
        elif base_score >= 75:
            # 75-90分，良等 - 茶包3 + 奶粉
            base_plan["products"].append("茶包3")
            base_plan["level"] = "良等"
            
        elif base_score >= 60:
            # 60-74分，中等 - 奶粉 + 坚果/鱼油
            base_plan["level"] = "中等"
            
        else:
            # <60分，差等 - 定制流程 + 丸剂 + 奶粉
            base_plan["products"].append("丸剂")
            base_plan["level"] = "差等"
            base_plan["special"] = "定制流程"
        
        return base_plan
    
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