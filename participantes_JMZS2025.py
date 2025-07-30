import csv

def generar_tabla_html(csv_file, output_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        # Crear el inicio de la tabla
        file.write('<table id="participantsTable" class="table table-striped table-bordered table-hover" style="width:100%">\n')
        file.write('    <thead class="table-primary">\n')
        file.write('        <tr>\n')
        file.write('            <th>N°</th>\n')
        file.write('            <th>Nombre</th>\n')
        file.write('            <th>Sesión</th>\n')
        file.write('            <th>Institución</th>\n')
        file.write('            <th>E-mail</th>\n')
        file.write('        </tr>\n')
        file.write('    </thead>\n')
        file.write('    <tbody>\n')

        # Agregar filas
        for i, row in enumerate(rows, start=1):
            file.write('        <tr>\n')
            file.write(f'           <td>{i}</td>\n')
            file.write(f'           <td>{row["Nombre"]}</td>\n')
            file.write(f'           <td>{row["Sesión"]}</td>\n')
            file.write(f'           <td>{row["Institución"]}</td>\n')
            file.write(f'           <td><a href="mailto:{row["E-mail"]}">{row["E-mail"]}</a></td>\n')
            file.write('        </tr>\n')

        # Cerrar la tabla
        file.write('    </tbody>\n')
        file.write('</table>\n')

# Ejemplo de uso
generar_tabla_html('jornada/static/docs/lista_participantes.csv', 'jornada/templates/jornada/tabla_participantes.html')
