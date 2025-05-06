import pytest
import sys
import os
from colorama import Fore, Back, Style, init

# Inicializar colorama
init(autoreset=True)

# Definir variável TERM se não estiver configurada
if "TERM" not in os.environ:
    os.environ["TERM"] = "xterm"  # Valor padrão simples

def clear_screen():
    """Limpa a tela do console sem depender da variável TERM."""
    # Método seguro que funciona em todos os ambientes
    print("\n" * 50)

def print_step(step_name, description=""):
    """Imprime um passo de execução formatado com cores."""
    print(f"{Fore.CYAN}[PASSO]{Style.RESET_ALL} {Fore.YELLOW}{step_name}{Style.RESET_ALL}")
    if description:
        print(f"  {Fore.WHITE}{description}{Style.RESET_ALL}")

def run_specific_test(test_name):
    """Executa um teste específico usando pytest."""
    print(f"\n{Fore.GREEN}Executando teste: {Fore.YELLOW}{test_name}{Style.RESET_ALL}\n")

    # Obter informações sobre o teste
    test_descriptions = {
        "test_update_user": "Teste de atualização de dados em uma tabela",
        "test_join_users_orders": "Teste de operação JOIN entre tabelas",
        "test_view_execution": "Teste de execução de uma VIEW",
        "test_trigger_execution": "Teste de execução de um TRIGGER",
        "test_foreign_key_constraint": "Teste de restrição de chave estrangeira",
        "test_index_performance": "Teste de performance com índices",
        "test_transaction_rollback": "Teste de transação e rollback",
        "test_parameterized_query": "Teste de consultas parametrizadas",
        "test_like_query": "Teste de consultas com operador LIKE",
        "test_cascade_delete": "Teste de deleção em cascata",
        "test_batch_insert_performance": "Teste de performance de inserção em lote"
    }

    if test_name in test_descriptions:
        print(f"{Fore.CYAN}Descrição: {Fore.WHITE}{test_descriptions[test_name]}{Style.RESET_ALL}\n")

    print_step("Preparando ambiente de teste", "Configurando banco de dados e dependências")
    print_step("Executando teste", f"Iniciando {test_name}")

    # Usar a flag -s para capturar a saída e suprimir mensagens de erro
    pytest.main(["-v", "-s", "-k", test_name])

    print_step("Teste concluído", "Verificando resultados")

    input(f"\n{Fore.GREEN}Pressione Enter para continuar...{Style.RESET_ALL}")

def run_basic_tests():
    """Executa os testes básicos (1-5) em sequência."""
    clear_screen()
    print(f"\n{Fore.GREEN}Executando testes básicos (1-5)...{Style.RESET_ALL}\n")

    print_step("Preparando ambiente de teste", "Configurando banco de dados e dependências")

    # Lista de testes básicos
    basic_tests = [
        "test_update_user",
        "test_join_users_orders",
        "test_view_execution",
        "test_trigger_execution",
        "test_foreign_key_constraint"
    ]

    # Descrições dos testes
    test_descriptions = {
        "test_update_user": "Teste de atualização de dados em uma tabela",
        "test_join_users_orders": "Teste de operação JOIN entre tabelas",
        "test_view_execution": "Teste de execução de uma VIEW",
        "test_trigger_execution": "Teste de execução de um TRIGGER",
        "test_foreign_key_constraint": "Teste de restrição de chave estrangeira"
    }

    # Mostrar descrições dos testes
    for test_name in basic_tests:
        print(f"\n{Fore.GREEN}Teste: {Fore.YELLOW}{test_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Descrição: {Fore.WHITE}{test_descriptions[test_name]}{Style.RESET_ALL}")

    print_step("Executando todos os testes básicos em uma única sessão", "Isso garante que o banco de dados seja limpo apenas uma vez no início")

    # Executar todos os testes básicos em uma única chamada do pytest
    # Construir a expressão para selecionar todos os testes básicos
    test_expression = " or ".join(basic_tests)
    pytest.main(["-v", "-s", "-k", test_expression])

    print_step("Testes básicos concluídos", "Verificando resultados")

    input(f"\n{Fore.GREEN}Pressione Enter para continuar...{Style.RESET_ALL}")

