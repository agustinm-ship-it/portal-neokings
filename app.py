import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Portal SPL - Neokings", layout="wide")

# Estilos CSS Oscuro Neón
st.markdown(
    """
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stButton>button {
        background-color: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stButton>button:hover { background-color: #30363d; border-color: #58a6ff; }
    .card-dia {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-size: 0.8rem;
    }
    .badge-verde { color: #3dd68c; font-weight: bold; }
    .badge-amarillo { color: #facc15; font-weight: bold; }
    .badge-rojo { color: #f87171; font-weight: bold; }
    .panel-accion {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .alerta-box {
        background-color: #2d1517;
        border: 1px solid #f87171;
        border-radius: 8px;
        padding: 10px;
        color: #f87171;
        font-size: 0.85rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# DATOS DE BASE (FALLBACK Y LOCALIDADES)
LOCALIDADES_BASE = {
    "Castelar": {
        "Zona": "OESTE",
        "Valor": 9700,
        "Dia": "Martes / Viernes",
        "Lat": -34.658,
        "Lon": -58.648,
    },
    "Hurlingham": {
        "Zona": "OESTE",
        "Valor": 10500,
        "Dia": "Martes / Viernes",
        "Lat": -34.588,
        "Lon": -58.638,
    },
    "Vicente Lopez": {
        "Zona": "NORTE",
        "Valor": 12700,
        "Dia": "Lunes / Jueves",
        "Lat": -34.528,
        "Lon": -58.473,
    },
    "Flores": {
        "Zona": "CABA",
        "Valor": 12500,
        "Dia": "Miércoles",
        "Lat": -34.628,
        "Lon": -58.461,
    },
    "Belgrano": {
        "Zona": "CABA",
        "Valor": 12500,
        "Dia": "Miércoles",
        "Lat": -34.561,
        "Lon": -58.456,
    },
}

# ENCABEZADO Y ATAJOS
col_titulo, col_btn1, col_btn2, col_btn3 = st.columns([3, 1.2, 1.2, 1.5])
with col_titulo:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_btn1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Cargando horario por zonas...")
with col_btn2:
    if st.button("📋 Reglas Carga"):
        st.toast("Horario límite: 17:30 hs | Cobros COD activos")
with col_btn3:
    if st.button("🔔 Alertas Pendientes (2)"):
        st.toast("⚠️ 2 pedidos en standby hace casi 2 horas")

# BANDERAS DÍAS DE LA SEMANA
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(
        "<div class='card-dia'><b>LUNES</b><br><small"
        " style='color:#8b949e'>Zona Norte</small><br>📦 10 | ⏱️ 6.0h<br><span"
        " class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        "<div class='card-dia'><b>MARTES</b><br><small"
        " style='color:#8b949e'>Zona Oeste</small><br>📦 18 | ⏱️ 5.8h<br><span"
        " class='badge-amarillo'>🟡 PRÓX. CRÍTICO</span></div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        "<div class='card-dia'><b>MIÉRCOLES</b><br><small"
        " style='color:#8b949e'>CABA / Sur</small><br>📦 22 | ⏱️ 7.2h<br><span"
        " class='badge-rojo'>🔴 CRÍTICO</span></div>",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        "<div class='card-dia'><b>JUEVES</b><br><small"
        " style='color:#8b949e'>Zona Norte</small><br>📦 8 | ⏱️ 4.1h<br><span"
        " class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        "<div class='card-dia'><b>VIERNES</b><br><small"
        " style='color:#8b949e'>Zona Oeste</small><br>📦 12 | ⏱️ 5.0h<br><span"
        " class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# COLUMNAS PRINCIPALES
col_izq, col_der = st.columns([1.4, 1])

with col_izq:
    st.markdown("##### 🔎 Búsqueda de Ubicación y Mapa AMBA")
    col_input, col_cant = st.columns([3, 1])

    with col_input:
        direccion_in = st.text_input(
            "Dirección del Cliente:",
            value="Tucumán 1763, Castelar",
            placeholder="Escribí una dirección o localidad...",
        )
    with col_cant:
        paquetes_in = st.number_input("Paquetes:", min_value=1, value=1)

    # Lógica de búsqueda dinámica
    loc_detectada = "Castelar"
    for loc_key in LOCALIDADES_BASE.keys():
        if loc_key.lower() in direccion_in.lower():
            loc_detectada = loc_key
            break

    data_loc = LOCALIDADES_BASE[loc_detectada]

    # Dibuja el mapa centrado en la ubicación buscada
    m = folium.Map(
        location=[data_loc["Lat"], data_loc["Lon"]],
        zoom_start=12,
        tiles="OpenStreetMap",
    )
    folium.Marker(
        [-34.654, -58.619],
        popup="Salida: Depósito Morón",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)
    folium.Marker(
        [data_loc["Lat"], data_loc["Lon"]],
        popup=f"{direccion_in} - BÚSQUEDA ACTUAL",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    folium.PolyLine(
        [[-34.654, -58.619], [data_loc["Lat"], data_loc["Lon"]]],
        color="#38bdf8",
        weight=4,
        opacity=0.85,
    ).add_to(m)

    st_folium(m, width=700, height=380)

with col_der:
    st.markdown("##### ⚙️ Panel de Cotización y Agendamiento")

    st.markdown(
        f"""
    <div class='panel-accion'>
        <div style='font-size: 0.9rem; color: #58a6ff; font-weight: bold;'>📍 UBICACIÓN DETECTADA: {loc_detectada.upper()} — ZONA {data_loc['Zona']}</div>
        <div style='display: flex; justify-content: space-between; margin-top: 10px;'>
            <div><b>Valor Sugerido:</b> ${data_loc['Valor']:,}</div>
            <div><b>Días Recomendados:</b> {data_loc['Dia']}</div>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem;'>
            <b>Posición Estimada en Ruta:</b> Parada #3<br>
            <b>Horario Estimado de Entrega:</b> 11:30 – 13:00 hs<br>
            <b>Kilómetros Adicionales:</b> +3.5 km
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    dia_seleccionado = st.selectbox(
        "📅 Seleccionar Día para Entregar:",
        [
            "Lunes (Zona Norte)",
            "Martes (Zona Oeste)",
            "Miércoles (CABA / Sur)",
            "Jueves (Zona Norte)",
            "Viernes (Zona Oeste)",
        ],
        index=1 if data_loc["Zona"] == "OESTE" else 0,
    )

    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.success("✅ Pedido Confirmado y sumado a la hoja de ruta.")
    with col_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Pedido en Standby por 2 horas.")

    if "Miércoles" in dia_seleccionado:
        st.markdown(
            """
        <div class='alerta-box'>
            ⚠️ <b>¡ATENCIÓN! La ruta del Miércoles está AL 100% (CRÍTICA).</b><br>
            Si lo dejás en pendiente y entra un confirmado, este pedido se desplazará al Jueves.
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button(
            "🔄 Reubicar al Jueves (Zona Habilitada)", use_container_width=True
        ):
            st.info(
                "📩 Notificación enviada al cliente con propuesta de"
                " reubicación."
            )
