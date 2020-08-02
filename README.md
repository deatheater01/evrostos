███████╗██╗░░░██╗██████╗░░█████╗░░██████╗████████╗░█████╗░░██████╗
██╔════╝██║░░░██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝
█████╗░░╚██╗░██╔╝██████╔╝██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░
██╔══╝░░░╚████╔╝░██╔══██╗██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗
███████╗░░╚██╔╝░░██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝
╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░

    
Covert Communications network

This is just a proof of concept.

Here the file is compressed and added into ip6 packet headers with a delay and sent

It requires python module scapy it is available through

`pip install scapy`

In this we set the flow label field of the ipv6 header to the required data. This can be done without affecting the transmission.

This is an inspiration from https://medium.com/@danielabloom/covert-channels-demystified-4b1f406a76e3.

# Usage
`remote_node.py -h`

Note : Both the files must be run with admin privileges.

