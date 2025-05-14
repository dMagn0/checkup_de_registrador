import maquinas.esteira as esteira 
from src.funcao_registrador import FuncaoRegistrador
from src.comunicador_modbus import ComunicadorModbus
from src.registrador import ListaRegistrador, Registrador
from threading import Thread
from time import sleep
import sys
from threading import Lock 

def variacao(lista:list) -> float:
    
    valor = 0
    for i in range(len(lista)-1):
        valor += lista[i+1]-lista[i]
    return valor/(len(lista)-1)

def rotina_de_motor(dict:dict) -> bool:
    """
    dict: dicionario com os registradores associados a funcao

    return: true
    """
    string_de_retorno = "Relatorio de comando do motor"
    lock = Lock()

    while dict.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 0:
        print("Favor ligar o motor da esteira antes de comecar.\n")
        sleep(5)
        with lock:
            dict.get(FuncaoRegistrador.mt_tipo_motor).leitura()
        pass
    
    if dict.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 1:
        print("\n----------------\nMotor verde selecionado.\n")
        string_de_retorno+= " VERDE (1): \n"
    elif dict.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 2:
        print("\n----------------\nMotor azul selecionado.\n.")
        string_de_retorno+= " AZUL (2): \n"
    else:
        print("Valor lido do endereço 708 em contradicao com a tabela.")
        string_de_retorno+=" ? :\n"
        inp = int(input("prosseguir para leitura mesmo assim? (0 cancela)"))
        if inp == 0:
            string_de_retorno+= "    Operacao cancelada. Endereco 708 invalido."
            return(False,string_de_retorno)
        pass
    
    print("\nRotina do motor:")
    
    #desligando o motor
    with lock:
        dict.get(FuncaoRegistrador.mot_ats48).escrita(0)
        dict.get(FuncaoRegistrador.mot_atv31).escrita(0)
        dict.get(FuncaoRegistrador.mot_tesys).escrita(0)

    sleep(1.5)

    #confere sel e indica:
    for i in range(1,4):
        with lock:
            dict.get(FuncaoRegistrador.mot_sel_driver).escrita(i)
        sleep(6)
        with lock:
            dict.get(FuncaoRegistrador.mot_sel_driver).leitura()
            dict.get(FuncaoRegistrador.mot_indica_driver).leitura()

        if dict.get(FuncaoRegistrador.mot_sel_driver).valor_de_leitura != dict.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura:
            inp = int(input(f"sel_driver ({dict.get(FuncaoRegistrador.mot_sel_driver).valor_de_leitura}) em contradicao com indica_driver ({dict.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}). Prosseguir?"))
            string_de_retorno+=f"    sel_driver ({dict.get(FuncaoRegistrador.mot_sel_driver).valor_de_leitura}) em contradicao com indica_driver ({dict.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}).\n"
            if inp == 0:
                string_de_retorno+="    Operacao cancelada."
                return(False,string_de_retorno)
            pass

        pass

    lista_val_desejados = [
        [
            20,
            20,
            30,
            20,
            20
        ],
        [
            15,
            15,
            0,
            15,
            15
        ]
    ]
    lista_regs = [
        dict.get(FuncaoRegistrador.mot_ats48_acc),
        dict.get(FuncaoRegistrador.mot_ats48_dcc),
        dict.get(FuncaoRegistrador.mot_atv31_velocidade),
        dict.get(FuncaoRegistrador.mot_atv31_acc),
        dict.get(FuncaoRegistrador.mot_atv31_dcc),
    ]

    for k in range(0,2):
        with lock:
            #altera parametro do motor
            for i,r in enumerate(lista_regs):
                r.escrita(lista_val_desejados[k][i])
        sleep(2)
        #leitura do motor
        for v in lista_regs:
            with lock:
                v.leitura()
            pass    

        for i in range(len(lista_val_desejados[k])):
            if lista_val_desejados[k][i] != lista_regs[i].valor_de_leitura:
                print(f"{lista_regs[i].endereco} com valor ({lista_regs[i].valor_de_leitura}) fora do esperado ({lista_val_desejados[k][i]})")
                string_de_retorno+=f"    {lista_regs[i].endereco} com valor ({lista_regs[i].valor_de_leitura}) fora do esperado ({lista_val_desejados[k][i]})"
            pass
    
    return (True,string_de_retorno)

