import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import calendar

df = pd.read_csv('dataset.csv')
df=df.drop(columns=['DISTRITO','UBIGEO','DEPARTAMENTO','PROVINCIA','FECHA_CORTE','CODIGO','NUMMUL','INTERES','GASTOS','COSTAS','DESCUENTO','TOTAL','FECHAPROYECCION'])#deshacer columnas que no son de interés
df=df.sort_values(by=['ESTADO','ZONA'])

conteo_por_zona = df.groupby(['ZONA', 'ESTADO']).size().unstack(fill_value=0)
fig = go.Figure()
fig.add_trace(go.Bar(x=conteo_por_zona.index, y=conteo_por_zona['A'],name="pendientes"))
fig.add_trace(go.Bar(x=conteo_por_zona.index, y=conteo_por_zona['P'],name="pagados"))      
fig.update_layout(
    title='Distribución por Zona',
    xaxis_title='Zona',
    yaxis_title='Valores',
    legend_title='Estado',
    barmode='group', # Coloca las barras en grupo para cada zona
    xaxis=dict(tickmode='linear', tick0=0, dtick=1), # Asegurando que se muestren todos los valores en X
    template='plotly_white' # Usar un tema claro para el gráfico
)
st.plotly_chart(fig, use_container_width=True)

# Obtener los valores y las etiquetas de la columna 'ESTADO'
labels = df['ESTADO'].value_counts().index
sizes = df['ESTADO'].value_counts().values

# Crear el gráfico de torta
fig2, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
# Asegurarse de que la torta sea circular
ax.axis('equal')
# Mostrarlo en Streamlit
st.pyplot(fig2)


fig3 = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3)])
fig3.update_layout( title='Distribución de Estados', plot_bgcolor='rgba(0, 0, 0, 0)', # Fondo transparente para la figura 
                #paper_bgcolor='lightblue', # Fondo del área del gráfico (opcional) 
                template='plotly_white', # Opcional: El tema de la figura 
                )
st.plotly_chart(fig3, use_container_width=True)

#GRAFICO DE ANIOMULTA Y MONTO
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
    xaxis_title="Monto Promedio",
    yaxis_title="Año de Multa",
    yaxis=dict(autorange="reversed"),  # Invertir el eje Y
    template="plotly_white"
)
st.plotly_chart(fig4, use_container_width=True)

df['mes'] = df['FECHAMULTA'].astype(str).str[4:6].astype(int)
df_values=df[['mes','MONTO']].groupby('mes').agg('count')
df_sorted = df_values.sort_values(by='MONTO', ascending=False)

# 4. Seleccionar los 5 meses con los counts más altos
df_top_5 = df_sorted.head(5)

fig5 = go.Figure()
fig5.add_trace(go.Bar(x=[calendar.month_name[num] for num in df_top_5.index.values], y=df_top_5.values.flatten() ,name="pendientes"))

fig5.update_layout(
    title='Distribución por Zona',
    xaxis_title='Mes',
    yaxis_title='Numero de multas',
    #legend_title='Estado',
    #barmode='group', # Coloca las barras en grupo para cada zona
    #xaxis=dict(tickmode='linear', tick0=0, dtick=1), # Asegurando que se muestren todos los valores en X
    template='plotly_white' # Usar un tema claro para el gráfico
)
st.plotly_chart(fig5, use_container_width=True)

df_multa=df['CODIGOMULTA'].value_counts()
df_top_10_multa = df_multa.head(10)
fig6 = go.Figure()

fig6.add_trace(go.Bar(
    x=df_top_10_multa.index.values,
    y=df_top_10_multa.values.flatten(),
    marker=dict(color='black'),
    name='Número de Ocurrencias'
))

# Configurar el diseño
fig6.update_layout(
    title='Top 10 Códigos de Multa vs. Número de Ocurrencias',
    xaxis_title='Código de Multa',
    yaxis_title='Número de Ocurrencias',
    xaxis=dict(tickangle=-45),  # Rotar las etiquetas del eje X
    template='plotly_white'
)
st.plotly_chart(fig6, use_container_width=True)



