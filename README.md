# Trabalho DC - Análise de Dados da Steam  

Esta base de dados é referente à plataforma **Steam**, uma das maiores lojas digitais de jogos para PC.  
Ela contém informações detalhadas sobre os jogos disponíveis, incluindo título, data de lançamento, gênero, desenvolvedor, preço, avaliações, suporte a sistemas operacionais e muito mais.  

> Base de dados: [Steam Store Data (Kaggle)](https://www.kaggle.com/datasets/amanbarthwal/steam-store-data/data)

## Objetivos da Análise

O projeto busca explorar o mercado de jogos da Steam por meio de perguntas que possam revelar padrões, tendências e relações entre preço, popularidade e qualidade dos jogos.


## Principais Análises Realizadas:

### Visçao Geral
- Top 5 jogos mais populares pela quantidade de avaliações.
- Gêneros mais comuns na Steam.
- Publishers com mais jogos publicados.
- Categorias mais populares (ex: "Multiplayer", "Single Player").

### Avaliações e Descontos
- Correlação entre descontos e avaliações gerais (comentado - no código, pode ser ativado futuramente).
- Evolução dos descontos médios por ano de lançamento:
    - De 1997 a 2005, não havia descontos registrados.
    - A partir de 2006, os descontos médios variam entre 3% e 8%.
    - Lançamentos recentes não apresentam descontos significativamente maiores que os mais antigos

### Tendências

- Gêneros em crescimento ou declínio nos últimos lançamentos (últimos 3 anos analisados), com gráfico de evolução por ano.
- Desenvolvedores com mais jogos publicados e média de avaliação de seus jogos.

### Filtros Interativos

- Selecionar jogos específicos.
- Filtrar por faixa de preço.
- Filtrar por avaliação mínima (%).
- Filtrar por gênero.
- Filtrar por conteúdo (idade, descriptors).
- Filtrar por ano de lançamento.

## Como Executar o Projeto

- Instalar as dependências:
    ```bash
    poetry install
    ```
- Iniciar o servidor Streamlit
    ```bash
    poetry run streamlit run src/app.py
    ```

O servidor estará disponível em [http://localhost:8501/](http://localhost:8501/)
