#!/usr/bin/env python3
"""
前后端字段一致性检查脚本
用于检测和报告前后端数据字段的不匹配问题
"""

import os
import re
import json
from typing import Dict, List, Set, Any
from pathlib import Path

class FieldConsistencyChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "backend"
        self.frontend_root = self.project_root / "frontend"
        
        # 存储提取的枚举值
        self.backend_enums = {}
        self.frontend_enums = {}
        
        # 问题报告
        self.issues = []
        
    def extract_python_enums(self) -> Dict[str, Dict[str, List[str]]]:
        """提取Python文件中的枚举值"""
        enums = {}
        
        # 扫描models和schemas目录
        for folder in ["models", "schemas"]:
            folder_path = self.backend_root / "app" / folder
            if not folder_path.exists():
                continue
                
            enums[folder] = {}
            
            for py_file in folder_path.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                    
                try:
                    content = py_file.read_text(encoding='utf-8')
                    file_enums = self._parse_python_enums(content)
                    if file_enums:
                        enums[folder][py_file.stem] = file_enums
                except Exception as e:
                    print(f"读取文件失败 {py_file}: {e}")
                    
        return enums
    
    def _parse_python_enums(self, content: str) -> Dict[str, List[str]]:
        """解析Python代码中的枚举定义"""
        enums = {}
        
        # 匹配枚举类定义
        enum_pattern = r'class\s+(\w+)\s*\([^)]*Enum[^)]*\):[^}]*?(?=class\s+\w+|$)'
        enum_matches = re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in enum_matches:
            enum_name = match.group(1)
            enum_body = match.group(0)
            
            # 提取枚举值
            value_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
            values = []
            
            for value_match in re.finditer(value_pattern, enum_body):
                key = value_match.group(1)
                value = value_match.group(2)
                values.append(f"{key}={value}")
                
            if values:
                enums[enum_name] = values
                
        return enums
    
    def extract_vue_enums(self) -> Dict[str, Dict[str, List[str]]]:
        """提取Vue文件中的枚举值选项"""
        enums = {}
        
        # 扫描前端views目录
        views_path = self.frontend_root / "src" / "views"
        if not views_path.exists():
            return enums
            
        for vue_file in views_path.rglob("*.vue"):
            try:
                content = vue_file.read_text(encoding='utf-8')
                file_enums = self._parse_vue_enums(content, vue_file.name)
                if file_enums:
                    enums[vue_file.stem] = file_enums
            except Exception as e:
                print(f"⚠️ 读取文件失败 {vue_file}: {e}")
                
        return enums
    
    def _parse_vue_enums(self, content: str, filename: str) -> Dict[str, List[str]]:
        """解析Vue文件中的选项值"""
        enums = {}
        
        # 匹配el-option标签
        option_pattern = r'<el-option[^>]*label\s*=\s*["\']([^"\']+)["\'][^>]*value\s*=\s*["\']([^"\']+)["\'][^>]*/?>'
        option_matches = re.finditer(option_pattern, content, re.MULTILINE)
        
        options = []
        for match in option_matches:
            label = match.group(1)
            value = match.group(2)
            if value and value not in ["", "all"]:  # 过滤空值和通用选项
                options.append(f"{label}={value}")
        
        if options:
            enums[f"{filename}_options"] = options
            
        # 匹配el-radio标签
        radio_pattern = r'<el-radio[^>]*label\s*=\s*["\']([^"\']+)["\'][^>]*>([^<]+)</el-radio>'
        radio_matches = re.finditer(radio_pattern, content, re.MULTILINE)
        
        radios = []
        for match in radio_matches:
            value = match.group(1)
            label = match.group(2).strip()
            if value:
                radios.append(f"{label}={value}")
        
        if radios:
            enums[f"{filename}_radios"] = radios
            
        return enums
    
    def compare_enums(self):
        """比较前后端枚举值并生成报告"""
        print("开始字段一致性检查...")
        
        # 提取枚举值
        print("提取后端枚举值...")
        self.backend_enums = self.extract_python_enums()
        
        print("提取前端枚举值...")
        self.frontend_enums = self.extract_vue_enums()
        
        # 生成报告
        self._generate_report()
        
    def _generate_report(self):
        """生成检查报告"""
        print("\n" + "="*80)
        print("📊 前后端字段一致性检查报告")
        print("="*80)
        
        # 显示后端枚举
        print("\n🔹 后端枚举值:")
        for folder, files in self.backend_enums.items():
            print(f"\n📁 {folder}/")
            for file, enums in files.items():
                print(f"  📄 {file}.py:")
                for enum_name, values in enums.items():
                    print(f"    🔸 {enum_name}: {len(values)} 个值")
                    for value in values[:3]:  # 只显示前3个
                        print(f"      - {value}")
                    if len(values) > 3:
                        print(f"      ... 还有 {len(values) - 3} 个值")
        
        # 显示前端枚举
        print("\n🔹 前端枚举值:")
        for file, enums in self.frontend_enums.items():
            print(f"  📄 {file}.vue:")
            for enum_name, values in enums.items():
                print(f"    🔸 {enum_name}: {len(values)} 个值")
                for value in values[:3]:  # 只显示前3个
                    print(f"      - {value}")
                if len(values) > 3:
                    print(f"      ... 还有 {len(values) - 3} 个值")
        
        # 寻找潜在问题
        print("\n🚨 潜在问题分析:")
        self._analyze_issues()
        
    def _analyze_issues(self):
        """分析潜在的字段不匹配问题"""
        issues_found = False
        
        # 检查用户相关字段
        user_backend = self._get_enum_values("UserRole", "models", "user") + \
                      self._get_enum_values("UserStatus", "models", "user")
        user_frontend = self._get_frontend_values("UserManagement")
        
        if user_backend and user_frontend:
            backend_values = set([v.split('=')[1] for v in user_backend])
            frontend_values = set([v.split('=')[1] for v in user_frontend])
            
            missing_in_frontend = backend_values - frontend_values
            missing_in_backend = frontend_values - backend_values
            
            if missing_in_frontend or missing_in_backend:
                issues_found = True
                print("❌ 用户管理字段不匹配:")
                if missing_in_frontend:
                    print(f"   前端缺失: {missing_in_frontend}")
                if missing_in_backend:
                    print(f"   后端缺失: {missing_in_backend}")
        
        # 检查产品相关字段
        product_backend = self._get_enum_values("ProductStatus", "models", "product")
        product_frontend = self._get_frontend_values("ProductManagement")
        
        if product_backend and product_frontend:
            backend_values = set([v.split('=')[1] for v in product_backend])
            frontend_values = set([v.split('=')[1] for v in product_frontend])
            
            missing_in_frontend = backend_values - frontend_values
            missing_in_backend = frontend_values - backend_values
            
            if missing_in_frontend or missing_in_backend:
                issues_found = True
                print("❌ 产品管理字段不匹配:")
                if missing_in_frontend:
                    print(f"   前端缺失: {missing_in_frontend}")
                if missing_in_backend:
                    print(f"   后端缺失: {missing_in_backend}")
        
        # 检查课程相关字段
        course_backend = self._get_enum_values("CourseCategory", "models", "course")
        course_frontend = self._get_frontend_values("CourseManagement")
        
        if course_backend and course_frontend:
            backend_values = set([v.split('=')[1] for v in course_backend])
            frontend_values = set([v.split('=')[1] for v in course_frontend])
            
            missing_in_frontend = backend_values - frontend_values
            missing_in_backend = frontend_values - backend_values
            
            if missing_in_frontend or missing_in_backend:
                issues_found = True
                print("❌ 课程管理字段不匹配:")
                if missing_in_frontend:
                    print(f"   前端缺失: {missing_in_frontend}")
                if missing_in_backend:
                    print(f"   后端缺失: {missing_in_backend}")
        
        if not issues_found:
            print("✅ 未发现明显的字段不匹配问题")
        
        print("\n💡 建议:")
        print("1. 定期运行此脚本检查字段一致性")
        print("2. 在修改枚举值前先更新文档")
        print("3. 考虑建立统一的枚举值定义文件")
        print("4. 增加自动化测试验证字段匹配")
    
    def _get_enum_values(self, enum_name: str, folder: str, file: str) -> List[str]:
        """获取指定的后端枚举值"""
        try:
            return self.backend_enums.get(folder, {}).get(file, {}).get(enum_name, [])
        except:
            return []
    
    def _get_frontend_values(self, file: str) -> List[str]:
        """获取指定的前端枚举值"""
        all_values = []
        file_enums = self.frontend_enums.get(file, {})
        for enum_values in file_enums.values():
            all_values.extend(enum_values)
        return all_values
    
    def save_report(self, output_file: str = None):
        """保存报告到文件"""
        if not output_file:
            output_file = self.project_root / "reports" / "field_consistency_report.json"
            
        # 确保目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            "timestamp": "2025-09-06",
            "backend_enums": self.backend_enums,
            "frontend_enums": self.frontend_enums,
            "issues": self.issues
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
            
        print(f"\n📄 报告已保存到: {output_file}")

def main():
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"项目根目录: {project_root}")
    
    # 创建检查器
    checker = FieldConsistencyChecker(str(project_root))
    
    # 运行检查
    checker.compare_enums()
    
    # 保存报告
    checker.save_report()

if __name__ == "__main__":
    main()