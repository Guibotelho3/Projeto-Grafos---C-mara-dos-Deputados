from grafo_ponderado import GrafoPonderado
import json
import requests

class Votacao:
    

    def criar_grafo(self, grafo):
        votacoes = list()
        lista1 = list()
        lista_deputados = dict()
        peso = 0
        f_ano = int(input("Digite um ano para filtrar"))
        if f_ano < 2001 or f_ano > 2023:
            print("Erro! Ano inválido, digite um valor entre 2001 e 2023")
        response = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio={f_ano}-01-01&ordem=DESC&ordenarPor=dataHoraRegistro")
        votacoes = response.json()["dados"]
        print(f"Coletando as informações dos deputados e dos votos...")
        for votacao in votacoes:
            votacao_id = votacao["id"]
            print(f"ID: {votacao_id} ...")
            response2 = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}/votos")
            dados_votos = response2.json()["dados"]
            for voto in dados_votos:
                nome_deputado = voto["deputado_"]["nome"].replace(" ", "_")
                if nome_deputado not in lista_deputados:
                    lista_deputados[nome_deputado] = {} 
                lista_deputados[nome_deputado][votacao_id]= voto["tipoVoto"]
        file = open(f"votacoes_deputados.txt", "wt", encoding="utf-8")
        lista_deputados_ordenada = sorted(lista_deputados.items(), key=lambda x: len(x[1]), reverse=True)
        for d in lista_deputados:
            file.write(f"{d} {len(lista_deputados[d])}\n") 
        file.close()
        file = open(f"grafo.txt", "wt", encoding="utf-8")
        for i in range(len(lista_deputados_ordenada)- 1):
            d1 = lista_deputados_ordenada[i][0] 
            v1 = lista_deputados_ordenada[i][1] 
            son_d1 = v1.values()
            for k in range(i+1, len(lista_deputados_ordenada)):
                d2 = lista_deputados_ordenada[k][0] 
                v2 = lista_deputados_ordenada[k][1] 
                son_d2 = v2.values 
                if d1!= d2:
                    if v1.keys() == v2.keys():
                        if son_d1 == son_d2: 
                            peso = peso + 1
                            grafo.adicionar_aresta_bidimensional(d1,d2,peso)
                file.write(f"{grafo.num_nos} {grafo.num_arestas}\n")
                file.write(f"{d1} {d2} {peso}\n")
        file.close()
        print("O grafo foi criado no arquivo .txt localizado no diretório do projeto")
        return lista_deputados
