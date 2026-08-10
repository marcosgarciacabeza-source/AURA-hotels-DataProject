import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE HOTELES Y CANALES
hoteles = [
    {"id": "H-01", "tipo": "Vacacional", "habs": 250, "precio_base": 180, "salas": 2, "regimen": "Pensión Completa"},
    {"id": "H-02", "tipo": "Urbano", "habs": 45, "precio_base": 120, "salas": 1, "regimen": "Flexible"},
    {"id": "H-03", "tipo": "Corporativo", "habs": 180, "precio_base": 110, "salas": 4, "regimen": "Flexible"},
    {"id": "H-04", "tipo": "Montaña", "habs": 60, "precio_base": 140, "salas": 1, "regimen": "Flexible"}
]

canales = [
    {"id": "C-01", "nombre": "Directo Web", "pesos": [0.25, 0.20, 0.15, 0.20]},      # Pesos por hotel (H-01, H-02, H-03, H-04)
    {"id": "C-02", "nombre": "Directo Call Center", "pesos": [0.15, 0.10, 0.05, 0.15]},
    {"id": "C-03", "nombre": "Walk-in", "pesos": [0.02, 0.05, 0.05, 0.05]},
    {"id": "C-04", "nombre": "Booking.com", "pesos": [0.35, 0.45, 0.25, 0.45]},
    {"id": "C-05", "nombre": "Expedia", "pesos": [0.13, 0.15, 0.10, 0.10]},
    {"id": "C-06", "nombre": "Mayorista / B2B", "pesos": [0.10, 0.05, 0.05, 0.05]},
    {"id": "C-07", "nombre": "Corporativo", "pesos": [0.00, 0.00, 0.40, 0.00]}       # Exclusivo o casi del H-03
]

fecha_inicio = datetime(2023, 1, 1)
dias_totales = 365 * 3 # 3 años (aproximado, sin bisiestos estrictos para simplificar)
data = []

np.random.seed(42)

