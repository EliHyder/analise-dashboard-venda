# 📊 Análise de Dados de Vendas com Python

Projeto de análise de dados desenvolvido em Python para processar planilhas Excel de vendas e produtos, calcular indicadores comerciais e gerar um dashboard interativo com gráficos e informações sobre o desempenho das vendas.

## 🎯 Objetivo

Transformar dados de vendas em informações úteis para a análise de desempenho comercial, permitindo visualizar o faturamento, os custos, os lucros e os produtos com melhor desempenho.

## 🚀 Funcionalidades

- Leitura de arquivos Excel de vendas e produtos.
- Cruzamento de informações por meio do ID dos produtos.
- Cálculo automático de faturamento, custos e lucro.
- Cálculo da margem de lucro e do ticket médio.
- Análise da quantidade total de produtos vendidos.
- Análise do faturamento e do lucro ao longo do tempo.
- Identificação dos produtos com maior faturamento.
- Comparação da quantidade vendida por produto.
- Tabela detalhada com os indicadores de cada produto.
- Geração automática de um dashboard em HTML.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Pandas:** manipulação, limpeza e análise dos dados.
- **OpenPyXL:** leitura de arquivos Excel.
- **Plotly:** criação de gráficos interativos.
- **Tkinter:** seleção dos arquivos por meio de janelas.

## 📁 Estrutura do projeto

```text
analise-vendas/
├── main.py
├── requirements.txt
├── vendas_teste.xlsx
├── produtos_teste.xlsx
└── dashboard.html
```

O arquivo `dashboard.html` é gerado automaticamente após a execução do programa. Os arquivos Excel de teste são exemplos para validar o funcionamento da aplicação.

## 📋 Formato dos arquivos Excel

O programa utiliza dois arquivos de entrada.

### 1. Arquivo de vendas

| Produto | Quantidade | Data |
|---|---:|---|
| 1 | 5 | 01/09/2026 |
| 2 | 3 | 02/09/2026 |
| 1 | 2 | 03/09/2026 |

- `Produto`: identificador do produto vendido.
- `Quantidade`: quantidade vendida.
- `Data`: data da venda, no formato dia/mês/ano.

### 2. Arquivo de produtos

| ID | Nome | Preço | Gasto |
|---|---|---:|---:|
| 1 | Teclado | 250.00 | 150.00 |
| 2 | Mouse | 120.00 | 65.00 |

- `ID`: identificador único do produto.
- `Nome`: nome do produto.
- `Preço`: preço de venda por unidade.
- `Gasto`: custo por unidade do produto.

**Importante:** os identificadores do arquivo de vendas devem corresponder aos IDs cadastrados no arquivo de produtos. Os nomes das colunas devem ser mantidos conforme especificado.

## ⚙️ Instalação

### Pré-requisitos

- Python 3.10 ou superior.
- Pip, gerenciador de pacotes do Python.

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/analise-vendas.git
```

Entre na pasta do projeto:

```bash
cd analise-vendas
```

Substitua `SEU-USUARIO` pelo seu nome de usuário ou organização do GitHub.

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` ainda não existir, crie-o com o seguinte conteúdo:

```text
pandas
openpyxl
plotly
```

### 3. Execute o programa

```bash
python main.py
```

O programa abrirá janelas para selecionar o arquivo de vendas e o arquivo de produtos.

Após o processamento, será gerado o arquivo `dashboard.html`, que pode ser aberto em um navegador para visualizar os resultados.

## 📈 Indicadores e visualizações

O dashboard apresenta:

| Indicador | Descrição |
|---|---|
| Faturamento total | Soma do valor das vendas |
| Custo total | Soma dos custos dos produtos vendidos |
| Lucro total | Faturamento menos custos |
| Margem de lucro | Percentual do lucro em relação ao faturamento |
| Quantidade vendida | Total de unidades comercializadas |
| Número de vendas | Quantidade de registros de vendas válidos |
| Ticket médio | Faturamento dividido pelo número de registros válidos |

### Gráficos

- Faturamento mensal.
- Lucro mensal.
- Top 10 produtos por faturamento.
- Top 10 produtos por quantidade vendida.
- Lucro dos principais produtos.

Também é exibida uma tabela com o desempenho financeiro dos produtos.

## 🧮 Cálculos utilizados

**Faturamento:**

```python
faturamento = quantidade * preco
```

**Custo total:**

```python
custo = quantidade * gasto
```

**Lucro:**

```python
lucro = faturamento - custo
```

**Margem de lucro:**

```python
margem = (lucro / faturamento) * 100
```

## ⚠️ Observações

- O campo `Gasto` deve representar o custo unitário do produto para que os cálculos sejam realizados corretamente.
- O ticket médio deste projeto representa o faturamento médio por registro de venda, não necessariamente por pedido ou cliente.
- O programa desconsidera registros com campos essenciais inválidos.
- Produtos sem cadastro correspondente são sinalizados no terminal.
- Os gráficos do Plotly utilizam uma biblioteca JavaScript carregada por CDN; portanto, a visualização interativa pode exigir conexão com a internet.

## 🔮 Melhorias futuras

- Adicionar filtros por período e produto.
- Comparar o desempenho entre meses.
- Identificar produtos com maior e menor margem de lucro.
- Exportar relatórios em Excel e PDF.
- Criar uma interface com Streamlit.
- Implementar tratamento de erros e relatórios de qualidade dos dados mais detalhados.

## 👨‍💻 Autor

Desenvolvido como projeto de estudo e portfólio na área de Python, análise de dados e visualização de informações.

## 📄 Licença

Este projeto pode ser disponibilizado sob a licença MIT. Para isso, adicione um arquivo `LICENSE` contendo os termos dessa licença ao repositório.