def coleta_dados_direta(dict_motor:dict,lista_leitura:list) -> dict:

    NUMERO_DE_AMOSTRAS = 10
    TEMPO_ENTRE_AMOSTRA = 1
    lock = Lock()
    
    
    driver = dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura
    #DIRETA:
    if driver != 3:
        with lock:
            dict_motor.get(FuncaoRegistrador.mot_sel_driver).escrita(3)
        sleep(2)
        pass

    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [1]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 3:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [3]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_tesys com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura}], esperado = [0]\n")

    #coleta dados com motor desligado 
    print("coletando com motor desligado...")
    dicionario_de_amostras_motor_desligado = dict()
    lista_estados = esteira.get_estado_desligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_desligado[i] = dict()
        for reg in lista_leitura:
            dicionario_de_amostras_motor_desligado[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_desligado[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass
    
    print("coletando com motor ligado...")

    #coleta com motor ligado
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_tesys).escrita(1)
    sleep(5)

    dicionario_de_amostras_motor_ligado = dict()
    lista_estados = esteira.get_estado_ligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_ligado[i] = dict()
        for reg in lista_leitura:
            reg.leitura()
            dicionario_de_amostras_motor_ligado[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_ligado[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass
    
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_tesys).escrita(0)
    sleep(10)

    """
    with open('saida.txt','w') as f:
        f.write(str(dicionario_de_amostras_motor_desligado))
    """
    return {'desligado':dicionario_de_amostras_motor_desligado,'ligado':dicionario_de_amostras_motor_ligado }

def coleta_dados_soft(dict_motor:dict,lista_leitura:list) -> dict:
    NUMERO_DE_AMOSTRAS = 10
    TEMPO_ENTRE_AMOSTRA = 1
    lock = Lock()
    
    
    driver = dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura

    print("coletando com motor desligado...")
    #SOFT:
    if driver != 1:
        with lock:
            dict_motor.get(FuncaoRegistrador.mot_sel_driver).escrita(1)
        sleep(3)
        pass

    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_ats48).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [1]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [1]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_ats48 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura}], esperado = [0]\n")

    #coleta dados com motor desligado 
    dicionario_de_amostras_motor_desligado = dict()
    lista_estados = esteira.get_estado_desligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_desligado[i] = dict()
        for reg in lista_leitura:
            dicionario_de_amostras_motor_desligado[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_desligado[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass

    print("coletando com motor ligado...")   
    #coleta com motor ligado
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_ats48).escrita(1)
    sleep(5)

    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_ats48).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [0]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [1]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_ats48 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura}], esperado = [1]\n")

    dicionario_de_amostras_motor_ligado = dict()
    lista_estados = esteira.get_estado_ligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_ligado[i] = dict()
        for reg in lista_leitura:
            reg.leitura()
            dicionario_de_amostras_motor_ligado[i][reg] = list()
            pass
        pass


    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_ligado[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass
    
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_ats48).escrita(0)
    sleep(10)
    return {'desligado':dicionario_de_amostras_motor_desligado,'ligado':dicionario_de_amostras_motor_ligado }

