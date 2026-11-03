import json, urllib.request, urllib.error
BASE="https://api.relay.link"
def req(m,p,b=None,h=None,t=25):
    d=json.dumps(b).encode() if b is not None else None
    hh={"content-type":"application/json","accept":"application/json"}
    if h: hh.update(h)
    r=urllib.request.Request(BASE+p,data=d,headers=hh,method=m)
    try:
        with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

print("### A. /requests/v3 -> ambil wallet aktif dari transaksi nyata")
s,b=req("GET","/requests/v3?limit=5")
print(s, b[:500], "\n")

print("### B. /protocol/executions -> id contoh")
s,b=req("GET","/protocol/executions/test")
print(s, b[:300], "\n")

print("### C. published-requests (kalau ada)")
s,b=req("GET","/published-requests")
print(s, b[:400], "\n")

print("### D. withdrawals/balances butuh recoveryAddress")
s,b=req("GET","/withdrawals/balances?recoveryAddress=0x48A7F32009473dE12582911CF0782e5268F2B9E4&ownerChainId=8453")
print(s, b[:400], "\n")
