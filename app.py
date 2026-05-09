import streamlit as st

from database import (
    obter_caso_nao_repetido,
    embaralhar_diagnostico,
    obter_cor_raridade
)

from game_logic import (
    inicializar_estado,
    validar_resposta,
    adicionar_pontos,
    remover_vida,
    adicionar_streak,
    resetar_streak,
    reiniciar_timer,
    tempo_restante
)


# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Plantão Word",
    page_icon="🩺",
    layout="centered"
)

inicializar_estado()


# ==========================================
# NOVO CASO
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

    st.session_state.dica_usada = False

    reiniciar_timer()


if "caso" not in st.session_state:
    carregar_novo_caso()


caso = st.session_state.caso


# ==========================================
# HEADER
# ==========================================

st.title("🩺 Plantão Word")

st.caption("Diagnostique. Aprenda. Evolua.")


# ==========================================
# STATUS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏆 Pontos", st.session_state.score)

with col2:
    st.metric("🔥 Streak", st.session_state.streak)

with col3:
    st.metric("❤️ Vidas", st.session_state.vidas)

with col4:
    st.metric("👑 Recorde", st.session_state.high_score)


# ==========================================
# TIMER
# ==========================================

tempo = tempo_restante()

st.metric("⏱️ Tempo", f"{tempo}s")

if tempo <= 0 and not st.session_state.respondido:

    st.warning("⏰ Tempo esgotado!")

    remover_vida()

    resetar_streak()

    st.session_state.respondido = True


# ==========================================
# PROGRESSO
# ==========================================

progresso = len(st.session_state.casos_usados) / 15

if progresso > 1:
    progresso = 1.0

st.progress(progresso)


# ==========================================
# CASO
# ==========================================

st.divider()

raridade = caso.get("raridade", "Comum")

icone = obter_cor_raridade(raridade)

st.subheader(f"{icone} Caso {raridade}")

st.info(caso["descricao"])

st.write(f"🩺 Especialidade: **{caso['especialidade']}**")

st.write(f"⭐ Dificuldade: {caso['dificuldade']}")


# ==========================================
# LETRAS
# ==========================================

st.subheader("🔤 Letras")

st.write(" ".join(st.session_state.letras))


# ==========================================
# DICA
# ==========================================

if not st.session_state.dica_usada:

    if st.button("💡 Usar dica (-5 pontos)"):

        st.session_state.score = max(
            st.session_state.score - 5,
            0
        )

        st.session_state.dica_usada = True


if st.session_state.dica_usada:

    st.info(f"💡 Dica: {caso['dica']}")


# ==========================================
# INPUT
# ==========================================

resposta = st.text_input(
    "Qual o diagnóstico?"
)


# ==========================================
# RESPONDER
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
            f"❌ Diagnóstico correto: "
            f"{caso['diagnostico']}"
        )

        remover_vida()

        resetar_streak()

    st.subheader("📚 Explicação")

    st.write(caso["explicacao"])


# ==========================================
# GAME OVER
# ==========================================

if st.session_state.vidas <= 0:

    st.error("💀 GAME OVER")

    st.write(
        f"🏆 Pontuação Final: "
        f"{st.session_state.score}"
    )

    st.write(
        f"👑 Melhor Pontuação: "
        f"{st.session_state.high_score}"
    )

    if st.button("🔄 Jogar Novamente"):

        st.session_state.clear()

        st.rerun()


# ==========================================
# PRÓXIMO CASO
# ==========================================

elif st.session_state.respondido:

    if st.button("➡️ Próximo Caso"):

        carregar_novo_caso()

        st.rerun()
