import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tkinter import Tk, filedialog
from pathlib import Path
import webbrowser

# ============================================================
# CONFIGURAÇÕES
# ============================================================

COLUNAS_VENDAS = ["Produto", "Quantidade", "Data"]
COLUNAS_PRODUTOS = ["ID", "Nome", "Preço", "Gasto"]


# ============================================================
# SELEÇÃO DOS ARQUIVOS
# ============================================================

def selecionar_arquivo(titulo):
    root = Tk()
    root.withdraw()

    arquivo = filedialog.askopenfilename(
        title=titulo,
        filetypes=[
            ("Arquivos Excel", "*.xlsx *.xls"),
            ("Todos os arquivos", "*.*")
        ]
    )

    root.destroy()

    return arquivo


# ============================================================
# LEITURA DOS ARQUIVOS
# ============================================================

def carregar_dados():
    print("Selecione o arquivo de VENDAS.")

    arquivo_vendas = selecionar_arquivo(
        "Selecione o arquivo de vendas"
    )

    if not arquivo_vendas:
        raise Exception("Arquivo de vendas não selecionado.")

    print("Selecione o arquivo de PRODUTOS.")

    arquivo_produtos = selecionar_arquivo(
        "Selecione o arquivo de produtos"
    )

    if not arquivo_produtos:
        raise Exception("Arquivo de produtos não selecionado.")

    vendas = pd.read_excel(arquivo_vendas)
    produtos = pd.read_excel(arquivo_produtos)

    return vendas, produtos


# ============================================================
# VALIDAÇÃO
# ============================================================

def validar_colunas(df, colunas, nome):
    faltando = [
        coluna for coluna in colunas
        if coluna not in df.columns
    ]

    if faltando:
        raise ValueError(
            f"O arquivo de {nome} não possui as colunas: "
            f"{', '.join(faltando)}"
        )


def preparar_dados(vendas, produtos):

    validar_colunas(
        vendas,
        COLUNAS_VENDAS,
        "vendas"
    )

    validar_colunas(
        produtos,
        COLUNAS_PRODUTOS,
        "produtos"
    )

    # Cópias para evitar alterações indesejadas
    vendas = vendas.copy()
    produtos = produtos.copy()

    # Conversão da data
    vendas["Data"] = pd.to_datetime(
        vendas["Data"],
        dayfirst=True,
        errors="coerce"
    )

    # Conversão numérica
    vendas["Quantidade"] = pd.to_numeric(
        vendas["Quantidade"],
        errors="coerce"
    )

    produtos["Preço"] = pd.to_numeric(
        produtos["Preço"],
        errors="coerce"
    )

    produtos["Gasto"] = pd.to_numeric(
        produtos["Gasto"],
        errors="coerce"
    )

    # Remover registros inválidos
    vendas = vendas.dropna(
        subset=["Produto", "Quantidade", "Data"]
    )

    produtos = produtos.dropna(
        subset=["ID", "Preço", "Gasto"]
    )

    # Padronizar IDs
    vendas["Produto"] = vendas["Produto"].astype(str)
    produtos["ID"] = produtos["ID"].astype(str)

    return vendas, produtos


# ============================================================
# JUNÇÃO DOS DADOS
# ============================================================

def juntar_dados(vendas, produtos):

    dados = vendas.merge(
        produtos,
        left_on="Produto",
        right_on="ID",
        how="left"
    )

    # Verificar produtos que não foram encontrados
    produtos_nao_encontrados = dados[
        dados["Nome"].isna()
    ]

    if len(produtos_nao_encontrados) > 0:

        print("\nATENÇÃO:")
        print(
            f"{len(produtos_nao_encontrados)} "
            "vendas possuem produto sem cadastro."
        )

    # Cálculos
    dados["Faturamento"] = (
        dados["Quantidade"] *
        dados["Preço"]
    )

    dados["Custo"] = (
        dados["Quantidade"] *
        dados["Gasto"]
    )

    dados["Lucro"] = (
        dados["Faturamento"] -
        dados["Custo"]
    )

    dados["Margem"] = (
        dados["Lucro"] /
        dados["Faturamento"]
    ).fillna(0) * 100

    return dados


# ============================================================
# INDICADORES
# ============================================================