def coleta_dados_inv(dict_motor:dict,lista_leitura:list) -> dict:
    NUMERO_DE_AMOSTRAS = 10
    TEMPO_ENTRE_AMOSTRA = 1
    lock = Lock()
    
    
    driver = dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura

    print("coletando com motor desligado...")
    #INVERSOR:
    if driver != 2:
        with lock:
            dict_motor.get(FuncaoRegistrador.mot_sel_driver).escrita(2)
        sleep(3)
        pass

    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_atv31).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [1]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 2:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [2]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_atv31 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura}], esperado = [0]\n")

    #coleta dados com motor desligado 
    dicionario_de_amostras_motor_desligado = dict()
    lista_estados = esteira.get_estado_desligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_desligado[i] = dict()
        for reg in lista_leitura:
            dicionario_de_amostras_motor_desligado[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_desligado[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass
    
    print("coletando com motor ligado(0hz)...")
    #coleta com motor ligado
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_atv31).escrita(1)
        dict_motor.get(FuncaoRegistrador.mot_atv31_velocidade).escrita(0)
        
    sleep(5)

    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_atv31).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [0]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 2:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [2]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_atv31 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura}], esperado = [1]\n")

    dicionario_de_amostras_motor_ligado_0 = dict()
    lista_estados = esteira.get_estado_ligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_ligado_0[i] = dict()
        for reg in lista_leitura:
            reg.leitura()
            dicionario_de_amostras_motor_ligado_0[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_ligado_0[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass

    print("coletando com motor ligado(30hz)...")
    #50%
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_atv31_velocidade).escrita(30)
        
    sleep(3)
    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_atv31).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [0]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 2:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [2]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_atv31 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura}], esperado = [1]\n")

    dicionario_de_amostras_motor_ligado_1 = dict()
    lista_estados = esteira.get_estado_ligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_ligado_1[i] = dict()
        for reg in lista_leitura:
            reg.leitura()
            dicionario_de_amostras_motor_ligado_1[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_ligado_1[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass

    print("coletando com motor ligado(60hz)...")
    #100%
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_atv31_velocidade).escrita(60)
        
    sleep(3)

    with lock:
        dict_motor.get(FuncaoRegistrador.mt_habilita).leitura()
        dict_motor.get(FuncaoRegistrador.mot_indica_driver).leitura()
        dict_motor.get(FuncaoRegistrador.mot_status_atv31).leitura()
    
    if dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura != 0:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        habilita com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mt_habilita).valor_de_leitura}], esperado = [0]\n")
    if dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != 2:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        indica_driver com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura}], esperado = [2]\n")
    if dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura != 1:
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(f"        status_atv31 com valor contraditorio. valor = [{dict_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura}], esperado = [1]\n")

    dicionario_de_amostras_motor_ligado_2 = dict()
    lista_estados = esteira.get_estado_ligado()
    for i,l in enumerate(lista_estados):
        dicionario_de_amostras_motor_ligado_2[i] = dict()
        for reg in lista_leitura:
            reg.leitura()
            dicionario_de_amostras_motor_ligado_2[i][reg] = list()
            pass
        pass

    with lock:
        for i,l in enumerate(lista_estados):
            #escreve estado
            for num_amostras in range(0,NUMERO_DE_AMOSTRAS):
                for reg in lista_leitura:
                    reg.leitura()
                    dicionario_de_amostras_motor_ligado_2[i][reg].append(reg.valor_de_leitura)
                    pass
                sleep(TEMPO_ENTRE_AMOSTRA)
            pass
        pass
    with lock:
        dict_motor.get(FuncaoRegistrador.mot_atv31).escrita(0)
    sleep(5)
    return {'desligado':dicionario_de_amostras_motor_desligado,
            'ligado_0':dicionario_de_amostras_motor_ligado_0,
            'ligado_1':dicionario_de_amostras_motor_ligado_1,
            'ligado_2':dicionario_de_amostras_motor_ligado_2 }

    pass

def escreve_dicionario(dicionario,estado=1):
    
    with open('saida\\esteira.txt','a') as f:
        for key, value in dicionario.items():
            if estado == 0:
                f.write(f"       {esteira.get_estado_desligado()[key]}:\n")
            else:
                f.write(f"       {esteira.get_estado_ligado()[key]}:\n")
            for key2,value2 in value.items():
                f.write(f"          {key2.nome}:\n")
                f.write(f"              maximo: {max(value2)},  minimo: {min(value2)},  media: {sum(value2)/len(value2)},   variacao media por tempo: {variacao(value2)}")
                if key2.confere == True:
                    f.write(f"***********")
                f.write("\n")
    pass
