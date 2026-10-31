import requests
import geopandas as gpd

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

base = {
    "where": "COD_DPTO=15",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

features, offset, bloque = [], 0, 500  # Cambiado a 500 según la instrucción
vueltas = 0

print("Iniciando descarga paginada (bloques de 500)...")

while True:
    vueltas += 1
    p = {**base, "resultOffset": offset, "resultRecordCount": bloque}
    datos = requests.get(url, params=p, timeout=30).json()
    nuevos = datos.get("features", [])
    features += nuevos
    print(f"Vuelta {vueltas} | offset {offset}: +{len(nuevos)} (total {len(features)})")
    
    if len(nuevos) < bloque:
        break
    offset += bloque

print(f"\nTOTAL RECUPERADO: {len(features)} veredas")

# Convertimos a GeoDataFrame para contar municipios distintos
gdf = gpd.GeoDataFrame.from_features(features, crs=4326)
municipios_unicos = gdf["NOMB_MPIO"].nunique()
print(f"Municipios distintos (NOMB_MPIO): {municipios_unicos}")