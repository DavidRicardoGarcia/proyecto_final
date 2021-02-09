#!/usr/bin/python
from pychartdir import *
import datetime

class gantt_diagram:
    def __init__(self,fechai,fechaf):
        self.taskno=[]
        self.startDate = []
        self.endDate = []
        self.labels = []
        self.fecha_inicio=fechai
        self.fecha_final=fechaf
        self.colors=[0x00cc00, 0x00cc00, 0x00cc00, 0x0000cc, 0x0000cc, 0xcc0000, 0xcc0000, 0x0000cc, 0xcc0000,
        0xcc0000, 0x00cc00, 0xcc0000, 0x57A336,0x54644D,0x5C4D64]
        self.c = XYChart(1200,1000, 0xccccff, 0x000000, 1)
        self.c.addTitle("Diagrama de Gantt Punta Delicias", "timesbi.ttf", 15, 0xffffff).setBackground(0x000080)
        self.c.setPlotArea(120, 150, 1000, 700, 0xffffff, 0xeeeeee, LineColor, 0xc0c0c0, 0xc0c0c0).setGridWidth(2, 1, 1, 1)
        self.c.swapXY()
        self.c.yAxis().setDateScale(chartTime((self.fecha_inicio.year), (self.fecha_inicio.month), (self.fecha_inicio.day),0), chartTime((self.fecha_final.year), (self.fecha_final.month), (self.fecha_final.day),24), 86400/24)
        self.c.yAxis().setMultiFormat(StartOfDayFilter(), "<*font=arialbd.ttf*>{value|dd}",StartOfHourFilter(), "-{value|h}")



    def cargar_datos(self,a):

        #cargar los labels, startDate y endDate
        cont=0
        for x in a:
            self.labels.append(x['TIPO'])
            if(x['Actividad']):
                for i in x['Actividad']:
                    fechainicio=datetime.datetime.strptime(i['TAREA']['fecha inicio'],'%m %d %Y')
                    año=fechainicio.year
                    mes=fechainicio.month
                    dia=fechainicio.day
                    self.startDate.append(chartTime(año,mes,dia,i['HINICIO']))
                    #print((2020,10,0+i['DIA'],i['HINICIO']))
                    diasextras=int(i['HORAS']/24)
                    horafinal=i['HORAS']%24
                    if(i['TAREA']['fecha finalizacion']=='---'):
                        self.endDate.append(chartTime(año,mes,dia,i['HINICIO']+horafinal))
                    else:    
                        fechafin=datetime.datetime.strptime(i['TAREA']['fecha finalizacion'],'%m %d %Y')
                        año=fechafin.year
                        mes=fechafin.month
                        dia=fechafin.day
                        self.endDate.append(chartTime(año,mes,dia,i['HINICIO']+horafinal))
                    #print((2020,10,0+i['DIA']+diasextras,i['HINICIO']+horafinal))
                    self.taskno.append(cont)
            else:
                self.startDate.append(chartTime((self.fecha_inicio.year), (self.fecha_inicio.month), (self.fecha_inicio.day),0))
                self.endDate.append(chartTime((self.fecha_inicio.year), (self.fecha_inicio.month), (self.fecha_inicio.day),0))
                self.taskno.append(cont)
            cont+=1


                
    def graficar(self):
        # Set the y-axis to shown on the top (right + swapXY = top)
        self.c.setYAxisOnRight()

        # Set the labels on the x axis
        self.c.xAxis().setLabels(self.labels)

        # Reverse the x-axis scale so that it points downwards.
        self.c.xAxis().setReverse()

        # Set the horizontal ticks and grid lines to be between the bars
        self.c.xAxis().setTickOffset(0.5)

        # Add a green (33ff33) box-whisker layer showing the box only.
        layer = self.c.addBoxWhiskerLayer2(self.startDate, self.endDate, None, None, None,self.colors)
        layer.setXData(self.taskno)
        layer.setBorderColor(SameAsMainColor)

        # Divide the plot area height ( = 200 in this chart) by the number of tasks to get the height of
        # each slot. Use 80% of that as the bar height.
        layer.setDataWidth(int(200 * 4 / 5 / len(self.labels)))
        #layer.setDataWidth(int(200 * 4 / 5 / len(self.labels)))
        # Output the chart
        self.c.makeChart("prueba.png")
