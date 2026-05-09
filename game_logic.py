import streamlit as st
import time


def inicializar_estado():

    valores_iniciais = {
        "score": 0,
        "high_score": 0,
        "casos_usados": [],
        "respondido": False,
        "streak": 0,
        "vidas": 3,
        "dica_usada": False,
        "tempo_inicio": time.time()
    }

    for chave, valor in valores_iniciais.items():

        if chave not in st.session_state:
            st.session_state[chave] = valor


def validar_resposta(resposta_usuario, resposta_correta):

    return (
        resposta_usuario.strip().upper()
        == resposta_correta.upper()
    )


def adicionar_pontos(pontos=10):

    st.session_state.score += pontos

    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score


def remover_vida():

    st.session_state.vidas -= 1


def adicionar_streak():

    st.session_state.streak += 1


def resetar_streak():

    st.session_state.streak = 0


def reiniciar_timer():

    st.session_state.tempo_inicio = time.time()


def tempo_restante(limite=20):

    tempo_passado = time.time() - st.session_state.tempo_inicio

    restante = int(limite - tempo_passado)

    return max(restante, 0)
