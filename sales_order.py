# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import streamlit as st

st.markdown("# Análisis de ventas")
st.markdown("## Tienda Electron Tec (online-store)")
st.markdown("---")
#

st.markdown(

    "Una persona que lleva vendiendo durante un año en diferentes sitios de venta on-line nos ha pedido estudiar y evaluar los datos que ha, inteligentemente, recolectado durante este año de ventas. Esta persona no sabe que provecho puede sacarle a esta información, por lo que nosotros vamos a ayudarlo y explicaremos el proceso."

)
#
st.markdown(

    "Los datos que nos entregó fue un archivo ___.CSV___, el cual contiene información de cada una de sus ventas realizadas durante el periodo mencionado, este archivo es una suma de los reportes que les da cada uno de los sitios en el cual él publica sus productos. Visualizando la información apreciamos la siguiente información:"

)
st.markdown("- Fecha de la venta")
st.markdown("- ID de la venta")
st.markdown("- Producto's")
st.markdown("- Sitio de Venta")
st.markdown("- Donde fue enviado el pedido")
st.markdown("- Cantidad (producto)")
st.markdown("- Precio de cada producto")
st.markdown("- Costo de venta (comisión que es igual en todos los sitios)")
st.markdown("- El total de la venta sumando todos los productos")
st.markdown("- Margen (la diferencia entre el Total venta y Costo de venta)")
#
#

st.markdown("## Librerías que utilizaremos")
st.markdown("- pandas")
st.markdown("- numpy")
st.markdown("- cufflinks")
st.markdown("- plotly")
st.markdown("- folium")
st.markdown("- scipy")

# ## verificamos la informacion obtenida

# + jupyter={"source_hidden": true}
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import cufflinks as cf
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
import warnings
from scipy import stats

warnings.simplefilter(action="ignore", category=FutureWarning)
# %matplotlib inline
# Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

from plotly.subplots import make_subplots

# Use Plotly locally
cf.go_offline()

# + jupyter={"source_hidden": true}
df = pd.read_csv("sales_data.csv")
df_company = (
    df.drop(["Product_ean"], axis=1)
    .rename(columns={"catégorie": "Category"})
    .round({"Cost price": 2, "margin": 2})
)

df_company.head()

# + jupyter={"source_hidden": true}
df_company.info()
# -

st.markdown(

    "_El DataFrame está en buen estado, son 10 columnas en las cuales no se encuentra ningún valor nulo, en ninguna de sus 185.950 transacciones registrdas_."

)
st.markdown("")
st.markdown("# Gráficos y análisis")
st.markdown("## Gráficos de barras")
st.markdown(

    "Vamos a crear una nueva tabla con las columnas _Product_ y _Order ID_, haciendo referencia al mismo nombre que tienen en la tabla original, luego vamos a agrupar valores duplicados en la columna _Product_ obteniendo una tabla con la cantidad de veces que se ha realizado un pedido con el producto indicado."

)

# + jupyter={"source_hidden": true}
df_products = (
    df_company[["Product", "Order ID"]]
    .groupby(["Product"])
    .nunique()
    .sort_values(by=["Order ID"], ascending=False)
    .reset_index(drop=False)
)
df_products

# + jupyter={"source_hidden": true}
fig = px.bar(
    df_products,
    x="Product",
    y="Order ID",
    title="Productos / Total de pedidos",
    labels={"Order ID": "Total de pedidos", "Product": "Producto"},
    height=700,
    text="Order ID",
)
fig.update_traces(
    textfont_size=8,
    textposition="inside",
    textfont_color="white",
    texttemplate="%{y:,.2r}",
    marker_color="LightSeaGreen",
    marker_line_color="black",
    marker_line_width=1,
    width=0.85,
)
fig.update_layout(xaxis_tickangle=-90, plot_bgcolor="white")
st.plotly_chart(fig)
# -

st.markdown("---")
st.markdown(">El cliente vende un total de **19** productos distintos")

