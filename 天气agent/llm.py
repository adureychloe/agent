from openai import OpenAI
# main.py
import os
from dotenv import load_dotenv  # 仅开发环境需要
from weather import get_weather
from search_attraction import get_attraction
from instruction_tp import AGENT_SYSTEM_PROMPT

# 加载 .env 文件（仅本地开发时使用）
load_dotenv()

available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

class OpenAICompatibleClient:
    """
    一个用于调用任何兼容OpenAI接口的LLM服务的客户端。
    """
    def __init__(self, model: str,  api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def generate(self, prompt: str, system_prompt:str) -> str:
        """
        调用LLM服务生成响应。

        :param prompt: 用户输入的提示。
        :param system_prompt: 系统指令，用于引导模型行为。
        :return: LLM生成的响应文本。
        """
        print('正在调用大语言模型...')
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            anwser = response.choices[0].message.content
            print('大语言模型调用成功。')
            return anwser
        except Exception as e:
            print(f"调用LLM api时出错: {e}")
            return "错误：调用语言模型时出错"
        


