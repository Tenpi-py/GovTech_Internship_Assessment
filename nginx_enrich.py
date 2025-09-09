import json, re, sys
from typing import Optional, Dict
LINE_RE = re.compile(
    r'^(?P<remote_addr>\S+)\s+-\s+(?P<remote_user>\S+)\s+\[(?P<time_local>[^\]]+)\]\s+'
    r'\"(?P<request>[^\"]*)\"\s+(?P<status>\d{3})\s+(?P<body_bytes_sent>\d+|-)'
    r'\s+\"(?P<http_referer>[^\"]*)\"\s+\"(?P<http_user_agent>[^\"]*)\"'
)
def detect_browser(ua: str) -> Optional[str]:
    u = ua.lower()
    if "edg/" in u or "edg " in u or "edge" in u: return "Microsoft Edge"
    if "opera" in u or "opr/" in u: return "Opera"
    if "chrome" in u and "chromium" not in u and "edg" not in u and "opr/" not in u: return "Chrome"
    if "safari" in u and "chrome" not in u and "chromium" not in u: return "Safari"
    if "firefox" in u: return "Firefox"
    if "chromium" in u: return "Chromium"
    if "msie" in u or "trident/" in u: return "Internet Explorer"
    return None
def detect_os(ua: str) -> Optional[str]:
    u = ua.lower()
    if "windows nt 10" in u: return "Windows 10/11"
    if "windows nt 6.3" in u: return "Windows 8.1"
    if "windows nt 6.2" in u: return "Windows 8"
    if "windows nt 6.1" in u: return "Windows 7"
    if "windows" in u: return "Windows (other)"
    if "android" in u: return "Android"
    if any(x in u for x in ["iphone","ipad","ipod","cpu os"]): return "iOS/iPadOS"
    if "mac os x" in u or "macintosh" in u: return "macOS"
    if "linux" in u and "android" not in u: return "Linux"
    if "cros" in u: return "ChromeOS"
    return None
def detect_device(ua: str) -> str:
    u = ua.lower()
    if any(x in u for x in ["bot","crawl","spider","slurp","curl/","wget/","python-requests","requests/"]): return "Bot"
    if "mobile" in u and "ipad" not in u: return "Mobile"
    if any(x in u for x in ["tablet","ipad","nexus 7","sm-t"]): return "Tablet"
    if any(x in u for x in ["smart-tv"," smarttv","hbbtv","tv "]): return "Smart TV"
    return "Desktop"
def parse_line(line: str) -> Optional[Dict]:
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    d = m.groupdict()
    d["status"] = int(d["status"])
    d["body_bytes_sent"] = None if d["body_bytes_sent"] == "-" else int(d["body_bytes_sent"])
    # keep raw nginx timestamp
    d["time_local"] = d["time_local"]
    ua = d.get("http_user_agent", "") or ""
    d["ua_browser"] = detect_browser(ua)
    d["ua_os"] = detect_os(ua)
    d["ua_device"] = detect_device(ua)
    return d
def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_log> <output_json>", file=sys.stderr)
        sys.exit(2)
    input_path, output_path = sys.argv[1], sys.argv[2]
    out = []
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, 1):
            if not line.strip():
                continue
            parsed = parse_line(line)
            if parsed is None:
                out.append({"parse_error": True, "line_number": idx, "raw": line.rstrip("\n")})
            else:
                out.append(parsed)
    with open(output_path, "w", encoding="utf-8") as w:
        json.dump(out, w, ensure_ascii=False, indent=2)
if __name__ == "__main__":
    main()
