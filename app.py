import math
import folium
from geopy.geocoders import Nominatim
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Portal SPL - Neokings", layout="wide", page_icon="🚚"
)

# ESTILOS MODO OSCURO
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
        padding: 18px;
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

# ID DE GOOGLE SHEETS PARA LEER LA HOJA 'HORARIOS'
SHEET_ID = "https://docs.google.com/spreadsheets/d/1HSnCjlmmqSG5zSPYNAAAsujwRD4rhZGQf4e_4bGec88/edit?usp=sharing"


@st.cache_data(ttl=60)
def cargar_horarios_sheets(sheet_id):
    try:
        url_hor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=HORARIOS"
        df_hor = pd.read_csv(url_hor)
        resumen_horarios = df_hor.iloc[5:17, [0, 1]].dropna()
        resumen_horarios.columns = ["Zona", "Días y Franjas Horarias Habilitadas"]
        return resumen_horarios
    except Exception:
        # Base de Respaldo Integrada para Evitar Caídas
        return pd.DataFrame([
            {
                "Zona": "OESTE",
                "Días y Franjas Horarias Habilitadas": (
                    "Mar y Mié: 08:30-11:00 hs | Vie: 15:00-17:00 hs"
                ),
            },
            {
                "Zona": "CABA",
                "Días y Franjas Horarias Habilitadas": (
                    "Lun y Jue: 08:30-11:00 hs | Mié: 13:00-15:00 hs"
                ),
            },
            {
                "Zona": "NORTE",
                "Días y Franjas Horarias Habilitadas": (
                    "Lun: 13:00-15:00 hs | Vie: 11:00-13:00 hs"
                ),
            },
        ])


df_franjas = cargar_horarios_sheets(SHEET_ID)

# INICIALIZACIÓN DE LA MEMORIA DE SESIÓN (RUTA ACUMULADA)
if "pedidos_ruta" not in st.session_state:
    st.session_state.pedidos_ruta = []

# COORDENADAS BASE DEL DEPÓSITO (TUCUMÁN 1769, CASTELAR)
LAT_DEP = -34.6582
LON_DEP = -58.6481


# FUNCIÓN CÁLCULO DE DISTANCIA (HAVERSINE / TRACCIADO EN KM)
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


# 1. ENCABEZADO Y ATAJOS
col_head1, col_b1, col_b2, col_b3 = st.columns([3.5, 1, 1, 1.2])
with col_head1:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_b1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Cargando franjas horarias habilitadas...")
with col_b2:
    if st.button("📋 Reglas Carga"):
        st.toast("Horario límite de carga: 17:30 hs.")
with col_b3:
    if st.button("🔔 Alertas (2)"):
        st.toast("⚠️ 2 pedidos en standby cerca del límite.")

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

# 3. COLUMNAS PRINCIPALES
col_izq, col_der = st.columns([1.3, 1])