def calcular_indicadores(dados):

    faturamento = dados["Faturamento"].sum()

    custo = dados["Custo"].sum()

    lucro = dados["Lucro"].sum()

    quantidade = dados["Quantidade"].sum()

    numero_vendas = len(dados)

    ticket_medio = (
        faturamento / numero_vendas
        if numero_vendas > 0
        else 0
    )

    margem = (
        lucro / faturamento * 100
        if faturamento > 0
        else 0
    )

    return {
        "faturamento": faturamento,
        "custo": custo,
        "lucro": lucro,
        "quantidade": quantidade,
        "numero_vendas": numero_vendas,
        "ticket_medio": ticket_medio,
        "margem": margem
    }


# ============================================================
# ANÁLISES
# ============================================================

def analisar_produtos(dados):

    produtos = (
        dados
        .groupby(["Produto", "Nome"], dropna=False)
        .agg(
            Quantidade=("Quantidade", "sum"),
            Faturamento=("Faturamento", "sum"),
            Custo=("Custo", "sum"),
            Lucro=("Lucro", "sum")
        )
        .reset_index()
    )

    produtos["Margem"] = (
        produtos["Lucro"] /
        produtos["Faturamento"]
    ).fillna(0) * 100

    return produtos.sort_values(
        "Faturamento",
        ascending=False
    )


def analisar_vendas_por_dia(dados):

    diario = (
        dados
        .groupby("Data")
        .agg(
            Quantidade=("Quantidade", "sum"),
            Faturamento=("Faturamento", "sum"),
            Lucro=("Lucro", "sum")
        )
        .reset_index()
    )

    return diario.sort_values("Data")


def analisar_vendas_por_mes(dados):

    dados = dados.copy()

    dados["Mes"] = (
        dados["Data"]
        .dt.to_period("M")
        .astype(str)
    )

    mensal = (
        dados
        .groupby("Mes")
        .agg(
            Quantidade=("Quantidade", "sum"),
            Faturamento=("Faturamento", "sum"),
            Lucro=("Lucro", "sum")
        )
        .reset_index()
    )

    return mensal


# ============================================================
# FORMATAÇÃO
# ============================================================

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(
        ",", "X"
    ).replace(
        ".", ","
    ).replace(
        "X", "."
    )


# ============================================================
# DASHBOARD
# ============================================================

