import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de página
st.set_page_config(page_title="Resultados Test CIP-R 2026", page_icon="🎓", layout="centered")

# Estilos de la tarjeta con fondo oscuro y letra blanca
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .subtitle { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 40px; }
    .card { background-color: #1E293B; color: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3B82F6; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎯 Conoce tus Resultados: Test CIP-R 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Descubre tus principales intereses vocacionales ingresando tus datos</div>', unsafe_allow_html=True)

# Carga de datos optimizada
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Test CIP-R 4to Medio 2026 (1).xlsx", sheet_name='Respuestas decodificadas')
    return df

try:
    df_test = cargar_datos()
    df_test['Rut_clean'] = df_test['Rut sin puntos y con guión (Ej: 12345678-9)'].astype(str).str.strip().str.upper()

    # Formulario de consulta
    with st.container():
        rut_usuario = st.text_input("🔑 Ingresa tu RUT (con guión y dígito verificador, ej: 12345678-9):")
        buscar = st.button("Consultar mis resultados")

    if buscar or rut_usuario:
        rut_buscar = rut_usuario.strip().upper()
        estudiante = df_test[df_test['Rut_clean'] == rut_buscar]

        if not estudiante.empty:
            fila = estudiante.iloc[0]
            nombre = f"{fila['Nombres']} {fila['Primer Apellido']} {fila['Segundo Apellido']}"
            colegio = fila['Establecimientos']
            curso = fila['Curso']

            st.success(f"¡Hola, {nombre}! Hemos encontrado tus resultados.")
            
            # Ficha del Estudiante
            st.markdown(f"""
            <div class="card">
                <span style="font-size: 18px; font-weight: bold; color: #3B82F6;">📌 Ficha del Estudiante</span><br><br>
                🏫 <b>Colegio:</b> {colegio} <br>
                🎒 <b>Curso:</b> {curso}
            </div>
            """, unsafe_allow_html=True)

            # Las 13 áreas oficiales del test
            areas_oficiales = [
                'Musical', 'Humanística', 'Económica', 'Tecnológica', 'Biológica', 
                'Pedagógica', 'Artística', 'Médica', 'Cálculo', 'Jurídica', 
                'Comunicacional', 'Científica', 'Construcción'
            ]

            # Buscar los puntajes en el Excel ignorando espacios de más en los títulos de las columnas
            puntajes = {}
            for col_excel in fila.index:
                col_limpia = str(col_excel).strip()
                if col_limpia in areas_oficiales and not str(col_excel).endswith('.1'):
                    puntajes[col_limpia] = float(fila[col_excel])

            # Crear el DataFrame con los resultados ordenados
            df_resultados = pd.DataFrame({
                'Área Vocacional': list(puntajes.keys()),
                'Puntaje': list(puntajes.values())
            }).sort_values(by='Puntaje', ascending=False)

            # --- SECCIÓN GRÁFICA ---
            st.subheader("📊 Tu Perfil de Intereses Vocacionales")
            st.write("A mayor puntaje en el gráfico, mayor es tu afinidad o agrado por las actividades de esa área.")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x='Puntaje', y='Área Vocacional', data=df_resultados, palette='Blues_r', ax=ax)
            ax.set_xlabel('Puntaje Obtenido')
            ax.set_ylabel('Áreas del Test')
            st.pyplot(fig)

            # --- SECCIÓN DESTACADOS ---
            st.divider()
            st.subheader("🌟 Tus 3 Áreas de Mayor Interés")
            
            top_3 = df_resultados.head(3)
            cols = st.columns(3)
            
            descripciones = {
                'Musical': 'Composición, ejecución instrumental, canto y apreciación del arte sonoro.',
                'Humanística': 'Interés por la historia, literatura, filosofía y el estudio de la evolución social.',
                'Económica': 'Gestión de recursos, administración, finanzas y organización de empresas.',
                'Tecnológica': 'Uso y reparación de equipos electrónicos, programación y sistemas digitales.',
                'Biológica': 'Estudio de ecosistemas, investigación de flora, fauna y procesos naturales.',
                'Pedagógica': 'Enseñanza, tutoría, asesoramiento educativo y formación de personas.',
                'Artística': 'Expresión plástica, pintura, escultura, diseño de espacios y manualidades.',
                'Médica': 'Cuidado de pacientes, diagnosis, instrumental médico y bienestar de la salud.',
                'Cálculo': 'Resolución de ecuaciones algebraicas, geometría y modelamiento matemático.',
                'Jurídica': 'Defensa legal, análisis de leyes, juicios y resolución de conflictos institucionales.',
                'Comunicacional': 'Periodismo, redacción publicitaria, locución de radio y producción audiovisual.',
                'Científica': 'Investigación experimental en física, química, astronomía y el nivel atómico.',
                'Construcción': 'Diseño arquitectónico, supervisión de obras viales, puentes y estructuras.'
            }

            for idx, (index, row) in enumerate(top_3.iterrows()):
                area_nom = row['Área Vocacional']
                pts = row['Puntaje']
                desc = descripciones.get(area_nom, "Orientación hacia el desarrollo profesional de esta área.")
                
                with cols[idx]:
                    st.metric(label=f"Top {idx+1}: {area_nom}", value=f"{int(pts)} pts")
                    st.caption(desc)
                    
            st.info("💡 **Consejo:** Conversa sobre estos resultados con el orientador de tu liceo o el equipo PACE para explorar opciones de estudio.")
            
        else:
            st.error("❌ El RUT ingresado no se encuentra en los registros.")

except FileNotFoundError:
    st.error(f"No se encontró el archivo de Excel en la carpeta.")