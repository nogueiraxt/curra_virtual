# Curral Virtual

## Descrição do Projeto

O Curral Virtual é um sistema web desenvolvido em Python com o framework Django que oferece uma solução de gerenciamento para a ordenha de vacas. O projeto tem como objetivo principal o registro e a análise da produção de leite, permitindo um controle eficiente e detalhado para o produtor.

Este projeto é um excelente exemplo de desenvolvimento full-stack, demonstrando habilidades em modelagem de banco de dados, lógica de negócio, criação de interfaces web e interface de usuário.

## Funcionalidades

- **Gestão de Vacas:** Cadastro e listagem de vacas com informações detalhadas (nome, data de nascimento, filiação).
- **Controle de Ordenha:** Interface de formulário para lançamentos de ordenha, com campos para data, hora e quantidade de leite.
- **Cálculo de Produtividade:** Cálculo automático e dinâmico da média de produção diária por vaca.
- **Sistema de Relatórios:** Página de relatórios unificada com filtros por data e por vaca. O relatório exibe a produção total e a média diária no período selecionado.
- **Autenticação de Usuário:** Sistema de login e logout robusto para garantir que apenas usuários autorizados possam acessar e gerenciar os dados.
- **Operações CRUD:** Interface completa para **criar**, **visualizar**, **editar** e **excluir** lançamentos de ordenha.
- **Design Simples e Funcional:** A interface do usuário é clara e direta, focada na usabilidade.

## Tecnologias Utilizadas

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
</p>

## Instalação e Configuração

Siga os passos abaixo para configurar o projeto na sua máquina local.

### 1. Pré-requisitos

Certifique-se de ter instalado:
* Python 3.11 ou superior
* MySQL Server 8.0 ou superior
* XAMPP (para gerenciar o MySQL facilmente, se desejar)

### 2. Configuração do Banco de Dados

1.  Crie um banco de dados chamado `curral_virtual` no seu servidor MySQL (pode ser via MySQL Workbench ou phpMyAdmin).
2.  Atualize o arquivo `curral_virtual/settings.py` com as credenciais do seu banco de dados.

### 3. Instalação do Projeto

1.  Clone este repositório para o seu computador:
    ```bash
    git clone [https://github.com/nogueiraxt/curral-virtual.git](https://github.com/nogueiraxt/curral-virtual.git)
    cd curral-virtual
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    source venv/bin/activate  # No macOS/Linux
    ```
3.  Instale as dependências:
    ```bash
    pip install django mysqlclient
    ```

### 4. Execução do Servidor

1.  Aplique as migrações para criar as tabelas no seu banco de dados:
    ```bash
    python manage.py makemigrations curral
    python manage.py migrate
    ```
2.  Crie um superusuário para acessar o painel administrativo:
    ```bash
    python manage.py createsuperuser
    ```
3.  Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```
4.  Abra o navegador e acesse `http://127.0.0.1:8000/` para visualizar a aplicação.

## Melhorias Futuras

-   Adicionar gráficos para visualização da produção de leite.
-   Tornar a interface responsiva para dispositivos móveis.

## Autor

**Nogueira Pinheiro**
* [GitHub](https://github.com/nogueiraxt)
* [LinkedIn](https://www.linkedin.com/in/nogueira-pinheiro)
