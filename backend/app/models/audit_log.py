"""
审核日志模型
记录所有审核操作的历史
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # 被审核的实体信息
    entity_type = Column(String, nullable=False)  # course, expert, product
    entity_id = Column(Integer, nullable=False)   # 实体ID
    entity_title = Column(String)  # 实体标题/名称（冗余字段，便于查看）
    
    # 审核操作信息
    action = Column(String, nullable=False)  # submit, approve, reject, publish, offline
    old_status = Column(String)  # 原状态
    new_status = Column(String, nullable=False)  # 新状态
    
    # 操作人信息
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operator_name = Column(String, nullable=False)  # 操作人姓名（冗余字段）
    operator_role = Column(String)  # 操作人角色
    
    # 审核内容
    reason = Column(Text)  # 审核意见/拒绝原因
    attachment = Column(JSON)  # 附加信息（如：具体的修改建议）
    
    # 系统信息
    ip_address = Column(String)  # 操作IP
    user_agent = Column(String)  # 用户代理
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    operator = relationship("User")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, entity='{self.entity_type}:{self.entity_id}', action='{self.action}')>"

    class Config:
        """Pydantic配置"""
        from_attributes = True

    @property
    def entity_info(self):
        """返回实体信息的简要描述"""
        return f"{self.entity_type}#{self.entity_id}: {self.entity_title}"

    @property  
    def action_description(self):
        """返回操作描述"""
        action_map = {
            'submit': '提交审核',
            'approve': '审核通过', 
            'reject': '审核拒绝',
            'publish': '发布上线',
            'offline': '下架',
            'withdraw': '撤回'
        }
        return action_map.get(self.action, self.action)