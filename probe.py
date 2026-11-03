import json, urllib.request, urllib.error

BASE="https://api.relay.link"
W="0x0000000000000000000000000000000000000001"
REC="0x48A7F32009473dE12582911CF0782e5268F2B9E4"
USDC_BASE="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

def req(method, path, body=None, headers=None, timeout=30):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    h = {"content-type":"application/json","accept":"application/json"}
    if headers: h.update(headers)
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as x:
            return x.status, x.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8","replace")
    except Exception as e:
        return 0, f"ERR {type(e).__name__}: {e}"

print("### TEST 1: balances tanpa auth (kontrol)")
s,b = req("GET", f"/app-fees/{W}/balances")
print(f"{s}  {b[:300]}\n")

print("### TEST 2: claims history tanpa auth")
s,b = req("GET", f"/app-fees/{W}/claims")
print(f"{s}  {b[:300]}\n")

print("### TEST 3: CLAIM tanpa api key -> recipient KITA")
body={"chainId":8453,"currency":USDC_BASE,"recipient":REC}
s,b = req("POST", f"/app-fees/{W}/claim", body)
print(f"{s}  {b[:600]}\n")

print("### TEST 4: CLAIM dengan amount eksplisit")
body["amount"]="13199"
s,b = req("POST", f"/app-fees/{W}/claim", body)
print(f"{s}  {b[:600]}\n")

print("### TEST 5: screen/info (kontrol 401 dari sandbox)")
s,b = req("GET", f"/wallets/screen/info?wallet={W}")
print(f"{s}  {b[:300]}\n")

print("### TEST 6: screen/override TANPA api key")
s,b = req("POST","/wallets/screen/override",{"wallet":W,"action":"ALLOW","reason":"test"})
print(f"{s}  {b[:400]}\n")
