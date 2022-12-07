from posixpath import split
from tkinter import *
from tkinter import filedialog, ttk
import pandas as pd
import math
import operator
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import seaborn as sns
import numpy as np
from sklearn.tree import _tree
from sklearn import metrics

def browseDataset():
    filename = filedialog.askopenfilename(initialdir="/",title="Select dataset", filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))
    label_file_explorer.configure(text="File Opened: "+filename)
    newfilename = ''
    for i in filename:
        if i == "/":
            newfilename = newfilename + "/"
        newfilename = newfilename + i
    data = pd.read_csv(filename)
    print(data)
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
        
        
        f_names = []
        c_names = []
        f_names = cols
        print(f_names)
        for c in arrClass:
            c_names.append(str(c))
        print(type(c_names))
        le_class = LabelEncoder()
        df = data
        df[clickedAttribute.get()] = le_class.fit_transform(df[clickedAttribute.get()])
        dft = data.drop(clickedAttribute.get(), axis=1)
        print(dft)
        X_train, X_test, Y_train, Y_test = train_test_split(dft, df[clickedAttribute.get()], test_size=0.2, random_state=1)
        clf = DecisionTreeClassifier(max_depth = 3, random_state = 0,criterion="entropy")
        model = clf.fit(X_train, Y_train)
        Y_predicted = clf.predict(X_test)
        Y_test = Y_test.to_numpy()
        print(type(Y_predicted),type(Y_test))
        print(Y_predicted, "predicted", len(Y_predicted), Y_test, "Y_test", len(Y_test))
        c_matrix = confusion_matrix(Y_test,Y_predicted)
        
        print(c_matrix)
        print(classification_report(Y_test,Y_predicted))
        ax = plt.subplot()
        sns.heatmap(c_matrix, annot=True, fmt='g', ax=ax)
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels') 
        ax.set_title('Confusion Matrix')
        ax.xaxis.set_ticklabels(c_names)
        ax.yaxis.set_ticklabels(c_names)
        
        
        text_representation = tree.export_text(clf)
        # print(text_representation)
        print(f_names,c_names)
        print(type(f_names),type(c_names))
        fig = plt.figure(figsize=(25,20))
        _ = tree.plot_tree(clf, feature_names=f_names, class_names=c_names,filled=True)
        accuracy = "Accuracy " + str(metrics.accuracy_score(Y_test,Y_predicted))
        Label(window, text=accuracy).grid(row=10,column=1,padx=20,pady=5)
        plt.show()
        

        
        def get_rules(tree, feature_names, class_names):
            tree_ = tree.tree_
            feature_name = [
                feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
                for i in tree_.feature
            ]

            paths = []
            path = []
            
            def recurse(node, path, paths):
                
                if tree_.feature[node] != _tree.TREE_UNDEFINED:
                    name = feature_name[node]
                    threshold = tree_.threshold[node]
                    p1, p2 = list(path), list(path)
                    p1 += [f"({name} <= {np.round(threshold, 3)})"]
                    recurse(tree_.children_left[node], p1, paths)
                    p2 += [f"({name} > {np.round(threshold, 3)})"]
                    recurse(tree_.children_right[node], p2, paths)
                else:
                    path += [(tree_.value[node], tree_.n_node_samples[node])]
                    paths += [path]
                    
            recurse(0, path, paths)

            # sort by samples count
            samples_count = [p[-1][1] for p in paths]
            ii = list(np.argsort(samples_count))
            paths = [paths[i] for i in reversed(ii)]
            
            rules = []
            for path in paths:
                rule = "if "
                
                for p in path[:-1]:
                    if rule != "if ":
                        rule += " and "
                    rule += str(p)
                rule += " then "
                if class_names is None:
                    rule += "response: "+str(np.round(path[-1][0][0][0],3))
                else:
                    classes = path[-1][0][0]
                    l = np.argmax(classes)
                    rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
                rule += f" | based on {path[-1][1]:,} samples"
                rules += [rule]
                
            return rules 
        
        rules = get_rules(clf, f_names, c_names)
        win = Tk()
        win.title("Extracted Rules")
        win.geometry("500x500")
        win.config(background="white")
        i=0
        for r in rules:
            Label(win, text=r, justify='center').grid(row=i,column=1,padx=20,pady=5)
            i=i+1
        
        win.mainloop()
        for r in rules:
            print(r)
            
        
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