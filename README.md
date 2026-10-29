# Desenho Territorial e Regionalização da Saúde - Bahia 🗺️

Este projeto contém a estrutura de dados, o mapeamento relacional e os scripts voltados para a geração, união e estilização de mapas vetoriais (SVG/GeoJSON) baseados na divisão de **Macrorregiões e Regiões de Saúde** do estado da Bahia.

## 🚀 Sobre o Projeto

O objetivo principal deste projeto é automatizar o cruzamento de dados geográficos municipais com as normativas de agrupamento regional da Secretaria da Saúde do Estado da Bahia (Sesab). 

O desenho territorial em vigor baseia-se no **Plano Diretor de Regionalização (PDR 2007)**, aprovado pela Resolução CIB/BA nº 132/2007 e ajustado pela Resolução CIB/BA nº 057/2008. Atualmente, a conformação territorial permanece vigente nos termos do **Decreto Estadual nº 22.916, de 10 de julho de 2024**. 

O desenho territorial consolidado divide o estado da Bahia em **09 Macrorregiões** e **28 Regiões de Saúde** (anteriormente denominadas microrregiões).

## Fontes dos dados
- **Malha municipal:** `data/BA_Municipios_2022.json`, obtida no Instituto Brasileiro de Geografia e Estatística (IBGE). Fornece os limites e códigos dos municípios usados no mapa.
- **Regionalização:** `data/municipios_completo.xlsx`, planilha de relacionamento elaborada neste projeto com base na `docs/Cartilha_PDR_2026.pdf`. Ela associa os códigos IBGE dos municípios às regiões usadas no processamento, incluindo as colunas `NRS` e `BRS`.

O script cruza a malha do IBGE com a planilha pela correspondência entre `CD_MUN` e `Cod. IBGE`. A planilha representa a organização dos dados deste projeto; a cartilha é a referência utilizada para sua elaboração.

## Estrutura do projeto

```text
data/
  BA_Municipios_2022.json
  municipios_completo.xlsx
docs/
  Cartilha_PDR_2026.pdf
src/
  arquivos GeoJSON e prévias SVG gerados
process_map.py
```

## 🔄 Transição Administrativa: Das DIRES para as CIR

Visando fortalecer a descentralização administrativa do Estado, o desenho territorial passou por importantes adequações normativas e de gestão:

* **Compatibilização das DIRES:** Os municípios pertencentes às antigas Diretorias Regionais de Saúde (DIRES) foram compatibilizados com as microrregiões de saúde. Algumas microrregiões (como Brumado e Feira de Santana) ficaram com mais de uma DIRES em seu território, enquanto outras, como Camaçari, passaram a ser atendidas pela mesma DIRES de Salvador.
* **Decreto Presidencial nº 7.508:** Sob a vigência deste decreto nacional, as antigas "microrregiões" passaram a ser oficialmente denominadas **Regiões de Saúde (RS)**.
* **Comissões Intergestores Regionais (CIR):** A Resolução CIB/BA nº 275/2012 instituiu as CIRs em substituição aos antigos Colegiados de Gestão Microrregionais (CGMR), consolidando uma nova etapa da governança regional de saúde.

---

## 🛠️ Tecnologias e Como Utilizar

* **Linguagem/Ferramentas:** Python, GeoPandas, Pandas, Matplotlib, Shapely e Mapshaper.
* **Arquivos de Entrada:** Ficheiro GeoJSON/JSON com a malha municipal da Bahia e um CSV com a base relacional do PDR 2007.

### Gerar os mapas

```bash
pip install geopandas pandas matplotlib shapely openpyxl
```

Na pasta raiz do projeto, execute:

```bash
python process_map.py
```
O script salva em `src/`:

- `mapa_macrorregioes.geojson` e `mapa_macrorregioes_preview.svg`, agrupados pela coluna `NRS`;
- `mapa_Regioes_Saude.geojson` e `mapa_Regioes_Saude_preview.svg`, agrupados pela coluna `BRS`.


As prévias SVG são geradas pelo Matplotlib. Os GeoJSON podem ser convertidos em SVG no [Mapshaper](https://mapshaper.org/). Carregue o GeoJSON correspondente e execute:

```text
-proj EPSG:3857 -o mapa_macrorregioes.svg format=svg id-field=NRS
-proj EPSG:3857 -o mapa_Regioes_Saude.svg format=svg id-field=BRS
```

> **Observação:** Os arquivos em `dist/` já estão tratados e simplificados para melhorar o desempenho e a resposta dos mapas no Power BI.