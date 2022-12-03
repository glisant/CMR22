# Python program to create
# a file explorer in Tkinter

##ADD POSSIBILITY OF LABELING OR REMOVING PATIENTS
#To remove biomarkers you just skip over it at extraction
#Have a view graph that creates graphs of things you want on the go! 
from PIL import ImageTk
from tkinter import ttk
import PIL.Image
from tkinter.messagebox import showinfo
# import all components
# from the tkinter library
from tkinter import *
import CMR_DATA_EXTRACT
import CMR_graphing_interface
import shutil
import os
import time
all_data=[]
biomarkers=[ 'End-Systole Mean Intensity', 'End-Systole Intensity - Phase Normalized',
    'End-Systole Intensity - Series Normalized', 'End-Systole O2 Relative to Lv Bloodpool',
    'End-Systole O2 Relative to Rv Bloodpool', 'End-Systole O2 Relative to Lv & Rv Bloodpools',
    'End-Diastole Mean Intensity', 'End-Diastole Intensity - Phase Normalized',
    'End-Diastole Intensity - Series Normalized', 'End-Diastole O2 Relative to Lv Bloodpool',
    'End-Diastole O2 Relative to Rv Bloodpool', 'End-Diastole O2 Relative to Lv & Rv Bloodpools']

phase_FILE=''
RAW_FILES=[]

# import filedialog module
from tkinter import filedialog
  
# Function for opening the
# file explorer window
all_files_dirs=[]

def graph_t(exp,dataframe):
    window.destroy()
    
    app=CMR_graphing_interface.CMR_graphing(dataframe,exp)
    #app = CMR_graphing()
    app.mainloop()

def openNewWindow(exp,dataframe):
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Data Extracted Succesfully!")
    Label(newWindow,
          text ="Data Extracted Succesfully!").pack()
    # sets the geometry of toplevel
    newWindow.geometry("400x200")
    progress=ttk.Progressbar(
    newWindow,
    orient='horizontal',
    mode='determinate',
    length=280)
    
    progress.pack()
    
    
    progress.start(10)
    progress.stop()
    progress['value'] = 100
    Fl2=Label(newWindow,
          text ='You can click below to close windows or head to the graphing interface')
    Fl2.place(x=10,y=70)
    
    button_exit = ttk.Button(newWindow,
                     text = "Exit All",
                     command = exit)
    button_graph = ttk.Button(newWindow,
                     text = "Graph",
                     command = lambda: graph_t(exp,dataframe))
    
    button_exit.place(x=140,y=110)
    button_graph.place(x=220,y=110)
    #button_run1 = Button(window,
                        #text = "Begin",
                        #command = run)
    #button_run1.pack(ipady=60)
    #run(Fl2)
    #Fl2.config(text=f'Working on {1}...')
    
    #return(Fl2)
    
    # A Label widget to show in toplevel
    
    
def run():
    global all_files_dirs,status,filex, all_data
    
    #print('lol')
    ifiles=[]
    if len(all_files_dirs)>4:
        showinfo(title='Information', message='Too many files selected, please select 3 files + phase file. For more information contact glisant.plasa@mail.mcgill.ca')
        #print('Too many files selected, please select 3 files + phase file.')
        #exit()
    else:
        for file in all_files_dirs:
            src_path = file
            dst_path = f'{os.getcwd()}\{os.path.basename(file)}'
            ifiles.append(os.path.basename(file))
            try:
                shutil.copy(src_path, dst_path)
            except:
                pass
        
        if  len(ifiles)>0 and ifiles[-1]!='phases.xlsx':
            idp=ifiles.index('phases.xlsx')
            
            ifiles[-1], ifiles[idp]=ifiles[idp], ifiles[-1]
            
        
        markers0=Lb3.get(0,END)
        markers=[]
        for mark in markers0:
            markers.append('Biomarker: '+mark)
        
        required=[]
        for i in status:
            required.append(i.get())
        
        name=filex.get()
        if name=='':
            name='data_export_template'
        name+='.xlsx'
        
        f_export,data_frame=CMR_DATA_EXTRACT.run(markers,ifiles[0:len(ifiles)-1],ifiles[-1],name,required[0:3],status[5].get())
        all_data=f_export
        #1/0
        openNewWindow(f_export,data_frame)
