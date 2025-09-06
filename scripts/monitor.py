#!/usr/bin/env python3
"""
系统监控脚本
"""
import psutil
import requests
import time
import logging
import json
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        self.api_url = "http://localhost:8000/api/health"
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'response_time': 5.0  # 秒
        }
    
    def check_system_resources(self):
        """检查系统资源使用情况"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 网络IO
            net_io = psutil.net_io_counters()
            
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_total': memory.total // (1024**3),  # GB
                'memory_used': memory.used // (1024**3),   # GB
                'disk_percent': disk_percent,
                'disk_total': disk.total // (1024**3),     # GB
                'disk_used': disk.used // (1024**3),       # GB
                'network_bytes_sent': net_io.bytes_sent,
                'network_bytes_recv': net_io.bytes_recv
            }
            
            # 检查阈值
            alerts = []
            if cpu_percent > self.alert_thresholds['cpu_percent']:
                alerts.append(f"CPU使用率过高: {cpu_percent:.1f}%")
            
            if memory_percent > self.alert_thresholds['memory_percent']:
                alerts.append(f"内存使用率过高: {memory_percent:.1f}%")
            
            if disk_percent > self.alert_thresholds['disk_percent']:
                alerts.append(f"磁盘使用率过高: {disk_percent:.1f}%")
            
            if alerts:
                logger.warning("系统资源警告: " + ", ".join(alerts))
            else:
                logger.info(f"系统状态正常 - CPU: {cpu_percent:.1f}%, 内存: {memory_percent:.1f}%, 磁盘: {disk_percent:.1f}%")
            
            return stats, alerts
            
        except Exception as e:
            logger.error(f"系统资源检查失败: {e}")
            return None, [str(e)]
    
    def check_api_health(self):
        """检查API健康状态"""
        try:
            start_time = time.time()
            response = requests.get(self.api_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                if response_time > self.alert_thresholds['response_time']:
                    logger.warning(f"API响应时间过长: {response_time:.2f}s")
                else:
                    logger.info(f"API健康检查通过 - 响应时间: {response_time:.2f}s")
                
                return {
                    'status': 'healthy',
                    'response_time': response_time,
                    'status_code': response.status_code
                }
            else:
                logger.error(f"API健康检查失败 - 状态码: {response.status_code}")
                return {
                    'status': 'unhealthy',
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
                
        except requests.RequestException as e:
            logger.error(f"API健康检查异常: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_docker_containers(self):
        """检查Docker容器状态"""
        try:
            import docker
            client = docker.from_env()
            
            containers_info = []
            for container in client.containers.list(all=True):
                info = {
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else 'unknown'
                }
                containers_info.append(info)
                
                if container.status != 'running':
                    logger.warning(f"容器 {container.name} 状态异常: {container.status}")
                else:
                    logger.info(f"容器 {container.name} 运行正常")
            
            return containers_info
            
        except ImportError:
            logger.info("Docker SDK未安装，跳过容器检查")
            return None
        except Exception as e:
            logger.error(f"Docker容器检查失败: {e}")
            return None
    
    def save_metrics(self, data):
        """保存监控指标到文件"""
        try:
            metrics_file = Path("logs/metrics.jsonl")
            with open(metrics_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"保存监控指标失败: {e}")
    
    def run_check(self):
        """执行一次完整的监控检查"""
        logger.info("开始系统监控检查")
        
        # 系统资源检查
        system_stats, system_alerts = self.check_system_resources()
        
        # API健康检查
        api_status = self.check_api_health()
        
        # Docker容器检查
        container_status = self.check_docker_containers()
        
        # 汇总监控数据
        monitor_data = {
            'timestamp': datetime.now().isoformat(),
            'system': system_stats,
            'api': api_status,
            'containers': container_status,
            'alerts': system_alerts
        }
        
        # 保存监控数据
        self.save_metrics(monitor_data)
        
        logger.info("监控检查完成")
        return monitor_data

def main():
    """主函数"""
    monitor = SystemMonitor()
    
    try:
        # 创建日志目录
        Path("logs").mkdir(exist_ok=True)
        
        if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
            # 守护进程模式，每60秒检查一次
            logger.info("启动监控守护进程")
            while True:
                monitor.run_check()
                time.sleep(60)
        else:
            # 单次检查模式
            result = monitor.run_check()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    except KeyboardInterrupt:
        logger.info("监控程序被用户中断")
    except Exception as e:
        logger.error(f"监控程序异常: {e}")

if __name__ == "__main__":
    import sys
    main()