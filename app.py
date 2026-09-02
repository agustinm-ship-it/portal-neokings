import folium
from geopy.geocoders import Nominatim
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Portal SPL - Neokings", layout="wide")

# ESTILOS CSS MODO OSCURO NEÓN
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
    }
    .stButton>button:hover { background-color: #30363d; border-color: #58a6ff; }
    .panel-resumen {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .badge-precio { font-size: 1.6rem; font-weight: bold; color: #3dd68c; }
    .badge-zona { font-size: 1.1rem; font-weight: bold; color: #58a6ff; }
    </style>
""",
    unsafe_allow_html=True,
)

# ID DE TU GOOGLE SHEETS
# Reemplazá esta cadena con el ID exacto de la URL de tu archivo
SHEET_ID = "https://docs.google.com/spreadsheets/d/1HSnCjlmmqSG5zSPYNAAAsujwRD4rhZGQf4e_4bGec88/edit?usp=sharing"


@st.cache_data(ttl=60)  # Recarga datos automáticamente cada 60 segundos
def cargar_bases_desde_sheets(sheet_id):
    # Enlaces de exportación directos por nombre de hoja
    url_loc = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Localidades%20y%20valores"
    url_hor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=HORARIOS"

    df_loc = pd.read_csv(url_loc)
    df_hor = pd.read_csv(url_hor)

    # Extraer matriz de franjas por zona
    resumen_horarios = df_hor.iloc[5:17, [0, 1]].dropna()
    resumen_horarios.columns = ["Zona", "Días y Franjas Horarias Habilitadas"]

    return df_loc, resumen_horarios


# SI AÚN NO PONÉS EL ID REAL, USAREMOS LA BASE DE RESPALDO INTERNA PARA QUE NO FALLE
try:
    df_localidades, df_franjas = cargar_bases_desde_sheets(SHEET_ID)
except Exception:
    # Respaldo si no encuentra la URL
    df_localidades = pd.DataFrame([{
        "Localidad": "Castelar",
        "Partido": "Morón",
        "Zona": "OESTE",
        "Valor de viaje": 9700,
        "Código Postal": "1712",
        "Valor Recomendado": 9700,
    }])
    df_franjas = pd.DataFrame([{
        "Zona": "OESTE",
        "Días y Franjas Horarias Habilitadas": (
            "Martes y Viernes: 08:30-11:00 hs / 15:00-17:00 hs"
        ),
    }])

# ENCABEZADO
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### 🚚 COTIZADOR Y DESPACHO COMERCIAL - SISTEMA SPL")
with col_head2:
    vendedor = st.selectbox(
        "Vendedor Activo:",
        [
            "General",
            "Agustín M.",
            "Eugenia",
            "E. Gómez",
            "G. Collazo",
            "L. Moreno",
            "Celina Jara",
        ],
    )

st.markdown("---")

col_izq, col_der = st.columns([1.3, 1])

with col_izq:
    st.markdown("##### 🔎 Buscar Dirección Exacta (AMBA)")
    direccion_input = st.text_input(
        "Ingresá Calle, Altura y Localidad:",
        value="Tucumán 1763, Castelar",
        placeholder="Ej: Bacacay 1763, Flores",
    )

    geolocator = Nominatim(user_agent="neokings_spl_app")
    lat, lon = -34.654, -58.619
    localidad_detectada = "Castelar"

    if direccion_input:
        try:
            location = geolocator.geocode(
                f"{direccion_input}, Buenos Aires, Argentina"
            )
            if location:
                lat, lon = location.latitude, location.longitude
                for loc in df_localidades["Localidad"].unique():
                    if str(loc).lower() in direccion_input.lower():
                        localidad_detectada = loc
                        break
        except Exception:
            pass

    match = df_localidades[
        df_localidades["Localidad"].astype(str).str.lower()
        == localidad_detectada.lower()
    ]
    if match.empty:
        match = df_localidades.iloc[[0]]

    row_data = match.iloc[0]

    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")
    folium.Marker(
        [-34.654, -58.619],
        popup="Depósito Morón",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)
    folium.Marker(
        [lat, lon],
        popup=f"Cliente: {direccion_input}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    folium.PolyLine(
        [[-34.654, -58.619], [lat, lon]], color="#38bdf8", weight=4
    ).add_to(m)

    st_folium(m, width=650, height=360)

with col_der:
    st.markdown("##### 📊 Cotización y Horarios Habilitados")

    zona_key = row_data["Zona"]
    franja_match = df_franjas[df_franjas["Zona"] == zona_key]
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
        <div style='font-size: 0.9rem;'>
            <b>💰 Valor de Viaje:</b> ${row_data['Valor de viaje']:,}<br>
            <b>🏷️ Valor Recomendado:</b><br>
            <span class='badge-precio'>${row_data['Valor Recomendado']:,}</span>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem;'>
            <b>📅 Días y Franjas Horarias Habilitadas:</b><br>
            <span style='color:#facc15;'>{franja_txt}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    paquetes = st.number_input(
        "Cantidad de Bultos/Paquetes:", min_value=1, value=1
    )
    if st.button("✅ Confirmar y Agendar Pedido", use_container_width=True):
        st.success(
            f"Pedido agendado para {direccion_input} ({paquetes} bulto/s) -"
            f" Registrado por {vendedor}"
        )
