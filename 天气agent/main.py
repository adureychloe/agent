from openai import OpenAI
# main.py
import os
from dotenv import load_dotenv  # 仅开发环境需要
from weather import get_weather
from search_attraction import get_attraction
from instruction_tp import AGENT_SYSTEM_PROMPT
from llm import OpenAICompatibleClient
# 加载 .env 文件（仅本地开发时使用）
load_dotenv()

available_tools = { 
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

import re
import os

# ---1. 配置LLM客户端---

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")  # 设置Tavily API Key环境变量

llm = OpenAICompatibleClient(
    model=os.getenv("MODEL_ID"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# ---2. 初始化---
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个旅游景点。"
prompt_history = [f"用户请求：{user_prompt}"]

print(f"用户输入：{user_prompt}\n" + "="*40)

# ---3. 运行主循环 ---
for i in range(5): # 最大循环次数
    print(f"--- 循环 {i+1} ---\n")

    # 3.1 构建Prompt
    full_prompt = "\n".join(prompt_history)

    # 3.2 调用LLM
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    # 模型可能会输出多余的Thought-Action，因此需要截断
    match = re.search(r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)", llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print('已截断多余的Thought-Action对')
    print(f"LLM输出：\n{llm_output}\n")
    prompt_history.append(llm_output)

    # 3.3 解析LLM输出
    action_match = re.search(r"Action:\s*(.*)", llm_output,re.DOTALL)
    if not action_match:
        print("解析错误：未找到Action")
        break
    action_str = action_match.group(1).strip()
    print(f"解析到的Action：{action_str}\n")

    if action_str.startswith("finish"):
        final_answer = re.search(r'finish\(answer="(.*)"\)', action_str).group(1)
        print("任务完成，退出循环。")
        print(f"最终答案：{final_answer}")
        break
    
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误：未定义的工具 '{tool_name}'"

    # 3.4 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)

    