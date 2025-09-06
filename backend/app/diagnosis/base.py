"""
中医诊断系统基础框架
支持多病症扩展：失眠、胃病、早衰
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum


class DiseaseType(Enum):
    """疾病类型枚举"""
    INSOMNIA = "失眠"
    STOMACH = "胃病"
    AGING = "早衰"


class DiagnosisBase(ABC):
    """诊断引擎基类"""
    
    def __init__(self, disease_type: DiseaseType):
        self.disease_type = disease_type
    
    @abstractmethod
    def get_questionnaire(self) -> List[Dict]:
        """获取问诊问卷"""
        pass
    
    @abstractmethod
    def calculate_scores(self, answers: List[Dict]) -> Dict[str, float]:
        """计算各证型得分"""
        pass
    
    @abstractmethod
    def determine_syndrome(self, scores: Dict[str, float]) -> Dict:
        """确定最终证型"""
        pass
    
    @abstractmethod
    def get_treatment_plan(self, syndrome: str) -> Dict:
        """获取治疗方案"""
        pass


class KnowledgeBase(ABC):
    """知识库基类"""
    
    @abstractmethod
    def get_syndrome_patterns(self) -> Dict:
        """获取证型模式"""
        pass
    
    @abstractmethod
    def get_formulas(self) -> Dict:
        """获取方剂库"""
        pass
    
    @abstractmethod
    def get_external_treatments(self) -> Dict:
        """获取外治法"""
        pass
    
    @abstractmethod
    def get_diet_therapy(self) -> Dict:
        """获取食疗方"""
        pass