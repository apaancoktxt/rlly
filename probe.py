import json, urllib.request, urllib.error
RPCS=["https://eth.llamarpc.com","https://ethereum-rpc.publicnode.com","https://eth.drpc.org","https://rpc.ankr.com/eth","https://cloudflare-eth.com"]
S="0xf70da97812cb96acdf810712aa562db8dfa3dbef"
def rpc(url, method, params):
    d=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    r=urllib.request.Request(url,data=d,headers={"content-type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(r,timeout=25) as x:
            return json.load(x)
    except Exception as e:
        return {"error":str(e)[:100]}
for url in RPCS:
    res=rpc(url,"eth_getCode",[S,"latest"])
    code=res.get("result","")
    if code and len(code)>100:
        print(f"OK {url} code_len={len(code)}")
        open("solver_bytecode.txt","w").write(code)
        # balance
        b=rpc(url,"eth_getBalance",[S,"latest"])
        print("solver balance wei:", int(b.get("result","0x0"),16))
        break
    else:
        print(f"FAIL {url}: {res.get('error') or 'empty'}")
