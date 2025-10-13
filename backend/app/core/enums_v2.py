"""
重构版枚举管理系统 - 统一所有枚举定义和状态机
"""
from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class EnumItem:
    """枚举项配置"""
    code: str
    zh: str
    en: str
    description: str = ""
    order: int = 0
    next_states: List[str] = None
    required_permissions: List[str] = None
    color: str = "#409EFF"  # UI显示颜色
    
    def __post_init__(self):
        if self.next_states is None:
            self.next_states = []
        if self.required_permissions is None:
            self.required_permissions = []


class EnumConfig:
    """统一枚举配置管理"""
    
    # 商品分类
    PRODUCT_CATEGORIES = [
        EnumItem("HERBS", "中药材", "Herbs", "传统中药材料", 1, color="#67C23A"),
        EnumItem("WELLNESS", "养生产品", "Wellness Products", "养生保健产品", 2, color="#E6A23C"),
        EnumItem("MEDICAL_DEVICE", "医疗器械", "Medical Device", "医疗相关器械", 3, color="#F56C6C"),
        EnumItem("HEALTH_FOOD", "保健食品", "Health Food", "保健功能食品", 4, color="#909399"),
        EnumItem("TCM_BOOKS", "中医书籍", "TCM Books", "中医药相关书籍", 5, color="#606266"),
        EnumItem("ACCESSORIES", "配套用品", "Accessories", "相关配套用品", 6, color="#C0C4CC"),
    ]
    
    # 商品状态（完整状态机）
    PRODUCT_STATUSES = [
        EnumItem("DRAFT", "草稿", "Draft", "商品草稿状态", 1, 
                next_states=["PENDING"], color="#909399"),
        EnumItem("PENDING", "待审核", "Pending Review", "等待管理员审核", 2, 
                next_states=["APPROVED", "REJECTED"], color="#E6A23C"),
        EnumItem("APPROVED", "审核通过", "Approved", "管理员审核通过", 3, 
                next_states=["ACTIVE", "INACTIVE"], color="#67C23A"),
        EnumItem("REJECTED", "审核拒绝", "Rejected", "管理员审核拒绝", 4, 
                next_states=["PENDING"], color="#F56C6C"),
        EnumItem("ACTIVE", "在售", "Active", "商品正在销售", 5, 
                next_states=["INACTIVE", "OUT_OF_STOCK"], color="#409EFF"),
        EnumItem("INACTIVE", "下架", "Inactive", "商品已下架", 6, 
                next_states=["ACTIVE"], color="#C0C4CC"),
        EnumItem("OUT_OF_STOCK", "缺货", "Out of Stock", "商品库存不足", 7, 
                next_states=["ACTIVE", "INACTIVE"], color="#F56C6C"),
    ]
    
    # 审核状态
    AUDIT_STATUSES = [
        EnumItem("DRAFT", "草稿", "Draft", "草稿状态", 0,
                next_states=["PENDING"], color="#909399"),
        EnumItem("PENDING", "待审核", "Pending", "等待审核", 1,
                next_states=["APPROVED", "REJECTED"], color="#E6A23C"),
        EnumItem("APPROVED", "已通过", "Approved", "审核通过", 2,
                next_states=[], color="#67C23A"),
        EnumItem("REJECTED", "已拒绝", "Rejected", "审核拒绝", 3,
                next_states=["PENDING"], color="#F56C6C"),
    ]
    
    # 订单状态
    ORDER_STATUSES = [
        EnumItem("PENDING", "待付款", "Pending Payment", "等待用户付款", 1, 
                next_states=["PAID", "CANCELLED"], color="#E6A23C"),
        EnumItem("PAID", "已付款", "Paid", "用户已付款", 2, 
                next_states=["SHIPPED", "CANCELLED"], color="#67C23A"),
        EnumItem("SHIPPED", "已发货", "Shipped", "商品已发货", 3, 
                next_states=["DELIVERED", "RETURNED"], color="#409EFF"),
        EnumItem("DELIVERED", "已送达", "Delivered", "商品已送达", 4, 
                next_states=["COMPLETED", "RETURNED"], color="#67C23A"),
        EnumItem("COMPLETED", "已完成", "Completed", "订单完成", 5, 
                next_states=[], color="#909399"),
        EnumItem("CANCELLED", "已取消", "Cancelled", "订单已取消", 6, 
                next_states=[], color="#F56C6C"),
        EnumItem("RETURNED", "已退货", "Returned", "商品已退货", 7, 
                next_states=[], color="#C0C4CC"),
    ]
    
    # 用户角色
    USER_ROLES = [
        EnumItem("USER", "普通用户", "User", "普通注册用户", 1, color="#409EFF"),
        EnumItem("VIP", "VIP用户", "VIP", "VIP用户", 2, color="#67C23A"),
        EnumItem("DOCTOR", "医生", "Doctor", "医生用户", 3, color="#E6A23C"),
        EnumItem("EXPERT", "专家", "Expert", "医疗健康专家", 4, color="#67C23A"),
        EnumItem("ADMIN", "管理员", "Admin", "系统管理员", 5, color="#E6A23C"),
        EnumItem("SUPER_ADMIN", "超级管理员", "Super Admin", "超级管理员", 6, color="#F56C6C"),
    ]

    # 用户状态
    USER_STATUSES = [
        EnumItem("ACTIVE", "活跃", "Active", "用户状态正常", 1, color="#67C23A"),
        EnumItem("INACTIVE", "非活跃", "Inactive", "用户暂时非活跃", 2, color="#E6A23C"),
        EnumItem("SUSPENDED", "暂停", "Suspended", "用户被暂停", 3, color="#F56C6C"),
        EnumItem("BANNED", "封禁", "Banned", "用户被封禁", 4, color="#F56C6C"),
    ]

    # 专家分类
    EXPERT_CATEGORIES = [
        EnumItem("INTERNAL", "中医内科", "Internal Medicine", "中医内科专家", 1, color="#67C23A"),
        EnumItem("GYNECOLOGY", "中医妇科", "Gynecology", "中医妇科专家", 2, color="#E6A23C"),
        EnumItem("PEDIATRICS", "中医儿科", "Pediatrics", "中医儿科专家", 3, color="#409EFF"),
        EnumItem("ACUPUNCTURE", "针灸推拿", "Acupuncture", "针灸推拿专家", 4, color="#F56C6C"),
        EnumItem("HEALTH", "中医养生", "Health", "中医养生专家", 5, color="#909399"),
        EnumItem("TCM", "传统中医", "TCM", "传统中医专家", 6, color="#606266"),
        EnumItem("ORTHOPEDICS", "中医骨科", "Orthopedics", "中医骨科专家", 7, color="#C0C4CC"),
        EnumItem("DERMATOLOGY", "中医皮肤科", "Dermatology", "中医皮肤科专家", 8, color="#67C23A"),
    ]

    # 专家级别
    EXPERT_LEVELS = [
        EnumItem("JUNIOR", "初级医师", "Junior", "初级医师", 1, color="#E6A23C"),
        EnumItem("INTERMEDIATE", "中级医师", "Intermediate", "中级医师", 2, color="#409EFF"),
        EnumItem("SENIOR", "高级医师", "Senior", "高级医师", 3, color="#67C23A"),
        EnumItem("CHIEF", "主任医师", "Chief", "主任医师", 4, color="#F56C6C"),
    ]

    # 专家状态
    EXPERT_STATUSES = [
        EnumItem("ACTIVE", "在线服务", "Active", "专家在线服务", 1,
                next_states=["INACTIVE"], color="#67C23A"),
        EnumItem("INACTIVE", "暂停服务", "Inactive", "专家暂停服务", 2,
                next_states=["ACTIVE", "PENDING"], color="#C0C4CC"),
        EnumItem("PENDING", "待审核", "Pending", "专家资质待审核", 3,
                next_states=["ACTIVE", "REJECTED"], color="#E6A23C"),
        EnumItem("REJECTED", "审核未通过", "Rejected", "专家审核未通过", 4,
                next_states=["PENDING"], color="#F56C6C"),
    ]

    # 课程分类
    COURSE_CATEGORIES = [
        EnumItem("THEORY", "理论基础", "Theory", "中医理论基础课程", 1, color="#409EFF"),
        EnumItem("CLINICAL", "临床实践", "Clinical", "临床实践课程", 2, color="#67C23A"),
        EnumItem("WELLNESS", "养生保健", "Wellness", "养生保健课程", 3, color="#E6A23C"),
        EnumItem("ACUPUNCTURE", "针灸推拿", "Acupuncture", "针灸推拿课程", 4, color="#F56C6C"),
        EnumItem("PHARMACY", "中药方剂", "Pharmacy", "中药方剂课程", 5, color="#909399"),
        EnumItem("DISEASE_SPECIFIC", "逐病精讲", "Disease Specific", "逐病精讲课程", 6, color="#606266"),
        EnumItem("COMPREHENSIVE", "全面学医", "Comprehensive", "全面学医课程", 7, color="#C0C4CC"),
    ]

    # 视频状态
    VIDEO_STATUSES = [
        EnumItem("UPLOADING", "上传中", "Uploading", "视频上传中", 1,
                next_states=["PROCESSING", "ERROR"], color="#E6A23C"),
        EnumItem("PROCESSING", "处理中", "Processing", "视频处理中", 2,
                next_states=["READY", "ERROR"], color="#409EFF"),
        EnumItem("READY", "可播放", "Ready", "视频可播放", 3,
                next_states=[], color="#67C23A"),
        EnumItem("ERROR", "处理失败", "Error", "视频处理失败", 4,
                next_states=["UPLOADING"], color="#F56C6C"),
    ]

    # 咨询类型
    CONSULTATION_TYPES = [
        EnumItem("AI", "AI咨询", "AI Consultation", "人工智能咨询", 1, color="#409EFF"),
        EnumItem("TEXT", "文字咨询", "Text", "文字在线咨询", 2, color="#67C23A"),
        EnumItem("VOICE", "语音咨询", "Voice", "语音通话咨询", 3, color="#E6A23C"),
        EnumItem("VIDEO", "视频咨询", "Video", "视频通话咨询", 4, color="#F56C6C"),
    ]

    # 咨询状态
    CONSULTATION_STATUSES = [
        EnumItem("PENDING", "等待中", "Pending", "等待专家接受", 1,
                next_states=["ONGOING", "CANCELLED", "EXPIRED"], color="#E6A23C"),
        EnumItem("ONGOING", "进行中", "Ongoing", "咨询进行中", 2,
                next_states=["COMPLETED", "CANCELLED"], color="#409EFF"),
        EnumItem("COMPLETED", "已完成", "Completed", "咨询已完成", 3,
                next_states=[], color="#67C23A"),
        EnumItem("CANCELLED", "已取消", "Cancelled", "咨询已取消", 4,
                next_states=[], color="#F56C6C"),
        EnumItem("EXPIRED", "已过期", "Expired", "咨询已过期", 5,
                next_states=[], color="#C0C4CC"),
    ]

    # 支付状态
    PAYMENT_STATUSES = [
        EnumItem("PENDING", "待支付", "Pending", "等待支付", 1,
                next_states=["SUCCESS", "FAILED", "CANCELLED"], color="#E6A23C"),
        EnumItem("SUCCESS", "支付成功", "Success", "支付成功", 2,
                next_states=["REFUNDED"], color="#67C23A"),
        EnumItem("FAILED", "支付失败", "Failed", "支付失败", 3,
                next_states=["PENDING"], color="#F56C6C"),
        EnumItem("CANCELLED", "已取消", "Cancelled", "支付已取消", 4,
                next_states=[], color="#C0C4CC"),
        EnumItem("REFUNDED", "已退款", "Refunded", "支付已退款", 5,
                next_states=[], color="#909399"),
    ]


