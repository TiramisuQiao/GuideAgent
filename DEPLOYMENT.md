# 部署指南 - Deployment Guide

本文档提供米塔视界销售策略AI代理的完整部署指南。

## 🚀 快速部署

### 自动部署（推荐）

使用自动部署脚本，支持三种部署方式：

```bash
./deploy.sh
```

脚本会引导您选择：
1. **Docker部署**（推荐生产环境）
2. **本地uv部署**（推荐开发环境）
3. **Systemd服务部署**（推荐Linux服务器）

## 📦 部署方式详解

### 方式1：Docker部署（推荐）

#### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

#### 部署步骤

1. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，添加OpenRouter API密钥
nano .env
```

2. **构建并启动**
```bash
docker-compose up -d
```

3. **查看状态**
```bash
docker-compose ps
docker-compose logs -f
```

4. **访问应用**
打开浏览器访问: http://localhost:8501

#### 管理命令

```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 更新应用
git pull
docker-compose build
docker-compose up -d
```

### 方式2：本地uv部署

#### 前置要求
- Python 3.8+
- uv包管理器（脚本会自动安装）

#### 部署步骤

1. **安装uv（如未安装）**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

2. **配置环境**
```bash
cp .env.example .env
nano .env  # 添加API密钥
```

3. **安装依赖**
```bash
uv sync
```

4. **启动应用**
```bash
./run_web.sh
# 或
uv run streamlit run web_app.py
```

### 方式3：Systemd服务部署（Linux服务器）

适合需要后台运行和开机自启的生产环境。

#### 部署步骤

1. **使用部署脚本**
```bash
./deploy.sh
# 选择选项3
```

2. **手动部署（可选）**

创建服务文件 `/etc/systemd/system/mita-sales-agent.service`:

```ini
[Unit]
Description=米塔视界销售策略AI代理
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/GuideAgent
Environment="PATH=/home/YOUR_USERNAME/.cargo/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/YOUR_USERNAME/.cargo/bin/uv run streamlit run web_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start mita-sales-agent
sudo systemctl enable mita-sales-agent
```

#### 管理命令

```bash
# 查看状态
sudo systemctl status mita-sales-agent

# 查看日志
sudo journalctl -u mita-sales-agent -f

# 重启服务
sudo systemctl restart mita-sales-agent

# 停止服务
sudo systemctl stop mita-sales-agent

# 禁用自启
sudo systemctl disable mita-sales-agent
```

## 🌐 生产环境部署建议

### 使用Nginx反向代理

1. **安装Nginx**
```bash
sudo apt install nginx  # Ubuntu/Debian
sudo yum install nginx  # CentOS/RHEL
```

2. **配置反向代理**

创建 `/etc/nginx/sites-available/mita-sales-agent`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

3. **启用配置**
```bash
sudo ln -s /etc/nginx/sites-available/mita-sales-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 配置HTTPS（推荐）

使用Let's Encrypt免费证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 配置防火墙

```bash
# 允许HTTP/HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 🔧 OpenRouter配置

### 获取API密钥

1. 访问 https://openrouter.ai/keys
2. 注册或登录账号
3. 创建新的API密钥
4. 复制密钥到`.env`文件

### 推荐模型配置

在`.env`文件中配置：

```env
# 高质量输出（推荐）
MODEL_NAME=openai/gpt-4

# 平衡性能与成本
MODEL_NAME=openai/gpt-4-turbo

# 经济型选择
MODEL_NAME=openai/gpt-3.5-turbo

# Claude模型
MODEL_NAME=anthropic/claude-3-opus

# Gemini模型
MODEL_NAME=google/gemini-pro
```

### 成本优化建议

1. **开发环境**：使用`gpt-3.5-turbo`
2. **生产环境**：使用`gpt-4`或`gpt-4-turbo`
3. **高并发场景**：考虑添加缓存机制

## 📊 监控和日志

### Docker环境

```bash
# 实时查看日志
docker-compose logs -f

# 查看特定时间的日志
docker-compose logs --since 1h

# 导出日志
docker-compose logs > logs.txt
```

### Systemd环境

```bash
# 实时查看日志
sudo journalctl -u mita-sales-agent -f

# 查看最近的日志
sudo journalctl -u mita-sales-agent -n 100

# 导出日志
sudo journalctl -u mita-sales-agent > logs.txt
```

## 🔒 安全建议

1. **保护API密钥**
   - 不要将`.env`文件提交到版本控制
   - 使用环境变量或密钥管理服务
   - 定期轮换API密钥

2. **网络安全**
   - 使用HTTPS
   - 配置防火墙
   - 使用Nginx限制访问速率

3. **访问控制**
   - 考虑添加基础认证
   - 使用VPN或IP白名单
   - 配置CORS策略

## 🔄 更新和维护

### 更新应用

```bash
# 拉取最新代码
git pull

# Docker部署
docker-compose build
docker-compose up -d

# Systemd部署
uv sync
sudo systemctl restart mita-sales-agent
```

### 备份

建议定期备份：
- `.env`配置文件
- 日志文件
- 自定义修改的代码

## ❓ 常见问题

### Q: 端口已被占用？
**A:** 修改`docker-compose.yml`或启动命令中的端口：
```yaml
ports:
  - "8502:8501"  # 使用8502端口
```

### Q: 内存不足？
**A:** 调整Docker资源限制：
```yaml
services:
  mita-sales-agent:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Q: OpenRouter API调用失败？
**A:** 检查：
1. API密钥是否正确
2. 账户余额是否充足
3. 网络连接是否正常
4. 查看日志获取详细错误信息

### Q: 服务启动失败？
**A:** 检查：
1. `.env`文件是否存在且配置正确
2. 端口是否被占用
3. 查看日志获取错误信息
4. 确认依赖是否正确安装

## 📧 技术支持

遇到部署问题？
- 查看日志文件
- 检查配置文件
- 参考主文档`README.md`
- 联系技术支持团队

---

**部署愉快！🚀**
