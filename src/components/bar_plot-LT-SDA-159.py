import plotly.express as px


def build_plot(df, h=0):
    x = df.columns[0]
    y = df.columns[1]
    
    top_ten = df.groupby([x]).sum(y).sort_values(y, ascending=False).head(10)
    top_ten.reset_index(inplace=True)
    #top_ten["y_r"] = top_ten[y].round(2)
    top_ten[y] = top_ten[y].round(2)
    top_ten["x_s"] = top_ten[x].apply(lambda x: x[:12]+"...")

    title = f"Top 10 {x} by {y}"

    if h==0:
        fig = px.bar(top_ten, x="x_s", y=y, color=x, text_auto=".3s", title=title, height=600, width=960, hover_name=x, hover_data={"x_s": False, x: False, y: ':.2fk'}) # type: ignore
        fig.update_layout(showlegend=False, xaxis_title=x) 
    else:
        top_ten.sort_values(y, ascending=True, inplace=True)
        fig = px.bar(top_ten, y="x_s", x=y, color=x, text_auto=".3s", title=title, height=600, width=960, hover_name=x, hover_data={"x_s": False, x: False, y: ':.2fk'}) # type: ignore
        fig.update_layout(showlegend=False, yaxis_title=x)
        fig.update_layout(title={"yref": "paper", "y" : 1, "yanchor" : "bottom"})
    return fig
