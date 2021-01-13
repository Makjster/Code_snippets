#!/usr/bin/env python
# coding: utf-8

# In[116]:


# Author: Matti Johannsen
#Contact: Matti.Johannsen@gmx.de / Matti.Johannsen@rwth-aachen.de

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import ifcopenshell
from collections import Counter
import re


# In[271]:


class Root(Tk):
    
	#create the GUI
    def __init__(self):
        super(Root,self).__init__()
        self.title("IFC model placement changer")
        self.minsize(640,480)
        
        self.labelFrame = ttk.LabelFrame(self, text = "Open Files")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
 
       
        keyword = StringVar()
        self.button()
        self.button2()
        self.getDifference()
        self.showLine(keyword)
        
        tk.Label(self,text="Keyword").grid(row=4)

        Entry(self,textvariable=keyword).grid(row=4, column=1)
        
        
        
        #call fileDialog to browse for a file
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Bigger File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
        
         #call fileDialog to browse for a file
    def button2(self):
        self.button2 = ttk.Button(self.labelFrame, text = "Smaller File",command = self.fileDialog2)
        self.button2.grid(column = 2, row = 1)
        
    def fileDialog(self):
 
        self.filename = filedialog.askopenfilename(initialdir =  "D:/", title = "Select A File", filetype =
        (("ifc files","*.ifc"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
    
    def fileDialog2(self):
 
        self.filename2 = filedialog.askopenfilename(initialdir =  "D:/", title = "Select A File", filetype =
        (("ifc files","*.ifc"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 2, row = 2)
        self.label.configure(text = self.filename2) 
            
        #remove everything until the string
    def slicer(self, my_str,sub):
        index=my_str.find(sub)
        if index !=-1 :
             return my_str[index:] 
        else :
            raise Exception('Sub string not found!')
        #remove all unnecessary things
    def Cleaner(self, file):
        
        x = file.replace('DATA','')
        x = x.replace('SEC','')
        x = x.replace('END','')
        x = x.replace('ISO','')

        x1 = ''.join(i for i in x if not i.isdigit())
        x2 = re.sub(r'\(.*\)', '', x1)
        x3 = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", x2)
        s = re.sub("[\(\[].*?[\)\]]", "", x3)
        res = re.sub(r'[\W_]+', '\n', s)
        res1 = self.slicer(res,'IFCOWNERHISTORY')
        return res1
    
        #go through two files and find the different classes in them
    def findDifference(self):
        self.file1 = ifcopenshell.open(self.filename)
        self.file2 = ifcopenshell.open(self.filename2)
        
        f1 = self.file1.to_string()
        f2 = self.file2.to_string()
        cleanF1 = self.Cleaner(f1)
        countF1 = Counter(cleanF1.split())
        countF1 = Counter(countF1)
        no_integers1 = [x for x in countF1 if not isinstance(x, int)]

        cleanF2 = self.Cleaner(f2)
        countF2 = Counter(cleanF2.split())
        countF2 = Counter(countF2)
        no_integers_2 = [x for x in countF2 if not isinstance(x, int)]

        list_same = []
        list_not_same = []
        for x in no_integers1:
            if x in no_integers_2:
                list_same.append(x)
            else:
                list_not_same.append(x)
        
        self.label.grid(column = 3, row = 3)
        
        top = Toplevel(self)
        top.title("Result")
        
        msg = Message(top, text='\n'.join(map(str, list_not_same)))
        msg.pack()

    def getDifference(self, *args):
        self.button = ttk.Button(self.labelFrame, text = "Get Difference",command = self.findDifference)
        self.button.grid(column = 1, row = 3)
        
        #find lines in a file which have a self-determined keyword in them
    def findInFile(self, *args):
        self.file1 = ifcopenshell.open(self.filename)
        file2 = self.file1.to_string()
        file = file2.split()
        
        if '' in args:
            tk.Label(self,text="Enter a word you want to serach for in the file").grid(row=5)
            
        else:
            keyword = args[1]
            list_of_lines = []
            for line in file:
                if keyword.upper() in line:
                    list_of_lines.append(line)        
        
            top1 = Toplevel(self)
            top1.title("Result")
        
            msg = Message(top1, text='\n'.join(map(str, list_of_lines)))
            msg.pack()
        
    def showLine(self, keyword):
        self.button = ttk.Button(self.labelFrame, text = "Find in file",command = lambda: self.findInFile(self, keyword.get()))
        self.button.grid(column = 2, row = 3)


# In[272]:


if __name__ == '__main__':
    root = Root()
    root.mainloop()


# In[ ]:





# In[ ]:




