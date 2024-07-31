from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

# importando Pillow
from PIL import Image, ImageTk

# Importando barra de progresso do Tlinter
from tkinter.ttk import Progressbar

# Importando Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# importando calendario
from tkcalendar import Calendar, DateEntry
from datetime import date

# Importando função da view
from view import *

# cores 
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"   
co6 = "#038cfc"   
co7 = "#3fbfb9"   
co8 = "#263238"   
co9 = "#e9edf5"   

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# Criando tela
tela = Tk() 
tela.geometry("900x650") # Tamanho da tela
tela.configure(background=co9) # Cor de fundo
tela.resizable(width=FALSE, height=FALSE) # Tamanho fixo(Não permite maximinizar)

 # Estilo da janela
style = ttk.Style(tela)
style.theme_use("clam") # Tema da tela

# Criando frames para divisão da tela
frameCima = Frame(tela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(tela, width=1043, height=361, bg=co1,pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(tela, width=1043, height=300, bg=co1,relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pizza = Frame(frameMeio, width=580, height=250, bg=co2)
frame_gra_pizza.place(x=415, y=5)

# Trabalhando no frame de cima

# Acessando a imagem
app_img = Image.open("icons/log.png")
app_img = app_img.resize((45, 45)) # Tamanho da imagem
app_img = ImageTk.PhotoImage(app_img)

# Criando o label
app_logo = Label(frameCima, image=app_img, text="Orçamento Pessoal", width=900, compound=LEFT, padx=5, 
                 relief=RAISED, anchor=NW, font=("Verdana 20 bold"), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# Botao Sair do lado direito do frameCima
img_sair  = Image.open('icons/sair.png')
img_sair = img_sair.resize((20, 20))
img_sair = ImageTk.PhotoImage(img_sair)
botao_sair = Button(frameCima, image=img_sair, compound=LEFT, anchor=NW, text="   Sair".upper(), width=80, 
                    overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0, command=tela.destroy)
botao_sair.place(x=800, y=10)
# definindo tree como global
global tree

# Função inserir categoria
def inserir_categoria_b():
    nome = e_n_categoria.get()
    
    lista_inserir = [nome]
    
    for i in lista_inserir:
        if i== '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    # Passando a lista para a função inserir gastos presente na view
    inserir_categoria(lista_inserir)
    
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    
    e_n_categoria.delete(0, 'end')
    
    # Pegando os valores da categoria 
    categorias_funcao = consultar_categoria()
    categoria = []
    
    for i in categorias_funcao:
        categoria.append(i[1])
    
    # Atualizando a lista de categorias
    combo_categoria_despesas['values'] = (categoria)


# Função inserir receitas
def inserir_receita_b():
    nome = "Receita"
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()
    
    lista_inserir = [nome, data, quantia]
    
    if any(i == '' for i in lista_inserir):
        messagebox.showerror('Erro', 'Preencha todos os campos')
        return
        
    inserir_receitas(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    
    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')
    
    # Atualizando a tabela
    mostrar_renda()
    percentagem()
    grafico_barra()
    resumo_total()
    grafico_pizza()
    

def inserir_despesas_b():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesas.get()
    
    lista_inserir = [nome, data, quantia]
    
    if any(i == '' for i in lista_inserir):
        messagebox.showerror('Erro', 'Preencha todos os campos')
        return
        
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    
    combo_categoria_despesas.delete(0, 'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')
    
    

#Função para deletar dados da tabela informa mensagem de sucesso e de erro 
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dados_item = tree.item(treev_dados)
        treev_lista = treev_dados_item['values']
        valor = treev_lista[0]
        nome = treev_lista[1]
        
        if nome == 'Receita':
            excluir_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluidos com sucesso')
            
            #Atualizando a tabela
            percentagem()
            grafico_barra()
            resumo_total()
            grafico_pizza()
        else:
            excluir_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluidos com sucesso')
            
            #Atualizando a tabela
            percentagem()
            grafico_barra()
            resumo_total()
            grafico_pizza()
            
    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')

    
# Percentagem da barra de progresso
# Função para exibir a percentagem
def percentagem():
    l_nome = Label(frameMeio, text="Porcentagem da receita gasta", height=1,anchor=NW, font=('Verdana 12 '), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)


    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMeio, length=180,style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = percentagem_valor()[0]

    valor = percentagem_valor()[0]
    print(valor)
    l_percentagem = Label(frameMeio, text='{:,.2f} %'.format(valor), height=1,anchor=NW, font=('Verdana 12 '), bg=co1, fg=co4)
    l_percentagem.place(x=200, y=35)
    
# Função para grafico de barras
def grafico_barra():
    # Lista de categorias para o gráfico de barras
    lista_categorias = ['Renda', 'Despesas', 'Saldo']

    # Lista de valores correspondentes às categorias
    lista_valores = bar_valores()

    # Cria uma figura para o gráfico com tamanho e DPI especificados
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)

    # Adiciona um objeto de eixo à figura para desenhar o gráfico
    ax = figura.add_subplot(111)

    # Cria um gráfico de barras com as categorias e valores, definindo a cor e a largura das barras
    ax.bar(lista_categorias, lista_valores, color=['#1f77b4', '#ff7f0e', '#2ca02c'], width=0.9)

    # Inicializa um contador para percorrer os valores e adicionar texto às barras
    c = 0

    # Loop através de cada barra no gráfico
    for i in ax.patches:
        # Adiciona texto acima de cada barra, formatando o valor e ajustando a posição e estilo do texto
        ax.text(i.get_x() - .001, i.get_height() + .5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic', verticalalignment='bottom', color='dimgrey')
        c += 1

    # Define os rótulos do eixo x com o tamanho da fonte especificado
    ax.set_xticklabels(lista_categorias, fontsize=16)

    # Define a cor de fundo do gráfico
    ax.patch.set_facecolor('#ffffff')

    # Configura as cores e larguras das bordas do gráfico
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    # Torna as bordas superior, direita e esquerda invisíveis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove as marcações dos eixos x e y
    ax.tick_params(bottom=False, left=False)

    # Coloca o grid do eixo y abaixo das barras
    ax.set_axisbelow(True)

    # Remove a grade do eixo y e define a cor da grade
    ax.yaxis.grid(False, color='#EEEEEE')

    # Remove a grade do eixo x
    ax.xaxis.grid(False)

    # Cria um widget de canvas para a figura no Tkinter e posiciona no frame
    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)
        


# Função de resumo total
def resumo_total():
    
    # Resumo total da renda
    valor = bar_valores()
    
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal     ".upper(), anchor=NW, font=("Verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format((valor[0])), anchor=NW, font=("Arial 17"), bg=co1, fg="#545454")
    l_sumario.place(x=309, y=70)
    
    # Resumo total das despesas
 
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=("Arial 1"), bg="#545454")
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais  ".upper(), anchor=NW, font=("Verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format((valor[1])), anchor=NW, font=("Arial 17"), bg=co1, fg="#545454")
    l_sumario.place(x=309, y=150)
    
    # Resumo total do saldo
    
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=("Arial 1"), bg="#545454") 
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text="Total Saldo da Caixa   ".upper(), anchor=NW, font=("Verdana 12"), bg=co1, fg="#83a9e6")
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format((valor[2])), anchor=NW, font=("Arial 17"), bg=co1, fg="#545454")
    l_sumario.place(x=309, y=220)


