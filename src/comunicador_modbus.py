from sre_constants import RANGE
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from threading import Lock 
from pymodbus.constants import Endian
from src.registrador import Registrador, TipoDeLeitura

class ComunicadorModbus():
    Ip:str
    Porta:int
    _cliente:ModbusClient

    def __init__(self,Ip:str , Porta:int) -> None:
        """
        Ip: string, ip para se conectar
        Porta: int, numero da porta da conecçao
        """
        self.Ip = Ip
        self.Porta = Porta
        self.lock = Lock()
        pass

    def connect(self) -> bool:
        try:
            self._cliente =  ModbusClient(host=self.Ip,port = self.Porta)
            return(True)
        except Exception as e:
            print("Erro ao conectar: ", e.args)
            return(False) 

    def close_connection(self) -> bool:
        try:
            self._cliente.close()
            return(True)
        except Exception as e:
            print("Erro ao fechar conecção: ", e.args)
            return(False) 
            
    def __leitura(self, endereco:int, tipo:int, tamanho:int = [1]) -> list:
        """
        endereco: int, porta do registrador
        tipo: int, (coil = 0, discrete_input = 1, holding_register = 2, input_register = 3)
        tamanho: int, numero de endereço a ser lido
        """
        retorno:list
        # with self.lock:
        if tipo == 0:
            retorno = self._cliente.read_coils(endereco,tamanho)
        
        elif tipo == 1:
            retorno = self._cliente.read_discrete_inputs(endereco,tamanho)
        
        elif tipo == 2:
            retorno = self._cliente.read_holding_registers(endereco,tamanho)

        elif tipo == 3:
            retorno = self._cliente.read_input_registers(endereco,tamanho)
        else:
            print("comunicador_modbus.escreve(), parametro tipo errado :",tipo)
            retorno = [-666]    
        return retorno

    def escrita(self, endereco:int, tipo:int, valor:list)->bool:
        """
        endereco: int, porta do registrador
        tipo: int, (coil = 0, holding_register = 2)
        valor: lista, lista de valores a serem escritos
        """
        try:
            with self.lock:
                if tipo == 0:
                    self._cliente.write_multiple_coils(endereco,valor)
                if tipo == 2:
                    self._cliente.write_multiple_registers(endereco,valor)
        except Exception as e:
            print("Erro de escrita: ",e.args())
        return False

    def __leitura_fp(self, endereco:int, tipo:int = 2, tamanho:int = 1) ->list:
        """
        leitura tamanho*2 enderecos seguidos e transforma em lista de 32bit_float

        endereco: int, porta do primeiro registrador
        tipo: int, (holding_register = 2, input_register = 3)
        tamanho: int, numero de float_points a serem lidos 
        """
        if tipo != 2 and tipo != 3:
            print("Erro leitura_fps(), tipo errado: ",tipo)
            return [0]
        
        bpd = BinaryPayloadDecoder.fromRegisters(self.leitura(endereco,tipo,tamanho*2),byteorder=Endian.BIG,wordorder=Endian.LITTLE)
        saida = list()
        for i in range(0,tamanho):
            saida.append(bpd.decode_32bit_float())
        
        return saida

    def escrita_fp(self, endereco:int, valor:list) -> bool:
        """
        escreve 32bit_float nos registradores

        endereco: int, porta do primeiro registrador
        valor: int, lista de floats a serem escritos 
        """
        bpb = BinaryPayloadBuilder()
        for val in valor:
            bpb.add_32bit_float(val)
        self.escrita(endereco,2,bpb.to_registers())

        return True

    def __leitura_4x_embits(self, endereco:int, tamanho:int = 1) -> list:
        
        """
        leitura de holding em formato de bits

        endereco: int, porta do primeiro registrador
        tamanho: int, numero de holdings a serem lidos
        """
        bpd = BinaryPayloadDecoder.fromRegisters(self.leitura(endereco,2,tamanho))
        listaBits = list()
        for i in range(0,tamanho):
            # list1 = bpd.decode_bits()
            # list2 = bpd.decode_bits()
            # listaBits.append(list2+list1)

            listaBits.append(bpd.decode_bits()+bpd.decode_bits())
        # print(listaBits)
        return listaBits

    def escrita_4x_embits(self, endereco:int, valor:list) -> bool:
        """
        escrita de holding em formato de bits

        endereco: int, porta do primeiro registrador
        valor: lista, lista  de bits em pack de 16
        """
        bpb = BinaryPayloadBuilder()
        for val in valor:
            bpb.add_bits(val)
        self.escrita(endereco,2,bpb.to_registers())
        return True
    
    def leitura_manual(self, endereco:int, tipo:int, tamanho:int = [1]) -> list:
        return self.__leitura(endereco,tipo,tamanho)
    
    def get_leitura_4x_embits(self, endereco:int, tamanho:int = 1) -> list:
        retorno = None
        with self.lock:
            retorno = self.__leitura_4x_embits(endereco,tamanho)
        return retorno
    
    def leitura_de_registrador(self, registradores:list) -> None:
        
        with self.lock:
            for registrador in registradores:
                if registrador.tipo_leitura == TipoDeLeitura.normal:
                    registrador.set_valor_de_leitura(self.__leitura(registrador.endereco,registrador.tipo_registrador.value,1)[0])
                    pass
                elif registrador.tipo_leitura == TipoDeLeitura.float_32bit:
                    registrador.set_valor_de_leitura(self.__leitura_fp(registrador.endereco,registrador.tipo_registrador.value,1)[0])
                    pass
                elif registrador.tipo_leitura == TipoDeLeitura.bit_4x:
                    bit = 0
                    if self.bit_de_leitura < 8:
                        bit = registrador.bit_de_leitura+8
                    else:
                        bit = registrador.bit_de_leitura+8
                    registrador.set_valor_de_leitura(self.__leitura_4x_embits(registrador.endereco)[0][bit])
                    pass
            pass

        pass

if __name__ == "__main__":
    
    pass