import pandas as pd

def generar_html_ac(archivo_csv, año):
    # Leer el archivo CSV
    data = pd.read_csv(archivo_csv)

    # Filtrar por el año especificado
    data_año = data[data['Año'] == año]

    # Iniciar la estructura del HTML
    html_output = f"""
        <div class="row g-1">
    """

    # Obtener los semestres únicos en orden
    semestres_ordenados = sorted(data_año['Semestre'].unique(), key=lambda x: str(x))

    # Procesar cada semestre en el orden correcto
    for semestre in semestres_ordenados:
        html_output += f"""
            <div class="col-6">
                <h5 class="semester-title">{semestre}</h5>
        """

        # Filtrar las materias del semestre actual
        materias = data_año[data_año['Semestre'] == semestre]

        # Generar las asignaturas en el HTML
        for _, row in materias.iterrows():
            nombre = row['Nombre']
            codigo = row['Código']
            creditos = row['Créditos'] if pd.notna(row['Créditos']) else ""
            requisitos = row['Requisito'] if pd.notna(row['Requisito']) else "Sin requisito"
            rec_cod = row['Rec_cod'] if pd.notna(row['Rec_cod']) else ""
            bibliografia = row['Bibliografía'] if pd.notna(row['Bibliografía']) else "No disponible"

            # Si hay códigos en Rec_cod, agrégalos a los requisitos
            if rec_cod:
                requisitos += f" ({rec_cod})"

            # Generar enlace de material si existe (opcional)
            material = "" #f"https://example.com/{codigo}" if rec_cod else ""

            # Formatear la bibliografía como lista HTML si existe
            # bibliografia_formato = ""
            # if bibliografia:
            #     bibliografia_list = bibliografia.split(';')
            #     bibliografia_formato = "<ul class='text-justify'>" + "".join(f"<li>{ref.strip()}</li>" for ref in bibliografia_list) + "</ul>"


            # Generar la estructura de la materia en HTML con los nuevos atributos
            html_output += f"""
                <div class="subject-box"
                    data-nombre="{nombre}"
                    data-semestre="{semestre}"
                    data-codigo="{codigo}" 
                    data-creditos="{creditos}" 
                    data-requisitos="{requisitos}" 
                    data-material="{material}"
                    data-bibliografia="{bibliografia}">
                    {nombre}
                </div>
            """

        html_output += "</div>"  # Cerrar la columna del semestre

    html_output += "</div>"  # Cerrar la fila del año

    return html_output

# ---------- USO DEL SCRIPT ----------
archivo_csv = 'jornada/static/docs/ac.csv'  # Ruta del CSV
año_deseado = 2  # Cambia el año según sea necesario

html_resultante = generar_html_ac(archivo_csv, año_deseado)

# Guardar en un archivo HTML
output_path = f'jornada/templates/jornada/año_{año_deseado}.html'
with open(output_path, 'w', encoding="utf-8") as file:
    file.write(html_resultante)

print(f"Archivo generado: {output_path}")