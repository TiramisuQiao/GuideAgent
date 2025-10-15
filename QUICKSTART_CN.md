# 快速开始指南

## 🚀 三步开始使用

### 第一步：安装uv和依赖

推荐使用uv包管理器（比pip更快更可靠）：

```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# 同步依赖
uv sync
```

或使用传统pip方式：
```bash
pip install -r requirements.txt
```

### 第二步：配置OpenRouter API密钥

1. 获取API密钥：
   - 访问 https://openrouter.ai/keys
   - 注册或登录账号
   - 创建新的API密钥

2. 复制配置文件模板：
```bash
cp .env.example .env
```

3. 编辑 `.env` 文件，填入你的OpenRouter API密钥：
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx  # 你的OpenRouter密钥
OPENAI_API_BASE=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4
```

> 💡 **为什么用OpenRouter？**
> - 支持多种AI模型（GPT-4、Claude、Gemini等）
> - 国内访问更稳定
> - 价格透明，按需付费
> - 统一接口，方便切换模型

### 第三步：运行应用

#### 推荐方式1：使用启动脚本

最简单的方式，会自动检查uv和依赖：

```bash
./run_web.sh
```

#### 推荐方式2：使用uv直接运行

```bash
uv run streamlit run web_app.py
```

#### 传统方式：直接运行

```bash
streamlit run web_app.py
```

然后在浏览器中打开显示的地址（通常是 http://localhost:8501）

#### 命令行测试

```bash
# 使用uv运行（推荐）
uv run python sales_agent.py
uv run python example_usage.py

# 或传统方式
python sales_agent.py
python example_usage.py
```

#### 一键部署（生产环境）

支持Docker、本地uv、Systemd三种部署方式：

```bash
./deploy.sh
# 按提示选择部署方式
```

## 📝 使用说明

### Web界面使用

1. 打开浏览器访问应用
2. 左侧输入客户观察信息（可以选择"完整描述"或"结构化输入"模式）
3. 点击"生成策略"按钮
4. 右侧会显示生成的针对性推荐策略
5. 可以点击"下载策略"保存结果

### 快速示例按钮

Web界面底部提供了4个快速示例：
- 📌 企业高管
- 📌 科技爱好者
- 📌 怀疑客户
- 📌 家长客户

点击任意按钮可快速加载示例数据进行测试。

### Python代码调用

```python
from sales_agent import MiTaSalesAgent

# 初始化代理
agent = MiTaSalesAgent()

# 方法1：完整描述
strategy = agent.analyze_customer(
    full_observation="客户是一位中年男士，身穿西装..."
)

# 方法2：结构化输入
strategy = agent.analyze_customer(
    facial_expression="表情严肃",
    body_language="放慢脚步，侧头观看",
    verbal_communication="'这个有点意思'"
)

print(strategy)
```

## ❓ 常见问题

### Q: 出现"未找到API密钥"错误？
**A:** 请确保已创建 `.env` 文件并正确配置了 `OPENAI_API_KEY`。

### Q: 如何切换到其他AI模型？
**A:** 在 `.env` 文件中修改 `MODEL_NAME`：
- `MODEL_NAME=openai/gpt-4` - GPT-4（推荐，质量最高）
- `MODEL_NAME=openai/gpt-4-turbo` - GPT-4 Turbo（更快）
- `MODEL_NAME=openai/gpt-3.5-turbo` - GPT-3.5（经济型）
- `MODEL_NAME=anthropic/claude-3-opus` - Claude 3
- `MODEL_NAME=google/gemini-pro` - Gemini Pro

### Q: Web界面无法启动？
**A:** 
1. 确保已安装依赖：`uv sync` 或 `pip install streamlit`
2. 检查端口是否被占用
3. 查看错误日志

### Q: 生成速度很慢？
**A:** 
- 检查网络连接（OpenRouter服务器状态）
- 切换到更快的模型：`MODEL_NAME=openai/gpt-4-turbo`
- 或使用经济型模型：`MODEL_NAME=openai/gpt-3.5-turbo`

### Q: 想要定制提示词？
**A:** 编辑 `sales_agent.py` 文件中的 `SALES_PROMPT_TEMPLATE` 常量。

### Q: 如何在生产环境部署？
**A:** 运行 `./deploy.sh` 并选择合适的部署方式，详见 `DEPLOYMENT.md` 文档。

### Q: uv命令找不到？
**A:** 
1. 安装uv：`curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 加载环境：`source $HOME/.cargo/env`
3. 或将 `$HOME/.cargo/bin` 添加到PATH

## 📧 技术支持

遇到问题？请查看完整的 `README.md` 文档或联系技术支持团队。

---

**祝使用愉快！🎉**
