from enum import Enum, auto


class FuncaoRegistrador(Enum):
    mt_tipo_motor = auto()                  #"descricao":	"Tipo do motor (0 = Desligado, 1 = Verde ou 2 = Azul)"
    mt_habilita = auto()                    #"descricao":	"Indica Motor (0 = Rodando ou 1 = Parado)"
    mot_sel_driver = auto()                 #"descricao":	"Seleciona o Tipo de Partida  (Soft-start = 1, Inversor = 2, Direta = 3)"
    mot_ats48 = auto()                      #"descricao":	"Controla partida Soft-start (Liga = 1, Desliga = 0, Reset = 2) "
    mot_ats48_acc = auto()                  #"descricao":	"Define a rampa de aceleração do soft-start (10s a 60s)"
    mot_ats48_dcc = auto()                  #"descricao":	"Define a rampa de desaceleração do soft-start (10s a 60s)"
    mot_atv31 = auto()                      #"descricao":	"Controla partida Inversor (Liga = 1, Desliga = 0, Reset = 2) "
    mot_atv31_velocidade = auto()           #"descricao":	"Define a velocidade do Inversor (0 a 60Hz)"
    mot_atv31_acc = auto()                  #"descricao":	"Define a rampa de aceleração do inversor (10s a 60s)
    mot_atv31_dcc = auto()                  #"descricao":	"Define a rampa de desaceleração do inversor (10s a 60s)
    mot_tesys = auto()                      #"descricao":	"Controla partida Direta (Liga = 1, Desliga = 0, Reset = 2)
    mot_indica_driver = auto()              #confere com sel_driver
    mot_status_ats48 = auto()               #confere ats48 1 ligado 0 desligado
    mot_status_atv31 = auto()               #confere atv31 1 ligado 0 desligado
    mot_status_tesys = auto()               #confere tesys 1 ligado 0 desligado
    
    float = auto()                          #parametros:    ["valor para motor desligado","valor para motor ligado em maxima rotacao", "erro em porcentagem"]

    pass

"""
class MomentoMedida(Enum):
    verifica_estado = auto()
    motor_ligado = auto()
    motor_desligado = auto()
    
    pass
"""