from dash import dcc, html, callback,Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
app=Dash(__name__)
df=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('SpaceX Launch Records Dashboard',
            style={'padding-left':'40vw','font':'Arial Black','color':'BLACK','font-weight':'bold','font-size':30,'text-decoration':'underline'})]
            ,width={'size':3}),
        dbc.Col([
        dcc.Dropdown(id='SITES', multi= False,
        options=df['Launch Site'].unique(),
        # value='CCAFS LC-40',
        placeholder='Select Launch Site',
        style={'color':'black',"font-weight":'bold',
        'font-size':'22px','margin-bottom':'20px'})],width={'size':4})]),
    dbc.Row(
        dbc.Col([
        dcc.Graph(id='pie',style={'padding-left':'30vw','width': '45vw','height':'45vh','display':'inline-block'})],
    )),
    dbc.Row(dbc.Col([dcc.RangeSlider(0,10000,2500,value=[0,2500],id='slider')])),
    dbc.Row(
        dbc.Col([
        dcc.Graph(id='SCATTER',
        style={'padding-left':'30px','width': '95vw','height':'40vh','display':'inline-block'})])),
    dcc.Store(id='session', storage_type='session'),
],style={'height':'200vh'},fluid=True)
dx=df.copy()
@app.callback(
    Output('pie','figure'),
    Input('SITES','value')
 )
def pie_graph(site):
    global dx
    if site is None:
        piechart=px.pie(data_frame=df,values='class',names='Launch Site',color='Launch Site',
        hover_name='Launch Site')
        # piechart.update_layout(title_x=0.5,title_y=0.05,
        # font={'family':'Arial','size':18,},title_font_size=20,
        # showlegend=False)
        # labels={'TOP LEVEL':'BUILD COST'},
        # title='<b>'+x+' <b>BUILD COSTS',template='presentation')
        # piechart.update_traces(text=df['class'].map("${:,.1f}".format),textinfo='label+text+percent',
        # texttemplate = '<b>%{label}</br></br>%{text}</b></br>%{percent}</b>',textposition='auto')
    else:
        dx=df.loc[df['Launch Site']==site]
        piechart=px.pie(data_frame=dx,values='class',names='Booster Version',color='Booster Version',
        hover_name='Booster Version')
        # piechart.update_layout(title_x=0.5,title_y=0.05,
        # font={'family':'Arial','size':18,},title_font_size=20,
        # showlegend=False)
    # labels={'TOP LEVEL':'BUILD COST'},
    # title='<b>'+x+' <b>BUILD COSTS',template='presentation')
    # piechart.update_traces(text=dx[x].map("${:,.1f}".format),textinfo='label+text+percent',
    # texttemplate = '<b>%{label}</br></br>%{text}</b></br>%{percent}</b>',textposition='auto')
    return piechart
@app.callback(
    Output('SCATTER','figure'),
    Input('slider','value')
)
def table(payload):
    global dx
    dz=dx.loc[(payload[0]<dx['Payload Mass (kg)']) & (dx['Payload Mass (kg)']<payload[1])]
    dz['class']=dz['class'].astype(str)
    SCATTER=px.scatter(dz,x='Payload Mass (kg)',y='class',color='class',hover_data=['class'])
    return SCATTER
if __name__ == '__main__':
    app.run_server()