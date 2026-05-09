import streamlit as st

from database import (
    obter_caso_nao_repetido,
    embaralhar_diagnostico
)

from game_logic import (
    inicializar_estado,
    validar_resposta,
    adicionar_pontos,
    remover_vida,
    adicionar_streak,
    resetar_streak
)


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Plantão Word",
    page_icon="🩺",
    layout="centered"
)


# ==========================================
# ESTADO INICIAL
# ==========================================

inicializar_estado()


# ==========================================
# FUNÇÃO NOVO CASO
# ==========================================

def carregar_novo_caso():

    caso = obter_caso_nao_repetido(
        st.session_state.casos_usados
    )

    st.session_state.caso = caso

    st.session_state.casos_usados.append(caso["id"])

    st.session_state.letras = embaralhar_diagnostico(
        caso["diagnostico"]
    )

    st.session_state.respondido = False


# ==========================================
# PRIMEIRO CASO
# ==========================================

if "caso" not in st.session_state:
    carregar_novo_caso()


caso = st.session_state.caso


# ==========================================
# HEADER
# ==========================================

st.title("🩺 Plantão Word")

st.caption("Diagnostique. Aprenda. Evolua.")


# ==========================================
# STATUS PLAYER
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏆 Pontos", st.session_state.score)

with col2:
    st.metric("🔥 Streak", st.session_state.streak)

with col3:
    st.metric("❤️ Vidas", st.session_state.vidas)


# ==========================================
# BARRA DE PROGRESSO
# ==========================================

progresso = len(st.session_state.casos_usados) / 10

if progresso > 1:
    progresso = 1.0

st.progress(progresso)


# ==========================================
# CARD DO CASO
# ==========================================

st.divider()

st.subheader("📋 Caso Clínico")

st.info(caso["descricao"])

st.write(f"🩺 Especialidade: **{caso['especialidade']}**")

st.write(f"⭐ Dificuldade: {caso['dificuldade']}")


# ==========================================
# LETRAS
# ==========================================

st.subheader("🔤 Letras")

st.write(" ".join(st.session_state.letras))


# ==========================================
# INPUT
# ==========================================

resposta = st.text_input(
    "Qual o diagnóstico?"
)


# ==========================================
# BOTÃO RESPONDER
# ==========================================

if st.button("Responder") and not st.session_state.respondido:

    st.session_state.respondido = True

    correto = validar_resposta(
        resposta,
        caso["diagnostico"]
    )

    if correto:

        st.success("✅ Diagnóstico correto!")

        st.balloons()

        adicionar_pontos(10)

        adicionar_streak()

    else:

        st.error(
            f"❌ Resposta incorreta! "
            f"Diagnóstico: {caso['diagnostico']}"
        )

        remover_vida()

        resetar_streak()

    # EXPLICAÇÃO
    st.subheader("📚 Explicação")

    st.write(caso["explicacao"])


# ==========================================
# GAME OVER
# ==========================================

if st.session_state.vidas <= 0:

    st.error("💀 GAME OVER")

    st.write(
        f"Pontuação final: "
        f"{st.session_state.score}"
    )

    if st.button("Jogar Novamente"):

        st.session_state.clear()

        st.rerun()


# ==========================================
# PRÓXIMO CASO
# ==========================================

elif st.session_state.respondido:

    if st.button("➡️ Próximo Caso"):

        carregar_novo_caso()

        st.rerun()
