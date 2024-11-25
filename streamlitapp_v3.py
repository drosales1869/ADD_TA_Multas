import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pickle
import calendar

st.set_page_config(layout="wide")
df = pd.read_csv('dataset.csv')
df=df.drop(columns=['DISTRITO','UBIGEO','DEPARTAMENTO','PROVINCIA','FECHA_CORTE','CODIGO','NUMMUL','INTERES','GASTOS','COSTAS','DESCUENTO','TOTAL','FECHAPROYECCION'])#deshacer columnas que no son de interés
df=df.sort_values(by=['ESTADO','ZONA'])
st.title("Dashboard de Multas en el distrito de Ate")
conteo_por_zona = df.groupby(['ZONA', 'ESTADO']).size().unstack(fill_value=0)
izquierda, derecha=st.columns([1,1])
with izquierda:   
    fig = go.Figure()
    fig.add_trace(go.Bar(x=conteo_por_zona.index, y=conteo_por_zona['A'],name="pendientes"))
    fig.add_trace(go.Bar(x=conteo_por_zona.index, y=conteo_por_zona['P'],name="pagados"))      
    fig.update_layout(
        title='Distribución por Zonas del distrito de Ate',
        xaxis_title='Zona',
        yaxis_title='Valores',
        legend_title='Estado',
        barmode='group', # Coloca las barras en grupo para cada zona
        xaxis=dict(tickmode='linear', tick0=0, dtick=1), # Asegurando que se muestren todos los valores en X
        template='plotly_white' # Usar un tema claro para el gráfico
    )
    st.plotly_chart(fig, use_container_width=True)
with derecha:
    # Obtener los valores y las etiquetas de la columna 'ESTADO'
    labels = df['ESTADO'].value_counts().index
    sizes = df['ESTADO'].value_counts().values
    
    mean_monto_by_year = df.groupby('ANIOMULTA')['MONTO'].mean()
    top_10_years = mean_monto_by_year.nlargest(10)
    
    fig4 = go.Figure() 
    
    fig4.add_trace(go.Bar(
        x=top_10_years.values,
        y=top_10_years.index.astype(str),  # Convertir a cadena para que se vea mejor
        orientation='h',  # Barras horizontales
        marker=dict(color='skyblue'),
        name='Monto Promedio'
    ))
    
    # Configurar diseño
    fig4.update_layout(
        title="Top 10 Años con Mayores Montos Promedio",
        xaxis_title="Monto Promedio en Soles",
        yaxis_title="Año de Multa",
        yaxis=dict(autorange="reversed"),  # Invertir el eje Y
        template="plotly_white"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
with izquierda:
    fig3 = go.Figure(data=[go.Pie(labels=['Pagado','No pagado'], values=sizes, hole=0.3)])
    fig3.update_layout( title='Distribución de Estados de Multa', plot_bgcolor='rgba(0, 0, 0, 0)', # Fondo transparente para la figura 
                    #paper_bgcolor='lightblue', # Fondo del área del gráfico (opcional) 
                    template='plotly_white', # Opcional: El tema de la figura 
                    )
    st.plotly_chart(fig3, use_container_width=True)

#GRAFICO DE ANIOMULTA Y MONTO


df['mes'] = df['FECHAMULTA'].astype(str).str[4:6].astype(int)
df_values=df[['mes','MONTO']].groupby('mes').agg('count')
df_sorted = df_values.sort_values(by='MONTO', ascending=False)
df_top_5 = df_sorted.head(5)
with derecha:
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=[calendar.month_name[num] for num in df_top_5.index.values], y=df_top_5.values.flatten() ,name="pendientes"))
    
    fig5.update_layout(
        title='Distribución por Zonas del distrito de Ate',
        xaxis_title='Mes',
        yaxis_title='Numero de multas',
        #legend_title='Estado',
        #barmode='group', # Coloca las barras en grupo para cada zona
        #xaxis=dict(tickmode='linear', tick0=0, dtick=1), # Asegurando que se muestren todos los valores en X
        template='plotly_white' # Usar un tema claro para el gráfico
    )
    st.plotly_chart(fig5, use_container_width=True)
with izquierda:
    df_multa=df['CODIGOMULTA'].value_counts()
    df_top_10_multa = df_multa.head(10);
    df10 = df.iloc[df_top_10_multa.values.flatten()]
    
    # Paso 1: Contar las ocurrencias de cada "CODIGOMULTA" y seleccionar los 10 más frecuentes
    top_10_codigos_freq = df['CODIGOMULTA'].value_counts().head(10)

# Paso 2: Filtrar las filas donde "CODIGOMULTA" esté entre los más frecuentes
    top_10_df = df[df['CODIGOMULTA'].isin(top_10_codigos_freq.index)]

# Paso 3: Eliminar duplicados y crear una copia explícita
    top_10_unicos = top_10_df.drop_duplicates(subset='CODIGOMULTA', keep='first').copy()

# Paso 4: Agregar la frecuencia como columna auxiliar
    top_10_unicos.loc[:, 'FRECUENCIA'] = top_10_unicos['CODIGOMULTA'].map(top_10_codigos_freq)

