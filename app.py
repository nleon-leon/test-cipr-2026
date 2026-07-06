import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
from datetime import datetime

# Configuración de la página institucional
st.set_page_config(page_title="Portal CIP-R - Orientación Vocacional", page_icon="🎓", layout="wide")

st.title("📋 Cuestionario de Intereses Profesionales Revisado (CIP-R)")
st.write("Análisis de Resultados de Orientación Vocacional - Formato Oficial con Interpretación")

# --- LAS 13 ÁREAS EN EL ORDEN EXACTO ---
escalas_reales = {
    "Musical": ["¿Te interesa aprender a componer o arreglar piezas musicales?", "¿Te gustaría dominar la teoría musical?"],
    "Humanística": ["¿Te interesaría estudiar historia o filosofía?", "¿Te gustaría trabajar en resolución de conflictos?"],
    "Económica": ["¿Te atrae la idea de planificar estrategias financieras?", "¿Te interesaría administrar presupuestos?"],
    "Tecnológica": ["¿Te da curiosidad el desarrollo de software o IA?", "¿Te gustaría diseñar sistemas informáticos?"],
    "Biológica": ["¿Te interesa investigar los ecosistemas y la flora?", "¿Te gustaría trabajar en laboratorios orgánicos?"],
    "Pedagógica": ["¿Disfrutarías enseñando a jóvenes o capacitando personas?", "¿Te gustaría guiar el aprendizaje?"],
    "Artística": ["¿Te interesa el diseño gráfico o la arquitectura?", "¿Disfrutas creando conceptos visuales?"],
    "Médica": ["¿Te gustaría trabajar en el diagnóstico de la salud humana?", "¿Te interesa el ámbito clínico?"],
    "Cálculo": ["¿Te apasiona resolver problemas mediante matemáticas?", "¿Te interesa la estadística aplicada?"],
    "Jurídica": ["¿Te gustaría estudiar leyes y normativas?", "¿Te interesa la asesoría legal y derechos?"],
    "Comunicacional": ["¿Te atrae el periodismo o las relaciones públicas?", "¿Te gustaría dirigir campañas de comunicación?"],
    "Científica": ["¿Te interesa el método científico para descubrir nuevas leyes?", "¿Te gustaría investigar ciencias puras?"],
    "Construcción": ["¿Te gustaría dirigir obras civiles o edificaciones?", "¿Te interesa el cálculo estructural?"]
}

# --- BASE DE DATOS DE INTERPRETACIONES OFICIALES ---
interpretaciones = {
    "Musical": "Muestras una alta inclinación hacia la expresión sonora, composición, ejecución de instrumentos y la comprensión de estructuras musicales. Carreras afines: Intérprete Musical, Composición, Producción Musical, Pedagogía en Música.",
    "Humanística": "Te interesan los procesos culturales, la historia, el pensamiento social y el bienestar comunitario. Valoras el análisis crítico de la sociedad. Carreras afines: Psicología, Antropología, Trabajo Social, Sociología, Filosofía.",
    "Económica": "Presentas interés en la gestión de recursos, dirección de organizaciones, desarrollo de negocios y planificación financiera. Carreras afines: Ingeniería Comercial, Auditoría, Administración de Empresas, Comercio Exterior.",
    "Tecnológica": "Fuerte orientación hacia la innovación digital, la programación, el diseño de sistemas de información y la resolución de problemas lógicos y computacionales. Carreras afines: Ingeniería Civil Informática, Conectividad y Redes, Analista Programador.",
    "Biológica": "Te apasiona el estudio de los organismos vivos, los ecosistemas, la conservación ambiental y los procesos químicos y orgánicos de la naturaleza. Carreras afines: Biología Marina, Agronomía, Medicina Veterinaria, Biotecnología.",
    "Pedagógica": "Tienes vocación para transmitir conocimientos, guiar procesos de aprendizaje, diseñar metodologías educativas y potenciar las habilidades de otras personas. Carreras afines: Pedagogía (en diversas especialidades), Educación Parvularia, Psicopedagogía.",
    "Artística": "Fuerte canal de expresión visual, espacial y estética. Disfrutas de la creación de conceptos artísticos, el diseño técnico y las artes plásticas. Carreras afines: Arquitectura, Diseño Gráfico, Diseño de Interiores, Artes Visuales.",
    "Médica": "Interés centrado en el cuidado directo de la salud de las personas, la asistencia clínica, la prevención de enfermedades y el soporte biomédico. Carreras afines: Medicina, Enfermería, Kinesiología, Tecnología Médica, Obstetricia.",
    "Cálculo": "Inclinación natural hacia el razonamiento lógico-matemático, análisis cuantitativo de datos y resolución de problemas de ingeniería analítica. Carreras afines: Ingeniería Civil Matemática, Estadística, Licenciatura en Matemáticas.",
    "Jurídica": "Te motiva el estudio de las leyes, la defensa de los derechos, el análisis normativo, la justicia social y la diplomacia o mediación formal. Carreras afines: Derecho, Ciencias Políticas, Administración Pública.",
    "Comunicacional": "Gran interés en la difusión de información, producción de contenidos multimediales, redacción de crónicas y gestión de la opinión pública o corporativa. Carreras afines: Periodismo, Relaciones Públicas, Comunicación Audiovisual.",
    "Científica": "Fuerte interés por el desarrollo de la ciencia pura, la investigación de laboratorio, la aplicación rigurosa del método científico y la física/química avanzada. Carreras afines: Licenciatura en Física, Bioquímica, Astronomía, Química Pura.",
    "Construcción": "Orientación práctica y técnica hacia la infraestructura, planificación urbana, diseño de estructuras físicas y edificación residencial o industrial. Carreras afines: Ingeniería Civil en Construcción, Arquitectura, Técnico en Construcción."
}

