#!/usr/bin/env python3
"""
测试新的失眠诊断引擎
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.diagnosis.insomnia_diagnosis_engine import InsomniaDiagnosisEngine

# 测试数据 - 19题答案
test_answers = {
    "1": "A",      # 睡眠状况：好 (20分)
    "2": "A",      # 入睡时间：5分钟以内 (12分)
    "3": "A",      # 睡眠时长：8小时及以上 (12分)
    "4": "A",      # 醒来次数：几乎不醒来 (9分)
    "5": "A",      # 再次入睡：5分钟以内 (12分)
    "6": "A",      # 白天嗜睡：几乎没有 (9分)
    "7": ["A"],    # 睡眠困扰：反复清醒 (12-3=9分)
    "8": ["A"],    # 安眠药：苯二氮䓬类 (20-5=15分)
    "9": "A",      # 服药时长：1个月以内 (6分)
    "10": "是",    # 精神压力大 (肝肠+1)
    "11": "是",    # 周身酸痛 (血液+1)
    "12": "是",    # 电子产品超过3小时 (神内+1)
    "13": "是",    # 劳心耗神过度 (骨髓+1)
    "14": "是",    # 用脑过度 (脑髓+1)
    "15": ["A"],   # 肝肠证型症状 (肝肠+1)
    "16": ["A"],   # 血液证型症状 (血液+1)
    "17": ["A"],   # 神内证型症状 (神内+1)
    "18": ["A"],   # 骨髓证型症状 (骨髓+1)
    "19": ["A", "B"]  # 脑髓证型症状 (脑髓+2)
}

if __name__ == "__main__":
    print("=== 测试新的失眠诊断引擎 ===")
    
    try:
        # 调用新引擎
        result = InsomniaDiagnosisEngine.analyze_questionnaire(test_answers)
        
        print(f"基础分数: {result.base_score}")
        print(f"失眠等级: {result.level.value}")
        print(f"证型类型: {result.syndrome.value}")
        print(f"置信度: {result.confidence:.1%}")
        
        print("\n证型分数:")
        print(f"  肝肠: {result.syndrome_scores.liver_intestine}")
        print(f"  血液: {result.syndrome_scores.blood}")
        print(f"  神内: {result.syndrome_scores.neural}")
        print(f"  骨髓: {result.syndrome_scores.bone_marrow}")
        print(f"  脑髓: {result.syndrome_scores.brain_marrow}")
        
        print(f"\n治疗方案等级: {result.treatment_plan.get('level', '未知')}")
        print("推荐产品:", result.treatment_plan.get('products', []))
        print("穴位建议:", result.treatment_plan.get('acupoints', []))
        
        print("\n=== 测试成功！ ===")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()