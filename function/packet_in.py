import logging

from lib.proto.pkt_proto import *

# -------------------------------
#                                                                                                                  
# App Base Import                                                                                 
#                        
# -------------------------------

from function.nat import Nat_Flow_Add
from function.arp import Arp_Reply

def Packet_In_Handler(ofsw, msg):

    in_port = msg.match['in_port']

    pkt = packet.Packet(msg.data)
    # TODO: Packet library convert to string
    # self.logger.debug('Packet in = %s', str(pkt), self.sw_id)
    header_list = dict((p.protocol_name, p)
                    for p in pkt.protocols if type(p) != str)

    if ARP in header_list:
#        logging.info('[APR]  <in port>%s <keys> %s',
#                         in_port, header_list, extra=ofsw.sw_id)
        retcode, arp_pkt_set  = Arp_Reply(ofsw, msg, header_list)
        if retcode == "REP":
            Nat_Flow_Add(ofsw, arp_pkt_set)
        return

    if ICMP in header_list:
        logging.info('[ICMP]  <in port>%s <keys> %s',
                         in_port, header_list, extra=ofsw.sw_id)
            # Function to ICMP PACKET IN
        return


    if UDP in header_list:
        self.logging.info('[UDP]  <in port>%s <keys> %s',
                    in_port, header_list.values(), extra=ofsw.sw_id)
        return

    if TCP in header_list:
        logging.info('[TCP]  <in port>%s <keys> %s',
                    in_port, header_list.keys(), extra=ofsw.sw_id)
        return

