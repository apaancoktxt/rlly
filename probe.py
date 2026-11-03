import json, urllib.request, urllib.error
BASE="https://api.relay.link"
def get(p,t=25):
    try:
        with urllib.request.urlopen(BASE+p,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"
def post(p,b,t=30):
    d=json.dumps(b).encode()
    r=urllib.request.Request(BASE+p,data=d,headers={"content-type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

RID="0x1793666094e5345f3c05fe304f392d5d2b535625134a676efced0dd11c132393"
print("### A. FULL response executions/{id} (data apa saja yang bocor?)")
s,b=get(f"/protocol/executions/{RID}")
print(s)
print(json.dumps(json.loads(b),indent=1)[:1500] if s==200 else b[:300])

print("\n\n### B. apakah execution orang lain bisa diakses? (pakai requestId acak valid-format)")
import hashlib
for i in range(3):
    fake="0x"+hashlib.sha256(f"x{i}".encode()).hexdigest()
    s,b=get(f"/protocol/executions/{fake}")
    print(f"  {fake[:20]} -> {s} {b[:150]}")

print("\n\n### C. oracleAddress: apa ini infra? cek /chains/health")
s,b=get("/chains/health")
print(s,b[:600])
