import socket
from logger import Logger
from const import HOST, PORT_UDP

logger = Logger("UDP SERVER")


def create_udp_socket(host: str, port: int) -> socket:
    """
    Creates a UDP socket with the given host and port.

    Args:
        host (str): The IP address or hostname of the server.
        port (int): The port number to bind the socket to.

    Returns:
        socket: The created UDP socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    return server_socket


def handle_client_udp(
    server_socket: socket, client_address: tuple, data: bytes
) -> None:
    logger.log(f"Connection established with {client_address}")
    try:
        expression = data.decode()
        result = eval(expression)
        logger.log(f"{expression} = {result}")
        server_socket.sendto(str(result).encode(), client_address)

    except (SyntaxError, NameError, ZeroDivisionError) as e:
        logger.log(f"Error evaluating expression: {str(e)}")
        server_socket.sendto(str(e).encode(), client_address)


def main():
    server_socket = create_udp_socket(HOST, PORT_UDP)
    logger.info(f"UDP Server is running on {HOST}:{PORT_UDP}")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            if not data:
                break
            handle_client_udp(server_socket, client_address, data)

    except KeyboardInterrupt:
        logger.log("Exiting...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
