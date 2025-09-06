from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

# 二元诊断表的行元素（系统/脏腑）
class RowDimension(Enum):
    BONE_MARROW = "骨髓"
    LIVER_SPLEEN_CIRCULATION = "肝脾循环"  
    BLOOD_INTERNAL_CIRCULATION = "血内循环"
    SPIRIT_INTERNAL_CIRCULATION = "神内循环"
    # 需要医师补充完整的行元素

# 二元诊断表的列元素（状态）
class ColumnDimension(Enum):
    EMPTY_DEFICIENCY = "空虚"
    DEFICIENCY = "不足"
    STAGNATION = "不畅"
    # 需要医师补充完整的列元素

# 最终证型（行列交叉的结果）
class FinalSyndromeType(Enum):
    BONE_MARROW_EMPTY = "骨髓空虚"
    BRAIN_MARROW_EMPTY = "脑髓空虚"
    LIVER_SPLEEN_STAGNATION = "肝脾不畅"
    LIVER_YIN_DEFICIENCY = "肝郁脾虚"  
    BLOOD_DEFICIENCY = "气血两虚"
    BLOOD_STASIS = "气滞血瘀"
    SPIRIT_EMPTY = "精髓空虚"
    NEURASTHENIA = "神经衰弱"
    # 医师需要补充所有6个证型

@dataclass
class QuestionnaireAnswer:
    """问诊表答案"""
    question_id: int
    selected_options: List[str]

@dataclass
class PatientAnswers:
    """患者所有答案"""
    answers: List[QuestionnaireAnswer]
    
    def get_answer_by_question_id(self, question_id: int) -> Optional[QuestionnaireAnswer]:
        for answer in self.answers:
            if answer.question_id == question_id:
                return answer
        return None

@dataclass
class BinaryDiagnosisResult:
    """二元诊断结果"""
    row_dimension: RowDimension
    column_dimension: ColumnDimension  
    final_syndrome: FinalSyndromeType
    confidence_score: float  # 诊断置信度
    
    # 各维度得分详情
    row_scores: Dict[RowDimension, float]
    column_scores: Dict[ColumnDimension, float]
    
@dataclass
class TreatmentRecommendation:
    """治疗建议"""
    syndrome_type: FinalSyndromeType
    herbal_formula: Dict[str, str]  # 药材:剂量
    external_treatment: List[str]  # 外治法
    diet_therapy: List[str]  # 食疗方
    lifestyle_advice: List[str]  # 生活建议
    course_duration: str  # 疗程建议