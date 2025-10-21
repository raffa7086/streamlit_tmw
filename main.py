import streamlit as st
import pandas as pd

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
        last_dt = df_instituicao.sort_index().iloc[-1]
        st.bar_chart(last_dt)