# + jupyter={"source_hidden": true}
df_products_2 = (
    df_company[["Product", "Order ID"]]
    .groupby(["Product"])
    .nunique()
    .sort_values(by=["Order ID"], ascending=False)
    .iloc[:3]
    .reset_index(drop=False)
)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df_products_2["Order ID"],
        y=df_products_2["Product"],
        name="Tres mas vendidos",
        marker_color="LightSeaGreen",
        orientation="h",
    )
)
fig.update_traces(
    textfont_size=8,
    textposition="inside",
    textfont_color="white",
    texttemplate="%{x:,.2r}",
    marker_color="LightSeaGreen",
    marker_line_color="black",
    marker_line_width=1,
    width=0.85,
)
fig.update_layout(
    template="plotly_white", plot_bgcolor="white", title="Tres mas vendidos"
)
st.plotly_chart(fig)

# + jupyter={"source_hidden": true}
df_products_3 = (
    df_company[["Product", "Order ID"]]
    .groupby(["Product"])
    .nunique()
    .sort_values(by=["Order ID"], ascending=True)
    .iloc[:3]
    .reset_index(drop=False)
)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df_products_3["Order ID"],
        y=df_products_3["Product"],
        name="Three best products by orders",
        marker_color="LightSeaGreen",
        orientation="h",
    )
)
fig.update_traces(
    textfont_size=8,
    textposition="inside",
    textfont_color="white",
    texttemplate="%{x:,.2r}",
    marker_color="LightSeaGreen",
    marker_line_color="black",
    marker_line_width=1,
    width=0.85,
)
fig.update_layout(
    template="plotly_white", plot_bgcolor="white", title="Tres menos vendidos"
)
st.plotly_chart(fig)

# + jupyter={"source_hidden": true}
df_product_margin = (
    df_company.groupby(["Product"])["margin"]
    .sum()
    .sort_values(ascending=False)
    .iloc[:3]
    .reset_index(drop=False)
)
df_product_margin

# + jupyter={"source_hidden": true}
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df_product_margin["margin"],
        y=df_product_margin["Product"],
        name="Three best products by orders",
        marker_color="LightSeaGreen",
        orientation="h",
    )
)
fig.update_traces(
    textfont_size=8,
    textposition="inside",
    textfont_color="white",
    texttemplate="%{x:,.2r}",
    marker_color="LightSeaGreen",
    marker_line_color="black",
    marker_line_width=1,
    width=0.85,
)
fig.update_layout(
    template="plotly_white",
    plot_bgcolor="white",
    title="Tres productos con mejor margin",
)
st.plotly_chart(fig)

# + jupyter={"source_hidden": true}
df_product_margin = (
    df_company.groupby(["Product"])["margin"]
    .sum()
    .sort_values(ascending=True)
    .iloc[:3]
    .reset_index(drop=False)
)
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df_product_margin["margin"],
        y=df_product_margin["Product"],
        name="Three best products by orders",
        marker_color="LightSeaGreen",
        orientation="h",
    )
)
fig.update_traces(
    textfont_size=8,
    textposition="inside",
    textfont_color="white",
    texttemplate="%{x:,.2r}",
    marker_color="LightSeaGreen",
    marker_line_color="black",
    marker_line_width=1,
    width=0.85,
)
fig.update_layout(
    template="plotly_white",
    plot_bgcolor="white",
    title="Tres productos con peor margin",
)
st.plotly_chart(fig)
# -

#
st.markdown("Tres productos que han dejado menor margen:")
st.markdown("1. AAA Batteries(4-pack)")
st.markdown("2. AA Batteries(4-pack)")
st.markdown("3. Wired Headphones")

st.markdown(

    "Ahora agrupamos por `Category` y `Product` mas una nueva columna con un **count** de la columna `Product`"

)
st.markdown(

    "Así obtendremos un gráfico que muestra el margen de cada producto y en que tienda se vendió."

)

