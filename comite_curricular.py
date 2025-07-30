import pandas as pd
# Leer el archivo CSV
csv_path = 'jornada/static/docs/comite_curricular.csv'
data = pd.read_csv(csv_path)

# Iniciar la estructura de la tabla en HTML
html_table = """
<table class="table table-striped table-bordered">
    <thead class="table-light">
        <tr>
            <th scope="col">N°</th>
            <th scope="col">Nombre</th>
            <th scope="col">Cargo</th>
            <th scope="col">E-mail</th>
        </tr>
    </thead>
    <tbody>
"""

# Crear filas de la tabla a partir del CSV
for index, row in data.iterrows():
    html_table += f"""
        <tr>
            <td>{index + 1}</td>
            <td>{row['Nombre']}</td>
            <td>{row['Cargo']}</td>
            <td><a href="mailto:{row['E-mail']}">{row['E-mail']}</a></td>
        </tr>
    """

# Cerrar la tabla
html_table += """
    </tbody>
</table>
"""

# Guardar el HTML en un archivo
output_path = 'jornada/templates/jornada/comite-curricular.html'  # Cambiar si es necesario
with open(output_path, 'w') as file:
    file.write(html_table)

output_path
