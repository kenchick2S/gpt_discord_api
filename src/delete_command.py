import requests
import os

'''
    幫 discord bot 建立 commands
'''

# ⚠️ 請填入你的資料
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APPLICATION_ID = os.getenv("DISCORD_APP_ID")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # 測試伺服器 ID
COMMAND_ID = "1399600056767873054"

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands/{COMMAND_ID}"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}"
}

response = requests.delete(url, headers=headers)

if response.status_code == 204:
    print("✅ 指令成功刪除！")
else:
    print("❌ 刪除失敗：", response.status_code, response.text)