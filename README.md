███████╗██╗░░░██╗██████╗░░█████╗░░██████╗████████╗░█████╗░░██████╗
██╔════╝██║░░░██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝
█████╗░░╚██╗░██╔╝██████╔╝██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░
██╔══╝░░░╚████╔╝░██╔══██╗██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗
███████╗░░╚██╔╝░░██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝
╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░

    
Covert Communications network

base_node.py is the server side code
remote_node.py is the client side or the node from which data must be transferred

It requires python module scapy it is available through

`pip install scapy`

In this we set the flow label field of the ipv6 header to the required data. This can be done without affecting the transmission.

This is an inspiration from https://medium.com/@danielabloom/covert-channels-demystified-4b1f406a76e3.

# Usage
`base_node.py -h`
`remote_node.py -h`

Note both the files must be run with admin privileges.

