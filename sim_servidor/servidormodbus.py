from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random

class ServidorMODBUS():
    """
    Classe Servidor MODBUS
    """
    def __init__(self, host_ip,port):
        """
        Construtor
        """

        self._server =  ModbusServer(host=host_ip, port=port,no_block=True)
    
    def run(self):
        """
         Execução do servidor
        """
        self._server.start()
        print("Servidor em execução")
        print("--------------------")
        self._server.data_bank.set_holding_registers(708,[1]) # mt_tipo_motor
        self._server.data_bank.set_holding_registers(1328,[2]) #mt_habilita
        print("--------------------\n\n")
        while True:
            i = int(input("Leitura = 0, Escrita = 1:\n"))
            if i == 1:
                addr = int(input("Endereco de escrita:"))
                val = int(input("valor de escrita:"))
                self._server.data_bank.set_holding_registers(addr,[val])
                print(f"valor ({self._server.data_bank.get_holding_registers(addr)}) escrito no endereco {addr}\n")
            elif i == 0:
                addr = int(input("Endereco de leitura:"))
                print(f"valor lido: {self._server.data_bank.get_holding_registers(addr)}\n")
            else:
                break
        # 64323, 32, 5446, 43618

if __name__ == "__main__":
    s = ServidorMODBUS('localhost',502)
    s.run()