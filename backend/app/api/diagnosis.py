"""
诊断系统API接口
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from ..database import get_db
from ..diagnosis.insomnia_diagnosis_engine import InsomniaDiagnosisEngine
from ..diagnosis.insomnia_questionnaire import InsomniaQuestionnaire
from ..knowledge.insomnia_knowledge import InsomniaKnowledgeBase
from ..models.insomnia_models import Symptoms

router = APIRouter(prefix="/diagnosis", tags=["诊断系统"])

def _get_question_hint(question_num: int, category: str, question_type: str) -> str:
    """获取问题提示信息"""
    if question_num <= 9:
        return "基础睡眠状况评估 - 用于计算失眠严重程度"
    elif category == "肝肠证型":
        return "情绪压力相关症状 - 影响肝气郁滞诊断"
    elif category == "血液证型":
        return "身体疼痛相关症状 - 影响气血状态诊断"
    elif category == "神内证型":
        return "精神神经相关症状 - 影响神经功能诊断"
    elif category == "骨髓证型":
        return "肾虚相关症状 - 影响肾精不足诊断"
    elif category == "脑髓证型":
        return "脑力消耗相关症状 - 影响脑髓空虚诊断"
    else:
        return "请根据您的实际情况选择最符合的选项"

# 请求体模型定义（兼容588项目的数据格式）
class AnswerItem(BaseModel):
    question_id: int
    selected_options: List[str]

class AnalyzeRequest(BaseModel):
    answers: List[AnswerItem]
    
    class Config:
        # 允许额外字段，兼容更多的请求格式
        extra = "allow"

# 失眠诊断引擎和知识库
questionnaire = InsomniaQuestionnaire()
knowledge_base = InsomniaKnowledgeBase()
# 版本: 2.1 - 添加了布局信息


@router.get("/diseases")
async def get_diseases():
    """获取支持的疾病类型"""
    return {
        "diseases": [
            {"code": "insomnia", "name": "失眠", "status": "active"},
            {"code": "stomach", "name": "胃病", "status": "active"},
            {"code": "aging", "name": "早衰", "status": "active"}
        ]
    }



@router.get("/insomnia/questionnaire")
async def get_insomnia_questionnaire():
    """获取18题失眠问诊问卷"""
    try:
        questions = questionnaire.get_questions()
        # 转换为API返回格式，添加美化信息
        formatted_questions = []
        for i, q in enumerate(questions):
            # 判断问题类型的显示名称
            type_display = {
                "single": "单选题",
                "multiple": "多选题", 
                "yes_no": "是非题"
            }.get(q.type, "单选题")
            
            # 添加问题序号和美化格式
            question_number = f"第{i+1}题"
            
            # 为不同类型的问题添加不同的样式类
            css_class = {
                "基础评分": "basic-question",
                "肝肠证型": "liver-question", 
                "血液证型": "blood-question",
                "神内证型": "neural-question",
                "骨髓证型": "bone-question",
                "脑髓证型": "brain-question"
            }.get(q.category, "default-question")
            
            # 确定每行显示的选项数量
            options_per_row = 3 if len(q.options) >= 3 else len(q.options)
            if q.type == "yes_no":
                options_per_row = 2  # 是非题只有两个选项
            elif len(q.options) == 4:
                options_per_row = 2  # 4个选项时每行显示2个
            elif len(q.options) >= 5:
                options_per_row = 3  # 5个或更多选项时每行显示3个
            
            formatted_question = {
                "id": q.id,
                "number": question_number,
                "text": q.text,
                "type": q.type,
                "type_display": type_display,
                "category": q.category,
                "css_class": css_class,
                "required": q.required,
                "options": [
                    {
                        "value": opt.value, 
                        "label": opt.label, 
                        "score": opt.score,
                        "display": f"{opt.value}. {opt.label}"
                    } for opt in q.options
                ],
                # 添加布局信息
                "layout": {
                    "question_alignment": "center",
                    "options_per_row": options_per_row,
                    "option_alignment": "left",
                    "show_question_number": True
                },
                # 添加问题提示信息
                "hint": _get_question_hint(i+1, q.category, q.type)
            }
            formatted_questions.append(formatted_question)
        
        # 返回问卷和概要信息
        summary = questionnaire.get_questionnaire_summary()
        
        # 按分组整理问题
        question_groups = [
            {
                "group_id": 1,
                "group_name": "基础睡眠评估",
                "group_description": "评估您的基础睡眠状况，计算失眠严重程度",
                "questions": [q for q in formatted_questions if q["category"] == "基础评分"],
                "icon": "🛏️",
                "color": "#4A90E2"
            },
            {
                "group_id": 2, 
                "group_name": "中医证型分析",
                "group_description": "根据中医理论分析您的体质特点和证型",
                "questions": [q for q in formatted_questions if q["category"] != "基础评分"],
                "icon": "⚗️",
                "color": "#7ED321"
            }
        ]
        
        return {
            "success": True,
            "data": {
                "questions": formatted_questions,
                "question_groups": question_groups,
                "total": len(formatted_questions),
                "summary": summary,
                "questionnaire_info": {
                    "title": "失眠中医辨证问卷",
                    "subtitle": "基于18题专业失眠评估系统",
                    "version": "2.0",
                    "description": "结合现代医学和传统中医理论的综合性失眠诊断问卷",
                    "estimated_time": "5-8分钟",
                    "total_questions": len(formatted_questions)
                },
                "layout_config": {
                    "question_container": {
                        "alignment": "center",
                        "max_width": "800px",
                        "margin": "0 auto",
                        "padding": "20px"
                    },
                    "question_title": {
                        "text_align": "center",
                        "font_weight": "bold",
                        "margin_bottom": "15px"
                    },
                    "options_container": {
                        "display": "grid",
                        "grid_template_columns": "repeat(auto-fit, minmax(200px, 1fr))",
                        "gap": "10px",
                        "justify_items": "start",
                        "margin_top": "10px"
                    },
                    "option_item": {
                        "display": "flex",
                        "align_items": "center",
                        "padding": "8px 12px",
                        "border_radius": "6px",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease"
                    }
                },
                "instructions": [
                    "请根据您最近一个月的实际情况如实回答",
                    "每道题目都有相应的提示信息帮助您理解",
                    "前9题为基础评估，后10题为中医证型分析",
                    "所有题目均为必填项，请认真考虑后选择"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问卷失败: {str(e)}")


@router.api_route("/insomnia/analyze", methods=["POST"])  
async def analyze_insomnia(request: Request):
    """失眠诊断分析 - 使用18题问卷的精确诊断逻辑"""
    try:
        # 解析请求数据
        body = await request.body()
        import json
        data = json.loads(body.decode('utf-8'))
        
        if not data or 'answers' not in data:
            return {
                'success': False,
                'error': '请提供患者答案数据'
            }
        
        # 将前端答案格式转换为诊断引擎需要的格式
        answers_dict = {}
        
        for answer_data in data['answers']:
            question_id = str(answer_data['question_id'])
            selected_options = answer_data.get('selected_options', [])
            
            # 处理不同类型的问题
            if len(selected_options) == 1:
                # 单选题或是非题
                answers_dict[question_id] = selected_options[0]
            elif len(selected_options) > 1:
                # 多选题
                answers_dict[question_id] = selected_options
            else:
                # 未选择
                answers_dict[question_id] = []
        
        # 使用新的失眠诊断引擎进行分析
        diagnosis_result = InsomniaDiagnosisEngine.analyze_questionnaire(answers_dict)
        
        # 返回完整的诊断结果
        return {
            'success': True,
            'data': {
                'patient_id': data.get('patient_id', 'diagnosed_patient'),
                'diagnosis_result': {
                    # 基础信息
                    'base_score': diagnosis_result.base_score,
                    'insomnia_level': diagnosis_result.level.value,
                    'syndrome_type': diagnosis_result.syndrome.value,
                    'confidence_score': diagnosis_result.confidence,
                    
                    # 详细得分
                    'detailed_scores': {
                        'liver_intestine': diagnosis_result.syndrome_scores.liver_intestine,
                        'blood': diagnosis_result.syndrome_scores.blood,
                        'neural': diagnosis_result.syndrome_scores.neural,
                        'bone_marrow': diagnosis_result.syndrome_scores.bone_marrow,
                        'brain_marrow': diagnosis_result.syndrome_scores.brain_marrow
                    },
                    
                    # 治疗方案
                    'treatment_plan': diagnosis_result.treatment_plan,
                    
                    # 诊断描述
                    'description': f"{diagnosis_result.base_score}分{diagnosis_result.level.value}，证型：{diagnosis_result.syndrome.value}，置信度：{diagnosis_result.confidence:.1%}"
                },
                'timestamp': '2024-01-01T00:00:00Z',
                'processed_answers': len(data['answers'])
            }
        }
        
    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': f"诊断分析失败: {str(e)}",
            'traceback': traceback.format_exc()
        }


@router.get("/insomnia/knowledge/syndromes")
async def get_insomnia_syndromes():
    """获取失眠证型知识"""
    try:
        syndromes = knowledge_base.SYNDROME_PATTERNS
        return {"syndromes": syndromes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取证型知识失败: {str(e)}")


@router.get("/insomnia/knowledge/formulas")
async def get_insomnia_formulas():
    """获取失眠方剂知识"""
    try:
        formulas = knowledge_base.CLASSICAL_FORMULAS
        return {"formulas": formulas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取方剂知识失败: {str(e)}")


@router.get("/insomnia/knowledge/treatments")
async def get_insomnia_treatments():
    """获取失眠外治法知识"""
    try:
        treatments = knowledge_base.EXTERNAL_TREATMENTS
        return {"treatments": treatments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取外治法知识失败: {str(e)}")


@router.get("/insomnia/knowledge/diet")
async def get_insomnia_diet():
    """获取失眠食疗知识"""
    try:
        diet = knowledge_base.DIET_THERAPY
        return {"diet": diet}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取食疗知识失败: {str(e)}")


# 胃病诊断接口
@router.get("/stomach/questionnaire")
async def get_stomach_questionnaire():
    """获取胃病问诊问卷"""
    return {"message": "胃病问卷系统初始化中", "questions": [], "total": 0}


@router.post("/stomach/analyze") 
async def analyze_stomach(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """胃病诊断分析"""
    try:
        answers = request.answers
        return {
            "message": "胃病诊断系统初始化中", 
            "diagnosis": {}, 
            "status": "pending",
            "received_answers": len(answers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"胃病诊断分析失败: {str(e)}")


# 早衰诊断接口
@router.get("/aging/questionnaire")
async def get_aging_questionnaire():
    """获取早衰问诊问卷"""
    return {"message": "早衰问卷系统初始化中", "questions": [], "total": 0}


@router.post("/aging/analyze")
async def analyze_aging(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """早衰诊断分析"""
    try:
        answers = request.answers
        return {
            "message": "早衰诊断系统初始化中", 
            "diagnosis": {}, 
            "status": "pending",
            "received_answers": len(answers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"早衰诊断分析失败: {str(e)}")