def printa_dados(dict_direta, dict_soft,dict_inversor):
    
    with open('saida\\esteira.txt','a') as f:
        f.write("Partida Direta:\n")
        f.write("   Motor Desligado:\n")
    escreve_dicionario(dict_direta['desligado'],0)
    
    with open('saida\\esteira.txt','a') as f:
        f.write("   Motor Ligado:\n")
    escreve_dicionario(dict_direta['ligado'])
    
    with open('saida\\esteira.txt','a') as f:
        f.write("\nPartida Soft:\n")
        f.write("   Motor Desligado:\n")
    escreve_dicionario(dict_soft['desligado'],0)
    
    with open('saida\\esteira.txt','a') as f:
        f.write("   Motor Ligado:\n")
    escreve_dicionario(dict_soft['ligado'])
    
    with open('saida\\esteira.txt','a') as f:
        f.write("\nPartida Inversora:\n")
        f.write("   Motor Desligado:\n")
    escreve_dicionario(dict_inversor['desligado'],0)
    
    with open('saida\\esteira.txt','a') as f:
        f.write("   Motor Ligado em 0hz:\n")
    escreve_dicionario(dict_inversor['ligado_0'])
    
    with open('saida\\esteira.txt','a') as f:
        f.write("   Motor Ligado em 30hz:\n")
    escreve_dicionario(dict_inversor['ligado_1'])
    
    with open('saida\\esteira.txt','a') as f:
        f.write("   Motor Ligado em 60hz:\n")
    escreve_dicionario(dict_inversor['ligado_2'])
    
    with open('saida\\esteira.txt','a') as f:
        f.write("\n")

    
    pass

def processa_dados(dict_direta, dict_soft,dict_inversor):

    with open('saida\\relatorio_esteira.txt','a') as f:
        f.write(f"    Partida Direta:\n")
        for estado, dicionario_de_valor in dict_direta["desligado"].items():
            f.write(f"        desligado, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_desligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = reg.valor_esperado_desligado[0]+reg.valor_esperado_desligado[1]
                    val_min = reg.valor_esperado_desligado[0]-reg.valor_esperado_desligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_desligado[0]}\n")
        for estado, dicionario_de_valor in dict_direta["ligado"].items():
            f.write(f"        ligado, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_ligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = reg.valor_esperado_ligado[0]+reg.valor_esperado_ligado[1]
                    val_min = reg.valor_esperado_ligado[0]-reg.valor_esperado_ligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_ligado[0]}\n")
        f.write(f"    Partida Soft-Start:\n")
        for estado, dicionario_de_valor in dict_soft["desligado"].items():
            f.write(f"        desligado, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_desligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = reg.valor_esperado_desligado[0]+reg.valor_esperado_desligado[1]
                    val_min = reg.valor_esperado_desligado[0]-reg.valor_esperado_desligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_desligado[0]}\n")
        for estado, dicionario_de_valor in dict_soft["ligado"].items():
            f.write(f"        ligado, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_ligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = reg.valor_esperado_ligado[0]+reg.valor_esperado_ligado[1]
                    val_min = reg.valor_esperado_ligado[0]-reg.valor_esperado_ligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_ligado[0]}\n")
        f.write(f"    Partida Inversora:\n")
        for estado, dicionario_de_valor in dict_inversor["desligado"].items():
            f.write(f"        desligado, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_desligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = reg.valor_esperado_desligado[0]+reg.valor_esperado_desligado[1]
                    val_min = reg.valor_esperado_desligado[0]-reg.valor_esperado_desligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_desligado[0]}\n")
        for estado, dicionario_de_valor in dict_inversor["ligado_0"].items():
            f.write(f"        ligado em 0hz, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_ligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = (reg.valor_esperado_ligado[0]*0)+reg.valor_esperado_ligado[1]
                    val_min = (reg.valor_esperado_ligado[0]*0)-reg.valor_esperado_ligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_ligado[0]}*0\n")
        for estado, dicionario_de_valor in dict_inversor["ligado_1"].items():
            f.write(f"        ligado em 30hz, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_ligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = (reg.valor_esperado_ligado[0]*0.5)+reg.valor_esperado_ligado[1]
                    val_min = (reg.valor_esperado_ligado[0]*0.5)-reg.valor_esperado_ligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_ligado[0]}*.5\n")
        for estado, dicionario_de_valor in dict_inversor["ligado_2"].items():
            f.write(f"        ligado em 60hz, {estado}:\n")
            for reg,lista in dicionario_de_valor.items():
                if reg.valor_esperado_ligado == None:
                    continue
                else:
                    media = sum(lista)/len(lista)
                    val_max = (reg.valor_esperado_ligado[0]*1)+reg.valor_esperado_ligado[1]
                    val_min = (reg.valor_esperado_ligado[0]*1)-reg.valor_esperado_ligado[1]
                    if media<=val_max and media>=val_min:
                        continue
                    else:
                        f.write(f"            {reg.nome}[{reg.endereco}]: valor = {media}, esperado = {reg.valor_esperado_ligado[0]}*1\n")

    return

