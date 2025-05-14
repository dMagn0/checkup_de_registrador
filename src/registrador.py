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
    valor_de_leitura = None
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

    def leitura(self):
        try:
            if self.tipo_leitura == TipoDeLeitura.normal:
                self.valor_de_leitura = self._comunicadorModbus.leitura(self.endereco,self.tipo_registrador.value,1)[0]
                pass
            elif self.tipo_leitura == TipoDeLeitura.float_32bit:
                self.valor_de_leitura = self._comunicadorModbus.leitura_fp(self.endereco,self.tipo_registrador.value,1)[0]
                pass
            elif self.tipo_leitura == TipoDeLeitura.bit_4x:
                if self.bit_de_leitura < 8:
                    bit = self.bit_de_leitura+8
                else:
                    bit = self.bit_de_leitura+8
                self.valor_de_leitura = self._comunicadorModbus.leitura_4x_embits(self.endereco)[0][bit]
                pass

            self.valor_de_leitura = self.valor_de_leitura/self.divisor
        except Exception as e:
            print(f"excecao na leitura do endereco {self.endereco}: ",e)
            self.valor_de_leitura = None
        return

    def escrita(self,valor) -> bool:
        
        valor = valor*self.divisor

        """if self.escrita_restrita == True:
            if valor not in self.valores_de_escrita:
                print("valor errado: ", self.nome,":",valor)
                return False"""
        
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
            leitura = self._comunicadorModbus.leitura_4x_embits(self.endereco)[0]
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
    
class ListaRegistrador():
    lista_registradores_comando:list
    lista_registradores_flutuantes:list
    _reg_tipo_motor:Registrador
    def get_tipo_motor(self) -> Registrador:return(self._reg_tipo_motor)
    _reg_habilita:Registrador
    def get_habilita(self) -> Registrador:return(self._reg_habilita)
    _reg_sel_driver:Registrador
    def get_sel_driver(self) -> Registrador:return(self._reg_sel_driver)
    _reg_ats48:Registrador
    def get_ats48(self) -> Registrador:return(self._reg_ats48)
    _reg_ats48_acc:Registrador
    def get_ats48_acc(self) -> Registrador:return(self._reg_ats48_acc)
    _reg_ats48_dcc:Registrador
    def get_ats48_dcc(self) -> Registrador:return(self._reg_ats48_dcc)
    _reg_atv31:Registrador
    def get_atv31(self) -> Registrador:return(self._reg_atv31)
    _reg_atv31_velocidade:Registrador
    def get_atv31_velocidade(self) -> Registrador:return(self._reg_atv31_velocidade)
    _reg_atv31_acc:Registrador
    def get_atv31_acc(self) -> Registrador:return(self._reg_atv31_acc)
    _reg_atv31_dcc:Registrador
    def get_atv31_dcc(self) -> Registrador:return(self._reg_atv31_dcc)
    _reg_tesys:Registrador
    def get_tesys(self) -> Registrador:return(self._reg_tesys)
    _reg_indica_driver:Registrador
    def get_indica_driver(self) -> Registrador:return(self._reg_indica_driver)
    _reg_status_ats48:Registrador
    def get_status_ats48(self) -> Registrador:return(self._reg_status_ats48)
    _reg_status_atv31:Registrador
    def get_status_atv31(self) -> Registrador:return(self._reg_status_atv31)
    _reg_status_tesys:Registrador
    def get_status_tesys(self) -> Registrador:return(self._reg_status_tesys)


    def __init__(self, lista_regs:list, com:ComunicadorModbus = None) -> None:
        self.lista_registradores_comando = []
        self.lista_registradores_flutuantes = []

        for m in lista_regs:
            reg = Registrador(com,m)
            self.add_reg(reg)
            pass
        pass
    
    def add_reg(self, reg:Registrador):
        func = reg.funcao
        if func == FuncaoRegistrador.mt_tipo_motor:
            self._reg_tipo_motor = reg
            pass
        elif func == FuncaoRegistrador.mt_habilita:
            self._reg_habilita = reg
            pass
        elif func == FuncaoRegistrador.mot_sel_driver:
            self._reg_sel_driver = reg
            pass
        elif func == FuncaoRegistrador.mot_ats48:
            self._reg_ats48 = reg
            pass
        elif func == FuncaoRegistrador.mot_ats48_acc:
            self._reg_ats48_acc = reg
            pass
        elif func == FuncaoRegistrador.mot_ats48_dcc:
            self._reg_ats48_dcc = reg
            pass
        elif func == FuncaoRegistrador.mot_atv31:
            self._reg_atv31 = reg
            pass
        elif func == FuncaoRegistrador.mot_atv31_velocidade:
            self._reg_atv31_velocidade = reg
            pass
        elif func == FuncaoRegistrador.mot_atv31_acc:
            self._reg_atv31_acc = reg
            pass
        elif func == FuncaoRegistrador.mot_atv31_dcc:
            self._reg_atv31_dcc = reg
            pass
        elif func == FuncaoRegistrador.mot_tesys:
            self._reg_tesys = reg
            pass
        elif func == FuncaoRegistrador.mot_indica_driver:
            self._reg_indica_driver = reg
            pass
        elif func == FuncaoRegistrador.mot_status_ats48:
            self._reg_status_ats48 = reg
            pass
        elif func == FuncaoRegistrador.mot_status_atv31:
            self._reg_status_atv31 = reg
            pass
        elif func == FuncaoRegistrador.mot_status_tesys:
            self._reg_status_tesys = reg
            pass
        elif func == FuncaoRegistrador.float:
            self.lista_registradores_flutuantes.append(reg)
            pass
        else:
            self.lista_registradores_comando.append(reg)
        pass