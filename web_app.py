"""
米塔视界销售策略AI代理 - Web界面
基于Streamlit的交互式Web应用
"""

import streamlit as st
from sales_agent import MiTaSalesAgent
import os


def init_agent():
    """初始化代理"""
    try:
        if 'agent' not in st.session_state:
            st.session_state.agent = MiTaSalesAgent()
        return True
    except ValueError as e:
        st.error(f"❌ 初始化失败: {e}")
        st.info("请确保已配置.env文件并设置OPENAI_API_KEY")
        return False


def main():
    st.set_page_config(
        page_title="米塔视界销售策略AI助手",
        page_icon="🤖",
        layout="wide"
    )
    
    # 标题
    st.title("🤖 米塔视界销售策略AI助手")
    st.markdown("---")
    
    # 侧边栏 - 公司信息
    with st.sidebar:
        st.header("🏢 公司信息")
        st.markdown("""
        **公司名称：** 米塔视界
        
        **核心技术：**
        - 空间智能交互技术
        - 裸眼3D显示技术
        - 无介质空中成像技术
        
        **成功案例：**
        - 美的(Midea)
        - 四川大学博物馆
        - 央视《焦点访谈》报道
        """)
        
        st.markdown("---")
        st.info("💡 请在右侧描述观察到的客户特征，系统将生成针对性推荐策略")
    
    # 初始化代理
    if not init_agent():
        return
    
    # 主界面
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 客户观察输入")
        
        # 选择输入模式
        input_mode = st.radio(
            "选择输入模式：",
            ["完整描述", "结构化输入"],
            horizontal=True
        )
        
        if input_mode == "完整描述":
            observation = st.text_area(
                "请描述您观察到的客户：",
                height=250,
                placeholder="例如：目标是一位看起来像企业高管的中年男士，身穿西装，表情严肃。他没有停留，但走过时明显放慢了脚步..."
            )
            
            if st.button("🚀 生成策略", type="primary", use_container_width=True):
                if observation.strip():
                    with st.spinner("正在分析客户并生成策略..."):
                        try:
                            strategy = st.session_state.agent.analyze_customer(
                                full_observation=observation
                            )
                            st.session_state.strategy = strategy
                        except Exception as e:
                            st.error(f"生成策略时出错: {e}")
                else:
                    st.warning("请输入客户观察描述！")
        
        else:  # 结构化输入
            st.markdown("**请分别描述客户的三个维度：**")
            
            facial_expression = st.text_input(
                "👀 神态表情",
                placeholder="例如：眉头紧锁、表情好奇、面带微笑"
            )
            
            body_language = st.text_area(
                "🤸 身体动作",
                height=100,
                placeholder="例如：驻足观看、用手机拍照、与同伴讨论"
            )
            
            verbal_communication = st.text_area(
                "💬 语言交流",
                height=100,
                placeholder="例如：'哇，这是什么技术？'、'这个能用来做什么？'"
            )
            
            if st.button("🚀 生成策略", type="primary", use_container_width=True):
                if facial_expression or body_language or verbal_communication:
                    with st.spinner("正在分析客户并生成策略..."):
                        try:
                            strategy = st.session_state.agent.analyze_customer(
                                facial_expression=facial_expression or None,
                                body_language=body_language or None,
                                verbal_communication=verbal_communication or None
                            )
                            st.session_state.strategy = strategy
                        except Exception as e:
                            st.error(f"生成策略时出错: {e}")
                else:
                    st.warning("请至少填写一个观察维度！")
    
    with col2:
        st.header("📊 针对性推荐策略")
        
        if 'strategy' in st.session_state:
            # 显示策略
            st.markdown(st.session_state.strategy)
            
            # 复制按钮
            st.download_button(
                label="📋 下载策略",
                data=st.session_state.strategy,
                file_name="sales_strategy.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("👈 请在左侧输入客户观察信息并点击'生成策略'按钮")
    
    # 快速示例
    st.markdown("---")
    st.header("💡 快速示例")
    
    examples = {
        "企业高管": {
            "observation": "目标是一位看起来像企业高管的中年男士，身穿西装，表情严肃。他没有停留，但走过时明显放慢了脚步，侧头看了一眼我们的空中成像设备，并对旁边的助理低声说了一句'这个有点意思'。"
        },
        "科技爱好者": {
            "facial": "眼睛发亮，表情兴奋，嘴角上扬",
            "body": "立即驻足观看，拿出手机拍照，不断指着设备与朋友讨论",
            "verbal": "'哇，这太酷了！这是用什么原理实现的？能买吗？'"
        },
        "怀疑客户": {
            "facial": "眉头微皱，表情质疑",
            "body": "双手抱胸，站在远处观望",
            "verbal": "'又是噱头吧，这种东西实用吗？价格肯定很贵。'"
        },
        "家长客户": {
            "facial": "面带微笑，温和友善",
            "body": "牵着孩子的手，孩子兴奋地指着屏幕，家长弯腰倾听孩子说话",
            "verbal": "孩子说：'妈妈快看！图像在空中！' 家长回应：'是挺有意思的。'"
        }
    }
    
    cols = st.columns(4)
    for idx, (name, data) in enumerate(examples.items()):
        with cols[idx]:
            if st.button(f"📌 {name}", use_container_width=True):
                if "observation" in data:
                    st.session_state.example_data = {
                        "mode": "完整描述",
                        "observation": data["observation"]
                    }
                else:
                    st.session_state.example_data = {
                        "mode": "结构化输入",
                        "facial": data.get("facial", ""),
                        "body": data.get("body", ""),
                        "verbal": data.get("verbal", "")
                    }
                st.rerun()


if __name__ == "__main__":
    main()
