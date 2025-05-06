import pytest
import sqlite3
import time
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

def print_action(action, details=""):
    """Imprime uma ação de teste formatada com cores."""
    print(f"{Fore.BLUE}[AÇÃO]{Style.RESET_ALL} {Fore.GREEN}{action}{Style.RESET_ALL}")
    if details:
        print(f"  {Fore.WHITE}{details}{Style.RESET_ALL}")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Fixture que executa uma vez por sessão de teste.
    Exclui tabelas existentes e cria todas as tabelas necessárias para os testes.
    """
    connection = sqlite3.connect("../identifier.sqlite")
    cursor = connection.cursor()

    # Excluir tabelas existentes se existirem
    tables_to_drop = ["users", "orders", "logs", "test", "children", "parents", "performance_test"]
    views_to_drop = ["user_orders"]
    triggers_to_drop = ["order_insert"]

    # Excluir triggers
    for trigger in triggers_to_drop:
        cursor.execute(f"DROP TRIGGER IF EXISTS {trigger}")

    # Excluir views
    for view in views_to_drop:
        cursor.execute(f"DROP VIEW IF EXISTS {view}")

    # Excluir tabelas
    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Criar todas as tabelas necessárias para os testes
    # Tabelas principais
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT, FOREIGN KEY (user_id) REFERENCES users(id))")
    cursor.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, action TEXT)")

    # Tabela para teste de índice
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE INDEX idx_name ON test(name)")

    # Cria tabelas com CASCADE
    cursor.execute("CREATE TABLE parents (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE children (id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, FOREIGN KEY (parent_id) REFERENCES parents(id) ON DELETE CASCADE)")

    # Cria tabela para teste de peformance
    cursor.execute("CREATE TABLE performance_test (id INTEGER PRIMARY KEY, value TEXT)")

    # Criar view
    cursor.execute("CREATE VIEW user_orders AS SELECT users.name, orders.item FROM users INNER JOIN orders ON users.id = orders.user_id")

    # Criar trigger
    cursor.execute("CREATE TRIGGER order_insert AFTER INSERT ON orders BEGIN INSERT INTO logs (action) VALUES ('Novo pedido registrado'); END;")

    connection.commit()
    cursor.close()
    connection.close()

@pytest.fixture
def db_connection():
    """Cria e fecha conexão com banco de dados."""
    connection = sqlite3.connect("../identifier.sqlite")

    # Habilitar suporte a chaves estrangeiras
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()

    yield connection
    connection.close()

# 📌 Teste de Atualização
def test_update_user(db_connection):
    print_action("Iniciando teste de atualização de usuário")
    cursor = db_connection.cursor()

    print_action("Inserindo usuário", "Nome: 'Alice'")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
    db_connection.commit()

    print_action("Atualizando usuário", "Alterando nome de 'Alice' para 'Alicia'")
    cursor.execute("UPDATE users SET name = 'Alicia' WHERE name = 'Alice'")
    db_connection.commit()

    print_action("Verificando resultado", "Buscando usuário com nome 'Alicia'")
    cursor.execute("SELECT name FROM users WHERE name = 'Alicia'")
    result = cursor.fetchone()
    cursor.close()

    print_action("Validando resultado", f"Resultado encontrado: {result}")
    assert result is not None, "O nome atualizado deveria existir no banco."
    assert result[0] == "Alicia", "O nome do usuário deveria ter sido atualizado."
    print_action("Teste concluído com sucesso", "✅")

# 📌 Teste de JOIN
def test_join_users_orders(db_connection):
    print_action("Iniciando teste de JOIN entre tabelas")
    cursor = db_connection.cursor()

    print_action("Inserindo usuário", "Nome: 'Bob'")
    cursor.execute("INSERT INTO users (name) VALUES ('Bob')")

    print_action("Inserindo pedido", "Usuário ID: 2, Item: 'Laptop'")
    cursor.execute("INSERT INTO orders (user_id, item) VALUES (2, 'Laptop')")
    db_connection.commit()

    print_action("Executando consulta JOIN", "Selecionando da view user_orders")
    cursor.execute("SELECT * FROM user_orders")
    result = cursor.fetchone()
    cursor.close()

    print_action("Validando resultado", f"Resultado encontrado: {result}")
    assert result is not None, "O JOIN deveria retornar pelo menos um resultado."
    assert result[0] == "Bob", "O nome do usuário deveria ser 'Bob'."
    assert result[1] == "Laptop", "O item comprado deveria ser 'Laptop'."
    print_action("Teste concluído com sucesso", "✅")

# 📌 Teste de View
def test_view_execution(db_connection):
    print_action("Iniciando teste de execução de VIEW")
    cursor = db_connection.cursor()

    print_action("Inserindo usuário", "Nome: 'Charlie'")
    # Inserir usuário e obter o ID gerado
    cursor.execute("INSERT INTO users (name) VALUES ('Charlie')")
    user_id = cursor.lastrowid
    print_action("ID do usuário gerado", f"user_id: {user_id}")

    print_action("Inserindo pedido", f"Usuário ID: {user_id}, Item: 'Smartphone'")
    # Usar Verifica se foi gerado o trigger da view
    cursor.execute("INSERT INTO orders (user_id, item) VALUES (?, 'Smartphone')", (user_id,))
    db_connection.commit()

    print_action("Consultando VIEW", "Selecionando da view user_orders onde name = 'Charlie'")
    cursor.execute("SELECT * FROM user_orders where name = 'Charlie'")
    result = cursor.fetchone()
    cursor.close()

    print_action("Validando resultado", f"Resultado encontrado: {result}")
    assert result is not None, "A view deveria conter pelo menos um registro."
    assert result[0] == "Charlie", "O nome do usuário deveria ser 'Charlie'."
    assert result[1] == "Smartphone", "O item comprado deveria ser 'Smartphone'."
    print_action("Teste concluído com sucesso", "✅")

# 📌 Teste de Trigger
def test_trigger_execution(db_connection):
    print_action("Iniciando teste de execução de TRIGGER")
    cursor = db_connection.cursor()

    print_action("Inserindo pedido", "Usuário ID: 1, Item: 'Teclado'")
    cursor.execute("INSERT INTO orders (user_id, item) VALUES (1, 'Teclado')")
    db_connection.commit()
    print_action("Trigger acionado", "Deve ter inserido um registro na tabela logs")

    print_action("Verificando logs", "Contando registros na tabela logs")
    cursor.execute("SELECT COUNT(*) FROM logs")
    count = cursor.fetchone()[0]
    print_action("Resultado da contagem", f"Total de logs: {count}")
    cursor.close()

    print_action("Validando resultado")
    assert count == 3, "O trigger deveria ter inserido um log automaticamente."
    print_action("Teste concluído com sucesso", "✅")


def test_foreign_key_constraint(db_connection):
    """Testa se a chave estrangeira impede inserções inválidas."""
    print_action("Iniciando teste de restrição de chave estrangeira")
    cursor = db_connection.cursor()

    print_action("Tentando inserir pedido com chave estrangeira inválida", "Usuário ID: 99 (não existe)")
    # Tentando inserir um pedido sem um usuário correspondente
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO orders (user_id, item) VALUES (99, 'Celular')")
        db_connection.commit()

    print_action("Erro de integridade capturado", "Restrição de chave estrangeira funcionou corretamente")
    cursor.close()
    print_action("Teste concluído com sucesso", "✅")

def test_index_performance(db_connection):
    """Testa se um índice melhora a busca de registros."""
    print_action("Iniciando teste de performance com índice")
    cursor = db_connection.cursor()

    print_action("Inserindo dados de teste", "Adicionando 1000 registros na tabela test")
    # Inserindo muitos dados para testar busca rápida
    for i in range(1, 1001):
        cursor.execute("INSERT INTO test (name) VALUES (?)", (f"User_{i}",))
        if i % 200 == 0:  # Mostrar progresso a cada 200 inserções
            print_action("Progresso", f"Inseridos {i} registros")
    db_connection.commit()
    print_action("Inserção concluída", "1000 registros inseridos com sucesso")

    print_action("Analisando plano de execução", "Verificando se a consulta utiliza o índice")
    # Testando se busca usa índice
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM test WHERE name = 'User_500'")
    result = cursor.fetchall()
    cursor.close()

    # Verifica se o plano de execução menciona o uso do índice
    plano_execucao = str(result)
    print_action("Plano de execução obtido", f"Resultado: {plano_execucao}")

    print_action("Validando uso do índice")
    assert "COVERING INDEX" in plano_execucao, "A busca deveria utilizar o índice."
    print_action("Teste concluído com sucesso", "✅")

#######################
#        PASSO 7      #
#######################

# 1. Teste de transação e rollback
def test_transaction_rollback(db_connection, setup_database):
    """Testa se transações podem ser revertidas corretamente."""
    print_action("Iniciando teste de transação e rollback")
    cursor = db_connection.cursor()

    print_action("Inserindo usuário", "Nome: 'Marcelo'")
    # Insere um usuário e confirma a transação
    cursor.execute("INSERT INTO users (name) VALUES ('Marcelo')")
    db_connection.commit()  # Confirma a primeira inserção
    print_action("Transação confirmada", "Primeira inserção concluída com sucesso")

    print_action("Iniciando nova transação", "Tentando inserir pedido com user_id inválido")
    # Inicia uma nova transação
    try:
        # Tenta inserir um pedido com user_id inválido (deve falhar)
        cursor.execute("INSERT INTO orders (user_id, item) VALUES (99, 'Monitor')")
        db_connection.commit()
        print_action("ERRO", "Esta operação deveria falhar, mas não falhou!")
    except sqlite3.IntegrityError:
        # Ocorre erro, faz rollback
        print_action("Erro de integridade detectado", "Executando rollback da transação")
        db_connection.rollback()
        print_action("Rollback concluído", "Transação revertida com sucesso")

    print_action("Verificando persistência", "Checando se o usuário 'Marcelo' ainda existe")
    # Verifica se o usuário Marcelo ainda existe (não foi afetado pelo rollback)
    cursor.execute("SELECT COUNT(*) FROM users WHERE name = 'Marcelo'")
    count = cursor.fetchone()[0]
    print_action("Resultado da contagem", f"Encontrados: {count}")
    cursor.close()

    print_action("Validando resultado")
    assert count == 1, "O usuário deveria existir mesmo após rollback da transação."
    print_action("Teste concluído com sucesso", "✅")

# 2. Teste de consulta parametrizada (prevenção de SQL Injection)
def test_parameterized_query(db_connection, setup_database):
    """Testa se consultas parametrizadas funcionam corretamente."""
    print_action("Iniciando teste de consultas parametrizadas (prevenção de SQL Injection)")
    cursor = db_connection.cursor()

    # Insere um usuário usando parâmetros (forma segura)
    nome_usuario = "Maria'; DROP TABLE users; --"
    print_action("Inserindo usuário com nome malicioso", f"Nome: '{nome_usuario}'")
    print_action("Usando consulta parametrizada", "INSERT INTO users (name) VALUES (?)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", (nome_usuario,))
    db_connection.commit()
    print_action("Inserção concluída", "Usuário inserido com parâmetros de forma segura")

    print_action("Verificando inserção", "Buscando usuário com nome malicioso")
    # Verifica se o usuário foi inserido corretamente
    cursor.execute("SELECT name FROM users WHERE name = ?", (nome_usuario,))
    result = cursor.fetchone()
    print_action("Resultado da busca", f"Encontrado: {result}")

    print_action("Verificando integridade", "Checando se a tabela users ainda existe")
    # Verifica se a tabela users ainda existe
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()[0]
    print_action("Resultado da verificação", f"Tabela existe: {table_exists == 1}")

    cursor.close()

    print_action("Validando resultados")
    assert result is not None, "O usuário com nome especial deveria existir."
    assert result[0] == nome_usuario, "O nome do usuário deveria ser exatamente como inserido."
    assert table_exists == 1, "A tabela users deveria continuar existindo após a inserção."
    print_action("Teste concluído com sucesso", "✅")

# 3. Teste de consulta com LIKE
def test_like_query(db_connection, setup_database):
    """Testa consultas usando operador LIKE."""
    print_action("Iniciando teste de consulta com operador LIKE")
    cursor = db_connection.cursor()

    print_action("Inserindo usuários de teste")
    # Insere vários usuários
    usuarios = ["João Silva", "Maria Silva", "José Souza", "Ana Santos"]
    for i, usuario in enumerate(usuarios):
        print_action(f"Inserindo usuário {i+1}/{len(usuarios)}", f"Nome: '{usuario}'")
        cursor.execute("INSERT INTO users (name) VALUES (?)", (usuario,))
    db_connection.commit()
    print_action("Inserção concluída", f"{len(usuarios)} usuários inseridos com sucesso")

    print_action("Executando consulta com LIKE", "Buscando usuários com sobrenome 'Silva'")
    # Consulta usuários com sobrenome 'Silva'
    cursor.execute("SELECT COUNT(*) FROM users WHERE name LIKE '%Silva'")
    count = cursor.fetchone()[0]
    print_action("Resultado da consulta", f"Encontrados: {count} usuários")
    cursor.close()

    print_action("Validando resultado")
    assert count == 2, "Deveriam existir 2 usuários com sobrenome Silva."
    print_action("Teste concluído com sucesso", "✅")

# 4. Teste de deleção em cascata
def test_cascade_delete(db_connection):
    """Testa deleção em cascata com ON DELETE CASCADE."""
    print_action("Iniciando teste de deleção em cascata")
    cursor = db_connection.cursor()

    print_action("Inserindo dados de teste", "Criando estrutura de pais e filhos")
    # Insere dados
    print_action("Inserindo pais")
    cursor.execute("INSERT INTO parents (name) VALUES ('Pai1')")
    cursor.execute("INSERT INTO parents (name) VALUES ('Pai2')")

    print_action("Inserindo filhos", "Associando filhos aos pais")
    cursor.execute("INSERT INTO children (parent_id, name) VALUES (1, 'Filho1')")
    cursor.execute("INSERT INTO children (parent_id, name) VALUES (1, 'Filho2')")
    cursor.execute("INSERT INTO children (parent_id, name) VALUES (2, 'Filho3')")
    cursor.execute("INSERT INTO children (parent_id, name) VALUES (2, 'Filho4')")
    db_connection.commit()
    print_action("Dados inseridos com sucesso", "2 pais e 4 filhos")

    print_action("Executando deleção em cascata", "Deletando Pai1 (id=1)")
    # Deleta o pai
    cursor.execute("DELETE FROM parents WHERE id = 1")
    db_connection.commit()
    print_action("Deleção concluída", "Pai1 foi removido")

    print_action("Verificando efeito cascata", "Contando filhos do Pai1 que deveriam ter sido removidos")
    # Verifica se os filhos foram deletados
    cursor.execute("SELECT COUNT(*) FROM children WHERE parent_id = 1")
    count = cursor.fetchone()[0]
    print_action("Resultado da contagem", f"Filhos restantes: {count}")
    cursor.close()

    print_action("Validando resultado")
    assert count == 0, "Todos os filhos deveriam ter sido deletados em cascata."
    print_action("Teste concluído com sucesso", "✅")

# 5. Teste de desempenho para operações em lote
def test_batch_insert_performance(db_connection):
    """Testa o desempenho de inserções em lote vs individuais."""
    print_action("Iniciando teste de performance de inserção em lote")
    cursor = db_connection.cursor()

    print_action("Medindo tempo para inserções individuais", "Inserindo 100 registros um a um")
    # Mede tempo para inserções individuais
    start_time = time.time()
    for i in range(100):
        cursor.execute("INSERT INTO performance_test (value) VALUES (?)", (f"Value {i}",))
        db_connection.commit()
        if i % 25 == 0 and i > 0:  # Mostrar progresso a cada 25 inserções
            print_action("Progresso", f"Inseridos {i}/100 registros individualmente")
    individual_time = time.time() - start_time
    print_action("Inserções individuais concluídas", f"Tempo total: {individual_time:.4f} segundos")

    print_action("Limpando tabela para próximo teste")
    # Limpa tabela
    cursor.execute("DELETE FROM performance_test")
    db_connection.commit()

    print_action("Medindo tempo para inserção em lote", "Inserindo 100 registros em uma única operação")
    # Mede tempo para inserção em lote
    start_time = time.time()
    values = [(f"Value {i}",) for i in range(100)]
    cursor.executemany("INSERT INTO performance_test (value) VALUES (?)", values)
    db_connection.commit()
    batch_time = time.time() - start_time
    print_action("Inserção em lote concluída", f"Tempo total: {batch_time:.4f} segundos")

    cursor.close()

    print_action("Comparando resultados", f"Individual: {individual_time:.4f}s vs Lote: {batch_time:.4f}s")
    # Verifica se a inserção em lote é mais rápida
    assert batch_time < individual_time, "Inserção em lote deveria ser mais rápida que inserções individuais."
    print_action("Teste concluído com sucesso", "✅ Inserção em lote é mais rápida")

"""
#################################################
##       Passo 8: Conceitos e Referências      ##
#################################################

