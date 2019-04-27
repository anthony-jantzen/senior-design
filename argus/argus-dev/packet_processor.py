"""
Packet processor for argus. Takes in a raw pcap file fresh from the press
Once packets are read in, filter_packets is run to eliminate packets that
don't provide appropriate information.

Then process_packets looks for useful information in the remaining packets
"""

from queue import PriorityQueue
from scapy.layers.dot11 import Dot11Beacon, Dot11ProbeResp
from scapy.all import PcapReader

import itertools


IGNORED_PKT_TYPES = [Dot11Beacon, Dot11ProbeResp]


class PacketProcessor:
    """PacketProcessor processes input packets into a queue for the
    location calculator

    Args:
        packet_file_list(str): list of packet files

    """
    def __init__(self, access_points):
        self.__access_points = access_points
        self.__raw_packets = {}
        self.__readers = []

        self.location_data = {}
        for apname in access_points:
            self.location_data[apname] = {}

    def run(self):
        """
        Run the packet processor
        """
        for ap_name, ap_info in self.__access_points.items():
            self._process_pcap(ap_name, ap_info['capture_file'])

        self._process_packets()

    def close(self):
        """
        Close open pcap files
        """
        for reader in self.__readers:
            reader.close()

    def _process_pcap(self, apname, fname):
        """
        Searches an individual pcap file for usefull packets
        """
        def filt(pkt):
            for pktype in IGNORED_PKT_TYPES:
                if pktype in pkt:
                    return False
            return True

        reader = PcapReader(fname)
        self.__readers.append(reader)
        self.__raw_packets[apname] = filter(filt, reader)

    def _process_packets(self):
        """Processes the packets into the queue for location calculation
        Each item in the queue have the following structure:

        location_data = {
            ARGUS1 : {
                <MAC1> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC2> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC3> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...]
            }
            ARGUS2 : {
                <MAC1> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC2> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC3> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...]
            }
            ARGUS3 : {
                <MAC1> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC2> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...],
                <MAC3> : QUEUE: [(time1, RSSI1), (time2, RSSI2), ...]
            }
        }
        """
        for ap, packets in self.__raw_packets.items():
            for packet in packets:
                packet_data = self.process_packet(packet)
                if packet_data is not None:
                    rssi_tuple = (packet_data['TIME'], packet_data['RSSI'])
                    try:
                        self.location_data[ap][packet_data['MAC']].put(rssi_tuple)
                    except KeyError:
                        self.location_data[ap][packet_data['MAC']] = PriorityQueue()
                        self.location_data[ap][packet_data['MAC']].put(rssi_tuple)

    @staticmethod
    def process_packet(packet):
        """Takes a scapy packet object as input and extracts information in the
        following format:
        item = {
            'MAC' : device mac address,
            'AP' : ap device communicated with (argus1, argus2, argus3),
            'RSSI' : signal strength of that device,
            'TIME' : timestamp of when the packet sent
        }
        Args:
            packet: scapy packet for processing
        """
        packet_data = {}

        # We only care about the transmitter address
        packet_data['MAC'] = packet.addr2
        packet_data['RSSI'] = packet.dBm_AntSignal
        packet_data['TIME'] = packet.time
        if packet_data['MAC'] is not None:
            return packet_data

        return None
