"""
快递鸟物流查询API服务
官方文档: https://www.kdniao.com/documents
"""
import hashlib
import base64
import json
import httpx
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class KDNiaoConfig(BaseModel):
    """快递鸟配置"""
    ebusiness_id: str  # 商户ID
    app_key: str  # API密钥
    api_url: str = "http://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx"


class TrackingInfo(BaseModel):
    """物流轨迹信息"""
    time: str  # 时间
    context: str  # 描述
    location: Optional[str] = None  # 地点


class KDNiaoService:
    """快递鸟服务封装"""

    # 快递公司代码映射（快递鸟API代码）
    COURIER_CODE_MAP = {
        "SF": "SF",  # 顺丰速运
        "ZTO": "ZTO",  # 中通快递
        "YTO": "YTO",  # 圆通速递
        "STO": "STO",  # 申通快递
        "YD": "YD",  # 韵达快递
        "JTSD": "JTSD",  # 极兔速递
        "JD": "JD",  # 京东物流
        "EMS": "EMS",  # 邮政EMS
        "DBKD": "DBKD",  # 德邦快递
    }

    def __init__(self, config: KDNiaoConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()

    def _generate_sign(self, request_data: str) -> str:
        """
        生成数据签名
        签名规则: MD5(RequestData + AppKey)，然后Base64编码
        """
        sign_str = request_data + self.config.app_key
        md5_hash = hashlib.md5(sign_str.encode('utf-8')).digest()
        sign = base64.b64encode(md5_hash).decode('utf-8')
        return sign

    async def track_shipment(
        self,
        courier_code: str,
        tracking_number: str
    ) -> Dict:
        """
        查询物流轨迹

        Args:
            courier_code: 快递公司代码（我们自己的枚举值）
            tracking_number: 物流单号

        Returns:
            物流查询结果
        """
        # 转换为快递鸟的快递公司代码
        kdniao_courier_code = self.COURIER_CODE_MAP.get(courier_code, courier_code)

        # 构建请求数据
        request_data = {
            "OrderCode": "",  # 订单编号（可选）
            "ShipperCode": kdniao_courier_code,
            "LogisticCode": tracking_number
        }
        request_data_json = json.dumps(request_data, ensure_ascii=False)

        # 生成签名
        data_sign = self._generate_sign(request_data_json)

        # 构建POST请求参数
        post_data = {
            "RequestData": request_data_json,
            "EBusinessID": self.config.ebusiness_id,
            "RequestType": "1002",  # 即时查询类型
            "DataSign": data_sign,
            "DataType": "2"  # 返回JSON格式
        }

        try:
            # 发送请求
            response = await self.client.post(
                self.config.api_url,
                data=post_data
            )
            response.raise_for_status()

            # 解析响应
            result = response.json()
            return self._parse_tracking_response(result)

        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP请求失败: {str(e)}",
                "tracking_history": []
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"响应解析失败: {str(e)}",
                "tracking_history": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"查询失败: {str(e)}",
                "tracking_history": []
            }

    def _parse_tracking_response(self, response: Dict) -> Dict:
        """
        解析快递鸟API响应

        响应格式:
        {
            "Success": true,
            "EBusinessID": "1693946",
            "ShipperCode": "SF",
            "LogisticCode": "SF1234567890",
            "State": "3",  # 物流状态: 0-无轨迹, 1-已揽收, 2-在途中, 3-已签收, 4-问题件
            "Traces": [
                {
                    "AcceptTime": "2025-10-25 10:00:00",
                    "AcceptStation": "【北京市】快件已被【xxx】揽收",
                    "Remark": null
                }
            ]
        }
        """
        if not response.get("Success"):
            return {
                "success": False,
                "error": response.get("Reason", "查询失败"),
                "tracking_history": []
            }

        # 解析物流轨迹
        traces = response.get("Traces", [])
        tracking_history = []

        for trace in traces:
            tracking_history.append({
                "time": trace.get("AcceptTime", ""),
                "status": trace.get("AcceptStation", ""),
                "location": self._extract_location(trace.get("AcceptStation", ""))
            })

        # 判断配送状态
        state = response.get("State", "0")
        shipping_status = self._map_state_to_status(state)

        return {
            "success": True,
            "courier_code": response.get("ShipperCode"),
            "tracking_number": response.get("LogisticCode"),
            "state": state,
            "shipping_status": shipping_status,
            "tracking_history": tracking_history,
            "last_update": tracking_history[0]["time"] if tracking_history else None
        }

    def _extract_location(self, station_info: str) -> Optional[str]:
        """从物流描述中提取地点信息"""
        if "【" in station_info and "】" in station_info:
            start = station_info.find("【") + 1
            end = station_info.find("】")
            return station_info[start:end]
        return None

    def _map_state_to_status(self, state: str) -> str:
        """
        将快递鸟的状态映射到我们的ShippingStatus枚举

        快递鸟状态:
        0: 无轨迹 -> PENDING
        1: 已揽收 -> SHIPPED
        2: 在途中 -> IN_TRANSIT
        3: 已签收 -> DELIVERED
        4: 问题件 -> FAILED
        """
        mapping = {
            "0": "PENDING",
            "1": "SHIPPED",
            "2": "IN_TRANSIT",
            "3": "DELIVERED",
            "4": "FAILED"
        }
        return mapping.get(state, "PENDING")


# 全局服务实例（需要在应用启动时初始化）
kdniao_service: Optional[KDNiaoService] = None


def init_kdniao_service(ebusiness_id: str, app_key: str):
    """初始化快递鸟服务"""
    global kdniao_service
    config = KDNiaoConfig(
        ebusiness_id=ebusiness_id,
        app_key=app_key
    )
    kdniao_service = KDNiaoService(config)
    return kdniao_service


def get_kdniao_service() -> KDNiaoService:
    """获取快递鸟服务实例"""
    if kdniao_service is None:
        raise RuntimeError("快递鸟服务未初始化，请先调用 init_kdniao_service()")
    return kdniao_service
