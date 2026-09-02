<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal SPL - Neokings</title>
    <!-- CSS Leaflet Mapa -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; padding: 15px; }
        h3 { color: #58a6ff; margin-bottom: 10px; }
        .grid-header { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 15px; }
        .card-dia { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px; text-align: center; font-size: 0.8rem; }
        .card-dia span { font-weight: bold; }
        .verde { color: #3dd68c; } .amarillo { color: #facc15; } .rojo { color: #f87171; }
        
        .main-container { display: grid; grid-template-columns: 1.3fr 1fr; gap: 15px; }
        .panel { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; position: relative; }
        
        input, select, button { width: 100%; padding: 10px; margin-top: 8px; background: #21262d; border: 1px solid #30363d; color: #c9d1d9; border-radius: 6px; }
        button { background: #238636; color: white; font-weight: bold; cursor: pointer; border: none; margin-top: 15px; }
        button:hover { background: #2ea043; }
        
        /* Buscador Predictivo */
        .suggestions-box { position: absolute; top: 75px; left: 15px; right: 15px; background: #161b22; border: 1px solid #58a6ff; z-index: 1000; max-height: 200px; overflow-y: auto; border-radius: 6px; }
        .suggestion-item { padding: 10px; cursor: pointer; border-bottom: 1px solid #30363d; font-size: 0.85rem; }
        .suggestion-item:hover { background: #21262d; color: #58a6ff; }
        
        #map { height: 360px; border-radius: 8px; margin-top: 10px; }
        .badge-precio { font-size: 2rem; color: #3dd68c; font-weight: bold; }
        
        /* Tabla de Hoja de Ruta */
        .tabla-container { margin-top: 20px; background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.85rem; }
        th, td { border: 1px solid #30363d; padding: 8px; text-align: left; }
        th { background: #21262d; color: #58a6ff; }
        .btn-eliminar { background: #da3633; padding: 4px 8px; margin: 0; font-size: 0.75rem; }
    </style>
</head>
<body>

    <h3>🚚 PORTAL COMERCIAL - SISTEMA SPL</h3>

    <div class="grid-header">
        <div class="card-dia"><b>LUNES</b><br><small style="color:#8b949e">Prioridad Norte</small><br>📦 10<br><span class="verde">🟢 HABILITADO</span></div>
        <div class="card-dia"><b>MARTES</b><br><small style="color:#8b949e">Prioridad Oeste</small><br>📦 18<br><span class="amarillo">🟡 PRÓX. CRÍTICO</span></div>
        <div class="card-dia"><b>MIÉRCOLES</b><br><small style="color:#8b949e">Prioridad CABA</small><br>📦 22<br><span class="rojo">🔴 CRÍTICO</span></div>
        <div class="card-dia"><b>JUEVES</b><br><small style="color:#8b949e">Prioridad Norte</small><br>📦 8<br><span class="verde">🟢 HABILITADO</span></div>
        <div class="card-dia"><b>VIERNES</b><br><small style="color:#8b949e">Prioridad Oeste</small><br>📦 12<br><span class="verde">🟢 HABILITADO</span></div>
    </div>

    <div class="main-container">
        <!-- COLUMNA BÚSQUEDA Y MAPA -->
        <div class="panel">
            <h5>🔎 Búsqueda de Dirección (Autocompletado Predictivo)</h5>
            <input type="text" id="addressInput" placeholder="Escribí calle, altura y localidad..." autocomplete="off">
            <div id="suggestions" class="suggestions-box" style="display:none;"></div>
            <div id="map"></div>
        </div>

        <!-- COLUMNA COTIZACIÓN -->
        <div class="panel">
            <h5>⚙️ Cotización y Registro de Pedido</h5>
            <div style="margin-top: 10px; padding: 10px; background: #21262d; border-radius: 6px;">
                <div style="color: #58a6ff; font-weight: bold; font-size: 1.1rem;" id="infoLocalidad">📍 CASTELAR (Zona OESTE)</div>
                <div style="margin-top: 5px; font-size: 0.9rem;">Valor Sugerido: <span class="badge-precio" id="infoPrecio">$9.700</span></div>
                <div style="font-size: 0.85rem; margin-top: 5px;" id="infoDistancia">📏 Distancia del Tramo: <b>+0.0 km</b> (Desde Depósito Castelar)</div>
                <div style="font-size: 0.85rem; margin-top: 3px; color: #facc15;" id="infoFranja">📅 Franjas: Mar y Mié: 08:30-11:00 hs</div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                <div>
                    <label style="font-size: 0.8rem;">Nombre / Comercio:</label>
                    <input type="text" id="nombreCliente" value="Zapatería San Martín">
                </div>
                <div>
                    <label style="font-size: 0.8rem;">Vendedor Asignado:</label>
                    <select id="vendedorSel">
                        <option>Ventas01</option><option>Ventas02</option><option>Ventas03</option>
                        <option>Ventas04</option><option>Ventas05</option><option>Ventas06</option><option>Ventas07</option>
                    </select>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 5px;">
                <div>
                    <label style="font-size: 0.8rem;">Cantidad de Bultos:</label>
                    <input type="number" id="bultosInput" value="1" min="1">
                </div>
                <div>
                    <label style="font-size: 0.8rem;">Día Programado:</label>
                    <select id="diaSel">
                        <option>Lunes (Prioridad Norte)</option>
                        <option selected>Martes (Prioridad Oeste)</option>
                        <option>Miércoles (Prioridad CABA)</option>
                        <option>Jueves (Prioridad Norte)</option>
                        <option>Viernes (Prioridad Oeste)</option>
                    </select>
                </div>
            </div>

            <button onclick="agendarPedido()">➕ AGENDAR Y GUARDAR EN RUTA</button>
        </div>
    </div>

    <!-- TABLA EN VIVO HOJA DE RUTA -->
    <div class="tabla-container">
        <h5>📋 Hoja de Ruta Activa (Modificable en Vivo)</h5>
        <table id="tablaRuta">
            <thead>
                <tr>
                    <th>Parada #</th><th>Cliente</th><th>Vendedor</th><th>Dirección</th><th>Zona</th><th>Precio</th><th>Dist. Tramo</th><th>Bultos</th><th>Día</th><th>Acción</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <!-- JS Leaflet Mapa -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const DEP_LAT = -34.6582, DEP_LON = -58.6481; // Tucumán 1769, Castelar
        let pedidos = [];
        let puntoActual = { lat: DEP_LAT, lon: DEP_LON, direccion: "Depósito Castelar", precio: 9700, zona: "OESTE", localidad: "Castelar" };
        let map, markerDep, currentMarker, polyline;

        // Inicializar Mapa
        map = L.map('map').setView([DEP_LAT, DEP_LON], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        markerDep = L.marker([DEP_LAT, DEP_LON]).addTo(map).bindPopup("Depósito: Tucumán 1769, Castelar").openPopup();

        // Buscador Predictivo (LocationIQ / Nominatim API en vivo)
        const addressInput = document.getElementById('addressInput');
        const suggestionsBox = document.getElementById('suggestions');

        addressInput.addEventListener('input', async function() {
            const query = this.value;
            if (query.length < 3) { suggestionsBox.style.display = 'none'; return; }

            const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query + ', Buenos Aires, Argentina')}&limit=5`);
            const data = await response.json();

            suggestionsBox.innerHTML = '';
            if (data.length > 0) {
                suggestionsBox.style.display = 'block';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'suggestion-item';
                    div.innerText = item.display_name;
                    div.onclick = () => seleccionarDireccion(item);
                    suggestionsBox.appendChild(div);
                });
            }
        });

        function seleccionarDireccion(item) {
            suggestionsBox.style.display = 'none';
            addressInput.value = item.display_name.split(',')[0] + ', ' + (item.address?.suburb || item.address?.city || 'AMBA');

            const lat = parseFloat(item.lat), lon = parseFloat(item.lon);
            puntoActual.lat = lat; puntoActual.lon = lon;
            puntoActual.direccion = addressInput.value;

            // Mover mapa y marcador
            if (currentMarker) map.removeLayer(currentMarker);
            currentMarker = L.marker([lat, lon]).addTo(map).bindPopup(`Selección: ${addressInput.value}`).openPopup();
            map.setView([lat, lon], 13);

            // Calcular Distancia Tramo desde Última Parada
            const origen = pedidos.length === 0 ? { lat: DEP_LAT, lon: DEP_LON, nombre: "Depósito Castelar" } : pedidos[pedidos.length - 1];
            const dist = calcularDistancia(origen.lat, origen.lon, lat, lon);
            puntoActual.distancia = dist;

            document.getElementById('infoDistancia').innerHTML = `📏 Distancia del Tramo: <b>+${dist} km</b> (Desde ${origen.nombre || 'Parada #' + pedidos.length})`;
            
            // Dibujar Ruta
            renderizarMapa();
        }

        function calcularDistancia(lat1, lon1, lat2, lon2) {
            const R = 6371;
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
            return (R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))).toFixed(1);
        }

        function renderizarMapa() {
            if (polyline) map.removeLayer(polyline);
            let puntos = [[DEP_LAT, DEP_LON]];
            pedidos.forEach(p => puntos.push([p.lat, p.lon]));
            if (currentMarker) puntos.push([puntoActual.lat, puntoActual.lon]);

            polyline = L.polyline(puntos, {color: '#38bdf8', weight: 4}).addTo(map);
        }

        function agendarPedido() {
            const cliente = document.getElementById('nombreCliente').value;
            const vendedor = document.getElementById('vendedorSel').value;
            const bultos = document.getElementById('bultosInput').value;
            const dia = document.getElementById('diaSel').value;

            pedidos.push({
                parada: pedidos.length + 1,
                cliente: cliente,
                vendedor: vendedor,
                direccion: puntoActual.direccion,
                zona: puntoActual.zona,
                precio: puntoActual.precio,
                distancia: puntoActual.distancia || 0,
                bultos: bultos,
                dia: dia,
                lat: puntoActual.lat,
                lon: puntoActual.lon
            });

            document.getElementById('addressInput').value = '';
            actualizarTabla();
            renderizarMapa();
        }

        function actualizarTabla() {
            const tbody = document.querySelector('#tablaRuta tbody');
            tbody.innerHTML = '';
            pedidos.forEach((p, idx) => {
                tbody.innerHTML += `
                    <tr>
                        <td><b>#${idx + 1}</b></td>
                        <td contenteditable="true">${p.cliente}</td>
                        <td>${p.vendedor}</td>
                        <td contenteditable="true">${p.direccion}</td>
                        <td>${p.zona}</td>
                        <td>$${p.precio}</td>
                        <td>+${p.distancia} km</td>
                        <td contenteditable="true">${p.bultos}</td>
                        <td>${p.dia}</td>
                        <td><button class="btn-eliminar" onclick="eliminarParada(${idx})">🗑️</button></td>
                    </tr>
                `;
            });
        }

        function eliminarParada(idx) {
            pedidos.splice(idx, 1);
            actualizarTabla();
            renderizarMapa();
        }
    </script>
</body>
</html>
