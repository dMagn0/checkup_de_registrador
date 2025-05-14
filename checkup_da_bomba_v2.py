import maquinas.bomba as bomba
import numpy as np
from src.funcao_registrador import FuncaoRegistrador
from src.comunicador_modbus import ComunicadorModbus
from src.registrador import ListaRegistrador, Registrador
from threading import Thread
from time import sleep
import sys
from threading import Lock 
from src.checkup_bancada import CheckupBancada


def main_func():

    cb = CheckupBancada(bomba.get_bomba_ip(),bomba.get_bomba_port(),caminho_pasta = "saida",nome_bancada="bomba")
    
    cb.set_controle_motor(bomba.get_reg_motor())
    cb.set_registrador_motor(bomba.get_reg_saida_motor())
    cb.set_registrador_linear(bomba.get_reg_saida_bancada())
    cb.start()
 
if __name__=="__main__":
    # cb = CheckupBancada(bomba.get_bomba_ip(),bomba.get_bomba_port(),caminho_pasta = "saida",nome_bancada="bomba")
    cb = CheckupBancada(bomba.get_bomba_ip(),bomba.get_bomba_port(),caminho_pasta = "saida",nome_bancada="teste",debug=True)
    cb.set_controle_motor(bomba.get_reg_motor())
    cb.set_registrador_motor(bomba.get_reg_saida_motor())
    cb.set_registrador_linear(bomba.get_reg_lin())
    cb.comeca_checkup()