def criar_dashboard(dados):

    indicadores = calcular_indicadores(dados)

    produtos = analisar_produtos(dados)

    diario = analisar_vendas_por_dia(dados)

    mensal = analisar_vendas_por_mes(dados)

    # --------------------------------------------------------
    # GRÁFICO 1 - FATURAMENTO POR MÊS
    # --------------------------------------------------------

    grafico_mensal = px.line(
        mensal,
        x="Mes",
        y="Faturamento",
        markers=True,
        title="Faturamento por mês"
    )

    grafico_mensal.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento"
    )

    # --------------------------------------------------------
    # GRÁFICO 2 - LUCRO POR MÊS
    # --------------------------------------------------------

    grafico_lucro = px.line(
        mensal,
        x="Mes",
        y="Lucro",
        markers=True,
        title="Lucro por mês"
    )

    grafico_lucro.update_layout(
        xaxis_title="Mês",
        yaxis_title="Lucro"
    )

    # --------------------------------------------------------
    # GRÁFICO 3 - TOP 10 PRODUTOS
    # --------------------------------------------------------

    top_produtos = produtos.head(10)

    grafico_produtos = px.bar(
        top_produtos,
        x="Nome",
        y="Faturamento",
        title="Top 10 produtos por faturamento"
    )

    grafico_produtos.update_layout(
        xaxis_title="Produto",
        yaxis_title="Faturamento"
    )

    # --------------------------------------------------------
    # GRÁFICO 4 - QUANTIDADE VENDIDA
    # --------------------------------------------------------

    grafico_quantidade = px.bar(
        top_produtos,
        x="Nome",
        y="Quantidade",
        title="Top 10 produtos por quantidade vendida"
    )

    grafico_quantidade.update_layout(
        xaxis_title="Produto",
        yaxis_title="Quantidade"
    )

    # --------------------------------------------------------
    # GRÁFICO 5 - LUCRO POR PRODUTO
    # --------------------------------------------------------

    grafico_lucro_produto = px.bar(
        top_produtos,
        x="Nome",
        y="Lucro",
        title="Lucro dos principais produtos"
    )

    # --------------------------------------------------------
    # TABELA DE PRODUTOS
    # --------------------------------------------------------

    tabela = produtos.head(20).copy()

    tabela["Faturamento"] = tabela["Faturamento"].apply(moeda)

    tabela["Custo"] = tabela["Custo"].apply(moeda)

    tabela["Lucro"] = tabela["Lucro"].apply(moeda)

    tabela["Margem"] = (
        tabela["Margem"]
        .round(2)
        .astype(str) + "%"
    )

    tabela_html = tabela[
        [
            "Produto",
            "Nome",
            "Quantidade",
            "Faturamento",
            "Custo",
            "Lucro",
            "Margem"
        ]
    ].to_html(
        index=False,
        classes="tabela"
    )

    # --------------------------------------------------------
    # HTML DOS GRÁFICOS
    # --------------------------------------------------------

    html_mensal = grafico_mensal.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    html_lucro = grafico_lucro.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    html_produtos = grafico_produtos.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    html_quantidade = grafico_quantidade.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    html_lucro_produto = grafico_lucro_produto.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    # --------------------------------------------------------
    # HTML FINAL
    # --------------------------------------------------------

    html = f"""
<!DOCTYPE html>

<html lang="pt-BR">

<head>

<meta charset="UTF-8">

<title>Dashboard de Vendas</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 30px;
}}

h1 {{
    color: #222;
}}

.dashboard {{
    max-width: 1400px;
    margin: auto;
}}

.cards {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}}

.card h3 {{
    margin: 0;
    color: #777;
    font-size: 14px;
}}

.card p {{
    font-size: 26px;
    font-weight: bold;
    margin: 10px 0 0;
}}

.grafico {{
    background: white;
    margin-bottom: 25px;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}}

.tabela {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}

.tabela th,
.tabela td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

.tabela th {{
    background: #eee;
}}

</style>

</head>

<body>

<div class="dashboard">

<h1>Dashboard de Vendas</h1>

<div class="cards">

<div class="card">
<h3>Faturamento</h3>
<p>{moeda(indicadores["faturamento"])}</p>
</div>

<div class="card">
<h3>Custo</h3>
<p>{moeda(indicadores["custo"])}</p>
</div>

<div class="card">
<h3>Lucro</h3>
<p>{moeda(indicadores["lucro"])}</p>
</div>

<div class="card">
<h3>Margem</h3>
<p>{indicadores["margem"]:.2f}%</p>
</div>

<div class="card">
<h3>Produtos vendidos</h3>
<p>{indicadores["quantidade"]:,.0f}</p>
</div>

<div class="card">
<h3>Número de vendas</h3>
<p>{indicadores["numero_vendas"]:,}</p>
</div>

<div class="card">
<h3>Ticket médio</h3>
<p>{moeda(indicadores["ticket_medio"])}</p>
</div>

</div>

<div class="grafico">
{html_mensal}
</div>

<div class="grafico">
{html_lucro}
</div>

<div class="grafico">
{html_produtos}
</div>

<div class="grafico">
{html_quantidade}
</div>

<div class="grafico">
{html_lucro_produto}
</div>

<h2>Desempenho dos produtos</h2>

{tabela_html}

</div>

</body>

</html>
"""

    caminho = Path("dashboard.html")

    caminho.write_text(
        html,
        encoding="utf-8"
    )

    return caminho


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 50)
    print("       ANÁLISE DE VENDAS")
    print("=" * 50)

    try:

        vendas, produtos = carregar_dados()

        print("\nArquivos carregados.")

        vendas, produtos = preparar_dados(
            vendas,
            produtos
        )

        print(
            f"Vendas encontradas: {len(vendas)}"
        )

        print(
            f"Produtos cadastrados: {len(produtos)}"
        )

        dados = juntar_dados(
            vendas,
            produtos
        )

        indicadores = calcular_indicadores(
            dados
        )

        print("\n" + "=" * 50)
        print("RESULTADOS")
        print("=" * 50)

        print(
            f"Faturamento: "
            f"{moeda(indicadores['faturamento'])}"
        )

        print(
            f"Custo: "
            f"{moeda(indicadores['custo'])}"
        )

        print(
            f"Lucro: "
            f"{moeda(indicadores['lucro'])}"
        )

        print(
            f"Margem: "
            f"{indicadores['margem']:.2f}%"
        )

        print(
            f"Quantidade vendida: "
            f"{indicadores['quantidade']:.0f}"
        )

        print(
            f"Ticket médio: "
            f"{moeda(indicadores['ticket_medio'])}"
        )

        print("\nGerando dashboard...")

        dashboard = criar_dashboard(
            dados
        )

        print(
            f"\nDashboard criado: {dashboard.absolute()}"
        )

        print(
            "\nAbra o arquivo dashboard.html "
            "no navegador."
        )

        webbrowser.open_new_tab("dashboard.html")

    except Exception as erro:

        print("\nERRO:")
        print(erro)


if __name__ == "__main__":
    main()