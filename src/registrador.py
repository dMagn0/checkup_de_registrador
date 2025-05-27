from enum import Enum
from src.comunicador_modbus import ComunicadorModbus
from src.funcao_registrador import FuncaoRegistrador

class TipoRegistrador(Enum):
    coil = 0
    discrete_input = 1
    holding_register = 2
    input_register = 3
    pass
class TipoDeLeitura(Enum):
    normal = 0
    float_32bit = 1
    bit_4x = 2
    pass


class Registrador():
    endereco:int
    tipo_registrador:TipoRegistrador
    tipo_leitura:TipoDeLeitura
    _comunicadorModbus:ComunicadorModbus
    valor_de_leitura:float = None
    bit_de_leitura:int = -1
    divisor:int
    nome:str
    funcao:FuncaoRegistrador
    valores_de_escrita:list
    descricao:str

    valor_esperado_desligado:list
    valor_esperado_ligado:list
    erro:float
    variacao_por_rotacao:bool
    confere:bool
    somente_varicao:bool

    def __init__(self, com:ComunicadorModbus, variaveis:dict) -> None:
        self._comunicadorModbus = com
        try:
            self.endereco = variaveis["addr"]
            self.tipo_registrador = TipoRegistrador.holding_register
            self.bit_de_leitura = variaveis["bit"]
            if variaveis["tipo"] == "FP":
                self.tipo_leitura = TipoDeLeitura.float_32bit
            elif variaveis["tipo"] == "4X":
                if self.bit_de_leitura == -1:
                    self.tipo_leitura = TipoDeLeitura.normal
                else:
                    self.tipo_leitura = TipoDeLeitura.bit_4x
            self.divisor = variaveis["divisor"]
            self.nome = variaveis.get("nome")
            #self.descricao = variaveis.get("descricao")
            self.funcao = variaveis.get("funcao")
            self.valores_de_escrita = variaveis.get("valores_de_escrita")
            self.descricao = variaveis.get("descricao")
            self.somente_varicao = variaveis.get("somente_variacao",False)
            ##
            temp = variaveis.get("valor")
            if temp == None:
                self.valor_esperado_desligado = variaveis.get("valor_desligado")
                self.valor_esperado_ligado = variaveis.get("valor_ligado")
            else:
                self.valor_esperado_desligado = temp
                self.valor_esperado_ligado = temp
            
            temp = variaveis.get("variacao_por_rotacao")
            if temp == None:
                self.variacao_por_rotacao = False
            else:
                self.variacao_por_rotacao = temp

            self.erro = variaveis.get("erro")

            temp = variaveis.get("confere")
            if temp == None:
                self.confere = False
            else:
                self.confere = temp

            pass
        except Exception as e:
            print("Erro de criação de registrador: ", e.args)
            return
        pass
    def _set_valor_de_leitura(self, valor:float ) -> None:
        try:
            self.valor_de_leitura = valor/self.divisor
        except Exception as e:
            print(f"excecao na leitura do endereco {self.endereco}: ",e)
            self.valor_de_leitura = None    
        pass

    def leitura(self):
        self._comunicadorModbus.leitura([self])
        return

    def escrita(self,valor) -> bool:
        
        valor = valor*self.divisor
        
        if self.tipo_leitura == TipoDeLeitura.normal:
            self._comunicadorModbus.escrita(self.endereco,self.tipo_registrador.value,[(int)(valor)])
            pass
        elif self.tipo_leitura == TipoDeLeitura.float_32bit:
            self._comunicadorModbus.escrita_fp(self.endereco, [(float)(valor)])
            pass
        elif self.tipo_leitura == TipoDeLeitura.bit_4x:
            if (int)(valor)!=1 and (int)(valor)!=0:
                print("erro de escrita. Valor(",(int)(valor),") deve ser 1 ou 0")
                return False
            leitura = self._comunicadorModbus.get_leitura_4x_embits(self.endereco)[0]
            if self.bit_de_leitura < 8:
                bit = self.bit_de_leitura+8
            else:
                bit = self.bit_de_leitura-8

            leitura[bit]=(int)(valor)
            self._comunicadorModbus.escrita_4x_embits(self.endereco, [leitura])
            pass
        else:
            print("erro de escrita, widget ",self.endereco,", ",self.tipo_registrador)
            return False
        
        return True
    