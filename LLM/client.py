import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load .env located next to this file (robust when running from other cwd)
base_dir = os.path.dirname(__file__)
load_dotenv(os.path.join(base_dir, ".env"))

class HelloAgentsLLM:
    """"调用任何兼容OpenAI接口的LLM服务的客户端。默认使用流式输出，适合实时交互场景。"""
    def __init__(self, model: str = None, api_key: str = None, base_url: str = None, timeout: int = None):

        self.model = model or os.getenv("LLM_MODEL_ID")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        # ensure timeout is an int
        timeout_env = timeout if timeout is not None else os.getenv("LLM_TIMEOUT", 60)
        try:
            self.timeout = int(timeout_env)
        except Exception:
            self.timeout = 60

        # Debug prints to help diagnose connection issues
        print(f"LLM client config -> model: {self.model}, base_url: {self.base_url}, timeout: {self.timeout}")
        if not self.api_key:
            print("Warning: LLM API key is empty. Set LLM_API_KEY in .env or pass api_key explicitly.")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

    def think(self, messages: List[Dict[str,str]], temperature: float = 0) -> str:
        """
        调用LLM服务生成响应。
        """
        print('正在调用 {} 模型...'.format(self.model))
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True  # 使用流式输出
            )

            # 处理流式输出
            print("大模型响应成功：")
            collected_content = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)  # 实时输出
                collected_content.append(content)
            print()
            return ''.join(collected_content)


        except Exception as e:
            print(f"调用LLM API时出错: {e}")
            return None
if __name__ == "__main__":
    try:
        llmClient = HelloAgentsLLM()

        example_messages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}

        ]

        print("=== 测试调用 LLM ===")
        response = llmClient.think(example_messages)
        if response:
            print(f"LLM输出：\n{response}\n")
    except Exception as e:
        print(f"调用LLM时出错: {e}")
        
   