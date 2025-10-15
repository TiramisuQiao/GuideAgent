# 项目更新摘要 - Update Summary

## ✅ 完成的更新

本次更新已将项目升级为使用 **uv包管理器** 和 **OpenRouter API**，并添加了完整的部署支持。

---

## 🔄 主要变更

### 1. 包管理升级到uv

#### 新增文件
- ✅ `pyproject.toml` - uv项目配置文件

#### 修改内容
- 保留 `requirements.txt` 用于向后兼容
- 更新 `run_web.sh` 自动检查和使用uv
- 文档中推荐使用uv命令

#### 使用方法
```bash
# 安装uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖
uv sync

# 运行应用
uv run streamlit run web_app.py
```

---

### 2. 切换到OpenRouter API

#### 修改文件
- ✅ `.env.example` - 更新为OpenRouter配置模板
- ✅ `sales_agent.py` - 添加OpenRouter特定配置支持

#### 配置示例
```env
OPENAI_API_KEY=sk-or-v1-xxxxx
OPENAI_API_BASE=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4
```

#### OpenRouter优势
- ✅ 多模型支持（GPT-4、Claude、Gemini等）
- ✅ 国内访问友好，无需VPN
- ✅ 价格透明，按需付费
- ✅ 统一接口，易于切换

#### 获取API密钥
访问：https://openrouter.ai/keys

---

### 3. 完整部署支持

#### 新增文件
- ✅ `deploy.sh` - 一键部署脚本（支持3种部署方式）
- ✅ `Dockerfile` - Docker部署配置
- ✅ `docker-compose.yml` - Docker Compose配置
- ✅ `.dockerignore` - Docker构建忽略文件
- ✅ `DEPLOYMENT.md` - 完整部署文档

#### 支持的部署方式

**方式1：Docker部署（推荐生产环境）**
```bash
./deploy.sh
# 选择选项 1
```

**方式2：本地uv部署（推荐开发环境）**
```bash
./deploy.sh
# 选择选项 2
```

**方式3：Systemd服务（Linux服务器）**
```bash
./deploy.sh
# 选择选项 3
```

---

### 4. 文档更新

#### 更新的文档
- ✅ `README.md` - 主文档全面更新
- ✅ `QUICKSTART_CN.md` - 快速开始指南更新
- ✅ `DEPLOYMENT.md` - 新增部署文档

#### 文档改进
- 添加OpenRouter配置说明章节
- 添加uv使用说明
- 更新所有代码示例
- 添加部署最佳实践
- 更新常见问题解答

---

## 📂 完整项目结构

```
GuideAgent/
├── sales_agent.py          # 主代理类（已更新OpenRouter支持）
├── web_app.py             # Streamlit Web界面
├── example_usage.py        # 命令行使用示例
├── run_web.sh             # Web应用启动脚本（已更新）
├── deploy.sh              # 一键部署脚本（新增）
├── pyproject.toml         # uv项目配置文件（新增）
├── requirements.txt        # Python依赖包（兼容）
├── Dockerfile             # Docker部署配置（新增）
├── docker-compose.yml     # Docker Compose配置（新增）
├── .dockerignore          # Docker忽略文件（新增）
├── .env.example           # 环境变量示例（已更新）
├── .env                   # 环境变量配置（需自行创建）
├── .gitignore            # Git忽略文件
├── README.md              # 项目文档（已更新）
├── QUICKSTART_CN.md       # 快速开始指南（已更新）
├── DEPLOYMENT.md          # 部署文档（新增）
└── UPDATE_SUMMARY.md      # 本更新摘要（新增）
```

---

## 🚀 快速开始（更新后）

### 第一次使用

1. **安装uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

2. **配置API密钥**
```bash
cp .env.example .env
# 编辑.env，添加OpenRouter API密钥
```

3. **同步依赖**
```bash
uv sync
```

4. **启动应用**
```bash
./run_web.sh
```

