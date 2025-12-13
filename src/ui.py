import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timezone, timedelta

class UI:

    def prepare_data(self, earthquake):
        
        self.data = pd.DataFrame([
            {
                "lon": row["geometry"]["coordinates"][0],
                "lat": row["geometry"]["coordinates"][1],
                "depth": row["geometry"]["coordinates"][2],
                "mag": row['properties']['mag'],
                "place": row['properties']['place'],
                "time": datetime.fromtimestamp(row['properties']['time']/1000, tz=timezone.utc).strftime("%H:%M:%S %d-%m-%Y")
            }
            for row in earthquake.data["features"]
        ])

        return self.data
    
    def filter_data(self, min_mag=0, date=None):

        filtered = self.data[self.data["mag"] >= min_mag]

        if date is not None:
            filtered = filtered[filtered["time"].apply(lambda x: x.split()[1]).isin([date])]

        self.data = filtered

        return self.data

    def map(self, earthquake, min_mag=0, date=None):
        
        self.data = self.prepare_data(earthquake)
        self.data = self.filter_data(min_mag, date)

        if self.data.empty:
            st.warning("No hay terremotos que cumplan el filtro.")
            return
        
        fig = px.scatter_mapbox(
            self.data,
            lat="lat",
            lon="lon",
            size="mag",
            color="mag",
            hover_name="place",
            hover_data={"depth": True, "time": True, "lat": False, "lon": False},
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=25,
            zoom=1,
            mapbox_style="open-street-map"
        )
        st.plotly_chart(fig, width="stretch")

    def core(self, earthquake):
        st.title("Visualizador de Terremotos 🌍")

        if st.button("Actualizar datos"):
            earthquake.connect()

        min_mag = st.slider("Magnitud mínima", 0.0, 10.0, 2.5, 0.1)

        date = st.selectbox(
            label="Seleccionar fechas para mostrar",
            options=[
                (datetime.today() - timedelta(days=i)).strftime("%d-%m-%Y") for i in range(7)
            ]
        )
        
        if earthquake.data is None:
            st.info("No hay datos disponibles. Pulsa 'Actualizar datos'.")
            return

        self.map(earthquake, min_mag, date)
