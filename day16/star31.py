import math
from dataclasses import dataclass, field
import bitstring

@dataclass
class Packet:
    packet_version: int
    start: int
    end: int

@dataclass
class Literal(Packet):
    value: int
    packet_type = 4

@dataclass
class Operator(Packet):
    packet_type: int
    children: list[Packet]


def parse_next_packet(b, pos=0, align=True):
    start = pos + 0
    pversion = b[pos:pos+3]
    ptype = b[pos+3:pos+6]
    pos = pos + 6

    if ptype.uint == 4:
        value, pos = parse_literals(b, pos, align=align)
        packet = Literal(packet_version=pversion.uint, start=start, end=pos-1, value=value)
    else:
        packets, pos = parse_operator(b, pos)
        packet = Operator(packet_version=pversion.uint, start=start, end=pos-1, 
                          packet_type=ptype.uint, children=packets)
    return packet, pos

def parse_literals(b, pos, align=True):
    start = pos + 0
    b_value = bitstring.BitArray()
    while b[pos]:
        b_value.append(b[pos+1 : pos+5])
        pos += 5
    b_value.append(b[pos+1 : pos+5])
    pos += 5
    if align:
        pos = math.ceil(pos/4) * 4
    return b_value.uint, pos

def parse_operator(b, pos):
    if b[pos]:
        return parse_operator_num(b, pos+1)
    else:
        return parse_operator_length(b, pos+1)

def parse_operator_length(b, pos):
    length = b[pos:pos+15].uint
    pos += 15
    pfinal = pos + length
    packets = []
    while pos < pfinal:
        packet, pos = parse_next_packet(b, pos, align=False)
        packets.append(packet)
    return packets, pos

def parse_operator_num(b, pos):
    num = b[pos:pos+11].uint
    pos += 11
    packets = []
    i = 0
    while i < num:
        packet, pos = parse_next_packet(b, pos, align=False)
        packets.append(packet)
        i += 1  
    return packets, pos

def sum_versions(packet):
    if type(packet) is Literal:
        return packet.packet_version
    else:
        return packet.packet_version + sum([sum_versions(p) for p in packet.children])

with open('input.txt') as f:
    transmission = f.read().strip()
b_transmission = bitstring.Bits('0x' + transmission)

packet, _ = parse_next_packet(b_transmission)

print("sum of versions = ", sum_versions(packet))