class EnumManager:
    """枚举管理器 - 提供枚举操作方法"""
    
    @staticmethod
    def get_enum_items(enum_type: str) -> List[EnumItem]:
        """获取指定类型的枚举项"""
        enum_map = {
            "PRODUCT_CATEGORY": EnumConfig.PRODUCT_CATEGORIES,
            "PRODUCT_STATUS": EnumConfig.PRODUCT_STATUSES,
            "AUDIT_STATUS": EnumConfig.AUDIT_STATUSES,
            "ORDER_STATUS": EnumConfig.ORDER_STATUSES,
            "USER_ROLE": EnumConfig.USER_ROLES,
            "USER_STATUS": EnumConfig.USER_STATUSES,
            "EXPERT_CATEGORY": EnumConfig.EXPERT_CATEGORIES,
            "EXPERT_LEVEL": EnumConfig.EXPERT_LEVELS,
            "EXPERT_STATUS": EnumConfig.EXPERT_STATUSES,
            "COURSE_CATEGORY": EnumConfig.COURSE_CATEGORIES,
            "VIDEO_STATUS": EnumConfig.VIDEO_STATUSES,
            "CONSULTATION_TYPE": EnumConfig.CONSULTATION_TYPES,
            "CONSULTATION_STATUS": EnumConfig.CONSULTATION_STATUSES,
            "PAYMENT_STATUS": EnumConfig.PAYMENT_STATUSES,
        }
        return enum_map.get(enum_type, [])
    
    @staticmethod
    def get_enum_dict(enum_type: str) -> Dict[str, EnumItem]:
        """获取枚举字典（code -> EnumItem）"""
        items = EnumManager.get_enum_items(enum_type)
        return {item.code: item for item in items}
    
    @staticmethod
    def get_enum_label(enum_type: str, code: str) -> str:
        """获取枚举显示标签"""
        enum_dict = EnumManager.get_enum_dict(enum_type)
        return enum_dict.get(code, EnumItem(code, code, code)).zh
    
    @staticmethod
    def get_next_states(enum_type: str, current_state: str) -> List[str]:
        """获取状态机的下一步可选状态"""
        enum_dict = EnumManager.get_enum_dict(enum_type)
        current_item = enum_dict.get(current_state)
        return current_item.next_states if current_item else []
    
    @staticmethod
    def can_transition_to(enum_type: str, from_state: str, to_state: str) -> bool:
        """检查状态转换是否合法"""
        next_states = EnumManager.get_next_states(enum_type, from_state)
        return to_state in next_states
    
    @staticmethod
    def validate_enum_value(enum_type: str, value: str) -> bool:
        """验证枚举值是否有效"""
        enum_dict = EnumManager.get_enum_dict(enum_type)
        return value in enum_dict
    
    @staticmethod
    def get_all_enum_codes(enum_type: str) -> List[str]:
        """获取所有枚举代码"""
        items = EnumManager.get_enum_items(enum_type)
        return [item.code for item in items]


