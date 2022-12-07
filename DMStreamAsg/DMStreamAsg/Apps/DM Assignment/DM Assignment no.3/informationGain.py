from posixpath import split
from tkinter import *
from tkinter import filedialog, ttk
import pandas as pd
import math
import operator

def browseDataset():
    filename = filedialog.askopenfilename(initialdir="/",title="Select dataset", filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))
    label_file_explorer.configure(text="File Opened: "+filename)
    newfilename = ''
    for i in filename:
        if i == "/":
            newfilename = newfilename + "/"
        newfilename = newfilename + i
    data = pd.read_csv(filename)
    cols = []
    for i in data.columns:
        cols.append(i)
    clickedAttribute = StringVar()
    clickedAttribute.set("Select Attribute")
    dropCols = OptionMenu(window, clickedAttribute, *cols)
    dropCols.grid(column=1,row=5,padx=20,pady=30)
    
    dropAttribute = StringVar()
    dropAttribute.set("Drop Attribute")
    dropCols = OptionMenu(window, dropAttribute, *cols)
    dropCols.grid(column=2,row=5,padx=20,pady=30)
    
    d = {}
    split_i = {}
    Button(window,text="Compute",command= lambda:compute()).grid(column=1,row=6,padx=20,pady=30) 
    Button(window,text="Drop Column",command= lambda:dropCol()).grid(column=2,row=6,padx=20,pady=30) 
    
    def dropCol():
        print(dropAttribute.get())
        cols.remove(dropAttribute.get())
        # window.mainloop()
        
    def compute():
        cols.remove(clickedAttribute.get())
        print(clickedAttribute.get())
        print(cols)
        arrClass = data[clickedAttribute.get()].unique()
        g = data.groupby(clickedAttribute.get())
        print(arrClass, g)
        f = {
        clickedAttribute.get() : 'count'
        }
        v = g.agg(f)
        total = 0
        for category in arrClass:
            total += v.transpose()[category]
            
        info_d = 0
        for category in arrClass:
            info_d += calcEntropy(float(v.transpose()[category]), total)
            
        for i in cols:
            arrAttribute = data[i].unique()
            g1 = data.groupby(i)
            print(arrAttribute, i)
            f1 = {
            i : 'count'
            }
            v1 = g1.agg(f1)
            
            total1 = 0
            for eachValue in arrAttribute:
                total1 += v1.transpose()[eachValue]
                
                    
            info_d1 = 0
            split_info = 0
            for eachValue in arrAttribute:
                for k in arrClass:
                    num = 0
                    for j in range(len(data)):
                        if data.loc[j, clickedAttribute.get()] == k and data.loc[j, i] == eachValue:
                            num += 1
                    info_d1 += calcEntropy(num, float(v1.transpose()[eachValue]))
                info_d1 *= float(v1.transpose()[eachValue])/total1
                split_info += calcEntropy(float(v1.transpose()[eachValue]), total1)    
            d[i] = float(info_d1)
            split_i[i] = float(split_info)
        
        sorted_d = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))
        print(d)
        print(sorted_d)
        columns = ('Attributes', 'Info', 'Gain', 'Gain ratio')
        tv1 = ttk.Treeview(window, columns=columns, show='headings')
        tv1.grid(column=1,row=8,padx=5,pady=8)
        
        tv1.heading('Attributes', text='Attributes')
        tv1.heading('Info', text='Info')
        tv1.heading('Gain', text='Gain')
        tv1.heading('Gain ratio', text='Gain ratio')
        
        tuples = []
        for n in sorted_d:
            tuples.append((f'{n}', f'{sorted_d[n]}', f'{float(info_d-sorted_d[n])}', f'{(float(info_d-sorted_d[n])/float(split_i[n]))}'))
        for tuple in tuples:
            tv1.insert('', END, values=tuple)
        tv1.grid(row=7, column=1, sticky='nsew')
         
    def calcEntropy(c,n):
        if c <= 0:
            return 0.0 
        return -(c*1.0/n)*math.log(c*1.0/n, 2)
        
        
    
window = Tk()
window.title("Measure of central tendancy")
window.geometry("500x500")
window.config(background="white")
label_file_explorer = Label(window,text="Choose Dataset from File Explorer",justify='center',height=4,fg="blue")
button_explore = Button(window,text="Browse Dataset",command=browseDataset)
button_exit = Button(window,text="Exit",command=exit)
label_file_explorer.grid(column=1,row=1,padx=20,pady=30)
button_explore.grid(column=3,row=1,padx=20,pady=30)
button_exit.grid(column=5,row=1,padx=20,pady=30)
window.mainloop()