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
    </style>
""",
    unsafe_allow_html=True,
)

# ID DE GOOGLE SHEETS
SHEET_ID = "1HSnCjlmmqSG5zSPYNAAAsujwRD4rhZGQf4e_4bGec88"


@st.cache_data(ttl=30)
def cargar_datos_sheets(sheet_id):
    url_loc = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Localidades%20y%20valores"
    url_hor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=HORARIOS"
    df_loc = pd.read_csv(url_loc)
    df_hor = pd.read_csv(url_hor)

    df_loc.columns = [c.strip() for c in df_loc.columns]
    resumen_horarios = df_hor.iloc[5:17, [0, 1]].dropna()
    resumen_horarios.columns = ["Zona", "Días y Franjas Horarias Habilitadas"]

    return df_loc, resumen_horarios


try:
    df_localidades, df_franjas = cargar_datos_sheets(SHEET_ID)
except Exception:
    st.error(
        "⚠️ Error al conectar con Google Sheets. Verificá la clave y permisos."
    )
    st.stop()

if "pedidos_ruta" not in st.session_state:
    st.session_state.pedidos_ruta = []

# DEPÓSITO BASE: TUCUMÁN 1769, CASTELAR
LAT_DEP, LON_DEP = -34.6582, -58.6481


def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


PRIORIDADES = {
    "OESTE": "Martes y Viernes (Prioridad Zona Oeste)",
    "CABA": "Lunes y Miércoles (Prioridad CABA)",
    "NORTE": "Lunes y Jueves (Prioridad Zona Norte)",
    "SUR": "Martes y Miércoles (Prioridad Zona Sur)",
}

# 1. ENCABEZADO Y ATAJOS
col_head1, col_b1, col_b2, col_b3 = st.columns([3.5, 1, 1, 1.2])
with col_head1:
    st.markdown("### 🚚 PORTAL COMERCIAL - SISTEMA SPL")
with col_b1:
    if st.button("📅 Matriz Semanal"):
        st.toast("Matriz de zonificación cargada.")
with col_b2:
    if st.button("📋 Reglas Carga"):
        st.toast("Horario límite: 17:30 hs.")
with col_b3:
    if st.button("🔔 Alertas (2)"):
        st.toast("⚠️ 2 pedidos pendientes en límite.")

# 2. CAPACIDAD SEMANAL
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(
        "<div class='card-dia'><b>LUNES</b><br><small"
        " style='color:#8b949e'>Prioridad Norte / CABA</small><br>📦 10 |"
        " ⏱️ 6.0h<br><span class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        "<div class='card-dia'><b>MARTES</b><br><small"
        " style='color:#8b949e'>Prioridad Oeste / Sur</small><br>📦 18 | ⏱️"
        " 5.8h<br><span class='badge-amarillo'>🟡 PRÓX. CRÍTICO</span></div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        "<div class='card-dia'><b>MIÉRCOLES</b><br><small"
        " style='color:#8b949e'>Prioridad CABA / Sur</small><br>📦 22 | ⏱️"
        " 7.2h<br><span class='badge-rojo'>🔴 CRÍTICO</span></div>",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        "<div class='card-dia'><b>JUEVES</b><br><small"
        " style='color:#8b949e'>Prioridad Norte</small><br>📦 8 | ⏱️"
        " 4.1h<br><span class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        "<div class='card-dia'><b>VIERNES</b><br><small"
        " style='color:#8b949e'>Prioridad Oeste</small><br>📦 12 | ⏱️"
        " 5.0h<br><span class='badge-verde'>🟢 HABILITADO</span></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

col_izq, col_der = st.columns([1.3, 1])

with col_izq:
    st.markdown("##### 🔎 Búsqueda de Dirección con Autocompletado")

    # BUSCADOR PREDICTIVO AUTOCOMPLETADO
    opciones_localidades = (
        df_localidades["Localidad"].dropna().unique().tolist()
    )
    loc_elegida = st.selectbox(
        "1. Escribí o seleccioná la Localidad/Barrio:",
        options=opciones_localidades,
        index=0,
    )

    calle_elegida = st.text_input(
        "2. Calle y Altura exactas:",
        value="Avenida de Mayo 1000",
        placeholder="Ej: Marcelo T. de Alvear 2442",
    )

    direccion_input = f"{calle_elegida}, {loc_elegida}"

    lat_actual, lon_actual = LAT_DEP, LON_DEP

    if direccion_input.strip():
        try:
            geolocator = Nominatim(user_agent="neokings_spl_v13")
            loc_geo = geolocator.geocode(
                f"{direccion_input}, Buenos Aires, Argentina"
            )
            if loc_geo:
                lat_actual, lon_actual = loc_geo.latitude, loc_geo.longitude
        except Exception:
            pass

    match = df_localidades[
        df_localidades["Localidad"].astype(str).str.lower()
        == loc_elegida.lower()
    ]
    row_data = (
        match.iloc[0] if not match.empty else df_localidades.iloc[0]
    )

    # DETERMINACIÓN DINÁMICA DEL PUNTO ANTERIOR DE LA RUTA
    if len(st.session_state.pedidos_ruta) == 0:
        origen_lat, origen_lon = LAT_DEP, LON_DEP
        origen_nombre = "Depósito Castelar"
        num_parada = 1
    else:
        ultimo = st.session_state.pedidos_ruta[-1]
        origen_lat, origen_lon = ultimo["lat"], ultimo["lon"]
        origen_nombre = f"Parada #{len(st.session_state.pedidos_ruta)}"
        num_parada = len(st.session_state.pedidos_ruta) + 1

    dist_tramo = calcular_distancia(
        origen_lat, origen_lon, lat_actual, lon_actual
    )

    # MAPA CON RUTA
    m = folium.Map(
        location=[lat_actual, lon_actual], zoom_start=12, tiles="OpenStreetMap"
    )
    folium.Marker(
        [LAT_DEP, LON_DEP],
        popup="Depósito: Tucumán 1769, Castelar",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(m)

    puntos_trayectoria = [[LAT_DEP, LON_DEP]]
    for idx, ped in enumerate(st.session_state.pedidos_ruta):
        pt = [ped["lat"], ped["lon"]]
        puntos_trayectoria.append(pt)
        folium.Marker(
            pt,
            popup=(
                f"Parada #{idx + 1}: {ped['cliente']} - {ped['direccion']}"
            ),
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    puntos_trayectoria.append([lat_actual, lon_actual])
    folium.Marker(
        [lat_actual, lon_actual],
        popup=f"Actual (#{num_parada}): {direccion_input}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

    folium.PolyLine(
        puntos_trayectoria, color="#38bdf8", weight=4, opacity=0.85
    ).add_to(m)

    st_folium(m, width=680, height=360)

with col_der:
    st.markdown("##### ⚙️ Cotización y Datos del Cliente")

    zona_key = str(row_data["Zona"])
    franja_match = df_franjas[
        df_franjas["Zona"].astype(str).str.upper() == zona_key.upper()
    ]
    franja_txt = (
        franja_match.iloc[0]["Días y Franjas Horarias Habilitadas"]
        if not franja_match.empty
        else "Consulte disponibilidad con logística."
    )
    prioridad_txt = PRIORIDADES.get(
        zona_key, "Según cronograma semanal de zona"
    )

    st.markdown(
        f"""
    <div class='panel-resumen'>
        <div class='badge-zona'>📍 {str(row_data['Localidad']).upper()} ({row_data['Partido']}) — ZONA {row_data['Zona']}</div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <small style='color: #8b949e;'>Valor Sugerido:</small><br>
                <span class='badge-precio'>${row_data['Valor Recomendado']:,}</span>
            </div>
            <div style='text-align: right;'>
                <small style='color: #8b949e;'>Orden de Ruta:</small><br>
                <span style='font-size: 1.1rem; font-weight: bold; color: #58a6ff;'>Parada #{num_parada}</span>
            </div>
        </div>
        <hr style='border-color: #30363d; margin: 10px 0;'>
        <div style='font-size: 0.85rem; line-height: 1.6;'>
            ⭐ <b>Días de Prioridad:</b> <span style='color:#facc15;'>{prioridad_txt}</span><br>
            📏 <b>Distancia del Tramo:</b> +{dist_tramo} km (Desde {origen_nombre})<br>
            📅 <b>Franjas Habilitadas:</b> {franja_txt}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nombre_cliente = st.text_input(
            "👤 Nombre / Comercio del Cliente:",
            value="Zapatería San Martín",
            placeholder="Ej: Juan Pérez",
        )
    with col_c2:
        vendedor_sel = st.selectbox(
            "🏷️ Vendedor Asignado:",
            [
                "Ventas01",
                "Ventas02",
                "Ventas03",
                "Ventas04",
                "Ventas05",
                "Ventas06",
                "Ventas07",
            ],
            index=0,
        )

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        bultos = st.number_input(
            "📦 Cantidad de Bultos:", min_value=1, value=1
        )
    with col_b2:
        dia_agendado = st.selectbox(
            "📅 Día de Entrega:",
            [
                "Lunes (Prioridad Norte)",
                "Martes (Prioridad Oeste)",
                "Miércoles (Prioridad CABA / Sur)",
                "Jueves (Prioridad Norte)",
                "Viernes (Prioridad Oeste)",
            ],
            index=1,
        )

    c_act1, c_act2 = st.columns(2)
    with c_act1:
        if st.button("➕ Agendar CONFIRMADO", use_container_width=True):
            st.session_state.pedidos_ruta.append({
                "parada": num_parada,
                "cliente": nombre_cliente,
                "vendedor": vendedor_sel,
                "direccion": direccion_input,
                "localidad": row_data["Localidad"],
                "zona": row_data["Zona"],
                "precio": row_data["Valor Recomendado"],
                "distancia": dist_tramo,
                "bultos": bultos,
                "dia": dia_agendado,
                "lat": lat_actual,
                "lon": lon_actual,
            })
            st.success(
                f"✅ Parada #{num_parada} ({nombre_cliente}) agendada por"
                f" {vendedor_sel}."
            )
            st.rerun()
    with c_act2:
        if st.button("⏳ Dejar PENDIENTE", use_container_width=True):
            st.warning("⏱️ Guardado en Standby por 2 horas.")

# TABLA EN VIVO EDITABLE PARA LOS VENDEDORES
if len(st.session_state.pedidos_ruta) > 0:
    st.markdown("---")
    st.markdown(
        "##### 📋 Hoja de Ruta Activa (Podés editar directamente en la tabla)"
    )
    df_tabla = pd.DataFrame(st.session_state.pedidos_ruta)[
        [
            "parada",
            "cliente",
            "vendedor",
            "direccion",
            "localidad",
            "zona",
            "precio",
            "distancia",
            "bultos",
            "dia",
        ]
    ]
    df_tabla.columns = [
        "Parada #",
        "Cliente",
        "Vendedor",
        "Dirección",
        "Localidad",
        "Zona",
        "Precio ($)",
        "Dist. Tramo (km)",
        "Bultos",
        "Día Programado",
    ]

    # COMPONENTE EDITABLE INTERACTIVO
    edited_df = st.data_editor(
        df_tabla, use_container_width=True, num_rows="dynamic"
    )