def show_manual():
    """Exibe o manual com explicações detalhadas sobre os testes."""
    clear_screen()
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'MANUAL DO SISTEMA DE TESTES DE BANCO DE DADOS':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}DESCRIÇÃO GERAL:{Style.RESET_ALL}")
    print("Este sistema executa testes automatizados para um banco de dados SQLite,")
    print("abordando diversos aspectos de operações em banco de dados.")

    print(f"\n{Fore.GREEN}TIPOS DE TESTES DISPONÍVEIS:{Style.RESET_ALL}")

    tests_info = [
        ("1. Testes Básicos",
         "Executa testes de Atualização, JOIN, View, Trigger e Integridade Referencial."),
        ("2. Testes de Performance de Índice",
         "Avalia o impacto dos índices na performance de consultas."),
        ("3. Testes de Transação e Rollback",
         "Testa a capacidade de reverter operações em caso de erro."),
        ("4. Testes de Consultas Parametrizadas",
         "Verifica a segurança contra SQL Injection usando consultas parametrizadas."),
        ("5. Testes de Consultas com LIKE",
         "Testa consultas usando o operador LIKE para busca de padrões."),
        ("6. Testes de Deleção em Cascata",
         "Verifica se a deleção em cascata funciona corretamente para manter a integridade."),
        ("7. Testes de Performance de Inserção em Lote",
         "Compara o desempenho entre inserções individuais e em lote.")
    ]

    for test, description in tests_info:
        print(f"{Fore.YELLOW}{test}{Style.RESET_ALL}")
        print(f"  {description}")

    print(f"\n{Fore.GREEN}CONCEITOS IMPORTANTES:{Style.RESET_ALL}")

    concepts = [
        ("Integridade Referencial",
         "Garante que relações entre tabelas permaneçam consistentes."),
        ("View (Visão)",
         "Tabela virtual baseada no resultado de uma consulta SQL."),
        ("Trigger (Gatilho)",
         "Procedimento executado automaticamente quando ocorre um evento específico."),
        ("Join (Junção)",
         "Operação que combina colunas de uma ou mais tabelas com base em campos relacionados."),
        ("Índice",
         "Estrutura que melhora a velocidade de recuperação de dados em uma tabela.")
    ]

    for concept, description in concepts:
        print(f"{Fore.YELLOW}{concept}{Style.RESET_ALL}")
        print(f"  {description}")

    print(f"\n{Fore.GREEN}COMO USAR O SISTEMA:{Style.RESET_ALL}")
    print("1. Selecione uma opção do menu principal digitando o número correspondente")
    print("2. Observe os passos de execução do teste que serão exibidos no console")
    print("3. Analise os resultados para entender o comportamento do banco de dados")

    input(f"\n{Fore.GREEN}Pressione Enter para voltar ao menu principal...{Style.RESET_ALL}")

def main_menu():
    """Exibe o menu principal de testes."""
    while True:
        clear_screen()
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'SISTEMA DE TESTES DE BANCO DE DADOS':^50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Escolha uma opção:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Testes Básicos (Atualização, JOIN, View, Trigger, Integridade Referencial)")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Testes de Performance de Índice")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Testes de Transação e Rollback")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Testes de Consultas Parametrizadas")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} Testes de Consultas com LIKE")
        print(f"{Fore.GREEN}6.{Style.RESET_ALL} Testes de Deleção em Cascata")
        print(f"{Fore.GREEN}7.{Style.RESET_ALL} Testes de Performance de Inserção em Lote")
        print(f"{Fore.YELLOW}M.{Style.RESET_ALL} Manual e Explicações Detalhadas")
        print(f"{Fore.BLUE}0.{Style.RESET_ALL} Executar todos os testes")
        print(f"{Fore.RED}Q.{Style.RESET_ALL} Sair")

        opcao = input(f"\n{Fore.CYAN}Digite sua escolha: {Style.RESET_ALL}").strip().upper()

        if opcao == '1':
            run_basic_tests()
        elif opcao == '2':
            run_specific_test("test_index_performance")
        elif opcao == '3':
            run_specific_test("test_transaction_rollback")
        elif opcao == '4':
            run_specific_test("test_parameterized_query")
        elif opcao == '5':
            run_specific_test("test_like_query")
        elif opcao == '6':
            run_specific_test("test_cascade_delete")
        elif opcao == '7':
            run_specific_test("test_batch_insert_performance")
        elif opcao == 'M':
            show_manual()
        elif opcao == '0':
            clear_screen()
            print(f"\n{Fore.GREEN}Executando todos os testes...{Style.RESET_ALL}\n")
            print_step("Preparando ambiente de teste", "Configurando banco de dados e dependências")
            print_step("Executando todos os testes", "Isso pode levar algum tempo")
            pytest.main(["-v", "-s"])
            print_step("Testes concluídos", "Verificando resultados")
            input(f"\n{Fore.GREEN}Pressione Enter para continuar...{Style.RESET_ALL}")
        elif opcao == 'Q':
            print(f"\n{Fore.YELLOW}Encerrando o sistema de testes. Até logo!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.{Style.RESET_ALL}")
            input(f"\n{Fore.GREEN}Pressione Enter para continuar...{Style.RESET_ALL}")

if __name__ == "__main__":
    main_menu()
