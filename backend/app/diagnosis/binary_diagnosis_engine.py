from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class FinalSyndromeType(str, Enum):
    """最终证型枚举"""
    SYNDROME_1 = "骨髓空虚型失眠"
    SYNDROME_2 = "脑髓空虚型失眠" 
    SYNDROME_3 = "肝血不足型失眠"
    SYNDROME_4 = "肝阴不足型失眠"
    SYNDROME_5 = "肾阴虚型失眠"
    SYNDROME_6 = "肾阳虚型失眠"
    SYNDROME_7 = "肝气郁滞型失眠"
    SYNDROME_8 = "肾内血瘀型失眠"
    SYNDROME_9 = "精气衰竭型失眠"

@dataclass
class DiagnosticScores:
    """诊断得分数据类"""
    bone_marrow_score: float = 0.0
    brain_marrow_score: float = 0.0
    liver_blood_score: float = 0.0
    liver_yin_score: float = 0.0
    kidney_yin_score: float = 0.0
    kidney_yang_score: float = 0.0
    liver_qi_stagnation_score: float = 0.0
    kidney_blood_stasis_score: float = 0.0
    essence_deficiency_score: float = 0.0

@dataclass
class Symptoms:
    """症状数据类"""
    primary_symptoms: List[str] = None
    secondary_symptoms: List[str] = None
    tongue_appearance: str = ""
    pulse_condition: str = ""
    
    def __post_init__(self):
        if self.primary_symptoms is None:
            self.primary_symptoms = []
        if self.secondary_symptoms is None:
            self.secondary_symptoms = []

@dataclass
class BinaryDiagnosisResult:
    """诊断结果数据类"""
    final_syndrome: str
    confidence_score: float
    detailed_scores: DiagnosticScores
    recommendations: List[str]
    description: str

