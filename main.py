import streamlit as st

st.set_page_config(page_title="Finanças", page_icon="💰")

st.markdown("""
            # Finanças
            ### Aqui você pode gerenciar suas finanças pessoais.
            - Adicione suas despesas
            - Visualize seus gastos
            - Planeje seu orçamento
            """)

st.file_uploader(label="Carregar arquivo de despesas", type=["csv", "xlsx"])