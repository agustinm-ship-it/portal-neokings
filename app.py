import folium
from geopy.geocoders import Nominatim
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Portal SPL - Neokings", layout="wide", page_icon="🚚"
)

# ESTILOS MODO OSCURO NEÓN (DISEÑO LIMPIO)
st.markdown(
    """
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .block-container { padding-top: 1.2rem; padding-bottom: 1.2rem; }
    
    /* Botones Atajo */
    .stButton>button {
        background-color: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stButton>button:hover { background-color: #30363d; border-color: #58a6ff; }

    /* Tarjetas de Días */
    .card-dia {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 0.82rem;
    }
    .badge-verde { color: #3dd68c; font-weight: bold; }
    .badge-amarillo { color: #facc15; font-weight: bold; }
    .badge-rojo { color: #f87171; font-weight: bold; }
    
    /* Panel de Cotización */
    .panel-resumen {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .badge-precio { font-size: 2.2rem; font-weight: bold; color: #3dd68c; line-height: 1.1; }
    .badge-zona { font-size: 1.2rem; font-weight: bold; color: #58a6ff; }
    .info-alerta {
        background-color: #2d1517;
        border: 1px solid #f87171;
        border-radius: 6px;
        padding: 8px 12px;
        color: #f87171;
        font-size: 0.82rem;
        margin-top: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# LINK A TU GOOGLE SHEETS
# Pegá el ID o la URL completa de tu archivo entre las comillas
SHEET_ID = "https://docs.google.com/spreadsheets/d/1HSnCjlmmqSG5zSPYNAAAsujwRD4rhZGQf4e_4bGec88/edit?usp=sharing"


@st.cache_data(ttl=30)
def cargar_bases_desde_sheets(sheet_id):
    try:
        url_loc = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Localidades%20y%20valores"
        url_hor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=HORARIOS"
        df_loc = pd.read_csv(url_loc)
        df_hor = pd.read_csv(url_hor)

        df_loc.columns = [c.strip() for c in df_loc.columns]
        resumen_horarios = df_hor.iloc[5:17, [0, 1]].dropna()
        resumen_horarios.columns = ["Zona", "Días y Franjas Horarias Habilitadas"]

        return df_loc, resumen_horarios
    except Exception:
        # Base de Respaldo Integrada para Evitar Pantallas Rojas
        datos_loc = [
            {
                "Localidad": "Castelar",
                "Partido": "Morón",
                "Zona": "OESTE",
                "Valor de viaje": 9700,
                "Código Postal": "1712",
                "Valor Recomendado": 9700,
            },
            {
                "Localidad": "Paso del Rey",
                "Partido": "Moreno",
                "Zona": "OESTE",
                "Valor de viaje": 11500,
                "Código Postal": "1742",
                "Valor Recomendado": 11500,
            },
            {
                "Localidad": "Belgrano",
                "Partido": "CABA",
                "Zona": "CABA/NORTE",
                "Valor de viaje": 13600,
                "Código Postal": "1428",
                "Valor Recomendado": 13600,
            },
            {
                "Localidad": "Flores",
                "Partido": "CABA",
                "Zona": "CABA",
                "Valor de viaje": 12500,
                "Código Postal": "1406",
                "Valor Recomendado": 12500,
            },
        ]
        datos_hor = [
            {
                "Zona": "OESTE",
                "Días y Franjas Horarias Habilitadas": (
                    "Mar y Mié: 08:30-11:00 hs | Vie: 15:00-17:00 hs"
                ),
            },
            {
                "Zona": "CABA/NORTE",
                "Días y Franjas Horarias Habilitadas": (
                    "Lun y Jue: 08:30-11:00 hs | Mié: 13:00-15:00 hs"
                ),
            },
            {
                "Zona": "CABA",
                "Días y Franjas Horarias Habilitadas": (
                    "Lun a Vie: 08:30-11:00 hs / 13:00-15:00 hs"
                ),
            },
        ]
        return pd.DataFrame(datos_loc), pd.DataFrame(datos_hor)


df_localidades, df_franjas = cargar_bases_desde_sheets(SHEET_ID)

# 1. ENCABEZADO Y ATAJOS (LIMPIO)
col_head1, col_b1, col_b2, col_b3 = st.columns([3.5, 1, 1, 1.2])
with col_head1:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_b1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Cargando matriz semanal de zonificación...")
with col_b2:
    if st.button("📋 Reglas Carga"):
        st.toast("Horario límite de carga: 17:30 hs.")
with col_b3:
    if st.button("🔔 Alertas (2)"):
        st.toast("⚠️ 2 pedidos pendientes hace más de 1h 45m.")

# 2. BANDERAS DÍAS DE LA SEMANA
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

# 3. MÓDULO PRINCIPAL DE BÚSQUEDA Y AGENDAMIENTO
col_izq, col_der = st.columns([1.3, 1])

with col_izq:
    st.markdown("##### 🔎 Selección de Ubicación del Cliente")

    lista_localidades = (
        df_localidades["Localidad"].astype(str).unique().tolist()
    )
    localidad_sel = st.selectbox(
        "1. Localidad / Barrio (Padrón 245 Zonas):",
        options=lista_localidades,
        index=0,
    )

    calle_altura = st.text_input(
        "2. Calle y Altura exactos:",
        value="Santiago del Estero 1557",
        placeholder="Ej: Bacacay 1763",
    )

    # Coordenadas por defecto (Morón)
    lat, lon = -34.654, -58.619

    # Intentar obtener ubicación geográfica exacta
    if calle_altura and localidad_sel:
        geolocator = Nominatim(user_agent="neokings_spl_app_v4")
        try:
            query = f"{calle_altura}, {localidad_sel}, Buenos Aires, Argentina"
            location = geolocator.geocode(query)
            if location:
                lat, lon = location.latitude, location.longitude
        except Exception:
            pass

    # Obtener fila correspondiente
    match = df_localidades[
        df_localidades["Localidad"].astype(str).str.lower()
        == localidad_sel.lower()
    ]
    row_data = (
        match.iloc[0] if not match.empty else df_localidades.iloc[0]
    )

    # MAPA DEL AMBA CON RUTEO
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")
    folium.Marker(
        [-34.654, -58.619],
        popup="Depósito Morón",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)
    folium.Marker(
        [lat, lon],
        popup=f"Cliente: {calle_altura}, {localidad_sel}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    folium.PolyLine(
        [[-34.654, -58.619], [lat, lon]], color="#38bdf8", weight=4
    ).add_to(m)

    st_folium(m, width=680, height=360)

with col_der:
    st.markdown("##### ⚙️ Panel de Cotización y Agendamiento")

    zona_key = str(row_data["Zona"])
    franja_match = df_franjas[
        df_franjas["Zona"].astype(str).str.upper() == zona_key.upper()
    ]
    franja_txt = (
        franja_match.iloc[0]["Días y Franjas Horarias Habilitadas"]
        if not franja_match.empty
        else "Consulte disponibilidad con logística."
    )

    valor_viaje = row_data["Valor de viaje"]
    valor_rec = row_data["Valor Recomendado"]

    st.markdown(
        f"""
    <div class='panel-resumen'>
        <div class='badge-zona'>📍 {str(row_data['Localidad']).upper()} ({row_data['Partido']})</div>
        <div style='margin-top: 4px; font-size: 0.88rem;'>CP: <b>{row_data['Código Postal']}</b> | Zona SPL: <b>{row_data['Zona']}</b></div>
        <hr style='border-color: #30363d; margin: 12px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <small style='color: #8b949e;'>Valor de Viaje Base:</small><br>
                <span style='font-size: 1.1rem; font-weight: bold;'>${valor_viaje:,}</span>
            </div>
            <div style='text-align: right;'>
                <small style='color: #8b949e;'>Valor Recomendado:</small><br>
                <span class='badge-precio'>${valor_rec:,}</span>
            </div>
        </div>
        <hr style='border-color: #30363d; margin: 12px 0;'>
        <div style='font-size: 0.85rem;'>
            <b>📅 Días y Franjas Habilitadas:</b><br>
            <span style='color:#facc15;'>{franja_txt}</span>
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
            "<div class='info-alerta'>⚠️ <b>Atención:</b> La ruta del Miércoles"
            " está al 100% de capacidad (CRÍTICA).</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c_act1, c_act2 = st.columns(2)
    with c_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.success(
                f"✅ Pedido confirmado para {calle_altura}, {localidad_sel}"
                f" ({bultos} bulto/s) agendado para el {dia_agendado}."
            )
    with c_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Pedido guardado en Standby por 2 horas.")
