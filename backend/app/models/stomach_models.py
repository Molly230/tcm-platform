from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class StomachDiseaseSeverity(Enum):
    MILD = "轻度"
    MODERATE = "中度" 
    SEVERE = "重度"

class StomachDiseaseType(Enum):
    GASTRITIS = "胃炎"
    GASTRIC_ULCER = "胃溃疡"
    DUODENAL_ULCER = "十二指肠溃疡"
    FUNCTIONAL_DYSPEPSIA = "功能性消化不良"
    GERD = "胃食管反流病"

# 胃病诊断证型
class StomachSyndromeType(Enum):
    SPLEEN_STOMACH_QI_DEFICIENCY = "脾胃气虚"
    STOMACH_YIN_DEFICIENCY = "胃阴虚"
    LIVER_QI_INVADING_STOMACH = "肝气犯胃"
    STOMACH_HEAT = "胃热证"
    COLD_STOMACH = "胃寒证"
    BLOOD_STASIS_STOMACH = "胃络血瘀"

# 胃病诊断维度
class StomachDiagnosticDimensions(Enum):
    SPLEEN_QI_DEFICIENCY = "脾气虚"
    STOMACH_QI_DEFICIENCY = "胃气虚"
    STOMACH_YIN_INSUFFICIENCY = "胃阴不足"
    LIVER_QI_STAGNATION = "肝气郁滞"
    STOMACH_HEAT_PATTERN = "胃热证"
    STOMACH_COLD_PATTERN = "胃寒证"
    BLOOD_STASIS_PATTERN = "血瘀证"

@dataclass
class StomachPatientInfo:
    age: int
    gender: str
    occupation: str
    symptom_duration: int  # 症状持续时间(月)
    pain_frequency: int  # 疼痛频率(每周几次)
    pain_intensity: int  # 疼痛强度 1-10分
    appetite_score: int  # 食欲评分 1-10分
    
@dataclass
class StomachSymptoms:
    primary_symptoms: List[str]  # 主症：胃痛、胃胀、恶心等
    secondary_symptoms: List[str]  # 次症：嗳气、反酸、食欲不振等
    tongue_appearance: str  # 舌象
    pulse_condition: str  # 脉象
    bowel_movement: str  # 大便情况
    
@dataclass
class StomachHerbalPrescription:
    formula_name: str
    ingredients: Dict[str, str]  # 药材:剂量
    preparation_method: str
    dosage_instructions: str
    duration_days: int
    
@dataclass
class StomachExternalTreatment:
    method_name: str
    acupoints: List[str]
    technique: str
    frequency: str
    duration: str
    precautions: List[str]
    
@dataclass
class StomachDietTherapy:
    recipe_name: str
    ingredients: List[str]
    preparation: str
    timing: str  # 服用时间
    effects: str  # 功效
    contraindications: List[str]  # 禁忌
    
@dataclass
class StomachDiagnosticScores:
    """胃病诊断各维度得分"""
    spleen_qi_score: float = 0.0
    stomach_qi_score: float = 0.0
    stomach_yin_score: float = 0.0
    liver_qi_stagnation_score: float = 0.0
    stomach_heat_score: float = 0.0
    stomach_cold_score: float = 0.0
    blood_stasis_score: float = 0.0
    
@dataclass
class StomachTreatmentPlan:
    diagnosis: str
    final_syndrome_type: StomachSyndromeType
    diagnostic_scores: StomachDiagnosticScores
    herbal_prescription: StomachHerbalPrescription
    external_treatments: List[StomachExternalTreatment]
    diet_therapy: List[StomachDietTherapy]
    lifestyle_advice: List[str]