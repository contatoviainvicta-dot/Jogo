import streamlit as st


def inicializar_estado():

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "casos_usados" not in st.session_state:
        st.session_state.casos_usados = []

    if "respondido" not in st.session_state:
        st.session_state.respondido = False

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    if "vidas" not in st.session_state:
        st.session_state.vidas = 3


def validar_resposta(resposta_usuario, resposta_correta):

    return (
        resposta_usuario.strip().upper()
        == resposta_correta.upper()
    )


def adicionar_pontos(pontos=10):

    st.session_state.score += pontos


def remover_vida():

    st.session_state.vidas -= 1


def adicionar_streak():

    st.session_state.streak += 1


def resetar_streak():

    st.session_state.streak = 0
