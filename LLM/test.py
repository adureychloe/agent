from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='ms-d9f44733-ff22-4f01-bdb1-e26c217db1e3', # ModelScope Token
)

response = client.chat.completions.create(
    model='deepseek-ai/DeepSeek-V4-Pro-0813', # ModelScope Model-Id, required
    messages=[
        {
            'role': 'user',
            'content': '你好'
        }
    ],
    stream=True
)
done_reasoning = False
for chunk in response:
    if chunk.choices:
        reasoning_chunk = chunk.choices[0].delta.reasoning_content
        answer_chunk = chunk.choices[0].delta.content
        if reasoning_chunk != '':
            print(reasoning_chunk, end='', flush=True)
        elif answer_chunk != '':
            if not done_reasoning:
                print('\n\n === Final Answer ===\n')
                done_reasoning = True
            print(answer_chunk, end='', flush=True)