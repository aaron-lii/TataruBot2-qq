# -*- coding: utf-8 -*-
import logging

from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

import json
import requests

this_command = ""
chat_ai = on_command(this_command, rule=to_me(), priority=5)


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "用户自行填写"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


url_chat = "用户自行填写" + get_access_token()

async def chat_baidu(args):

    payload = json.dumps({
        "system": "你是最终幻想14里面的角色塔塔露.也是我的小助手,请简洁地回答我的问题,控制在20字以内。",
        "messages": [
            {"role": "user", "content": args}
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url_chat, headers=headers, data=payload, timeout=5)

        res_json = response.json()
        if "result" in res_json:
            return res_json["result"]
        else:
            logger.warning(response.text)
            return "叭 叭叭啦 叭叭叭啦~"
    except Exception as e:
        logger.warning("chat_ai应该是超时了：" + str(e))
        return "塔塔露没反应过来呀，请再说一遍"


@chat_ai.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):

    message_info = str(event.get_message()).strip()[-200:]
    return_str = await chat_baidu(message_info)
    await chat_ai.finish(return_str)

