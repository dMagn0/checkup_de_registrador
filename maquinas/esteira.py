from src.funcao_registrador import FuncaoRegistrador

def get_esteira_ip() ->str:
    return '10.15.20.24'
    return 'localhost'
def get_esteira_port() ->str:
    return 502

def get_reg_motor() -> list:
    return [   
        #controle do motor             
        {"funcao": FuncaoRegistrador.mt_tipo_motor,
            "tipo": "4X",
            "addr": 708,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mt_habilita,
            "tipo": "4X",
            "addr": 1330,
            "bit": 0,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_indica_driver,
            "tipo": "4X",
            "addr": 1216,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_status_ats48,
            "tipo": "4X",
            "addr": 886,
            "bit": -1,
            "divisor": 1,
        },
        {"funcao": FuncaoRegistrador.mot_status_atv31,
            "tipo": "4X",
            "addr": 888,
            "bit": -1,
            "divisor": 1,
        },
        {"funcao": FuncaoRegistrador.mot_status_tesys,
            "tipo": "4X",
            "addr": 890,
            "bit": -1,
            "divisor": 1,
        },
        {"funcao": FuncaoRegistrador.mot_sel_driver,
            "tipo": "4X",
            "addr": 1324,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_ats48,
            "tipo": "4X",
            "addr": 1316,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_ats48_acc,
            "tipo": "4X",
            "addr": 1317,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_ats48_dcc,
            "tipo": "4X",
            "addr": 1318,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_atv31,
            "tipo": "4X",
            "addr": 1312,
            "bit": -1,
            "divisor": 1
        },
        {"funcao": FuncaoRegistrador.mot_atv31_velocidade,
            "tipo": "4X",
            "addr": 1313,
            "bit": -1,
            "divisor": 10
        },
        {"funcao": FuncaoRegistrador.mot_atv31_acc,
            "tipo": "4X",
            "addr": 1314,
            "bit": -1,
            "divisor": 10
        },
        {"funcao": FuncaoRegistrador.mot_atv31_dcc,
            "tipo": "4X",
            "addr": 1315,
            "bit": -1,
            "divisor": 10
        },
        {"funcao": FuncaoRegistrador.mot_tesys,
            "tipo": "4X",
            "addr": 1319,
            "bit": -1,
            "divisor": 1
        }
    ]
    pass

"""
def get_reg_controle() -> list:
    return None
    pass

"""

def get_estado_desligado() -> list:
    return [[0]
    ]
def get_estado_ligado() -> list:
    return [[0]
    ]
    pass

