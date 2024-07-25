import psutil
import socket
import logging

# Configuração de logging
logging.basicConfig(filename='vpn_invasao.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para verificar se um processo está rodando
def verificar_processo(nome_processo):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == nome_processo:
            return True
    return False

# Função para verificar se uma conexão VPN está ativa
def verificar_vpn():
    for conn in psutil.net_connections(kind='all'):
        if conn.status == 'ESTABLISHED' and conn.type == 'SOCK_STREAM':
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((conn.laddr.ip, conn.laddr.port))
                sock.close()
                if conn.raddr.ip != '127.0.0.1' and conn.raddr.ip != '::1':
                    logging.info(f'Conexão VPN detectada: {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}')
                    return True
            except socket.error:
                pass
    return False

# Função para verificar se há tentativas de invasão
def verificar_invasao():
    if verificar_vpn():
        logging.warning('Tentativa de invasão via VPN detectada!')
        # Aqui você pode adicionar ações para bloquear a conexão VPN ou notificar o administrador
    else:
        logging.info('Nenhuma tentativa de invasão via VPN detectada.')

# Verificar se o processo de VPN está rodando
if verificar_processo('openvpn.exe') or verificar_processo('vpn.exe'):
    logging.info('Processo de VPN detectado.')
    verificar_invasao()
else:
    logging.info('Nenhum processo de VPN detectado.')

# Agendar a verificação para ser executada a cada 5 minutos
import schedule
import time

def verificar_invasao_agendada():
    verificar_invasao()
    schedule.every(5).minutes.do(verificar_invasao_agendada)

verificar_invasao_agendada()
while True:
    schedule.run_pending()
    time.sleep(1)