# Função grafico de pizza
def grafico_pizza():
    # Crie uma faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pizza)
    canva_categoria.get_tk_widget().grid(row=0, column=0)


    
percentagem()
grafico_barra()
resumo_total()
grafico_pizza()

# Criando frames dentro do FrameBaixo
frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2, padx=5)

# Tabela Renda Mensal
app_tabela = Label(frameMeio, text="Tabela Receitas e Despesas",anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)

# Função para mostrar renda
def mostrar_renda():
    tabela_head = ['#Id', 'Categoria', 'Data', 'Quantia']
    lista_itens = tabela() # Combine receitas e gastos se desejar

    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings")
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd = ["center", "center", "center", "center"]
    h = [30, 100, 100, 100]

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[tabela_head.index(col)], anchor=hd[tabela_head.index(col)])

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_renda()


# Configuracoes Despesas -----------------------------------
l_descricao = Label(frame_operacoes, text="Insira novas despesas", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_descricao.place(x=10, y=10)

l_descricao = Label(frame_operacoes, text="Categoria", height=1,anchor=NW,relief="flat", font=('Ivy 10'), bg=co1, fg=co4)
l_descricao.place(x=10, y=40)

# Pegando os categorias
categorias_funcao = consultar_categoria()
categorias = []

for i in categorias_funcao:
    categorias.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10,font=('Ivy 10'))
combo_categoria_despesas['values'] = (categorias)
combo_categoria_despesas.place(x=110, y=41)

l_cal_despeas = Label(frame_operacoes, text="Data", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_cal_despeas.place(x=10, y=70)

e_cal_despesas = DateEntry(frame_operacoes, width=12, background='darkblue',  foreground='white', borderwidth=2, year=2020, date_pattern='dd/MM/yyyy')
e_cal_despesas.place(x=110, y=71)

l_valor_despesas = Label(frame_operacoes, text="Quantia Total", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left',relief="solid")
e_valor_despesas.place(x=110, y=101)

# Botao Inserir despesas
img_add_despesas  = Image.open('icons/add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)

botao_inserir_despesas = Button(frame_operacoes,image=img_add_despesas, compound=LEFT, anchor=NW, text=" Adicionar".upper(), 
                                width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0, command=inserir_despesas_b)
botao_inserir_despesas.place(x=110, y=131)

# operacao Excluir -----------------------
l_n_categoria = Label(frame_operacoes, text="Excluir ação", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_n_categoria.place(x=10, y=190)


# Botao Deletar
img_delete  = Image.open('icons/deletar.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, image=img_delete, compound=LEFT, anchor=NW, text="   Deletar".upper(), width=80, 
                       overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0, command=deletar_dados)
botao_deletar.place(x=110, y=190)

# Configuracoes Receitas -----------------------------------

l_descricao = Label(frame_configuracao, text="Insira novas receitas", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_descricao.place(x=10, y=10)

l_cal_receitas = Label(frame_configuracao, text="Data", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background='darkblue',  foreground='white', borderwidth=2, year=2020, date_pattern='dd/MM/yyyy')
e_cal_receitas.place(x=110, y=41)

l_valor_receitas = Label(frame_configuracao, text="Quantia Total", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left',relief="solid")
e_valor_receitas.place(x=110, y=71)

# Botao Inserir
img_add_receitas  = Image.open('icons/add.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao, image=img_add_receitas, compound=LEFT, anchor=NW, text=" Adicionar".upper(), 
                                width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0, command=inserir_receita_b)
botao_inserir_receitas.place(x=110, y=111)


# operacao Nova Categoria -----------------------

l_n_categoria = Label(frame_configuracao, text="Nova categoria", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_n_categoria.place(x=10, y=160)
e_n_categoria = Entry(frame_configuracao, width=14, justify='left',relief="solid")
e_n_categoria.place(x=110, y=160)

# Botao Inserir
img_add_categoria  = Image.open('icons/add.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_configuracao,image=img_add_categoria, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, 
                                 overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0, command= inserir_categoria_b)
botao_inserir_categoria.place(x=110, y=190)


tela.mainloop() # Abrir a tela