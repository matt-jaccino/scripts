import socket
from argparse import ArgumentParser
from pathlib import Path


PACKET_SIZE = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_file(ip_addr: str, port: int, filename: str):
    if not Path(filename).exists():
        raise ValueError(f"The file '{filename}' does not exist!")

    print(f"Sending file '{filename}' to {ip_addr} over port {port}.")
    try:
        sock.connect((ip_addr, port))
    except Exception as exc:
        raise RuntimeError(
            f"Unable to connect to host: {exc}\n\n"
            "Is the host ready to receive files (running with `--mode R`)?"
        )
    print("  Connected.")

    print("  Sending file...")
    with open(filename, 'rb') as fp:
        sock.sendall(fp.read())

    print("  Done.")
    sock.close()


def recv_file(ip_addr: str, port: int, filename: str):
    if Path(filename).exists():
        print(f"The file '{filename}' already exists and will be overwritten!")

    print(f"Listening on {ip_addr} over port {port} to receive file '{filename}'.")
    sock.bind((ip_addr, port))
    sock.listen(1)
    print("  Waiting for client...")

    client, (client_addr, client_port) = sock.accept()
    print(f"  Receieved connection from {client_addr} over port {client_port}.")
    print(f"  Writing the content of the packets into '{filename}'.")
    with open(filename, 'wb') as fp:
        while file_bytes := client.recv(PACKET_SIZE):
            fp.write(file_bytes)

    print("  Done.")
    sock.close()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--ip-address",
        help="IP to send file to if sending or local address if receiving",
        type=str,
        required=True
    )
    parser.add_argument(
        "--port",
        help="Port to send file to if sending or receive on if receiving",
        type=int,
        required=True
    )
    parser.add_argument(
        "--file",
        help="Path to file to send if sending or write to if receiving",
        type=str,
        required=True
    )
    parser.add_argument(
        "--mode",
        help="[S]ending or [R]eceiving?",
        type=str,
        choices=['S', 'R'],
        required=True
    )

    args = parser.parse_args()

    if args.mode == 'S':
        print("*** SEND MODE ***")
        send_file(ip_addr=args.ip_address, port=args.port, filename=args.file)
    else:
        print("*** RECEIVE MODE ***")
        recv_file(ip_addr=args.ip_address, port=args.port, filename=args.file)


main()
