import json, urllib.request, urllib.error, hashlib
BASE="https://api.relay.link"
def get(p,t=25):
    try:
        with urllib.request.urlopen(BASE+p,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

print("### Kontrol: apakah 5 ID acak menghasilkan respons IDENTIK byte-per-byte?\n")
seen={}
for i in range(5):
    fid="0x"+hashlib.sha256(f"ctrl{i}".encode()).hexdigest()
    s,b=get(f"/protocol/executions/{fid}")
    d=json.loads(b) if s==200 else {}
    ex=d.get("execution",{})
    key=(ex.get("chainId"),ex.get("oracleAddress"),d.get("status"))
    seen.setdefault(key,[]).append(fid[:12])
    print(f"  {fid[:14]} -> chain={ex.get('chainId')} status={d.get('status')} hash={hashlib.md5(b.encode()).hexdigest()[:12]}")

print("\n=== RINGKASAN ===")
for k,v in seen.items():
    print(f"  {k} muncul {len(v)}x")

print("\n### Apakah idempotencyKey ECHO dari input? (bukan dari DB)")
fid="0x"+"de"*32
s,b=get(f"/protocol/executions/{fid}")
if s==200:
    d=json.loads(b)
    echo = d.get("execution",{}).get("idempotencyKey")
    print(f"  input : {fid}")
    print(f"  echo  : {echo}")
    print(f"  ECHO? : {echo==fid}")
