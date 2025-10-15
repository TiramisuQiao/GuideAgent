# 米塔视界销售策略AI代理

基于LangChain构建的智能销售策略助手，为"米塔视界"的线下展示店推销人员提供实时、个性化的客户互动策略。

> 🚀 **最新更新**：项目已升级支持 `uv` 包管理器和 `OpenRouter` API！[查看更新说明](UPDATE_SUMMARY.md)

## ⚡ 超快速开始

```bash
# 一键自动设置（推荐）
./setup.sh

# 或手动设置
curl -LsSf https://astral.sh/uv/install.sh | sh  # 安装uv
source $HOME/.cargo/env
uv sync                                          # 安装依赖
cp .env.example .env                              # 配置文件
# 编辑.env添加OpenRouter API密钥（https://openrouter.ai/keys）
./run_web.sh                                      # 启动应用
```

## 🌟 功能特性

- **实时客户分析**：根据客户的神态表情、身体动作和语言交流快速生成客户画像
- **个性化策略**：为每位客户量身定制互动开场白、推销术语和肢体语言建议
- **多种输入方式**：支持完整描述、结构化输入、字典输入等多种使用方式
- **吸引人的语音播报**：接入 MiniMax TTS，将策略结果实时转换成充满感染力的语音
- **Web界面**：提供直观的Streamlit Web界面，方便非技术人员使用
- **基于LangChain**：利用LangChain框架，易于扩展和集成

## 📋 前置要求

- Python 3.8+
- uv包管理器（推荐）或pip
- OpenRouter API密钥（推荐）或其他LLM服务API密钥

## 🚀 快速开始

### 1. 安装uv和依赖

推荐使用uv包管理器（更快、更可靠）：

```bash
# 安装uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# 同步依赖
uv sync
```

或使用传统pip方式：
```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

1. 获取API密钥：访问 https://openrouter.ai/keys 注册并创建密钥

2. 配置环境变量：
```bash
cp .env.example .env
```

3. 编辑`.env`文件，添加你的OpenRouter API密钥与 MiniMax TTS 密钥：
```env
OPENAI_API_KEY=sk-or-v1-xxxxx  # 你的OpenRouter API密钥
OPENAI_API_BASE=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4

# MiniMax TTS 语音配置
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_TTS_VOICE=female-qn-fantasy
MINIMAX_TTS_SPEED=1.05
```

### 3. 运行应用

#### 方式1：Web界面（推荐）

```bash
# 使用启动脚本（推荐，会自动检查uv和依赖）
./run_web.sh

# 或使用uv直接运行
uv run streamlit run web_app.py

# 或使用传统方式
streamlit run web_app.py
```

然后在浏览器中访问显示的URL（通常是 http://localhost:8501）

#### 方式2：命令行

```bash
# 使用uv运行示例
uv run python sales_agent.py
uv run python example_usage.py

# 或使用传统方式
python sales_agent.py
python example_usage.py
```

#### 方式3：一键部署

支持Docker、本地uv、Systemd三种部署方式：
```bash
./deploy.sh
```

详见 [DEPLOYMENT.md](DEPLOYMENT.md) 部署文档

## 💡 使用方法

### 方法1：完整描述输入

```python
from sales_agent import MiTaSalesAgent

agent = MiTaSalesAgent()

observation = """
目标是一位看起来像企业高管的中年男士，身穿西装，表情严肃。
他没有停留，但走过时明显放慢了脚步，侧头看了一眼我们的空中成像设备，
并对旁边的助理低声说了一句'这个有点意思'。
"""

strategy = agent.analyze_customer(full_observation=observation)
print(strategy)
```

### 方法2：结构化三维度输入

```python
from sales_agent import MiTaSalesAgent

agent = MiTaSalesAgent()

strategy = agent.analyze_customer(
    facial_expression="眼睛发亮，表情兴奋，嘴角上扬",
    body_language="立即驻足观看，拿出手机拍照，不断指着设备与朋友讨论",
    verbal_communication="'哇，这太酷了！这是用什么原理实现的？能买吗？'"
)
print(strategy)
```

### 方法3：字典输入

```python
from sales_agent import MiTaSalesAgent

agent = MiTaSalesAgent()

customer_data = {
    "facial_expression": "专注认真，若有所思",
    "body_language": "缓慢靠近，仔细观察设备细节，拿出笔记本记录",
    "verbal_communication": "'这个技术能应用在文化展览上吗？维护成本怎么样？'"
}

strategy = agent.analyze_customer_dict(customer_data)
print(strategy)
```

### 方法4：生成语音播报

```python
from sales_agent import MiTaSalesAgent

agent = MiTaSalesAgent(enable_tts=True)

result = agent.analyze_customer(
    facial_expression="眼神炯炯有神，充满好奇",
    body_language="围着设备转圈，频频点头示意",
    verbal_communication="'这体验太酷了，能不能马上试试看？'",
    with_voice=True,
    voice_params={
        "voice_id": "female-qn-fantasy",
        "emotion": "energetic",
        "speed": 1.05,
    },
)

audio_bytes = result["audio_bytes"]
with open("strategy_voice.mp3", "wb") as file:
    file.write(audio_bytes)

print(result["voiceover_script"])
```

### 方法4：自定义LLM配置

```python
from sales_agent import MiTaSalesAgent

# 使用自定义配置
agent = MiTaSalesAgent(
    api_key="your_api_key",
    base_url="https://your-api-endpoint.com/v1",
    model_name="gpt-4-turbo"
)