def get_reg_saida_motor() ->list:
    return [
        {"tipo": "FP", "addr": 884,"bit": -1, "nome": "es.encoder", "divisor": 1, "descricao": "Medida da Rotação do Motor (RPM)", "valor_desligado" : [0,0.1], "valor_ligado": [3100,1000], "variacao_por_rotacao": True},
        {"tipo": "FP", "addr": 1420,"bit": -1, "nome": "es.torque", "divisor": 100, "descricao": "Medida do Torque do motor", "valor_desligado" : [0,0.1], "valor_ligado": [2.2,1.2], "variacao_por_rotacao": True},
        {"tipo": "FP", "addr": 700,"bit": -1, "nome": "es.temp_r", "divisor": 10, "descricao": "Temperatura Enrolamento R Motor","valor" : [50,30]},
        {"tipo": "FP", "addr": 702,"bit": -1, "nome": "es.temp_s", "divisor": 10, "descricao": "Temperatura Enrolamento S Motor","valor" : [50,30]},
        {"tipo": "FP", "addr": 704,"bit": -1, "nome": "es.temp_t", "divisor": 10, "descricao": "Temperatura Enrolamento T Motor","valor" : [50,30]},
        {"tipo": "FP", "addr": 706,"bit": -1, "nome": "es.temp_carc", "divisor": 10, "descricao": "Temperatura Carcaça","valor" : [35,15]},

        {"tipo": "4X", "addr": 1204,"bit": -1, "nome": "es.demanda_anterior", "divisor": 1, "descricao": "Medida de Demanda Anterior","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X", "addr": 1205,"bit": -1, "nome": "es.demanda_atual", "divisor": 1, "descricao": "Medida de Demanda Atual","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X", "addr": 1206,"bit": -1, "nome": "es.demanda_media", "divisor": 1, "descricao": "Medida de Demanda Média","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X", "addr": 1207,"bit": -1, "nome": "es.demanda_pico", "divisor": 1, "descricao": "Medida de Demanda de Pico","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X", "addr": 1208,"bit": -1, "nome": "es.demanda_prevista", "divisor": 1, "descricao": "Medida de Demanda Prevista","valor" : [11.4,0.02]},

        {"tipo": "4X", "addr": 830,"bit": -1, "nome": "es.frequencia", "divisor": 100, "descricao": "Medida Frequência da Rede","valor" : [60,5]},

        {"tipo": "4X", "addr": 800,"bit": -1, "nome": "es.thd_tensao_rn", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Neutro", "valor": [2.0,1]},
        {"tipo": "4X", "addr": 801,"bit": -1, "nome": "es.thd_tensao_sn", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Neutro", "valor": [2.0,1]},
        {"tipo": "4X", "addr": 802,"bit": -1, "nome": "es.thd_tensao_tn", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Neutro", "valor": [2.0,1]},
        {"tipo": "4X", "addr": 804,"bit": -1, "nome": "es.thd_tensao_rs", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Fase S", "valor": [1.4,1]},
        {"tipo": "4X", "addr": 805,"bit": -1, "nome": "es.thd_tensao_st", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Fase T", "valor": [1.4,1]},
        {"tipo": "4X", "addr": 806,"bit": -1, "nome": "es.thd_tensao_tr", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Fase R", "valor": [1.4,1]},
        {"tipo": "4X", "addr": 874,"bit": -1, "nome": "es.thd_corrente_r", "divisor": 10, "descricao": "Medida do THD de Corrente da fase R", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X", "addr": 875,"bit": -1, "nome": "es.thd_corrente_s", "divisor": 10, "descricao": "Medida do THD de Corrente da fase S", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X", "addr": 876,"bit": -1, "nome": "es.thd_corrente_t", "divisor": 10, "descricao": "Medida do THD de Corrente da fase T", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X", "addr": 877,"bit": -1, "nome": "es.thd_corrente_n", "divisor": 10, "descricao": "Medida do THD de Corrente do Neutro", "valor": [3276.8,7]},

        {"tipo": "4X", "addr": 840,"bit": -1, "nome": "es.corrente_r", "divisor": 100, "descricao": "Corrente na fase R", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 841,"bit": -1, "nome": "es.corrente_s", "divisor": 100, "descricao": "Corrente na fase S", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 842,"bit": -1, "nome": "es.corrente_t", "divisor": 100, "descricao": "Corrente na fase T", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 843,"bit": -1, "nome": "es.corrente_n", "divisor": 100, "descricao": "Corrente no Neutro", "valor": [0,0.02]},
        {"tipo": "4X", "addr": 845,"bit": -1, "nome": "es.corrente_media", "divisor": 100, "descricao": "Corrente Média", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},

        {"tipo": "4X", "addr": 847,"bit": -1, "nome": "es.tensao_rs", "divisor": 10, "descricao": "ddp entre Fase R e S", "valor": [221,20]},
        {"tipo": "4X", "addr": 848,"bit": -1, "nome": "es.tensao_st", "divisor": 10, "descricao": "ddp entre Fase S e T", "valor": [221,20]},
        {"tipo": "4X", "addr": 849,"bit": -1, "nome": "es.tensao_tr", "divisor": 10, "descricao": "ddp entre Fase T e R", "valor": [221,20]},

        {"tipo": "4X", "addr": 852,"bit": -1, "nome": "es.ativa_r", "divisor": 1, "descricao": "Medida Potência Ativa Fase R", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 853,"bit": -1, "nome": "es.ativa_s", "divisor": 1, "descricao": "Medida Potência Ativa Fase S", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 854,"bit": -1, "nome": "es.ativa_t", "divisor": 1, "descricao": "Medida Potência Ativa Fase T", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X", "addr": 855,"bit": -1, "nome": "es.ativa_total", "divisor": 1, "descricao": "Medida Potência Ativa Total", "valor_desligado" : [0,6], "valor_ligado": [1050,750], "variacao_por_rotacao": True},

        {"tipo": "4X", "addr": 856,"bit": -1, "nome": "es.reativa_r", "divisor": 1, "descricao": "Medida Potência Reativa Fase R", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 857,"bit": -1, "nome": "es.reativa_s", "divisor": 1, "descricao": "Medida Potência Reativa Fase S", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 858,"bit": -1, "nome": "es.reativa_t", "divisor": 1, "descricao": "Medida Potência Reativa Fase T", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 859,"bit": -1, "nome": "es.reativa_total", "divisor": 1, "descricao": "Medida Potência Reativa Total", "valor_desligado" : [0,6], "valor_ligado": [1050,750], "variacao_por_rotacao":True},
        
        {"tipo": "4X", "addr": 860,"bit": -1, "nome": "es.aparente_r", "divisor": 1, "descricao": "Medida Potência Aparente Fase R", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 861,"bit": -1, "nome": "es.aparente_s", "divisor": 1, "descricao": "Medida Potência Aparente Fase S", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 862,"bit": -1, "nome": "es.aparente_t", "divisor": 1, "descricao": "Medida Potência Aparente Fase T", "valor_desligado" : [0,2], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X", "addr": 863,"bit": -1, "nome": "es.aparente_total", "divisor": 1, "descricao": "Medida Potência Aparente Total", "valor_desligado" : [0,2], "valor_ligado": [1050,750], "variacao_por_rotacao":True},
        
        {"tipo": "4X", "addr": 868,"bit": -1, "nome": "es.fp_r", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase R", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X", "addr": 869,"bit": -1, "nome": "es.fp_s", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase S", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X", "addr": 870,"bit": -1, "nome": "es.fp_t", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase T", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X", "addr": 871,"bit": -1, "nome": "es.fp_total", "divisor": 1000, "descricao": "Medida do Fator de Potência Total", "valor_ligado": [0.65,0.2]},
        
        {"tipo": "4X", "addr": 1210,"bit": -1, "nome": "es.energia_ativa", "divisor": 1, "descricao": "Medida da Energia Ativa", "valor_ligado": [850,150]},
        {"tipo": "4X", "addr": 1212,"bit": -1, "nome": "es.energia_reativa", "divisor": 1, "descricao": "Medida da Energia Reativa", "valor_ligado": [850,150]},
        {"tipo": "4X", "addr": 1214,"bit": -1, "nome": "es.energia_aparente", "divisor": 1, "descricao": "Medida da Energia Aparente", "valor_ligado": [850,150]},    
        
    ]
    pass

def reg_saida_bancada() ->list:
    return [
        {"tipo": "FP", "addr": 724,"bit": -1, "nome": "es.esteira", "divisor": 1, "descricao": "Velocidade da Esteira (m/min)", "valor_desligado" : 0, "valor_ligado": 85, "variacao_por_rotacao": True, "erro" : 15},
        {"tipo": "4X", "addr": 892,"bit": -1, "nome": "es.valor1", "divisor": 100, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 893,"bit": -1, "nome": "es.angulo1", "divisor": 1, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 894,"bit": -1, "nome": "es.valor2", "divisor": 100, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 895,"bit": -1, "nome": "es.angulo2", "divisor": 1, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 896,"bit": -1, "nome": "es.valor3", "divisor": 100, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 897,"bit": -1, "nome": "es.angulo3", "divisor": 1, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 898,"bit": -1, "nome": "es.valor4", "divisor": 100, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 899,"bit": -1, "nome": "es.angulo4", "divisor": 1, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 900,"bit": -1, "nome": "es.valor5", "divisor": 100, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True},
        {"tipo": "4X", "addr": 901,"bit": -1, "nome": "es.angulo5", "divisor": 1, "descricao": "Variável auxiliar do CLP", "valor_desligado" : 0, "valor_ligado": 0, "variacao_por_rotacao": True, "erro" : 0,"confere" : True}

    ]
"""
def get_esteira()->list:
    return [
#controle do motor
{"tipo": "4X", "addr": 708,"bit": -1, "nome": "es.tipo_motor", "divisor": 1, "descricao": "Tipo do motor (0 = Desligado, 1 = Verde ou 2 = Azul)"},
{"tipo": "4X", "addr": 1330,"bit": 0,  "nome": "es.habilita", "divisor": 1, "descricao": "Indica Motor (0 = Rodando ou 1 = Parado)"},
{"tipo": "4X", "addr": 1216,"bit": -1, "nome": "es.indica_driver", "divisor": 1, "descricao": "Indica a partida selecionada (Soft-start = 1, Inversor = 2, Direta = 3)"},
{"tipo": "4X", "addr": 1324,"bit": -1, "nome": "es.sel_driver", "divisor": 1, "descricao": "Seleciona o Tipo de Partida  (Soft-start = 1, Inversor = 2, Direta = 3)","permite_escrita":True,"valores_de_escrita":[1,2,3],"descricao_de_escrita":["Soft-start","Inversor","Direta"]},
{"tipo": "4X", "addr": 1316,"bit": -1, "nome": "es.ats48", "divisor": 1, "descricao": "Controla partida Soft-start (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
{"tipo": "4X", "addr": 1317,"bit": -1, "nome": "es.ats48_acc", "divisor": 1, "descricao": "Define a rampa de aceleração do soft-start (10s a 60s)","permite_escrita":True},
{"tipo": "4X", "addr": 1318,"bit": -1, "nome": "es.ats48_dcc", "divisor": 1, "descricao": "Define a rampa de desaceleração do soft-start (10s a 60s)","permite_escrita":True},
{"tipo": "4X", "addr": 1312,"bit": -1, "nome": "es.atv31", "divisor": 1, "descricao": "Controla partida Inversor (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
{"tipo": "4X", "addr": 1313,"bit": -1, "nome": "es.atv31_velocidade", "divisor": 10, "descricao": "Define a velocidade do Inversor (0 a 60Hz)","permite_escrita":True},
{"tipo": "4X", "addr": 1314,"bit": -1, "nome": "es.atv31_acc", "divisor": 10, "descricao": "Define a rampa de aceleração do inversor (10s a 60s)","permite_escrita":True},
{"tipo": "4X", "addr": 1315,"bit": -1, "nome": "es.atv31_dcc", "divisor": 10, "descricao": "Define a rampa de desaceleração do inversor (10s a 60s)","permite_escrita":True},
{"tipo": "4X", "addr": 1319,"bit": -1, "nome": "es.tesys", "divisor": 1, "descricao": "Controla partida Direta (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},

#status do motor
{"tipo": "FP", "addr": 884,"bit": -1, "nome": "es.encoder", "divisor": 1, "descricao": "Medida da Rotação do Motor (RPM)"},
{"tipo": "FP", "addr": 1420,"bit": -1, "nome": "es.torque", "divisor": 100, "descricao": "Medida do Torque do motor"},
{"tipo": "FP", "addr": 700,"bit": -1, "nome": "es.temp_r", "divisor": 10, "descricao": "Temperatura Enrolamento R Motor"},
{"tipo": "FP", "addr": 702,"bit": -1, "nome": "es.temp_s", "divisor": 10, "descricao": "Temperatura Enrolamento S Motor"},
{"tipo": "FP", "addr": 704,"bit": -1, "nome": "es.temp_t", "divisor": 10, "descricao": "Temperatura Enrolamento T Motor"},
{"tipo": "FP", "addr": 706,"bit": -1, "nome": "es.temp_carc", "divisor": 10, "descricao": "Temperatura Carcaça"},

#medidas de interesse
{"tipo": "FP", "addr": 724,"bit": -1, "nome": "es.esteira", "divisor": 1, "descricao": "Velocidade da Esteira (m/min)"},

#controle pid
{"tipo": "4X", "addr": 722,"bit": -1, "nome": "es.status_pid", "divisor": 1, "descricao": "Status do PID (0 = Automático ou 1 =  Manual)"},
{"tipo": "4X", "addr": 1332,"bit": -1, "nome": "es.sel_pid", "divisor": 1, "descricao": "Seleciona o tipo de PID (Automático = 0, Manual = 1)","permite_escrita":True},
{"tipo": "FP", "addr": 710,"bit": -1, "nome": "es.le_carga", "divisor": 1, "descricao": "Valor lido da Carga na esteira (PV - Variável de Processo)"},
{"tipo": "FP", "addr": 1302,"bit": -1, "nome": "es.carga", "divisor": 1, "descricao": "Define a Carga na esteira no PID (SP- Set Point)","permite_escrita":True},
{"tipo": "FP", "addr": 814,"bit": -1, "nome": "es.mv_le", "divisor": 1, "descricao": "Valor lido da Variável Manipulada quando em Auto (MV = SP-PV)"},
{"tipo": "FP", "addr": 1310,"bit": -1, "nome": "es.mv_escreve", "divisor": 1, "descricao": "Define o valor da Variável Manipulada (MV em porcentagem)","permite_escrita":True},
{"tipo": "FP", "addr": 1304,"bit": -1, "nome": "es.p", "divisor": 1, "descricao": "Define o valor do Controle Proporcional","permite_escrita":True},
{"tipo": "FP", "addr": 1306,"bit": -1, "nome": "es.i", "divisor": 1, "descricao": "Define o valor do Controle Integral","permite_escrita":True},
{"tipo": "FP", "addr": 1308,"bit": -1, "nome": "es.d", "divisor": 1, "descricao": "Define o valor do Controle Derivativo","permite_escrita":True},

#THD, corrente e tensao
{"tipo": "4X", "addr": 1204,"bit": -1, "nome": "es.demanda_anterior", "divisor": 1, "descricao": "Medida de Demanda Anterior"},
{"tipo": "4X", "addr": 1205,"bit": -1, "nome": "es.demanda_atual", "divisor": 1, "descricao": "Medida de Demanda Atual"},
{"tipo": "4X", "addr": 1206,"bit": -1, "nome": "es.demanda_media", "divisor": 1, "descricao": "Medida de Demanda Média"},
{"tipo": "4X", "addr": 1207,"bit": -1, "nome": "es.demanda_pico", "divisor": 1, "descricao": "Medida de Demanda de Pico"},
{"tipo": "4X", "addr": 1208,"bit": -1, "nome": "es.demanda_prevista", "divisor": 1, "descricao": "Medida de Demanda Prevista"},
{"tipo": "4X", "addr": 830,"bit": -1, "nome": "es.frequencia", "divisor": 100, "descricao": "Medida Frequência da Rede"},
{"tipo": "4X", "addr": 874,"bit": -1, "nome": "es.thd_corrente_r", "divisor": 10, "descricao": "Medida do THD de Corrente da fase R"},
{"tipo": "4X", "addr": 875,"bit": -1, "nome": "es.thd_corrente_s", "divisor": 10, "descricao": "Medida do THD de Corrente da fase S"},
{"tipo": "4X", "addr": 876,"bit": -1, "nome": "es.thd_corrente_t", "divisor": 10, "descricao": "Medida do THD de Corrente da fase T"},
{"tipo": "4X", "addr": 877,"bit": -1, "nome": "es.thd_corrente_n", "divisor": 10, "descricao": "Medida do THD de Corrente do Neutro"},
{"tipo": "4X", "addr": 800,"bit": -1, "nome": "es.thd_tensao_rn", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Neutro"},
{"tipo": "4X", "addr": 801,"bit": -1, "nome": "es.thd_tensao_sn", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Neutro"},
{"tipo": "4X", "addr": 802,"bit": -1, "nome": "es.thd_tensao_tn", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Neutro"},
{"tipo": "4X", "addr": 804,"bit": -1, "nome": "es.thd_tensao_rs", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Fase S"},
{"tipo": "4X", "addr": 805,"bit": -1, "nome": "es.thd_tensao_st", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Fase T"},
{"tipo": "4X", "addr": 806,"bit": -1, "nome": "es.thd_tensao_tr", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Fase R"},
{"tipo": "4X", "addr": 840,"bit": -1, "nome": "es.corrente_r", "divisor": 100, "descricao": "Corrente na fase R"},
{"tipo": "4X", "addr": 841,"bit": -1, "nome": "es.corrente_s", "divisor": 100, "descricao": "Corrente na fase S"},
{"tipo": "4X", "addr": 842,"bit": -1, "nome": "es.corrente_t", "divisor": 100, "descricao": "Corrente na fase T"},
{"tipo": "4X", "addr": 843,"bit": -1, "nome": "es.corrente_n", "divisor": 100, "descricao": "Corrente no Neutro"},
{"tipo": "4X", "addr": 845,"bit": -1, "nome": "es.corrente_media", "divisor": 100, "descricao": "Corrente Média"},
{"tipo": "4X", "addr": 847,"bit": -1, "nome": "es.tensao_rs", "divisor": 10, "descricao": "ddp entre Fase R e S"},
{"tipo": "4X", "addr": 848,"bit": -1, "nome": "es.tensao_st", "divisor": 10, "descricao": "ddp entre Fase S e T"},
{"tipo": "4X", "addr": 849,"bit": -1, "nome": "es.tensao_tr", "divisor": 10, "descricao": "ddp entre Fase T e R"},
{"tipo": "4X", "addr": 852,"bit": -1, "nome": "es.ativa_r", "divisor": 1, "descricao": "Medida Potência Ativa Fase R"},
{"tipo": "4X", "addr": 853,"bit": -1, "nome": "es.ativa_s", "divisor": 1, "descricao": "Medida Potência Ativa Fase S"},
{"tipo": "4X", "addr": 854,"bit": -1, "nome": "es.ativa_t", "divisor": 1, "descricao": "Medida Potência Ativa Fase T"},
{"tipo": "4X", "addr": 855,"bit": -1, "nome": "es.ativa_total", "divisor": 1, "descricao": "Medida Potência Ativa Total"},
{"tipo": "4X", "addr": 856,"bit": -1, "nome": "es.reativa_r", "divisor": 1, "descricao": "Medida Potência Reativa Fase R"},
{"tipo": "4X", "addr": 857,"bit": -1, "nome": "es.reativa_s", "divisor": 1, "descricao": "Medida Potência Reativa Fase S"},
{"tipo": "4X", "addr": 858,"bit": -1, "nome": "es.reativa_t", "divisor": 1, "descricao": "Medida Potência Reativa Fase T"},
{"tipo": "4X", "addr": 859,"bit": -1, "nome": "es.reativa_total", "divisor": 1, "descricao": "Medida Potência Reativa Total"},
{"tipo": "4X", "addr": 860,"bit": -1, "nome": "es.aparente_r", "divisor": 1, "descricao": "Medida Potência Aparente Fase R"},
{"tipo": "4X", "addr": 861,"bit": -1, "nome": "es.aparente_s", "divisor": 1, "descricao": "Medida Potência Aparente Fase S"},
{"tipo": "4X", "addr": 862,"bit": -1, "nome": "es.aparente_t", "divisor": 1, "descricao": "Medida Potência Aparente Fase T"},
{"tipo": "4X", "addr": 863,"bit": -1, "nome": "es.aparente_total", "divisor": 1, "descricao": "Medida Potência Aparente Total"},
{"tipo": "4X", "addr": 868,"bit": -1, "nome": "es.fp_r", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase R"},
{"tipo": "4X", "addr": 869,"bit": -1, "nome": "es.fp_s", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase S"},
{"tipo": "4X", "addr": 870,"bit": -1, "nome": "es.fp_t", "divisor": 1000, "descricao": "Medida do Fator de Potência Fase T"},
{"tipo": "4X", "addr": 871,"bit": -1, "nome": "es.fp_total", "divisor": 1000, "descricao": "Medida do Fator de Potência Total"},
{"tipo": "4X", "addr": 1210,"bit": -1, "nome": "es.energia_ativa", "divisor": 1, "descricao": "Medida da Energia Ativa"},
{"tipo": "4X", "addr": 1212,"bit": -1, "nome": "es.energia_reativa", "divisor": 1, "descricao": "Medida da Energia Reativa"},
{"tipo": "4X", "addr": 1214,"bit": -1, "nome": "es.energia_aparente", "divisor": 1, "descricao": "Medida da Energia Aparente"},
{"tipo": "4X", "addr": 886,"bit": -1, "nome": "es.status_ats48", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 888,"bit": -1, "nome": "es.status_atv31", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 890,"bit": -1, "nome": "es.status_tesys", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 892,"bit": -1, "nome": "es.valor1", "divisor": 100, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 893,"bit": -1, "nome": "es.angulo1", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 894,"bit": -1, "nome": "es.valor2", "divisor": 100, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 895,"bit": -1, "nome": "es.angulo2", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 896,"bit": -1, "nome": "es.valor3", "divisor": 100, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 897,"bit": -1, "nome": "es.angulo3", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 898,"bit": -1, "nome": "es.valor4", "divisor": 100, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 899,"bit": -1, "nome": "es.angulo4", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 900,"bit": -1, "nome": "es.valor5", "divisor": 100, "descricao": "Variável auxiliar do CLP"},
{"tipo": "4X", "addr": 901,"bit": -1, "nome": "es.angulo5", "divisor": 1, "descricao": "Variável auxiliar do CLP"}
]
    
    return [
    # Controle do Motor
    {"tipo": "4X", "addr": 1330,"bit": 0,  "nome": "es.habilita", "divisor": 1, "descricao": "Indica Motor (0 = Rodando ou 1 = Parado"},
    {"tipo": "4X", "addr": 1324,"bit": -1, "nome": "es.sel_driver", "divisor": 1, "descricao": "Seleciona o Tipo de Partida  (Soft-start = 1, Inversor = 2, Direta = 3)","permite_escrita":True,"valores_de_escrita":[1,2,3],"descricao_de_escrita":["Soft-start","Inversor","Direta"]},
    {"tipo": "4X", "addr": 1316,"bit": -1, "nome": "es.ats48", "divisor": 1, "descricao": "Controla partida Soft-start (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
    {"tipo": "4X", "addr": 1312,"bit": -1, "nome": "es.atv31", "divisor": 1, "descricao": "Controla partida Inversor (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
    {"tipo": "4X", "addr": 1319,"bit": -1, "nome": "es.tesys", "divisor": 1, "descricao": "Controla partida Direta (Liga = 1, Desliga = 0, Reset = 2) ","permite_escrita":True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
    {"tipo": "4X", "addr": 1332,"bit": -1, "nome": "es.sel_pid", "divisor": 1, "descricao": "Seleciona o tipo de PID (Automático = 0, Manual = 1)","permite_escrita":True},

    # Segurança e Proteção
    {"tipo": "4X", "addr": 708,"bit": -1, "nome": "es.tipo_motor", "divisor": 1, "descricao": "Tipo do motor (0 = Desligado, 1 = Verde ou 2 = Azul)"},
    {"tipo": "FP", "addr": 700,"bit": -1, "nome": "es.temp_r", "divisor": 10, "descricao": "Temperatura Enrolamento R Motor"},
    {"tipo": "FP", "addr": 702,"bit": -1, "nome": "es.temp_s", "divisor": 10, "descricao": "Temperatura Enrolamento S Motor"},
    {"tipo": "FP", "addr": 704,"bit": -1, "nome": "es.temp_t", "divisor": 10, "descricao": "Temperatura Enrolamento T Motor"},
    {"tipo": "FP", "addr": 706,"bit": -1, "nome": "es.temp_carc", "divisor": 10, "descricao": "Temperatura Carcaça"},

    # Medidas e Leituras
    {"tipo": "FP", "addr": 884,"bit": -1, "nome": "es.encoder", "divisor": 1, "descricao": "Medida da Rotação do Motor (RPM)"},
    {"tipo": "FP", "addr": 1420,"bit": -1, "nome": "es.torque", "divisor": 100, "descricao": "Medida do Torque do motor"},
    {"tipo": "FP", "addr": 724,"bit": -1, "nome": "es.esteira", "divisor": 1, "descricao": "Velocidade da Esteira (m/min)"},
    {"tipo": "FP", "addr": 710,"bit": -1, "nome": "es.le_carga", "divisor": 1, "descricao": "Valor lido da Carga na esteira (PV - Variável de Processo)"},

    # Controle PID
    {"tipo": "FP", "addr": 1302,"bit": -1, "nome": "es.carga", "divisor": 1, "descricao": "Define a Carga na esteira no PID (SP- Set Point)","permite_escrita":True},
    {"tipo": "FP", "addr": 1304,"bit": -1, "nome": "es.p", "divisor": 1, "descricao": "Define o valor do Controle Proporcional","permite_escrita":True},
    {"tipo": "FP", "addr": 1306,"bit": -1, "nome": "es.i", "divisor": 1, "descricao": "Define o valor do Controle Integral","permite_escrita":True},
    {"tipo": "FP", "addr": 1308,"bit": -1, "nome": "es.d", "divisor": 1, "descricao": "Define o valor do Controle Derivativo","permite_escrita":True},
    {"tipo": "FP", "addr": 1310,"bit": -1, "nome": "es.mv_escreve", "divisor": 1, "descricao": "Define o valor da Variável Manipulada (MV em porcentagem)","permite_escrita":True},
    {"tipo": "FP", "addr": 814,"bit": -1, "nome": "es.mv_le", "divisor": 1, "descricao": "Valor lido da Variável Manipulada quando em Auto (MV = SP-PV)"},

    # THD, Correntes e Tensão
    {"tipo": "4X", "addr": 800,"bit": -1, "nome": "es.thd_tensao_rn", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Neutro"},
    {"tipo": "4X", "addr": 801,"bit": -1, "nome": "es.thd_tensao_sn", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Neutro"},
    {"tipo": "4X", "addr": 802,"bit": -1, "nome": "es.thd_tensao_tn", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Neutro"},
    {"tipo": "4X", "addr": 804,"bit": -1, "nome": "es.thd_tensao_rs", "divisor": 10, "descricao": "Medida THD Tensão entre fase R e Fase S"},
    {"tipo": "4X", "addr": 805,"bit": -1, "nome": "es.thd_tensao_st", "divisor": 10, "descricao": "Medida THD Tensão entre fase S e Fase T"},
    {"tipo": "4X", "addr": 806,"bit": -1, "nome": "es.thd_tensao_tr", "divisor": 10, "descricao": "Medida THD Tensão entre fase T e Fase R"},

    # Auxiliares
    {"tipo": "4X", "addr": 886,"bit": -1, "nome": "es.status_ats48", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
    {"tipo": "4X", "addr": 888,"bit": -1, "nome": "es.status_atv31", "divisor": 1, "descricao": "Variável auxiliar do CLP"},
    {"tipo": "4X", "addr": 890,"bit": -1, "nome": "es.status_tesys", "divisor": 1, "descricao": "Variável auxiliar do CLP"}
]


"""    
    