### 一键部署（生产环境）

```bash
./deploy.sh
```

---

## 🔑 OpenRouter API使用指南

### 1. 注册和获取密钥

1. 访问 https://openrouter.ai
2. 注册或登录账号
3. 进入 https://openrouter.ai/keys
4. 点击 "Create Key" 创建API密钥
5. 复制密钥（格式：`sk-or-v1-xxxx`）

### 2. 配置密钥

编辑 `.env` 文件：
```env
OPENAI_API_KEY=sk-or-v1-your-actual-key-here
OPENAI_API_BASE=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4
```

### 3. 选择模型

根据需求选择合适的模型：

**高质量输出（推荐）**
```env
MODEL_NAME=openai/gpt-4
```

**平衡性能与成本**
```env
MODEL_NAME=openai/gpt-4-turbo
```

**经济型选择**
```env
MODEL_NAME=openai/gpt-3.5-turbo
```

**其他模型**
```env
MODEL_NAME=anthropic/claude-3-opus    # Claude 3
MODEL_NAME=google/gemini-pro          # Gemini Pro
```

查看所有模型：https://openrouter.ai/models

---

## 📊 费用说明

OpenRouter按实际使用量计费：

| 模型 | 每1000 tokens价格（输入/输出） |
|------|-------------------------------|
| GPT-4 | $0.03 / $0.06 |
| GPT-4 Turbo | $0.01 / $0.03 |
| GPT-3.5 Turbo | $0.0005 / $0.0015 |
| Claude 3 Opus | $0.015 / $0.075 |
| Gemini Pro | $0.000125 / $0.000375 |

*价格仅供参考，请访问 https://openrouter.ai/models 查看最新价格*

---

## 🔧 常见操作

### 更新依赖
```bash
uv sync --upgrade
```

### 添加新包
```bash
uv add package-name
```

### 查看已安装的包
```bash
uv pip list
```

### 切换模型
编辑 `.env` 文件中的 `MODEL_NAME`

### 查看日志（Docker部署）
```bash
docker-compose logs -f
```

### 重启服务（Systemd部署）
```bash
sudo systemctl restart mita-sales-agent
```

---

## ⚠️ 注意事项

### 兼容性
- 保留了 `requirements.txt`，仍可使用 `pip install -r requirements.txt`
- 所有旧的运行命令仍然有效
- 建议使用uv以获得更好的性能

### 安全性
- **不要**将 `.env` 文件提交到版本控制
- **不要**在代码中硬编码API密钥
- 定期更换API密钥

### 迁移
如果之前使用OpenAI官方API：
1. 修改 `.env` 中的 `OPENAI_API_BASE` 为 `https://openrouter.ai/api/v1`
2. 修改 `MODEL_NAME` 添加前缀，如 `openai/gpt-4`
3. 使用OpenRouter的API密钥

---

## 📚 相关文档

- [README.md](README.md) - 完整项目文档
- [QUICKSTART_CN.md](QUICKSTART_CN.md) - 快速开始指南
- [DEPLOYMENT.md](DEPLOYMENT.md) - 部署文档
- [OpenRouter文档](https://openrouter.ai/docs)
- [uv文档](https://github.com/astral-sh/uv)

---

## ✅ 验证安装

运行以下命令验证安装是否成功：

```bash
# 检查uv
uv --version

# 检查依赖
uv pip list

# 测试应用
uv run python sales_agent.py
```

---

## 🎉 完成！

现在你的项目已经：
- ✅ 使用uv包管理器（更快更可靠）
- ✅ 配置OpenRouter API（国内友好）
- ✅ 支持多种部署方式
- ✅ 文档完善更新

开始使用：
```bash
./run_web.sh
```

或部署到生产环境：
```bash
./deploy.sh
```

**祝使用愉快！🚀**

---

*更新时间：2025-10-15*
*版本：v1.0.0 (OpenRouter + uv)*
