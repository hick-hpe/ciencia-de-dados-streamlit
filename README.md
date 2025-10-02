# Ciência de Dados + Streamlit
Um projeto para apresentações de trabalhos em ciência de dados

## Iniciar projeto:
Para inciar o projeto, execute:
```bash
poetry new --name projeto .
```

## Instalar biblioteca
```bash
poetry add <biblioteca>
```

## Executar projeto existente

### Instalar bibliotecas existentes
Para instalar as bibliotecas, execute:
```bash
poetry install
```

## Executar servidor
Há duas manieras:
1. Abra através do `poetry`:
    ```bash
    poetry run streamlit run projeto/app.py
    ```

2. Ou Através do shell do `poetry`:
    ```bash
    poetry shell
    streamlit run projeto/app.py
    ```

    Para sair do shell:
    ```bash
    deactivate
    ```

