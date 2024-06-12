from tkinter import * 
from tkinter import filedialog as fd
from tkinter import ttk
import pyperclip
import win32com.client
from colorama import Fore, Back, Style, init

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
    word_limit=120
    app_title="Application"

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
                self.paragraphs.append(par)
            # self.doc.Close(True)
            # self.doc=[]

            for x in range(len(self.paragraphs)-1,0,-1):
                temp=self.paragraphs[x].Range.Text.split()
                if temp!=[]:
                    self.tree.insert('', 0, values=(str(x)+":"+temp[0], str(len(temp))))
        return self

    def word_deinit(self):
        # self.alert("Word saved.")
        if self.doc is not []:
            self.doc.Save()
            self.doc.Close(True)
        self.word.Quit()
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
        word_count=len(self.sentence_rem.split())
        kalan_metin = ''
        metin=self.sentence_rem
        kcrit=None
        delta=0
        for k in range(self.kstart,len(self.paragraphs),1):
            paragraph=self.paragraphs[k]
            
            if word_count+len(paragraph.Range.Text.split())>=self.word_limit:
                kcrit=k
                delta=0
                kelimeler=paragraph.Range.Text.split()
                
                while(not ((kelimeler[delta][-1]=='.') and word_count+delta>=self.word_limit)):
                    delta=delta+1 
                    if delta>=len(kelimeler):
                        delta=len(kelimeler)-1
                        break
                break
            else:
                word_count=word_count+len(paragraph.Range.Text.split())

        #print(Fore.BLUE + str(word_count+delta)+">=920 olmalı")
        if kcrit is not None:
            for k in range(self.kstart,kcrit,1):
                paragraph=self.paragraphs[k]
                metin=metin+paragraph.Range.Text+self.chr_esc+self.chr_esc

            # önceki paragraf
            paragraph=self.paragraphs[kcrit-1]
            #print(Fore.BLUE + str(kcrit-1)+":")
            #print(Fore.GREEN+paragraph.Range.Text+self.chr_esc)

            # kritik paragraf
            paragraph=self.paragraphs[kcrit]
            kelimeler=paragraph.Range.Text.split()
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
            #print(Fore.RED+paragraph.Range.Text)
            #print(Style.RESET_ALL)

            for k in range(kcrit+1,len(self.paragraphs),1):
                paragraph=self.paragraphs[k]
                kalan_metin=kalan_metin+paragraph.Range.Text+self.chr_esc
                
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

        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=1)

        self.lbl_par1 =Text(self.root, fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
        self.lbl_par1.grid(row=0,columnspan=2,sticky="ew")

        self.lbl_par2 =Text(self.root,  fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
        self.lbl_par2.grid(row=1,columnspan=2,sticky="ew") 

        lbl_filename_holder = Label(self.root, text = "File:",fg = "black",width=4,justify="left")
        lbl_filename_holder.grid(column=0,row=4,sticky="w")
        self.lbl_filename = Label(self.root, text = self.filename,justify="left")
        self.lbl_filename.grid(column=1,row=4,sticky="w")
                                                      
        lbl_wordlen_holder= Label(self.root, text = "Word limit:",fg = "black",width=10)
        lbl_wordlen_holder.grid(column=2,row=4,sticky="e")
        self.lbl_wordlen =Text(self.root,  fg="black", width=5,height=1)
        self.lbl_wordlen.grid(column=3,row=4,sticky="e")         
        self.lbl_wordlen.bind("<KeyRelease>", self.on_change)   
        self.lbl_wordlen.insert('1.0',str(self.word_limit))                                            

        self.lbl_total= Label(self.root, text = "./.",fg = "black",width=10)
        self.lbl_total.grid(column=3,row=5,sticky="w")
        self.lbl_total.config(bg="green",fg="white")

        self.tree=ttk.Treeview(None, columns=("paragraph","word_count"), show='headings')
        self.tree.heading('paragraph', text='Paragraph')
        self.tree.column('paragraph', minwidth=0, width=80, stretch=NO)
        self.tree.heading('word_count', text='Words')
        self.tree.column('word_count', minwidth=0, width=50, stretch=NO)
        self.tree.grid(row=0, column=2, sticky="nsw",rowspan=2,columnspan=3)

        self.root.update()
        self.word_initialize()

        self.root.mainloop()

    def __del__(self):
        self.word_deinit()

gui=GUI()