# Paso 5: Ordenar el DataFrame por frecuencia (descendente)
    resultado = top_10_unicos.sort_values(by='FRECUENCIA', ascending=False)[['CODIGOMULTA', 'DESCRIPCION']]


    
    fig6 = go.Figure()
    
    fig6.add_trace(go.Bar(
        x=df_top_10_multa.index.values,
        y=df_top_10_multa.values.flatten(),
        marker=dict(color='black'),
        name='Número de Ocurrencias'
    ))
    
    # Configurar el diseño
    fig6.update_layout(
        title='Top 10 Códigos de Multa vs <br>Número de Ocurrencias',
        xaxis_title='Código de Multa',
        yaxis_title='Número de Ocurrencias',
        xaxis=dict(tickangle=-45),  # Rotar las etiquetas del eje X
        template='plotly_white'
    )
    st.plotly_chart(fig6, use_container_width=True)
with derecha:
    st.markdown("<h3 style='font-size: 17px;'>Descripción de los Códigos de Multa:</h3>", unsafe_allow_html=True)
    descripciones_texto = ""
    for index, row in resultado.iterrows():
        descripciones_texto += f"\n Código {row['CODIGOMULTA']}:{row['DESCRIPCION']}\n\n"
    st.markdown(f"""
    <div style="height: 300px; overflow-y: scroll; border: 1px solid #ddd; padding: 20px;">
        {descripciones_texto}
    """, unsafe_allow_html=True)
    df['codigo_multa_numeric'] = pd.to_numeric(df['CODIGOMULTA'], errors='coerce')

# Filtrar las filas donde 'codigo_multa_numeric' es NaN (es decir, eran datos no numéricos)
filas_no_numericas = df[df['codigo_multa_numeric'].isna()]
df = df.dropna(subset=['codigo_multa_numeric'])

# Cargar el modelo guardado
with open('clf.pkl', 'rb') as file:
    clf = pickle.load(file)
    st.title("Predicción de Multa Pagada o No Pagada")
# Para la visualización del mes, convertimos de número a nombre
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Crear una columna para representar mejor cada usuario (opcional)
df['usuario'] = 'Año de la multa:'+(
    df['ANIOMULTA'].astype(str) + '| Número de Zona: ' +  # Convertir ANIOMULTA a str
    df['ZONA'].astype(str) + '| Mes: ' +  # Asegurarse de que ZONA sea string
    df['mes'].apply(lambda x: meses[int(x)-1] if pd.notna(x) else '') + ' | Monto:' +  # Convertir el mes de número a texto (y asegurar que sea un número válido)
    df['MONTO'].apply(lambda x: str(round(x, 2))) + ' | ' +  # Redondear el monto a 2 decimales y convertirlo a string
    'Código Giro: ' + df['CODIGODEGIRO'].astype(str) + ' | ' +  # Asegurarse de que CODIGODEGIRO sea string
    'Código Multa: ' + df['codigo_multa_numeric'].astype(str)  # Asegurarse de que 'codigo_multa_numeric' sea string
)

df_muestra = df.sample(n=20, random_state=42)  # Cambia el número si quieres más o menos usuarios

# Permitir al usuario seleccionar un usuario de la lista (solo los 20 seleccionados)
usuario_seleccionado = st.selectbox("Selecciona un usuario para predecir:", df_muestra['usuario'].unique())

# Extraer las características del usuario seleccionado
usuario_info = df[df['usuario'] == usuario_seleccionado].iloc[0]

# Mostrar las características del usuario seleccionado
st.markdown("<h3 style='font-size: 24px;'>Has seleccionado el siguiente usuario:</h3>", unsafe_allow_html=True)
st.write(f"Año de la multa: {usuario_info['ANIOMULTA']}")
st.write(f"Zona: {usuario_info['ZONA']}")
st.write(f"Mes: {meses[usuario_info['mes']-1]}")
st.write(f"Monto: {usuario_info['MONTO']}")
st.write(f"Código de Giro: {usuario_info['CODIGODEGIRO']}")
st.write(f"Código de Multa: {usuario_info['codigo_multa_numeric']}")

# Crear los datos de entrada para la predicción utilizando el usuario seleccionado
datos_entrada = pd.DataFrame({
    'MONTO': [usuario_info['MONTO']],
    'ANIOMULTA': [usuario_info['ANIOMULTA']],
    'ZONA': [usuario_info['ZONA']],
    'mes': [usuario_info['mes']],
    'CODIGODEGIRO': [usuario_info['CODIGODEGIRO']],
    'codigo_multa_numeric': [usuario_info['codigo_multa_numeric']]
})

# Realizar la predicción de probabilidad usando el modelo
probabilidades = clf.predict_proba(datos_entrada)

# Probabilidad de que sea pagada (Clase 1) y no pagada (Clase 0)
probabilidad_pagada = probabilidades[0][1]
probabilidad_no_pagada = probabilidades[0][0]

# Mostrar las probabilidades
st.write(f"Probabilidad de que la multa sea pagada: {probabilidad_pagada*100:.2f}%")
st.write(f"Probabilidad de que la multa sea no pagada: {probabilidad_no_pagada*100:.2f}%")

# Mostrar el resultado con el color correspondiente
if probabilidad_pagada > probabilidad_no_pagada:
    st.markdown("<h3>Es probable que la multa <span style='color: green;'>se pague</span></h3>", unsafe_allow_html=True)
else:
    st.markdown("<h3>Es probable que la multa <span style='color: red;'>no se pague</span></h3>", unsafe_allow_html=True)
