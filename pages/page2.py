import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input ,Output
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import dcc, html, callback, Output
import pathlib
import os 
# set pagetwo registry--------------------------------------------------------------------------------

dash.register_page(__name__,
                   path='/Departments',
                   name='Clinics Performance Report',
                   title='Clinics'
)
#load the data--------------------------------------------------------------------------------------
df=pd.read_excel('data\dataset.xlsx')

#------General Hospital Report ------------------------------------------------------------
#convert the date to datetime format-----------------------------------------------------------------------
df['Date']=pd.to_datetime(df['Date'])
#extract the month
df['Month']=df['Date'].dt.month_name()
df['year']=df['Date'].dt.year
#-----------------------------remove the white spaces
df.columns=df.columns.str.replace(" ","")
df=df.rename(columns={'CLINIC':'clinic','DOCTOR':'doctor','REVENUESCATEGORY':'revenue_category','CASH':'cash','CREDIT':'credit',
'TOTALREVENUES':'total_revenues','PATIENTS':'patients'})

layout=dbc.Container([
    dbc.Row(
        html.Marquee("Monthly Clinics Performance Dashboard-Designed by-Mohammed Bahageel-Data Analyst-the Information displayed is stricly confidential-This Report shows the Monthly Performance for each Clinic compared with last year"),
        style = {'color':'cyan'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='https://media0.giphy.com/media/hvDtUqsPbB2GNjhIdN/giphy.gif?cid=5e2148863a8ad0973c5d9deaa92353c6bbd932544462c74e&rid=giphy.gif&ct=g',top=True,bottom=False),
                dbc.CardBody([
                    html.H4('Abha Private Hospital',className='card-title'),
                    html.P('Choose The Clinc & the Revenue category:',className='card-text'),
                    dcc.Dropdown(id='selection_clinic',
                                 multi=False,
                                 options=[{'label':x,'value':x} for x in df['clinic'].unique()],
                                 value='الطوارئ',
                                 clearable=False ,style={'color': '#000000'}),
                    dcc.Dropdown(id='selection_op',
                                 multi=False,
                                 options=[{'label':x,'value':x} for x in df['revenue_category'].unique()],
                                 value='CONSULTATION ',
                                 clearable=False ,style={'color': '#000000'})
                ]),
            ])
        ],width=1,xs=12, sm=12, md=12, lg=5, xl=2),dbc.Col([
            html.Div(id='revenues')
        ],width=3,xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([html.Div(id='outpatvsinpts')],width=3,xs=12, sm=12, md=12, lg=6, xl=4),
        
    ]),
    html.Br(),
    dbc.Row([dbc.Col([html.Div(id='patientss')],width=6,xs=12, sm=12, md=12, lg=6, xl=6),dbc.Col([html.Div(id='cash_credits')],width=6,xs=12, sm=12, md=12, lg=6, xl=6)])
],fluid=True)


