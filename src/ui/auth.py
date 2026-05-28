import streamlit as st

from src.conexion_sheets import obtener_usuarios


def login(hoja):
    st.image("assets/logo_mundial.png", width="stretch")
    st.markdown(
        '<h1 class="titulo-mundial" style="text-align: center; font-size: 2rem; margin-top: -10px;">CO-FATALES 2026</h1>',
        unsafe_allow_html=True,
    )
    st.caption("Mundial 2026 — La apuesta de los amigos")

    st.divider()

    df_usuarios = obtener_usuarios()
    if df_usuarios.empty:
        st.error("No se pudo cargar la lista de usuarios.")
        return

    df_usuarios = df_usuarios.sort_values("Nombre").reset_index(drop=True)
    opciones = [
        f"{row['Nombre']} {row['Bandera']}"
        for _, row in df_usuarios.iterrows()
    ]
    placeholder = "Selecciona tu nombre..."
    opciones.insert(0, placeholder)

    st.subheader("🎫 Acceso al Quiniela")
    seleccion = st.selectbox(
        "¿Quién eres?",
        options=opciones,
        index=0,
        key="login_usuario",
    )

    if seleccion == placeholder:
        st.warning("Seleccioná tu nombre para continuar.")
        return

    nombre_limpio = seleccion.rsplit(" ", 1)[0]
    bandera = seleccion.rsplit(" ", 1)[1]

    match = df_usuarios[df_usuarios["Nombre"] == nombre_limpio]
    if match.empty:
        st.error("Usuario no encontrado.")
        return
    pin_real = str(match.iloc[0]["PIN"]).strip()

    pin = st.text_input("🔐 PIN de Acceso", type="password", key="login_pin")

    if st.button("Entrar", type="primary", use_container_width=True):
        if pin.strip() != pin_real:
            st.error("❌ PIN incorrecto. Volvé a intentar.")
            return
        st.session_state.autenticado = True
        st.session_state.usuario_data = {
            "nombre": nombre_limpio,
            "bandera": bandera,
        }
        st.session_state.usuario_nombre = nombre_limpio
        st.session_state.mostrar_ticket = True
        st.rerun()


def renderizar_ticket():
    nombre = st.session_state.usuario_data["nombre"]
    bandera = st.session_state.usuario_data["bandera"]
    st.balloons()
    st.markdown(
        f"""
        <div style="max-width: 460px; margin: 40px auto; padding: 30px 24px;
             background: linear-gradient(135deg, #1a1f26, #0e1117);
             border: 2px solid #FFD700; border-radius: 20px;
             box-shadow: 0 0 40px rgba(255, 215, 0, 0.2);
             text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎟️</div>
            <div style="color: #FFD700; font-weight: 900; font-size: 1.1rem;
                 letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px;">
                FATALITY PASS
            </div>
            <div style="color: #888; font-size: 0.75rem; letter-spacing: 1px;
                 margin-bottom: 16px;">
                LICENCIA DE DT DE SILLÓN
            </div>
            <div style="border-top: 1px dashed #333; border-bottom: 1px dashed #333;
                 padding: 16px 0; margin-bottom: 16px;">
                <div style="font-size: 0.85rem; color: #CCC; margin-bottom: 8px;">
                    Certificamos que
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #FAFAFA;">
                    {bandera} {nombre}
                </div>
                <div style="font-size: 0.8rem; color: #888; margin-top: 6px;">
                    tiene permiso oficial para insultar al VAR<br>
                    y fallar todos sus pronósticos.
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Aceptar mi triste realidad y entrar", type="primary", use_container_width=True):
        st.session_state.mostrar_ticket = False
        st.rerun()


def renderizar_sidebar_usuario():
    data = st.session_state.get("usuario_data", {})
    nombre = data.get("nombre", "")
    bandera = data.get("bandera", "")
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; padding: 12px; border-bottom: 1px solid #2a2a2a;">
            <div style="font-size: 0.65rem; color: #888; letter-spacing: 1px;">CONECTADO</div>
            <div style="font-size: 1.3rem; margin: 4px 0;">{bandera}</div>
            <div style="font-size: 0.9rem; font-weight: 700; color: #D4AF37;">{nombre}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    st.sidebar.radio(
        "Navegación",
        options=["Dashboard", "Oráculo IA", "Ranking"],
        key="navegacion",
        label_visibility="collapsed",
    )
    st.sidebar.divider()
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        for k in ["autenticado", "usuario_data", "usuario_nombre", "mostrar_ticket"]:
            st.session_state.pop(k, None)
        st.rerun()
