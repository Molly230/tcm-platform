"""
系统配置相关API - 包含枚举值管理
"""
from fastapi import APIRouter, Depends
from typing import Dict, List, Any

from app.core.enums_v2 import EnumManager
from app.core.response import success_response

router = APIRouter()


@router.get("/enums", summary="获取所有枚举配置")
def get_all_enums() -> Dict[str, Any]:
    """
    获取系统所有枚举配置
    前端可以通过这个接口获取最新的枚举值，避免硬编码
    """
    
    def enum_items_to_dict(items):
        """将EnumItem列表转换为前端需要的格式"""
        return [
            {
                "code": item.code,
                "zh": item.zh,
                "en": item.en,
                "description": item.description,
                "order": item.order,
                "nextStates": item.next_states,
                "requiredPermissions": item.required_permissions,
                "color": item.color
            }
            for item in items
        ]
    
    enum_types = [
        "PRODUCT_CATEGORY",
        "PRODUCT_STATUS", 
        "AUDIT_STATUS",
        "ORDER_STATUS",
        "USER_ROLE"
    ]
    
    result = {}
    for enum_type in enum_types:
        items = EnumManager.get_enum_items(enum_type)
        result[enum_type] = enum_items_to_dict(items)
    
    return success_response(data=result, message="枚举配置获取成功")


@router.get("/enums/{enum_type}", summary="获取指定类型枚举")
def get_enum_by_type(enum_type: str) -> Dict[str, Any]:
    """
    获取指定类型的枚举值
    
    支持的枚举类型:
    - PRODUCT_CATEGORY: 商品分类
    - PRODUCT_STATUS: 商品状态
    - AUDIT_STATUS: 审核状态
    - ORDER_STATUS: 订单状态
    - USER_ROLE: 用户角色
    """
    items = EnumManager.get_enum_items(enum_type)
    
    if not items:
        return success_response(data=[], message=f"枚举类型 {enum_type} 不存在")
    
    enum_data = [
        {
            "code": item.code,
            "zh": item.zh,
            "en": item.en,
            "description": item.description,
            "order": item.order,
            "nextStates": item.next_states,
            "requiredPermissions": item.required_permissions,
            "color": item.color
        }
        for item in items
    ]
    
    return success_response(data=enum_data, message=f"{enum_type} 枚举获取成功")


@router.get("/enums/{enum_type}/states/{current_state}", summary="获取状态机下一步状态")
def get_next_states(enum_type: str, current_state: str) -> Dict[str, Any]:
    """
    获取状态机中当前状态的下一步可选状态
    用于动态显示状态转换按钮
    """
    next_states = EnumManager.get_next_states(enum_type, current_state)
    
    # 获取下一步状态的详细信息
    all_items = EnumManager.get_enum_dict(enum_type)
    next_state_details = []
    
    for state in next_states:
        item = all_items.get(state)
        if item:
            next_state_details.append({
                "code": item.code,
                "zh": item.zh,
                "en": item.en,
                "description": item.description,
                "color": item.color,
                "requiredPermissions": item.required_permissions
            })
    
    return success_response(
        data={
            "currentState": current_state,
            "nextStates": next_states,
            "nextStateDetails": next_state_details
        },
        message="状态转换选项获取成功"
    )


@router.post("/enums/validate", summary="验证枚举值")
def validate_enum_values(validation_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    批量验证枚举值是否有效
    
    请求格式:
    {
        "PRODUCT_CATEGORY": "HERBS",
        "PRODUCT_STATUS": "ACTIVE",
        "transitions": [
            {"type": "PRODUCT_STATUS", "from": "PENDING", "to": "APPROVED"}
        ]
    }
    """
    results = {}
    errors = []
    
    # 验证基本枚举值
    for enum_type, value in validation_data.items():
        if enum_type == "transitions":
            continue
            
        is_valid = EnumManager.validate_enum_value(enum_type, value)
        results[f"{enum_type}_{value}"] = is_valid
        
        if not is_valid:
            errors.append(f"无效的{enum_type}值: {value}")
    
    # 验证状态转换
    transitions = validation_data.get("transitions", [])
    for transition in transitions:
        enum_type = transition.get("type")
        from_state = transition.get("from")
        to_state = transition.get("to")
        
        if enum_type and from_state and to_state:
            can_transition = EnumManager.can_transition_to(enum_type, from_state, to_state)
            results[f"transition_{enum_type}_{from_state}_to_{to_state}"] = can_transition
            
            if not can_transition:
                errors.append(f"无效的状态转换: {from_state} -> {to_state}")
    
    return success_response(
        data={
            "validationResults": results,
            "hasErrors": len(errors) > 0,
            "errors": errors
        },
        message="枚举值验证完成"
    )