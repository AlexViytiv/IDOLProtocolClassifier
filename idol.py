#!/usr/bin/env python
"""IDOL Protocol Processing Utility.

This utility is designed to process, distribute and send IDOL
packages with certain attribute for particular recipient.

Require : python
Syntax of run command :
$ sudo python <name_of_program> [<receivers.json>] [<messages.txt>]

"""
import sys
from time import sleep
from threading import Thread

import re
import json
from scapy.all import IP, ICMP, UDP, sr1, send, sniff

from fileloader import get_file_content


"""GLOBAL DEFAULT VALUES:
- DEFAULT_TTL ............... Time To Live parameter of ICMP packets
- DEFAULT_SLEEP_TIME ........ Sleep time before sniff interface
- DEFAULT_REPLY_TIMEOUT ..... Time to break waiting for response
- DEFAULT_LOG ............... name of default file with packets
- DEFAULT_RECEIVERS ......... name of file which containt all receivers
                              and their ip addresses
- PROTOCOL_TYPE_TO_SNIFF .... name of type of protocol which will be sniffed
                              in sniffer function
"""
DEFAULT_TTL = 20
DEFAULT_SLEEP_TIME = 1
DEFAULT_REPLY_TIMEOUT = 1
DEFAULT_LOG = 'messages.txt'
DEFAULT_RECEIVERS = 'receivers.json'
PROTOCOL_TYPE_TO_SNIFF = 'udp'




class Receiver:
    """ Class is abstract model of packet receiver. It used to save name of
    receiver, his ip address, list of his packets and regex that is receiver
    signature. Also class provides several methods to initialize receiver, add
    packets to receiver and send them to him.
    """
    def __init__(self, name, ip, signatures):
        """Constructor of class takes 4 arguments:
            - self - standard pointer to current object
            - name - name of receiver
            - ip   - ip address of receiver
            - signatures - dictionary of users signatures
        In this method all private variables become initialized.
        """
        self.__name = name
        self.__ip = ip
        self.__packets = []
        self.__clasifier = re.compile(signatures.get(self.__name))

    def __interface_sniffer(self, protocol_type):
        """Interface sniffer method sniff default interface for
        packets with certain destination ip address and protocol
        type.
        """
        for packet in sniff(filter=protocol_type, timeout=1):
            try:
                if packet.getlayer(IP).dst == self.__ip:
                    print(' Packet was sucessfully sent.')
                    return
            except AttributeError:
                pass

    def send_packets(self):
        """Method used to send packets to certain ip address.
        First, it send ICMP packet to check availability of
        receiver in network. If he is in network, program
        sends packets one-by-one and sniff interface for udp
        packets.
        """
        icmp_packet = IP(self.__ip, ttl=DEFAULT_TTL) / ICMP()
        reply = sr1(icmp_packet, timeout=DEFAULT_REPLY_TIMEOUT)

        if reply:
            for packet_payload in self.__packets:
                udp_packet = IP(dst=self.__ip) / UDP() / packet_payload

                sniffer = threading.Thread(target=self.__interface_sniffer,
                                           args=(PROTOCOL_TYPE_TO_SNIFF, ))
                sniffer.start()
                # required to be able to sniff sent packet
                sleep(DEFAULT_SLEEP_TIME)

                send(udp_packet)
                sniffer.join()
        else:
            print(' {0} is offline.'.format(self.__ip))

    def add_packet(self, packet):
        """Method check packet for matching to some regex
        and add it to receiver if first match the rule
        """
        if self.__clasifier.match(packet):
            self.__packets.append(packet)


def clasify_packets(packets, receivers):
    """Function clasify_packets() used to detect receiver
    of each packet. Every packet is represented by line
    in source file.
    """
    for packet in packets:
        if(len(packet.strip('\n')) == 0):
            continue

        for receiver in receivers:
            receiver.add_packet(packet)


def load_packets(filePath):
    """Function open_logs() used to open file that contain all
    received packets. If something goes wrong, it print message to inform
    user about possible problem.
    """
    try:
        content = get_file_content(filePath)
        packets = content.split('\n')
    except Exception as e:
        print(""" [Problem] | A problem has been identified. Please, send
                              info below to idolprotocol_support@gmail.com.""")
        print(' Problem report : {0}'.format(e.message))
        exit(1)

    return packets

def load_receivers(fileReceivers):
    """Load receivers names and ip adresses from .json file and
    create objects of class Receiver with previous initialization data.
    Signatures of all users used to detect destination of packet.
    """
    receivers = []
    with open(fileReceivers, 'r') as file:
        receivers_data = json.load(file)

    signatures = {'Ivasyk': r'^([^\n]{2})*$',
                  'Dmytryk': r'^[A-Z]([^\n]{2})*$',
                  'Ostap': r'^[^A-Z]([^\n]{2})*(?<!end)$',
                  'Lesya': r'.*(end)$'}
    for receiver_name in receivers_data.keys():
        receivers.append(Receiver(receiver_name,
                         receivers_data[receiver_name],
                         signatures))

    return receivers


def get_receivers():
    """The function is intended to determine how to obtain
    data about receivers:
        - via default file 'receivers.json'
        - via user custom file '*.json'
    """
    try:
        return load_receivers(sys.argv[1])
    except IndexError:
        return load_receivers(DEFAULT_RECEIVERS)
    except Exception:
        print(""" [Problem] | Make sure that there is 'receivers.json' file
                              or specify your own as program argument:
                                  $ sudo python idol.py <.json> <.txt>""")
        exit(1)


def process_logs():
    """The function is intended to determine how to obtain
    data about all packets that need to be sent:
        - via default file 'messages.txt'
        - via user custom file '*.txt'
    """
    try:
        return load_packets(sys.argv[2])
    except IndexError:
        return load_packets(DEFAULT_LOG)
    except Exception:
        print(""" [Problem] | Make sure that there is 'messages.txt' file
                              or specify your own as program argument:
                                  $ sudo python idol.py <.json> <.txt>""")
        exit(1)


def send_all_packets(receivers):
    """This function simplify process of sending packets to
    all receivers.
    """
    for receiver in receivers:
        receiver.send_packets()


def main():
    """Function main() realize calls of all functions.
    """
    receivers = get_receivers()
    packets = process_logs()
    clasify_packets(packets, receivers)
    send_all_packets(receivers)

    # Information to see result.
    print(' Process finished.')


if __name__ == '__main__':
    main()