# + jupyter={"source_hidden": true}
df_product_cat = df_company[["Product", "Category"]].reset_index(drop=True).iloc[:20000]
df_product_cat["product_count"] = df_product_cat.groupby(["Category", "Product"])[
    "Product"
].transform("count")
print(df_product_cat)

# + jupyter={"source_hidden": true}
fig = px.bar(
    df_product_cat,
    x="Product",
    y="product_count",
    color="Category",
    title="Graph",
    height=800,
    color_discrete_sequence=px.colors.qualitative.Dark24,
)
fig.update_traces(marker_line_width=0.8, marker={"opacity": 1})
fig.update_layout(xaxis_tickangle=-90, plot_bgcolor="white")
st.plotly_chart(fig)
# -

st.markdown("## Gráficos circulares")
st.markdown(

    "Si nos fijamos en la tabla original, vemos que la columna `Purchase Address` es un valor del tipo **str**, con el cual podemos trabajar y obtener aun más información."

)
st.markdown(

    "Por ejemplo, si separamos este valor del tipo **str** con base en el valor `,`, obtendremos una lista de 3 datos del tipo **str**:"

)
st.markdown(
    " **['944 Walnut St' , 'Boston' , 'MA 02215']** tomando como referencia una dirección existente en la tabla de manera aleatoria."

)
#

st.markdown(

    "Con esto podemos consultar la lista en la columna y obtener, por ejemplo, la **ciudad**."

)
st.markdown(

    "Uniendo esto y sumando la columna `Margin`, podemos conocer el margen obtenido por cada ciudad donde se encargó el producto."

)

# + jupyter={"source_hidden": true}
df_address = (
    df_company.groupby(["Purchase Address"])["margin"].sum().reset_index(drop=False)
)
city = df_address["Purchase Address"].str.split(pat=",", expand=True).copy()
city_df = (
    pd.DataFrame({"City": city[1], "Margin": df_address.margin})
    .groupby(["City"])
    .agg({"Margin": "sum", "City": lambda s: s.unique().tolist()})
    .drop(["City"], axis=1)
    .reset_index(drop=False)
)

city_df

# + jupyter={"source_hidden": true}
fig = px.pie(city_df, values="Margin", names="City", title="Ciudades / Margen (%)")
fig.update_traces(
    hoverinfo="label+percent",
    textfont_size=10,
    textinfo="label+percent",
    textposition="outside",
    marker=dict(line=dict(color="#FFFFFF", width=1)),
)
# -

st.markdown("---")
st.markdown(
    " Cantidad porcentual que tiene cada ciudad con respecto al total del margen obtenido durante el periodo"

)
st.markdown(

    "Siguiendo la metodología anterior, obtenemos el margen de cada estado, ayudándonos de una tabla _transitoria_ para poder volver a separar el valor **str** pero esta vez con base en ` ` espacio."

)

# + jupyter={"source_hidden": true}
transitoria = (
    pd.DataFrame({"State": city[2], "Margin": df_address.margin})
    .groupby(["State"])
    .agg({"Margin": "sum", "State": lambda s: s.unique()})
    .drop(["State"], axis=1)
    .reset_index(drop=False)
)

transitoria

# + jupyter={"source_hidden": true}
state = transitoria["State"].str.split(pat=" ", expand=True)
state_df = (
    pd.DataFrame({"State": state[1], "Margin": transitoria["Margin"]})
    .groupby(["State"])
    .agg({"Margin": "sum", "State": lambda s: s.unique().tolist()})
    .drop(["State"], axis=1)
    .reset_index(drop=False)
)


state_df

# + jupyter={"source_hidden": true}
fig = px.pie(
    state_df, values="Margin", names="State", title="States total % of margins"
)
fig.update_traces(
    hoverinfo="label+percent",
    textfont_size=10,
    textinfo="label+percent",
    textposition="outside",
    marker=dict(line=dict(color="#FFFFFF", width=1)),
)

# + jupyter={"source_hidden": true}
cities = (
    city_df.sort_values(by=["Margin"], ascending=False).iloc[:3].reset_index(drop=False)
)

