import socket
from logger import Logger
from const import HOST, SERVER_DNS, PORT_UDP

logger = Logger("UDP CLIENT")

DOMAIN_NAME = "udp_server"

media = ["(9 + 8)/2"]


def get_media():
    if media:
        return media.pop(0)
    else:
        return None


def send_dns_query(domain_name: str) -> tuple:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp:
            client_udp.sendto(domain_name.encode(), (HOST, SERVER_DNS))
            server_address = client_udp.recv(1024).decode()
            ip_address, server_port = server_address.split(":")

        return ip_address, int(server_port)

    except Exception as e:
        logger.log(f"Error resolving domain'{domain_name}': {str(e)}")
        return None, None


def resolve_equation(ip_address: str, equation: str) -> str:
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_udp.sendto(equation.encode(), (ip_address, PORT_UDP))
        result = client_udp.recv(1024).decode()
        try:
            media_calculada = eval(result)
            name = "Samara"
            if media_calculada >= 7.0:
                status = "Aprovado"
            else:
                status = "Reprovado"
        except Exception as e:
            status = "Erro ao calcular a média"

        return f"Aluna: {name}, Nota: {result}, Status: {status}"
    except Exception as e:
        print(f"Erro ao resolver a equação: {e}")
        return "Erro ao resolver a equação"
    finally:
        client_udp.close()


def udp_client():
    executed = False

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
        logger.log("Encerrando cliente UDP")


def send_server(command):
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client_udp.sendto(command.encode(), (HOST, PORT_UDP))
    except Exception as e:
        logger.log(f"Erro ao enviar comando para o servidor: {e}")
    finally:
        client_udp.close()


if __name__ == "__main__":
    udp_client()
    input("pressione ENTER para sair...")
