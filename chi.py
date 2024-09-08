import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Pruebas de Chi-Cuadrado", layout="wide")

# Título y descripción de la aplicación
st.title("Aplicación de Pruebas de Chi-Cuadrado")
st.write("""
Esta aplicación permite realizar diferentes pruebas de Chi-Cuadrado, incluyendo independencia, bondad de ajuste, y homogeneidad.
Puedes cargar tus datos, seleccionar las variables y realizar la prueba de forma interactiva.
""")

# Sidebar para configuración del modo
st.sidebar.title("Configuración de la Interfaz")
theme = st.sidebar.radio("Selecciona el tema", ["Claro", "Oscuro"])

# Aplicación del tema
if theme == "Oscuro":
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .css-1aumxhk, .css-16idsys, .css-1ukrds8 {
            background-color: #0e1117;
        }
        .css-10trblm {
            color: white;
        }
        .css-1cpxqw2 a {
            color: #ff4b4b;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
        }
        .stDownloadButton>button {
            background-color: #ff4b4b;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .css-1aumxhk, .css-16idsys, .css-1ukrds8 {
            background-color: white;
        }
        .css-10trblm {
            color: black;
        }
        .css-1cpxqw2 a {
            color: #584bff;
        }
        .stButton>button {
            background-color: #584bff;
            color: white;
        }
        .stDownloadButton>button {
            background-color: #584bff;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Carga de datos
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV o Excel", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write("Datos cargados:")
    st.dataframe(df.head())

    # Selección del tipo de prueba de Chi-Cuadrado
    st.write("### Selección del Tipo de Prueba de Chi-Cuadrado")
    test_type = st.selectbox("Selecciona el tipo de prueba", ["Independencia", "Bondad de Ajuste", "Homogeneidad"])

    columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if test_type == "Independencia":
        st.write("### Prueba de Independencia")
        var1 = st.selectbox("Selecciona la primera variable categórica", columns)
        var2 = st.selectbox("Selecciona la segunda variable categórica", [col for col in columns if col != var1])

        # Tabla de contingencia
        st.write("### Tabla de Contingencia")
        contingency_table = pd.crosstab(df[var1], df[var2])
        st.write(contingency_table)

        # Cálculo de la prueba Chi-Cuadrado
        st.write("### Resultados de la Prueba Chi-Cuadrado")
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        st.write(f"Chi-cuadrado: {chi2:.4f}")
        st.write(f"p-valor: {p_value:.4f}")
        st.write(f"Grados de libertad: {dof}")
        st.write("Frecuencias esperadas:")
        st.write(expected)

        # Interpretación de resultados
        st.write("### Interpretación de Resultados")
        alpha = st.number_input("Nivel de significancia (alpha)", value=0.05)
        interpretacion = ("Rechazamos la hipótesis nula. Existe una relación significativa entre las variables."
                          if p_value < alpha else
                          "No podemos rechazar la hipótesis nula. No existe evidencia suficiente para afirmar una relación significativa entre las variables.")
        st.write(interpretacion)

        # Visualización gráfica
        st.write("### Visualización Gráfica")

        # Gráfico circular para la primera variable
        fig1 = px.pie(df, names=var1, title=f"Distribución de {var1}")
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico circular para la segunda variable
        fig2 = px.pie(df, names=var2, title=f"Distribución de {var2}")
        st.plotly_chart(fig2, use_container_width=True)

    elif test_type == "Bondad de Ajuste":
        st.write("### Prueba de Bondad de Ajuste")
        variable = st.selectbox("Selecciona la variable categórica", columns)
        
        # Frecuencias observadas
        observed = df[variable].value_counts().sort_index()
        st.write("Frecuencias observadas:")
        st.write(observed)
        
        # Frecuencias esperadas
        expected_input = st.text_area("Ingresa las frecuencias esperadas (separadas por comas)")
        expected = np.array([float(x) for x in expected_input.split(",")])
        
        # Prueba de bondad de ajuste
        chi2, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
        st.write(f"Chi-cuadrado: {chi2:.4f}")
        st.write(f"p-valor: {p_value:.4f}")
        
        # Interpretación de resultados
        st.write("### Interpretación de Resultados")
        alpha = st.number_input("Nivel de significancia (alpha)", value=0.05)
        interpretacion = ("Rechazamos la hipótesis nula. La distribución observada difiere significativamente de la esperada."
                          if p_value < alpha else
                          "No podemos rechazar la hipótesis nula. No existe evidencia suficiente para afirmar que la distribución observada difiere de la esperada.")
        st.write(interpretacion)

    elif test_type == "Homogeneidad":
        st.write("### Prueba de Homogeneidad")
        variable = st.selectbox("Selecciona la variable categórica", columns)
        group = st.selectbox("Selecciona la variable de grupo", columns)
        
        contingency_table = pd.crosstab(df[variable], df[group])
        st.write("Tabla de Contingencia:")
        st.write(contingency_table)
        
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        st.write(f"Chi-cuadrado: {chi2:.4f}")
        st.write(f"p-valor: {p_value:.4f}")
        st.write(f"Grados de libertad: {dof}")
        st.write("Frecuencias esperadas:")
        st.write(expected)
        
        # Interpretación de resultados
        st.write("### Interpretación de Resultados")
        alpha = st.number_input("Nivel de significancia (alpha)", value=0.05)
        interpretacion = ("Rechazamos la hipótesis nula. Las distribuciones en los grupos no son homogéneas."
                          if p_value < alpha else
                          "No podemos rechazar la hipótesis nula. No existe evidencia suficiente para afirmar que las distribuciones en los grupos son diferentes.")
        st.write(interpretacion)

    # Generar reporte
    reporte = f"""
    Resultados de la Prueba Chi-Cuadrado ({test_type})\n
    Variables analizadas: {var1 if test_type == 'Independencia' else variable} y {var2 if test_type == 'Independencia' else 'N/A'}\n
    Chi-cuadrado: {chi2:.4f}\n
    p-valor: {p_value:.4f}\n
    Grados de libertad: {dof if test_type != 'Bondad de Ajuste' else 'N/A'}\n
    Nivel de significancia (alpha): {alpha}\n
    Interpretación: {interpretacion}
    """

    # Descargar reporte en texto
    st.download_button(
        label="Descargar Reporte (Texto)",
        data=reporte,
        file_name='reporte_chi_cuadrado.txt',
        mime='text/plain'
    )

else:
    st.write("Por favor, carga un archivo de datos para comenzar.")
