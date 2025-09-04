import requests
import os

'''
    幫 discord bot 建立 commands
'''

# ⚠️ 請填入你的資料
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APPLICATION_ID = os.getenv("DISCORD_APP_ID")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # 測試伺服器 ID

# Slash Command 定義
# command = {
#     "name": "hello",
#     "description": "打個招呼 👋",
#     "type": 1  # CHAT_INPUT
# }

command = {
  "name": "gpt",
  "description": "就是GPT就是GPT",
  "type": 1,
  "options": [
    {
      "name": "prompt",
      "description": "可以輸入任何訊息",
      "type": 3, 
      "required": True
    }
  ]
}

# 發送 API 請求
url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"
headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=command)

if response.status_code == 201:
    print("✅ Slash Command 註冊成功！")
else:
    print("❌ 發生錯誤：", response.status_code, response.text)
