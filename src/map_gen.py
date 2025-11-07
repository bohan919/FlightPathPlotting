import pandas as pd
from plotly.colors import sample_colorscale
import plotly.graph_objects as go


class Flight_Path_Map:
    def __init__(self, df, colourmap='Agsunset', map_style='dark') -> None:
        self.df = df
        self.colourmap = colourmap
        self.map_style = map_style

        self.elev_norm = (df['elev'] - df['elev'].min()) / (df['elev'].max() - df['elev'].min())
        self.colors = sample_colorscale(self.colourmap, self.elev_norm.tolist())

        self.fig = go.Figure()

        pass

    def change_colourmap(self, new_colourmap='Agsunset'):
        self.colors = sample_colorscale(new_colourmap, self.elev_norm.tolist())

        return
    
    def change_map_style(self, new_map_style='dark'):
        '''
        Options: dark, carto-darkmatter-nolabels, light, carto-positron-nolabels, satellite, satellite-streets,  
        '''

        self.map_style = new_map_style

        return

    def create_figure(self, zoom:float = 8):

        for i in range(len(self.df) - 1):
            self.fig.add_trace(go.Scattermap(
                lat=[self.df.iloc[i]['lat'], self.df.iloc[i + 1]['lat']],
                lon=[self.df.iloc[i]['lon'], self.df.iloc[i + 1]['lon']],
                mode='lines',
                line=dict(width=4, color=self.colors[i]),
                hoverinfo='none',
                showlegend=False
            ))

        self.fig.update_layout(
            map=dict(
                style=self.map_style,
                zoom=zoom,
                center=dict(lat=self.df['lat'].mean(), lon=self.df['lon'].mean())
            ),
            showlegend=False,
            margin={"r":0,"l":0,"t":0,"b":0},
        )

        self.fig.show()

        return
    
    def add_title(self, flight_name:str, zoom:float=8):

        # Add annotation (title) at bottom center
        self.fig.add_annotation(
            text=flight_name,
            xref="paper", yref="paper",
            x=0.5, y=-0.05,  # y < 0 positions it below the plot
            showarrow=False,
            font=dict(size=30, color="white", family='Courier New'),
            align="center",
            bgcolor="black",  # white background
            bordercolor="black",
            borderwidth=0,
        )

        self.fig.update_layout(
            map=dict(
                style=self.map_style,
                zoom=zoom,
                center=dict(lat=self.df['lat'].mean(), lon=self.df['lon'].mean())
            ),
            showlegend=False,
            margin={"r":20,"l":20,"t":20,"b":80},

            shapes=[
                dict(
                    type="rect",
                    xref="paper",
                    yref="paper",
                    x0=-0.1, y0=-0.1,
                    x1=1.1, y1=1.1,
                    line=dict(color="black", width=4),
                    layer="below"
                )
            ],
            paper_bgcolor="black",  # Set background to white
            # plot_bgcolor="white",   # Set plot area to white
        )

        self.fig.show()

        return


    def save_figure(self, file_name:str = 'map_output.png', width=1920, height=1080, scale=2):

        print('Saving image...')
        self.fig.write_image(file_name, width=width, height=height, scale=scale)
        print('Done')

        return