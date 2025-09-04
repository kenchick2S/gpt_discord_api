import subprocess
import threading
import time

output_buffer = []

def reader_thread(stdout_pipe):
    for line in iter(stdout_pipe.readline, ''):
        output_buffer.append(line.strip())
    # for line in iter(stdout_pipe.readline, b''):
    #     try:
    #         decoded = line.decode('utf-8')  # 或 'cp950' 視情況
    #     except UnicodeDecodeError:
    #         decoded = line.decode('utf-8', errors='replace')  # ❗防止崩潰
    #     output_buffer.append(decoded.strip())
    stdout_pipe.close()

# 啟動目標程式
proc = subprocess.Popen(
    ["C:/Users/admin/Desktop/gpt/Scripts/python.exe", "-u", "open_gpt_page.py"],  # 或其他執行檔
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    errors='ignore',
    bufsize=1
)

# 啟動讀取線程
t = threading.Thread(target=reader_thread, args=(proc.stdout,))
t.daemon = True
t.start()

try:
    while True:
        message = input()
        if message == "":
            break 
        proc.stdin.write(message+'\n')
        proc.stdin.flush()

        time.sleep(15)
        content = ""
        for line in output_buffer:
            content += line
        print(content)
        output_buffer.clear()
        print("-" * 30)

except KeyboardInterrupt:
    print("停止程式")
    proc.terminate()
    time.sleep(1)  # 給點時間讓它處理 SIGTERM
    if proc.poll() is None:
        print("❗ terminate 沒有效，改用 kill")
        proc.kill()