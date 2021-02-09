''' 
    TRABALHO PRATICO
    GCC108 - Teoria da Computacao
    Nome: Juliano Expedito de Andrade Godinho
    Turma: 14A
    Matricula: 201811302
    
'''

# Funcao para checar se a fita esta correta!
def checarFita(fita, alfabeto):
    
    for f in fita:
        # Se nao pertencer ao alfabeto, retorna False e a letra do alfabeto
        if f not in alfabeto:
            return False, f
    
    # Caso o alfabeto esteja correto, retorna True e uma string vazia
    return True, ''


# Utilizando o sys para abertura do arquivo
import sys

# Uma lista com os estados
# Cada posicao representa um estado que contem um dicionario com as transicoes
# [{}, {}, {}]
estados = []

# Alfabeto de entrada
alfabeto_entrada = []

# Alfabeto da fita
alfabeto_fita = []
        
# Abrindo o arquivo
f = open(sys.argv[1])

# Leitura do inicio
f.read(3)

# Lendo os estados
while f.read(1) != ',':
    
    # Lendo cada estado e uma virgula
    f3 = f.read(3)
    
    # Adicionando um dicionario vazio a lista de estados
    estados.append({})
    
    
# Leitura apos os estados
f.read(2)


# Lendo o alfabeto de entrada
while f.read(1) != ',':
    
    f2 = f.read(2)
    
    alfabeto_entrada.append(f2[0])
    
    
# Leitura apos alfabeto de entrada
f.read(2)


# Lendo o alfabeto da fita
while f.read(1) != '}':
    
    # Lendo uma letra do alfabeto
    f1 = f.read(1)
    
    # Adicionando ao alfabeto
    alfabeto_fita.append(f1)
    
    # Cria uma chave que corresponde a letra do alfabeto em cada estado na lista de estados
    for estado in estados:
        estado[f1] = {}


# Leitura apos o alfabeto da fita
f.read(4)


# Escrevendo as transicoes no dicionario de cada estado
while f.read(3)[1] != '}':
    
    # Lendo a linha da transicao
    # Exemplo(22 caracteres):  (q0, B) -> (q1, B, R),
    transicao = f.read(22)
    
    # Pegando o estado da lista estados
    estado = estados[eval(transicao[2])]
   
    '''
        Exemplo do formato:
            Estado q0 -> portanto pega-se a posicao 0 da lista de estados
            No dicionario desta posicao, entao se adiciona uma chave que corresponde a leitura
            E seu valor e uma tupla que corresponde (qj, y, D)
            Sendo qj o destino da transicao
            y a escrita
            e D a direcao
        Exemplo:
            (q0, B) -> (q1, B, R),
            Posicao 0 na lista estados
            {'B' : (q1, B, R)}
            Portanto, o estado q0 ao ler B, ira para q1, escrevera B na fita e ira para direita
    '''
    estado[transicao[5]]= (transicao[13], transicao[16], transicao[19])
    
    
# Guardando o estado inicial
estado_inicial = f.read(8)[3]

# Lendo a fita (Restante do arquivo)
fita = f.readlines()[0]

# Fechando o arquivo
f.close()

# Criando o estado atual
estado_atual = estado_inicial

# Posicao da fita
pos = 0

# Realizando a checagem da fita
checagem = checarFita(fita, alfabeto_fita)

# Caso a checagem esteja correta (True), entra no while para percorrer a fita
if checagem[0]:
    
    # Criando o arquivo para saida - Cria-se apenas se nao houver erro na fita
    f = open(sys.argv[2], 'w')
    
    # Loop
    while True:
        
        # Escrevendo a fita no arquivo
        f.write(fita[:pos] + '{{q{}}}'.format(estado_atual) + fita[pos:] + '\n')
        
        # Recebendo o estado
        estado = estados[eval(estado_atual)]
        
        # Leitura da posicao atual da fita
        leitura = fita[pos]
        
        # Tupla -> (Destino, Escrita, Movimento)
        tupla = estado[leitura]
        
        # Condicao de Parada
        # Caso o estado atual nao consiga transitar com a posicao atual da fita, programa para!
        if tupla == {}:
            break
        
        # Organizando e escrevendo na fita
        fita = fita[:pos] + tupla[1] + fita[pos+1:]
        
        # Movimentando
        if tupla[2] == 'R':
            pos += 1
        else: pos -= 1
        
        # Alterando o estado atual
        estado_atual = tupla[0]
    
# Caso a fita esteja incorreta, emite uma mensagem, indicando o erro na fita
else:
    print('Fita incorreta - Arquivo nao foi criado! {} nao pertence ao alfabeto da fita!'.format(checagem[1]))
        