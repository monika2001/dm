from email.policy import default
from itertools import groupby
from select import select
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import ttk
from turtle import width
import pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import seaborn as sns

my_w=tk.Tk()
my_w.title('2019BTECS00017 : Assignment No. 1')
my_w.geometry("600x500")

menubar=tk.Menu(my_w)
menu_f=tk.Menu(menubar,tearoff=0)
menu_ct=tk.Menu(menubar,tearoff=0)
menu_disp=tk.Menu(menubar,tearoff=0)
menu_display=tk.Menu(menubar,tearoff=0)


menubar.add_cascade(label='Upload file',menu=menu_f)
trv=ttk.Treeview(my_w,selectmode= 'browse')
trv = ttk.Treeview(my_w, columns=10, show='headings', height=15)
trv.grid(row=1,column=2,columnspan=3,padx=50,pady=50)
trv['show'] = 'tree'
my_w['bg']='gray'
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")
menu_f.add_command(label='new',command=lambda:upload_file())

def upload_file():
    file=filedialog.askopenfilename()
    if(file):
        fob=open(file,'r')
        i=0
        for data in fob:
            trv.insert("",'end',iid=i,text=data)
            i=i+1
        menubar.add_cascade(label='Central tendancy',menu=menu_ct)
        menubar.add_cascade(label='Dispersion',menu=menu_disp)
        menubar.add_cascade(label='Display Plots',menu=menu_display)
        menu_ct.add_command(label='select',command=lambda:show_attribute())
        menu_disp.add_command(label='select',command=lambda:show_dispersion())
        menu_display.add_command(label='select',command=lambda:show_Plots())
        def show_attribute():
            if(file):
                fob=open(file,'r')
                data = pd.read_csv(file)
                cols = []
            for i in data:
                cols = data.columns
                clickedAttribute = StringVar()
                clickedAttribute.set("Select Attribute")
                dropCols = OptionMenu(my_w, clickedAttribute, *cols)
                dropCols.grid(column=1,row=5)
                measureOfCentralTendancies = ["Mean","Mode","Median","Midrange","Variance","Standard Deviation"]
                clickedMCT = StringVar()
                clickedMCT.set("Select central tendancy")
                dropMCT = OptionMenu(my_w, clickedMCT, *measureOfCentralTendancies)
                dropMCT.grid(column=2,row=5)
                Button(my_w,text="Compute",command= lambda:computeOperation()).grid(column=2,row=9)
        

                def computeOperation():
                    attribute = clickedAttribute.get()
                    operation = clickedMCT.get()
                    print(attribute)
                    if operation == "Mean":
                        sum = 0
                        for i in range(len(data)):
                            sum += data.loc[i, attribute]
                        avg = sum/len(data)
                        print("Mean of given dataset is (",attribute,") ",avg)
                        res = "Mean of given dataset is ("+attribute+") "+str(avg)
                        Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                    elif operation == "Mode": 
                        freq = {}
                        for i in range(len(data)):
                            freq[data.loc[i, attribute]] = 0
                        maxFreq = 0
                        maxFreqElem = 0
                        for i in range(len(data)):
                            freq[data.loc[i, attribute]] = freq[data.loc[i, attribute]]+1
                            if freq[data.loc[i, attribute]] > maxFreq:
                                maxFreq = freq[data.loc[i, attribute]]
                                maxFreqElem = data.loc[i, attribute]
                        print("Mode of given dataset is (",attribute,") ",maxFreqElem)
                        res = "Mode of given dataset is ("+attribute+") "+str(maxFreqElem)
                        Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                    elif operation == "Median":
                        n = len(data)
                        i = int(n/2)
                        j = int((n/2)-1)
                        arr = []
                        for i in range(len(data)):
                            arr.append(data.loc[i, attribute])
                        arr.sort()
                        if n%2 == 1:
                            print(arr[i])
                            res = "Median of given dataset is ("+attribute+") "+str(arr[i])
                            Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                        else:
                            print((arr[i]+arr[j])/2)
                            res = "Median of given dataset is ("+attribute+") "+str((arr[i]+arr[j])/2)
                            Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                    elif operation == "Midrange":
                        n = len(data)
                        arr = []
                        for i in range(len(data)):
                            arr.append(data.loc[i, attribute])
                        arr.sort()
                        print(arr)
                        print("Midrange:",(arr[n-1]+arr[0])/2)
                        res = "Midrange of given dataset is ("+attribute+") "+str((arr[n-1]+arr[0])/2)
                        Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                    elif operation == "Variance" or operation == "Standard Deviation":
                        sum = 0
                        for i in range(len(data)):
                            sum += data.loc[i, attribute]
                        avg = sum/len(data)
                        sum = 0
                        for i in range(len(data)):
                            sum += (data.loc[i, attribute]-avg)*(data.loc[i, attribute]-avg)
                        var = sum/(len(data))
                        if operation == "Variance":
                            print("Variance", var)
                            res = "Variance of given dataset is ("+attribute+") "+str(var)
                            Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                        else:
                            print("SD:",math.sqrt(var)) 
                            res = "Standard Deviation of given dataset is ("+attribute+") "+str(math.sqrt(var)) 
                            Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)

        def show_dispersion():
                if(file):
                    fob=open(file,'r')
                    data = pd.read_csv(file)
                    cols = []
                for i in data:
                    cols = data.columns
                    clickedAttribute = StringVar()
                    clickedAttribute.set("Select Attribute")
                    dropCols = OptionMenu(my_w, clickedAttribute, *cols)
                    dropCols.grid(column=1,row=5)
                    dispersionOfData = ["Range","Quartiles","Inetrquartile range","Minimum","Maximum"]
                    clickedDisp = StringVar()
                    clickedDisp.set("Select Dispersion")
                    dropDisp = OptionMenu(my_w, clickedDisp, *dispersionOfData)
                    dropDisp.grid(column=2,row=5)
                    Button(my_w,text="Compute",command= lambda:ComputeDispersion()).grid(column=2,row=6)
                    # trv.insert("",'end',iid=None,text=data)
        
                    def ComputeDispersion():
                        attribute = clickedAttribute.get()
                        operation = clickedDisp.get()
                        print(attribute)
                        if operation == "Range":
                            arr = []
                            for i in range(len(data)):
                                arr.append(data.loc[i, attribute])
                            arr.sort()
                            print("Range of given dataset is (",attribute,") ",(arr[len(data)-1]-arr[0]))
                            res = "Range of given dataset is ("+attribute+") "+str(arr[len(data)-1]-arr[0])
                            Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                        elif operation == "Quartiles" or operation == "Inetrquartile range": 
                            arr = []
                            for i in range(len(data)):
                                arr.append(data.loc[i, attribute])
                            arr.sort()
                            if operation == "Quartiles": 
                                print("Lower quartile (",attribute,") ",(len(arr)+1)/4)
                                res1 = "Lower quartile is ("+attribute+") "+str((len(arr)+1)/4)
                                res2 = "Middle quartile is ("+attribute+") "+str((len(arr)+1)/2)
                                res3 = "Upper quartile is ("+attribute+") "+str(3*(len(arr)+1)/4)
                                Label(my_w,text=res1,width=80,height=3,fg='blue').grid(column=1,row=7)
                                Label(my_w,text=res2,width=80,height=3,fg='blue').grid(column=1,row=8)
                                Label(my_w,text=res3,width=80,height=3,fg='blue').grid(column=1,row=9)
                            else:
                                print("Interquartile range of given dataset is (",attribute,") ",(len(arr)+1)/4)
                                res = "Interquartile range of given dataset is ("+attribute+") "+str((3*(len(arr)+1)/4)-((len(arr)+1)/4))
                                Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=8)
                                
                        elif operation == "Minimum" or operation == "Maximum":
                            arr = []
                            for i in range(len(data)):
                                arr.append(data.loc[i, attribute])
                            arr.sort()
                            if operation == "Minimum":
                                res = "Minimum value of given dataset is ("+attribute+") "+str(arr[0])
                                Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)
                            else:
                                res = "Maximum value of given dataset is ("+attribute+") "+str(arr[len(data)-1])
                                Label(my_w,text=res,width=80,height=3,fg='blue').grid(column=1,row=7)

        def show_Plots():
            if(file):
                    fob=open(file,'r')
                    data = pd.read_csv(file)
                    cols = []
            for i in data.columns:
                cols.append(i)
                clickedAttribute1 = StringVar()
                clickedAttribute1.set("Select Attribute 1")
                clickedAttribute2 = StringVar()
                clickedAttribute2.set("Select Attribute 2")
                clickedClass = StringVar()
                clickedClass.set("Select class")
                plots = ["Quantile Plot","Quantile-Quantile Plot","Histogram","Scatter Plot","Boxplot"]
                clickedPlot = StringVar()
                clickedPlot.set("Select Plot")
                dropPlots = OptionMenu(my_w, clickedPlot, *plots)
                dropPlots.grid(column=1,row=6)
                Button(my_w,text="Select Attributes",command= lambda:selectAttributes()).grid(column=2,row=6)


                def computePlotOperation():
                        attribute1 = clickedAttribute1.get()
                        attribute2 = clickedAttribute2.get()
                        
                        operation = clickedPlot.get()
                        if operation == "Quantile Plot":
                            pass
                        elif operation == "Quantile-Quantile Plot": 
                            pass     
                        elif operation == "Histogram": 
                            sns.set_style("whitegrid")
                            sns.FacetGrid(data, hue=clickedClass.get(), height=5).map(sns.histplot, attribute1).add_legend()
                            plt.title("Histogram")
                            plt.show(block=True)
                        elif operation == "Scatter Plot":
                            sns.set_style("whitegrid")
                            sns.FacetGrid(data, hue=clickedClass.get(), height=4).map(plt.scatter, attribute1, attribute2).add_legend()
                            plt.title("Scatter plot")
                            plt.show(block=True)
                        elif operation == "Boxplot":
                            sns.set_style("whitegrid")
                            sns.boxplot(x=attribute1,y=attribute2,data=data)
                            plt.title("Boxplot")
                            plt.show(block=True)
        
                def selectAttributes():
                    operation = clickedPlot.get()
                    if operation == "Quantile Plot":
                        pass
                    elif operation == "Quantile-Quantile Plot": 
                        pass     
                    elif operation == "Histogram":   
                        dropCols = OptionMenu(my_w, clickedAttribute1, *cols)
                        dropCols.grid(column=3,row=8,padx=20,pady=30)  
                        dropCols = OptionMenu(my_w, clickedClass, *cols)
                        dropCols.grid(column=5,row=8,padx=20,pady=30) 
                        Button(my_w,text="Compute",command= lambda:computePlotOperation()).grid(column=4,row=6)
                
                    elif operation == "Scatter Plot":
                        dropCols = OptionMenu(my_w, clickedAttribute1, *cols)
                        dropCols.grid(column=2,row=8,padx=20,pady=30)
                        dropCols = OptionMenu(my_w, clickedAttribute2, *cols)
                        dropCols.grid(column=3,row=8,padx=20,pady=30)
                        dropCols = OptionMenu(my_w, clickedClass, *cols)
                        dropCols.grid(column=5,row=8)
                        Button(my_w,text="Compute",command= lambda:computePlotOperation()).grid(column=4,row=6)
                        
                    elif operation == "Boxplot":
                        dropCols = OptionMenu(my_w, clickedAttribute1, *cols)
                        dropCols.grid(column=2,row=8,padx=20,pady=30)
                        dropCols = OptionMenu(my_w, clickedAttribute2, *cols)
                        dropCols.grid(column=3,row=8,padx=20,pady=30)
                        Button(my_w,text="Compute",command= lambda:computePlotOperation()).grid(column=4,row=6)

my_w.config(menu=menubar)

my_w.mainloop()
