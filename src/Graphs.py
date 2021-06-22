import plotly.graph_objects as go
import numpy as np
import pandas as pd

class Graphs:

    def __init__(self, currency=None):
        self._currency = currency
        self._missing_dates = {}

    def update_currency(self, currency):
        self._currency = currency

        return None

    def _filter_missing_dates(self, data, timeframe):

        if timeframe not in self._missing_dates:

            # build complete timeline from start date to end date
            dt_all = pd.date_range(start=data['time'].iloc[0],end=data['time'].iloc[-1])

            # retrieve the dates that ARE in the original datset
            original_dates = [d.strftime("%Y-%m-%d") for d in data['time']]

            # define dates with missing values
            break_dates = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in original_dates]

            self._missing_dates[timeframe] = break_dates

        return self._missing_dates[timeframe]

    def _filter_data(self, data, start_time):
        return data[data['time'] >= start_time]

    def _candlestick_text(self, candlestick_info):

        return f"Open: {candlestick_info['open']:.5f}<br>" + \
                f"High: {candlestick_info['high']:.5f}<br>" + \
                f"Low: {candlestick_info['low']:.5f}<br>" + \
                f"Close: {candlestick_info['close']:.5f}<br>" + \
                f"Width: {candlestick_info['pip_difference']}"

    def _draw_hline(self, fig, y_val, line_dash, line_col, annotation=None):

        fig.add_hline(
            y=y_val,
            line_dash=line_dash,
            line_color=line_col,
            annotation_text=annotation or '',
            line_width=3
        )
        
        return None

    def plot_atr(self, data):
        
        atr_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['atr'],
                mode="lines"
            )
        ])

        atr_fig.update_layout(
            title=f"{self._currency} - ATR (Current value: {data['atr'].iloc[-1]})",
            template='simple_white',
            xaxis_title="Time",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False,
            yaxis={'visible': False, 'showticklabels': False}
        )

        return atr_fig

    def plot_tick_volume_fullday(self, data, start_time):

        data = self._filter_data(data.copy(), start_time)

        tick_vol_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['tick_volume'],
                mode="lines+markers"
            )
        ])

        tick_vol_fig.update_layout(
            title=f"{self._currency} - Tick Volume for today",
            xaxis_title="Time",
            yaxis_title="Volume",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return tick_vol_fig

    def plot_heatmap_fullday(self, data, start_time):

        data = self._filter_data(data.copy(), start_time)

        info_text = 'Time: %{x}<br><br>' + \
            'Open price: %{customdata[0]:.5f}<br>' + \
            'Close price: %{customdata[1]:.5f}<br>' + \
            '% Change: %{z:.3f}<br><br>' + \
            'High price: %{customdata[2]:.5f}<br>' + \
            'Low price: %{customdata[3]:.5f}<br><extra></extra>'
            
        customdata_list = np.dstack(
            (data['open'], data['close'], data['high'], data['low'])
        )

        heatmap_fig = go.Figure(
            data=go.Heatmap(
                customdata=customdata_list,
                z=[data['price_percentage_change']],
                y=None,
                x=data['time'],
                zmin=-0.25,
                zmax=0.25,
                colorscale='rdylgn',
                hovertemplate= info_text
            )
        )

        heatmap_fig.update_layout(
            title=f"{self._currency} - Heatmap for price changes today",
            xaxis_title="Time",
            hovermode='x',
        )

        heatmap_fig.update_yaxes(showticklabels=False)

        return heatmap_fig

    def plot_percentage_change(self, data, start_time):

        data = self._filter_data(data.copy(), start_time)

        percentage_change_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['price_percentage_change']
            )
        ])

        percentage_change_fig.update_layout(
            title=f"{self._currency} - Price Percentage Change for today",
            xaxis_title="Time",
            yaxis_title="Percentage change",
            hovermode='x',
            yaxis_tickformat='.3f'
        )

        self._draw_hline(percentage_change_fig, 0, "solid", "black")

        percentage_change_fig.add_hrect(
            y0=0.03, 
            y1=-0.03,
            fillcolor="#D55A5A",
            annotation_text="Less activity zone",
            annotation_position="outside bottom left",
            layer="below", 
            opacity=0.25
        )

        return percentage_change_fig

    def plot_candlesticks_fullday(self, data_day, start_time, indicators_df, timeframe):

        hover_list= data_day.apply(lambda data_row:self._candlestick_text(data_row), axis=1)

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close'],
                    text=hover_list,
                    hoverinfo='text'
                ),
                go.Scatter(
                    x=indicators_df['time'], 
                    y=indicators_df['sma'],
                    line=dict(color='black', width=5),
                    name=""
                )
            ]
        )

        candlesticks_minute_fig.update_layout(
            title=f"{self._currency} - Series ({timeframe})",
            template='simple_white',
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False,
            yaxis={'visible': False, 'showticklabels': False}
        )

        candlesticks_minute_fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=self._filter_missing_dates(data_day, timeframe)
                )
            ]
        )
        
        candlesticks_minute_fig.add_vline(
            x=start_time,
            line_dash="solid",
            line_color="black",
            line_width=3
        )

        return candlesticks_minute_fig

    def plot_rsi_figure(self, rsi_today):

        rsi_fig = go.Figure([
            go.Scatter(
                x=rsi_today['time'], 
                y=rsi_today['value'],
                mode="lines"
            )
        ])

        rsi_fig.update_layout(
            template='simple_white',
            xaxis_title="Time",
            yaxis_title="RSI Value",
            title=f"RSI of {self._currency}",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        rsi_fig.add_hrect(
            y0=0, 
            y1=30,
            fillcolor="palegreen",
            layer="below", 
            opacity=0.25
        )

        rsi_fig.add_hrect(
            y0=100, 
            y1=70,
            fillcolor="palegreen",
            layer="below", 
            opacity=0.25
        )

        self._draw_hline(rsi_fig, 50, "solid", "black")

        rsi_fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=self._filter_missing_dates(rsi_today, '1H')
                )
            ]
        )

        return rsi_fig