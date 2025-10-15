#!/bin/bash

# 米塔视界销售策略AI代理 - 部署脚本

set -e

echo "========================================"
echo "米塔视界销售策略AI代理 - 自动部署"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${RED}✗ 错误：未找到.env文件${NC}"
    echo "请先创建.env文件并配置API密钥："
    echo "  cp .env.example .env"
    echo "  然后编辑.env文件添加您的OpenRouter API密钥"
    echo ""
    echo "获取API密钥: https://openrouter.ai/keys"
    exit 1
fi

# 选择部署方式
echo "请选择部署方式:"
echo "1) Docker部署（推荐）"
echo "2) 本地uv部署"
echo "3) Systemd服务部署"
echo ""
read -p "请输入选项 (1-3): " deploy_option

case $deploy_option in
    1)
        echo ""
        echo -e "${GREEN}==> Docker部署模式${NC}"
        echo ""
        
        # 检查Docker
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}✗ Docker未安装${NC}"
            echo "请先安装Docker: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        # 检查docker-compose
        if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
            echo -e "${RED}✗ Docker Compose未安装${NC}"
            echo "请先安装Docker Compose"
            exit 1
        fi
        
        echo "🐳 构建Docker镜像..."
        docker-compose build
        
        echo ""
        echo "🚀 启动容器..."
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✓ 部署完成！${NC}"
        echo ""
        echo "访问地址: http://localhost:8501"
        echo ""
        echo "管理命令:"
        echo "  查看日志: docker-compose logs -f"
        echo "  停止服务: docker-compose down"
        echo "  重启服务: docker-compose restart"
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}==> 本地uv部署模式${NC}"
        echo ""
        
        # 检查uv
        if ! command -v uv &> /dev/null; then
            echo "⚠️  未安装uv，正在安装..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            source $HOME/.cargo/env
        fi
        
        echo "📦 使用uv同步依赖..."
        uv sync
        
        echo ""
        echo "🚀 启动Web应用..."
        echo ""
        echo -e "${GREEN}✓ 依赖安装完成！${NC}"
        echo ""
        echo "运行命令启动应用:"
        echo "  ./run_web.sh"
        echo "或"
        echo "  uv run streamlit run web_app.py"
        ;;
        
    3)
        echo ""
        echo -e "${GREEN}==> Systemd服务部署模式${NC}"
        echo ""
        
        # 检查uv
        if ! command -v uv &> /dev/null; then
            echo "⚠️  未安装uv，正在安装..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            source $HOME/.cargo/env
        fi
        
        echo "📦 使用uv同步依赖..."
        uv sync
        
        # 获取当前路径
        CURRENT_DIR=$(pwd)
        CURRENT_USER=$(whoami)
        
        # 创建systemd服务文件
        echo ""
        echo "📝 创建systemd服务文件..."
        
        sudo tee /etc/systemd/system/mita-sales-agent.service > /dev/null <<EOF
[Unit]
Description=米塔视界销售策略AI代理
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$HOME/.cargo/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$(which uv) run streamlit run web_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        # 重载systemd配置
        echo "🔄 重载systemd配置..."
        sudo systemctl daemon-reload
        
        # 启动服务
        echo "🚀 启动服务..."
        sudo systemctl start mita-sales-agent
        
        # 设置开机自启
        echo "⚙️  设置开机自启..."
        sudo systemctl enable mita-sales-agent
        
        echo ""
        echo -e "${GREEN}✓ 部署完成！${NC}"
        echo ""
        echo "访问地址: http://localhost:8501"
        echo ""
        echo "管理命令:"
        echo "  查看状态: sudo systemctl status mita-sales-agent"
        echo "  查看日志: sudo journalctl -u mita-sales-agent -f"
        echo "  停止服务: sudo systemctl stop mita-sales-agent"
        echo "  重启服务: sudo systemctl restart mita-sales-agent"
        echo "  禁用自启: sudo systemctl disable mita-sales-agent"
        ;;
        
    *)
        echo -e "${RED}✗ 无效的选项${NC}"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "部署完成！感谢使用米塔视界AI助手"
echo "========================================"
