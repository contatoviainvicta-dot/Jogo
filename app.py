import streamlit as st
import random

from database import obter_caso_aleatorio


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plantão Word",
    page_icon="🩺",
    layout="centered"
)


# SCORE
if "score" not in st.session_state:
    st.session_state.score = 0


# CASO ATUAL
if "caso" not in st.session_state:
    st.session_state.caso = obter_caso_aleatorio()


caso = st.session_state.caso


# TÍTULO
st.title("🩺 Plantão Word")

st.subheader("Descubra o diagnóstico")


# MOSTRAR CASO
st.write(caso["descricao"])


# EMBARALHAR LETRAS
letras = list(caso["diagnostico"])
random.shuffle(letras)

st.write("🔤 Letras:")
st.write(" ".join(letras))


# INPUT
resposta = st.text_input("Qual o diagnóstico?")


# BOTÃO RESPONDER
if st.button("Responder"):

    if resposta.strip().upper() == caso["diagnostico"]:

        st.success("✅ Diagnóstico correto!")

        st.session_state.score += 10

    else:

        st.error(
            f"❌ Resposta incorreta! Diagnóstico correto: {caso['diagnostico']}"
        )

    # EXPLICAÇÃO
    st.info(caso["explicacao"])


# PONTUAÇÃO
st.write(f"🏆 Pontuação: {st.session_state.score}")


# BOTÃO PRÓXIMO CASO
if st.button("Próximo Caso"):

    st.session_state.caso = obter_caso_aleatorio()

    st.rerun()
