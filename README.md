# Redes de Computadores

# Estrutura do Projeto

[proj_sockets] => [app] => [dns]
        |           |        |
        |           |        [const.py] 
        |           |        |
        |           |        [dns.py]
        |           |        |
        |           |        [logger.py]
        |           |
        |           |
        |           |
        |           |-----=> [tcp]
        |           |          |
        |           |          [clienteTCP.py]
        |           |          |
        |           |          [const.py]
        |           |          |
        |           |          [logger.py]
        |           |          |
        |           |          [servidorTCP.py]
        |           |
        |           |
        |           |------=> [udp]
        |           |          |
        |           |          [clienteUDP.py]
        |           |          |
        |           |          [cosnt.py]
        |           |          |
        |           |          [logger.py]
        |           |          |
        |           |          [servidorUDP.py]
        |           |
        |           |
        |           |------=> [.idea]
        |
        |
        |
        |------=>[pictures]=> [wireshark.png]
        |                            |
        |                     [tcp-dns.png]
        |                            |
        |                     [udp-dns.png]  
        |
        |
        |--------=> [.idea]
        |
        |
        |--------=> [venv]
