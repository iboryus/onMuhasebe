from tkinter import * 
from tkinter import filedialog as fd
from tkinter import ttk
import pyperclip
import win32com.client
from colorama import Fore, Back, Style, init
import json
import random
import math

class GUI:
    chr_esc="\n"
    filename=''
    # gui related
    root=[]
    lbl_filename=[]
    lbl_par1=[]
    lbl_par2=[]
    lbl_wordlen=[]
    lbl_total=[]
    tree=[]
    # word related
    word=[]
    doc=[]
    wb=[]
    paragraphs=[]
    kstart=0
    sentence_rem=""
    word_limit=920
    app_title="Application"

    #find-replace
    str_find=""
    str_replace=""

    #basliklar
    basliklar=[]
    basliklar32=[]
    i32=0

    marka="Kingroyal"

    def alert(self,msg):
        self.root.title(self.app_title+":"+msg)
        return self

    def word_initialize(self):
        init()      
        self.word=win32com.client.Dispatch("Word.Application")
        self.word.visible=False
        self.word.DisplayAlerts=False
        self.kstart=0
        self.alert("Word initialized")
        self.root.update()
        return self

    def grab_paragraphs(self):
        if len(self.filename)>0:
            self.wb=self.word.Documents.Open(self.filename)
            self.doc=self.word.ActiveDocument
            # get paragraphs from word                         
            for par in self.doc.Paragraphs:
                self.paragraphs.append(par.Range.Text)
            # self.doc.Close(True)
            # self.doc=[]
            self.word_deinit()
            self.i32=0
            for x in range(len(self.paragraphs)-1,0,-1):
                temp=self.paragraphs[x].split()
                if temp!=[]:
                    self.tree.insert('', 0, values=(str(x)+":"+temp[0], str(len(temp))))
        return self

    def word_deinit(self):
        # self.alert("Word saved.")
        if self.doc is not []:
            self.doc.Save()
            self.doc.Close(True)
            self.doc=[]
        self.word.Quit()
        self.word=[]
        return self

    def open_file(self,e):
        self.filename=""
        self.lbl_filename.config(text="")

        filetypes = (('Word files', '*.docx'),('All files', '*.*'))
        self.filename = fd.askopenfilename(
            title='Open a file',
            filetypes=filetypes)
        self.filename=self.filename.replace("\\","")
        self.filename=self.filename.replace("/","\\\\")
        print(self.filename)

        if len(self.filename)>0:
            self.lbl_filename.config(text=self.filename)
            if self.word is []:
                self.word_initialize()
            self.grab_paragraphs()
            self.lbl_filename.config(fg="green",bg="white")
        else:
            self.lbl_filename.config(fg="black",bg="red")
        return self

    def cut_paragraph(self,e):
        if len(self.paragraphs)>0:
            self.work()
        else:
            self.root.title("Application:First open a Word file.")
            self.root.update()
        return self
    
    def work(self):
        baslik_index=random.randint(0,len(self.basliklar)-1)
        word_count=len(self.sentence_rem.split())
        kalan_metin = ''
        
        metin=self.sentence_rem
        kcrit=None
        delta=0
        for k in range(self.kstart,len(self.paragraphs),1):
            paragraph=self.paragraphs[k]
            
            if word_count+len(paragraph.split())>=self.word_limit:
                kcrit=k
                delta=0
                kelimeler=paragraph.split()
                
                while(not ((kelimeler[delta][-1]=='.') and word_count+delta>=self.word_limit)):
                    delta=delta+1 
                    if delta>=len(kelimeler):
                        delta=len(kelimeler)-1
                        break
                break
            else:
                word_count=word_count+len(paragraph.split())

        #print(Fore.BLUE + str(word_count+delta)+">=920 olmalı")
        if kcrit is not None:
            parsayisi=kcrit-self.kstart-1
            dpar=math.floor(parsayisi/4)
            # print(parsayisi)
            # print(dpar)
            for k in range(self.kstart,kcrit,1):
                paragraph=self.paragraphs[k]
                if k==self.kstart+1:
                    metin=metin+"<h2><strong>"+self.marka+" "+self.basliklar[baslik_index]["h2"]+"</strong></h2>&nbsp;"
                elif k==self.kstart+dpar*2:
                    metin=metin+"<h3><strong>"+self.marka+" "+self.basliklar[baslik_index]["h31"]+"</strong></h3>&nbsp;"
                elif k==self.kstart+dpar*3:
                    metin=metin+"<h3><strong>"+self.marka+" "+self.basliklar32[self.i32]["h32"]+"</strong></h3>&nbsp;"
                    self.i32=self.i32+1
                    if self.i32==29:
                        self.i32=0
                elif k==self.kstart+dpar*4:
                    metin=metin+"<h4><strong>"+self.marka+" "+self.basliklar[baslik_index]["h4"]+"</strong></h4>&nbsp;"
                metin=metin+paragraph+self.chr_esc+self.chr_esc

            # önceki paragraf
            paragraph=self.paragraphs[kcrit-1]
            #print(Fore.BLUE + str(kcrit-1)+":")
            #print(Fore.GREEN+paragraph+self.chr_esc)

            # kritik paragraf
            paragraph=self.paragraphs[kcrit]
            kelimeler=paragraph.split()
            metin = metin +' '.join(kelimeler[:delta+1])+self.chr_esc+self.chr_esc
            kalan_metin = kalan_metin +' '.join(kelimeler[delta+1:])+self.chr_esc
            self.sentence_rem=' '.join(kelimeler[delta+1:])+self.chr_esc
            #print(Fore.BLUE + str(kcrit)+":")
            #print(Fore.GREEN+' '.join(kelimeler[:delta+1])+self.chr_esc)
            #print(Fore.RED+' '.join(kelimeler[delta+1:])+self.chr_esc)

            # sonraki paragraf
            self.kstart=kcrit+1 #python index kcrit+1
            self.alert("Starting index "+str(self.kstart))
            paragraph=self.paragraphs[kcrit+1]
            #print(Fore.BLUE + str(kcrit+1)+":")
            #print(Fore.RED+paragraph)
            #print(Style.RESET_ALL)

            for k in range(kcrit+1,len(self.paragraphs),1):
                paragraph=self.paragraphs[k]
                kalan_metin=kalan_metin+paragraph+self.chr_esc
                
            #print(str(len(metin.split()))+" Kelime Kesildi")
            #print(str(len(kalan_metin.split()))+" Kelime Kaldı")
            # print(metin)   
            self.lbl_par1.delete('1.0', END)                                                                           
            self.lbl_par2.delete('1.0', END)

            self.lbl_par1.insert('1.0',metin)                      
            self.lbl_par2.insert('1.0',kalan_metin)
            self.root.update()

            self.lbl_total.config(text=str(len(metin.split()))+"/"+str(len(kalan_metin.split())))
            pyperclip.copy(metin)
            # self.doc.Content.Text = kalan_metin
            # self.doc.Save()
        else:
            self.lbl_total.config(text="Anan!")
            self.lbl_total.config(bg="red")
      
        return self
    
    def on_change(self,e):
        if e.char.isnumeric():
            self.word_limit=int(self.lbl_wordlen.get("1.0",END))
            print(self.word_limit)
        else:
            pass
        return self
    
    def on_change_find(self,e):
        self.str_find=self.lbl_find.get("1.0",END)
        self.str_find=self.str_find.replace("\n","")
        return self
    
    def on_change_replace(self,e):
        self.str_replace=self.lbl_replace.get("1.0",END)
        self.str_replace=self.str_replace.replace("\n","")
        return self

    def on_btn_replace_click(self):
        str_find=self.str_find
        str_replace=self.str_replace
        print(str_find+"->"+str_replace)
        for i in range(0,len(self.paragraphs)):
            self.paragraphs[i]=self.paragraphs[i].replace(str_find,str_replace)
        return self
    
    def __init__(self):
        self.root = Tk()
        self.root.title("Application")
        self.root.geometry('800x600')

        # Menu
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File",underline=0, menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.open_file([]),underline=1,accelerator="Ctrl+O")
        file_menu.add_command(label="Cut", command=lambda: self.cut_paragraph([]),underline=1,accelerator="Ctrl+X")

        self.root.config(menu=menu_bar)                                                                                                                                   
        self.root.bind("<Control-o>",self.open_file)
        self.root.bind("<Control-x>",self.cut_paragraph)

        # GUI
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)
        self.root.columnconfigure(2,weight=1)

        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=1)

        self.lbl_par1 =Text(self.root, fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
        self.lbl_par1.grid(row=0,columnspan=2,sticky="ew")

        self.lbl_par2 =Text(self.root,  fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
        self.lbl_par2.grid(row=1,columnspan=2,sticky="ew") 

        lbl_filename_holder = Label(self.root, text = "File:",fg = "black",width=4,justify="left")
        lbl_filename_holder.grid(column=0,row=3,sticky="w")
        self.lbl_filename = Label(self.root, text = self.filename,justify="left")
        self.lbl_filename.grid(column=1,row=3,sticky="w")
                                                      
        lbl_wordlen_holder= Label(self.root, text = "Word limit:",fg = "black",width=10)
        lbl_wordlen_holder.grid(column=2,row=3,sticky="e")
        self.lbl_wordlen =Text(self.root,  fg="black", width=5,height=1)
        self.lbl_wordlen.grid(column=3,row=3,sticky="e")         
        self.lbl_wordlen.bind("<KeyRelease>", self.on_change)   
        self.lbl_wordlen.insert('1.0',str(self.word_limit))                                            

        self.lbl_total= Label(self.root, text = "./.",fg = "black",width=10)
        self.lbl_total.grid(column=3,row=4,sticky="w")
        self.lbl_total.config(bg="green",fg="white")


        frame1=Frame(None,height=30)
        # find
        frame1.grid(column=0,row=4,sticky="we")
        lbl_find_holder= Label(frame1, text = "Find:",fg = "black")
        lbl_find_holder.grid(column=0,row=0,sticky="w")
        self.lbl_find =Text(frame1,  fg="black", width=10,height=1)
        self.lbl_find.grid(column=1,row=0,sticky="w")         
        self.lbl_find.bind("<KeyRelease>", self.on_change_find)   
        #replace                          
        lbl_replace_holder= Label(frame1, text = "Replace:",fg = "black")
        lbl_replace_holder.grid(column=3,row=0,sticky="e")
        self.lbl_replace =Text(frame1,  fg="black", width=10,height=1)
        self.lbl_replace.grid(column=4,row=0,sticky="e")         
        self.lbl_replace.bind("<KeyRelease>", self.on_change_replace)   
        #button
        self.btn_replace=Button(frame1,text="Ok",command=self.on_btn_replace_click)
        self.btn_replace.grid(row=0,column=5)


        self.tree=ttk.Treeview(None, columns=("paragraph","word_count"), show='headings')
        self.tree.heading('paragraph', text='Paragraph')
        self.tree.column('paragraph', minwidth=0, width=120, stretch=NO)
        self.tree.heading('word_count', text='Words')
        self.tree.column('word_count', minwidth=0, width=80, stretch=NO)
        self.tree.grid(row=0, column=2,rowspan=2,columnspan=2,sticky="nswe")

        self.root.update()
        self.word_initialize()
        self.load_basliklar()

        self.root.mainloop()

    def load_basliklar(self):
        with open("basliklar.json","r",encoding="utf8") as file:
            self.basliklar=json.loads(''.join(file.readlines()))
        with open("basliklar32.json","r",encoding="utf8") as file:
            self.basliklar32=json.loads(''.join(file.readlines()))
        return self
    

    def __del__(self):
        # self.word_deinit()
        pass
    
gui=GUI()