strategy = agent.analyze_customer(full_observation="客户描述...")
print(strategy)
```

## 📊 输出格式

代理将生成包含以下四个部分的"针对性推荐策略"报告：

### 1. 客户画像速写
快速分析并判断该客户可能的身份背景、潜在需求和兴趣点。

### 2. 互动开场白
提供1-2句最能吸引该客户注意力的开场白。

### 3. 核心推销术语与讲解重点
- 列出2-3个最适合对该客户使用的核心技术术语
- 简述应该侧重讲解的技术优势或应用场景

### 4. 建议音色与肢体动作
- **音色**：描述讲解时应该使用的语气和语速
- **动作**：描述最能增强说服力的肢体语言

## 🏢 公司背景（内置于提示词）

- **公司名称**：米塔视界
- **核心技术**：空间智能交互技术、裸眼3D显示技术、无介质空中成像技术
- **产品**：AI驱动的软硬一体化空间交互系统
- **成功案例**：美的(Midea)、四川大学博物馆"波斯文化艺术展"、央视《焦点访谈》报道
- **使命**：推动数字世界与物理世界的深度融合

## 📁 项目结构

```
GuideAgent/
├── sales_agent.py          # 主代理类（核心LangChain实现）
├── web_app.py             # Streamlit Web界面
├── example_usage.py        # 命令行使用示例
├── run_web.sh             # Web应用启动脚本
├── deploy.sh              # 一键部署脚本
├── pyproject.toml         # uv项目配置文件
├── requirements.txt        # Python依赖包（pip兼容）
├── Dockerfile             # Docker部署配置
├── docker-compose.yml     # Docker Compose配置
├── .dockerignore          # Docker忽略文件
├── .env.example           # 环境变量示例
├── .env                   # 环境变量配置（需自行创建）
├── .gitignore            # Git忽略文件
├── README.md              # 项目文档
├── QUICKSTART_CN.md       # 快速开始指南（中文）
└── DEPLOYMENT.md          # 部署文档
```

## 🌐 OpenRouter配置说明

本项目默认使用OpenRouter作为AI模型提供商，原因如下：

### 为什么选择OpenRouter？

- ✅ **多模型支持**：统一接口访问GPT-4、Claude、Gemini等多种模型
- ✅ **价格透明**：按实际使用付费，无需包月订阅
- ✅ **国内友好**：相比OpenAI官方API，访问更稳定
- ✅ **易于切换**：通过修改MODEL_NAME即可切换模型
- ✅ **无需VPN**：直接访问，无需额外配置

### 支持的模型

在`.env`文件中配置`MODEL_NAME`：

```env
# OpenAI模型
MODEL_NAME=openai/gpt-4              # 推荐，质量最高
MODEL_NAME=openai/gpt-4-turbo        # 更快更便宜
MODEL_NAME=openai/gpt-3.5-turbo      # 最经济

# Anthropic Claude模型
MODEL_NAME=anthropic/claude-3-opus   # 高质量
MODEL_NAME=anthropic/claude-3-sonnet # 平衡型

# Google Gemini模型
MODEL_NAME=google/gemini-pro         # 谷歌最新模型
```

查看所有支持的模型：https://openrouter.ai/models

### 获取API密钥

1. 访问 https://openrouter.ai/keys
2. 注册或登录账号
3. 点击"Create Key"创建API密钥
4. 复制密钥（格式：`sk-or-v1-xxxx`）
5. 添加到`.env`文件的`OPENAI_API_KEY`

## 🔧 高级配置

### 使用uv包管理器

本项目推荐使用uv进行包管理：

```bash
# 安装依赖
uv sync

# 运行应用
uv run streamlit run web_app.py

# 运行Python脚本
uv run python sales_agent.py

# 添加新依赖
uv add package-name
```

### 直接使用OpenAI API

如果想使用OpenAI官方API（需要VPN），修改`.env`：

```env
OPENAI_API_KEY=sk-xxxxx
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4
```

### 自定义提示词

在`MiTaSalesAgent`类中修改`SALES_PROMPT_TEMPLATE`常量即可自定义提示词。

### 调整模型参数

在初始化LLM时调整参数：

```python
self.llm = ChatOpenAI(
    model=self.model_name,
    temperature=0.7,  # 创造性：0-2，越高越随机
    max_tokens=2000,  # 最大输出长度
    api_key=self.api_key,
)
```

## 🧪 测试场景

项目包含以下预设测试场景（见`example_usage.py`）：

1. **企业高管客户**：严肃、商务需求
2. **年轻科技爱好者**：兴奋、技术细节关注
3. **持怀疑态度客户**：质疑、需要说服
4. **带孩子的家长**：温和、教育娱乐需求
5. **博物馆策展人**：专业、应用场景关注

## 🛠️ 故障排除

### API密钥错误
```
ValueError: 未找到API密钥
```
**解决方案**：确保已创建`.env`文件并正确配置了`OPENAI_API_KEY`。

### 网络连接问题
如果使用OpenAI官方API遇到网络问题，可以配置代理或使用国内的API中转服务。

### 依赖版本冲突
```bash
pip install --upgrade -r requirements.txt
```

## 📝 注意事项

- 确保API密钥安全，不要将`.env`文件提交到版本控制系统
- 根据实际使用的LLM服务调整`temperature`等参数
- 首次运行可能需要下载模型，请耐心等待
- API调用会产生费用，请注意使用量

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请联系技术支持。

---

**Made with ❤️ for MiTa Vision (米塔视界)**