fig = px.pie(
    cities, values="Margin", names="City", title="Three cities with most margin"
)
fig.update_traces(
    hoverinfo="label+percent",
    textfont_size=10,
    textinfo="label+percent",
    textposition="outside",
    marker=dict(line=dict(color="#FFFFFF", width=1)),
)

# + jupyter={"source_hidden": true}
cities2 = (
    city_df.sort_values(by=["Margin"], ascending=True).iloc[:3].reset_index(drop=False)
)

fig = px.pie(
    cities2, values="Margin", names="City", title="Three cities with less margin"
)
fig.update_traces(
    hoverinfo="label+percent",
    textfont_size=10,
    textinfo="label+percent",
    textposition="outside",
    marker=dict(line=dict(color="#FFFFFF", width=1)),
)
# -

st.markdown("## Gráficos de Línea y Línea/Barra")

st.markdown(

    "Podemos hacer un gráfico de líneas agrupando por periodos de tiempo, de esta manera podremos analizar el comportamiento, respecto de sus ingresos, de venta del cliente."

)

# + jupyter={"source_hidden": true}
df_date_margin = df_company[["Order Date", "Cost price", "margin"]].copy()
df_date_margin.groupby(["Order Date"]).sum().sort_values(["margin"], ascending=False)
# -

st.markdown(
    "- Aqui realizamos una agrupacion en un rango de fechas, en este caso, un rango **semanal**"
)

# + jupyter={"source_hidden": true}
df_co = df_company.reset_index(drop=True).sort_values(["margin"], ascending=True).copy()
df_co.index.name = "id"
df_co["Order Date"] = pd.to_datetime(df_co["Order Date"])

df_dates = df_co[["Order Date", "Cost price", "margin"]].copy()
df_dates_grouped = df_dates.groupby(pd.Grouper(key="Order Date", freq="w"))

week = (
    df_dates_grouped.mean()
    .sort_values(["Order Date"], ascending=True)
    .reset_index(drop=False)
)
week

# + jupyter={"source_hidden": true}
fig = px.line(
    week,
    x="Order Date",
    y="margin",
    title="Ventas semanales por margen",
    labels={"Order Date": "Semanas", "margin": "Margen"},
    markers=True,
)

fig.update_layout(xaxis_tickangle=-90, plot_bgcolor="white")
st.plotly_chart(fig)

# + jupyter={"source_hidden": true}
import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=week["Order Date"],
        y=week["margin"],
        name="",
        marker_color="MediumPurple",
    )
)

fig.add_trace(
    go.Bar(
        x=week["Order Date"],
        y=week["margin"],
        name="Margin",
        marker_color="LightSeaGreen",
        opacity=0.8,
    )
)
fig.update_layout(title_text="Sales in time (weeks) by margin", showlegend=False)

st.plotly_chart(fig)
# -

st.markdown("## Visualización en mapas")
st.markdown(

    "Con la ayuda de la librería **Folium** vamos a mostrar el lugar geográfico donde las compras fueron realizadas."

)
st.markdown(

    "Tendremos que trabajar con alguna otra fuente de información que contenga las coordenadas geográficas de los estados y ciudades de USA. Adicionalmente vamos a elegir un dato como `weigth` para poder hacer un **Heatmap**, con esta información sabremos en qué lugar de Estados unidos se concentran la mayor cantidad de **_clientes_** y determinar la _posible mejor ubicacion_ para una tienda física."

)
st.markdown("1. Tabla con las coordenadas de las ciudades y estados de USA")

# + jupyter={"source_hidden": true}
df_us = pd.read_csv("us-cities-top-1k-multi-year.csv")
df_us
# -

st.markdown(
    " Fuente: [https://github.com/plotly/datasets/blob/master/us-cities-top-1k-multi-year.csv](https://github.com/plotly/datasets/blob/master/us-cities-top-1k-multi-year.csv)"

)

