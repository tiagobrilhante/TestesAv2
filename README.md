# Trabalho de Teste de Software - AV2

## Aluno
- Tiago da Silva Brilhante
- Matrícula: 03342706
- Curso/Período: Ciência da Computação / 7º Período – Noturno

## Descrição
Este projeto contém testes automatizados para um banco de dados SQLite, abordando diversos aspectos de operações em banco de dados:
- Testes de CRUD (Create, Read, Update, Delete)
- Testes de VIEW
- Testes de TRIGGER
- Testes de JOIN
- Testes de Integridade Referencial
- Testes de Performance
- Testes de Transações e Rollback
- Testes de Segurança (SQL Injection)

## Conceitos e Referências

### Integridade Referencial
A integridade referencial é um conceito em bancos de dados que garante que as relações entre tabelas permaneçam consistentes. Quando uma coluna em uma tabela faz referência a uma coluna em outra tabela, a integridade referencial assegura que cada valor nessa coluna corresponda a um valor existente na tabela referenciada.

**Referência:** Date, C. J. (2003). An Introduction to Database Systems (8th ed.). Addison-Wesley. p. 328-336.

### View (Visão)
Uma view é uma tabela virtual baseada no resultado de uma consulta SQL. As views não armazenam dados fisicamente; elas mostram os dados armazenados em outras tabelas. As views são usadas para simplificar consultas complexas, controlar o acesso a dados e apresentar os dados de maneira personalizada.

**Referência:** Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson. p. 201-210.

### Trigger (Gatilho)
Um trigger é um procedimento armazenado que é automaticamente executado quando ocorre um evento específico em uma tabela do banco de dados. Os triggers são usados para manter a integridade dos dados, auditar alterações em tabelas e automatizar tarefas relacionadas ao banco de dados.

**Referência:** Coronel, C., & Morris, S. (2018). Database Systems: Design, Implementation, & Management (13th ed.). Cengage Learning. p. 412-425.

### Join (Junção)
Join é uma operação que combina colunas de uma ou mais tabelas com base em um campo relacionado entre elas. Existem diferentes tipos de joins: INNER JOIN, LEFT JOIN, RIGHT JOIN e FULL JOIN, cada um com comportamento específico para combinar registros.

**Referência:** Garcia-Molina, H., Ullman, J. D., & Widom, J. (2014). Database Systems: The Complete Book (2nd ed.). Pearson. p. 155-172.

### Teste de Performance
Teste de performance em bancos de dados avalia o desempenho e a escalabilidade do sistema sob diferentes condições e cargas. Ele verifica tempos de resposta, uso de recursos e identifica gargalos para otimização.

**Referência:** Shasha, D., & Bonnet, P. (2002). Database Tuning: Principles, Experiments, and Troubleshooting Techniques. Morgan Kaufmann. p. 45-60.

## Como Executar

1. Certifique-se de ter o Python, pytest e colorama instalados
   ```
   pip install pytest colorama
   ```
2. Execute o script de menu:
   ```
   python run_testes.py
   ```
3. Selecione o teste que deseja executar ou escolha a opção "M" para acessar o manual detalhado

## Recursos do Sistema
- **Interface Colorida**: Utiliza a biblioteca colorama para melhorar a visualização no console
- **Manual Detalhado**: Acesse explicações completas sobre cada teste e conceitos de banco de dados
- **Passos Didáticos**: Durante a execução dos testes, são exibidos os passos sendo executados
- **Menu Intuitivo**: Interface de usuário simples e fácil de navegar

## Estrutura do Projeto
- `run_testes.py`: Interface de menu para executar os testes
- `test_database.py`: Contém todos os testes implementados
- `identifier.sqlite`: Banco de dados SQLite utilizado nos testes
