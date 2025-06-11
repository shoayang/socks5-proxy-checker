import requests

# === 你想要的 IP 前綴，例如 "36.224"（中華電信） ===
TARGET_PREFIX = "1.160"

# === 從 proxies.txt 讀取多筆 Proxy ===
with open("proxies.txt", "r") as f:
    proxy_list = [line.strip() for line in f if line.strip()]

matched_proxies = []

print("=== 每筆 Proxy 對應的 IP ===")
for raw in proxy_list:
    try:
        host, port, username, password = raw.split(":", 3)
        port = int(port)

        proxies = {
            "http": f"socks5h://{username}:{password}@{host}:{port}",
            "https": f"socks5h://{username}:{password}@{host}:{port}",
        }

        response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
        ip = response.json().get("ip", "未知")

        print(f"🔹 Proxy: {raw}")
        print(f"   → IP: {ip}")

        # 符合前綴條件就收錄
        if ip.startswith(TARGET_PREFIX):
            matched_proxies.append((raw, ip))

    except Exception as e:
        print(f"❌ Proxy: {raw}")
        print(f"   → 錯誤：{e}")

# === 最後統整結果 ===
print("\n==============================")
print(f"✅ 符合前綴 `{TARGET_PREFIX}` 的 Proxy 清單：")
for raw, ip in matched_proxies:
    print(f"{ip} ← {raw}")
print(f"共找到 {len(matched_proxies)} 筆符合條件的 Proxy。")