if __name__=="__main__":
    ip = esteira.get_esteira_ip()
    isLocal = False
    if isLocal:
        ip = "localhost"

    comunicador = ComunicadorModbus(ip, esteira.get_esteira_port())
    lock = Lock()
    
    if comunicador.connect() == False:
        print("servidor nao encontrado")
    

    dict_controlador_motor = dict()
    for i in esteira.get_reg_motor():
        dict_controlador_motor[i.get("funcao")] = Registrador(comunicador,i)
        pass

    #primeira tentativa de leitura
    with lock:
        dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()        
    if dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == None:
        print(f"\n--------------------------\nComunicador não esta recebendo informação do servidor. Operação cancelada.\nIP : {comunicador.Ip} , PORTA: {comunicador.Porta}")
        sys.exit()
    

    with open('saida\\esteira.txt','w') as f:
        f.write("")
    with open('saida\\relatorio_esteira.txt','w') as f:
        f.write("")

    list_reg_saida = list()
    for i in esteira.get_reg_saida_motor():
        list_reg_saida.append(Registrador(comunicador,i)) 

    list_reg_controle = list()
    """
    for i in esteira.get_reg_controle():
        list_reg_controle.append(Registrador(comunicador,i)) 
    
    #confere reg de controle  
    resp, relatorio = confere_controle(list_reg_controle)
    with open('saida\\relatorio_esteira.txt','a') as f:
        f.write(relatorio)
    if resp == False:
        print("Checkup cancelado.")
        sys.exit()
    """

    print("Favor ligar o motor da esteira antes de comecar.\n")

    while dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 0:
        print("Favor ligar o motor da bomba antes de comecar.\n")
        sleep(5)
        with lock:
            dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()
        pass

    leitura_verde = False
    leitura_azul = False

    while not leitura_verde or not leitura_azul:
        #confere motor
        resp, relatorio = rotina_de_motor(dict_controlador_motor)
        with open('saida\\relatorio_esteira.txt','a') as f:
            f.write(relatorio)
        if resp == False:
            print("Checkup cancelado.")
            sys.exit()


        print("\nPartida Direta:")
        dict_direta = coleta_dados_direta(dict_controlador_motor, list_reg_saida)
        print("\nPartida Soft:")
        dict_soft = coleta_dados_soft(dict_controlador_motor, list_reg_saida)
        print("\nPartida Inversora:")
        dict_inversor = coleta_dados_inv(dict_controlador_motor, list_reg_saida)

        processa_dados(dict_direta,dict_soft,dict_inversor)

        if dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 1:
            
            leitura_verde = True
            with open('saida\\esteira.txt','a') as f:
                f.write("Bomba Verde:\n")
            printa_dados(dict_direta,dict_soft,dict_inversor)
            
            while dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura != 2 and leitura_azul == False:
                print("Favor ligar o motor azul da esteira para proseguir.\n")
                with lock:
                    dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()
                sleep(5)
                pass
        elif dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 2:
            
            leitura_azul = True
            with open('saida\\esteira.txt','a') as f:
                f.write("Bomba Azul:\n")
            printa_dados(dict_direta,dict_soft,dict_inversor)
            while dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura != 1 and leitura_verde == False:
                print("Favor ligar o motor verde da esteira para proseguir.\n")
                with lock:
                    dict_controlador_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()
                sleep(5)
                pass
            pass
        pass
    pass
