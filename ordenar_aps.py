import requests

def solicitar_datos():
    print("--- CONSULTOR DE PUNTOS DE ACCESO (GeoAP) ---")
    
    #Selección del usuario de AP
    ap_id = input("Ingrese el ID del AP de referencia: ").strip()
    
    radio_input = input("Radio máximo en metros (deje vacío para sin límite): ").strip()
    radio = float(radio_input) if radio_input else None
    
    limite_input = input("Cantidad límite de resultados (deje vacío para sin límite): ").strip()
    limite = int(limite_input) if limite_input else None

    ejecutar_consulta(ap_id, radio, limite)

def ejecutar_consulta(ap_id, radio, limite):
    url_base = f"http://localhost:8000/aps/{ap_id}"
    
    try:
        #AP referencia
        resp_ref = requests.get(f"{url_base}/location")
        resp_ref.raise_for_status()
        ref = resp_ref.json()
        
        altura_ref = ref.get('altitude_m')
        build_ref = ref.get('building')

        print("\n" + "="*80)
        print(f"AP DE REFERENCIA: {ref.get('ap_code')}")
        print(f"COORDENADAS: Lat: {ref.get('latitude')} | Lon: {ref.get('longitude')} | Alt: {ref.get('altitude_m')}m")
        print(f"Edificio: {ref.get('building')}")
        print("="*80)

        #Parámetros de búsqueda
        params = {}
        if limite: params['limit'] = limite
        if radio: params['max_distance_m'] = radio

        #APs vecinos (según el límite de configuración dado (100 más que suficiente))
        resp_vecinos = requests.get(f"{url_base}/nearest", params=params)
        resp_vecinos.raise_for_status()
        vecinos = resp_vecinos.json()

        vecinos_build = [] #Vecinos en la misma construcción

        for item in vecinos:
            if item.get('building') == build_ref:
                vecinos_build.append(item)
        
        #Orden según el piso en el que se encuentre para considerar adyacencias con respecto al piso de prioridad
        if altura_ref > 6:
            vecinos_build.sort(key=lambda x: x['altitude_m'], reverse=True)
        else:
            vecinos_build.sort(key=lambda x: x['altitude_m'])
        
        vecinos_piso = [] #Vecinos en el mismo piso

        for i in vecinos_build:
            if i.get('altitude_m') == altura_ref:
                vecinos_piso.append(i)
                
        vecinos_build = vecinos_piso + [j for j in vecinos_build if j['altitude_m'] != altura_ref] #Ordenamiento de prioridad

        print(f"\nSe encontraron {len(vecinos_build)} vecinos cercanos en {ref.get('building')}:")
        print(f"{'ID VECINO':<25} | {'DISTANCIA':<12} | {'LATITUD':<12} | {'LONGITUD':<12} | {'ALTITUD'}")
        print("-" * 85)

        for v in vecinos_build:
            #Información individual de los vecinos
            codigo = v.get('ap_code', 'N/A')
            dist = f"{v.get('distance_m', 0):.2f}m"
            lat = v.get('latitude', 'N/A')
            lon = v.get('longitude', 'N/A')
            alt = f"{v.get('altitude_m', 'N/A')}m"
            
            print(f"{codigo:<25} | {dist:<12} | {lat:<12} | {lon:<12} | {alt}")

    except requests.exceptions.HTTPError:
        print(f"\n[Error] No se encontró el AP '{ap_id}'. Verifique el ID.")
    except Exception as e:
        print(f"\n[Error] Ocurrió un problema: {e}")

if __name__ == "__main__":
    solicitar_datos()