import pandas as pd
import streamlit as st
import webbrowser
import datetime
from streamlit_folium import folium_static
import json
import requests
from pandas import json_normalize
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go


import pyrebase




st.set_page_config(
    page_title="Dash Board IA-hackaton",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("TEAM DS IA-CKATON , PARA LA SEGUIRDAD VIAL")
st.subheader("By Team Ds-“SEGURIDAPP” -Aplicación Móvil y Web para Inventariar y Geolocalizar los Semáforos validados con Inteligencia Artificial y Visualización en tiempo real")

st.markdown("""

* **Modulo APP -Movil** Obtener  imagenes y georeferenciadas mediante una aplicacion movil 
* Procesar los datos obtenidos e Inventariar en tiempo real Semaforos utilizando Geolocacion y QR 
* Genear una base de datos de imagenes para posteriormente  etiquetalos  por un modelo IA y validar las imagenes.
* **DashBoar Web** Visualizar en un DashBoar los datos obtenidos por la APP-movil en un mapa georefrenciados  y obtener indicadores
""")
st.image("diagrama.png")

############################################################################
# Row number (Zero): This is to give the App title:
null0_1, row0_2, null0_2, row0_3, null0_3 = st.columns((0.23, 5, 0.1, 5, 0.1))

with row0_2:
    st.title("VISUALIZACION")
    st.write(
    """
    **Obtencion del dataset recolectado por la APP-Movil**
    """)

# Row number (1): This is to give the App Introduction: we'll have 5 Columns:


###########################

null2_1, row2_1, row2_2, row2_3, row2_4, row2_5 = st.columns((0.1, 2.8, 0.1, 0.8, 0.8, 0.1))

with row2_1:
    geojson_url = "https://subirimagen-63f7f.firebaseio.com/Image.json"
    df = pd.read_json(geojson_url).T
    df["codigo"] = df["codigo"].astype(int)
    df["conteo"] = 1
    df["Lat"] = df["Lat"].astype(float)
    df["Long"] = df["Long"].astype(float)

    list_departamentos=df['zona'].unique().tolist()
    departamento = st.selectbox(" ", list_departamentos)

    st.write(df)


with row2_3:
    st.write(
        """
        #### **Indicadores:**
        """)



# Now, let's divide user's input into 2 groups: House Details & Neighborhood Details and each will be in seperate column: row2_3 & row2_4
d1=df["conteo"].sum()
sqft = row2_3.number_input('TOTAL DATOS', min_value=0, max_value=d1+1, value=d1, help="Min=381, Max=5000")

##gsRating = row2_4.number_input('value', min_value=1, max_value=10, value=9, help="Min=1, Max=10, [GreatSchools.org](https://www.greatschools.org/)")
##median_income = row2_4.number_input('value', min_value=45000, max_value=182000, value=170000, help="Min=$25K, Max=$182K")

d4=df["zona"].value_counts().max()
lot_size = row2_3.number_input('zonas con mayor reporte', min_value=0, max_value=d4+1, value=d4, help="Min=0, Max=18000")

list_valores = df['zona'].unique().tolist()

property_type = row2_3.selectbox('Departamentos Reportados', list_valores, index=0)
beds = row2_3.selectbox('Ultimo reporte', (1, 2, 3, 4, 5), index=3)


#####################################

def dataframe():
    st.write("dataframe")
dataframe()


def open_web():
    webbrowser.open('https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python')



def mapa_clusters():
    with st.form('my_form5'):
        Title = st.title("Mapa clusters")
        list_valores = df['zona'].unique().tolist()
        valores = st.selectbox(" ", list_valores)
        btn_zoon = st.form_submit_button("ver")
        if btn_zoon:
            mc = MarkerCluster()
            some_map = folium.Map(location=[df["Lat"].mean(), df["Long"].mean()], zoom_map=10)
            for row in df.itertuples():
                mc.add_child(folium.Marker(location=[row.Lat, row.Long], popup=row.objeto))
            folium_static(some_map.add_child(mc), width=1050, height=600)




def mapa():
    with st.form('my_form2'):
        Title = st.title("Mapa")
        list_valores = df['zona'].unique().tolist()
        valores = st.selectbox(" ", list_valores)
        btn_zoon = st.form_submit_button("Ver")
        if btn_zoon:
            some_map = folium.Map(location=[df["Lat"].mean(), df["Long"].mean()], zoom_map=40)
            for row in df.itertuples():
                some_map.add_child(folium.Marker(location=[row.Lat, row.Long], popup=row.objeto))

            folium_static(some_map, width=1050, height=500)






def mapa_head():
    fig = px.density_mapbox(df, lat=df["Lat"], lon=df["Long"], z=df["codigo"], radius=30,
                            center=dict(lat=-13.528703, lon=-71.941385), zoom=10,
                            mapbox_style="open-street-map")
    st.plotly_chart(fig, width=10, height=10)

    ######################

def elemento():
    with st.form('my_form10'):
        Title = st.title("Inspeccionar elementos")
        max=int(len(df.index))
        number = st.slider("elementos", min_value=0, max_value=max)
        btn_elemento=st.form_submit_button("Ver")
        if btn_elemento:
            fila = pd.DataFrame(df.iloc[number]).T  # Primera fila
            fila_reset = fila.reset_index(drop=True)
            st.write(fila_reset)



elemento()




def container2():
    col1, col2,  = st.columns(2)

    with col1:
        with st.form('Form1'):
            st.write("Estado de Los semaforos")
            df2 = pd.DataFrame(df['estado'].value_counts())
            df2 = df2.reset_index()
            fig9 = px.bar(df2, x='index', y="estado", width=500, height=500)
            st.plotly_chart(fig9)
            st.form_submit_button("Actualizar")

    with col2:
        with st.form('Form2'):
            st.write("Tipo de bien reportado")
            grouped_df2 = df.groupby(['objeto', 'trafico']).sum()
            grouped_df2 = grouped_df2.reset_index()
            fig = px.pie(grouped_df2, values='conteo', names='objeto', color='objeto', hole=.3,
                         color_discrete_map={'MUCHO': 'lightcyan',
                                             'SOLO HORA PUNTA': 'cyan',
                                             'POCO': 'royalblue',
                                             'MUCHO': 'darkblue'}, width=500, height=500)

            st.plotly_chart(fig)
            st.form_submit_button("Actualizar")


container2()

def container3():
    colu2, colu3 = st.columns(2)

    with colu2:
        st.subheader("Trafico")
        with st.form('Form4'):
            grouped_df2 = df.groupby(['objeto', 'trafico']).sum()
            grouped_df2 = grouped_df2.reset_index()
            fig = px.pie(grouped_df2, values='conteo', names='trafico', color='trafico', hole=.3,
                         color_discrete_map={'MUCHO': 'lightcyan',
                                             'SOLO HORA PUNTA': 'cyan',
                                             'POCO': 'royalblue',
                                             'MUCHO': 'darkblue'}, width=500, height=500)

            st.plotly_chart(fig)
            st.form_submit_button()

    with colu3:
        st.subheader("Departamento")
        with st.form('Form5'):
            df2 = pd.DataFrame(df['zona'].value_counts())
            df2 = df2.reset_index()
            fig2 = px.bar(df2, x='zona', y="index",orientation='h',width=500, height=500)
            st.plotly_chart(fig2)
            st.form_submit_button()
container3()
#############

def container4():
    grouped_df = df.groupby(['fecha', 'trafico']).sum()
    grouped_df = grouped_df.reset_index()
    fig3 = px.line(grouped_df, x="fecha", y="conteo", title='Linea de tiempo de reportes', width=1200, height=500)
    fig3.update_xaxes(rangeslider_visible=True)

    st.plotly_chart(fig3)



container4()




def bar():
    st.sidebar.image("logo2.jpg")
    st.sidebar.title("Inicio")
    options = st.sidebar.selectbox("INVENTARIO DE BIENES", ("SEMAFOROS", "PUENTES PEATONALES","PASOS PEATONALES"))
    d = st.sidebar.date_input("Select Fecha", datetime.date.today() - datetime.timedelta(days=2))
    t = st.sidebar.time_input('Select Hora', datetime.time(1, 30))
    date = datetime.datetime.combine(d, t).strftime("%Y-%m-%d %H:%M:%S")
    button5=st.sidebar.button("DATABASE")
    if button5:
        dataframe()
    st.sidebar.title("Opciones en Mapas")
    check1=st.sidebar.checkbox("Ubicacion de Semaforos")
    if check1:
        mapa()

    check2=st.sidebar.checkbox("Mapa de trafico")

    if check2:
        mapa_head()

    check3=st.sidebar.checkbox("Mapa clusters")
    if check3:
        mapa_clusters()
    button4=st.sidebar.button("Exportar")
    if button4:
        open_web()

bar()

st.subheader("Notas")
st.write(
    """
    - El dashboar esta desarrollado en [Streamlit](https://streamlit.io/) y python    
    - Se comsumen los datos mediante el API de google firebase Google Cloud.
    - Para Los graficos interactivos se usaron las librerias Plotly y seaborn.
    - Para la visualizacion de los mapas se utilizaron las libreias de Folium y plotly.
    - Se pueden agregar mas metricas e indicadores en la visualizacion . 
    - Las imagenes estan almacenadas en el storage database cloud Firebase.
    - La aplicacion movil esta desarrollada integramente para la plataforma Android.
    - Se utilizo codigo JAVA nativo para el desarrollo de la aplicacion en Android Studio.
    - El servicio de realtime database de Firebase esta integrado al SDK de android esta se encuentra cifrada para proteger los datos.
    - para Validar las imagenes se utilizo un modelo pre-entrenado con las Librerias Pytorch,con el Dataset [LISA traffic Light Dataset](https://www.kaggle.com/mbornoe/lisa-traffic-light-dataset) 
    - La base de datos consta de secuencias de video de prueba y capacitación continuas, con un total de 43.007 cuadros y 113.888 semáforos anotados. Las secuencias son capturadas por una cámara estéreo montada en el techo de un vehículo que se conduce tanto de noche como de día con diferentes condiciones de luz y clima.


     
    

   
    Desarrollado por  [Hector Jakson letona Q ](https://www.linkedin.com/in/hector-jakson-letona-377b4b201/). 

    """
)

st.markdown(
    """
    ### Codigo 
    El codigo en Python y JAVA estaran disponibles en cuanto finalicen el evento en el repositorio de GITHUB data is from  https://github.com/elextor
    """
)
st.markdown(
    " Peru , 30 de setiembre del 2021 , AI - IACKATON - MTC"
)


st.markdown("![visitors](https://visitor-badge.glitch.me/badge?page_id=remingm.covid)")