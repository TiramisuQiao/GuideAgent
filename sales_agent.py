"""
米塔视界销售策略AI助手
Sales Strategy Agent for MiTa Vision using LangChain
"""

import os
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from tts import MiniMaxTTSClient, MiniMaxTTSError


class MiTaSalesAgent:
    """米塔视界销售策略AI代理"""
    
    # 完整的销售策略提示词模板
    SALES_PROMPT_TEMPLATE = """**角色扮演:**
你是一家名为"米塔视界"的前沿科技公司的王牌销售策略师。你的角色是实时指导一名线下展示店的推销人员，根据现场观察到的潜在客户信息，为其生成一套完整的、个性化的推荐与互动策略。

**公司背景:**
*   **公司名称:** 米塔视界
*   **核心技术:** 专注于"空间智能交互技术"，拥有自主研发的"裸眼3D显示技术"和"无介质空中成像技术"。
*   **产品:** AI驱动的软硬一体化空间交互系统，包括颠覆性的裸眼3D智能终端和可实现空中悬浮影像人机交互的空中成像设备。
*   **成功案例:** 已在广告零售（如美的Midea）、文旅（如四川大学博物馆"波斯文化艺术展"）等领域实现商业化落地，并获得过央视《焦点访谈》的报道。
*   **使命:** 推动数字世界与物理世界的深度融合。

**任务要求:**
我将以推销人员的身份，向你描述一位刚刚路过我们展台的潜在客户。我的描述将包含以下三个维度：
1.  **神态表情:** (例如：眉头紧锁、表情好奇、面带微笑、不屑一顾)
2.  **身体动作:** (例如：驻足观看、用手机拍照、指着屏幕、与同伴讨论、快步走过)
3.  **语言交流:** (例如："哇，这是什么技术？"、"这是全息投影吗？"、"这个能用来做什么？"、"看着挺贵的。")

根据我的描述，你必须立刻生成一份名为 **"针对性推荐策略"** 的报告，报告必须包含以下四个部分，并严格按照格式输出：

1.  **客户画像速写:**
    *   快速分析并判断该客户可能的身份背景、潜在需求和兴趣点。

2.  **互动开场白:**
    *   提供1-2句最能吸引该客户注意力的开场白。

3.  **核心推销术语与讲解重点:**
    *   列出2-3个最适合对该客户使用的核心技术术语（从公司背景中选取）。
    *   简述应该侧重讲解的技术优势或应用场景。

4.  **建议音色与肢体动作:**
    *   **音色:** 描述讲解时应该使用的语气和语速 (例如：专业稳重、热情洋溢、亲切温和)。
    *   **动作:** 描述最能增强说服力的肢体语言 (例如：用手引导视线、做出邀请体验的手势、身体微微前倾表示专注)。

---

**推销人员观察描述:**
{customer_observation}

**请立即生成针对性推荐策略:**"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model_name: str = "gpt-4",
        enable_tts: bool = False,
    ):
        """
        初始化销售策略代理
        
        Args:
            api_key: OpenAI API密钥
            base_url: API基础URL
            model_name: 使用的模型名称
        """
        # 加载环境变量
        load_dotenv()
        
        # 配置API
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_API_BASE")
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-4")
        
        if not self.api_key:
            raise ValueError("未找到API密钥。请设置OPENAI_API_KEY环境变量或在初始化时提供api_key参数。")
        
        # 初始化LLM
        llm_params = {
            "model": self.model_name,
            "temperature": 0.7,
            "api_key": self.api_key,
        }
        
        if self.base_url:
            llm_params["base_url"] = self.base_url
            
            # OpenRouter特定配置
            if "openrouter.ai" in self.base_url:
                app_name = os.getenv("OPENROUTER_APP_NAME", "MiTaVision-SalesAgent")
                app_url = os.getenv("OPENROUTER_APP_URL", "http://localhost:8501")
                llm_params["default_headers"] = {
                    "HTTP-Referer": app_url,
                    "X-Title": app_name,
                }
            
        self.llm = ChatOpenAI(**llm_params)
        
        # 创建提示词模板
        self.prompt = ChatPromptTemplate.from_template(self.SALES_PROMPT_TEMPLATE)
        
        # 构建链
        self.chain = self.prompt | self.llm | StrOutputParser()

        self._tts_client: Optional[MiniMaxTTSClient] = None
        if enable_tts:
            self._tts_client = self._init_tts_client()

    def _init_tts_client(self) -> MiniMaxTTSClient:
        try:
            return MiniMaxTTSClient()
        except MiniMaxTTSError as exc:
            raise MiniMaxTTSError("初始化 MiniMax TTS 客户端失败，请检查环境变量配置。") from exc

    def _get_tts_client(self) -> MiniMaxTTSClient:
        if self._tts_client is None:
            self._tts_client = self._init_tts_client()
        return self._tts_client

    def analyze_customer(
        self,
        facial_expression: str = None,
        body_language: str = None,
        verbal_communication: str = None,
        full_observation: str = None,
        *,
        with_voice: bool = False,
        voice_intro: Optional[str] = None,
        voice_outro: Optional[str] = None,
        voice_params: Optional[Dict[str, Union[str, float]]] = None,
    ) -> Union[str, Dict[str, Union[str, bytes, Dict[str, Any]]]]:
        """
        分析客户并生成针对性推荐策略
        
        Args:
            facial_expression: 神态表情描述
            body_language: 身体动作描述
            verbal_communication: 语言交流描述
            full_observation: 完整的客户观察描述（如果提供，则优先使用此项）
            with_voice: 是否需要同时生成吸引用户的语音稿及音频
            voice_intro: 自定义语音稿开场白
            voice_outro: 自定义语音稿收尾语
            voice_params: 传递给 TTS 客户端的额外参数（如 voice_id、speed 等）

        Returns:
            with_voice 为 False 时返回字符串；否则返回包含文本、语音稿和音频的字典
        """
        if full_observation:
            observation = full_observation
        else:
            # 组合各个维度的描述
            observation_parts = []
            if facial_expression:
                observation_parts.append(f"神态表情: {facial_expression}")
            if body_language:
                observation_parts.append(f"身体动作: {body_language}")
            if verbal_communication:
                observation_parts.append(f"语言交流: {verbal_communication}")
            
            if not observation_parts:
                raise ValueError("请至少提供一种客户观察描述")
            
            observation = "\n".join(observation_parts)
        
        # 调用链生成策略
        response = self.chain.invoke({
            "customer_observation": observation
        })

        if not with_voice:
            return response

        tts_client = self._get_tts_client()
        filtered_voice_params: Dict[str, Union[str, float]] = {}
        if voice_params:
            allowed = {"voice_id", "emotion", "speed", "pitch", "volume", "model", "response_format"}
            filtered_voice_params = {
                key: value for key, value in voice_params.items() if key in allowed
            }

        try:
            voice_result = tts_client.generate_voiceover(
                response,
                intro=voice_intro,
                outro=voice_outro,
                **filtered_voice_params,
            )
        except MiniMaxTTSError as exc:
            raise MiniMaxTTSError(f"语音生成失败: {exc}") from exc

        return {
            "strategy": response,
            "voiceover_script": voice_result["script"],
            "audio_bytes": voice_result["audio_bytes"],
            "tts_metadata": voice_result["metadata"],
        }
    
    def analyze_customer_dict(
        self,
        customer_data: Dict[str, str],
        *,
        with_voice: bool = False,
        voice_intro: Optional[str] = None,
        voice_outro: Optional[str] = None,
        voice_params: Optional[Dict[str, Union[str, float]]] = None,
    ) -> Union[str, Dict[str, Union[str, bytes, Dict[str, Any]]]]:
        """
        使用字典形式的客户数据生成策略
        
        Args:
            customer_data: 包含客户观察信息的字典
                可以包含 'facial_expression', 'body_language', 'verbal_communication', 'full_observation'
        
        Returns:
            生成的针对性推荐策略
        """
        return self.analyze_customer(
            facial_expression=customer_data.get("facial_expression"),
            body_language=customer_data.get("body_language"),
            verbal_communication=customer_data.get("verbal_communication"),
            full_observation=customer_data.get("full_observation"),
            with_voice=with_voice,
            voice_intro=voice_intro,
            voice_outro=voice_outro,
            voice_params=voice_params,
        )


def main():
    """示例用法"""
    print("=" * 80)
    print("米塔视界销售策略AI助手")
    print("=" * 80)
    print()
    
    # 初始化代理
    try:
        agent = MiTaSalesAgent()
        print("✓ AI代理初始化成功！\n")
    except ValueError as e:
        print(f"✗ 初始化失败: {e}")
        print("请创建.env文件并配置OPENAI_API_KEY")
        return
    
    # 示例客户观察
    example_observation = """
    目标是一位看起来像企业高管的中年男士，身穿西装，表情严肃。他没有停留，但走过时明显放慢了脚步，侧头看了一眼我们的空中成像设备，并对旁边的助理低声说了一句'这个有点意思'。
    """
    
    print("推销人员观察描述:")
    print("-" * 80)
    print(example_observation.strip())
    print("-" * 80)
    print()
    print("正在生成针对性推荐策略...\n")
    
    # 生成策略
    strategy = agent.analyze_customer(full_observation=example_observation)
    
    print("=" * 80)
    print(strategy)
    print("=" * 80)


if __name__ == "__main__":
    main()
