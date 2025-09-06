"""
失眠诊断引擎 - 从588系统移植
"""
from typing import Dict, List, Tuple
from .base import DiagnosisBase, DiseaseType


class InsomniaDiagnosis(DiagnosisBase):
    """失眠诊断引擎"""
    
    def __init__(self):
        super().__init__(DiseaseType.INSOMNIA)
        
        # 症状权重配置
        self.SYMPTOM_WEIGHTS = {
            "骨髓空虚": {
                "严重失眠": 3.0,
                "记忆力下降": 2.5,
                "腰膝酸软": 2.0,
                "头晕耳鸣": 1.5,
                "精神萎靡": 2.0
            },
            "脑髓空虚": {
                "健忘": 3.0,
                "精神恍惚": 2.5,
                "头部空痛": 2.0,
                "思维迟缓": 2.0,
                "反应迟钝": 1.5
            },
            "肝血不足": {
                "多梦": 3.0,
                "易惊醒": 2.5,
                "面色萎黄": 2.0,
                "月经量少": 2.0,
                "视物模糊": 1.5
            },
            "肝阴不足": {
                "烦躁不眠": 3.0,
                "口干": 2.0,
                "眼干": 2.0,
                "头晕目眩": 2.5,
                "五心烦热": 1.5
            },
            "肾阴虚": {
                "五心烦热": 3.0,
                "盗汗": 2.5,
                "腰膝酸软": 2.0,
                "耳鸣": 2.0,
                "口干咽燥": 1.5
            },
            "肾阳虚": {
                "畏寒肢冷": 3.0,
                "夜尿频多": 2.5,
                "精神萎靡": 2.0,
                "腰酸": 2.0,
                "性功能减退": 1.5
            },
            "肝气郁滞": {
                "入睡困难": 3.0,
                "易怒": 2.5,
                "胸胁胀痛": 2.0,
                "善太息": 2.0,
                "情绪低落": 1.5
            },
            "肾内血瘀": {
                "腰痛固定": 3.0,
                "夜间加重": 2.5,
                "尿色深": 2.0,
                "舌质紫暗": 2.0,
                "小便不利": 1.5
            },
            "精气衰竭": {
                "极度疲劳": 3.0,
                "精神萎靡": 2.5,
                "反应迟钝": 2.0,
                "体力严重下降": 2.0,
                "免疫力低下": 1.5
            }
        }
        
        # 舌脉权重配置
        self.TONGUE_PULSE_WEIGHTS = {
            "骨髓空虚": {"tongue": {"淡红舌苔薄白": 2.0}, "pulse": {"沉细脉": 2.0}},
            "脑髓空虚": {"tongue": {"淡胖舌": 2.0}, "pulse": {"弱脉": 2.0}},
            "肝血不足": {"tongue": {"淡红舌": 2.0}, "pulse": {"细脉": 2.0}},
            "肝阴不足": {"tongue": {"红舌少苔": 2.0}, "pulse": {"弦细脉": 2.0}},
            "肾阴虚": {"tongue": {"红舌少津": 2.0}, "pulse": {"细数脉": 2.0}},
            "肾阳虚": {"tongue": {"淡胖舌苔白": 2.0}, "pulse": {"沉迟脉": 2.0}},
            "肝气郁滞": {"tongue": {"暗红舌或有瘀点": 2.0}, "pulse": {"弦脉": 2.0}},
            "肾内血瘀": {"tongue": {"紫暗舌有瘀斑": 2.0}, "pulse": {"沉涩脉": 2.0}},
            "精气衰竭": {"tongue": {"淡暗舌苔厚腻": 2.0}, "pulse": {"沉弱脉": 2.0}}
        }
    
    def get_questionnaire(self) -> List[Dict]:
        """获取失眠问诊问卷 - 简化版，完整版待添加"""
        return [
            {
                "id": 1,
                "text": "您认为自己的睡眠状况如何？",
                "type": "单选",
                "options": [
                    {"value": "好", "label": "好", "score": 0},
                    {"value": "一般", "label": "一般", "score": 1},
                    {"value": "较差", "label": "较差", "score": 2}
                ],
                "category": "睡眠质量"
            },
            # 更多问题待从588系统完整移植...
        ]
    
    def calculate_scores(self, answers: List[Dict]) -> Dict[str, float]:
        """计算各证型得分"""
        scores = {}
        
        # 提取症状和舌脉信息
        symptoms = []
        tongue = ""
        pulse = ""
        
        # 从答案中解析症状（这里需要根据实际问卷结构调整）
        for answer in answers:
            # 临时处理逻辑，实际需要根据问卷映射症状
            pass
        
        # 计算各证型得分
        for syndrome in self.SYMPTOM_WEIGHTS.keys():
            score = self._calculate_syndrome_score(syndrome, symptoms, tongue, pulse)
            scores[syndrome] = score
        
        return scores
    
    def _calculate_syndrome_score(self, syndrome: str, symptoms: List[str], 
                                  tongue: str, pulse: str) -> float:
        """计算单个证型得分"""
        total_score = 0.0
        
        # 症状得分
        symptom_weights = self.SYMPTOM_WEIGHTS.get(syndrome, {})
        for symptom in symptoms:
            if symptom in symptom_weights:
                total_score += symptom_weights[symptom]
        
        # 舌象得分
        tongue_weights = self.TONGUE_PULSE_WEIGHTS.get(syndrome, {}).get("tongue", {})
        if tongue in tongue_weights:
            total_score += tongue_weights[tongue]
        
        # 脉象得分
        pulse_weights = self.TONGUE_PULSE_WEIGHTS.get(syndrome, {}).get("pulse", {})
        if pulse in pulse_weights:
            total_score += pulse_weights[pulse]
        
        return total_score
    
    def determine_syndrome(self, scores: Dict[str, float]) -> Dict:
        """确定最终证型"""
        if not scores:
            return {"syndrome": "未确定", "confidence": 0.0}
        
        # 获取最高分证型
        max_syndrome = max(scores.items(), key=lambda x: x[1])
        syndrome_name, max_score = max_syndrome
        
        # 计算置信度（简化版）
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return {
            "syndrome": syndrome_name,
            "confidence": confidence,
            "all_scores": scores
        }
    
    def get_treatment_plan(self, syndrome: str) -> Dict:
        """获取治疗方案 - 框架结构，具体内容待完善"""
        return {
            "syndrome": syndrome,
            "herbal_formula": f"{syndrome}对应方剂（待完善）",
            "external_treatments": f"{syndrome}外治法（待完善）",
            "diet_therapy": f"{syndrome}食疗方（待完善）",
            "lifestyle": f"{syndrome}生活调理（待完善）"
        }