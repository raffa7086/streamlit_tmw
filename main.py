import streamlit as st
import pandas as pd

def calcular_metricas(df: pd.DataFrame):
    df_data = df.groupby(by='Data')[["Valor"]].sum()
    df_data["Desloc"] = df_data["Valor"].shift(1)
    df_data["Diferença"] = df_data["Valor"] - df_data["Desloc"]
    df_data["Avg 6M"] = df_data["Diferença"].rolling(6).mean().round(0)
    df_data["Avg 12M"] = df_data["Diferença"].rolling(12).mean().round(0)
    df_data["Avg 24M"] = df_data["Diferença"].rolling(24).mean().round(0)
    df_data["Diferença Rel."] = (df_data["Valor"] / df_data["Desloc"] -1)
    df_data["Avg 6M Total"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data["Avg 12M Total"] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data["Avg 24M Total"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] - x[0])
    df_data["Avg 6M Total Rel."] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_data["Avg 12M Total Rel."] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] / x[0] - 1)
    df_data["Avg 24M Total Rel."] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] / x[0] - 1)

    df_data = df_data.drop(columns=["Desloc"])

    return df_data

st.set_page_config(page_title="Finanças", page_icon="💰")

st.markdown("""
            # Finanças
            ### Aqui você pode gerenciar suas finanças pessoais.
            - Adicione suas despesas
            - Visualize seus gastos
            - Planeje seu orçamento
            """)

# Widget de upload de arquivo
file_upload = st.file_uploader(label="Carregar arquivo de despesas", type=["csv", "xlsx"])

# Verificar se um arquivo foi carregado
if file_upload is not None:
    # Processar o arquivo carregado
    df = pd.read_csv(file_upload)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

    # Exibir o conteúdo do arquivo
    exp1 = st.expander("Dados Brutos")    
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt, use_container_width=True)

    # Tabela dinâmica por instituição
    exp2 = st.expander("Tabela Dinâmica por Instituição")
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')

    # Abas para dados, histórico e distribuição
    tab_data, tab_history, tb_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

    # Conteúdo das abas
    with tab_data:
        st.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)
    
    with tb_share:

        date = st.selectbox("Filtro Data", options=df_instituicao.index)

        # date = st.date_input("Selecione a data para ver a distribuição:", 
        #                     min_value=df['Data'].min(), 
        #                     max_value=df['Data'].max())
        
        # if date not in df_instituicao.index:
        #     st.warning("Nenhum dado disponível para a data selecionada.")

        # else:
        st.bar_chart(df_instituicao.loc[date])

    exp3 = st.expander("Estatísticas Gerais")
    
    df_stats = calcular_metricas(df)

    columns_config = {

        "Diferença": st.column_config.NumberColumn("Diferença", format="R$ %f"),
        "Avg 6M": st.column_config.NumberColumn("Avg 6M", format="R$ %f"),
        "Avg 12M": st.column_config.NumberColumn("Avg 12M", format="R$ %f"),
        "Avg 24M": st.column_config.NumberColumn("Avg 24M", format="R$ %f"),
        "Diferença Rel.": st.column_config.NumberColumn("Diferença Rel.", format="percent"),
        "Avg 6M Total": st.column_config.NumberColumn("Avg 6M Total", format="R$ %f"),
        "Avg 12M Total": st.column_config.NumberColumn("Dif. Avg 12M Total", format="R$ %f"),
        "Avg 24M Total": st.column_config.NumberColumn("Dif. Avg 24M Total", format="R$ %f"),
        "Avg 6M Total Rel.": st.column_config.NumberColumn("Dif. Avg 6M Total Rel.", format="percent"),
        "Avg 12M Total Rel.": st.column_config.NumberColumn("Dif. Avg 12M Total Rel.", format="percent"),
        "Avg 24M Total Rel.": st.column_config.NumberColumn("Dif. Avg 24M Total Rel.", format="percent")

    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Histórico Evolução", "Crescimento Relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config)

    with tab_abs:
        abs_cols = [
            "Diferença", 
            "Avg 6M", 
            "Avg 12M", 
            "Avg 24M", 
        ]
        st.line_chart(df_stats[abs_cols])

    with tab_rel:
        rel_cols = [
            "Diferença Rel.", 
            "Avg 6M Total Rel.", 
            "Avg 12M Total Rel.", 
            "Avg 24M Total Rel."
        ]
        st.line_chart(data=df_stats[rel_cols])