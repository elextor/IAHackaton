# IAHackaton
Hackaton mtc
![Aquí la descripción de la imagen por si no carga](https://github.com/elextor/IAHackaton/blob/main/diagrama.png)



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
     
