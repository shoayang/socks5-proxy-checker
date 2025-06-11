import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import concurrent.futures
import threading

# === 查詢結果儲存區 ===
queried_results = []

# === 查詢單一 Proxy ===
def query_proxy(index, total, raw):
    try:
        host, port, username, password = raw.split(":", 3)
        port = int(port)
        proxy_dict = {
            "http": f"socks5h://{username}:{password}@{host}:{port}",
            "https": f"socks5h://{username}:{password}@{host}:{port}"
        }
        resp = requests.get("https://api.ipify.org?format=json", proxies=proxy_dict, timeout=5)
        ip = resp.json().get("ip", "未知")
        return (index, raw, ip, None)
    except Exception as e:
        return (index, raw, None, str(e))

# === 安全插入文字到顯示區 ===
def safe_print(text, tag=None):
    output_text.config(state="normal")
    output_text.insert(tk.END, text, tag)
    output_text.see(tk.END)
    output_text.config(state="disabled")

# === 查詢所有 Proxy ===
def run_query_all(proxies):
    global queried_results
    queried_results = []
    total = len(proxies)

    safe_print(f"\n🔍 查詢中，總共 {total} 筆 Proxy...\n\n", "title")
    query_button.config(state=tk.DISABLED)
    filter_button.config(state=tk.DISABLED)

    done_results = []

    def handle_result(result):
        index, raw, ip, error = result
        safe_print("────────────────────────────────────────────\n", "info")
        if error is None:
            msg = f"🟢 [{index+1}/{total}] 成功連線\n\nProxy:\n  {raw}\n\n對應 IP:\n  {ip}\n"
            safe_print(msg, "success")
            queried_results.append((raw, ip))
        else:
            msg = f"🔴 [{index+1}/{total}] 連線失敗\n\nProxy:\n  {raw}\n\n錯誤原因:\n  {error}\n"
            safe_print(msg, "error")
        safe_print("────────────────────────────────────────────\n", "info")

        done_results.append(1)
        if len(done_results) == total:
            success_count = len(queried_results)
            fail_count = total - success_count
            safe_print(f"\n==============================\n", "title")
            safe_print(f"✅ 成功：{success_count} 筆\n", "title")
            safe_print(f"❌ 失敗：{fail_count} 筆\n", "title")
            safe_print(f"==============================\n\n", "title")
            query_button.config(state=tk.NORMAL)
            filter_button.config(state=tk.NORMAL)

    def threaded_query():
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(query_proxy, idx, total, raw): idx for idx, raw in enumerate(proxies)}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                window.after(0, handle_result, result)

    threading.Thread(target=threaded_query, daemon=True).start()

# === GUI 操作區 ===
def start_query():
    proxy_text = input_text.get("1.0", tk.END).strip()
    if not proxy_text:
        messagebox.showwarning("警告", "請輸入 Proxy 清單")
        return
    proxies = [line.strip() for line in proxy_text.splitlines() if line.strip()]
    run_query_all(proxies)

def filter_by_prefix():
    prefix = prefix_entry.get().strip()
    if not queried_results:
        messagebox.showinfo("提示", "請先執行查詢")
        return
    if not prefix:
        messagebox.showwarning("警告", "請輸入前綴")
        return

    matched = [(raw, ip) for (raw, ip) in queried_results if ip.startswith(prefix)]

    safe_print(f"\n=== ✅ 符合前綴 `{prefix}` 的 Proxy 共 {len(matched)} 筆 ===\n", "title")
    for idx, (raw, ip) in enumerate(matched, start=1):
        safe_print("────────────────────────────────────────────\n", "info")
        msg = f"🔵 [{idx}] 符合前綴\n\nProxy:\n  {raw}\n\n對應 IP:\n  {ip}\n"
        safe_print(msg, "highlight")
        safe_print("────────────────────────────────────────────\n", "info")
    safe_print("\n", "highlight")

def clear_input():
    input_text.delete("1.0", tk.END)

# === 建立 GUI ===
window = tk.Tk()
window.title("SOCKS5 Proxy Checker4")
window.geometry("900x650")

# === 輸入區 ===
tk.Label(window, text="輸入 SOCKS5 Proxy（一行一筆）:").pack()
input_text = scrolledtext.ScrolledText(window, width=110, height=10, font=("Consolas", 12))
input_text.pack(pady=5)

# === 建立上方按鈕列 ===
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

query_button = tk.Button(button_frame, text="🔍 查詢 Proxy 對應 IP", width=25, command=start_query)
query_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="🧹 清除 Proxy 輸入", width=25, command=clear_input)
clear_button.grid(row=0, column=1, padx=10)

# === IP 前綴輸入區 ===
tk.Label(window, text="輸入 IP 前綴（例如 36.224）:").pack()
prefix_entry = tk.Entry(window, width=30, font=("Consolas", 12))
prefix_entry.pack(pady=5)

# === 過濾按鈕（保持原位） ===
filter_button = tk.Button(window, text="✅ 過濾符合前綴的 IP", command=filter_by_prefix)
filter_button.pack(pady=5)

# === 輸出區 ===
output_text = scrolledtext.ScrolledText(window, width=110, height=20, state="disabled", font=("Consolas", 12))
output_text.pack(pady=5)
output_text.tag_config("success", foreground="green", font=("Consolas", 11))
output_text.tag_config("error", foreground="red", font=("Consolas", 11))
output_text.tag_config("highlight", foreground="blue", font=("Cascadia Mono", 12))
output_text.tag_config("title", foreground="blue", font=("Consolas", 12, "bold"))
output_text.tag_config("info", foreground="gray", font=("Consolas", 10, "italic"))

# === 執行 ===
window.mainloop()