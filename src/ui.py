import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timezone

class UI:

    def prepare_data(self, earthquake, min_mag=0):
        
        data = pd.DataFrame([
            {
                "lon": row["geometry"]["coordinates"][0],
                "lat": row["geometry"]["coordinates"][1],
                "depth": row["geometry"]["coordinates"][2],
                "mag": row['properties']['mag'],
                "place": row['properties']['place'],
                "time": datetime.fromtimestamp(row['properties']['time']/1000, tz=timezone.utc).strftime("%H:%M:%S %d-%m-%Y")
            }
            for row in earthquake.data["features"]
            if row['properties']['mag'] >= min_mag
        ])

        return data

    def map(self, earthquake, min_mag=0):
        
        data = self.prepare_data(earthquake, min_mag)

        if data.empty:
            st.warning("No hay terremotos que cumplan el filtro.")
            return
        
        fig = px.scatter_mapbox(
            data,
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
        min_mag = st.slider("Magnitud mínima", 0.0, 10.0, 2.5, 0.1)
        self.map(earthquake, min_mag)
