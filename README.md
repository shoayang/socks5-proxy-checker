# SOCKS5 Proxy Checker GUI

This is a Python-based graphical tool (built with Tkinter) for batch checking the real IP addresses behind multiple SOCKS5 proxies.  
It also allows filtering based on a specified IP prefix. The tool displays progress and errors in real-time and uses clear formatting for readability.

---

## Features

- Supports SOCKS5 proxies in the format: `host:port:username:password`
- Checks real IP using `https://api.ipify.org`
- Filters results based on user-specified IP prefix (e.g., `36.224`)
- IP checking and prefix filtering are handled separately
- Displays status and progress per proxy
- Scrollable, styled GUI with input clearing functionality

---

## Requirements

- Python 3.8 or higher
- Required packages:
  - `requests`
  - `PySocks`

---

## Installation

Install dependencies once via pip:

```bash
pip install requests pysocks
```

---

## Usage

Run the application with:

```bash
python main.py
```

If using the `.exe` version, simply double-click to run without needing a Python environment.

---

## How to Use

1. Paste multiple proxies into the input area (one per line)
2. Click "Check Proxies"
3. Enter your desired IP prefix (e.g., `36.224`)
4. Click "Filter Matching IPs"
5. Results and filtered matches will be displayed clearly below

---

## Input Format Example

```
gate.nodemaven.com:1080:user-country-tw-region-taipei-isp-chunghwa_telecom-ipv4-true-sid-abc123:password
gate.nodemaven.com:1080:user-country-tw-region-taoyuan-isp-chunghwa_telecom-ipv4-true-sid-xyz456:password
```

---

## Project Structure

```
socks5-proxy-checker/
├── main.py              # Main application
├── README.md            # This file
├── requirements.txt     # (Optional) Dependency list
├── dist/                # Folder for compiled .exe
└── .gitignore           # Git ignore file
```

---

## License

This project is licensed under the MIT License.
