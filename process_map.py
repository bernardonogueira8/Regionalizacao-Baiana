import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape

def carregar_geojson_seguro(caminho_arquivo):
    """Carrega um GeoJSON e converte seus dados para GeoDataFrame."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = []
    for feat in data['features']:
        properties = feat['properties']
        # Converte a geometria para Shapely.
        geom = shape(feat['geometry'])
        properties['geometry'] = geom
        features.append(properties)
        
    return gpd.GeoDataFrame(features, geometry='geometry')

def criar_mapa_e_geojson(gdf_in, coluna_agrupamento, nome_arquivo_base, paleta_cores='Set3'):
    """Agrupa os municípios e exporta o GeoJSON e a prévia em SVG."""
    print(f"\nProcessando {coluna_agrupamento}...")

    gdf_dissolvido = gdf_in.dissolve(by=coluna_agrupamento, as_index=False)

    nome_arquivo_geojson = f"src/{nome_arquivo_base}.geojson"
    gdf_dissolvido.to_file(nome_arquivo_geojson, driver="GeoJSON")
    print(f"GeoJSON salvo: {nome_arquivo_geojson}")

    gdf_dissolvido['centroid'] = gdf_dissolvido.geometry.centroid
    
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='white')
    gdf_dissolvido.plot(
        ax=ax, 
        column=coluna_agrupamento, 
        cmap=paleta_cores, 
        edgecolor='white', 
        linewidth=1.0,
        alpha=0.9
    )
    
    # Adiciona o rótulo de cada região.
    for idx, row in gdf_dissolvido.iterrows():
        centroid = row['centroid']
        texto_rotulo = str(row[coluna_agrupamento])
        ax.text(
            centroid.x, centroid.y, texto_rotulo, 
            fontsize=8, 
            fontweight='bold', 
            ha='center', 
            va='center',
            color='#333333',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3', lw=0)
        )
        
    ax.axis("off")
    plt.tight_layout()
    caminho_preview = f"src/{nome_arquivo_base}_preview.svg"
    plt.savefig(caminho_preview, format="svg", bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Prévia salva: {caminho_preview}")


if __name__ == "__main__":
    caminho_geojson = 'data/BA_Municipios_2022.json'
    caminho_excel = 'data/municipios_completo.xlsx'
    
    print("Carregando dados...")
    gdf = carregar_geojson_seguro(caminho_geojson)
    df_map = pd.read_excel(caminho_excel)
    
    gdf['CD_MUN'] = gdf['CD_MUN'].astype(str)
    df_map['Cod. IBGE'] = df_map['Cod. IBGE'].astype(str)
    
    print("Associando municípios às regiões...")
    gdf_merged = gdf.merge(df_map, left_on='CD_MUN', right_on='Cod. IBGE', how='inner')
    
    print(f"Municípios associados: {gdf_merged.shape[0]}")

    criar_mapa_e_geojson(gdf_merged, 'NRS', 'mapa_macrorregioes', paleta_cores='Pastel1')
    criar_mapa_e_geojson(gdf_merged, 'BRS', 'mapa_Regioes_Saude', paleta_cores='Pastel2')

    print("\nProcessamento concluído.")
    print("Para converter no Mapshaper, use:")
    print("-proj EPSG:3857 -o mapa_macrorregioes.svg format=svg id-field=NRS")
    print("-proj EPSG:3857 -o mapa_Regioes_Saude.svg format=svg id-field=BRS")