def browseFiles(idin):
    global lists,runsid,all_files_dirs
    filename = filedialog.askopenfilenames(
                                          title = "Select Files",
                                          filetypes = (("Excel files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))
    if lists[idin].size()==1 and runsid[idin]==0:
        runsid[idin]=1
        lists[idin].delete(0)
    for file in filename:
        all_files_dirs.append(file)
        lists[idin].insert(END,os.path.basename(file)+ '\n')
    #print(all_files_dirs)
    # Change label contents
    #label_file_explorer.configure(text="File Opened: "+filename)
def reset():
    global Lb3
    Lb3.delete(0,END)
    for marker in biomarkers:
        Lb3.insert(END,marker)
      
def remove_item(idin):
    global lists,all_files_dirs
    if idin>1 or runsid[idin]>0:
        selected_checkbox = lists[idin].curselection()
        if selected_checkbox!=():
            file_torem=lists[idin].get(selected_checkbox)
            for _,f in enumerate(all_files_dirs):
                if os.path.basename(f)==file_torem:
                    all_files_dirs.remove(f)
            #all_files_dirs
        #for selected_checkbox in selected_checkboxs[::-1]:
            lists[idin].delete(selected_checkbox)                                                                                                  
# Create the newWindow window
window = Tk()
window.resizable(False,False)
window.wm_attributes('-transparentcolor', 'red')
# Set window title
window.title('Automated Data Extraction')
width = 350
height = 120
img = PIL.Image.open("CMR_logo_right.png")
img2 = PIL.Image.open("CMR_logo_left.png")
img = img.resize((170,100), PIL.Image.ANTIALIAS)
img2 = img2.resize((190,90), PIL.Image.ANTIALIAS)
photoImg =  ImageTk.PhotoImage(img)
photoImg2 =  ImageTk.PhotoImage(img2)
Label(image=photoImg,bg='lightblue').place(x=450, y=100)
Label(image=photoImg2,bg='lightblue').place(x=5, y=80)
# Set window size
window.geometry("625x500")
  
#Set window background color
window.config(background = "lightblue")
  
# Create a File Explorer label
#label_file_explorer = Label(window,
                            #text = "File Explorer using Tkinter",
                            #width = 100, height = 4,
                            #fg = "blue")
  
l1 = Label(window, text = "1. Please browse for and select the raw data files:",bg='lightblue')
#l2 = Label(window, text = "Phase Data:")


#l2.place(row = 4, column = 0)
runsid=[0,0]
button_explore_raw_data = ttk.Button(window,
                        text = "Browse Raw Data",
                        command = lambda: browseFiles(0))

button_remove_raw_data = ttk.Button(window,
                        text = "Remove Selected",
                        command = lambda: remove_item(0))

button_explore_phases = ttk.Button(window,
                        text = "Browse Phases",
                        command = lambda: browseFiles(1))


button_remove_phases = ttk.Button(window,
                        text = "Remove Selected",
                        command = lambda: remove_item(1))

button_remove_marker = ttk.Button(window,
                        text = "Remove Selected Marker",
                        command = lambda: remove_item(2))

button_remove_reset = ttk.Button(window,
                        text = "Reset",
                        command =reset)

button_run = ttk.Button(window,
                        text = "Extract Data",
                        command = run)
  
button_exit = ttk.Button(window,
                     text = "Exit",
                     command = exit)
  
# place method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
#label_file_explorer.place(column = 1, row = 1)
l2 = Label(window, text = "2. Select Parts of the data you want to include:", bg='lightblue')
l3 = Label(window, text = "Biomarkers:", bg='lightblue',font='bold')
l4 = Label(window, text = "Select Output Filename:", bg='lightblue')
status=[]
for i in range(7):
    status.append(IntVar())
c = Checkbutton(window, text = "Baseline Breath-Hold", bg='lightblue', variable=status[0])
c.place(x = 270, y = 250)
 
c1 = Checkbutton(window, text = "0s", bg='lightblue', variable=status[1])
c1.place(x = 420, y = 250)
 
c2 = Checkbutton(window, text = "30s", bg='lightblue', variable=status[2])
c2.place(x = 470, y = 250)

c3 = Checkbutton(window, text = "Basal Slices", bg='lightblue', variable=status[3])
c3.place(x = 270, y = 280)

c4 = Checkbutton(window, text = "Mid Slices", bg='lightblue', variable=status[4])
c4.place(x = 420, y = 280)

c5 = Checkbutton(window, text = "Include a dataframe file", bg='lightblue', variable=status[5])
c5.place(x = 270, y = 310)

c6 = Checkbutton(window, text = "Include HTML graph", bg='lightblue', variable=status[6])
c6.place(x = 420, y = 310)

boxes=[c,c1,c2,c3,c4,c5,c6]

for _,box in enumerate(boxes):
    if _<5:
        box.select()
filex= Entry(window, 
         text="Export Filename")
filex.place(x = 400, y = 400)

Lb1= Listbox (height=4, width=100)
Lb1.insert(1, "Please select GLOBAL.xlsx, ENDO.xlsx and EPI.xlsx. Selected Files will appear here.")
l1.place(x = 10, y = 10)
l2.place(x = 10, y = 210)
l3.place(x = 10, y = 230)
l4.place(x = 270, y = 400)

Lb1.place(x = 10, y = 34)

Lb2= Listbox (height=2, width=30)

Lb2.insert(1, "Please select the phases file.")
Lb2.place(x = 10, y = 160)

Lb3= Listbox (height=12, width=42)
for marker in biomarkers:
    Lb3.insert(END,marker)
Lb3.place(x = 10, y = 250)


lists=[Lb1,Lb2,Lb3]
button_run.place(x=528,y=398)
button_remove_raw_data.place(x = 350, y = 110)
button_explore_raw_data.place(x = 200, y = 110)
button_explore_phases.place(x = 200, y = 165)
button_remove_phases.place(x = 350, y = 165)
button_remove_marker.place(x = 30, y = 452)
button_remove_reset.place(x = 200, y = 452)


# Let the window wait for any events
window.mainloop()