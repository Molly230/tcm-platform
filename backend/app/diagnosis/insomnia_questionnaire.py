from typing import Dict, List
from dataclasses import dataclass

@dataclass
class QuestionOption:
    """问题选项"""
    value: str
    label: str
    score: int = 0

@dataclass
class Question:
    """问题定义"""
    id: int
    text: str
    type: str  # "single", "multiple", "yes_no"
    options: List[QuestionOption]
    category: str = ""
    required: bool = True

class InsomniaQuestionnaire:
    """19题失眠问卷"""
    
    @staticmethod
    def get_questions() -> List[Question]:
        """获取完整的19题问卷"""
        
        questions = [
            # 基础评分题（1-9题）
            Question(
                id=1,
                text="您认为自己的睡眠状况如何？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "好", 20),
                    QuestionOption("B", "一般", 10),
                    QuestionOption("C", "较差", 0)
                ]
            ),
            
            Question(
                id=2,
                text="通常情况下，您从上床准备睡觉到真正入睡需要多长时间？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "5分钟以内", 12),
                    QuestionOption("B", "6-15分钟", 12),
                    QuestionOption("C", "16-30分钟", 9),
                    QuestionOption("D", "31-60分钟", 6),
                    QuestionOption("E", "60分钟以上", 3),
                    QuestionOption("F", "极长时间", 0)
                ]
            ),
            
            Question(
                id=3,
                text="过去一个月内，您每天夜间睡眠时间有多长？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "8小时及以上", 12),
                    QuestionOption("B", "7-8小时", 12),
                    QuestionOption("C", "6-7小时", 9),
                    QuestionOption("D", "5-6小时", 6),
                    QuestionOption("E", "5小时以下", 3),
                    QuestionOption("F", "极少睡眠", 0)
                ]
            ),
            
            Question(
                id=4,
                text="过去一个月内，您夜间平均醒来的次数大约是？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "几乎不醒来", 9),
                    QuestionOption("B", "1次", 9),
                    QuestionOption("C", "2-3次", 6),
                    QuestionOption("D", "4次及以上", 3),
                    QuestionOption("E", "频繁醒来", 0)
                ]
            ),
            
            Question(
                id=5,
                text="过去一个月内，您夜间醒来后，再次入睡通常需要多长时间？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "5分钟以内", 12),
                    QuestionOption("B", "6-15分钟", 12),
                    QuestionOption("C", "16-30分钟", 9),
                    QuestionOption("D", "31-60分钟", 6),
                    QuestionOption("E", "60分钟以上", 3),
                    QuestionOption("F", "极长时间", 0)
                ]
            ),
            
            Question(
                id=6,
                text="过去一个月内，您是否会在白天出现不可抗拒的睡眠欲望（如工作、学习或开车时突然想睡觉）？",
                type="single",
                category="基础评分",
                options=[
                    QuestionOption("A", "几乎没有", 9),
                    QuestionOption("B", "每周1-2次", 6),
                    QuestionOption("C", "每周3-5次", 3),
                    QuestionOption("D", "每天都有", 0)
                ]
            ),
            
            Question(
                id=7,
                text="您有怎样的睡眠困扰？（多选）",
                type="multiple",
                category="基础评分",
                options=[
                    QuestionOption("A", "反复清醒", -3),
                    QuestionOption("B", "整夜做梦", -3),
                    QuestionOption("C", "晨起疲倦", -3),
                    QuestionOption("D", "难以入眠", -3),
                    QuestionOption("E", "无", 0)
                ]
            ),
            
            Question(
                id=8,
                text="您是否服用过以下安眠药物？（多选）",
                type="multiple",
                category="基础评分",
                options=[
                    QuestionOption("A", "苯二氮䓬类：地西泮、劳拉西泮", -5),
                    QuestionOption("B", "非苯二氮䓬类：唑吡坦、右佐匹克隆", -5),
                    QuestionOption("C", "褪黑素受体激动剂：雷美替胺", -5),
                    QuestionOption("D", "食欲素受体拮抗剂：苏沃雷生", -5),
                    QuestionOption("E", "抗抑郁药物：曲唑酮、米氮平", -5),
                    QuestionOption("F", "无", 0)
                ]
            ),
            
            # 服药时长（第9题）- 条件显示：仅当第8题选择了药物时显示
            Question(
                id=9,
                text="您服用安眠药时长周期？",
                type="single",
                category="基础评分",
                required=False,
                options=[
                    QuestionOption("A", "1个月以内", 6),
                    QuestionOption("B", "1-3个月", 4),
                    QuestionOption("C", "3个月以上", 2),
                    QuestionOption("D", "长期使用", 0)
                ]
            ),
            
            # 证型评分题（10-19题）
            Question(
                id=10,
                text="您是否经常精神压力大/情绪紧张？",
                type="yes_no",
                category="肝肠证型",
                options=[
                    QuestionOption("是", "是", 1),
                    QuestionOption("否", "否", 0)
                ]
            ),
            
            Question(
                id=11,
                text="您是否经常周身酸痛/脊柱疼痛？",
                type="yes_no",
                category="血液证型",
                options=[
                    QuestionOption("是", "是", 1),
                    QuestionOption("否", "否", 0)
                ]
            ),
            
            Question(
                id=12,
                text="您是否接触电子产品超过3小时/天？",
                type="yes_no",
                category="神内证型",
                options=[
                    QuestionOption("是", "是", 1),
                    QuestionOption("否", "否", 0)
                ]
            ),
            
            Question(
                id=13,
                text="您是否劳心耗神过度？",
                type="yes_no",
                category="骨髓证型",
                options=[
                    QuestionOption("是", "是", 1),
                    QuestionOption("否", "否", 0)
                ]
            ),
            
            Question(
                id=14,
                text="您是否用脑过度？",
                type="yes_no",
                category="脑髓证型",
                options=[
                    QuestionOption("是", "是", 1),
                    QuestionOption("否", "否", 0)
                ]
            ),
            
            Question(
                id=15,
                text="您近期有无如下问题？",
                type="multiple",
                category="肝肠证型",
                options=[
                    QuestionOption("A", "时有耳鸣", 1),
                    QuestionOption("B", "时发痔疮，肛周瘙痒", 1),
                    QuestionOption("C", "腹胀/腹部不适", 1),
                    QuestionOption("D", "无", 0)
                ]
            ),
            
            Question(
                id=16,
                text="您近期有无如下问题？",
                type="multiple",
                category="血液证型",
                options=[
                    QuestionOption("A", "夜间憋醒/胸闷，心跳加速", 1),
                    QuestionOption("B", "皮肤瘙痒，发荨麻疹", 1),
                    QuestionOption("C", "咳嗽/气短/喘促等", 1),
                    QuestionOption("D", "无", 0)
                ]
            ),
            
            Question(
                id=17,
                text="您近期有无如下问题？",
                type="multiple",
                category="神内证型",
                options=[
                    QuestionOption("A", "面色黯黑，无精打采", 1),
                    QuestionOption("B", "容易受惊，害怕", 1),
                    QuestionOption("C", "夜间盗汗", 1),
                    QuestionOption("D", "无", 0)
                ]
            ),
            
            Question(
                id=18,
                text="您近期有无如下问题？",
                type="multiple",
                category="骨髓证型",
                options=[
                    QuestionOption("A", "腰酸无力", 1),
                    QuestionOption("B", "身寒怕冷", 1),
                    QuestionOption("C", "夜尿频繁", 1),
                    QuestionOption("D", "无", 0)
                ]
            ),
            
            Question(
                id=19,
                text="您近期有无如下问题？",
                type="multiple",
                category="脑髓证型",
                options=[
                    QuestionOption("A", "好忘事，记忆力下降", 1),
                    QuestionOption("B", "白天嗜睡", 1),
                    QuestionOption("C", "偏头痛/头痛", 1),
                    QuestionOption("D", "无", 0)
                ]
            )
        ]
        
        return questions
    
    @staticmethod
    def get_questionnaire_summary() -> Dict:
        """获取问卷概要信息"""
        questions = InsomniaQuestionnaire.get_questions()
        
        return {
            "total_questions": len(questions),
            "categories": {
                "基础评分": "1-8题，计算失眠严重程度",
                "肝肠证型": "10、15题，情绪压力相关",
                "血液证型": "11、16题，身体疼痛相关", 
                "神内证型": "12、17题，精神神经相关",
                "骨髓证型": "13、18题，肾虚相关",
                "脑髓证型": "14、19题，脑力消耗相关"
            },
            "scoring_rules": {
                "基础分数": "1-8题总分，用于确定失眠等级（第9题不参与评分）",
                "证型分数": "10-19题分别计分，用于证型矩阵匹配",
                "等级划分": "无需治疗(≥103分)、初级失眠(60-102分)、中级失眠(45-59分)、高级失眠(≤44分)"
            }
        }