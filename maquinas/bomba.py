from src.funcao_registrador import FuncaoRegistrador

def get_bomba_ip() ->str:
    return '10.15.20.23'
    return 'localhost'
def get_bomba_port() ->str:
    return 502

def get_reg_motor() -> list:
    return [        
        #controle do motor
        {"funcao": FuncaoRegistrador.mt_tipo_motor,
            "tipo": "4X",
            "addr": 708,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mt_habilita,
            "tipo": "4X",
            "addr": 1328,
            "bit": 6,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_indica_driver,
            "tipo": "4X",
            "addr": 1216,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_status_ats48,
            "tipo": "4X",
            "addr":	886,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_status_atv31,
            "tipo": "4X",
            "addr":	888,
            "bit": -1		 ,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_status_tesys,
            "tipo": "4X",
            "addr":	890,
            "bit": -1		 ,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_sel_driver,
            "tipo": "4X",
            "addr": 1324,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_tesys,
            "tipo": "4X",
            "addr":	1319,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_ats48,
            "tipo": "4X",
            "addr": 1316,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_ats48_acc,
            "tipo": "4X",
            "addr": 1317,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_ats48_dcc,
            "tipo": "4X",
            "addr": 1318,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_atv31,
            "tipo": "4X",
            "addr": 1312,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_atv31_velocidade,
            "tipo": "4X",
            "addr": 1313,
            "bit": -1,
            "divisor":	10,
        },
        {"funcao": FuncaoRegistrador.mot_atv31_acc,
            "tipo": "4X",
            "addr": 1314,
            "bit": -1,
            "divisor":	1,
        },
        {"funcao": FuncaoRegistrador.mot_atv31_dcc,
            "tipo": "4X",
            "addr": 1315,
            "bit": -1,
            "divisor":	1,
        }
    ]
    pass

def get_reg_controle() -> list:
    return [        
        {"addr":	716,
            "tipo": "4X",
            "bit": 	5 	,
            "nome": "bc.sol_inf",
            "divisor":	1,
            "valores_de_escrita": [0,1]
        },
        {"addr":	716,
            "tipo": "4X",
            "bit": 	6 	,
            "nome": "bc.sol_sup",
            "divisor":	1,
            "valores_de_escrita": [0,1]
        }
    ]
    pass

def get_estado_desligado() -> list:
    return [
        [0,0],
    ]
def get_estado_ligado() -> list:
    return [
        [0,0],
    ]
    pass

