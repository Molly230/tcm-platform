from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class QuestionType(Enum):
    SINGLE_CHOICE = "单选"
    MULTIPLE_CHOICE = "多选"
    
@dataclass
class QuestionOption:
    value: str
    label: str
    score: float = 0.0  # 选项对应的分值

@dataclass  
class Question:
    id: int
    text: str
    type: QuestionType
    options: List[QuestionOption]
    category: str  # 问题分类，用于后续诊断

class InsomniaQuestionnaire:
    """失眠问诊表"""
    
    QUESTIONS = [
        Question(
            id=1,
            text="您认为自己的睡眠状况如何？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("好", "好"),
                QuestionOption("一般", "一般"), 
                QuestionOption("较差", "较差")
            ],
            category="睡眠质量"
        ),
        Question(
            id=2,
            text="通常情况下，您从上床准备睡觉到真正入睡需要多长时间？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("5分钟以内", "5分钟以内"),
                QuestionOption("6-15分钟", "6-15分钟"),
                QuestionOption("16-30分钟", "16-30分钟"),
                QuestionOption("31-60分钟", "31-60分钟"),
                QuestionOption("60分钟以上", "60分钟以上")
            ],
            category="入睡时间"
        ),
        Question(
            id=3,
            text="过去一个月内，您每天夜间睡眠时间有多长？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("8小时及以上", "8小时及以上"),
                QuestionOption("7-8小时", "7-8小时"),
                QuestionOption("6-7小时", "6-7小时"),
                QuestionOption("5-6小时", "5-6小时"),
                QuestionOption("5小时以下", "5小时以下")
            ],
            category="睡眠时长"
        ),
        Question(
            id=4,
            text="过去一个月内，您夜间平均醒来的次数大约是？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("几乎不醒来", "几乎不醒来"),
                QuestionOption("1次", "1次"),
                QuestionOption("2-3次", "2-3次"),
                QuestionOption("4次及以上", "4次及以上")
            ],
            category="夜醒次数"
        ),
        Question(
            id=5,
            text="过去一个月内，您夜间醒来后，再次入睡通常需要多长时间？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("5分钟以内", "5分钟以内"),
                QuestionOption("6-15分钟", "6-15分钟"),
                QuestionOption("16-30分钟", "16-30分钟"),
                QuestionOption("31-60分钟", "31-60分钟"),
                QuestionOption("60分钟以上", "60分钟以上")
            ],
            category="再入睡时间"
        ),
        Question(
            id=6,
            text="过去一个月内，您是否会在白天出现不可抗拒的睡眠欲望（如工作、学习或开车时突然想睡觉）？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("几乎没有", "几乎没有"),
                QuestionOption("每周1-2次", "每周1-2次"),
                QuestionOption("每周3-5次", "每周3-5次"),
                QuestionOption("每天都有", "每天都有")
            ],
            category="白天嗜睡"
        ),
        Question(
            id=7,
            text="您有怎样的睡眠困扰？（多选）",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("反复清醒", "反复清醒"),
                QuestionOption("整夜做梦", "整夜做梦"),
                QuestionOption("晨起疲倦", "晨起疲倦"),
                QuestionOption("难以入眠", "难以入眠")
            ],
            category="睡眠困扰"
        ),
        Question(
            id=8,
            text="您是否服用过以下类药物？（多选）",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("苯二氮卓类：地西泮、劳拉西泮", "苯二氮卓类：地西泮、劳拉西泮"),
                QuestionOption("非苯二氮卓类：唑吡坦、右佐匹克隆", "非苯二氮卓类：唑吡坦、右佐匹克隆"),
                QuestionOption("褪黑素受体激动剂：雷美替胺", "褪黑素受体激动剂：雷美替胺"),
                QuestionOption("食欲素受体拮抗剂：苏沃雷生", "食欲素受体拮抗剂：苏沃雷生"),
                QuestionOption("抗抑郁药物：曲唑酮、米氮平", "抗抑郁药物：曲唑酮、米氮平")
            ],
            category="用药史"
        ),
        Question(
            id=9,
            text="您服用安眠药时长多久？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("1个月以内", "1个月以内"),
                QuestionOption("1-3个月（慢性）", "1-3个月（慢性）"),
                QuestionOption("3个月以上（高级）", "3个月以上（高级）")
            ],
            category="用药时长"
        ),
        Question(
            id=10,
            text="您是否经常精神压力大/情绪紧张？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="精神状态"
        ),
        Question(
            id=11,
            text="您近期有无如下问题？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("时有耳鸣", "时有耳鸣"),
                QuestionOption("时实疲乏，乏力周身疲", "时实疲乏，乏力周身疲"),
                QuestionOption("腹胀/腹泻不适", "腹胀/腹泻不适")
            ],
            category="身体症状"
        ),
        Question(
            id=12,
            text="您是否经常周身酸痛/骨节疼痛？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="疼痛症状"
        ),
        Question(
            id=13,
            text="您近期有无如下问题？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("夜间遗精/遗尿，心悸加速", "夜间遗精/遗尿，心悸加速"),
                QuestionOption("皮肤蚊疹，发骚麻疹", "皮肤蚊疹，发骚麻疹"),
                QuestionOption("咳嗽/气短/难呼气", "咳嗽/气短/难呼气")
            ],
            category="特殊症状"
        ),
        Question(
            id=14,
            text="您是否持续电子产品超过3小时/天？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="生活习惯"
        ),
        Question(
            id=15,
            text="您近期有无如下问题？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("面色暗黑，无精打采", "面色暗黑，无精打采"),
                QuestionOption("容易受惊，害怕", "容易受惊，害怕"),
                QuestionOption("夜间盗汗", "夜间盗汗")
            ],
            category="中医症状"
        ),
        Question(
            id=16,
            text="您是否劳心耗神过度？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="精神消耗"
        ),
        Question(
            id=17,
            text="您近期有无如下问题？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("腰酸无力", "腰酸无力")
            ],
            category="肾虚症状"
        ),
        Question(
            id=18,
            text="您是否用脑过度？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="用脑过度"
        ),
        Question(
            id=19,
            text="您近期有无如下问题？",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("好忘事，记忆力下降", "好忘事，记忆力下降"),
                QuestionOption("白天嗜睡", "白天嗜睡"),
                QuestionOption("偏头痛/头痛", "偏头痛/头痛")
            ],
            category="认知功能"
        )
    ]

    @classmethod
    def get_questions(cls):
        """获取所有问题"""
        return cls.QUESTIONS
    
    @classmethod
    def get_question_by_id(cls, question_id: int):
        """根据ID获取问题"""
        for question in cls.QUESTIONS:
            if question.id == question_id:
                return question
        return None
        
    @classmethod
    def validate_answers(cls, answers: List[dict]) -> bool:
        """验证答案格式"""
        if len(answers) != len(cls.QUESTIONS):
            return False
            
        for answer in answers:
            if 'question_id' not in answer or 'selected_options' not in answer:
                return False
                
        return True