from app import app

import pandas as pd
#import chart_studio.plotly as py
#import plotly.figure_factory as ff
import plotly.express as px
#import dash
from dash import dcc, html
from dash.dependencies import Input, Output



# Set Plotly credentials
#py.plotly.tools.set_credentials_file(username='rosaaortega', api_key='vxt1WtiwSC0pRQ3sawpa')

# Load data from Excel
file_path = "tabla_transformada.xlsx"  # Update with your actual file path
df = pd.read_excel(file_path)


# Ensure months are sorted correctly
month_order = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]
df["Mes"] = pd.Categorical(df["Mes"], categories=month_order, ordered=True)

# Layout de la app
app.layout = html.Div([
    html.H1("Ingreso Mensual por Año", style={"textAlign": "center"}),

    # Checkbox para seleccionar múltiples industrias
    dcc.Checklist(
        id="industry_selector",
        options=[{"label": i, "value": i} for i in df["Industria"].unique()],
        value=[df["Industria"].unique()[0]],  # Industria por defecto seleccionada
        inline=True
    ),

    # Gráfico de líneas
    dcc.Graph(id="line_chart")
])

# Callback para actualizar el gráfico
@app.callback(
    Output("line_chart", "figure"),
    [Input("industry_selector", "value")]
)
def update_chart(selected_industries):
    # Filtrar los datos por industrias seleccionadas
    df_filtered = df[df["Industria"].isin(selected_industries)]

    # Agrupar por mes y año, sumando los montos
    df_grouped = df_filtered.groupby(["Año","Mes"], as_index=False)["Monto"].sum()

    # Crear la gráfica
    fig = px.line(df_grouped, x="Mes", y="Monto", color="Año",
                  title="Ingreso Mensual Total",
                  )
    # Publicar en Chart Studio
    #py.plot(fig, filename='ingresos-por-sector', auto_open=True)

    return fig

# Ejecutar la app
if __name__ == "__main__":
    app.run_server(debug=True)
