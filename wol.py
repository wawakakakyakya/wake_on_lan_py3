# -*- coding: utf-8 -*-
import sys
import socket
import time
import argparse
import binascii
import traceback

_USAGE = """Usage:
  python wol.py [options] <MAC address>...

Options:
  -m, --mac <MAC Address>
    MAC Address
  -i, --ip <IP address>
    Default IP address is '<broadcast>'
  -p, --port
    Show this help.
  -h, --help
    Show this help.
"""


class WakeOnLan:

    def chkargs(self):

        try:

            parser = argparse.ArgumentParser(description='Check tcp connectivity')
            parser.add_argument('--mac', '-m', dest='mac', type=str, help='target MAC ADDRESS, required', required=True)
            parser.add_argument('--ip', '-i', dest='host', type=str, default="255.255.255.255",
                                help='Destinaiton IP ADDRESS, not required')
            parser.add_argument('--port', '-p', dest='port', type=int, default='9',
                                help='target port, Default is 9, not required', )

            args = parser.parse_args()

            if "-" in args.mac:
                args.mac = args.mac.replace("-", ":")

            if len(args.mac.split(":")) != 6:
                raise Exception("Mac address is insufficient")

            for m in args.mac.split(":"):
                if len(m) != 2:
                    raise Exception("Mac address is insufficient")
                
            return args
        
        except Exception as e:
            print("Exception: {0}".format(e))
            #print(traceback.format_exc())
            sys.exit(1)

    def createpacket(self, args):
        try:

            brcastmac = 'F'*12
            enc_dst_mac = ''.join(args.mac.split(':')).encode()
            magicpacket = binascii.unhexlify(brcastmac.encode() + (enc_dst_mac * 16))  # create magicpacket
    
            return magicpacket
    
        except Exception as e:
            print("Exception: {0}".format(e))
            print(traceback.format_exc())
            sys.exit(1)
    
    
    def sendpacket(self, p, args):
        
        try:
    
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # connet udp
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # enable broadcast
            s.sendto(p, (args.host, args.port))  # send magicpacket
            s.close()
    
        except Exception as e:
            print("Exception: {0}".format(e))
            print(traceback.format_exc())
            sys.exit(1)
    
    
    def main(self):
        try:

            args = self.chkargs()
            packet = self.createpacket(args)
            self.sendpacket(packet, args)
            print("WOL executed to %s" % args.mac)
    
            return 0
    
        except socket.error as socerr:
            print("socket error: {0}".format(socerr))
            sys.exit(1)
    
        except binascii.Error as binascerr:
            print("binascii.Error: {0}".format(binascerr))
            sys.exit(1)
    
        except Exception as e:
            print("Exception: {0}".format(e))
            print(traceback.format_exc())
            sys.exit(1)
    

if __name__ == "__main__":
    start = time.time()
    WakeOnLan().main()
    elapstedtime = time.time() - start

    print("execute time is %s" % elapstedtime)
    
