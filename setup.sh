#!/bin/bash

# 米塔视界销售策略AI代理 - 自动化设置脚本
# MiTa Vision Sales Agent - Automated Setup Script

set -e

echo "============================================"
echo "米塔视界销售策略AI代理 - 自动化设置"
echo "MiTa Vision Sales Agent - Automated Setup"
echo "============================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 步骤1: 检查并安装uv
echo -e "${BLUE}[1/4] 检查uv包管理器...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv未安装，正在自动安装...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    source $HOME/.cargo/env
    echo -e "${GREEN}✓ uv安装成功！${NC}"
else
    echo -e "${GREEN}✓ uv已安装${NC}"
fi
echo ""

# 步骤2: 同步依赖
echo -e "${BLUE}[2/4] 安装Python依赖...${NC}"
uv sync
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# 步骤3: 配置环境变量
echo -e "${BLUE}[3/4] 配置环境变量...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ 已创建.env配置文件${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  重要：请编辑.env文件并添加您的API密钥${NC}"
    echo ""
    echo "步骤："
    echo "  1. 访问 https://openrouter.ai/keys"
    echo "  2. 注册并创建API密钥"
    echo "  3. 编辑 .env 文件，替换 OPENAI_API_KEY 的值"
    echo ""
    read -p "按回车键继续查看.env文件内容..." 
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat .env
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    read -p "是否现在编辑.env文件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo -e "${GREEN}✓ .env文件已存在${NC}"
fi
echo ""

# 步骤4: 验证配置
echo -e "${BLUE}[4/4] 验证配置...${NC}"

# 检查API密钥是否配置
if grep -q "your_openrouter_api_key_here" .env 2>/dev/null; then
    echo -e "${RED}✗ 警告：.env文件中的API密钥尚未配置${NC}"
    echo "  请编辑.env文件并添加有效的OpenRouter API密钥"
    echo ""
    SETUP_COMPLETE=false
else
    echo -e "${GREEN}✓ API密钥已配置${NC}"
    SETUP_COMPLETE=true
fi
echo ""

# 显示安装摘要
echo "============================================"
echo -e "${GREEN}安装完成！${NC}"
echo "============================================"
echo ""

if [ "$SETUP_COMPLETE" = true ]; then
    echo -e "${GREEN}✓ 所有配置已完成，可以开始使用！${NC}"
    echo ""
    echo "快速开始："
    echo "  ./run_web.sh                      # 启动Web界面"
    echo "  uv run python sales_agent.py      # 运行命令行示例"
    echo ""
    echo "部署到生产环境："
    echo "  ./deploy.sh                       # 一键部署脚本"
    echo ""
    echo "查看文档："
    echo "  cat README.md                     # 完整文档"
    echo "  cat QUICKSTART_CN.md              # 快速开始指南"
    echo "  cat DEPLOYMENT.md                 # 部署文档"
    echo ""
    
    read -p "是否现在启动Web应用？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "正在启动Web应用..."
        echo ""
        ./run_web.sh
    fi
else
    echo -e "${YELLOW}⚠️  请先完成以下步骤：${NC}"
    echo ""
    echo "1. 获取OpenRouter API密钥："
    echo "   访问 https://openrouter.ai/keys"
    echo ""
    echo "2. 编辑配置文件："
    echo "   nano .env"
    echo "   或"
    echo "   vim .env"
    echo ""
    echo "3. 将API密钥添加到OPENAI_API_KEY变量"
    echo ""
    echo "4. 运行应用："
    echo "   ./run_web.sh"
    echo ""
fi

echo "============================================"
echo "需要帮助？"
echo "  - 查看文档: cat README.md"
echo "  - 快速指南: cat QUICKSTART_CN.md"
echo "  - 更新说明: cat UPDATE_SUMMARY.md"
echo "============================================"
