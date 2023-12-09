import requests

class GrafoPonderado:
    
    def __init__(self) -> None:
        self.lista_adj = {}
        self.num_nos = 0
        self.num_arestas = 0

    def adicionar_no(self, no):
        if no in self.lista_adj:
            print(f"AVISO: No {no} ja existe")
            return
        self.lista_adj[no] = {}
        self.num_nos += 1

    def adicionar_aresta(self, no1, no2, peso):
        if no1 not in self.lista_adj:
            self.adicionar_no(no1)
        if no2 not in self.lista_adj:
            self.adicionar_no(no2)
        self.lista_adj[no1][no2] = peso
        self.num_arestas += 1

    def adicionar_nos(self, nos):
        for no in nos:
            self.adicionar_no(no)

    def adicionar_aresta_bidirecional(self, no1, no2, peso):
        self.adicionar_aresta(no1, no2, peso)
        self.adicionar_aresta(no2, no1, peso)

    def remove_aresta(self, no1, no2):
        try:
          self.lista_adj[no1].pop(no2)
          self.num_arestas -= 1
        except KeyError as e:
            print(f"AVISO: Aresta {no1} -> {no2} não existe")

    def __str__(self):
        saida = ""
        for no in self.lista_adj:
            saida += str(no) + " -> " + str(self.lista_adj[no]) + "\n"
        return saida
    
    def ler_arquivo(self, nome_arquivo):
        file = open(nome_arquivo, 'r')
        i = 0
        for linha in file:
            i += 1
            if i == 1:
                continue
            conteudo = linha.strip().split(" ")
            u = conteudo[0]
            v = conteudo[1]
            w = int(conteudo[2])
            self.adicionar_aresta(u, v, w)
        file.close()

    def remove_no(self, no):
        for no2 in self.lista_adj:
            if no in self.lista_adj[no2]:
                self.lista_adj[no2].pop(no)
                self.num_arestas -= 1
        self.num_arestas -= len(self.lista_adj[no])
        self.num_nos -= 1
        self.lista_adj.pop(no)

    def bellman_ford(self, s):
        dist = {}
        pred = {}
        for no in self.lista_adj:
            dist[no] = float('inf')
            pred[no] = None
        dist[s] = 0
        for i in range(self.num_nos - 1):
            for u in self.lista_adj:
                for v in self.lista_adj[u]:
                    w = self.lista_adj[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
        return (dist, pred)

    def bellman_ford_melhorado(self, s):
        dist = {}
        pred = {}
        for no in self.lista_adj:
            dist[no] = float('inf')
            pred[no] = None
        dist[s] = 0
        for i in range(self.num_nos - 1):
            trocou = False
            for u in self.lista_adj:
                for v in self.lista_adj[u]:
                    w = self.lista_adj[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
                        trocou = True
            if not trocou:
                break
        return (dist, pred)
    
    def is_link(self, node_in, node_out):
        return node_out in self.lista_adj[node_in]
    
    def pound_of(self, node_in, node_out):
        if not self.is_link(node_in, node_out): return None
        return self.lista_adj[node_in][node_out]
    
    