# 为了向后兼容，保留原有的Enum类
class ProductCategory(str, Enum):
    HERBS = "HERBS"
    WELLNESS = "WELLNESS"
    MEDICAL_DEVICE = "MEDICAL_DEVICE"
    HEALTH_FOOD = "HEALTH_FOOD"
    TCM_BOOKS = "TCM_BOOKS"
    ACCESSORIES = "ACCESSORIES"


class ProductStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class AuditStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class UserRole(str, Enum):
    USER = "USER"
    VIP = "VIP"
    DOCTOR = "DOCTOR"
    EXPERT = "EXPERT"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


class ExpertCategory(str, Enum):
    INTERNAL = "INTERNAL"
    GYNECOLOGY = "GYNECOLOGY"
    PEDIATRICS = "PEDIATRICS"
    ACUPUNCTURE = "ACUPUNCTURE"
    HEALTH = "HEALTH"
    TCM = "TCM"
    ORTHOPEDICS = "ORTHOPEDICS"
    DERMATOLOGY = "DERMATOLOGY"


class ExpertLevel(str, Enum):
    JUNIOR = "JUNIOR"
    INTERMEDIATE = "INTERMEDIATE"
    SENIOR = "SENIOR"
    CHIEF = "CHIEF"


class ExpertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class CourseCategory(str, Enum):
    THEORY = "THEORY"
    CLINICAL = "CLINICAL"
    WELLNESS = "WELLNESS"
    ACUPUNCTURE = "ACUPUNCTURE"
    PHARMACY = "PHARMACY"
    DISEASE_SPECIFIC = "DISEASE_SPECIFIC"
    COMPREHENSIVE = "COMPREHENSIVE"


class VideoStatus(str, Enum):
    UPLOADING = "UPLOADING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    ERROR = "ERROR"


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class ConsultationType(str, Enum):
    AI = "AI"
    TEXT = "TEXT"
    VOICE = "VOICE"
    VIDEO = "VIDEO"


class ConsultationStatus(str, Enum):
    PENDING = "PENDING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class PaymentMethod(str, Enum):
    ALIPAY = "ALIPAY"
    WECHAT_PAY = "WECHAT_PAY"
    BANK_CARD = "BANK_CARD"
    BALANCE = "BALANCE"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"