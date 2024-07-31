import sys
import sqlite3 as lite
from datetime import datetime

# importando pandas
import pandas as pd

#criando uma conexão
con = lite.connect('dados.db')

#========= Inserção de dados===========

#inserindo dados na tabela Renda
def inserir_renda_mensal(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Renda (nome, renda) VALUES (?, ?)"
        cur.execute(query,i)
        
#inserindo dados na tabela Categoria
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i)

#inserindo dados na tabela Receitas
def inserir_receitas(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query,i)

#inserindo dados na tabela Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query,i)
        
# ========= Consultas ===========

#consultando dados da tabela Renda
def consultar_renda_mensal():
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Renda")
        rows = cur.fetchall()
        return rows

#consultando dados da tabela Categoria
def consultar_categoria():
    lista_itens =[]
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
        return lista_itens

#consultando dados da tabela Receitas
def consultar_receitas():
    lista_itens =[]
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
        return lista_itens

#consultando dados da tabela Gastos 
def consultar_gastos():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
        return lista_itens

# ========= Exclusão ===========

#excluindo dados da tabela Categoria    
def excluir_categoria(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Categoria WHERE id = ?"
        cur.execute(query,i)

#excluindo dados da tabela Receitas
def excluir_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id = ?"
        cur.execute(query,i)

#excluindo dados da tabela Gastos
def excluir_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id = ?"
        cur.execute(query,i)

    
def tabela():
    try:
        gastos = consultar_gastos()
        receitas = consultar_receitas()
        tabela_lista = gastos + receitas
    except lite.Error as e:
        print(f"Erro ao compilar tabela: {e}")
        tabela_lista = []
    return tabela_lista

def bar_valores():
    # Receita Total ------------------------
    receitas = consultar_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesas Total ------------------------
    gastos = consultar_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gastos_total = sum(gastos_lista)

    # Despesas Total ------------------------
    saldo_total = receita_total - gastos_total

    return[receita_total,gastos_total,saldo_total]

def percentagem_valor():

    # Receita Total ------------------------
    receitas = consultar_receitas()
    receitas_lista = [i[3] for i in receitas]
    receita_total = sum(receitas_lista)

    # Despesas Total ------------------------
    despesas = consultar_gastos()
    despesas_lista = [i[3] for i in despesas]
    despesas_total = sum(despesas_lista)

    # Verificação para evitar divisão por zero
    if receita_total == 0:
        return [0]  # Pode retornar 0 ou uma mensagem de erro apropriada
    
    # Cálculo da porcentagem
    total = ((receita_total - despesas_total) / receita_total) * 100
    return [total]

def pie_valores():
    gastos = consultar_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista,columns = ['id', 'Categoria', 'Data', 'valor'])

    # Get the sum of the durations per month
    dataframe = dataframe.groupby('Categoria')['valor'].sum()
   
    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias,lista_quantias])     