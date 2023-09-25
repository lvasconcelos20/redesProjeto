import socket
from logger import Logger
from const import HOST, SERVER_DNS, PORT_TCP

logger = Logger("TCP CLIENT")

DOMAIN_NAME = "tcp_server"

media = ["(6 + 6)/2"]


def get_media():
    if media:
        return media.pop(0)  # tira e retorna o primeiro item da lista
    else:
        return None


def send_dns_query(domain_name: str) -> tuple:
    """
    Finds the IP address of a domain name using a DNS server.

    Args:
        domain_name (str): The domain name to be resolved.

    Returns:
        tuple: A tuple containing the IP address (str) and the server port (int) of the domain name.
    """
    try:
        # Create a UDP socket for DNS resolution
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp:
            # Send a DNS query to resolve the domain name
            client_udp.sendto(DOMAIN_NAME.encode(), (HOST, SERVER_DNS))
            server_address = client_udp.recv(1024).decode()
            ip_address, server_port = server_address.split(":")

        return ip_address, int(server_port)

    except Exception as e:
        # Handle any exceptions that may occur during DNS resolution
        logger.log(f"Error resolving domain '{domain_name}': {str(e)}")
        return None, None


def resolve_equation(ip_address: str, equation: str) -> str:
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_tcp.settimeout(5)
        client_tcp.connect((ip_address, PORT_TCP))
        client_tcp.sendall(equation.encode())
        result = client_tcp.recv(1024).decode()

        # Calcular se o aluno foi aprovado ou não com base no resultado da equação
        try:
            nome = "João"
            media_calculada = eval(result)  # Avaliar a expressão para calcular a média
            if media_calculada >= 7.0:
                status = "Aprovado"
            else:
                status = "Reprovado"
        except Exception as e:
            status = "Erro ao calcular a média"

        return f"Aluno: {nome}, Nota: {result}, Status: {status}"

    except Exception as e:
        print(f"Erro ao resolver a equação: {e}")
        return "Erro ao resolver a equação"

    finally:
        client_tcp.close()


def tcp_client():
    executed = False  # Variável de controle para verificar se já executou

    try:
        while not executed:
            expression = get_media()
            if expression:
                logger.log(f"A média é: {expression}")

                ip_address, server_port = send_dns_query(f"{DOMAIN_NAME}")
                if ip_address:
                    result = resolve_equation(ip_address, expression)
                    logger.log(result)
                else:
                    logger.log("Servidor não encontrado para esse nome.")

                executed = True  # Define como True após a primeira execução
            else:
                logger.log("Todas as expressões de média foram usadas.")
    except KeyboardInterrupt:
        send_server("sair")
        logger.log("Aplicação encerrada pelo usuário")
    except Exception as e:
        logger.log(f"Erro: {e}")
    finally:
        logger.log("Encerrando cliente TCP")


def send_server(command):
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_tcp.connect((HOST, PORT_TCP))
    client_tcp.sendall(command.encode())
    client_tcp.close()


if __name__ == "__main__":
    tcp_client()
    input("pressione enter para sair...")
