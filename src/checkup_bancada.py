import maquinas.bomba as bomba
import numpy as np
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

class CheckupBancada():
    _lock = Lock()
    #_isLocal = False
    _comunicadorModbus:ComunicadorModbus

    _caminho_relatorio:str
    _caminho_dados:str

    _dict_controle_motor:dict
    _list_registrador_motor:list
    _list_registrador_linear:list

    _turn_on_cooldown:float
    _turn_off_cooldown:float
    _switch_cooldown:float    
    
    _max_std_aceitavel:float

    _debug_log:False

    nome_bancada:str

    def __init__(self,ip:str,porta:str,islocal:bool = False,**kwargs):
        self._comunicadorModbus = ComunicadorModbus("localhost" if islocal else ip, porta)

        if self._comunicadorModbus.connect() == False:
            print("servidor nao encontrado")
            sys.exit()

        self._list_registrador_linear = None

        saida = kwargs.get("caminho_pasta","saida")
        bancada = kwargs.get("nome_bancada","bancada")
            
        self._caminho_relatorio = saida+"\\relatorio_"+bancada+".txt"
        self._caminho_dados = saida+"\\dados_"+bancada+".txt"
        self.nome_bancada = bancada

        self._bool_primeira_escrita_dados=True
        self._bool_primeira_escrita_relatorio=True

        self._numero_de_amostras = kwargs.get("numero_de_amostras",10)
        self._tempo_entre_coleta_de_amostras = kwargs.get("tempo_de_amostra",0.5)
        self._turn_on_cooldown = kwargs.get("on_cooldown",1)
        self._turn_off_cooldown = kwargs.get("off_cooldown",1)
        self._switch_cooldown = kwargs.get("on_cooldown",2)

        self._max_std_aceitavel = kwargs.get("max_std", 100)

        self._debug_log = kwargs.get("debug",False)
        pass

    def __del__(self):
        self._comunicadorModbus.close_connection()
        pass

    def escreve_no_relatorio(self,informacao:str):
        if self._bool_primeira_escrita_relatorio:
            with open(self._caminho_relatorio,'w') as f:
                f.write("")
            self._bool_primeira_escrita_relatorio = False

        with open(self._caminho_relatorio,'a') as f:
            f.write(informacao)

        pass
    def escreve_dado(self,informacao:str):
        if self._bool_primeira_escrita_dados:
            with open(self._caminho_dados,'w') as f:
                f.write("")
            self._bool_primeira_escrita_dados = False

        with open(self._caminho_dados,'a') as f:
            f.write(informacao)

        pass

    def set_controle_motor(self, lista:list):
        self._dict_controle_motor = dict()
        for i in lista:
            self._dict_controle_motor[i.get("funcao")] = Registrador(self._comunicadorModbus,i)
            pass
        pass

    def set_registrador_motor(self, lista:list):
        self._list_registrador_motor = list()
        for i in lista:
            self._list_registrador_motor.append(Registrador(self._comunicadorModbus,i)) 
        pass

    def set_registrador_linear(self, lista:list):
        self._list_registrador_linear = list()
        for i in lista:
            self._list_registrador_linear.append(Registrador(self._comunicadorModbus,i)) 
        pass
    
    def leitura_controle_motor(self):
        with self._lock:
            for reg in self._dict_controle_motor.values():
                reg.leitura()
        pass
    def leitura_registrador_motor(self):
        with self._lock:
            for reg in self._list_registrador_motor:
                reg.leitura()
        pass
    def leitura_registrador_linear(self):
        with self._lock:
            for reg in self._list_registrador_linear:
                reg.leitura()
        pass

    def desliga_motor(self):
        if self._comunicadorModbus.Ip == "localhost":
            return

        self.leitura_controle_motor()

        soft = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura
        inv = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura
        dir = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura

        if self._debug_log:
            print("desligando motor...")
            print(f"{dir}, {inv}, {soft}")

        #comando para desligar
        if dir+inv+soft == 0:
            if self._debug_log:
                input("motor ja esta desligado, prosseguir?")
                print("motor desligado.")
            return
        
        if dir == 1:
            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_tesys).escrita(0)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura == 1:
                sleep(0.5)
                self.leitura_controle_motor()
        elif soft == 1:
            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48).escrita(0)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura == 1:
                sleep(0.5)
                self.leitura_controle_motor()
        elif inv == 1:
            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31).escrita(0)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura == 1:
                sleep(0.5)
                self.leitura_controle_motor()
        else:
            input("erro ao desligar. Realize a operacao manualmente e depois pressione para proseguir.")
        """
            dir = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura
            soft = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura
            inv = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura

            #comando para resetar
            if dir == 2:
                with self._lock:
                    self._dict_controle_motor.get(FuncaoRegistrador.mot_tesys).escrita(2)
                while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura != 0:
                    sleep(0.5)
                    with self._lock:
                        self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).leitura()
            elif soft == 2:
                with self._lock:
                    self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48).escrita(2)
                while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura != 0:
                    sleep(0.5)
                    with self._lock:
                        self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).leitura()
            elif inv == 2:
                with self._lock:
                    self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31).escrita(2)
                while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura != 0:
                    sleep(0.5)
                    with self._lock:
                        self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).leitura()
                
        """
        if self._debug_log:
            print("tempo de espera...")
        sleep(self._turn_off_cooldown)
        if self._debug_log:
            print("motor desligado.")
        pass

    def liga_motor(self):
        if self._comunicadorModbus.Ip == "localhost":
            return

        if self._debug_log:
            print("ligando motor...")

        self.leitura_controle_motor()

        soft = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura
        inv = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura
        dir = self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura

        if (dir + soft + inv >= 1):
            if self._debug_log:
                print(f"liga_motor chamado com motor ligado. d[{dir}], s[{soft}], i[{inv}]")
            self.desliga_motor()
        
        driver = self._dict_controle_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura

        if driver == 1:
            limite = 0

            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48).escrita(1)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura == 0:
                if limite >= 40:
                    input("nao foi possível ligar o motor na partida selecionada. Pressione para prosseguir.")
                    break
                limite = limite +1
                
                sleep(0.5)
                self.leitura_controle_motor()
        elif driver == 2:
            limite = 0

            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31).escrita(1)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura == 0:
                if limite >= 40:
                    input("nao foi possível ligar o motor na partida selecionada. Pressione para prosseguir.")
                    break
                limite = limite +1
                
                sleep(0.5)
                self.leitura_controle_motor()
        elif driver == 3:
            limite = 0

            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mot_tesys).escrita(1)
            while self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura == 0:
                if limite >= 40:
                    input("nao foi possível ligar o motor na partida selecionada. Pressione para prosseguir.")
                    break
                limite = limite +1
                
                sleep(0.5)
                self.leitura_controle_motor()
        else:
            input("indica_driver com valor fora do esperado, ligue o motor manualmente e depois pressione para prosseguir")
       
        if self._debug_log:
            print("tempo de espera...")
        sleep(self._turn_on_cooldown)
        if self._debug_log:
            print("motor ligado.")
        pass

    def seleciona_partida(self,partida):
        "soft = 1, inversora = 2, direta = 3"
        if self._comunicadorModbus.Ip == "localhost":
            return

        self.leitura_controle_motor()
        if self._debug_log:
            print("selecionando partida...")

        if (self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura + self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura + self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura)>1:
            if self._debug_log:
                print("trocando partida com motor em reset")
            self.desliga_motor()
        
        if (self._dict_controle_motor.get(FuncaoRegistrador.mot_status_ats48).valor_de_leitura + self._dict_controle_motor.get(FuncaoRegistrador.mot_status_atv31).valor_de_leitura + self._dict_controle_motor.get(FuncaoRegistrador.mot_status_tesys).valor_de_leitura)>0:
            if self._debug_log:
                print("trocando partida com motor ligado")
            self.desliga_motor()
        
        with self._lock:
            self._dict_controle_motor.get(FuncaoRegistrador.mot_sel_driver).escrita(partida)
        while self._dict_controle_motor.get(FuncaoRegistrador.mot_indica_driver).valor_de_leitura != partida:
            sleep(0.5)
            self.leitura_controle_motor()
        
        if self._debug_log:
            print("tempo de espera...")
        sleep(self._switch_cooldown)
        if self._debug_log:
            print("partida selecionada.")

        pass
    
    def prepara_partida_soft(self):
        self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48_acc).escrita(15)
        self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48_dcc).escrita(15)
        sleep(0.5)
        self.leitura_controle_motor()
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48_acc).valor_de_leitura != 15:
            input(f"erro ao atualizar variavel do motor ats48_acc, mude manualmente e aperte para prosseguir.")
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_ats48_dcc).valor_de_leitura != 15:
            input(f"erro ao atualizar variavel do motor ats48_dcc, mude manualmente e aperte para prosseguir.") 
        pass
    def prepara_partida_inv(self):
        self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_velocidade).escrita(0)
        self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_acc).escrita(15)
        self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_dcc).escrita(15)
        sleep(0.5)
        self.leitura_controle_motor()
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_velocidade).valor_de_leitura != (0):
            input(f"erro ao atualizar variavel do motor atv31_velocidade para {0}, mude manualmente e aperte para prosseguir.")
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_acc).valor_de_leitura != (15):
            input(f"erro ao atualizar variavel do motor atv31_acc para {15}, mude manualmente e aperte para prosseguir.")
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_dcc).valor_de_leitura != (15):
            input(f"erro ao atualizar variavel do motor atv31_dcc para {15}, mude manualmente e aperte para prosseguir.")
        pass
    def inv_velocidade(self,valor:int):
        self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_velocidade).escrita(valor)
        sleep(0.5)
        self.leitura_controle_motor()
        if self._dict_controle_motor.get(FuncaoRegistrador.mot_atv31_velocidade).valor_de_leitura != (valor):
            input(f"erro ao atualizar variavel do motor atv31_velocidade para {valor}, mude manualmente e aperte para prosseguir.")

    def processa_lista(self,registrador:Registrador, lista_dados:list,**kwargs):
        defeito = False
        resposta = f"{registrador.nome}[{registrador.endereco}]: "
        isOn = kwargs.get("motor_ligado", False)
        if registrador.variacao_por_rotacao:
            multiplicador = kwargs.get("multiplicador", 1)
        else:
            multiplicador = 1

            
        if registrador.somente_varicao:
            if np.std(lista_dados)>registrador.valor_esperado_desligado[0]:
                defeito = True
                resposta+= f"(STD[{np.std(lista_dados)}] muito alto) "
        else:
            media = sum(lista_dados)/len(lista_dados)
            val_max = 0 
            val_min = 0 
            if isOn:
                val_max = (registrador.valor_esperado_ligado[0]*multiplicador)+registrador.valor_esperado_ligado[1]
                val_min = (registrador.valor_esperado_ligado[0]*multiplicador)-registrador.valor_esperado_ligado[1]
            else:
                val_max = (registrador.valor_esperado_desligado[0]*multiplicador)+registrador.valor_esperado_desligado[1]
                val_min = (registrador.valor_esperado_desligado[0]*multiplicador)-registrador.valor_esperado_desligado[1]
            
            if not (media<=val_max) or not (media>=val_min):
                defeito = True
                resposta+= f"(Media[{media}] incoerente) "
            if np.std(lista_dados)>self._max_std_aceitavel:
                defeito = True
                resposta+= f"(STD[{np.std(lista_dados)}] muito alto) "
            if max(lista_dados) > 65000:
                defeito = True
                resposta += f"(Valor saturado [{max(lista_dados)}])"
        
            

        if not defeito:
            resposta = ""
            
        return defeito, resposta
    
    def escreve_relatorio(self, dicionario:dict,nome_motor:str):
        self.escreve_dado("")
        self.escreve_no_relatorio("")
        with open(self._caminho_relatorio,'a') as f:
            f.write(nome_motor+":\n")
            for key, value in dicionario.items():
                f.write(f"    {key}:\n")
                for key2,value2 in value.items():
                    f.write(f"        {key2}:\n")
                    
                    const = 1

                    if key2 == "Motor Desligado":
                        for reg,lista in value2.items():
                            if reg.valor_esperado_desligado == None:
                                continue

                            defeito, resposta = self.processa_lista(reg,lista)
                            if defeito:
                                f.write(f"            {resposta}\n")
                            pass
                        continue
                    else:
                        if key2 == "Motor Ligado em 0Hz":
                            const = 0
                        elif key2 == "Motor Ligado em 30Hz":
                            const = 0.5
                        elif key2 == "Motor Ligado em 60Hz":
                            const = 1.2
                        for reg,lista in value2.items():
                            if reg.valor_esperado_ligado == None:
                                continue

                            defeito, resposta = self.processa_lista(reg,lista,motor_ligado=True,multiplicador=const)
                            if defeito:
                                f.write(f"            {resposta}\n")
                            pass
                        pass
                    pass
                pass
            pass

        with open(self._caminho_dados,'a') as f:
            f.write(nome_motor+":\n")
            for key, value in dicionario.items():
                f.write(f"    {key}:\n")
                for key2,value2 in value.items():
                    f.write(f"        {key2}:\n")
                    for reg,lista in value2.items():
                        f.write(f"          {reg.nome} ({reg.descricao}):\n")
                        f.write(f"              max: {max(lista)},  min: {min(lista)},  media: {sum(lista)/len(lista)},   std: {np.std(lista)},   valores: {lista}")
                        if reg.confere == True:
                            f.write(f" /****/")
                        f.write("\n")

        return

    def coleta_dados_motor(self, partida_direta=False):

        #nao le coisa errada 
        sleep(self._tempo_entre_coleta_de_amostras)
        self.leitura_registrador_motor()
        sleep(self._tempo_entre_coleta_de_amostras)
        self.leitura_registrador_motor()
        sleep(self._tempo_entre_coleta_de_amostras)
        self.leitura_registrador_motor()
        sleep(self._tempo_entre_coleta_de_amostras)
        #---------------

        dict_saida = {}
        for reg in self._list_registrador_motor:
            dict_saida[reg] = []
        if partida_direta:
            if self._list_registrador_linear != None:
                for reg in self._list_registrador_linear:
                    dict_saida[reg] = []
        
        temp = 0
        for num in range(0,self._numero_de_amostras):
            
            if temp > 2*self._tempo_entre_coleta_de_amostras:
                print(f"{((num/self._numero_de_amostras)*100):.1f}%")
                temp = 0

            self.leitura_registrador_motor()
            if partida_direta:
                if self._list_registrador_linear != None:
                    self.leitura_registrador_linear()

            for reg in dict_saida.keys():
                dict_saida[reg].append(reg.valor_de_leitura)

            sleep(self._tempo_entre_coleta_de_amostras)
            temp = temp + self._tempo_entre_coleta_de_amostras


        return dict_saida

    def comeca_checkup(self): 

        with self._lock:
            self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()        
        if self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == None:
            print(f"\n--------------------------\nComunicador não esta recebendo informação do servidor. Operação cancelada.\nIP : {self._comunicadorModbus.Ip} , PORTA: {self._comunicadorModbus.Porta}")
            sys.exit()

        
        leitura_verde = False
        leitura_azul = False

        print(f"Favor ligar o motor do(a) {self.nome_bancada} antes de comecar.")

        while self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 0:
            print(f"Favor ligar o motor do(a) {self.nome_bancada} antes de comecar.")
            sleep(5)
            with self._lock:
                self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).leitura()
            pass

        while not leitura_verde or not leitura_azul:
            # self.confere_controle()

            # GPSTERCO
            tipos_motor = {1: "Motor VERDE (1)", 2: "Motor AZUL (2)"}
            tipo_motor = self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura
            nome_do_motor = tipos_motor.get(tipo_motor, "Tipo de motor desconhecido")
            print(f"----------------\n{nome_do_motor} selecionado.\n----------------")

            self.desliga_motor()

            dicionario_de_dados = {}
            dicionario_de_dados["Partida Soft"] = {"Motor Desligado":{},"Motor Ligado":{}}
            dicionario_de_dados["Partida Inversora"] = {"Motor Desligado":{},"Motor Ligado em 0Hz":{},"Motor Ligado em 30Hz":{},"Motor Ligado em 60Hz":{}}
            dicionario_de_dados["Partida Direta"] = {"Motor Desligado":{},"Motor Ligado":{}}


            r = input("pressione para começar a leitura dos dados na partida soft-start.")
            if not r.strip():
                r=0
            else:
                r = int(r)
            
            if r != -3:
                r = -2
                while r == -2:
                    print("Partida Soft:")
                    self.seleciona_partida(1)
                    self.prepara_partida_soft()
                    
                    print("motor desligado...")
                    dicionario_de_dados["Partida Soft"]["Motor Desligado"] = self.coleta_dados_motor()

                    self.liga_motor()
                    print("motor ligado...")
                    dicionario_de_dados["Partida Soft"]["Motor Ligado"] = self.coleta_dados_motor()
                    self.desliga_motor()
                    
                    r = input("pressione para começar a leitura dos dados na partida inversora.")
                    if not r.strip():  
                        r=0
                    else:
                        r = int(r)
            
            if r != -3:
                r=-2
                while r == -2:
                    print("Partida Inversora:")
                    self.seleciona_partida(2)
                    self.prepara_partida_inv()

                    print("motor desligado...")
                    dicionario_de_dados["Partida Inversora"]["Motor Desligado"] = self.coleta_dados_motor()
                    
                    self.liga_motor()
                    print("motor ligado em 0hz...")
                    dicionario_de_dados["Partida Inversora"]["Motor Ligado em 0Hz"] = self.coleta_dados_motor()
                    self.desliga_motor()

                    r = input("pressione para continuar a leitura inversora a 30 hz.")
                    if not r.strip(): 
                        r=0
                    else:
                        r = int(r)
            
            if r != -3:
                r=-2
                while r == -2:
                    self.liga_motor()
                    self.inv_velocidade(30)
                    print("motor ligado em 30hz...")
                    dicionario_de_dados["Partida Inversora"]["Motor Ligado em 30Hz"] = self.coleta_dados_motor()
                    self.desliga_motor()

                    r = input("pressione para continuar a leitura inversora a 60 hz.")
                    if not r.strip():
                        r=0
                    else:
                        r = int(r)
            
            if r != -3:
                r=-2
                while r == -2:
                    self.liga_motor()
                    self.inv_velocidade(60)
                    print("motor ligado 60hz...")
                    dicionario_de_dados["Partida Inversora"]["Motor Ligado em 60Hz"] = self.coleta_dados_motor()
                    self.desliga_motor()

                    r = input("pressione para começar a leitura dos dados na partida direta.")
                    if not r.strip():  
                        r=0
                    else:
                        r = int(r)
            
            if r != -3:
                r=-2
                while r == -2:
                    print("Partida Direta:")
                    self.seleciona_partida(3)

                    print("motor desligado...")
                    dicionario_de_dados["Partida Direta"]["Motor Desligado"] = self.coleta_dados_motor(True)

                    self.liga_motor()
                    print("motor ligado...")
                    dicionario_de_dados["Partida Direta"]["Motor Ligado"] = self.coleta_dados_motor(True)
                    self.desliga_motor()
                    
                    r = input("pressione para prosseguir pro relatorio.")
                    if not r.strip():
                        r=0
                    else:
                        r = int(r)

            self.escreve_relatorio(dicionario_de_dados,nome_do_motor)
            
            if self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 1:
                leitura_verde = True
                
                while self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura != 2 and leitura_azul == False:
                    resposta = input("Favor ligar o motor AZUL(2) da bomba para proseguir. (0 para sair)\n")
                    if resposta == "0":
                        sys.exit()

                    self.leitura_controle_motor()
                    sleep(5)
                    pass
            elif self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura == 2:
                leitura_azul = True

                while self._dict_controle_motor.get(FuncaoRegistrador.mt_tipo_motor).valor_de_leitura != 1 and leitura_verde == False:
                    resposta = input("Favor ligar o motor verde da bomba para proseguir. (0 para sair)\n")
                    if resposta == "0":
                        sys.exit()
                        
                    self.leitura_controle_motor()
                    sleep(5)
                    pass
                pass
            pass
        pass
    
    def checkup_especifico(self):
        ## melhor nao

        nivel_muito_alto_superior= Registrador({"tipo": "4X","addr":	716,"bit": 	4 	,"nome": "bc.naa_tq_superior","divisor": 1, "descricao":	"Indicador de Nível Muito Alto"})
        nivel_muito_alto_inferior= Registrador({"tipo": "4X","addr":	716,"bit": 	7 	,"nome": "bc.naa_tq_superior","divisor": 1, "descricao":	"Indicador de Nível Muito Alto"})
        srsa= Registrador({"tipo": "4X","addr":	716,"bit": 	0 	,"nome": "bc.na_tq_superior","divisor":	1, "descricao":	"Sensor de Reservatório Superior Nível Alto (Ativo = 1)"})
        srsb= Registrador({"tipo": "4X","addr":	716,"bit": 	1 	,"nome": "bc.nb_tq_superior","divisor":	1, "descricao":	"Sensor de Reservatório Superior Nível Baixo (Ativo = 0)"})
        sria= Registrador({"tipo": "4X","addr":	716,"bit": 	2 	,"nome": "bc.na_tq_inferior","divisor":	1, "descricao":	"Sensor de Reservatório Inferior Nível Alto (Ativo = 1)"})
        srib= Registrador({"tipo": "4X","addr":	716,"bit": 	3 	,"nome": "bc.nb_tq_inferior","divisor":	1, "descricao":	"Sensor de Reservatório Inferior Nível Baixo (Ativo = 0)"})
        niv_sup = Registrador({ "tipo": "FP","addr":	714,"bit": -1	,"nome": "bc.lit01","divisor": 1, "descricao":	"Medida do Nível do Reservatório superior (Porcentagem)"})
        pit01 = Registrador({ "tipo": "FP","addr":	710,"bit": -1   ,"nome": "bc.pit01","divisor":	1, "descricao":	"Medida da Pressão PIT-01","valor": [2.5,2.5]})
        fit01 = Registrador({ "tipo": "FP","addr":	712,"bit": -1   ,"nome": "bc.fit01","divisor":	1, "descricao":	"Medida da Vazão FIT-01","valor": [2.5,2.5]})

        input("Espere o tanque superior esvaziar,aguarde um pouco e confirme para prosseguir.")
        sleep(1)

        pass
    
    pass

