from tkinter import *
from tkinter import filedialog
import pandas as pd
import math
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def SolveAssignment(assignment):
    
    if assignment == "Assignment1" or assignment == "Assignment2":
        def browseDataset():
            filename = filedialog.askopenfilename(initialdir="/",title="Select dataset", filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))
            label_file_explorer.configure(text="File Opened: "+filename)
            newfilename = ''
            for i in filename:
                if i == "/":
                    newfilename = newfilename + "/"
                newfilename = newfilename + i
            data = pd.read_csv(filename)
            d = pd.read_csv(filename)
                
            if assignment == "Assignment1":
                window1 = Tk()
                window1.title("Assignment1")
                window1.geometry("300x300")
                menubar = Menu(window1)
                questions = Menu(menubar, tearoff = 0)
                menubar.add_cascade(label ='Topics', menu = questions)
                questions.add_command(label ='Data Display', command = lambda: SolveQuestion("Data Display"))
                questions.add_command(label ='Measure of central tendencies', command = lambda: SolveQuestion("Measure of central tendencies"))
                questions.add_command(label ='Dispersion of data', command = lambda: SolveQuestion("Dispersion of data"))
                questions.add_command(label ='Plots', command = lambda: SolveQuestion("Plots"))
                Label(window1,text="Select Topic from Menu",fg="red",bg="yellow",height=4).grid(row=0,column=0,padx=20,pady=30)
                def SolveQuestion(question):
                    if question == "Data Display":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        trv=ttk.Treeview(window2, columns=10, show='headings', height=15)
                        trv.grid(row=3,column=1,columnspan=6,padx=20,pady=20)
                        trv['show'] = 'tree'
                        fob = open(newfilename, 'r')
                        i=0
                        for d in fob:
                            # d = str(i) + ',' + d
                            # arr = d.split(',')
                            # arr.insert(0,i)
                            # d = tuple(arr)
                            # print(d)
                            # trv.insert("",'end',iid=i,values=d)
                            trv.insert("",'end',iid=i,text=d)
                            i=i+1
                        window2.mainloop()
                    elif question == "Measure of central tendencies":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute = StringVar(window2)
                        clickedAttribute.set("Select Attribute")
                        dropCols = OptionMenu(window2, clickedAttribute, *cols)
                        dropCols.grid(column=1,row=5,padx=20,pady=30)
                        measureOfCentralTendancies = ["Mean","Mode","Median","Midrange","Variance","Standard Deviation"]
                        clickedMCT = StringVar(window2)
                        clickedMCT.set("Select MCT")
                        dropMCT = OptionMenu(window2, clickedMCT, *measureOfCentralTendancies)
                        dropMCT.grid(column=2,row=5)
                        Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=2,row=7,padx=20,pady=30)

                        def computeOperation():
                            attribute = clickedAttribute.get()
                            operation = clickedMCT.get()
                            if operation == "Mean":
                                sum = 0
                                for i in range(len(data)):
                                    sum += data.loc[i, attribute]
                                avg = sum/len(data)
                                res = "Mean of given dataset is ("+attribute+") "+str(avg)
                                Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
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
                                res = "Mode of given dataset is ("+attribute+") "+str(maxFreqElem)
                                Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                            elif operation == "Median":
                                n = len(data)
                                i = int(n/2)
                                j = int((n/2)-1)
                                arr = []
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute])
                                arr.sort()
                                if n%2 == 1:
                                    res = "Median of given dataset is ("+attribute+") "+str(arr[i])
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                                else:
                                    res = "Median of given dataset is ("+attribute+") "+str((arr[i]+arr[j])/2)
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                            elif operation == "Midrange":
                                n = len(data)
                                arr = []
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute])
                                arr.sort()
                                res = "Midrange of given dataset is ("+attribute+") "+str((arr[n-1]+arr[0])/2)
                                Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
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
                                    res = "Variance of given dataset is ("+attribute+") "+str(var)
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                                else:
                                    res = "Standard Deviation of given dataset is ("+attribute+") "+str(math.sqrt(var)) 
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)  
                        window2.mainloop()
                    elif question == "Dispersion of data":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute = StringVar(window2)
                        clickedAttribute.set("Select Attribute")
                        dropCols = OptionMenu(window2, clickedAttribute, *cols)
                        dropCols.grid(column=1,row=5,padx=20,pady=30)
                        dispersionOfData = ["Range","Quartiles","Inetrquartile range","Minimum","Maximum"]
                        clickedDispersion = StringVar(window2)
                        clickedDispersion.set("Select Dispersion Operation")
                        dropDisp = OptionMenu(window2, clickedDispersion, *dispersionOfData)
                        dropDisp.grid(column=2,row=5)
                        Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=2,row=7,padx=20,pady=30)
                        
                        def computeOperation():
                            attribute = clickedAttribute.get()
                            operation = clickedDispersion.get()
                            if operation == "Range":
                                arr = []
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute])
                                arr.sort()
                                res = "Range of given dataset is ("+attribute+") "+str(arr[len(data)-1]-arr[0])
                                Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                            elif operation == "Quartiles" or operation == "Inetrquartile range": 
                                arr = []
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute])
                                arr.sort()
                                if operation == "Quartiles": 
                                    res1 = "Lower quartile(Q1) is ("+attribute+") "+str((len(arr)+1)/4)
                                    res2 = "Middle quartile(Q2) is ("+attribute+") "+str((len(arr)+1)/2)
                                    res3 = "Upper quartile(Q3) is ("+attribute+") "+str(3*(len(arr)+1)/4)
                                    Label(window2,text=res1,width=80,height=3,fg='green').grid(column=1,row=7)
                                    Label(window2,text=res2,width=80,height=3,fg='green').grid(column=1,row=8)
                                    Label(window2,text=res3,width=80,height=3,fg='green').grid(column=1,row=9)
                                else:
                                    res = "Interquartile range(Q3-Q1) of given dataset is ("+attribute+") "+str((3*(len(arr)+1)/4)-((len(arr)+1)/4))
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=8)
                                    
                            elif operation == "Minimum" or operation == "Maximum":
                                arr = []
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute])
                                arr.sort()
                                if operation == "Minimum":
                                    res = "Minimum value of given dataset is ("+attribute+") "+str(arr[0])
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                                else:
                                    res = "Maximum value of given dataset is ("+attribute+") "+str(arr[len(data)-1])
                                    Label(window2,text=res,width=80,height=3,fg='green').grid(column=1,row=7)
                        window2.mainloop()
                    elif question == "Plots":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute1 = StringVar(window2)
                        clickedAttribute1.set("Select Attribute 1")
                        clickedAttribute2 = StringVar(window2)
                        clickedAttribute2.set("Select Attribute 2")
                        clickedClass = StringVar(window2)
                        clickedClass.set("Select class")
                        plots = ["Quantile-Quantile Plot","Histogram","Scatter Plot","Boxplot"]
                        clickedPlot = StringVar(window2)
                        clickedPlot.set("Select Plot")
                        dropPlots = OptionMenu(window2, clickedPlot, *plots)
                        dropPlots.grid(column=1,row=6,padx=20,pady=30)
                        Button(window2,text="Select Attributes",command= lambda:selectAttributes()).grid(column=2,row=6,padx=20,pady=30)
                        
                        def computeOperation():
                            attribute1 = clickedAttribute1.get()
                            attribute2 = clickedAttribute2.get()
                            
                            operation = clickedPlot.get()
                            if operation == "Quantile-Quantile Plot": 
                                arr = []
                                sum = 0
                                for i in range(len(data)):
                                    arr.append(data.loc[i, attribute1])  
                                    sum += data.loc[i, attribute1]
                                avg = sum/len(arr)
                                sum = 0
                                for i in range(len(data)):
                                    sum += (data.loc[i, attribute1]-avg)*(data.loc[i, attribute1]-avg)
                                var = sum/(len(data))
                                sd = math.sqrt(var)
                                z = (arr-avg)/sd
                                stats.probplot(z, dist="norm", plot=plt)
                                plt.title("Normal Q-Q plot")
                                plt.show()
                                
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
                            if operation == "Quantile-Quantile Plot":
                                dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                                dropCols.grid(column=3,row=8,padx=20,pady=30)  
                                Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
                            
                            elif operation == "Histogram":   
                                dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                                dropCols.grid(column=3,row=8,padx=20,pady=30)  
                                dropCols = OptionMenu(window2, clickedClass, *cols)
                                dropCols.grid(column=5,row=8,padx=20,pady=30) 
                                Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
                        
                            elif operation == "Scatter Plot":
                                dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                                dropCols.grid(column=2,row=8,padx=20,pady=30)
                                dropCols = OptionMenu(window2, clickedAttribute2, *cols)
                                dropCols.grid(column=3,row=8,padx=20,pady=30)
                                dropCols = OptionMenu(window2, clickedClass, *cols)
                                dropCols.grid(column=5,row=8)
                                Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)

                            elif operation == "Boxplot":
                                dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                                dropCols.grid(column=2,row=8,padx=20,pady=30)
                                dropCols = OptionMenu(window2, clickedAttribute2, *cols)
                                dropCols.grid(column=3,row=8,padx=20,pady=30)
                                Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=4,row=6)
                        window2.mainloop()
                window1.config(menu = menubar)
                window1.mainloop()
            
            elif assignment == "Assignment2":
                window1 = Tk()
                window1.title("Assignment2")
                window1.geometry("300x300")
                menubar = Menu(window1)
                questions = Menu(menubar, tearoff = 0)
                menubar.add_cascade(label ='Topics', menu = questions)
                questions.add_command(label ='Chi-Square Test', command = lambda: SolveQuestion("Chi-Square Test"))
                questions.add_command(label ='Correlation(Pearson) Coefficient', command = lambda: SolveQuestion("Correlation(Pearson) Coefficient"))
                questions.add_command(label ='Normalization Techniques', command = lambda: SolveQuestion("Normalization Techniques"))
                Label(window1,text="Select Topic from Menu",fg="red",bg="yellow",height=4).grid(row=0,column=0,padx=20,pady=30)
                def SolveQuestion(question):
                    if question == "Chi-Square Test":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute1 = StringVar(window2)
                        clickedAttribute1.set("Select Attribute1")
                        dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                        dropCols.grid(column=1,row=5,padx=20,pady=30)
                        clickedAttribute2 = StringVar(window2)
                        clickedAttribute2.set("Select Attribute2")
                        dropCols = OptionMenu(window2, clickedAttribute2, *cols)
                        dropCols.grid(column=2,row=5)
                        clickedClass = StringVar(window2)
                        clickedClass.set("Select Class")
                        dropCols = OptionMenu(window2, clickedClass, *cols)
                        dropCols.grid(column=3,row=5)
                        Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=2,row=7,padx=20,pady=30) 
                        
                        def computeOperation():
                            attribute1 = clickedAttribute1.get()
                            attribute2 = clickedAttribute2.get()
                            category = clickedClass.get()
                            arrClass = data[category].unique()
                            g = data.groupby(category)
                            f = {
                            attribute1: 'sum',
                            attribute2: 'sum'
                            }
                            v1 = g.agg(f)
                            print(v1)
                            v = v1.transpose()
                            print(v)
                            
                            tv1 = ttk.Treeview(window2,height=3)
                            tv1.grid(column=1,row=8,padx=5,pady=8)
                            tv1["column"] = list(v.columns)
                            tv1["show"] = "headings"
                            for column in tv1["columns"]:
                                tv1.heading(column, text=column)

                            df_rows = v.to_numpy().tolist()
                            for row in df_rows:
                                tv1.insert("", "end", values=row)

                            total = v1[attribute1].sum()+v1[attribute2].sum()
                            chiSquare = 0.0
                            for i in arrClass:
                                chiSquare += (v.loc[attribute1][i]-(((v[i].sum())*(v1[attribute1].sum()))/total))*(v.loc[attribute1][i]-(((v[i].sum())*(v1[attribute1].sum()))/total))/(((v[i].sum())*(v1[attribute1].sum()))/total)
                                chiSquare += (v.loc[attribute2][i]-(((v[i].sum())*(v1[attribute2].sum()))/total))*(v.loc[attribute2][i]-(((v[i].sum())*(v1[attribute2].sum()))/total))/(((v[i].sum())*(v1[attribute2].sum()))/total)
                            
                            degreeOfFreedom = (len(v)-1)*(len(v1)-1)
                            Label(window2,text="Chi-square value is "+str(chiSquare), justify='center',height=2,fg="green").grid(column=1,row=9,padx=5,pady=8) 
                            Label(window2,text="Degree of Freedom is "+str(degreeOfFreedom), justify='center',height=2,fg="green").grid(column=1,row=10,padx=5,pady=8) 
                            res = ""
                            if chiSquare > degreeOfFreedom:
                                res = "Attributes " + attribute1 + ' and ' + attribute2 + " are strongly correlated."
                            else:
                                res = "Attributes " + attribute1 + ' and ' + attribute2 + " are not correlated."
                            Label(window2,text=res, justify='center',height=2,fg="green").grid(column=1,row=11,padx=5,pady=8)
                        window2.mainloop()
                    elif question == "Correlation(Pearson) Coefficient":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute1 = StringVar(window2)
                        clickedAttribute1.set("Select Attribute1")
                        dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                        dropCols.grid(column=1,row=5,padx=20,pady=30)
                        clickedAttribute2 = StringVar(window2)
                        clickedAttribute2.set("Select Attribute2")
                        dropCols = OptionMenu(window2, clickedAttribute2, *cols)
                        dropCols.grid(column=2,row=5)
                        Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=2,row=7,padx=20,pady=30) 
                        
                        def computeOperation():
                            attribute1 = clickedAttribute1.get()
                            attribute2 = clickedAttribute2.get()
                            
                            sum = 0
                            for i in range(len(data)):
                                sum += data.loc[i, attribute1]
                            avg1 = sum/len(data)
                            sum = 0
                            for i in range(len(data)):
                                sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute1]-avg1)
                            var1 = sum/(len(data))
                            sd1 = math.sqrt(var1)
                            
                            sum = 0
                            for i in range(len(data)):
                                sum += data.loc[i, attribute2]
                            avg2 = sum/len(data)
                            sum = 0
                            for i in range(len(data)):
                                sum += (data.loc[i, attribute2]-avg2)*(data.loc[i, attribute2]-avg2)
                            var2 = sum/(len(data))
                            sd2 = math.sqrt(var2)
                            
                            sum = 0
                            for i in range(len(data)):
                                sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute2]-avg2)
                            covariance = sum/len(data)
                            pearsonCoeff = covariance/(sd1*sd2)    
                            Label(window2,text="Covariance value is "+str(covariance), justify='center',height=2,fg="green").grid(column=1,row=8,padx=5,pady=8) 
                            Label(window2,text="Correlation coefficient(Pearson coefficient) is "+str(pearsonCoeff), justify='center',height=2,fg="green").grid(column=1,row=9,padx=5,pady=8) 
                            res = ""
                            if pearsonCoeff > 0:
                                res = "Attributes " + attribute1 + ' and ' + attribute2 + " are positively correlated."
                            elif pearsonCoeff < 0:
                                res = "Attributes " + attribute1 + ' and ' + attribute2 + " are negatively correlated."
                            elif pearsonCoeff == 0:
                                res = "Attributes " + attribute1 + ' and ' + attribute2 + " are independant."
                            Label(window2,text=res, justify='center',height=2,fg="green").grid(column=1,row=11,padx=5,pady=8)
                        window2.mainloop()
                    elif question == "Normalization Techniques":
                        window2 = Tk()
                        window2.title(question)
                        window2.geometry("500x500")
                        cols = []
                        for i in data.columns:
                            cols.append(i)
                        clickedAttribute1 = StringVar(window2)
                        clickedAttribute1.set("Select Attribute1")
                        dropCols = OptionMenu(window2, clickedAttribute1, *cols)
                        dropCols.grid(column=1,row=5,padx=20,pady=30)
                        clickedAttribute2 = StringVar(window2)
                        clickedAttribute2.set("Select Attribute2")
                        dropCols = OptionMenu(window2, clickedAttribute2, *cols)
                        dropCols.grid(column=2,row=5)
                        clickedClass = StringVar(window2)
                        clickedClass.set("Select class")
                        dropCols = OptionMenu(window2, clickedClass, *cols)
                        dropCols.grid(column=3,row=5)
                        normalizationOperations = ["Min-Max normalization","Z-Score normalization","Normalization by decimal scaling"]
                        clickedOperation = StringVar(window2)
                        clickedOperation.set("Select Normalization Operation")
                        dropOperations = OptionMenu(window2, clickedOperation, *normalizationOperations)
                        dropOperations.grid(column=4,row=5)
                        Button(window2,text="Compute",command= lambda:computeOperation()).grid(column=2,row=7,padx=20,pady=30) 
                        
                        def computeOperation():
                            attribute1 = clickedAttribute1.get()
                            attribute2 = clickedAttribute2.get() 
                            operation = clickedOperation.get()
                            if operation == "Min-Max normalization":
                                n = len(data)
                                arr1 = []
                                for i in range(len(data)):
                                    arr1.append(data.loc[i, attribute1])
                                arr1.sort()
                                min1 = arr1[0]
                                max1 = arr1[n-1]
                                
                                arr2 = []
                                for i in range(len(data)):
                                    arr2.append(data.loc[i, attribute2])
                                arr2.sort()
                                min2 = arr2[0]
                                max2 = arr2[n-1]
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute1] = ((data.loc[i, attribute1]-min1)/(max1-min1))
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute2] = ((data.loc[i, attribute2]-min2)/(max2-min2))
                            elif operation == "Z-Score normalization":
                                sum = 0
                                for i in range(len(data)):
                                    sum += data.loc[i, attribute1]
                                avg1 = sum/len(data)
                                sum = 0
                                for i in range(len(data)):
                                    sum += (data.loc[i, attribute1]-avg1)*(data.loc[i, attribute1]-avg1)
                                var1 = sum/(len(data))
                                sd1 = math.sqrt(var1)
                                
                                sum = 0
                                for i in range(len(data)):
                                    sum += data.loc[i, attribute2]
                                avg2 = sum/len(data)
                                sum = 0
                                for i in range(len(data)):
                                    sum += (data.loc[i, attribute2]-avg2)*(data.loc[i, attribute2]-avg2)
                                var2 = sum/(len(data))
                                sd2 = math.sqrt(var2)
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute1] = ((data.loc[i, attribute1]-avg1)/sd1)
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute2] = ((data.loc[i, attribute2]-avg2)/sd2)
                            elif operation == "Normalization by decimal scaling":        
                                j1 = 0
                                j2 = 0
                                n = len(data)
                                arr1 = []
                                for i in range(len(data)):
                                    arr1.append(data.loc[i, attribute1])
                                arr1.sort()
                                max1 = arr1[n-1]
                                
                                arr2 = []
                                for i in range(len(data)):
                                    arr2.append(data.loc[i, attribute2])
                                arr2.sort()
                                max2 = arr2[n-1]
                                
                                while max1 > 1:
                                    max1 /= 10
                                    j1 += 1
                                while max2 > 1:
                                    max2 /= 10
                                    j2 += 1
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute1] = ((data.loc[i, attribute1])/(pow(10,j1)))
                                
                                for i in range(len(data)):
                                    d.loc[i, attribute2] = ((data.loc[i, attribute2])/(pow(10,j2)))
                            
                            Label(window2,text="Normalized Attributes", justify='center',height=2,fg="green").grid(column=1,row=8,padx=5,pady=8)         
                            tv1 = ttk.Treeview(window2,height=15)
                            tv1.grid(column=1,row=9,padx=5,pady=8)
                            tv1["column"] = [attribute1,attribute2]
                            tv1["show"] = "headings"
                            for column in tv1["columns"]:
                                tv1.heading(column, text=column)
                            i = 0
                            while i < len(data):
                                tv1.insert("", "end", iid=i, values=(d.loc[i, attribute1],d.loc[i, attribute2]))
                                i += 1
                            sns.set_style("whitegrid")
                            sns.FacetGrid(d, hue=clickedClass.get(), height=4).map(plt.scatter, attribute1, attribute2).add_legend()
                            plt.title("Scatter plot")
                            plt.show(block=True)
                        window2.mainloop()
                window1.config(menu = menubar)
                window1.mainloop()
            
        # window.config(background="white")
        label_file_explorer = Label(window,text="Choose Dataset from File Explorer",justify='center',height=4,fg="blue")
        button_explore = Button(window,text="Browse Dataset",command=browseDataset)
        button_exit = Button(window,text="Exit",command=exit)
        label_file_explorer.grid(column=1,row=1,padx=20,pady=30)
        button_explore.grid(column=3,row=1,padx=20,pady=30)
        button_exit.grid(column=5,row=1,padx=20,pady=30)


window = Tk()
window.title("Data Analysis Tool")
window.geometry("500x500")

# Creating Menubar
menubar = Menu(window)
  
# Adding File Menu and commands
assignements = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Assignment', menu = assignements)
assignements.add_command(label ='Assignment 1', command = lambda: SolveAssignment("Assignment1"))
assignements.add_command(label ='Assignment 2', command = lambda: SolveAssignment("Assignment2"))
# display Menu
window.config(menu = menubar)
window.mainloop()