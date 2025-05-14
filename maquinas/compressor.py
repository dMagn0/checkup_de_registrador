from src.funcao_registrador import FuncaoRegistrador
#incompleto

def get_compressor_ip() ->str:
    return '10.15.20.22'
    return 'localhost'
def get_compressor_port() ->str:
    return 502


def get_reg_motor() -> list:
    return [                
        {"funcao": FuncaoRegistrador.mt_tipo_motor,
            "tipo": "4X", 
            "addr":	708,
            "bit": -1,
            "divisor":	1,
        },
    ]
    pass

def get_reg_controle() -> list:
    pass

def get_estado_desligado() -> list:
    return [
        [0,0,0,0],
        [0,0,1,1]
    ]
def get_estado_ligado() -> list:
    return [
        [0,0,0,0],
        [1,1,0,0]
    ]
    pass

def get_reg_saida() ->list:
    
    pass


"""
def get_compressor()->list:
    return [
{
    "tipo": "4X", 
    "addr":	708,
    "bit": -1		,
    "nome": "co.tipo_motor", 
    "divisor":	1,
    "descricao": "	Tipo do motor (0 = Desligado, 1 = Verde ou 2 = Azul)",
    "permite_escrita":False
},
{
    "tipo": "4X", "addr":	710,"bit": -1		,"nome": "co.pressostato", "divisor":	1,"descricao": "	Indicador de Pressão Alta"
},
{
    "tipo": "4X", "addr":	712,"bit": 	0	,"nome": "co.xv1", "divisor":	1,"descricao": "	Contrrole da Válvula XV-01 (Aberta = 0, Fechada = 1)", "permite_escrita": True,"valores_de_escrita":[0,1],"descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", "addr":	712,"bit": 	1	,"nome": "co.xv2", "divisor":	1,"descricao": "Controle da Válvula XV-02 (Aberta = 0, Fechada = 1)", "permite_escrita": True,"valores_de_escrita":[0,1],"descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", "addr":	712, "bit": 	2	, "nome": "co.xv3", "divisor":	1, "descricao": "	Contrrole da Válvula XV-03 (Aberta = 0, Fechada = 1)", "permite_escrita": True, "valores_de_escrita":[0,1], "descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", "addr":	712, "bit": 	3	, "nome": "co.xv4", "divisor":	1, "descricao": "	Contrrole da Válvula XV-04 (Aberta = 0, Fechada = 1)", "permite_escrita": True, "valores_de_escrita":[0,1], "descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", 
    "addr":	712,
    "bit": 	4	,
    "nome": "co.xv5", 
    "divisor":	1,
    "descricao": "	Contrrole da Válvula XV-05 (Aberta = 0, Fechada = 1)",
    "permite_escrita": True,
    "valores_de_escrita":[0,1],
    "descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", 
    "addr":	712,
    "bit": 	5	,
    "nome": "co.xv6", 
    "divisor":	1,
    "descricao": "	Contrrole da Válvula XV-06 (Aberta = 0, Fechada = 1)",
    "permite_escrita": True,
    "valores_de_escrita":[0,1],
    "descricao_de_escrita":["Fechado","Aberto"]
},
{
    "tipo": "4X", "addr":	714,"bit": -1		,"nome": "co.pv_pid", "divisor":	1,"descricao": "	Valor lido da Vazão (PV - Variável de Processo)"
},
{
    "tipo": "4X", "addr":	722,"bit": -1		,"nome": "co.status_pid", "divisor":	1,"descricao": "	Status do PID (0 = Automático ou 1 =  Manual)"
},
{
    "tipo": "FP", "addr":	700,"bit": -1		,"nome": "co.temp_r", "divisor":	10,"descricao": "	Temperatura Enrolamento R Motor"
},
{"tipo": "FP", "addr":	702,"bit": -1		,"nome": "co.temp_s", "divisor":	10,"descricao": "	Temperatura Enrolamento S Motor"},
{"tipo": "FP", "addr":	704,"bit": -1		,"nome": "co.temp_t", "divisor":	10,"descricao": "	Temperatura Enrolamento T Motor"},
{"tipo": "FP", "addr":	706,"bit": -1		,"nome": "co.temp_carc", "divisor":	10,"descricao": "	Temperatura Carcaça"},
{"tipo": "FP", "addr":	714,"bit": -1		,"nome": "co.pressao", "divisor":	1,"descricao": "	Pressão no Reservatório (PIT-01)"},
{"tipo": "FP", "addr":	716,"bit": -1		,"nome": "co.fit02", "divisor":	1,"descricao": "	Vazão no Ramo das Válvulas 02 a 06 (FIT-02)"},
{"tipo": "FP", "addr":	718,"bit": -1		,"nome": "co.fit03", "divisor":	1,"descricao": "	Vazão no Ramo da Válvula 01 (FIT-03)"},
{"tipo": "FP", "addr":	814,"bit": -1		,"nome": "co.mv_le", "divisor":	1,"descricao": "	Valor lido da Variável Manipulada quando em Auto (MV = SP-PV)"},
{"tipo": "4X", "addr":	800,"bit": -1		,"nome": "co.thd_tensao_rn", "divisor":	10,"descricao": "	Medida THD Tensão entre fase R e Fase S"},
{"tipo": "4X", "addr":	801,"bit": -1		,"nome": "co.thd_tensao_sn", "divisor":	10,"descricao": "	Medida THD Tensão entre fase S e Fase T"},
{"tipo": "4X", "addr":	802,"bit": -1		,"nome": "co.thd_tensao_tn", "divisor":	10,"descricao": "	Medida THD Tensão entre fase T e Fase R"},
{"tipo": "4X", "addr":	804,"bit": -1		,"nome": "co.thd_tensao_rs", "divisor":	10,"descricao": "	Medida THD Tensão entre fase R e Neutro"},
{"tipo": "4X", "addr":	805,"bit": -1		,"nome": "co.thd_tensao_st", "divisor":	10,"descricao": "	Medida THD Tensão entre fase S e Neutro"},
{"tipo": "4X", "addr":	806,"bit": -1		,"nome": "co.thd_tensao_tr", "divisor":	10,"descricao": "	Medida THD Tensão entre fase T e Neutro"},
{"tipo": "4X", "addr":	830,"bit": -1		,"nome": "co.frequencia", "divisor":	100,"descricao": "	Frequência da rede"},
{"tipo": "4X", "addr":	840,"bit": -1		,"nome": "co.corrente_r", "divisor":	10,"descricao": "	Corrente na fase R"},
{"tipo": "4X", "addr":	841,"bit": -1		,"nome": "co.corrente_s", "divisor":	10,"descricao": "	Corrente na fase S"},
{"tipo": "4X", "addr":	842,"bit": -1		,"nome": "co.corrente_t", "divisor":	10,"descricao": "	Corrente na fase T"},
{"tipo": "4X", "addr":	843,"bit": -1		,"nome": "co.corrente_n", "divisor":	10,"descricao": "	Corrente no Neutro"},
{"tipo": "4X", "addr":	845,"bit": -1		,"nome": "co.corrente_media", "divisor":	10,"descricao": "	Corrente Média"},
{"tipo": "4X", "addr":	847,"bit": -1		,"nome": "co.tensao_rs", "divisor":	10,"descricao": "	ddp entre Fase R e S"},
{"tipo": "4X", "addr":	848,"bit": -1		,"nome": "co.tensao_st", "divisor":	10,"descricao": "	ddp entre Fase S e T"},
{"tipo": "4X", "addr":	849,"bit": -1		,"nome": "co.tensao_tr", "divisor":	10,"descricao": "	ddp entre Fase T e R"},
{"tipo": "4X", "addr":	852,"bit": -1		,"nome": "co.ativa_r", "divisor":	1,"descricao": "	Medida Potência Ativa Fase R"},
{"tipo": "4X", "addr":	853,"bit": -1		,"nome": "co.ativa_s", "divisor":	1,"descricao": "	Medida Potência Ativa Fase S"},
{"tipo": "4X", "addr":	854,"bit": -1		,"nome": "co.ativa_t", "divisor":	1,"descricao": "	Medida Potência Ativa Fase T"},
{"tipo": "4X", "addr":	855,"bit": -1		,"nome": "co.ativa_total", "divisor":	1,"descricao": "	Medida Potência Ativa Total"},
{"tipo": "4X", "addr":	856,"bit": -1		,"nome": "co.reativa_r", "divisor":	1,"descricao": "	Medida Potência Reativa Fase R"},
{"tipo": "4X", "addr":	857,"bit": -1		,"nome": "co.reativa_s", "divisor":	1,"descricao": "	Medida Potência Reativa Fase S"},
{"tipo": "4X", "addr":	858,"bit": -1		,"nome": "co.reativa_t", "divisor":	1,"descricao": "	Medida Potência Reativa Fase T"},
{"tipo": "4X", "addr":	859,"bit": -1		,"nome": "co.reativa_total", "divisor":	1,"descricao": "	Medida Potência Reativa Total"},
{"tipo": "4X", "addr":	860,"bit": -1		,"nome": "co.aparente_r", "divisor":	1,"descricao": "	Medida Potência Aparente Fase R"},
{"tipo": "4X", "addr":	861,"bit": -1		,"nome": "co.aparente_s", "divisor":	1,"descricao": "	Medida Potência Aparente Fase S"},
{"tipo": "4X", "addr":	862,"bit": -1		,"nome": "co.aparente_t", "divisor":	1,"descricao": "	Medida Potência Aparente Fase T"},
{"tipo": "4X", "addr":	863,"bit": -1		,"nome": "co.aparente_total", "divisor":	1,"descricao": "	Medida Potência Aparente Total"},
{"tipo": "4X", "addr":	868,"bit": -1		,"nome": "co.fp_r", "divisor":	1000,"descricao": "	Medida do Fator de Potência Fase R"},
{"tipo": "4X", "addr":	869,"bit": -1		,"nome": "co.fp_s", "divisor":	1000,"descricao": "	Medida do Fator de Potência Fase S"},
{"tipo": "4X", "addr":	870,"bit": -1		,"nome": "co.fp_t", "divisor":	1000,"descricao": "	Medida do Fator de Potência Fase T"},
{"tipo": "4X", "addr":	871,"bit": -1		,"nome": "co.fp_total", "divisor":	1000,"descricao": "	Medida do Fator de Potência Total"},
{"tipo": "4X", "addr":	874,"bit": -1		,"nome": "co.thd_corrente_r", "divisor":	10,"descricao": "	Medida do THD de Corrente da fase R"},
{"tipo": "4X", "addr":	875,"bit": -1		,"nome": "co.thd_corrente_s", "divisor":	10,"descricao": "	Medida do THD de Corrente da fase S"},
{"tipo": "4X", "addr":	876,"bit": -1		,"nome": "co.thd_corrente_t", "divisor":	10,"descricao": "	Medida do THD de Corrente da fase T"},
{"tipo": "4X", "addr":	877,"bit": -1		,"nome": "co.thd_corrente_n", "divisor":	10,"descricao": "	Medida do THD de Corrente do Neutro"},
{"tipo": "4X", "addr":	886,"bit": -1		,"nome": "co.status_ats48", "divisor":	1,"descricao": "	Variável auxiliar do CLP"},
{"tipo": "4X", "addr":	888,"bit": -1		,"nome": "co.status_atv31", "divisor":	1,"descricao": "	Variável auxiliar do CLP"},
{"tipo": "4X", "addr":	890,"bit": -1		,"nome": "co.status_tesys", "divisor":	1,"descricao": "	Variável auxiliar do CLP"},
{"tipo": "FP", "addr":	884,"bit": -1		,"nome": "co.encoder", "divisor":	1,"descricao": "	Medida da Rotação do Motor (Hz)"},
{"tipo": "4X", "addr":	1216,"bit": -1		,"nome": "co.indica_driver", "divisor":	1,"descricao": "	Indica a partida selecionada (Direta = 0, Soft-start = 1, Inversor = 2)", "permite_escrita":False},
{"tipo": "4X", "addr":	1316,"bit": -1		,"nome": "co.ats48", "divisor":	1,"descricao": "	Controla partida Soft-start (Liga = 1, Desliga = 0, Reset = 2) ", "permite_escrita": True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
{"tipo": "4X", "addr":	1317,"bit": -1		,"nome": "co.ats48_acc", "divisor":	1,"descricao": "	Define a rampa de aceleração do soft-start e inversor (10s a 60s)", "permite_escrita": True},
{"tipo": "4X", "addr":	1318,"bit": -1		,"nome": "co.ats48_dcc", "divisor":	1,"descricao": "	Define a rampa de desaceleração do soft-start e inversor (10s a 60s)", "permite_escrita": True},
{"tipo": "4X", "addr":	1319,"bit": -1		,"nome": "co.tesys", "divisor":	1,"descricao": "	Controla partida Direta (Liga = 1, Desliga = 0, Reset = 2) ", "permite_escrita": True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
{"tipo": "4X", "addr":	1324,"bit": -1		,"nome": "co.sel_driver", "divisor":	1,"descricao": "	Seleciona o Tipo de Partida  (Soft-start = 1, Inversor = 2, Direta = 3)", "permite_escrita": True,"valores_de_escrita":[1,2,3],"descricao_de_escrita":["Soft-Start","Inversor","Direta"]},
{"tipo": "4X", "addr":	1332,"bit": -1		,"nome": "co.sel_pid", "divisor":	1,"descricao": "	Seleciona o tipo de PID (Automático = 0, Manual = 1)", "permite_escrita": True,"valores_de_escrita":[0,1],"descricao_de_escrita":["Automático","Manual"]},
{"tipo": "4X", "addr":	1204,"bit": -1		,"nome": "co.demanda_anterior", "divisor":	10,"descricao": "	Medida de Demanda Anterior"},
{"tipo": "4X", "addr":	1205,"bit": -1		,"nome": "co.demanda_atual", "divisor":	10,"descricao": "	Medida de Demanda Atual"},
{"tipo": "4X", "addr":	1206,"bit": -1		,"nome": "co.demanda_media", "divisor":	10,"descricao": "	Medidade de Demanda Média"},
{"tipo": "4X", "addr":	1207,"bit": -1		,"nome": "co.demanda_pico", "divisor":	10,"descricao": "	Medidade de Demanda de Pico"},
{"tipo": "4X", "addr":	1208,"bit": -1		,"nome": "co.demanda_prevista", "divisor":	10,"descricao": "	Medida de Demanda Prevista"},
{"tipo": "4X", "addr":	1210,"bit": -1		,"nome": "co.energia_ativa", "divisor":	1,"descricao": "	Medida da Energia Ativa"},
{"tipo": "4X", "addr":	1212,"bit": -1		,"nome": "co.energia_reativa", "divisor":	1,"descricao": "	Medida da Energia Reativa"},
{"tipo": "4X", "addr":	1214,"bit": -1		,"nome": "co.energia_aparente", "divisor":	1,"descricao": "	Medida da Energia Aparente"},
{"tipo": "4X", "addr":	1312,"bit": -1		,"nome": "co.atv31", "divisor":	1,"descricao": "	Controla partida Inversor (Liga = 1, Desliga = 0, Reset = 2) ", "permite_escrita": True,"valores_de_escrita":[1,0,2],"descricao_de_escrita":["Liga","Desliga","Reset"]},
{"tipo": "4X", "addr":	1313,"bit": -1		,"nome": "co.atv31_velocidade", "divisor":	10,"descricao": "	Define a velocidade do Inversor (0 a 60Hz)"},
{"tipo": "4X", "addr":	1328,"bit": 	1	,"nome": "co.habilita", "divisor":	1,"descricao": "	Indica Motor ligado ou não"},
{"tipo": "FP", "addr":	1302,"bit": -1		,"nome": "co.sp_pid", "divisor":	1,"descricao": "	Define a Vazão no PID (SP- Set Point)", "permite_escrita": True},
{"tipo": "FP", "addr":	1304,"bit": -1		,"nome": "co.p", "divisor":	1,"descricao": "	Define o valor do Controle Proporcional", "permite_escrita": True},
{"tipo": "FP", "addr":	1306,"bit": -1		,"nome": "co.i", "divisor":	1,"descricao": "	Define o valor do Controle Integral", "permite_escrita": True},
{"tipo": "FP", "addr":	1308,"bit": -1		,"nome": "co.d", "divisor":	1,"descricao": "	Define o valor do Controle Derivativo]", "permite_escrita": True},
{"tipo": "FP", "addr":	1310,"bit": -1		,"nome": "co.mv_escreve", "divisor":	1,"descricao": "	Define o valor da Variável Manipulada (MV em porcentagem)", "permite_escrita": True},
{"tipo": "FP", "addr":	1314,"bit": -1		,"nome": "co.pv_pid", "divisor":	1,"descricao": "	Valor lido da Vazão (PV - Variável de Processo)"},
{"tipo": "FP", "addr":	1420,"bit": -1		,"nome": "co.torque", "divisor":	1,"descricao": "	Medida do Torque"}
]
"""