st.markdown(

    "Pero son demasiados datos, filtraremos solamente por las ciudades presentes en nuestros datos, luego tendremos que agrupar nuevamente para obtener el margen de cada **_estado_**, entendiendo que un estado puede tener una o más ciudades."

)

# + jupyter={"source_hidden": true}
df_us_cities_lat_lng = df_us[["City", "lat", "lon"]].copy()
cities = (
    df_us_cities_lat_lng.loc[
        (df_us_cities_lat_lng["City"] == "San Francisco")
        | (df_us_cities_lat_lng["City"] == "Los Angeles")
        | (df_us_cities_lat_lng["City"] == "New York")
        | (df_us_cities_lat_lng["City"] == "Boston")
        | (df_us_cities_lat_lng["City"] == "Atlanta")
        | (df_us_cities_lat_lng["City"] == "Dallas")
        | (df_us_cities_lat_lng["City"] == "Seattle")
        | (df_us_cities_lat_lng["City"] == "Portland")
        | (df_us_cities_lat_lng["City"] == "Austin")
    ]
    .drop_duplicates(subset=["City"], keep="first")
    .sort_values(by=["City"], ascending=True)
    .reset_index(drop=True)
)

cities
# -

st.markdown(

    "Utilizaremos como **weight** la columna `Margin`, así obtendremos la coloración del mapa con base en el margen generado por cada **_estado_** de USA."

)

# + jupyter={"source_hidden": true}
df_geo_margin = cities.join(
    city_df["Margin"], how="outer", lsuffix="_cities", rsuffix="_city_df"
)
df_geo_margin

# + jupyter={"source_hidden": true}
import folium
import requests

from streamlit_folium import st_folium


x = 39.8283
y = -98.5795
m = folium.Map(location=[x, y], zoom_start=4, key="map1")
city_margin = df_geo_margin[["City", "Margin"]].copy()
us_states = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
folium.Choropleth(
    geo_data=us_states,
    data=state_df,
    columns=["State", "Margin"],
    key_on="feature.id",
    fill_color="RdPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Margin rates (%)",
).add_to(m)
folium.LayerControl().add_to(m)
st_data = st_folium(m, width=725)
# -

st.markdown(

    "**Folium** necesita la geometría geográfica de cada uno de los estados de USA, **Folium** recomienda la información de ejemplo disponible en [Github](https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json) en formato **.json**st.markdown("
    ")"

)
st.markdown(

    "Con esta información podríamos decir que el _mejor posible_ lugar para instalar una sucursal física es **California**, considerando que es el estado de USA que más margen le proporciona en el periodo estudiadost.markdown("
    ")"

)
st.markdown("# Conclusiones")
st.markdown(

    "Estudiando, desmembrando y analizando la información que nos proporcionó el cliente podemos concluir bastantes cosas."

)
st.markdown(

    "Realizamos un análisis **Económico** de la situación actual del cliente y como podría proyectarse a futuro, considerando varios aspectosst.markdown("
    ")"

)
st.markdown("### Situación actual del cliente")
st.markdown(

    "El cliente no mostró un aumento de sus ventas en el transcurso del periodo estudiado, mostrando una diferencia negativa de las dos únicas semanas iguales (de distinto año)."

)
st.markdown(

    "La semana del **6 de Enero del 2019** el cliente margino **118.2535 USD** y la semana del **5 de Enero del 2020** margino **112.9792 USD**, esto representa una diferencia de **-4.65%**. Esto no quiere decir que el negocio no fue exitoso, para eso deberíamos conocer y estudiar el **VAN** y la **TIR**.st.markdown("
    ")"

)
st.markdown(

    "Nos damos cuenta, de que las mejores semanas que tuvo nuestro cliente, fueron las semanas del **31 de Marzo del 2019**, **5 de Mayo del 2019** y **11 de Agosto del 2019**, con márgenes que alcanzaron los **124.6876 USD**, **124.5632 USD** y **126.7785 USD** respectivamente."

)

