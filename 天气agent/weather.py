import requests
import json

def get_weather(city: str) -> str:
    """
    通过调用wttr.in接口获取天气信息
    """
    # API端点，请求JSON格式的数据
    url = f"http://wttr.in/{city}?format=j1"

    try:
        # 发起网络请求
        response = requests.get(url)
        # 检查响应状态码是否是200（成功）
        response.raise_for_status()
        # 解析JSON响应
        data = response.json()

        # 提取当前的天气状况
        current_weather = data['current_condition'][0]
        temperature = current_weather['temp_C']
        weather_desc = current_weather['weatherDesc'][0]['value']

        return f"当前{city}的天气是{weather_desc}，温度是{temperature}摄氏度。"
    
    except requests.exceptions.RequestException as e:
        # 处理网络错误
        return f"错误:查询天气时遇到网络问题 - {e}"
    
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"
    
    