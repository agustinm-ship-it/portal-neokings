import folium
from geopy.geocoders import Nominatim
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Portal SPL - Neokings", layout="wide", page_icon="🚚"
)

# ESTILOS OSCURO NEÓN SIN SELECTOR SUPERIOR
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
        padding: 10px;
        text-align: center;
        font-size: 0.82rem;
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
    </style>
""",
    unsafe_allow_html=True,
)

# ID DE TU GOOGLE SHEETS
SHEET_ID = "https://docs.google.com/spreadsheets/d/1HSnCjlmmqSG5zSPYNAAAsujwRD4rhZGQf4e_4bGec88/edit?usp=sharing"


@st.cache_data(ttl=30)
def cargar_bases_desde_sheets(sheet_id):
    try:
        url_loc = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Localidades%20y%20valores"
        url_hor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=HORARIOS"
        df_loc = pd.read_csv(url_loc)
        df_hor = pd.read_csv(url_hor)

        # Limpieza de columnas
        df_loc.columns = [c.strip() for c in df_loc.columns]
        resumen_horarios = df_hor.iloc[5:17, [0, 1]].dropna()
        resumen_horarios.columns = ["Zona", "Días y Franjas Horarias Habilitadas"]

        return df_loc, resumen_horarios
    except Exception:
        # Respaldo si no está configurado el ID aún
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
        ]
        return pd.DataFrame(datos_loc), pd.DataFrame(datos_hor)


df_localidades, df_franjas = cargar_bases_desde_sheets(SHEET_ID)

# 1. ENCABEZADO Y BOTONES DE ATAJO (SIN VENDEDORES)
col_head1, col_b1, col_b2, col_b3 = st.columns([3, 1, 1, 1.2])
with col_head1:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_b1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Matriz de zonificación cargada.")
with col_b2:
    if st.button("📋 Reglas Carga"):
        st.toast("Límite de carga: 17:30 hs.")
with col_b3:
    if st.button("🔔 Alertas Pendientes (2)"):
        st.toast("⚠️ 2 pedidos en standby hace 1h 45m.")

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
    st.markdown("##### 🔎 Búsqueda de Dirección / Localidad")

    # BUSCADOR AUTOCOMPLETADO
    lista_opciones = df_localidades["Localidad"].astype(str).tolist()
    localidad_sel = st.selectbox(
        "Seleccioná la Localidad/Barrio:",
        options=lista_opciones,
        index=0,
    )

    calle_altura = st.text_input(
        "Dirección exacta (Calle y Altura):",
        value="Santiago del Estero 1557",
        placeholder="Ej: Bacacay 1763",
    )

    # GEOCODIFICACIÓN
    geolocator = Nominatim(user_agent="neokings_spl_app_v3")
    lat, lon = -34.654, -58.619

    try:
        query_geo = f"{calle_altura}, {localidad_sel}, Buenos Aires, Argentina"
        location = geolocator.geocode(query_geo)
        if location:
            lat, lon = location.latitude, location.longitude
    except Exception:
        pass

    # CRUCE CON PLANILLA
    match = df_localidades[
        df_localidades["Localidad"].astype(str).str.lower()
        == localidad_sel.lower()
    ]
    row_data = (
        match.iloc[0] if not match.empty else df_localidades.iloc[0]
    )

    # MAPA
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

    st_folium(m, width=650, height=340)

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

    st.markdown(
        f"""
    <div class='panel-resumen'>
        <div class='badge-zona'>📍 {str(row_data['Localidad']).upper()} ({row_data['Partido']})</div>
        <div style='margin-top: 5px;'>CP: <b>{row_data['Código Postal']}</b> | Zona SPL: <b>{row_data['Zona']}</b></div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between;'>
            <div><b>💰 Valor de Viaje:</b><br>${row_data['Valor de viaje']:,}</div>
            <div><b>🏷️ Valor Recomendado:</b><br><span class='badge-precio'>${row_data['Valor Recomendado']:,}</span></div>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem;'>
            <b>📅 Días y Franjas Habilitadas:</b><br>
            <span style='color:#facc15;'>{franja_txt}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    bultos = st.number_input("📦 Cantidad de Bultos/Paquetes:", min_value=1, value=1)

    c_act1, c_act2 = st.columns(2)
    with c_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.success(
                f"✅ Pedido confirmado para {calle_altura}, {localidad_sel} ({bultos} bulto/s)."
            )
    with c_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Pedido guardado en Standby por 2 horas.")
