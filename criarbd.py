#imprtanto o SQLite3
import sqlite3 as lite

#criando uma conexão
con = lite.connect('dados.db')

#criando tabela categoria
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria (id INTEGER PRIMARY KEY AUTOINCREMENT, nome INTEGER)")

#criado tabela receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Receitas (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")

#criado tabela gastos
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")