if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

# Identificación del Alumno
with st.container():
    st.subheader("🔑 Identificación del Estudiante")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("NOMBRE COMPLETO:", "")
        rut = st.text_input("RUT:", "")
    with col2:
        establecimiento = st.text_input("ESTABLECIMIENTO:", value="LICEO INDUSTRIAL DE ANGOL")
        curso = st.text_input("CURSO / NIVEL:", value="4°D")

st.markdown("---")

# Cuestionario
st.subheader("📝 Cuestionario")
for area, preguntas in escalas_reales.items():
    with st.expander(f"Área: {area}"):
        for preg in preguntas:
            key = f"{area}_{preg}"
            st.session_state.respuestas[key] = st.slider(preg, 1, 5, 3, key=key)

# Procesamiento
if st.button("📊 Calcular Resultados e Interpretación"):
    if not nombre or not rut:
        st.warning("Por favor, introduce tu Nombre y RUT para generar el informe oficial.")
    else:
        puntajes = {}
        for area, preguntas in escalas_reales.items():
            suma = 0
            for preg in preguntas:
                suma += st.session_state.respuestas[f"{area}_{preg}"]
            promedio = suma / len(preguntas)
            porcentaje = int((promedio - 1) / 4 * 100)
            puntajes[area] = porcentaje
            
        df_resultados = pd.DataFrame(list(puntajes.items()), columns=['Escala', 'Puntaje'])
        
        st.success(f"¡Análisis procesado para {nombre}!")
        
        # Obtener las 3 mejores áreas
        ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        top_3 = ordenados[:3]
        
        # Gráfico Oficial en pantalla
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(df_resultados['Escala'], df_resultados['Puntaje'], color="#06b6d4", marker='o', linewidth=2)
        ax.fill_between(df_resultados['Escala'], df_resultados['Puntaje'], color="#06b6d4", alpha=0.2)
        ax.set_ylim(0, 100)
        ax.set_ylabel('Porcentaje')
        ax.set_title('Distribución de tus intereses vocacionales', fontweight='bold', pad=12)
        plt.xticks(rotation=35, ha='right', fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        
        # --- NUEVA SECCIÓN: INTERPRETACIÓN EN PANTALLA ---
        st.markdown("---")
        st.subheader("🏆 Tus 3 Principales Áreas de Interés Vocacional")
        
        cols_top = st.columns(3)
        for idx, (area_top, porc_top) in enumerate(top_3):
            with cols_top[idx]:
                st.metric(label=f"Área Top {idx+1}", value=f"{area_top} ({porc_top}%)")
                st.info(interpretaciones[area_top])
        
        # Guardar gráfico en memoria para pasarlo al PDF
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=300)
        img_buf.seek(0)
        
        # --- CONSTRUCCIÓN DEL REPORTE PDF OFICIAL ---
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado institucional
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 5, "ANÁLISIS DE RESULTADOS DE ORIENTACIÓN VOCACIONAL", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"Fecha de Emisión: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(6)
        
        # Recuadro de Datos del Alumno
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(10, 22, 190, 32, "FD")
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(30, 41, 59)
        pdf.text(14, 28, f"NOMBRE COMPLETO:  {nombre.upper()}")
        pdf.text(14, 35, f"RUT:              {rut}")
        pdf.text(14, 42, f"ESTABLECIMIENTO:  {establecimiento.upper()}")
        pdf.text(14, 49, f"CURSO:            {curso.upper()}  |  INSTRUMENTO: CIP-R")
        
        pdf.ln(28)
        
        pdf.set_font("Helvetica", "I", 8.5)
        pdf.set_text_color(100, 116, 139)
        nota_texto = "Nota: Usa los resultados como una guía, no como una regla absoluta: Los resultados del test pueden orientarte en la elección de un camino para tu desarrollo profesional, pero no determinan tu futuro."
        pdf.multi_cell(190, 4.5, nota_texto)
        pdf.ln(2)
        
        # Insertar Gráfico Turquesa Oficial
        pdf.image(img_buf, x=10, w=190)
        pdf.ln(3)
        
        # Sección de Interpretación de las 3 mejores áreas en el PDF
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(2, 132, 199)
        pdf.cell(0, 6, "Interpretación de tus 3 áreas destacadas", ln=True)
        pdf.ln(2)
        
        for idx, (area_pdf, porc_pdf) in enumerate(top_3):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, f"N°{idx+1}: {area_pdf} — Coincidencia del {porc_pdf}%", ln=True)
            
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(190, 4.5, interpretaciones[area_pdf])
            pdf.ln(2)
            
        pdf_bytes = pdf.output()
        
        # Botón de descarga final para el alumno
        st.download_button(
            label="📥 Descargar Reporte PDF con Interpretación",
            data=pdf_bytes,
            file_name=f"Reporte_Interpretado_CIPR_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