# 2. GENERACIÓN DIARIA
for d in range(dias_totales):
    fecha_actual = fecha_inicio + timedelta(days=d)
    ano = fecha_actual.year
    mes = fecha_actual.month
    dia_semana = fecha_actual.weekday()
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    
    # Condición de apertura para el Hotel 4 (1 de Julio de 2024)
    limite_h4 = datetime(2024, 7, 1)
    
    for idx_h, h in enumerate(hoteles):
        # SI ES EL HOTEL 4 Y ESTAMOS ANTES DE LA FECHA DE APERTURA, SE SALTA
        if h["id"] == "H-04" and fecha_actual < limite_h4:
            continue
            
        # --- LÓGICA DE OCUPACIÓN ---
        ocupacion_pct = 0.60
        if h["tipo"] == "Vacacional" and mes in [6, 7, 8]:
            ocupacion_pct += 0.28
        elif h["tipo"] == "Corporativo" and dia_semana >= 5:
            ocupacion_pct -= 0.35
        elif h["tipo"] == "Montaña" and mes in [12, 1, 2]:
            ocupacion_pct += 0.25
            
        # Añadir un ligero crecimiento anual del mercado general (+2% en 2024, +4% en 2025)
        if ano == 2024: ocupacion_pct += 0.02
        if ano == 2025: ocupacion_pct += 0.04
            
        ocupacion_pct = max(0.12, min(0.96, ocupacion_pct))
        habs_vendidas_totales = int(h["habs"] * ocupacion_pct)
        
        if habs_vendidas_totales == 0:
            continue

        # --- DISTRIBUCIÓN POR CANALES ---
        # Extraemos los pesos específicos de este hotel para repartir las habitaciones
        pesos_canales = [c["pesos"][idx_h] for c in canales]
        pesos_canales = [p / sum(pesos_canales) for p in pesos_canales] # Normalizar pesos
        
        # Asignamos cuántas habitaciones van a cada canal
        habs_por_canal = np.random.multinomial(habs_vendidas_totales, pesos_canales)
        
        for idx_c, habs_canal in enumerate(habs_por_canal):
            if habs_canal == 0:
                continue
                
            id_canal = canales[idx_c]["id"]
            
            # --- DISTRIBUCIÓN POR TIPO DE HABITACIÓN DENTRO DEL CANAL ---
            # Definimos el mix de habitaciones del hotel
            if h["id"] in ["H-01", "H-04"]: # Tienen Suites
                pool_tipos = ["Standard", "Premium", "Suite"]
                prob_tipos = [0.70, 0.20, 0.10]
            else:
                pool_tipos = ["Standard", "Premium"]
                prob_tipos = [0.85, 0.15]
                
            habs_por_tipo = np.random.multinomial(habs_canal, prob_tipos)
            
            for idx_t, cant_habs in enumerate(habs_por_tipo):
                if cant_habs == 0:
                    continue
                    
                tipo_hab = pool_tipos[idx_t]
                
                # Precios dinámicos por tipo y ocupación
                factor_tipo = 1.0 if tipo_hab == "Standard" else (1.4 if tipo_hab == "Premium" else 2.0)
                factor_demanda = 1 + (ocupacion_pct * 0.25)
                
                # El H-01 es más caro porque es Pensión Completa
                precio_habitacion = h["precio_base"] * factor_tipo * factor_demanda
                
                ingreso_alojamiento = cant_habs * precio_habitacion
                costo_alojamiento = ingreso_alojamiento * (0.12 if tipo_hab == "Standard" else 0.18)
                
                # Guardar fila de Alojamiento
                data.append([fecha_str, h["id"], id_canal, "Habitaciones", tipo_hab, cant_habs, round(ingreso_alojamiento, 2), round(costo_alojamiento, 2)])
                
                # --- CARGOS DE DESAYUNO (Excepto H-01 que es Pensión Completa) ---
                if h["regimen"] == "Flexible":
                    # Simulamos que el 60% lo tiene incluido en tarifa y el 20% lo compra suelto. El resto no desayuna.
                    desayunos_incluidos = int(cant_habs * 0.60)
                    desayunos_sueltos = int(cant_habs * 0.20)
                    
                    if desayunos_incluidos > 0:
                        ing_des_inc = desayunos_incluidos * 12.00 # Precio fijo incluido
                        costo_des_inc = ing_des_inc * 0.25 # Coste de materia prima del desayuno (25%)
                        data.append([fecha_str, h["id"], id_canal, "F&B", "Desayuno Incluido", desayunos_incluidos, round(ing_des_inc, 2), round(costo_des_inc, 2)])
                        
                    if desayunos_sueltos > 0:
                        ing_des_sue = desayunos_sueltos * 18.00 # Más caro si es suelto
                        costo_des_sue = ing_des_sue * 0.25
                        data.append([fecha_str, h["id"], id_canal, "F&B", "Desayuno Suelto", desayunos_sueltos, round(ing_des_sue, 2), round(costo_des_sue, 2)])

        # --- CARGOS DE F&B A LA CARTA / RESTAURANTE (Excepto H-01) ---
        if h["regimen"] == "Flexible":
            gasto_fb_base = 40 if dia_semana in [4, 5] else 25
            ingreso_fb = habs_vendidas_totales * gasto_fb_base * np.random.uniform(0.75, 1.25)
            costo_fb = ingreso_fb * np.random.uniform(0.32, 0.36) # Alrededor del 34% de Food Cost
            num_tickets = int(habs_vendidas_totales * np.random.uniform(0.8, 1.8))
            
            # El F&B general lo asignamos al canal directo o mayoritario del día para simplificar
            data.append([fecha_str, h["id"], "C-01", "F&B", "Restaurante A la Carta", num_tickets, round(ingreso_fb, 2), round(costo_fb, 2)])

        # --- CARGOS DE MICE / SALAS DE EVENTOS ---
        # Limitado por el número máximo de salas de cada hotel
        if h["salas"] > 0 and dia_semana < 5 and np.random.rand() > 0.6:
            salas_ocupadas = np.random.randint(1, h["salas"] + 1)
            for s in range(salas_ocupadas):
                ingreso_sala = np.random.choice([1000, 2200, 4500])
                costo_sala = ingreso_sala * np.random.uniform(0.07, 0.12)
                data.append([fecha_str, h["id"], "C-07" if h["id"]=="H-03" else "C-01", "MICE", "Alquiler de Salas", 1, round(ingreso_sala, 2), round(costo_sala, 2)])

# 3. EXPORTACIÓN A CSV
df = pd.DataFrame(data, columns=["Fecha", "ID_Hotel", "ID_Canal", "Departamento", "Concepto", "Numero_Cargos", "Ingreso_Total", "Costo_Directo"])
df.to_csv("Fact_Cargos_Diarios_PRO.csv", index=False)
print(f"¡Dataset espectacular generado con éxito! Total de filas: {len(df)}")