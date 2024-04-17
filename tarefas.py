import flet as ft
import sqlite3 

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE # Define cor de fundo (Branca)
        self.page.window_width = 350 # Define a largura da Aplicação
        self.page.window_height = 450 #Define a altura da Aplicação
        self.page.window_resizable = False # impede Redimencionamento de Tela
        self.page.window_always_on_top = True # Mantem a Janela do App sempre por cima das outras
        self.page.title = 'Lista de Tarefas' # Define o Título da Aplicação
        self.task = ''
        self.view = 'all'
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(nome, status)') #cria uma tabela chamada TASK no Banco de Dados com as colunas informadas entre parenteses
        self.results = self.db_execute('SELECT * FROM tasks') # seleciona todas as tarefas no Banco de Dados.
        self.main_page() # chama uma função inicial


    def db_execute(self, query, params=[]):
        with sqlite3.connect('database.db') as conn: # Cria uma conexão com o Banco de Dados.
            cur = conn.cursor() #Cria o Cursor na conexão
            cur.execute(query, params)  #Insere as informações no Banco de Dados através do Cursor.
            conn.commit()  #Salva as informaçõe no Banco de Dados.
            return cur.fetchall() #Retorna todas as linhas solicitadas no Banco de Dados.


    def checked(self, e): # Função para checagem das tarefas selecionadas e adiciona no Banco de Dados
        is_checked = e.control.value # Armazena o valor do evento
        label = e.control.label #Armazena a Label do evento( o nome de onde foi marcado)

        if is_checked: # Se houver mudança
            self.db_execute('UPDATE tasks SET status = "complete" WHERE nome = ?', params=[label]) #Atualiza a tabela TASK na coluna STATUS para complete de acordo com o nome (Label)
        else:
            self.db_execute('UPDATE tasks SET status = "incomplete" WHERE nome = ?', params=[label]) #Atualiza a tabela TASK na coluna STATUS para incomplete de acordo com o nome (Label)
        
        if self.view == 'all': #Checa a ABA de vizualização.
            self.results = self.db_execute('SELECT * FROM tasks') #Adiciona todos os dados na variável atual
        else:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = ?', params=[self.view]) # Adiciona os dados a variável de acordo com o a variavel View (Aba atual)

        self.update_task_list() # Função para atualizar lista de tarefas



    def tasks_container(self): #Função cria container para alocaçãodos elementos principais do App
        return ft.Container(
            height=self.page.height * 0.8, # Mantem o Container em 80% do tamanho da página
            content= ft.Column(
                controls=[
                    ft.Checkbox(label = res[0], on_change = self.checked, value = True if res[1] == 'complete' else False) # Adiciona no Container os nomes e o Status de cada tarefa que estiver no Banco de dados
                    for res in self.results if res  # Itera para realizar a adição das tarefas no container se RES for verdadeiro - Não intendi muito, mas...
                ],
            )
        )
    
    
    def set_value(self, e): #Função pega o valor da caixa de entrada de tarefa (Text_field)
        self.task = e.control.value  # salva o valorcontido no Input_Task.
    
    def add(self, e, input_task):  # Função para adicionar tarefas.
        name = self.task  #salva o valor do INPUT_TASK na variável nome.
        status = 'incomplete' #Status inicial da tarefa.

        if name: #Se não estiver vazia
            self.db_execute(query='INSERT INTO tasks VALUES (?,?)', params=[name, status]) # insere a tarefa no Banco de dados
            input_task.value = ''  # Limpa a caixa de Tarefas
            self.results = self.db_execute('SELECT * FROM tasks') #Adiciona todas as Tarefas na variável 'result'
            self.update_task_list() # Chama a Função para Atualizar a Lista de Tarefas.

    def update_task_list(self): #Atualiza a Lista de Tarefas
        tasks = self.tasks_container() #Referencia o Container a uma Variável
        self.page.controls.pop() # Atualiza a pagina (Tela do App)
        self.page.add(tasks) # Adiciona as tarefas na tela do App
        self.page.update() # Atualiza a o App para que as alterações apareção no  App


    def tabs_changed(self, e):  #Função para distribuir tarefas as suas respectivas ABAS
        if e.control.selected_index == 0: # Caso a primeira ABA (Todos) estiver selecionada
            self.results = self.db_execute('SELECT * FROM tasks') #Solicita todoas as tarefas no Banco de Dados.
            self.view = 'all' # Muda a variável View para Todos
        elif e.control.selected_index == 1: # Caso a segunda ABA (Em Andamentos) estiver selecionada
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"') #Solicita todoas as tarefas Incompletas no Banco de Dados.
            self.view = 'incomplete'  # Muda a variável View para incompleto
        elif e.control.selected_index == 2:  #Caso a Terceira ABA (Finalizados) estiver selecionada
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "complete"') #Solicita todoas as tarefas Completas no Banco de Dados.
            self.view = 'complete'  # Muda a variável View paracompleto
        self.update_task_list()  # Atualiza a o App para que as alterações apareção no  App

    
    def main_page(self): # Funçãoque cria os elementos da pagina principal do App
        input_task = ft.TextField(hint_text= 'Digite uma tarefa', expand=True, on_change=self.set_value) # Entrada de texto com uma frase definida (digite uma tarefa)enquanto o ON_CHANGE pega o valor digitado no input_task
        input_bar = ft.Row(
            controls=[ #Defene os controles que estaram na linha.
                input_task, # insere o campo de texto definido anteriomente na linha 'input_bar'
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,   #Adiciona um Botão Flutoante com um Ícone de +
                    on_click=lambda e: self.add(e, input_task) # Função para passar o Evento e o valor contido na caixa de texto Tarefa (Input-task) para a Função add
                )
                

            ]
        )
        # Cria Tabs (Notebook no Tkinter)
        tabs = ft.Tabs(
            selected_index=0, #indica a selecionada por Defoult
            on_change=self.tabs_changed, # Verifica evetos nas ABAS
            tabs=[
                ft.Tab(text='Todos'), #Inserir testo na Borda
                ft.Tab(text='Em andamento'),
                ft.Tab(text='Finalizados')
            ]
        )

        tasks = self.tasks_container() # Atribui o Container a variável tasks

        self.page.add(input_bar, tabs,tasks) # insere os elementos na pagina.

ft.app(target=ToDo) # Inicia o APP

