#!/bin/bash
# 提交前字段一致性检查脚本

echo "=== 提交前字段一致性检查 ==="

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# 1. 运行字段检查脚本
echo "1. 检查字段一致性..."
python scripts/simple_field_check.py > /tmp/field_check.log 2>&1

# 检查是否有明显的不匹配问题
if grep -q "错误\|失败\|不匹配" /tmp/field_check.log; then
    echo "❌ 发现潜在的字段不匹配问题"
    echo "详细信息:"
    cat /tmp/field_check.log
    echo ""
    echo "建议:"
    echo "1. 检查 docs/FIELD_MAPPING.md 文档"
    echo "2. 运行 'python scripts/simple_field_check.py' 查看详细报告"
    echo "3. 修复不匹配的字段后重新提交"
    exit 1
fi

# 2. 检查是否有未跟踪的重要文件
echo "2. 检查重要文件状态..."

# 检查是否有未提交的枚举定义文件
IMPORTANT_FILES=(
    "backend/app/models/user.py"
    "backend/app/models/course.py"
    "backend/app/models/product.py"
    "backend/app/schemas/user.py"
    "backend/app/schemas/course.py"
    "backend/app/schemas/product.py"
    "frontend/src/views/admin/UserManagement.vue"
    "frontend/src/views/admin/CourseManagement.vue"
    "frontend/src/views/admin/ProductManagement.vue"
)

UNCOMMITTED_CHANGES=0
for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ] && git diff --quiet HEAD "$file" 2>/dev/null; then
        :  # 文件没有改动，继续检查下一个
    elif [ -f "$file" ]; then
        echo "   发现未提交的改动: $file"
        UNCOMMITTED_CHANGES=1
    fi
done

# 3. 基本语法检查
echo "3. 基本语法检查..."

# 检查Python语法（如果有Python文件）
echo "   检查Python语法..."
for py_file in $(find backend -name "*.py" 2>/dev/null | head -10); do
    if [ -f "$py_file" ]; then
        python -m py_compile "$py_file" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌ Python语法错误: $py_file"
            python -m py_compile "$py_file"
            exit 1
        fi
    fi
done

# 检查Vue文件基本语法
echo "   检查Vue文件基本结构..."
for vue_file in $(find frontend/src -name "*.vue" 2>/dev/null | head -10); do
    if [ -f "$vue_file" ]; then
        # 检查基本的Vue文件结构
        if ! grep -q "<template>" "$vue_file" || ! grep -q "</template>" "$vue_file"; then
            echo "⚠️  Vue文件可能缺少template标签: $vue_file"
        fi
    fi
done

# 4. 文档更新检查
echo "4. 检查文档更新..."

# 如果有枚举相关文件存在，提示检查文档更新
ENUM_FILES_CHANGED=0
for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ]; then
        ENUM_FILES_CHANGED=1
        break
    fi
done

if [ $ENUM_FILES_CHANGED -eq 1 ]; then
    echo "   检测到枚举相关文件有改动，请确认："
    echo "   - 是否需要更新 docs/FIELD_MAPPING.md ?"
    echo "   - 是否需要更新 docs/ENUM_STANDARDS.md ?"
    echo "   - 是否需要更新API文档?"
fi

# 最终结果
echo ""
if [ $UNCOMMITTED_CHANGES -eq 1 ]; then
    echo "⚠️  发现未提交的重要文件改动，请检查是否需要一起提交"
fi

echo "✅ 提交前检查完成"
echo ""
echo "提示:"
echo "- 如果修改了枚举值，请运行 'python scripts/simple_field_check.py' 进行详细检查"
echo "- 请确保前后端测试通过后再部署"
echo "- 生产部署前建议运行完整的集成测试"

exit 0