class BinaryDiagnosisEngine:
    """二元诊断推理引擎 - 从588项目完整迁移的严密逻辑"""
    
    # 症状权重配置 - 九个诊断维度的精确权重系统
    SYMPTOM_WEIGHTS = {
        # 骨髓空虚相关症状
        "骨髓空虚": {
            "严重失眠": 3.0,
            "记忆力下降": 2.5,
            "腰膝酸软": 2.0,
            "头晕耳鸣": 1.5,
            "精神萎靡": 2.0,
            "骨关节疼痛": 1.8,
            "牙齿松动": 1.2,
            "头发早白": 1.0
        },
        # 脑髓空虚相关症状  
        "脑髓空虚": {
            "健忘": 3.0,
            "精神恍惚": 2.5,
            "头部空痛": 2.0,
            "思维迟缓": 2.0,
            "反应迟钝": 1.5,
            "注意力难集中": 1.8,
            "学习能力下降": 1.6,
            "语言表达困难": 1.4
        },
        # 肝血不足相关症状
        "肝血不足": {
            "多梦": 3.0,
            "易惊醒": 2.5,
            "面色萎黄": 2.0,
            "月经量少": 2.0,
            "视物模糊": 1.5,
            "爪甲苍白": 1.3,
            "肌肉抽搐": 1.6,
            "眼睛干涩": 1.4
        },
        # 肝阴不足相关症状
        "肝阴不足": {
            "烦躁不眠": 3.0,
            "口干": 2.0,
            "眼干": 2.0,
            "头晕目眩": 2.5,
            "五心烦热": 1.5,
            "咽干": 1.3,
            "心烦易怒": 1.8,
            "潮热盗汗": 1.6
        },
        # 肾阴虚相关症状
        "肾阴虚": {
            "五心烦热": 3.0,
            "盗汗": 2.5,
            "腰膝酸软": 2.0,
            "耳鸣": 2.0,
            "口干咽燥": 1.5,
            "遗精": 1.8,
            "月经不调": 1.6,
            "骨蒸潮热": 1.9
        },
        # 肾阳虚相关症状
        "肾阳虚": {
            "畏寒肢冷": 3.0,
            "夜尿频多": 2.5,
            "精神萎靡": 2.0,
            "腰酸": 2.0,
            "性功能减退": 1.5,
            "浮肿": 1.8,
            "大便溏薄": 1.4,
            "面色苍白": 1.3
        },
        # 肝气郁滞相关症状
        "肝气郁滞": {
            "入睡困难": 3.0,
            "易怒": 2.5,
            "胸胁胀痛": 2.0,
            "善太息": 2.0,
            "情绪低落": 1.5,
            "乳房胀痛": 1.6,
            "腹胀": 1.4,
            "咽部异物感": 1.3
        },
        # 肾内血瘀相关症状
        "肾内血瘀": {
            "腰痛固定": 3.0,
            "夜间加重": 2.5,
            "尿色深": 2.0,
            "舌质紫暗": 2.0,
            "小便不利": 1.5,
            "刺痛": 1.8,
            "血尿": 2.2,
            "包块": 1.9
        },
        # 精气衰竭相关症状
        "精气衰竭": {
            "极度疲劳": 3.0,
            "精神萎靡": 2.5,
            "反应迟钝": 2.0,
            "体力严重下降": 2.0,
            "免疫力低下": 1.5,
            "呼吸短促": 1.7,
            "心悸": 1.6,
            "食欲不振": 1.4
        }
    }
    
    # 舌脉权重配置
    TONGUE_PULSE_WEIGHTS = {
        "骨髓空虚": {
            "tongue": {
                "淡红舌苔薄白": 2.0,
                "淡舌": 1.8,
                "舌体瘦薄": 1.5
            },
            "pulse": {
                "沉细脉": 2.0,
                "细脉": 1.8,
                "弱脉": 1.6
            }
        },
        "脑髓空虚": {
            "tongue": {
                "淡胖舌": 2.0,
                "舌体胖大": 1.8,
                "齿痕舌": 1.6
            },
            "pulse": {
                "弱脉": 2.0,
                "沉弱脉": 1.9,
                "细弱脉": 1.7
            }
        },
        "肝血不足": {
            "tongue": {
                "淡红舌": 2.0,
                "淡白舌": 1.8,
                "舌质淡": 1.6
            },
            "pulse": {
                "细脉": 2.0,
                "弦细脉": 1.8,
                "沉细脉": 1.6
            }
        },
        "肝阴不足": {
            "tongue": {
                "红舌少苔": 2.0,
                "舌红": 1.8,
                "少苔": 1.5
            },
            "pulse": {
                "弦细脉": 2.0,
                "细数脉": 1.8,
                "弦脉": 1.6
            }
        },
        "肾阴虚": {
            "tongue": {
                "红舌少津": 2.0,
                "舌红": 1.8,
                "少津": 1.6
            },
            "pulse": {
                "细数脉": 2.0,
                "数脉": 1.8,
                "沉细数脉": 1.9
            }
        },
        "肾阳虚": {
            "tongue": {
                "淡胖舌苔白": 2.0,
                "淡胖舌": 1.8,
                "苔白": 1.5
            },
            "pulse": {
                "沉迟脉": 2.0,
                "迟脉": 1.8,
                "沉弱脉": 1.7
            }
        },
        "肝气郁滞": {
            "tongue": {
                "暗红舌或有瘀点": 2.0,
                "舌边红": 1.8,
                "苔薄白": 1.4
            },
            "pulse": {
                "弦脉": 2.0,
                "弦滑脉": 1.8,
                "弦数脉": 1.6
            }
        },
        "肾内血瘀": {
            "tongue": {
                "紫暗舌有瘀斑": 2.0,
                "舌质紫暗": 1.9,
                "瘀斑": 1.7
            },
            "pulse": {
                "沉涩脉": 2.0,
                "涩脉": 1.8,
                "沉弦脉": 1.6
            }
        },
        "精气衰竭": {
            "tongue": {
                "淡暗舌苔厚腻": 2.0,
                "舌淡": 1.7,
                "苔厚腻": 1.8
            },
            "pulse": {
                "沉弱脉": 2.0,
                "微脉": 1.9,
                "弱脉": 1.7
            }
        }
    }
    
    # 证型映射表 - 从维度得分到最终诊断
    SYNDROME_MAPPING = {
        "骨髓空虚": FinalSyndromeType.SYNDROME_1,
        "脑髓空虚": FinalSyndromeType.SYNDROME_2,
        "肝血不足": FinalSyndromeType.SYNDROME_3,
        "肝阴不足": FinalSyndromeType.SYNDROME_4,
        "肾阴虚": FinalSyndromeType.SYNDROME_5,
        "肾阳虚": FinalSyndromeType.SYNDROME_6,
        "肝气郁滞": FinalSyndromeType.SYNDROME_7,
        "肾内血瘀": FinalSyndromeType.SYNDROME_8,
        "精气衰竭": FinalSyndromeType.SYNDROME_9
    }
    
    @classmethod
    def analyze_symptoms(cls, patient_answers: dict) -> BinaryDiagnosisResult:
        """
        主入口函数：分析患者回答并返回诊断结果
        这是从588项目完整迁移的严密逻辑
        """
        # 1. 解析患者回答为症状对象
        symptoms = cls._parse_patient_answers(patient_answers)
        
        # 2. 计算九个维度的得分
        scores = cls.calculate_scores(symptoms)
        
        # 3. 确定最终证型
        final_syndrome, confidence = cls.determine_final_syndrome(scores)
        
        # 4. 生成建议和描述
        recommendations = cls._generate_recommendations(final_syndrome)
        description = cls._generate_description(final_syndrome, confidence)
        
        return BinaryDiagnosisResult(
            final_syndrome=final_syndrome.value,
            confidence_score=confidence,
            detailed_scores=scores,
            recommendations=recommendations,
            description=description
        )
    
    @classmethod
    def _parse_patient_answers(cls, patient_answers: dict) -> Symptoms:
        """解析患者回答为症状对象"""
        primary_symptoms = []
        secondary_symptoms = []
        tongue_appearance = ""
        pulse_condition = ""
        
        # 解析问卷回答
        for answer_data in patient_answers.get('answers', []):
            question_id = answer_data.get('question_id')
            answer = answer_data.get('answer')
            
            # 根据问题ID和答案映射到症状
            symptoms_mapping = cls._get_symptoms_mapping()
            if question_id in symptoms_mapping and answer in symptoms_mapping[question_id]:
                mapped_symptoms = symptoms_mapping[question_id][answer]
                if isinstance(mapped_symptoms, list):
                    primary_symptoms.extend(mapped_symptoms)
                else:
                    primary_symptoms.append(mapped_symptoms)
        
        return Symptoms(
            primary_symptoms=primary_symptoms,
            secondary_symptoms=secondary_symptoms,
            tongue_appearance=tongue_appearance,
            pulse_condition=pulse_condition
        )
    
    @classmethod
    def _get_symptoms_mapping(cls) -> dict:
        """获取问题到症状的映射表 - 19项专业评估问题"""
        return {
            1: {"A": "入睡困难", "B": "易惊醒", "C": "早醒", "D": "睡眠浅"},
            2: {"A": "严重失眠", "B": "中度失眠", "C": "轻度失眠"},
            3: {"A": "精神萎靡", "B": "极度疲劳", "C": "体力严重下降"},
            4: {"A": "记忆力下降", "B": "健忘", "C": "注意力难集中"},
            5: {"A": "情绪低落", "B": "易怒", "C": "烦躁不眠"},
            6: {"A": "头晕耳鸣", "B": "头部空痛", "C": "头晕目眩"},
            7: {"A": "腰膝酸软", "B": "腰酸", "C": "腰痛固定"},
            8: {"A": "五心烦热", "B": "盗汗", "C": "潮热盗汗"},
            9: {"A": "畏寒肢冷", "B": "夜尿频多", "C": "浮肿"},
            10: {"A": "胸胁胀痛", "B": "善太息", "C": "咽部异物感"},
            11: {"A": "口干", "B": "口干咽燥", "C": "眼干"},
            12: {"A": "多梦", "B": "视物模糊", "C": "面色萎黄"},
            13: {"A": "反应迟钝", "B": "思维迟缓", "C": "精神恍惚"},
            14: {"A": "心悸", "B": "呼吸短促", "C": "胸闷"},
            15: {"A": "食欲不振", "B": "腹胀", "C": "大便溏薄"},
            16: {"A": "尿色深", "B": "小便不利", "C": "血尿"},
            17: {"A": "免疫力低下", "B": "容易感冒", "C": "恢复缓慢"},
            18: {"A": "月经量少", "B": "月经不调", "C": "乳房胀痛"},
            19: {"A": "性功能减退", "B": "遗精", "C": "性欲减退"}
        }
    
    @classmethod
    def calculate_scores(cls, symptoms: Symptoms) -> DiagnosticScores:
        """计算各证型得分 - 九个维度的精确计算"""
        scores = DiagnosticScores()
        
        # 计算症状得分
        all_symptoms = symptoms.primary_symptoms + symptoms.secondary_symptoms
        
        # 九个维度的得分计算
        scores.bone_marrow_score = cls._calculate_dimension_score(
            "骨髓空虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.brain_marrow_score = cls._calculate_dimension_score(
            "脑髓空虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.liver_blood_score = cls._calculate_dimension_score(
            "肝血不足", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.liver_yin_score = cls._calculate_dimension_score(
            "肝阴不足", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.kidney_yin_score = cls._calculate_dimension_score(
            "肾阴虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.kidney_yang_score = cls._calculate_dimension_score(
            "肾阳虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.liver_qi_stagnation_score = cls._calculate_dimension_score(
            "肝气郁滞", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.kidney_blood_stasis_score = cls._calculate_dimension_score(
            "肾内血瘀", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        scores.essence_deficiency_score = cls._calculate_dimension_score(
            "精气衰竭", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        return scores
    
    @classmethod
    def _calculate_dimension_score(cls, dimension: str, symptoms: List[str], 
                                   tongue: str, pulse: str) -> float:
        """计算单个维度得分"""
        total_score = 0.0
        
        # 症状得分
        symptom_weights = cls.SYMPTOM_WEIGHTS.get(dimension, {})
        for symptom in symptoms:
            if symptom in symptom_weights:
                total_score += symptom_weights[symptom]
        
        # 舌象得分
        tongue_weights = cls.TONGUE_PULSE_WEIGHTS.get(dimension, {}).get("tongue", {})
        if tongue in tongue_weights:
            total_score += tongue_weights[tongue]
        
        # 脉象得分
        pulse_weights = cls.TONGUE_PULSE_WEIGHTS.get(dimension, {}).get("pulse", {})
        if pulse in pulse_weights:
            total_score += pulse_weights[pulse]
        
        return total_score
    
    @classmethod
    def determine_final_syndrome(cls, scores: DiagnosticScores) -> Tuple[FinalSyndromeType, float]:
        """根据得分确定最终证型和置信度"""
        # 获取所有得分
        score_dict = {
            "骨髓空虚": scores.bone_marrow_score,
            "脑髓空虚": scores.brain_marrow_score,
            "肝血不足": scores.liver_blood_score,
            "肝阴不足": scores.liver_yin_score,
            "肾阴虚": scores.kidney_yin_score,
            "肾阳虚": scores.kidney_yang_score,
            "肝气郁滞": scores.liver_qi_stagnation_score,
            "肾内血瘀": scores.kidney_blood_stasis_score,
            "精气衰竭": scores.essence_deficiency_score
        }
        
        # 找到最高分维度
        max_dimension = max(score_dict.items(), key=lambda x: x[1])
        max_score = max_dimension[1]
        
        # 计算置信度（基于最高分与其他分数的差距）
        sorted_scores = sorted(score_dict.values(), reverse=True)
        if len(sorted_scores) > 1 and sorted_scores[0] > 0:
            confidence = min(0.95, (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0] + 0.6)
        else:
            confidence = 0.6
        
        # 映射到最终证型
        final_syndrome = cls.SYNDROME_MAPPING[max_dimension[0]]
        
        return final_syndrome, confidence
    
    @classmethod
    def _generate_recommendations(cls, syndrome: FinalSyndromeType) -> List[str]:
        """生成针对性调理建议"""
        recommendations_map = {
            FinalSyndromeType.SYNDROME_1: [
                "补肾填髓，养血安神",
                "推荐食疗：黑芝麻、核桃、枸杞子",
                "适当运动：太极拳、八段锦",
                "保持规律作息，避免熬夜"
            ],
            FinalSyndromeType.SYNDROME_2: [
                "补肾填髓，健脑益智",
                "推荐食疗：核桃、鱼头汤、莲子",
                "脑部按摩：百会、四神聪穴位",
                "减少用脑过度，保证充足睡眠"
            ],
            FinalSyndromeType.SYNDROME_3: [
                "养血补肝，安神定志",
                "推荐食疗：红枣、阿胶、动物肝脏",
                "眼部保健：枸杞菊花茶",
                "情绪调节，避免过度思虑"
            ],
            FinalSyndromeType.SYNDROME_4: [
                "滋阴养肝，清热安神",
                "推荐食疗：百合、银耳、梨子",
                "避免辛辣燥热食物",
                "保持心情平和，练习冥想"
            ],
            FinalSyndromeType.SYNDROME_5: [
                "滋阴补肾，降火安神",
                "推荐食疗：山药、黑豆、海参",
                "避免房事过度，节制欲望",
                "多食滋阴润燥食物"
            ],
            FinalSyndromeType.SYNDROME_6: [
                "温阳补肾，暖宫安神",
                "推荐食疗：羊肉、肉桂、附子汤",
                "保暖防寒，特别是腰部",
                "适当运动，增强体质"
            ],
            FinalSyndromeType.SYNDROME_7: [
                "疏肝解郁，理气安神",
                "推荐食疗：玫瑰花茶、柑橘皮",
                "情绪调节：多与人交流",
                "避免情绪波动，学会释放压力"
            ],
            FinalSyndromeType.SYNDROME_8: [
                "活血化瘀，通络安神",
                "推荐食疗：山楂、红花茶、丹参",
                "适当活动，促进血液循环",
                "避免久坐，定期按摩腰部"
            ],
            FinalSyndromeType.SYNDROME_9: [
                "大补元气，回阳固脱",
                "推荐食疗：人参、鹿茸、燕窝",
                "严格卧床休息，避免劳累",
                "紧急情况建议及时就医"
            ]
        }
        
        return recommendations_map.get(syndrome, ["请咨询专业中医师进行详细诊断"])
    
    @classmethod
    def _generate_description(cls, syndrome: FinalSyndromeType, confidence: float) -> str:
        """生成诊断描述"""
        confidence_level = "高" if confidence > 0.8 else "中" if confidence > 0.6 else "低"
        
        descriptions = {
            FinalSyndromeType.SYNDROME_1: "骨髓空虚型失眠，主要表现为肾精不足，骨髓失养",
            FinalSyndromeType.SYNDROME_2: "脑髓空虚型失眠，主要表现为脑髓不足，神志不安",
            FinalSyndromeType.SYNDROME_3: "肝血不足型失眠，主要表现为肝血亏虚，心神失养",
            FinalSyndromeType.SYNDROME_4: "肝阴不足型失眠，主要表现为肝阴亏虚，虚火上炎",
            FinalSyndromeType.SYNDROME_5: "肾阴虚型失眠，主要表现为肾阴不足，虚火内扰",
            FinalSyndromeType.SYNDROME_6: "肾阳虚型失眠，主要表现为肾阳不足，阳虚内寒",
            FinalSyndromeType.SYNDROME_7: "肝气郁滞型失眠，主要表现为肝气不舒，气机郁滞",
            FinalSyndromeType.SYNDROME_8: "肾内血瘀型失眠，主要表现为血行不畅，瘀阻经络",
            FinalSyndromeType.SYNDROME_9: "精气衰竭型失眠，主要表现为精气大虚，元神散乱"
        }
        
        base_description = descriptions.get(syndrome, "未明确证型")
        return f"{base_description}。诊断置信度：{confidence_level}（{confidence:.1%}）"