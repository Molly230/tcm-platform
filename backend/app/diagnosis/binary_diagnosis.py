from typing import Dict, List, Tuple
from app.models.insomnia_models import DiagnosticScores, FinalSyndromeType, Symptoms

class BinaryDiagnosisEngine:
    """二元诊断推理引擎"""
    
    # 症状权重配置 - 需要医师填入具体权重
    SYMPTOM_WEIGHTS = {
        # 骨髓空虚相关症状
        "骨髓空虚": {
            "严重失眠": 3.0,
            "记忆力下降": 2.5,
            "腰膝酸软": 2.0,
            "头晕耳鸣": 1.5,
            "精神萎靡": 2.0
        },
        # 脑髓空虚相关症状  
        "脑髓空虚": {
            "健忘": 3.0,
            "精神恍惚": 2.5,
            "头部空痛": 2.0,
            "思维迟缓": 2.0,
            "反应迟钝": 1.5
        },
        # 肝血不足相关症状
        "肝血不足": {
            "多梦": 3.0,
            "易惊醒": 2.5,
            "面色萎黄": 2.0,
            "月经量少": 2.0,
            "视物模糊": 1.5
        },
        # 肝阴不足相关症状
        "肝阴不足": {
            "烦躁不眠": 3.0,
            "口干": 2.0,
            "眼干": 2.0,
            "头晕目眩": 2.5,
            "五心烦热": 1.5
        },
        # 肾阴虚相关症状
        "肾阴虚": {
            "五心烦热": 3.0,
            "盗汗": 2.5,
            "腰膝酸软": 2.0,
            "耳鸣": 2.0,
            "口干咽燥": 1.5
        },
        # 肾阳虚相关症状
        "肾阳虚": {
            "畏寒肢冷": 3.0,
            "夜尿频多": 2.5,
            "精神萎靡": 2.0,
            "腰酸": 2.0,
            "性功能减退": 1.5
        },
        # 肝气郁滞相关症状
        "肝气郁滞": {
            "入睡困难": 3.0,
            "易怒": 2.5,
            "胸胁胀痛": 2.0,
            "善太息": 2.0,
            "情绪低落": 1.5
        },
        # 肾内血瘀相关症状
        "肾内血瘀": {
            "腰痛固定": 3.0,
            "夜间加重": 2.5,
            "尿色深": 2.0,
            "舌质紫暗": 2.0,
            "小便不利": 1.5
        },
        # 精气衰竭相关症状
        "精气衰竭": {
            "极度疲劳": 3.0,
            "精神萎靡": 2.5,
            "反应迟钝": 2.0,
            "体力严重下降": 2.0,
            "免疫力低下": 1.5
        }
    }
    
    # 舌脉权重配置
    TONGUE_PULSE_WEIGHTS = {
        "骨髓空虚": {
            "tongue": {"淡红舌苔薄白": 2.0},
            "pulse": {"沉细脉": 2.0}
        },
        "脑髓空虚": {
            "tongue": {"淡胖舌": 2.0},
            "pulse": {"弱脉": 2.0}
        },
        "肝血不足": {
            "tongue": {"淡红舌": 2.0},
            "pulse": {"细脉": 2.0}
        },
        "肝阴不足": {
            "tongue": {"红舌少苔": 2.0},
            "pulse": {"弦细脉": 2.0}
        },
        "肾阴虚": {
            "tongue": {"红舌少津": 2.0},
            "pulse": {"细数脉": 2.0}
        },
        "肾阳虚": {
            "tongue": {"淡胖舌苔白": 2.0},
            "pulse": {"沉迟脉": 2.0}
        },
        "肝气郁滞": {
            "tongue": {"暗红舌或有瘀点": 2.0},
            "pulse": {"弦脉": 2.0}
        },
        "肾内血瘀": {
            "tongue": {"紫暗舌有瘀斑": 2.0},
            "pulse": {"沉涩脉": 2.0}
        },
        "精气衰竭": {
            "tongue": {"淡暗舌苔厚腻": 2.0},
            "pulse": {"沉弱脉": 2.0}
        }
    }
    
    @classmethod
    def calculate_scores(cls, symptoms: Symptoms) -> DiagnosticScores:
        """计算各证型得分"""
        scores = DiagnosticScores()
        
        # 计算症状得分
        all_symptoms = symptoms.primary_symptoms + symptoms.secondary_symptoms
        
        # 骨髓空虚得分
        scores.bone_marrow_score = cls._calculate_dimension_score(
            "骨髓空虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 脑髓空虚得分
        scores.brain_marrow_score = cls._calculate_dimension_score(
            "脑髓空虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肝血不足得分
        scores.liver_blood_score = cls._calculate_dimension_score(
            "肝血不足", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肝阴不足得分
        scores.liver_yin_score = cls._calculate_dimension_score(
            "肝阴不足", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肾阴虚得分
        scores.kidney_yin_score = cls._calculate_dimension_score(
            "肾阴虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肾阳虚得分
        scores.kidney_yang_score = cls._calculate_dimension_score(
            "肾阳虚", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肝气郁滞得分
        scores.liver_qi_stagnation_score = cls._calculate_dimension_score(
            "肝气郁滞", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 肾内血瘀得分
        scores.kidney_blood_stasis_score = cls._calculate_dimension_score(
            "肾内血瘀", all_symptoms, symptoms.tongue_appearance, symptoms.pulse_condition
        )
        
        # 精气衰竭得分
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
    def determine_final_syndrome(cls, scores: DiagnosticScores) -> FinalSyndromeType:
        """
        根据得分确定最终证型
        这里需要医师提供具体的判定规则
        """
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
        
        # 临时逻辑：取最高分对应的证型
        # TODO: 医师需要提供更复杂的判定规则
        max_dimension = max(score_dict.items(), key=lambda x: x[1])
        
        # 这里需要医师提供维度组合到最终证型的映射规则
        # 暂时返回证型1
        return FinalSyndromeType.SYNDROME_1