#the callback---------------------------------------------------------------------------------------------------------------------------------------------------------------
@callback(
    Output('revenues','children'),
    Output('outpatvsinpts','children'),
    Output('patientss','children'),
    Output('cash_credits','children'),
    Input('selection_op','value'),
    Input('selection_clinic','value'),
)
def update_graph(selected_category,selected_clinic):
    df22=df[(df['year']==2022)&(df['revenue_category']==selected_category)&(df['clinic']==selected_clinic)]
    df23=df[(df['year']==2023)&(df['revenue_category']==selected_category)&(df['clinic']==selected_clinic)]
    dfgroupedclincs22=df22.groupby(['Date','Month'])['total_revenues'].sum().reset_index('Date').sort_values('Date')
    dfgroupedclincs23=df23.groupby(['Date','Month'])['total_revenues'].sum().reset_index('Date').sort_values('Date')
    #plot the first chart-----------------------------------------------------------------------------------------
    dfgroupedclincs23['changes']=round(dfgroupedclincs23['total_revenues']/dfgroupedclincs22['total_revenues']-1,2)*100
    color2=np.where(dfgroupedclincs23['changes']>0,'green','red')
    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
    row_heights=[0.7,0.2] )
    fig.layout.template="plotly_dark"
    fig.add_trace(go.Scatter(x=dfgroupedclincs22.index,y=dfgroupedclincs22['total_revenues'],
                line=dict(color='#00FFFF'),line_shape='spline',
                name="Revenues in 2022"),
                row=1,col=1,secondary_y=False)
    fig.add_trace(go.Scatter(x=dfgroupedclincs23.index,y=dfgroupedclincs23['total_revenues'],line=dict(color='#66FF33'),line_shape='spline',
            name="Revenues in 2023"),row=1,col=1,secondary_y=False)
    fig.add_trace(go.Bar( x=dfgroupedclincs23.index,y=dfgroupedclincs23['changes'],marker_color=color2,name='change%')
                ,row=2,col=1,secondary_y=False)

    fig.update_layout(title=f'Total Revenues Of  {selected_category} --{selected_clinic}',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),

        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=True,
        legend=dict(orientation='h',yanchor='bottom',y=1.02, xanchor='right',x=1))
    fig.update_traces(xaxis='x2' )
    #plot the second chart -----------------------------------------------------------------------------------------------------------------------
    # plot the patients chart
    dfgroupedclincsp22=df22.groupby(['Date','Month'])['patients'].sum().reset_index('Date').sort_values('Date')
    dfgroupedclincsp23=df23.groupby(['Date','Month'])['patients'].sum().reset_index('Date').sort_values('Date')
    dfgroupedclincsp23['changes_patients']=round(dfgroupedclincsp23['patients']/dfgroupedclincsp22['patients']-1,2)*100
    color3=np.where(dfgroupedclincsp23['changes_patients']>0,'green','red')
    fig1=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
    row_heights=[0.7,0.2] )
    fig1.layout.template="plotly_dark"
    fig1.add_trace(go.Scatter(x=dfgroupedclincsp22.index,y=dfgroupedclincsp22['patients'],
                line=dict(color='#00FFFF'),line_shape='spline',
                name="Revenues in 2022"),
                row=1,col=1,secondary_y=False)
    fig1.add_trace(go.Scatter(x=dfgroupedclincsp23.index,y=dfgroupedclincsp23['patients'],line=dict(color='#66FF33'),line_shape='spline',
            name="Revenues in 2023"),row=1,col=1,secondary_y=False)
    fig1.add_trace(go.Bar( x=dfgroupedclincs23.index,y=dfgroupedclincsp23['changes_patients'],marker_color=color3,name='change%')
                ,row=2,col=1,secondary_y=False)

    fig1.update_layout(title=f'Total Patients of {selected_category}----{selected_clinic}',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),

        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02, xanchor='right',x=1))
    fig1.update_traces(xaxis='x2' )
    #plot the third graph---------------------------------------------------------------------------------------------------------------------------------------
    dfgrougedcash22=df22.groupby(['Month','Date'])['cash'].sum().reset_index('Date').sort_values('Date')
    dfgrougedcr22=df22.groupby(['Month','Date'])['credit'].sum().reset_index('Date').sort_values('Date')
    dfgrougedcash23=df23.groupby(['Month','Date'])['cash'].sum().reset_index('Date').sort_values('Date')
    dfgrougedcr23=df23.groupby(['Month','Date'])['credit'].sum().reset_index('Date').sort_values('Date')
    fig2=go.Figure()
    fig2.add_scatter(name='Total Monthly cash of 2022',x=dfgrougedcash22.index,y=dfgrougedcash22['cash']  ,line=dict(color='#66FF33'))
    fig2.add_scatter(name='Total Monthly credit  of 2022',x=dfgrougedcr22.index,y=dfgrougedcr22['credit'] ,line=dict(color='#e10600'))
    fig2.add_scatter(name='Total Monthly cash of 2023',x=dfgrougedcash23.index,y=dfgrougedcash23['cash']  ,line=dict(color='#66FF33',dash='dash'))
    fig2.add_scatter(name='Total Monthly credit of 2023',x=dfgrougedcr23.index,y=dfgrougedcr23['credit']  ,line=dict(color='#e10600',dash='dash'))
    fig2.update_layout(title=f'Credit and Cash portions of {selected_category} on Monthly Basis--{selected_clinic}',xaxis=dict(showgrid=True),
                       yaxis=dict(showgrid=True),hovermode='x unified',paper_bgcolor='#000000',
                    plot_bgcolor='#000000' ,legend=dict(yanchor='bottom',y=1.02,xanchor='right',x=1,orientation='h')) 
    fig2.layout.template='plotly_dark'
    fig2.update_traces(mode="lines",hoverinfo='all')
    #plot the last graph-------------------------------------------------------------------------------------------------------------------------------------------------
    df23inpat=df[(df['year']==2023)&(df['revenue_category']=='INPATIENTS ')&(df['clinic']==selected_clinic)]
    df23total=df[(df['year']==2023)&(df['revenue_category']=='TOTAL REVENUES ')&(df['clinic']==selected_clinic)]
    dfInpatients=df23inpat.groupby(['Month','Date'])['patients'].sum().reset_index('Date').sort_values('Date')
    dfTotal_outpatients=df23total.groupby(['Month','Date'])['patients'].sum().reset_index('Date').sort_values('Date')
    dfconversion=round(dfInpatients['patients']/dfTotal_outpatients['patients'] ,3)*100
    fig3=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
                   row_heights=[0.7,0.2] )

    fig3.layout.template="plotly_dark"

    fig3.add_trace(go.Bar(x=dfTotal_outpatients.index,y=dfTotal_outpatients['patients'],marker_color='cyan',
                name="Total Outpatients in 2023"),
                    row=1,col=1,secondary_y=False)
    fig3.add_trace(go.Bar(x=dfInpatients.index,y=dfInpatients['patients'],marker_color='red',
                    name="Inpatients in 2023"),row=1,col=1,secondary_y=False)
    fig3.add_trace(go.Scatter(x=dfTotal_outpatients.index,y=dfconversion,
                line=dict(color='#66FF33') ,
                    name="Conversion Rate"),
                    row=2,col=1,secondary_y=False)
    fig3.update_layout(title=f'Outpatients Vs Inpatients and Conversion Rates in 2023--{selected_clinic}',
                       xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
                    hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' 
                    ,showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))
    fig3.update_traces(xaxis='x2')
    return dcc.Graph(figure=fig),dcc.Graph(figure=fig3),dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)


    




