from flask import Flask, request, jsonify, abort
import os
import nacl.signing
import nacl.exceptions

import subprocess
import threading
import time
import requests

output_buffer = []

def reader_thread(stdout_pipe):
    for line in iter(stdout_pipe.readline, ''):
        output_buffer.append(line.strip())
    stdout_pipe.close()

# 啟動目標程式
proc = subprocess.Popen(
    ["C:/Users/admin/Desktop/gpt/Scripts/python.exe", "-u", "open_gpt_page.py"],  # 或其他執行檔
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# 啟動讀取線程
t = threading.Thread(target=reader_thread, args=(proc.stdout,))
t.daemon = True
t.start()

# Flask app 初始化
app = Flask(__name__)

# 從環境變數載入 Discord Public Key
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask Discord Bot Server Running!"

@app.route("/interactions", methods=["POST"])
def interactions():
    # 從 Discord header 中取得簽名
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        abort(401, "Missing signature headers")

    # Discord 要求：先驗證簽名再讀取 body
    try:
        body = request.data.decode("utf-8")
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except nacl.exceptions.BadSignatureError:
        abort(401, "Invalid request signature")

    # 通過驗證，處理 interaction 資料
    data = request.json

    # Ping (type = 1) - Discord 要求第一次驗證會送這個
    if data["type"] == 1:
        return jsonify({"type": 1})  # Pong 回應

    # Slash Command (type = 2)
    elif data["type"] == 2:
        cmd_name = data["data"]["name"]

        if cmd_name == "hello":
            return jsonify({
                "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
                "data": {
                    "content": "🎉 你的 Slash 指令收到了！"
                }
            })
        elif cmd_name == "gpt":
            options = data["data"].get("options", [])

            prompt = None
            for option in options:
                if option["name"] == "prompt":
                    prompt = option["value"]
            
            interaction_token = data["token"]
            application_id = data["application_id"]
        
            
            # 2️⃣ 開一個背景執行的 follow-up 發送流程
            from threading import Thread
            def delayed_response():
                try:
                    proc.stdin.write(prompt+'\n')
                    proc.stdin.flush()

                    time.sleep(15)
                    content = ""
                    for line in output_buffer:
                        content += line
                    print(content)
                    output_buffer.clear()
                except:
                    content = "來不及回應"

                follow_up_url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
                headers = {"Content-Type": "application/json"}
                data = {
                    "content": content
                }
                requests.post(follow_up_url, headers=headers, json=data)

            Thread(target=delayed_response).start()

            return jsonify({"type": 5})

    return jsonify({"error": "Unhandled interaction type"}), 400

if __name__ == "__main__":
    app.run(port=5000)