def get_reg_saida_motor() ->list:
    return [
        #status do motor
        {"tipo": "FP","addr":	727,"bit": -1		 ,"nome": "bc.encoder","divisor":	1, "descricao":	"Medida da Rotação do Motor selecionado (RPM)", "valor_desligado" : [0,0.1], "valor_ligado": [3100,1000], "variacao_por_rotacao": True},
        {"tipo": "FP","addr":	884,"bit": -1		 ,"nome": "bc.encoder_dina","divisor":	1, "descricao":	"Medida da Rotação do Motor selecionado (RPM) no Dinamômetro", "valor_desligado" : [0,0.1], "valor_ligado": [4,4.1]},
        {"tipo": "FP","addr":	1334,"bit": -1		 ,"nome": "bc.torque","divisor":	1, "descricao":	"Medida do Torque no Motor Selecionado", "valor_desligado" : [0,0.1], "valor_ligado": [2.2,1.2], "variacao_por_rotacao": True},
        {"tipo": "FP","addr":	700,"bit": -1		 ,"nome": "bc.temp_r","divisor":	10, "descricao":	"Temperatura Enrolamento R Motor","valor" : [50,30]},
        {"tipo": "FP","addr":	702,"bit": -1		 ,"nome": "bc.temp_s","divisor":	10, "descricao":	"Temperatura Enrolamento S Motor","valor" : [50,30]},
        {"tipo": "FP","addr":	704,"bit": -1		 ,"nome": "bc.temp_t","divisor":	10, "descricao":	"Temperatura Enrolamento T Motor","valor" : [50,30]},
        {"tipo": "FP","addr":	706,"bit": -1		 ,"nome": "bc.temp_carc","divisor":	10, "descricao":	"Temperatura Carcaça","valor" : [35,15]},

        
        #THD, corrente e tensao
        {"tipo": "4X","addr":	1204,"bit": -1		 ,"nome": "bc.demanda_anterior","divisor":	10, "descricao":	"Medida de Demanda Anterior","somente_variacao" : True,"valor":[30]},
        {"tipo": "4X","addr":	1205,"bit": -1		 ,"nome": "bc.demanda_atual","divisor":	10, "descricao":	"Medida de Demanda Atual","somente_variacao" : True,"valor":[30]},
        {"tipo": "4X","addr":	1206,"bit": -1		 ,"nome": "bc.demanda_media","divisor":	10, "descricao":	"Medidade de Demanda Média","somente_variacao" : True,"valor":[30]},
        {"tipo": "4X","addr":	1207,"bit": -1		 ,"nome": "bc.demanda_pico","divisor":	10, "descricao":	"Medidade de Demanda de Pico","somente_variacao" : True,"valor":[30]},
        {"tipo": "4X","addr":	1208,"bit": -1		 ,"nome": "bc.demanda_prevista","divisor":	10, "descricao":	"Medida de Demanda Prevista","somente_variacao" : True,"valor":[30]},

        {"tipo": "4X","addr":   830,"bit": -1        ,"nome": "bc.frequencia","divisor":	100, "descricao":	"Frequência Rede","valor" : [60,5]},
        
        {"tipo": "4X","addr":	800,"bit": -1		 ,"nome": "bc.thd_tensao_rn","divisor":	10, "descricao":	"Medida THD Tensão entre fase R e Neutro", "valor": [2.0,1]},
        {"tipo": "4X","addr":	801,"bit": -1		 ,"nome": "bc.thd_tensao_sn","divisor":	10, "descricao":	"Medida THD Tensão entre fase S e Neutro", "valor": [2.0,1]},
        {"tipo": "4X","addr":	802,"bit": -1		 ,"nome": "bc.thd_tensao_tn","divisor":	10, "descricao":	"Medida THD Tensão entre fase T e Neutro", "valor": [2.0,1]},
        {"tipo": "4X","addr":	804,"bit": -1		 ,"nome": "bc.thd_tensao_rs","divisor":	10, "descricao":	"Medida THD Tensão entre fase R e Fase S", "valor": [1.4,1]},
        {"tipo": "4X","addr":	805,"bit": -1		 ,"nome": "bc.thd_tensao_st","divisor":	10, "descricao":	"Medida THD Tensão entre fase S e Fase T", "valor": [1.4,1]},
        {"tipo": "4X","addr":	806,"bit": -1		 ,"nome": "bc.thd_tensao_tr","divisor":	10, "descricao":	"Medida THD Tensão entre fase T e Fase R", "valor": [1.4,1]},
        {"tipo": "4X","addr":	874,"bit": -1		 ,"nome": "bc.thd_corrente_r","divisor":	10, "descricao":	"Medida do THD de Corrente da fase R", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X","addr":	875,"bit": -1		 ,"nome": "bc.thd_corrente_s","divisor":	10, "descricao":	"Medida do THD de Corrente da fase S", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X","addr":	876,"bit": -1		 ,"nome": "bc.thd_corrente_t","divisor":	10, "descricao":	"Medida do THD de Corrente da fase T", "valor_ligado": [3,1.4],"variacao_por_rotacao": True},#nao sei
        {"tipo": "4X","addr":	877,"bit": -1		 ,"nome": "bc.thd_corrente_n","divisor":	10, "descricao":	"Medida do THD de Corrente do Neutro", "valor": [3276.8,7]},

        {"tipo": "4X","addr":	840,"bit": -1		 ,"nome": "bc.corrente_r","divisor":	10, "descricao":	"Corrente na fase R", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	841,"bit": -1		 ,"nome": "bc.corrente_s","divisor":	10, "descricao":	"Corrente na fase S", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	842,"bit": -1		 ,"nome": "bc.corrente_t","divisor":	10, "descricao":	"Corrente na fase T", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	843,"bit": -1		 ,"nome": "bc.corrente_n","divisor":	10, "descricao":	"Corrente no Neutro", "valor": [0,0.2]},
        {"tipo": "4X","addr":	845,"bit": -1		 ,"nome": "bc.corrente_media","divisor":	10, "descricao":	"Corrente Média", "valor_desligado" : [0,0.2], "valor_ligado": [3.4,1.4], "variacao_por_rotacao": True},
        
        {"tipo": "4X","addr":	847,"bit": -1		 ,"nome": "bc.tensao_rs","divisor":	10, "descricao":	"ddp entre Fase R e S", "valor": [221,20]},
        {"tipo": "4X","addr":	848,"bit": -1		 ,"nome": "bc.tensao_st","divisor":	10, "descricao":	"ddp entre Fase S e T", "valor": [221,20]},
        {"tipo": "4X","addr":	849,"bit": -1		 ,"nome": "bc.tensao_tr","divisor":	10, "descricao":	"ddp entre Fase T e R", "valor": [221,20]},
        
        {"tipo": "4X","addr":	852,"bit": -1		 ,"nome": "bc.ativa_r","divisor":	1, "descricao":	"Medida Potência Ativa Fase R", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	853,"bit": -1		 ,"nome": "bc.ativa_s","divisor":	1, "descricao":	"Medida Potência Ativa Fase S", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	854,"bit": -1		 ,"nome": "bc.ativa_t","divisor":	1, "descricao":	"Medida Potência Ativa Fase T", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao": True},
        {"tipo": "4X","addr":	855,"bit": -1		 ,"nome": "bc.ativa_total","divisor":	1, "descricao":	"Medida Potência Ativa Total", "valor_desligado" : [30,30], "valor_ligado": [1050,750], "variacao_por_rotacao": True},
        
        {"tipo": "4X","addr":	856,"bit": -1		 ,"nome": "bc.reativa_r","divisor":	1, "descricao":	"Medida Potência Reativa Fase R", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	857,"bit": -1		 ,"nome": "bc.reativa_s","divisor":	1, "descricao":	"Medida Potência Reativa Fase S", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	858,"bit": -1		 ,"nome": "bc.reativa_t","divisor":	1, "descricao":	"Medida Potência Reativa Fase T", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	859,"bit": -1		 ,"nome": "bc.reativa_total","divisor":	1, "descricao":	"Medida Potência Reativa Total", "valor_desligado" : [30,30], "valor_ligado": [1050,750], "variacao_por_rotacao":True},
        
        {"tipo": "4X","addr":	860,"bit": -1		 ,"nome": "bc.aparente_r","divisor":	1, "descricao":	"Medida Potência Aparente Fase R", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	861,"bit": -1		 ,"nome": "bc.aparente_s","divisor":	1, "descricao":	"Medida Potência Aparente Fase S", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	862,"bit": -1		 ,"nome": "bc.aparente_t","divisor":	1, "descricao":	"Medida Potência Aparente Fase T", "valor_desligado" : [10,10], "valor_ligado": [350,250], "variacao_por_rotacao":True},
        {"tipo": "4X","addr":	863,"bit": -1		 ,"nome": "bc.aparente_total","divisor":	1, "descricao":	"Medida Potência Aparente Total", "valor_desligado" : [30,30], "valor_ligado": [1050,750], "variacao_por_rotacao":True},

        {"tipo": "4X","addr":	868,"bit": -1		 ,"nome": "bc.fp_r","divisor":	1000, "descricao":	"Medida do Fator de Potência Fase R", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X","addr":	869,"bit": -1		 ,"nome": "bc.fp_s","divisor":	1000, "descricao":	"Medida do Fator de Potência Fase S", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X","addr":	870,"bit": -1		 ,"nome": "bc.fp_t","divisor":	1000, "descricao":	"Medida do Fator de Potência Fase T", "valor_ligado": [0.65,0.2]},
        {"tipo": "4X","addr":	871,"bit": -1		 ,"nome": "bc.fp_total","divisor":	1000, "descricao":	"Medida do Fator de Potência Total", "valor_ligado": [0.65,0.2]},

        {"tipo": "4X","addr":	1210,"bit": -1		 ,"nome": "bc.energia_ativa","divisor":	1, "descricao":	"Medida da Energia Ativa", "valor_ligado": [800,150]},
        {"tipo": "4X","addr":	1212,"bit": -1		 ,"nome": "bc.energia_reativa","divisor":	1, "descricao":	"Medida da Energia Reativa", "valor_ligado": [800,150]},
        {"tipo": "4X","addr":	1214,"bit": -1		 ,"nome": "bc.energia_aparente","divisor":	1, "descricao":	"Medida da Energia Aparente", "valor_ligado": [800,150]},    
        
        
        {"tipo": "4X","addr":	1322,"bit": -1		 ,"nome": "bc.tipo_u_i","divisor":	1, "descricao":	"**?","permite_escrita":True, "valor":[0,0]},
        {"tipo": "4X","addr":	1336,"bit": -1		 ,"nome": "bc.index_harmonica","divisor":	1, "descricao":	"**?","permite_escrita":True, "valor":[0,0]},
        {"tipo": "4X","addr":	1337,"bit": -1		 ,"nome": "bc.fase","divisor":	1, "descricao":	"**?","permite_escrita":True, "valor":[0,0] },

    ]

def get_reg_lin():
    return [
        { "tipo": "FP","addr":	710,"bit": -1		 ,"nome": "bc.pit01","divisor":	1, "descricao":	"Medida da Pressão PIT-01","valor": [2.5,2.5]},
        { "tipo": "FP","addr":	712,"bit": -1		 ,"nome": "bc.fit01","divisor":	1, "descricao":	"Medida da Vazão FIT-01","valor": [2.5,2.5]},
        { "tipo": "FP","addr":	714,"bit": -1		 ,"nome": "bc.lit01","divisor":	1, "descricao":	"Medida do Nível do Reservatório superior (Porcentagem)","valor": [50,50]},
    ]

def get_reg_saida_bancada():
    return [
        {"tipo": "4X","addr":	716,"bit": 	4 	,"nome": "bc.naa_tq_superior","divisor":	1, "descricao":	"Indicador de Nível Muito Alto","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X","addr":	716,"bit": 	7 	,"nome": "bc.naa_tq_superior","divisor":	1, "descricao":	"Indicador de Nível Muito Alto","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X","addr":	716,"bit": 	0 	,"nome": "bc.na_tq_superior","divisor":	1, "descricao":	"Sensor de Reservatório Superior Nível Alto (Ativo = 1)","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X","addr":	716,"bit": 	1 	,"nome": "bc.nb_tq_superior","divisor":	1, "descricao":	"Sensor de Reservatório Superior Nível Baixo (Ativo = 0)","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X","addr":	716,"bit": 	2 	,"nome": "bc.na_tq_inferior","divisor":	1, "descricao":	"Sensor de Reservatório Inferior Nível Alto (Ativo = 1)","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        {"tipo": "4X","addr":	716,"bit": 	3 	,"nome": "bc.nb_tq_inferior","divisor":	1, "descricao":	"Sensor de Reservatório Inferior Nível Baixo (Ativo = 0)","valor_desligado" : [0,0], "valor_ligado": [0,0]},
        { "tipo": "FP","addr":	714,"bit": -1		 ,"nome": "bc.lit01","divisor":	1, "descricao":	"Medida do Nível do Reservatório superior (Porcentagem)","valor_desligado" : [0,0], "valor_ligado": [0,0]},
    ]

if __name__=="__main__":
    pass