###  Integridade Referencial  ####
A integridade referencial é um conceito em bancos de dados que garante que as relações entre tabelas permaneçam 
consistentes. 
Quando uma coluna em uma tabela faz referência a uma coluna em outra tabela, a integridade referencial assegura 
que cada valor nessa coluna corresponda a um valor existente na tabela referenciada.

Referência:
Date, C. J. (2003). An Introduction to Database Systems (8th ed.). Addison-Wesley. p. 328-336.

###  View (Visão)  ###
Uma view é uma tabela virtual baseada no resultado de uma consulta SQL. As views não armazenam dados fisicamente; 
elas mostram os dados armazenados em outras tabelas. As views são usadas para simplificar consultas complexas, 
controlar o acesso a dados e apresentar os dados de maneira personalizada.

Referência:
Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson. p. 201-210.

###  Trigger (Gatilho)  ###
Um trigger é um procedimento armazenado que é automaticamente executado quando ocorre um evento específico em 
uma tabela do banco de dados. Os triggers são usados para manter a integridade dos dados, auditar alterações 
em tabelas e automatizar tarefas relacionadas ao banco de dados.

Referência:
Coronel, C., & Morris, S. (2018). Database Systems: Design, Implementation, & Management (13th ed.). Cengage Learning. p. 412-425.

###  Join (Junção)  ###
Join é uma operação que combina colunas de uma ou mais tabelas com base em um campo relacionado entre elas. 
Existem diferentes tipos de joins: INNER JOIN, LEFT JOIN, RIGHT JOIN e FULL JOIN, cada um com comportamento 
específico para combinar registros.

Referência:
Garcia-Molina, H., Ullman, J. D., & Widom, J. (2014). Database Systems: The Complete Book (2nd ed.). Pearson. p. 155-172.

###  Teste de Performance  ###
Teste de performance em bancos de dados avalia o desempenho e a escalabilidade do sistema sob diferentes condições e 
cargas. Ele verifica tempos de resposta, uso de recursos e identifica gargalos para otimização.

Referência:
Shasha, D., & Bonnet, P. (2002). Database Tuning: Principles, Experiments, and Troubleshooting Techniques. Morgan Kaufmann. p. 45-60.
"""
