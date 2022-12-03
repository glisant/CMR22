# Python program to create
# a file explorer in Tkinter

##ADD POSSIBILITY OF LABELING OR REMOVING PATIENTS
#To remove biomarkers you just skip over it at extraction
#Have a view graph that creates graphs of things you want on the go! 
from PIL import ImageTk
from textwrap import wrap
import warnings
warnings.filterwarnings("ignore")
import PIL.Image
from scipy import stats
import pandas as pd
# import all components
# from the tkinter library
from tkinter import *
import copy
#import CMR_DATA_EXTRACT
import shutil
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt

class CMR_graphing(tk.Tk):
    def __init__(self,exported_frame,exported_data):
        self.lists=[]
        self.patient_categories=[]
        self.categories=[]
        self.buttons=[]
        self.exported_data=exported_data
        self.exported_frame=exported_frame
        self.graphs=[]
        self.patients=list(self.exported_data.keys())
        self.currently_disp=0
        self.currently_graphing=[]

        self.subsegments=['Segments','Basal Slices','Mid Slices','MORE Slices','LAD','RCA','LCX']
        self.segments=['Baseline','30 Seconds','0 Seconds','HV MORE changeOS','MORE changeOS','Regional Heterogeneity']

        self.value_ids=['Base Segments', 'Base Ave', 'Base Coro', 'Norm 0s Segments',
            'Norm 0s Ave', 'Norm 0s Coro', 'Norm 30s Segments', 'Norm 30s Ave',
            'Norm 30s Coro', 'MORE Segmental changeOS', 'MORE changeOS',
            'MORE Coro changeOS', 'HV MORE Segmental changeOS',
            'HV MORE changeOS', 'HV MORE Coro changeOS']
        self.graph_ids=['Segments','Basal Slices','Mid Slices','MORE Slices','LAD', 'RCA','LCX']
        super().__init__()

        # configure the root self.selectionframe
        self.title('CMR Graphing Interface')
        self.geometry("560x800")
        self.resizable(False,False)
        self.config(background = "lightblue")

        #canvas for options:
        self.selectionframe = Frame(self, bg='aliceblue', highlightbackground="black", highlightthickness=3, width=550,height=790)
        self.selectionframe.pack_propagate(0)
        self.selectionframe.place(x=5, y=5)

        #canvas for graph:
        self.graphframe = Frame(self, bg='lightblue', highlightbackground="black", highlightthickness=3, width=1485-550,height=790)
        self.graphframe.pack_propagate(0)
        self.graphframe.place(x=560, y=5)

        width = 350
        height = 120
        img = PIL.Image.open("CMR_logo_right.png")
        img2 = PIL.Image.open("CMR_logo_left.png")
        img = img.resize((125,75), PIL.Image.ANTIALIAS)
        img2 = img2.resize((190,90), PIL.Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(img)
        photoImg2 =  ImageTk.PhotoImage(img2)
        label = Label(self.selectionframe,bg='aliceblue', image = photoImg2)
        label.photo=photoImg2
        label.place(x=340,y=8)
        label2 = Label(self.selectionframe,bg='aliceblue', image = photoImg)
        label2.photo=photoImg
        label2.place(x=400,y=80)
        
        #photoImg2 =  ImageTk.PhotoImage(img2)
        
        # label
        self.sframe_title = ttk.Label(self.selectionframe, text='Graph Options',font=('Times',20),background='aliceblue')
        self.sframe_title.pack()

        ttk.Label(self.selectionframe, text='Graph By',font=('Times',13),background='aliceblue').place(x=15,y=50)
        
        ttk.Label(self.selectionframe, text='Graph Parts',font=('Times',13),background='aliceblue').place(x=15,y=120)

        ttk.Label(self.selectionframe, text='Include in Graph',font=('Times',13),background='aliceblue').place(x=15,y=220)

        ttk.Label(self.selectionframe, text='Show Statistics',font=('Times',13),background='aliceblue').place(x=15,y=320)

        ttk.Label(self.selectionframe, text='Type of Graph',font=('Times',13),background='aliceblue').place(x=15,y=420)

        ttk.Label(self.selectionframe, text='Num of subject categories:',font=('Times',13),background='aliceblue').place(x=15,y=490)

        #ttk.Label(self.selectionframe, text='Enter Number of groups:',font=('Times',13),background='aliceblue').place(x=15,y=490)
        ttk.Label(self.selectionframe, text='Labels:',font=('Times',13),background='aliceblue').place(x=15,y=520)
        self.num_groups=ttk.Entry(self.selectionframe, text='Patient Groups',font=('Times',13),background='aliceblue',width=4)
        self.num_groups.place(x=210,y=490)

        self.gframe_title = ttk.Label(self.graphframe, text='Graph',font=('Times',20), background='lightblue')
        self.gframe_title.pack()

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack()

        self.button_select_patients = ttk.Button(self.selectionframe, text='Label Subjects',command= lambda: self.create_lists(self.num_groups.get()))
        #self.button_select_patients['command'] = self.button_clicked
        self.button_select_patients.place(x=260,y=490)

        self.button_graph = ttk.Button(self.selectionframe, text='Graph',command= lambda: self.graph_basic(self.exported_data))

        self.button_delete_all = ttk.Button(self.selectionframe, text='Delete All Graphs',command=self.delete_all_graphs)
        self.button_delete_patient = ttk.Button(self.selectionframe, text='Delete Patient',command=self.delete_patient)
        
        self.button_next_graph = ttk.Button(self.graphframe, text='Next Graph',command= lambda: self.view_graph(self.currently_disp+1))
        self.button_prev_graph = ttk.Button(self.graphframe, text='Previous Graph',command= lambda: self.view_graph(self.currently_disp-1))
        
        
        self.button_graph.place(x=440,y=745)
        self.button_delete_all.place(x=320,y=745)
        self.button_delete_patient.place(x=15,y=745)
        
        
        self.create_lists(1)
        self.status_reqs=[]

        for i in range(26):
            self.status_reqs.append(IntVar())
        c = Checkbutton(self.selectionframe, text = "Patient", bg=('aliceblue'), variable=self.status_reqs[0])
        c1 = Checkbutton(self.selectionframe, text = "Biomarker", bg='aliceblue', variable=self.status_reqs[1])
        c2 = Checkbutton(self.selectionframe, text = "Patient and Biomarker", bg='aliceblue', variable=self.status_reqs[2])
        graph_by_boxes=[c,c1,c2]
        self.place_boxes_sel(graph_by_boxes,config=3,xpad=100)


        c3 = Checkbutton(self.selectionframe, text = "All", bg='aliceblue', variable=self.status_reqs[3], command=self.dis_check)
        c4 = Checkbutton(self.selectionframe, text = "Segments", bg='aliceblue', variable=self.status_reqs[4])
        c5 = Checkbutton(self.selectionframe, text = "Basal Slices", bg='aliceblue', variable=self.status_reqs[5])
        c6 = Checkbutton(self.selectionframe, text = "Mid Slices", bg='aliceblue', variable=self.status_reqs[6])
        c7 = Checkbutton(self.selectionframe, text = "MORE Slices", bg='aliceblue', variable=self.status_reqs[7])
        c8 = Checkbutton(self.selectionframe, text = "LAD", bg='aliceblue', variable=self.status_reqs[8])
        c9 = Checkbutton(self.selectionframe, text = "RCA", bg='aliceblue', variable=self.status_reqs[9])
        c10 = Checkbutton(self.selectionframe, text = "LCX", bg='aliceblue', variable=self.status_reqs[10])
        self.graph_parts=[c3, c4, c5, c6, c7, c8, c9, c10 ]
        self.place_boxes_sel(self.graph_parts,config=4,xpad=100,starting_y=150)


        c11 = Checkbutton(self.selectionframe, text = "Baseline", bg='aliceblue', variable=self.status_reqs[11])
        c12 = Checkbutton(self.selectionframe, text = "30 Seconds", bg='aliceblue', variable=self.status_reqs[12])
        c13 = Checkbutton(self.selectionframe, text = "0 Seconds", bg='aliceblue', variable=self.status_reqs[13])
        c14 = Checkbutton(self.selectionframe, text = "HV MORE changeOS", bg='aliceblue', variable=self.status_reqs[14])
        c15 = Checkbutton(self.selectionframe, text = "MORE changeOS", bg='aliceblue', variable=self.status_reqs[15])
        c16 = Checkbutton(self.selectionframe, text = "Regional Heterogeneity", bg='aliceblue', variable=self.status_reqs[16])
  
        graph_include=[c11, c12, c13, c14, c15, c16]
        self.place_boxes_sel(graph_include,config=3,xpad=150,starting_y=250)


        c17 = Checkbutton(self.selectionframe, text = "Mean", bg='aliceblue', variable=self.status_reqs[17])
        c18 = Checkbutton(self.selectionframe, text = "Sum", bg='aliceblue', variable=self.status_reqs[18])
        c19 = Checkbutton(self.selectionframe, text = "Count", bg='aliceblue', variable=self.status_reqs[19])
        c20 = Checkbutton(self.selectionframe, text = "Student t-test", bg='aliceblue', variable=self.status_reqs[20])
        c21 = Checkbutton(self.selectionframe, text = "Welch", bg='aliceblue', variable=self.status_reqs[21])
        c22 = Checkbutton(self.selectionframe, text = "ANOVA", bg='aliceblue', variable=self.status_reqs[22])
        
  
        graph_stats=[c17, c18, c19, c20, c21, c22]
        self.place_boxes_sel(graph_stats,config=3,xpad=150,starting_y=350)


        c23 = Checkbutton(self.selectionframe, text = "Scatter", bg='aliceblue', variable=self.status_reqs[23])
        c24 = Checkbutton(self.selectionframe, text = "Histogram", bg='aliceblue', variable=self.status_reqs[24])
        c25 = Checkbutton(self.selectionframe, text = "Boxplot", bg='aliceblue', variable=self.status_reqs[25])
        #c26 = Checkbutton(self.selectionframe, text = "Student t-test", bg='aliceblue', variable=self.status_reqs[2])
        #c27 = Checkbutton(self.selectionframe, text = "Welch", bg='aliceblue', variable=self.status_reqs[0])
        #c32 = Checkbutton(self.selectionframe, text = "ANOVA", bg='aliceblue', variable=self.status_reqs[0])

        graph_type=[c23, c24, c25]
        self.place_boxes_sel(graph_type,config=3,xpad=150,starting_y=450)

    def place_boxes_sel(self,boxes,config=2, starting_y=80,xpad=150,x0=15):
        
        longest_width=xpad
        for _,box in enumerate(boxes):
            x_dis=((_)%config)*(longest_width+10)
            y_dis=((_)//config)*30
            box.place(x=x0+x_dis,y=starting_y+y_dis)
            
    def create_lists(self,num_of):
        if num_of=='':
            showinfo(title='Information', message='Please enter a subject category number. For more information contact glisant.plasa@mail.mcgill.ca')
        elif int(num_of)>3:
            showinfo(title='Information', message='Number of categories is too large. Currently only up to 3 categories of patients are supported. For more information contact glisant.plasa@mail.mcgill.ca')
        else:
            self.patients=list(self.exported_data.keys())
    
            if len(self.lists)>0:
                for _,i in enumerate(self.lists):
                    self.categories[_].destroy()
                    self.lists[_].delete(0,END)
                    i.destroy()
            widthl=20
            heightl=10
            
            self.lists=[]
            self.patient_categories=[]
            for i in range(int(num_of)):
                self.patient_categories.append(f'Type {i}')
                self.lists.append(Listbox(height=heightl, width=widthl,selectmode = "multiple"))
            self.place_boxes_sel(self.lists,config=int(num_of),xpad=(widthl*6)+50,starting_y=580)
            self.categories=[]

            for patient in self.patients:
                self.lists[0].insert(END,patient)
            
            for _,cat in enumerate(self.patient_categories):
                self.categories.append(ttk.Entry(self.selectionframe,font=('Times',10),background='aliceblue',width=15))
                self.categories[_].insert(END,self.patient_categories[_])
            self.place_boxes_sel(self.categories,config=int(num_of),xpad=(widthl*6)+50,starting_y=547,x0=20)

            if len(self.buttons)>0:
                for i in self.buttons:
                    i.destroy()
            self.buttons=[]

            if len(self.lists)>1:
                c1=Button(self.selectionframe,text='-->',command= lambda: self.move_to(self.lists[0],self.lists[1]))
                c1.place(x=145,y=605)
                c2=Button(self.selectionframe,text='<--',command= lambda: self.move_to(self.lists[1],self.lists[0]))
                c2.place(x=145,y=665)
                
                if len(self.lists)>2:
                    c3=Button(self.selectionframe,text='-->',command= lambda: self.move_to(self.lists[1],self.lists[2]))
                    c3.place(x=145+180,y=605)
                    c4=Button(self.selectionframe,text='<--',command= lambda: self.move_to(self.lists[2],self.lists[1]))
                    c4.place(x=145+180,y=665)
                  
    def move_to(self,fromlist,tolist):
        indexList= fromlist.curselection()

        for i in indexList[::-1]:
            index=i
            val=fromlist.get(index)
            fromlist.delete(index)
            tolist.insert(END,val)

    def graph_boxplot(self,category='',segments_run=[], subsegments_run=[],data=[]):
        data=data.loc[data['Value']!='MISSING']
        markers=list(self.exported_data[self.patients[0]].keys())
        files=['GLOBAL','ENDO','EPI']
        #print(pd.unique(data['Segment Subtype']))
        if category=='patient':
            for segment in pd.unique(data['Segment Type']):
                dt_seg=data.loc[(data['Segment Type']==segment)]
                for subsegment in pd.unique(data['Segment Subtype']):
                    
                    dt=dt_seg.loc[(dt_seg['Segment Subtype']==subsegment)]
                    markers=pd.unique(dt['Biomarker'])
                    to_graph=[]
                    y_ax_labels=[]
                    for i in range(len(pd.unique(data['Category']))):
                        to_graph.append([])
                    for marker in markers:
                        dt_marker=dt[dt['Biomarker']==marker]
                        upper_limit = dt_marker['Value'].quantile(0.75)
                        lower_limit = dt_marker['Value'].quantile(0.25)
                        dt_marker=dt_marker[(dt_marker['Value'] <= upper_limit) & (dt_marker['Value'] >= lower_limit)]
                        for _,i in enumerate(pd.unique(data['Category'])):
                            to_graph[_].append(dt_marker[(dt_marker['Category'] == i)]['Value'])

                        #dt_cat1=dt_marker[(dt_marker['Category'] == 'Type 0')]['Value']
                        #print(dt_cat1)
                        #dt_cat2=dt_marker[(dt_marker['Category'] == 'Type 1')]['Value']
                        mar_st=marker.replace('Biomarker: ','')
                        mar_st=mar_st.replace('-',' ')
                        mar_st = [word[0] for word in mar_st.split()]
                        mar_st=''.join(mar_st)
                        y_ax_labels.append(mar_st)
                    
                    
                    #to_graph_1.append(dt_marker['Value'])
                    #to_graph_1.append(dt_cat1)
                    #to_graph_2.append(dt_cat2)
                    
                    fig=plt.Figure(figsize=(9,6))

                    ax=fig.add_subplot(111)
                    xs=[-0.4,0.4]
                    colors=['#D7191C','#2C7BB6']
                    graphs=[]
                    if len(to_graph)==3:
                        for _,i in enumerate(to_graph):
                            bpl = ax.boxplot(i, positions=np.array(range(len(i)))*2.0+xs[_], sym='', widths=0.6,vert = 0)
                            self.set_box_color(bpl, colors[_])
                    else:
                        if self.status_reqs[20].get():
                            for _,i in enumerate(to_graph[0]):
                                stat, pvalue = stats.ttest_ind(to_graph[0][_], to_graph[1][_])
                                pvalue_asterisks=self.convert_pvalue_to_asterisks(pvalue)
                                if pvalue_asterisks!='ns':
                                    y_ax_labels[_]=(f'{y_ax_labels[_]} {pvalue_asterisks}') 
                        
                                #ax.text(np.mean(to_graph[0][_]),(_*2)-0.5,round(np.mean(to_graph[0][_]),3))
                                #ax.text(np.mean(to_graph[1][_]),(_*2)+0.2,round(np.mean(to_graph[1][_]),3))
                        for _,i in enumerate(to_graph):
                            bpl = ax.boxplot(i, positions=np.array(range(len(i)))*2.0+xs[_], sym='', widths=0.6,vert = 0)
                            self.set_box_color(bpl, colors[_])

                    #bpr = ax.boxplot(to_graph[1], positions=np.array(range(len(to_graph[1])))*2.0+0.4, sym='', widths=0.6,vert = 0)
                    # colors are from http://colorbrewer2.org/
                    #self.set_box_color(bpr, '#2C7BB6')
                    ax.set_yticks(range(0, len(markers) * 2, 2))
                    ax.set_yticklabels(y_ax_labels,fontsize=8)
                    #print(y_ax_labels)
                    #plt.xticks(range(0, len(markers) * 2, 2), markers)
                    #plt.ylim(-2, len(markers)*2)
                    #plt.tight_layout()
                    #ax.boxplot(to_graph_1,vert = 0)
                    fig.patch.set_facecolor('lightblue')
                    num_ct=len(pd.unique(data['Category']))
                    cats=", ".join((pd.unique(data['Category'])))
                    fig.suptitle("\n".join(wrap(f'Figure shows OS-CMR values in the {subsegment} for {segment} in {len(self.patients)} patients across biomarkers. Patients are grouped in {num_ct} categories, namely {cats}.',100)), fontsize=10)
                    #{", ".join(segments_run)} 
                    fig.subplots_adjust(left=0.1, right=0.995, top=0.89, bottom=0.04)
                    chart=FigureCanvasTkAgg(fig,self.graphframe)

                    self.graphs.append(chart)

        #for i in range(12):
            #data.append(np.random.normal(70, 40, 200))
        #fig=plt.Figure(figsize=(9,6))
        #fig.add_subplot(111).boxplot(data,vert = 0)
 
        # Creating plot
        #fig.patch.set_facecolor('lightblue')
        #fig.suptitle('Graph', fontsize=20)
        #chart=FigureCanvasTkAgg(fig,self.graphframe)
        #self.graphs.append(chart)
        #self.update_cur_view()

        #if len(self.graphs)==1:
        self.view_graph(0)
    
    def set_box_color(self,bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
    
    def find_indices(self,a_list, item_to_find):
        indices = []
        for idx, value in enumerate(a_list):
            if value == item_to_find:
                indices.append(idx)
        return indices
    
    def convert_pvalue_to_asterisks(self,pvalue):
        if pvalue <= 0.0001:
            return "****"
        elif pvalue <= 0.001:
            return "***"
        elif pvalue <= 0.01:
            return "**"
        elif pvalue <= 0.05:
            return "*"
        return "ns"
    
    def graph_basic(self,data):

        if self.num_groups.get()=='':
            showinfo(title='Information', message='Please enter number of subject categories. For more information contact glisant.plasa@mail.mcgill.ca')
            return

        if self.winfo_width()<1500:
            self.geometry("1500x800")
        self.statuses_get=[]

        self.values_wanted=[]   
        for i in self.status_reqs:
            self.statuses_get.append(i.get())

        self.group_by=self.statuses_get[0:3]
        self.graphs_parts=self.statuses_get[3:11]
        self.include_parts=self.statuses_get[11:17]
        self.include_stats=self.statuses_get[17:23]
        self.type_of_graph=self.statuses_get[23:26]
        self.num_categories=int(self.num_groups.get())
        self.patient_categories=[]
        self.allowed=[]
        
        for i in self.categories:
            self.patient_categories.append(i.get())

        allowed_ids_segments=self.find_indices(self.include_parts,1)
        segments_run=[]
        subsegments_run=[]
        for i in allowed_ids_segments:
            segments_run.append(self.segments[i])
            if i==5:
                subsegments_run+=['MORE SD','MORE Range','Transmural Regional Heterogeneity','Radial Heterogeneity','Circumferential Heterogeneity','ABS Circumferential Heterogeneity','Transmural Longitudinal Heterogeneity','Longitudinal Heterogeneity']

        allowed_ids_subsegments=self.find_indices(self.graphs_parts,1)
        
        if 0 in allowed_ids_subsegments:
            subsegments_run=self.subsegments+['AHA 1','AHA 2','AHA 3','AHA 4','AHA 5','AHA 6','AHA 7','AHA 8','AHA 9','AHA 10','AHA 11','AHA 12']
        else:
            for i in allowed_ids_subsegments:
                if i==1:
                    subsegments_run+=['AHA 1','AHA 2','AHA 3','AHA 4','AHA 5','AHA 6','AHA 7','AHA 8','AHA 9','AHA 10','AHA 11','AHA 12']
                else:
                    subsegments_run.append(self.subsegments[i-1])

        self.patients_by_category={}
        for _,i in enumerate(self.categories):
            self.patients_by_category[i.get()]=self.lists[_].get(0, END)


        data_frame_run=copy.deepcopy(self.exported_frame)
        data_frame_run=data_frame_run.loc[(data_frame_run['Segment Type'].isin(segments_run)) & (data_frame_run['Segment Subtype'].isin(subsegments_run))]
        data_frame_run['Category']=0
        for category in self.patients_by_category:
            for pat in self.patients_by_category[category]:
                updated=data_frame_run['Patient']==pat
                data_frame_run.loc[updated,'Category']=category
                #data_frame_run[data_frame_run['Patient']==pat]['Category']=category
            #data_frame_run[data_frame_run['Patient'].isin(self.patients_by_category[category])]['Category']=category
            #data_frame_run[data_frame_run['Patient'].isin(self.patients_by_category[category])]['Category']=category
        print(segments_run)
        #print(segments_run)
        if self.group_by[0]:
            print('Category: Patient')
            if self.type_of_graph[2]:
                self.graph_boxplot('patient',segments_run, subsegments_run,data_frame_run)
            if self.type_of_graph[0]:
                self.graph_scatter('patient',segments_run, subsegments_run,data_frame_run)
            #self.graph_by_patient()


        """
        
        x=[1,2,3,4,5]
        y=np.random.rand(5)

        self.exported_data
        fig=plt.Figure(figsize=(9,6))
        fig.add_subplot(111).plot(x,y,"bo")
        fig.patch.set_facecolor('lightblue')
        fig.suptitle('Graph', fontsize=20)
        chart=FigureCanvasTkAgg(fig,self.graphframe)
        self.graphs.append(chart)

        if len(self.graphs)==1:
            self.view_graph(0)

        
        self.update_cur_view()
        """
        if self.currently_disp==len(self.graphs)-1:
  
            self.button_next_graph['state']='disabled'
        elif self.currently_disp<len(self.graphs):
            
            self.button_next_graph['state']='enabled'
        if self.currently_disp==0:
            self.button_prev_graph['state']='disabled'
        else:
            self.button_prev_graph['state']='enabled'
        self.button_next_graph.place(x=650,y=750)
        self.button_prev_graph.place(x=550,y=750)
    def graph_scatter(self,category='',segments_run=[], subsegments_run=[],data=[]):
        data=data.loc[data['Value']!='MISSING']
        markers=list(self.exported_data[self.patients[0]].keys())
        markers=pd.unique(data['Biomarker'])
        files=['GLOBAL','ENDO','EPI']
        #print(pd.unique(data['Segment Subtype']))
        
        for segment in pd.unique(data['Segment Type']):
            dt_seg=data.loc[(data['Segment Type']==segment)]
            
            for subsegment in pd.unique(dt_seg['Segment Subtype']):
                to_graph=[]
                to_graph_x=[]
                to_graph_y=[]
                for i in range(len(pd.unique(data['Category']))):
                    to_graph.append([])
                    to_graph_x.append([])
                    to_graph_y.append([])
                y_ax_labels=[]
                dt=dt_seg.loc[(dt_seg['Segment Subtype']==subsegment)]
                upper_limit = dt['Value'].quantile(0.75)
                lower_limit = dt['Value'].quantile(0.25)
                dt=dt[(dt['Value'] <= upper_limit) & (dt['Value'] >= lower_limit)]

                for mr_id,marker in enumerate(markers):
                    dt_marker=dt[dt['Biomarker']==marker]
                
                    for _,i in enumerate(pd.unique(data['Category'])):
                        cur_list=list(dt_marker[(dt_marker['Category'] == i)]['Value'])
                        to_graph_y[_]+=cur_list
                        mar_st=marker.replace('Biomarker: ','')
                        mar_st=mar_st.replace('-',' ')
                        mar_st = [word[0] for word in mar_st.split()]
                        mar_st=''.join(mar_st)

                        to_graph_x[_]+=[mar_st]*len(cur_list)

                #dt_cat1=dt_marker[(dt_marker['Category'] == 'Type 0')]['Value']
                #print(dt_cat1)
                #dt_cat2=dt_marker[(dt_marker['Category'] == 'Type 1')]['Value']
                #mar_st=marker.replace('Biomarker: ','')
                #mar_st=mar_st.replace('-',' ')
                #mar_st = [word[0] for word in mar_st.split()]
                #mar_st=''.join(mar_st)
                #y_ax_labels.append(mar_st)

                #to_graph_1.append(dt_marker['Value'])
                #to_graph_1.append(dt_cat1)
                #to_graph_2.append(dt_cat2)
                fig=plt.Figure(figsize=(9,6))

                ax=fig.add_subplot(111)
                xs=[-0.4,0.4]
                colors=['#D7191C','#2C7BB6']
                graphs=[]
                
                for _,i in enumerate(to_graph_x):
                    #if self.status_reqs[20].get():
                        #for val in to_graph_x 
                        #stat, pvalue = stats.ttest_ind(to_graph[0][_], to_graph[1][_])
                        #pvalue_asterisks=self.convert_pvalue_to_asterisks(pvalue)
                            #if pvalue_asterisks!='ns':
                                #y_ax_labels[_]=(f'{y_ax_labels[_]} {pvalue_asterisks}') 
                    #u, ind = np.unique(i, return_inverse=True)
                    ax.scatter(i, to_graph_y[_])
                    #plt.xticks(rotation=45, ha='right')

                    #ax.set_xticks(range(len(u)), u)
                    #plt.plot(ind,to_graph_y[_])
                    #plt.show()
                        #self.set_box_color(bpl, colors[_])
                #else:
                    
                    
                            #ax.text(np.mean(to_graph[0][_]),(_*2)-0.5,round(np.mean(to_graph[0][_]),3))
                            #ax.text(np.mean(to_graph[1][_]),(_*2)+0.2,round(np.mean(to_graph[1][_]),3))
                   # for _,i in enumerate(to_graph):
                       # bpl = ax.boxplot(i, positions=np.array(range(len(i)))*2.0+xs[_], sym='', widths=0.6,vert = 0)
                        #self.set_box_color(bpl, colors[_])

                #bpr = ax.boxplot(to_graph[1], positions=np.array(range(len(to_graph[1])))*2.0+0.4, sym='', widths=0.6,vert = 0)
                # colors are from http://colorbrewer2.org/
                #self.set_box_color(bpr, '#2C7BB6')
                #ax.set_yticks(range(0, len(markers) * 2, 2))
                #ax.set_yticklabels(y_ax_labels,fontsize=8)
                #print(y_ax_labels)
                #plt.xticks(range(0, len(markers) * 2, 2), markers)
                #plt.ylim(-2, len(markers)*2)
                #plt.tight_layout()
                #ax.boxplot(to_graph_1,vert = 0)
                fig.autofmt_xdate(rotation=45)
                fig.patch.set_facecolor('lightblue')
                num_ct=len(pd.unique(data['Category']))
                cats=", ".join((pd.unique(data['Category'])))
                fig.suptitle("\n".join(wrap(f'Figure shows OS-CMR values in the {subsegment} for {segment} in {len(self.patients)} patients across biomarkers. Patients are grouped in {num_ct} categories, namely {cats}.',100)), fontsize=10)
                #{", ".join(segments_run)} 
                fig.subplots_adjust(left=0.1, right=0.995, top=0.912, bottom=0.14)
                chart=FigureCanvasTkAgg(fig,self.graphframe)

                self.graphs.append(chart)

        #for i in range(12):
            #data.append(np.random.normal(70, 40, 200))
        #fig=plt.Figure(figsize=(9,6))
        #fig.add_subplot(111).boxplot(data,vert = 0)
 
        # Creating plot
        #fig.patch.set_facecolor('lightblue')
        #fig.suptitle('Graph', fontsize=20)
        #chart=FigureCanvasTkAgg(fig,self.graphframe)
        #self.graphs.append(chart)
        #self.update_cur_view()

        #if len(self.graphs)==1:
        self.view_graph(0)
        #pass
    def dis_check(self):
        if self.status_reqs[3].get():
            for i in self.graph_parts:
                i.config(state=DISABLED)
            self.graph_parts[0].config(state=NORMAL)
        else:
            for i in self.graph_parts:
                i.config(state=NORMAL)

    def view_graph(self,numid):
        
        
        if numid>len(self.graphs)-1 or numid<0:
            #numid=0
            return 
        
        try:
            self.currently_graphing.get_tk_widget().place_forget()
        except:
            pass

        self.currently_graphing=self.graphs[numid]
        try:
            self.toolbar.destroy()
        except:
            pass
        self.currently_graphing.get_tk_widget().place(x=0)
        self.toolbar=NavigationToolbar2Tk(self.currently_graphing,self.graphframe)
        self.toolbar.update()
        self.currently_graphing._tkcanvas.place(x=0,y=100)
        self.gframe_title.pack()
        self.currently_disp=numid

        if self.currently_disp==len(self.graphs)-1:
            self.button_next_graph['state']='disabled'
        elif self.currently_disp<len(self.graphs):
            self.button_next_graph['state']='enabled'
        if self.currently_disp==0:
            self.button_prev_graph['state']='disabled'
        else:
            self.button_prev_graph['state']='enabled'


        self.update_cur_view()
        self.button_next_graph.lift()
        self.button_prev_graph.lift()

    def update_cur_view(self):
        self.cur_graph_count=ttk.Label(self.graphframe, text=f'Showing {self.currently_disp+1}/{len(self.graphs)}',font=('Times',13), background='#f4f4f4')
        self.cur_graph_count.place_forget()
        self.cur_graph_count.place(x=400,y=750)
        self.cur_graph_count.lift()

    def button_clicked(self):
        #self.destroy()
        #import graphing_interface
        exit()
        #showinfo(title='Information', message='Hello, Tkinter!')
    def delete_all_graphs(self):
        for i in self.graphs:
            i.get_tk_widget().destroy()
        self.geometry("560x800")
        self.graphs=[]
        self.currently_disp=0
        self.currently_graphing=[]

    def delete_patient(self):
        indexList= self.lists[0].curselection()
        for i in indexList[::-1]:
            index=i
            val=self.lists[0].get(index)
            self.lists[0].delete(index)
            self.patients.remove(val)

import pickle
"""
with open('data_frame_export.pickle', 'rb') as handle:
    b = pickle.load(handle)
with open('data_export.pickle', 'rb') as handle:
    a = pickle.load(handle)
app = CMR_graphing(b,a)
#app = CMR_graphing()
app.mainloop()
"""
