import json, re, sys
from typing import Optional, Dict
# Nginx "combined" format
LINE_RE = re.compile(
    r'^(?P<remote_addr>\S+)\s+-\s+(?P<remote_user>\S+)\s+\[(?P<time_local>[^\]]+)\]\s+'
    r'\"(?P<request>[^\"]*)\"\s+(?P<status>\d{3})\s+(?P<body_bytes_sent>\d+|-)'
    r'\s+\"(?P<http_referer>[^\"]*)\"\s+\"(?P<http_user_agent>[^\"]*)\"'
)
def parse_line(line: str) -> Optional[Dict]:
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    d = m.groupdict()
    # (no type conversions yet)
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
