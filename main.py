import numpy


if __name__=="__main__":
    # print(numpy.std([0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6553.5, 6553.5, 6553.5]))
    dicionario_de_dados = {}
    dicionario_de_dados["Partida Soft"] = {"Motor Desligado":{},"Motor Ligado":{}}
    dicionario_de_dados["Partida Inversora"] = {"Motor Desligado":{},"Motor Ligado em 0Hz":{},"Motor Ligado em 30Hz":{},"Motor Ligado em 60Hz":{}}
    dicionario_de_dados["Partida Direta"] = {"Motor Desligado":{},"Motor Ligado":{}}

    print("nome_motor"+":\n")
    for key, value in dicionario_de_dados.items():
        print(f"    {key}:\n")
        for key2,value2 in value.items():
            print(f"        {key2}:\n")
            for reg,lista in value2.items():
                print(f"          {reg.nome} ({reg.descricao}):\n")
                print(f"              max: {max(lista)},  min: {min(lista)},  media: {sum(lista)/len(lista)},   std: {np.std(lista)},   valores: {lista}")
                if reg.confere == True:
                    print(f" /****/")
                print("\n")