"""
示例：如何使用米塔视界销售策略AI代理
"""

from sales_agent import MiTaSalesAgent


def example_1_full_observation():
    """示例1：使用完整的观察描述"""
    print("\n" + "=" * 80)
    print("示例1：企业高管客户")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    observation = """
    目标是一位看起来像企业高管的中年男士，身穿西装，表情严肃。
    他没有停留，但走过时明显放慢了脚步，侧头看了一眼我们的空中成像设备，
    并对旁边的助理低声说了一句'这个有点意思'。
    """
    
    result = agent.analyze_customer(full_observation=observation)
    print(result)


def example_2_structured_input():
    """示例2：使用结构化的三维度输入"""
    print("\n" + "=" * 80)
    print("示例2：年轻科技爱好者")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    result = agent.analyze_customer(
        facial_expression="眼睛发亮，表情兴奋，嘴角上扬",
        body_language="立即驻足观看，拿出手机拍照，不断指着设备与朋友讨论",
        verbal_communication="'哇，这太酷了！这是用什么原理实现的？能买吗？'"
    )
    print(result)


def example_3_skeptical_customer():
    """示例3：持怀疑态度的客户"""
    print("\n" + "=" * 80)
    print("示例3：持怀疑态度的客户")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    result = agent.analyze_customer(
        facial_expression="眉头微皱，表情质疑",
        body_language="双手抱胸，站在远处观望",
        verbal_communication="'又是噱头吧，这种东西实用吗？价格肯定很贵。'"
    )
    print(result)


def example_4_family_visitor():
    """示例4：家庭访客"""
    print("\n" + "=" * 80)
    print("示例4：带孩子的家长")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    result = agent.analyze_customer(
        facial_expression="面带微笑，温和友善",
        body_language="牵着孩子的手，孩子兴奋地指着屏幕，家长弯腰倾听孩子说话",
        verbal_communication="孩子说：'妈妈快看！图像在空中！' 家长回应：'是挺有意思的。'"
    )
    print(result)


def example_5_dict_input():
    """示例5：使用字典输入"""
    print("\n" + "=" * 80)
    print("示例5：使用字典输入 - 博物馆策展人")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    customer_data = {
        "facial_expression": "专注认真，若有所思",
        "body_language": "缓慢靠近，仔细观察设备细节，拿出笔记本记录",
        "verbal_communication": "'这个技术能应用在文化展览上吗？维护成本怎么样？'"
    }
    
    result = agent.analyze_customer_dict(customer_data)
    print(result)


def interactive_mode():
    """交互模式：允许用户输入自定义观察"""
    print("\n" + "=" * 80)
    print("交互模式：自定义客户观察")
    print("=" * 80 + "\n")
    
    agent = MiTaSalesAgent()
    
    print("请描述您观察到的客户特征：")
    print("-" * 80)
    
    facial = input("神态表情 (按回车跳过): ").strip()
    body = input("身体动作 (按回车跳过): ").strip()
    verbal = input("语言交流 (按回车跳过): ").strip()
    
    if not facial and not body and not verbal:
        print("\n请至少提供一项观察信息！")
        return
    
    print("\n正在生成策略...\n")
    
    result = agent.analyze_customer(
        facial_expression=facial or None,
        body_language=body or None,
        verbal_communication=verbal or None
    )
    
    print("\n" + "=" * 80)
    print(result)
    print("=" * 80)


if __name__ == "__main__":
    try:
        # 运行所有示例
        print("\n🚀 米塔视界销售策略AI代理 - 使用示例\n")
        
        # 运行预设示例
        example_1_full_observation()
        example_2_structured_input()
        example_3_skeptical_customer()
        example_4_family_visitor()
        example_5_dict_input()
        
        # 询问是否进入交互模式
        print("\n" + "=" * 80)
        response = input("\n是否进入交互模式进行自定义测试？(y/n): ").strip().lower()
        if response == 'y':
            interactive_mode()
        
        print("\n✓ 所有示例运行完成！\n")
        
    except ValueError as e:
        print(f"\n✗ 错误: {e}")
        print("请确保已创建.env文件并配置了OPENAI_API_KEY\n")
    except KeyboardInterrupt:
        print("\n\n程序已退出。\n")
