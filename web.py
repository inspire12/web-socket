import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('192.168.101.118', 2123)
s.connect(addr)

# header
magicCode = 1234
pType = 12
pVer = 1

# body
userIp = bytes('192.168.3.101', encoding='UTF-8')
url = bytes('https://abc.com/def.jsp?param1=test¶m2=ABC', encoding='UTF-8')
urlLen = len('https://abc.com/def.jsp?param1=test¶m2=ABC')
userId = bytes('yhkim', encoding='UTF-8')
userIdLen = len('yhkim')

values = (magicCode, pType, pVer, userIp, urlLen, url, userIdLen, userId)
fmt = '>I I h 16s I {}s I {}s'.format(urlLen, userIdLen)
packer = struct.Struct(fmt)

sendData = packer.pack(*values)
print(sendData)
try:
    s.sendall(sendData)
    print("\n")
    print(s.recv(1024))
finally:
    s.close()

