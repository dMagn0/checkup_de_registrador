import maquinas.bomba as bomba
import maquinas.esteira as esteira
import maquinas.ventilador as ventilador
import maquinas.compressor as compressor

import numpy as np
from src.funcao_registrador import FuncaoRegistrador
from src.comunicador_modbus import ComunicadorModbus
from src.registrador import ListaRegistrador, Registrador
from threading import Thread
from time import sleep
import sys
from threading import Lock 

from src.checkup_bancada import CheckupBancada


def ckp_bomba():

    cb = CheckupBancada(bomba.get_bomba_ip(),bomba.get_bomba_port(),caminho_pasta = "saida\\bomba",nome_bancada="bomba_28_01", debug = True)
    
    cb.set_controle_motor(bomba.get_reg_motor())
    cb.set_registrador_motor(bomba.get_reg_saida_motor())
    cb.set_registrador_linear(bomba.get_reg_lin())
    cb.comeca_checkup()

def ckp_esteira():

    cb = CheckupBancada(esteira.get_esteira_ip(),esteira.get_esteira_port(),caminho_pasta = "saida\\esteira",nome_bancada="esteira_28_01", debug = True)
    
    cb.set_controle_motor(esteira.get_reg_motor())
    cb.set_registrador_motor(esteira.get_reg_saida_motor())
    #cb.set_registrador_linear(esteira.get_reg_saida_bancada())
    cb.comeca_checkup()

def ckp_ventilador():

    cb = CheckupBancada(ventilador.get_ventilador_ip(),ventilador.get_ventilador_port(),caminho_pasta = "saida\\ventilador",nome_bancada="ventilador_28_01", debug = True)
    
    cb.set_controle_motor(ventilador.get_reg_motor())
    cb.set_registrador_motor(ventilador.get_reg_saida_motor())
    #cb.set_registrador_linear(ventilador.get_reg_saida_bancada())
    cb.comeca_checkup()

def ckp_compressor():

    cb = CheckupBancada(compressor.get_compressor_ip(),compressor.get_compressor_port(),caminho_pasta = "saida",nome_bancada="compressor")
    
    cb.set_controle_motor(compressor.get_reg_motor())
    #cb.set_registrador_motor(compressor.get_reg_saida_motor())
    #cb.set_registrador_linear(compressor.get_reg_saida_bancada())
    cb.comeca_checkup()

if __name__=="__main__":
    r = int(input("bomba = 0, esteira = 1, ventilador = 2\n::"))
    
    if r == 0:
        ckp_bomba()
    if r == 1:
        ckp_esteira()
    if r == 2:
        ckp_ventilador()
        pass
        