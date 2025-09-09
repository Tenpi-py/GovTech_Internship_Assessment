# Nginx Log Parser & Data Enricher (Python)

**Division / Team:** CSG-ENG-DTP  
**Assessment:** Nginx log parser and data enricher

---

## Overview

This script reads **Nginx access logs** in the default **combined** format, parses each line into JSON, and enriches the result with additional fields derived from the **User-Agent** string:

- **`ua_browser`** → Chrome, Firefox, Safari, Edge, etc.  
- **`ua_os`** → Windows, macOS, Android, iOS, Linux, etc.  
- **`ua_device`** → Desktop, Mobile, Tablet, Smart TV, Bot.  

It outputs a JSON file containing an array of enriched log records.

---

## Quickstart

### 1. Prerequisites
- Python **3.8+** (tested up to 3.12).
- No third-party libraries required.

### 2. Run the script
```bash
python script.py <input_log> <output_json>
```

Example:
```bash
python nginx_enrich.py sample_access.log output.json
```

### 3. Output
- The script will produce a JSON file (`output.json`) with one object per log line.
- Unparsable lines are preserved as objects with:
  ```json
  { "parse_error": true, "line_number": 6, "raw": "invalid line ..." }
  ```

---

## Input Format (Nginx "combined")

The parser expects the **combined** log format (Nginx default):

```
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
```

Example:
```
203.0.113.9 - - [09/Sep/2025:12:03:27 +0000] "GET / HTTP/1.1" 200 1024 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
```

---

## Output Fields

Each parsed log entry includes:

- `remote_addr` → client IP  
- `remote_user` → user (or `-`)  
- `time_local` → raw timestamp string from Nginx  
- `request` → full HTTP request string  
- `status` → integer HTTP status code  
- `body_bytes_sent` → integer (or `null` if `-`)  
- `http_referer` → HTTP referer  
- `http_user_agent` → raw UA string  

**Enriched fields:**
- `ua_browser`  
- `ua_os`  
- `ua_device`  

---

## Example

**Input log line:**
```
127.0.0.1 - - [09/Sep/2025:12:00:00 +0000] "GET / HTTP/1.1" 200 512 "-" "curl/8.0.1"
```

**Output JSON object:**
```json
{
  "remote_addr": "127.0.0.1",
  "remote_user": "-",
  "time_local": "09/Sep/2025:12:00:00 +0000",
  "request": "GET / HTTP/1.1",
  "status": 200,
  "body_bytes_sent": 512,
  "http_referer": "-",
  "http_user_agent": "curl/8.0.1",
  "ua_browser": null,
  "ua_os": null,
  "ua_device": "Bot"
}
```

---

## Assumptions

- Input log format is the default **combined** format. If your `log_format` differs, the regex may need adjustment.  
- Timestamps (`time_local`) are left as **raw strings** (not converted to ISO-8601).  
- User-Agent parsing is heuristic-based, not exhaustive. It covers the most common browsers, OSes, devices, and bots.  
- Unparsable lines are not discarded—they are included with a `parse_error` marker.

---

## Repository Structure

```
.
├── nginx_enrich.py        # main script
├── sample_access.log      # example Nginx log
├── output.json            # sample output after running script
└── README.md              # this file
```

---

## License
For academic/assessment use only. Not licensed for redistribution.
