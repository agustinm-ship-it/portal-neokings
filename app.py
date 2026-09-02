import math
import folium
from geopy.geocoders import Nominatim
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Portal SPL - Neokings", layout="wide", page_icon="🚚"
)

# ESTILOS UI/UX OSCURO NEÓN
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
    
    .panel-resumen {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .badge-precio { font-size: 1.8rem; font-weight: bold; color: #3dd68c; }
    .badge-zona { font-size: 1.1rem; font-weight: bold; color: #58a6ff; }
    .alerta-box {
        background-color: #2d1517;
        border: 1px solid #f87171;
        border-radius: 8px;
        padding: 10px;
        color: #f87171;
        font-size: 0.82rem;
        margin-top: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 1. ENCABEZADO Y ATAJOS LÍDER LOGÍSTICO
col_head1, col_b1, col_b2, col_b3 = st.columns([3.5, 1, 1, 1.2])
with col_head1:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_b1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Cargando matriz por zonas...")
with col_b2:
    if st.button("📋 Reglas Carga"):
        st.toast("Horario límite de carga: 17:30 hs.")
with col_b3:
    if st.button("🔔 Alertas (2)"):
        st.toast("⚠️ 2 pedidos en standby cerca del límite de 2hs.")

# 2. CUADROS SEMANALES DE CAPACIDAD
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

# 3. COLUMNAS PRINCIPALES (BÚSQUEDA Y PANEL DE ACCIÓN)
col_izq, col_der = st.columns([1.3, 1])

# Coordenadas base Depósito Morón
LAT_DEP = -34.654
LON_DEP = -58.619

with col_izq:
    st.markdown("##### 🔎 Buscar Dirección Completa (AMBA)")

    # UN SOLO BUSCADOR DIRECTO
    direccion_input = st.text_input(
        "Escribí la Dirección Completa (Calle, Altura y Localidad):",
        value="Santiago del Estero 1557, Paso del Rey",
        placeholder="Ej: Bacacay 1763, Flores",
    )

    lat, lon = LAT_DEP, LON_DEP
    localidad_detectada = "Paso del Rey"
    partido_detectado = "Moreno"
    zona_spl = "OESTE"
    precio_base = 11500

    # GEOLOCALIZACIÓN Y DETECCIÓN AUTOMÁTICA EN UN PASO
    if direccion_input:
        geolocator = Nominatim(user_agent="neokings_spl_app_v5")
        try:
            query = f"{direccion_input}, Buenos Aires, Argentina"
            location = geolocator.geocode(query)
            if location:
                lat, lon = location.latitude, location.longitude

                # Reglas automáticas de zonas por palabras clave
                text_low = direccion_input.lower()
                if "flores" in text_low or "caba" in text_low:
                    localidad_detectada, partido_detectado, zona_spl, (
                        precio_base
                    ) = ("Flores", "CABA", "CABA", 12500)
                elif "belgrano" in text_low:
                    localidad_detectada, partido_detectado, zona_spl, (
                        precio_base
                    ) = ("Belgrano", "CABA", "CABA/NORTE", 13600)
                elif "castelar" in text_low:
                    localidad_detectada, partido_detectado, zona_spl, (
                        precio_base
                    ) = ("Castelar", "Morón", "OESTE", 9700)
                elif "paso del rey" in text_low or "moreno" in text_low:
                    localidad_detectada, partido_detectado, zona_spl, (
                        precio_base
                    ) = ("Paso del Rey", "Moreno", "OESTE", 11500)
        except Exception:
            pass

    # CÁLCULO ESTIMADO DE DISTANCIA Y METRICAS DE RUTA
    dist_km = round(
        math.sqrt((lat - LAT_DEP) ** 2 + (lon - LON_DEP) ** 2) * 111, 1
    )
    if dist_km == 0:
        dist_km = 8.4

    # MAPA
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")
    folium.Marker(
        [LAT_DEP, LON_DEP],
        popup="Salida: Depósito Morón",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)
    folium.Marker(
        [lat, lon],
        popup=f"Entrega: {direccion_input}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    folium.PolyLine(
        [[LAT_DEP, LON_DEP], [lat, lon]], color="#38bdf8", weight=4, opacity=0.85
    ).add_to(m)

    st_folium(m, width=680, height=360)

with col_der:
    st.markdown("##### ⚙️ Panel de Cotización y Agendamiento")

    st.markdown(
        f"""
    <div class='panel-resumen'>
        <div class='badge-zona'>📍 {localidad_detectada.upper()} ({partido_detectado})</div>
        <div style='margin-top: 4px; font-size: 0.85rem;'>Zona SPL: <b>{zona_spl}</b></div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <small style='color: #8b949e;'>Valor de Viaje Base:</small><br>
                <span style='font-size: 1.1rem; font-weight: bold;'>${precio_base:,}</span>
            </div>
            <div style='text-align: right;'>
                <small style='color: #8b949e;'>Valor Sugerido:</small><br>
                <span class='badge-precio'>${precio_base:,}</span>
            </div>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem; line-height: 1.6;'>
            📍 <b>Posición Estimada en Ruta:</b> Parada #3<br>
            ⏱️ <b>Horario Estimado de Entrega:</b> 11:30 – 13:00 hs<br>
            🛣️ <b>Kilómetros Adicionales:</b> +{dist_km} km desde Depósito
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    bultos = st.number_input("📦 Cantidad de Bultos/Paquetes:", min_value=1, value=1)
    dia_agendado = st.selectbox(
        "📅 Seleccionar Día para Programar Entrega:",
        [
            "Martes (Zona Oeste)",
            "Viernes (Zona Oeste)",
            "Lunes (Zona Norte)",
            "Miércoles (CABA / Sur)",
            "Jueves (Zona Norte)",
        ],
    )

    if "Miércoles" in dia_agendado:
        st.markdown(
            "<div class='alerta-box'>⚠️ <b>¡Ruta Crítica!</b> La capacidad del"
            " Miércoles está al 100%. Te recomendamos agendar para el Jueves o"
            " Viernes.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c_act1, c_act2 = st.columns(2)
    with c_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.success(
                f"✅ Pedido guardado para {direccion_input} ({bultos} bulto/s)"
                f" - {dia_agendado}."
            )
    with c_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Pedido guardado en Standby por 2 horas.")