# + jupyter={"source_hidden": true}
fig = make_subplots(rows=1, cols=2)
fig.add_trace(
    go.Scatter(
        x=week["Order Date"],
        y=week["margin"],
        mode="markers+lines",
        name="Lineas scatter",
        marker_color="Blue",
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Bar(
        x=week["Order Date"],
        y=week["margin"],
        name="Barras",
        marker_color="LightSeaGreen",
        opacity=0.8,
    ),
    row=1,
    col=2,
)
fig.update_layout(
    xaxis_tickangle=-90, plot_bgcolor="white", title_text="Margen semanal"
)
st.plotly_chart(fig)
st.markdown(" Gráfico de Línea y Barras con fechas")
st.markdown(

    "En realidad podemos decir que fue un comportamiento bastante parejo, sin considerar su peor semana, la cual fue el **22 de Septiembre del 2019** con un margen de **99.9839 USD**, pero, es este valor apropiado para ser considerado?."

)
st.markdown("")
st.markdown(

    "El promedio`(media aritmética)` semanal de margen es de **115.3102USD**, tomando en cuenta todos los datos. Ahora bien, debemos ser más prolijos y lo que haremos será obtener el promedio sin considerar los **outliers**, aplicando la identificación por el **rango de los quintiles** `(media truncada)`."

)
st.markdown("")
st.markdown(

    "Con un Boxplot podremos apreciar si existen valores fuera de rango, así como también identificarlos para no considerarlos en la ecuación, y claro, en Python son dos líneas de código."

)
st.markdown("1- Grafiquemos")

# + jupyter={"source_hidden": true}
fig = px.box(week, y=["margin"], width=350)
fig.update_layout(plot_bgcolor="white", title_text="Plotbox de los margenes semanales")
st.plotly_chart(fig)
# -

st.markdown(

    "Se aprecian dos valores que están fuera de rango, uno de los cuales es, efectivamente, la peor semana antes mencionada del **22 de Septiembre del 2019**."

)
st.markdown(

    "Y bueno, ¿dónde quedaron las dos líneas de código para obtener el promedio truncado?"

)
st.markdown("")
st.markdown(
    """
```python
trim_mean = stats.trim_mean(dataFrame, 0.2)
trim_mean
```
            """

)
st.markdown("")
st.markdown("todo gracias a la librería **scipy**.")

# + jupyter={"source_hidden": true}
from scipy import stats

trim_mean = stats.trim_mean(week["margin"], 0.2)
trim_mean
# -

st.markdown(" Promedio truncado del margen semanal.")

# + jupyter={"source_hidden": true}
dif_porcen = ((115.3102 - 115.32014074521601) / 115.3102) * 100
dif_porcen

# -

st.markdown("Diferencia porcentual entre promedios obtenidos.")
st.markdown(

    "La diferencia porcentual entre el promedio aritmético y el promedio truncado es de un **-0.0086 %**"

)
st.markdown("## Geolocalización de sucursal física")
st.markdown(

    "Logramos obtener el total de los **margenes** categorizados por **ciudades** y luego en **estados** de **Estados Unidos**, país en el cual nuestro cliente ofrece sus productos, con esto queríamos responder a la pregunta del cliente __¿Dónde instalarse con una sucursal física para su negocio?__"

)
st.markdown("---")
st.markdown(

    "En el gráfico vemos que la mayor concentración del margen obtenido, durante el periodo calculado, se encuentra en el estado de **California**. Y no solo eso, es en toda la **Costa Oeste** donde se encuentran los estados con una concentración significativa."

)
#

x = 39.8283
y = -98.5795
m = folium.Map(location=[x, y], zoom_start=4, key="map1-2")
city_margin = df_geo_margin[["City", "Margin"]].copy()
us_states = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
folium.Choropleth(
    geo_data=us_states,
    data=state_df,
    columns=["State", "Margin"],
    key_on="feature.id",
    fill_color="RdPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Margin rates (%)",
).add_to(m)
folium.LayerControl().add_to(m)

st_data = st_folium(m)
# -
