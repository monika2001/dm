from posixpath import split
from tkinter import *
from tkinter import filedialog, ttk
import pandas as pd
import math
import operator
import itertools

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
            
        gini_d = 1
        for category in arrClass:
            gini_d -= ((float(v.transpose()[category])/total)*(float(v.transpose()[category])/total))
            
        print(gini_d, "gini_d")
        
            
        
        for i in cols:
            arrAttribute = data[i].unique()
            g1 = data.groupby(i)
            print(arrAttribute, i)
            f1 = {
            i : 'count'
            }
            v1 = g1.agg(f1)
            list1 = []            
            total1 = 0
            for eachValue in arrAttribute:
                total1 += v1.transpose()[eachValue]
                list1.append(eachValue)
                
            list_combinations = []
            for r in range(len(list1)+1):
                for combination in itertools.combinations(list1, r):
                    list_combinations.append(combination)
            
            list_combinations = list_combinations[1:-1]
            prob = 1
            for t in list_combinations:
                print(t)
                tot = 0
                gini_di = 0
                for l in t:
                    tot += v1.transpose()[l]
                for l in t:
                    print(l)
                    for k in arrClass:
                        num = 0
                        for j in range(len(data)):
                            if data.loc[j, clickedAttribute.get()] == k and data.loc[j, i] == l:
                                num += 1
                        prob -= ((float(num)/float(v1.transpose()[l]))*(float((num)/float(v1.transpose()[l]))))
                    gini_di += (float(v1.transpose()[l])/float(tot))*prob
                key = 'Gini'+str(i)+str(t)
                d[key] = float(gini_di)
                    
        dictionary_keys = list(d.keys())
        sorted_d = {dictionary_keys[i]: sorted(
            d.values())[i] for i in range(len(dictionary_keys))}
        
        print(d)
        print(sorted_d)
        columns = ('Criteria', 'Gini Index')
        tv1 = ttk.Treeview(window, columns=columns, show='headings')
        tv1.grid(column=1,row=8,padx=5,pady=8)
        
        tv1.heading('Criteria', text='Criteria')
        tv1.heading('Gini Index', text='Gini Index')
        
        tuples = []
        for n in sorted_d:
            tuples.append((f'{n}', f'{sorted_d[n]}'))
        for tuple in tuples:
            tv1.insert('', END, values=tuple)
        tv1.grid(row=7, column=1, sticky='nsew')      
        
    
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