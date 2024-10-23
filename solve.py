import sys
from pwn import *

#context.log_level="debug"

host=sys.argv[1]
port=int(sys.argv[2])

r=remote(host,port)

flag=b""
for i in range(64):
    pad=b"\x00"*(64-(len(flag)+1))
    for c in range(256):
        pay=pad+flag+bytes([c,])+pad
        r.sendline(pay.hex().encode())
        ct=r.recvuntil(b"\n",drop=True).decode()
        ct=bytes.fromhex(ct)
        if ct[:64]==ct[64:128]:
            print(f"found {c}")
            flag+=bytes([c,])
            break
    else:
        break

print(flag)
r.close()
