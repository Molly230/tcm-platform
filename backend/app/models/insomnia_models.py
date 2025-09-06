from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class InsomniaSeverity(Enum):
    MILD = "轻度"
    MODERATE = "中度" 
    SEVERE = "重度"

class InsomniaType(Enum):
    DIFFICULTY_FALLING_ASLEEP = "入睡困难"
    FREQUENT_AWAKENING = "易醒多梦"
    EARLY_AWAKENING = "早醒"
    MIXED = "混合型"

# 二元诊断系统 - 最终6个证型
class FinalSyndromeType(Enum):
    SYNDROME_1 = "证型1"
    SYNDROME_2 = "证型2" 
    SYNDROME_3 = "证型3"
    SYNDROME_4 = "证型4"
    SYNDROME_5 = "证型5"
    SYNDROME_6 = "证型6"

# 二元诊断的基础分类要素
class DiagnosticDimensions(Enum):
    # 虚实分类
    BONE_MARROW_EMPTY_DEFICIENCY = "骨髓空虚"
    BRAIN_MARROW_EMPTY_DEFICIENCY = "脑髓空虚" 
    LIVER_BLOOD_INSUFFICIENCY = "肝血不足"
    LIVER_YIN_INSUFFICIENCY = "肝阴不足"
    KIDNEY_YIN_DEFICIENCY = "肾阴虚"
    KIDNEY_YANG_DEFICIENCY = "肾阳虚"
    LIVER_QI_STAGNATION_BLOOD_STASIS = "肝气郁滞"
    KIDNEY_INTERNAL_BLOOD_STASIS = "肾内血瘀"
    HEART_KIDNEY_ESSENCE_DEFICIENCY = "精气衰竭"

@dataclass
class PatientInfo:
    age: int
    gender: str
    occupation: str
    sleep_duration: float
    sleep_onset_time: int  # 入睡时间(分钟)
    awakening_frequency: int  # 夜醒次数
    sleep_quality_score: int  # 1-10分
    
@dataclass
class Symptoms:
    primary_symptoms: List[str]  # 主症
    secondary_symptoms: List[str]  # 次症
    tongue_appearance: str  # 舌象
    pulse_condition: str  # 脉象
    mental_state: str  # 精神状态
    
@dataclass
class HerbalPrescription:
    formula_name: str
    ingredients: Dict[str, str]  # 药材:剂量
    preparation_method: str
    dosage_instructions: str
    duration_days: int
    
@dataclass
class ExternalTreatment:
    method_name: str
    acupoints: List[str]
    technique: str
    frequency: str
    duration: str
    precautions: List[str]
    
@dataclass
class DietTherapy:
    recipe_name: str
    ingredients: List[str]
    preparation: str
    timing: str  # 服用时间
    effects: str  # 功效
    contraindications: List[str]  # 禁忌
    
@dataclass
class DiagnosticScores:
    """二元诊断各维度得分"""
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
class TreatmentPlan:
    diagnosis: str
    final_syndrome_type: FinalSyndromeType
    diagnostic_scores: DiagnosticScores
    herbal_prescription: HerbalPrescription
    external_treatments: List[ExternalTreatment]
    diet_therapy: List[DietTherapy]
    lifestyle_advice: List[str]