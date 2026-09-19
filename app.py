import streamlit as st
import random

# GENERAR EJERCICIO

def generar_ejercicio():

    P = random.choice([True, False])
    Q = random.choice([True, False])
    R = random.choice([True, False])

    expresiones = [
        "(P ∧ Q) ∨ ¬R",
        "(P ∨ Q) ∧ R",
        "¬P ∨ (Q ∧ R)",
        "(P ∧ ¬Q) ∨ R",
        "(P ∨ ¬Q) ∧ ¬R"
    ]

    expresion = random.choice(expresiones)

    if expresion == "(P ∧ Q) ∨ ¬R":
        resultado = (P and Q) or not R

    elif expresion == "(P ∨ Q) ∧ R":
        resultado = (P or Q) and R

    elif expresion == "¬P ∨ (Q ∧ R)":
        resultado = not P or (Q and R)

    elif expresion == "(P ∧ ¬Q) ∨ R":
        resultado = (P and not Q) or R

    else:
        resultado = (P or not Q) and not R

    return P, Q, R, expresion, resultado

# VARIABLES DEL JUEGO

if "ejercicio" not in st.session_state:
    st.session_state.ejercicio = generar_ejercicio()

if "puntos" not in st.session_state:
    st.session_state.puntos = 0

if "vidas" not in st.session_state:
    st.session_state.vidas = 3

if "ejercicio_actual" not in st.session_state:
    st.session_state.ejercicio_actual = 1

if "juego_terminado" not in st.session_state:
    st.session_state.juego_terminado = False

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "mensaje" not in st.session_state:
    st.session_state.mensaje = ""
    
if "juego_terminado" not in st.session_state:
    st.session_state.juego_terminado = False

P, Q, R, expresion, resultado = st.session_state.ejercicio

# TITULO

st.title("🧠 Logic Quest")
st.subheader("Desafío de Tablas de Verdad")

# COLUMNAS

if st.session_state.juego_terminado:

    st.success("🏆 ¡Juego terminado!")

    st.write(
        f"### Puntuación final: {st.session_state.puntos} puntos"
    )

    st.write(
        f"Completaste los 10 ejercicios."
    )

columna1, columna2 = st.columns([2, 1])

# COLUMNA IZQUIERDA

with columna1:
    
    st.write(
        f"**Ejercicio {st.session_state.ejercicio_actual} de 10**"
    )

    st.write("### 🎯 Ejercicio")

    st.code(expresion)

    st.write("P =", "Verdadero" if P else "Falso")
    st.write("Q =", "Verdadero" if Q else "Falso")
    st.write("R =", "Verdadero" if R else "Falso")

if not st.session_state.respondido:

    with st.form("respuesta"):

        respuesta = st.radio(
            "¿Cuál es el resultado de la expresión?",
            ["Verdadero", "Falso"]
        )

        btn_evaluar = st.form_submit_button("Evaluar")

else:

    btn_evaluar = False

# PROCESAR RESPUESTA

if btn_evaluar and not st.session_state.respondido and not st.session_state.juego_terminado:

    respuesta_correcta = "Verdadero" if resultado else "Falso"

    if respuesta == respuesta_correcta:

        # Respuesta correcta
        st.session_state.puntos += 10
        st.session_state.mensaje = "correcto"
        st.session_state.respondido = True

        # Si completa los 10 ejercicios, termina el juego
        if st.session_state.ejercicio_actual == 10:
            st.session_state.juego_terminado = True

    else:

        # Respuesta incorrecta
        st.session_state.vidas -= 1
        st.session_state.mensaje = "incorrecto"

        # Si pierde las 3 vidas, termina el juego
        if st.session_state.vidas == 0:

            st.session_state.juego_terminado = True
            st.session_state.respondido = True

        else:

            # Genera otro ejercicio
            # pero mantiene el mismo número de ejercicio
            st.session_state.ejercicio = generar_ejercicio()

            st.session_state.respondido = False

            st.rerun()
# COLUMNA DERECHA

with columna2:

    st.metric("🏆 Puntos", st.session_state.puntos)

    st.metric("❤️ Vidas", st.session_state.vidas)

    if st.session_state.mensaje == "correcto":
        st.success("✅ ¡Correcto!\n\n+10 puntos")

    elif st.session_state.mensaje == "incorrecto":
        st.error("❌ Incorrecto\n\n-1 vida")

    if st.session_state.respondido:

        respuesta_correcta = "Verdadero" if resultado else "Falso"

        st.write("Respuesta correcta:")
        st.write("**" + respuesta_correcta + "**")

    if not st.session_state.juego_terminado:
        if st.session_state.ejercicio_actual < 10:
            btn_siguiente = st.button("➡️ Siguiente ejercicio")
        else:
            btn_siguiente = False
        
    else:
        btn_siguiente = False

if st.session_state.juego_terminado:

    st.error("💀 ¡GAME OVER!")

    st.write("🏆 Puntuación final:", st.session_state.puntos)

    st.write("❤️ Te quedaste sin vidas.")
    
# SIGUIENTE EJERCICIO

if btn_siguiente:

    if st.session_state.ejercicio_actual < 10:

        st.session_state.ejercicio_actual += 1

        st.session_state.ejercicio = generar_ejercicio()

        st.session_state.respondido = False

        st.session_state.mensaje = ""

        st.rerun()

    else:

        st.session_state.juego_terminado = True

        st.rerun()
