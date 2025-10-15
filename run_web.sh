#!/bin/bash

# 米塔视界销售策略AI代理 - Web应用启动脚本

echo "========================================"
echo "米塔视界销售策略AI助手 - Web界面"
echo "========================================"
echo ""

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "⚠️  警告：未安装uv包管理器"
    echo "正在安装uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo "✓ uv安装完成，请重新运行此脚本"
    echo "或者手动运行: source $HOME/.cargo/env"
    exit 0
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo "⚠️  警告：未找到.env文件"
    echo "请先复制.env.example为.env并配置API密钥："
    echo "  cp .env.example .env"
    echo "  然后编辑.env文件添加您的OpenRouter API密钥"
    echo ""
    echo "获取API密钥: https://openrouter.ai/keys"
    echo ""
    read -p "是否现在创建.env文件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✓ .env文件已创建，请编辑该文件添加您的API密钥"
        echo ""
        exit 0
    else
        exit 1
    fi
fi

# 使用uv同步依赖
echo "📦 检查并安装依赖..."
uv sync

# 启动应用
echo ""
echo "🚀 启动Web应用..."
echo "应用将在浏览器中自动打开"
echo "按 Ctrl+C 停止服务"
echo ""

uv run streamlit run web_app.py