with col_izq:
    st.markdown("##### 🔎 Buscar Dirección Completa")

    col_inp, col_clean = st.columns([4, 1])
    with col_inp:
        direccion_input = st.text_input(
            "Escribí Calle, Altura y Localidad:",
            value="Bacacay 1763, Flores",
            placeholder="Ej: Tucumán 1763, Castelar",
            label_visibility="collapsed",
        )
    with col_clean:
        if st.button("🗑️ Reiniciar Ruta"):
            st.session_state.pedidos_ruta = []
            st.rerun()

    lat_actual, lon_actual = LAT_DEP, LON_DEP
    localidad_det, zona_det, precio_sugerido = "Castelar", "OESTE", 9700

    if direccion_input:
        geolocator = Nominatim(user_agent="neokings_spl_app_v6")
        try:
            location = geolocator.geocode(
                f"{direccion_input}, Buenos Aires, Argentina"
            )
            if location:
                lat_actual, lon_actual = location.latitude, location.longitude

                # Detección automática de Zona y Precio Base
                txt = direccion_input.lower()
                if "flores" in txt or "caba" in txt:
                    localidad_det, zona_det, precio_sugerido = (
                        "Flores",
                        "CABA",
                        12500,
                    )
                elif "belgrano" in txt:
                    localidad_det, zona_det, precio_sugerido = (
                        "Belgrano",
                        "CABA/NORTE",
                        13600,
                    )
                elif "castelar" in txt or "moron" in txt:
                    localidad_det, zona_det, precio_sugerido = (
                        "Castelar",
                        "OESTE",
                        9700,
                    )
                elif "paso del rey" in txt or "moreno" in txt:
                    localidad_det, zona_det, precio_sugerido = (
                        "Paso del Rey",
                        "OESTE",
                        11500,
                    )
        except Exception:
            pass

    # DETERMINAR PUNTO DE ORIGEN PARA CÁLCULO DE KM DEL TRAMO
    if len(st.session_state.pedidos_ruta) == 0:
        origen_lat, origen_lon = LAT_DEP, LON_DEP
        origen_nombre = "Depósito Castelar"
        num_parada = 1
    else:
        ultimo_pedido = st.session_state.pedidos_ruta[-1]
        origen_lat, origen_lon = ultimo_pedido["lat"], ultimo_pedido["lon"]
        origen_nombre = f"Parada #{len(st.session_state.pedidos_ruta)}"
        num_parada = len(st.session_state.pedidos_ruta) + 1

    dist_tramo = calcular_distancia(
        origen_lat, origen_lon, lat_actual, lon_actual
    )

    # CONSTRUCCIÓN DEL MAPA INTERACTIVO Y DIBUJO DE TRAYECTORIA
    m = folium.Map(
        location=[lat_actual, lon_actual], zoom_start=12, tiles="OpenStreetMap"
    )

    # Pin Depósito
    folium.Marker(
        [LAT_DEP, LON_DEP],
        popup="Depósito: Tucumán 1769, Castelar",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)

    # Trazado de ruta acumulada
    puntos_trayectoria = [[LAT_DEP, LON_DEP]]
    for idx, ped in enumerate(st.session_state.pedidos_ruta):
        pt = [ped["lat"], ped["lon"]]
        puntos_trayectoria.append(pt)
        folium.Marker(
            pt,
            popup=f"Parada #{idx + 1}: {ped['direccion']}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    # Punto actual en búsqueda
    puntos_trayectoria.append([lat_actual, lon_actual])
    folium.Marker(
        [lat_actual, lon_actual],
        popup=f"Búsqueda Actual (#{num_parada}): {direccion_input}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

    # Dibujar la línea de trayectoria continua
    folium.PolyLine(
        puntos_trayectoria, color="#38bdf8", weight=4, opacity=0.85
    ).add_to(m)

    st_folium(m, width=680, height=360)

with col_der:
    st.markdown("##### ⚙️ Panel de Cotización y Agendamiento")

    franja_match = df_franjas[
        df_franjas["Zona"].astype(str).str.upper() == zona_det.upper()
    ]
    franja_txt = (
        franja_match.iloc[0]["Días y Franjas Horarias Habilitadas"]
        if not franja_match.empty
        else "Consulte disponibilidad con logística."
    )

    st.markdown(
        f"""
    <div class='panel-resumen'>
        <div class='badge-zona'>📍 {localidad_det.upper()} — ZONA {zona_det}</div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <small style='color: #8b949e;'>Valor Sugerido:</small><br>
                <span class='badge-precio'>${precio_sugerido:,}</span>
            </div>
            <div style='text-align: right;'>
                <small style='color: #8b949e;'>Orden de Ruta:</small><br>
                <span style='font-size: 1.1rem; font-weight: bold; color: #58a6ff;'>Parada #{num_parada}</span>
            </div>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem; line-height: 1.6;'>
            📏 <b>Distancia del Tramo:</b> +{dist_tramo} km (Desde {origen_nombre})<br>
            ⏱️ <b>Ventana Estimada:</b> 11:30 – 13:00 hs<br>
            📅 <b>Franjas Habilitadas:</b><br>
            <span style='color:#facc15;'>{franja_txt}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    bultos = st.number_input(
        "📦 Cantidad de Bultos/Paquetes:", min_value=1, value=1
    )
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
            "<div class='alerta-box'>⚠️ <b>¡Ruta Crítica!</b> Capacidad del"
            " Miércoles al 100%.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c_act1, c_act2 = st.columns(2)
    with c_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.session_state.pedidos_ruta.append({
                "direccion": direccion_input,
                "lat": lat_actual,
                "lon": lon_actual,
                "bultos": bultos,
                "dia": dia_agendado,
            })
            st.success(f"✅ Pedido #{num_parada} guardado en la hoja de ruta.")
            st.rerun()
    with c_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Pedido guardado en Standby por 2 horas.")
