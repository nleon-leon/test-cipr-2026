import streamlit as Size
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# Configuración de la página
st.set_page_config(page_title="Test CIP-R con Reporte PDF", page_icon="📊", layout="wide")

st.title("📋 Cuestionario de Intereses Profesionales Revisado (CIP-R)")
st.write("Responde a las siguientes preguntas con total sinceridad para descubrir tu perfil vocacional.")

# --- DATOS DEL TEST (Escalas y Preguntas) ---
escalas = {
    "Cálculo y Administración": ["¿Te gustaría llevar la contabilidad de una empresa?", "¿Te interesa aprender a calcular impuestos y presupuestos?"],
    "Científica y Tecnológica": ["¿Te da curiosidad saber cómo funcionan los virus a nivel molecular?", "¿Te gustaría investigar nuevos materiales para la tecnología?"],
    "Humanística y Social": ["¿Te interesaría trabajar ayudando a resolver problemas comunitarios?", "¿Te gustaría estudiar el comportamiento de las sociedades?"],
    "Artística y Creativa": ["¿Disfrutas diseñando logotipos o espacios visuales?", "¿Te interesaría aprender técnicas de pintura o escultura?"],
    "Naturaleza y Aire Libre": ["¿Te gustaría trabajar en la conservación de parques nacionales?", "¿Te interesa el estudio y cuidado de la fauna silvestre?"]
}

# Inicializar estado para guardar respuestas
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

nombre = st.text_input("Introduce tu nombre completo:", "")

st.subheader("📝 Cuestionario")
st.write("Selecciona tu nivel de interés para cada actividad (1: No me interesa, 5: Me interesa mucho)")

# Mostrar preguntas dinámicamente
for escala, preguntas in escalas.items():
    with st.expander(f"Área: {escala}"):
        for preg in preguntas:
            key = f"{escala}_{preg}"
            st.session_state.respuestas[key] = st.slider(preg, 1, 5, 3, key=key)

# --- PROCESAMIENTO DE RESULTADOS ---
if st.button("📊 Calcular Resultados y Generar Reporte"):
    if not nombre:
        st.warning("Por favor, introduce tu nombre antes de calcular los resultados.")
    else:
        # Calcular promedios por escala
        puntajes = {}
        for escala, preguntas in escalas.items():
            suma = 0
            for preg in preguntas:
                suma += st.session_state.respuestas[f"{escala}_{preg}"]
            puntajes[escala] = suma / len(preguntas)
        
        df_resultados = pd.DataFrame(list(puntajes.items()), columns=['Escala', 'Puntaje'])
        
        st.success(f"¡Test completado con éxito, {nombre}!")
        
        # Mostrar gráfico en pantalla
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#38bdf8', '#0ea5e9', '#0284c7', '#0369a1', '#075985']
        ax.barh(df_resultados['Escala'], df_resultados['Puntaje'], color=colors)
        ax.set_xlim(1, 5)
        ax.set_xlabel('Nivel de Interés')
        plt.tight_layout()
        st.pyplot(fig)
        
        # --- GENERACIÓN DEL PDF ---
        # Guardar gráfico en buffer de memoria
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=300)
        img_buf.seek(0)
        
        # Crear PDF clásico
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(3, 105, 161) # Color azul institucional
        pdf.cell(0, 15, "Reporte Oficial - Test CIP-R", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"Evaluado: {nombre}", ln=True)
        pdf.cell(0, 8, "Herramienta: Cuestionario de Intereses Profesionales Revisado", ln=True)
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, "Resultados por Escala:", ln=True)
        pdf.set_font("Helvetica", "", 12)
        
        for esc, punt en puntajes.items():
            pdf.cell(0, 7, f"  • {esc}: {punt:.1f} / 5.0", ln=True)
            
        pdf.ln(10)
        
        # Insertar gráfico en el PDF
        pdf.image(img_buf, x=15, w=180)
        
        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, "Nota: Este reporte es de carácter meramente orientativo y pedagógico. Se recomienda analizar los resultados en conjunto con un orientador vocacional.", align="C")
        
        # Output PDF a bytes
        pdf_bytes = pdf.output()
        
        # Botón de descarga del archivo
        st.download_button(
            label="📥 Descargar Reporte en PDF",
            data=pdf_bytes,
            file_name=f"Reporte_CIPR_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
