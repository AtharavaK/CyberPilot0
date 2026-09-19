import urllib.request, json, time

BASE = "http://127.0.0.1:8000/api/v1"

# --- Start scan ---
payload = json.dumps({"target_url": "https://demo-ai-app.com"}).encode()
req = urllib.request.Request(f"{BASE}/scan/start", data=payload,
                             headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req) as r:
    start_resp = json.loads(r.read())

scan_id = start_resp["scan_id"]
print(f"[START] scan_id={scan_id}  status={start_resp['status']}")
print(f"        message={start_resp['message']}")

# --- Poll status ---
for attempt in range(10):
    time.sleep(2)
    with urllib.request.urlopen(f"{BASE}/scan/{scan_id}/status") as r:
        status_resp = json.loads(r.read())
    current = status_resp.get("status", "COMPLETED")
    print(f"[POLL {attempt+1}] status={current}")
    if current == "COMPLETED" or "overall_score" in status_resp:
        print("\n=== FINAL REPORT ===")
        print(f"  Target:        {status_resp.get('target_url')}")
        print(f"  Overall Score: {status_resp.get('overall_score')}/100")
        print(f"  Findings ({len(status_resp.get('findings', []))}):")
        for f in status_resp.get("findings", []):
            print(f"    [{f['severity']}] {f['agent_name']}: {f['description']}")
            if f.get('remediation'):
                print(f"           -> {f['remediation']}")
        break
