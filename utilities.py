import plotly_express as px

def plot_function(plottyp, dataframe, xvar, yvar,func_name, func_title):
    if plottyp == "bar":
        fig = px.bar(title = func_title)
        fig.add_bar(x=dataframe[xvar], y=dataframe[yvar], name = func_name)
    elif plottyp == "line":
        fig = px.line(dataframe, x= xvar, y=yvar)
    else:
        print('Please fill in either "line" or "bar".')  
    return fig.show()