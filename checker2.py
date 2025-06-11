import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import concurrent.futures

# 儲存已查詢的 Proxy 結果
queried_results = []

# 查詢單一 proxy 並回傳結果
def query_proxy(index, total, raw):
    try:
        host, port, username, password = raw.split(":", 3)
        port = int(port)
        proxy_dict = {
            "http": f"socks5h://{username}:{password}@{host}:{port}",
            "https": f"socks5h://{username}:{password}@{host}:{port}"
        }

        resp = requests.get("https://api.ipify.org?format=json", proxies=proxy_dict, timeout=10)
        ip = resp.json().get("ip", "未知")
        return (index, raw, ip, None)
    except Exception as e:
        return (index, raw, None, e)

def check_proxies():
    global queried_results
    proxy_text = input_text.get("1.0", tk.END).strip()
    if not proxy_text:
        messagebox.showwarning("警告", "請輸入 proxy 清單")
        return

    proxies = [line.strip() for line in proxy_text.splitlines() if line.strip()]
    output_text.delete("1.0", tk.END)
    queried_results = []

    total = len(proxies)
    output_text.insert(tk.END, f"🔍 開始查詢共 {total} 筆 Proxy（多執行緒中...）\n\n")
    output_text.update()

    def callback(result):
        index, raw, ip, error = result
        progress_text = f"[{index+1}/{total}] "
        if error is None:
            line = f"{progress_text}🔹 Proxy: {raw}\n    → IP: {ip}\n\n"
            queried_results.append((raw, ip))
            output_text.insert(tk.END, line, "success")
        else:
            line = f"{progress_text}❌ Proxy: {raw}\n    → 錯誤：{error}\n\n"
            output_text.insert(tk.END, line, "error")
        output_text.update()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for idx, raw in enumerate(proxies):
            futures.append(executor.submit(query_proxy, idx, total, raw))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            window.after(0, callback, result)

def filter_by_prefix():
    prefix = prefix_entry.get().strip()
    if not queried_results:
        messagebox.showinfo("提示", "請先執行『查詢 IP』")
        return
    if not prefix:
        messagebox.showwarning("警告", "請輸入要比對的 IP 前綴")
        return

    matched = [(raw, ip) for (raw, ip) in queried_results if ip.startswith(prefix)]

    output_text.insert(tk.END, f"\n=== ✅ 符合前綴 `{prefix}` 的 Proxy 共 {len(matched)} 筆 ===\n", "highlight")
    for idx, (raw, ip) in enumerate(matched, start=1):
        output_text.insert(tk.END, f"{idx}. {ip} ← {raw}\n", "highlight")
    output_text.insert(tk.END, "\n")
    output_text.update()

def clear_input():
    input_text.delete("1.0", tk.END)

# 建立 GUI 視窗
window = tk.Tk()
window.title("SOCKS5 Proxy IP 查詢工具（多執行緒高速版）")
window.geometry("900x650")

tk.Label(window, text="輸入 SOCKS5 Proxy（一行一筆）:").pack()
input_text = scrolledtext.ScrolledText(window, width=110, height=10)
input_text.pack(pady=5)

tk.Button(window, text="🧹 清除 Proxy 輸入", command=clear_input).pack(pady=2)

tk.Label(window, text="輸入 IP 前綴（例如 36.224）:").pack()
prefix_entry = tk.Entry(window, width=30)
prefix_entry.pack(pady=5)

tk.Button(window, text="🔍 查詢 Proxy 對應 IP", command=check_proxies).pack(pady=5)
tk.Button(window, text="✅ 過濾符合前綴的 IP", command=filter_by_prefix).pack(pady=5)

output_text = scrolledtext.ScrolledText(window, width=110, height=20)
output_text.pack(pady=5)

# 標籤樣式
output_text.tag_config("success", foreground="green")
output_text.tag_config("error", foreground="red")
output_text.tag_config("highlight", foreground="blue", font=("Courier", 10, "bold"))

window.mainloop()
