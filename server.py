from socket import *
from binascii import hexlify, unhexlify
import sys

from System.Core.Colors import bcolors

HOST = "127.0.0.1"
PORT = 502

BUFSIZ = 1024

def_resp = "297500000053ff0450303030303030303030303030303333333730000000000000000000000000000058303030303632353633353800000000000000000000000000000000000000000fe80000000600000000000000000000";  # 6 response to read input registers

rcv_list = [
    "0001000000060a0100000001",  # 1 modbus read coils
    "0001000000060a0300050002",  # 2 modbus read holding reg
    "0001000000060a0500020000",  # 4 modbus write signle coil
    "000100000006ff020063001e",  # 5 modbus Read discrete Inputs
    "297500000006ff0400300028",  # 6 modbus read input registers
    "485a00000008ff0f000700030100",  # 7 modbus write multiple coils
    "0001000000060a0100000001",  # 3 modbus read coils
    ]
send_resp = [
    "0001000000040a010100", #1 response to read coils
    "0001000000070a030400090018", #2 response to  read holding reg
    "0001000000060a0500020000", #4 response to write single coils
    "000000000007ff040400000000000100000007ff0204bd4f6739", #5 response to Read discrete Inputs
    "297500000053ff0450303030303030303030303030303333333730000000000000000000000000000058303030303632353633353800000000000000000000000000000000000000000fe80000000600000000000000000000", #6 response to read input registers
    "297a00000008ff0f000500010100", #7 response to write multiple coils
    "0001000000040a010100", #3 response to read coils
]

def send_response(tcpCliSock, addr, port, rcv, rcv_msg):
    matched = False

    for idx in range(0, (len(rcv))):
        if hexlify(rcv_msg) == rcv[idx]:
            matched = True
            tcpCliSock.sendall(unhexlify(send_resp[idx]))
            print(bcolors.OKGREEN + '[+] Sending attack response to ' + bcolors.BOLD + str(addr[0]) + bcolors.ENDC+ ' : ' + hexlify(rcv_msg).decode('utf-8') + bcolors.ENDC)
            #print("Sending attack response to %s: %s" % (addr[0], send_resp[idx]))
            break

    if not matched:
        tcpCliSock.sendall(unhexlify(def_resp))


def main():
    global HOST, BUFSIZ, PORT, send_resp, rcv_list

    try:
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    except error as e:
        print(bcolors.FAIL + '[-] Failed creating socket.' + bcolors.ENDC)
        sys.exit(1)

    try:
        print('[*] Connecting to: ' + bcolors.BOLD + str(HOST)+':'+str(PORT) + bcolors.ENDC)
        ADDR = (HOST, PORT)

        tcpSerSock.bind(ADDR)
        tcpSerSock.listen(5)

    except PermissionError:
        print(bcolors.FAIL + '[-] Cannot connect to port ' + str(PORT) + '. Please provide root privileges.' + bcolors.ENDC)
        sys.exit(1)
    print(bcolors.OKGREEN + '[+] Connection enstablished!' + bcolors.ENDC)
    while True:
        print(bcolors.OKGREEN +'[+] Listening ...'+ bcolors.ENDC)
        tcpCliSock, addr = tcpSerSock.accept()

        while True:
            rcv_msg = tcpCliSock.recv(BUFSIZ)
            if not rcv_msg:
                break
            print(bcolors.OKGREEN + '[+] Received attack packet from ' + bcolors.BOLD + str(addr[0]) + bcolors.ENDC+ ' : ' + hexlify(rcv_msg).decode('utf-8') + bcolors.ENDC)
            # str1 = raw_input('any key to continue> ')
            send_response(tcpCliSock, addr, PORT, rcv_list, hexlify(rcv_msg))

        tcpCliSock.close()


if __name__ == "__main__":
    print(bcolors.OKBLUE + 'MODBUS Server v 1.0.0' + bcolors.ENDC)

    try:
        main()

    except:
        exit(0)
