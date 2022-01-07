from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
from src.ElliotWaves.misc.point import point

class candle_chart:
    def __init__(self,df: pd.DataFrame) -> None:
        self.fig = go.Figure(data=[go.Candlestick(x=df.index,
            open= df['O'],
            high= df['H'],
            low=  df['L'],
            close=df['C'])])
        self.fig.update_yaxes(fixedrange=False)
        self.fig.update_layout(height=1000)
        self.max = df.H.max()
        self.min = df.L.min()
        pass

    def add_marker(self, marker_candle:pd.Series)->candle_chart:
        self.fig.add_shape(type="line",
            x0=marker_candle.name, x1=marker_candle.name, y0=self.min, y1=marker_candle["L"],
            line=dict(
                color="MediumPurple",
                width=4,
                dash="dot",
            )
        )

        self.fig.add_shape(type="line",
            x0=marker_candle.name, x1=marker_candle.name, y0=marker_candle["H"], y1=self.max,
            line=dict(
                color="MediumPurple",
                width=4,
                dash="dot",
            )
        )
        return self
    
    def add_wave_from_point(self, start_point: point, end_point:point, main_wave: bool = True)->candle_chart:
        return self.add_wave(start_point.timestamp,start_point.price,end_point.timestamp,end_point.price,main_wave)
        
    def add_wave(self, start_dt:pd.Timestamp, start_value:float, end_dt:pd.Timestamp, end_value:float, main_wave: bool = True)->candle_chart:
        if end_value > start_value:
            color = "Green"
        else:
            color = "Red"
        if main_wave:
            dash = "solid"
        else:
            dash = "dashdot"
        self.fig.add_shape(type="line",
            x0=start_dt, x1=end_dt, y0=start_value, y1=end_value,
            line=dict(
                color=color,
                width=2,
                dash=dash,
            )
        )
        return self
    
    def show(self):
        self.fig.show()