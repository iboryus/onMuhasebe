from tkinter import * 
from tkinter import filedialog as fd
from tkinter import ttk
from dataclasses import dataclass
import pyperclip
import win32com.client
import json
import random
import math

@dataclass
class Sentence:
    words:list
    def __len__(self):
        return len(self.words)
    def word_count(self):
        return len(self.words)
    def __getitem__(self, items):
        return self.words[items]
    def tostring(self):
        val=" ".join(self.words)+". "
        return val

@dataclass
class Paragraph:
    sentences:list

    def __init__(self,text:str):
        data=text.replace(". ",".")
        vec=data.split(".")
        if vec.count("\r")>0:
            if vec[-1][-1]=="\r":
                vec[-1]=vec[-1][:-1]
        self.sentences=[Sentence(sentence.split(" ")) for sentence in vec]

    def __len__(self):
        return len(self.sentences)

    def word_count(self):
        return len(self.tostring().split())
    
    def __getitem__(self, items):
        return self.sentences[items]
    
    def get(self,start,stop):
        return self.sentences[start:stop+1]
    
    def tostring(self):
        val="".join([s.tostring() for s in self.sentences])+"\r\n"
        return val

class WordApp:
    __word=[]
    __filename=""
    paragraphs=[]

    def __init__(self):
        self.start_word_app()

    def __del__(self):
        self.word_close()

    def alert(self,msg):
        print(msg)
        return self
    
    def start_word_app(self):
        self.__word=win32com.client.Dispatch("Word.Application")
        self.__word.visible=False
        self.__word.DisplayAlerts=False
        self.alert("Word started...")
        return self
    
    def word_close(self):
        # if self.doc is not []:
        #     self.doc.Save()
        #     self.doc.Close(True)
        #     self.doc=[]
        if self.__word==[]:
            return self
        else:
            self.__word.Quit()
            self.alert("Word closed.")
            self.__word=[]
        return self
    
    def open_file(self,e):
        self.__filename=""

        filetypes = (('Word files', '*.docx'),('All files', '*.*'))
        self.__filename = fd.askopenfilename(
            title='Open a file',
            filetypes=filetypes)
        self.__filename=self.__filename.replace("\\","")
        self.__filename=self.__filename.replace("/","\\\\")
        print(self.__filename)

        if len(self.__filename)>0:
            if self.__word is []:
                self.start_word_app()
            self.grab_paragraphs()
        else:
            self.alert("Open a file!")
        return self
    
    def grab_paragraphs(self):
        if len(self.__filename)>0:
            wb=self.__word.Documents.Open(self.__filename)
            doc=self.__word.ActiveDocument
            self.paragraphs=[]
            # get paragraphs from word                         
            for par in doc.Paragraphs:
                data=par.Range.Text
                self.paragraphs.append(Paragraph(data))
            self.word_close()
            
            print(str(len(self.paragraphs))+" paragraphs counted.")
        else:
            self.alert("Open a file!!")
        return self
    
    def process_paragraphs(self,paragraphs:list):
        word_limit=50
        result=[]
        word_count=0
        for par_index in range(0,len(paragraphs)):
            par=paragraphs[par_index]
            
            if word_count+par.word_count()>word_limit: #critical paragraph
                s_index_old=0
                for s_index in range(0,len(par)):
                    sentence=par[s_index]
                    if word_count+sentence.word_count()>word_limit: #critical sentence
                        new_result=[par_index,s_index_old,s_index,word_count]
                        result.append(new_result)

                        word_count=0
                        s_index_old=s_index+1
                    else:
                        word_count+=sentence.word_count()

                new_result=[par_index,s_index_old,len(par)]
                result.append(new_result)
                
            else:
                word_count+=par.word_count()

        print(result)

        i=0
        while i<len(result)-1:
            text=""
            if len(result[i])==4:
                res=result[i]
                ip=res[0]
                par=paragraphs[ip]
                sentences=par.get(res[1],res[2])
                text+=par.tostring()
                text=text.replace(". . ",". \r\n")
                print(f"{text} {len(text.split())} words\n")
                i+=1
            else:
                res_start=result[i]
                res_stop=result[i+1]

                for ip in range(res_start[0],res_stop[0]+1):
                    par=paragraphs[ip]
                    if ip==res_start[0]:
                        text+="".join([s.tostring() for s in par.get(res_start[1],res_start[2])])
                    elif ip==res_stop[0]:
                        text+="".join([s.tostring() for s in par.get(res_stop[1],res_stop[2])])
                    else:
                        text+=par.tostring()
                i+=2
                text=text.replace(". . ",". \r\n")
                print(f"{text} {len(text.split())} words\n")
            

        return self
                        


# italic kısmında paragraf yapıyor
# . . ekliyor

if __name__=="__main__":
    app=WordApp()
    # app.open_file([])
    paragraph1=Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin at massa ut nulla pellentesque elementum id non leo. Vivamus sagittis pretium mauris et porttitor. Nunc sollicitudin gravida nisi a tempus. Cras et faucibus sem. Etiam gravida commodo nibh, dapibus pellentesque ligula luctus quis. Etiam viverra lobortis nisi non rutrum. Nullam et venenatis eros, pharetra tempor quam. Nam quis bibendum metus. Morbi posuere imperdiet diam, a luctus felis tempor a. Pellentesque condimentum libero eget justo accumsan dignissim. Ut eleifend maximus nulla at pretium.")
    paragraph2=Paragraph("Mauris ac sagittis tellus, in tincidunt magna. Phasellus porttitor mauris non orci convallis venenatis. Nam sed ultrices felis. Etiam sed mi nulla. Praesent volutpat pellentesque condimentum. Integer sit amet lacus arcu. Sed mollis dictum scelerisque.")
    paragraph3=Paragraph("Cras facilisis massa non nisi aliquam, eu posuere risus porttitor. Duis gravida elit nec imperdiet sagittis. Donec eget euismod nisl. Aenean leo nisl, rutrum non diam at, aliquet sagittis massa. Donec pharetra ut mauris id pellentesque. Aliquam vulputate porta dapibus. Vivamus nec libero quis mauris aliquet varius. Proin auctor, massa fringilla cursus pretium, sem dolor blandit ex, in bibendum nisi sapien non diam. Sed non orci eu odio vestibulum vulputate. Phasellus enim eros, aliquet condimentum mattis sed, finibus nec velit. Vivamus at magna faucibus, fringilla nibh quis, consectetur tortor. Nullam iaculis luctus lacus, non vestibulum elit posuere eget.")
    paragraph4=Paragraph("Integer mollis ornare urna, eget lobortis risus varius bibendum. Morbi rutrum libero in egestas convallis. Aliquam sed quam mauris. Nulla tincidunt pharetra dolor, vel efficitur sem pulvinar sit amet. Sed varius ut nulla nec mollis. Curabitur ac vehicula sem. Nam sed tellus ut sem faucibus cursus. Mauris molestie diam quis lectus tincidunt pellentesque dictum eget urna. Integer interdum tempus consequat. In quis nibh nec turpis vestibulum maximus sed ut elit. Sed dictum leo vel mauris blandit pellentesque. Aenean at pretium erat. Integer ac venenatis odio. Suspendisse dignissim ullamcorper fermentum. In purus justo, varius et bibendum id, varius et arcu.")
    paragraph5=Paragraph("Vestibulum neque magna, dictum vel pulvinar a, consequat nec est. Cras scelerisque tempor metus, id dictum dolor convallis vel. Mauris ut dignissim urna, id mattis arcu. Curabitur eu venenatis tellus. Curabitur lacinia at ligula nec finibus. Donec bibendum arcu ac enim dapibus, sed pretium purus commodo. Pellentesque viverra nulla nibh, non cursus libero hendrerit suscipit. Cras et eros vel ipsum convallis consectetur volutpat ac eros. Suspendisse potenti. Phasellus eros felis, volutpat ac ipsum quis, egestas pretium velit. Cras sit amet nulla vestibulum, convallis nunc vitae, sagittis sapien. Duis eget egestas justo, in luctus mi.")
    paragraph6=Paragraph("Fusce ac tincidunt erat. Ut at felis elit. Mauris magna lectus, varius eget mattis sed, finibus in erat. Vivamus quis semper erat. Donec pharetra justo tellus. Pellentesque vel efficitur orci, sit amet finibus libero. Morbi dictum vel quam vel vulputate. Vivamus aliquet quis tortor in fringilla. Maecenas vitae tellus tincidunt justo blandit dapibus nec ac tellus. Praesent in lacus lobortis nunc interdum venenatis. Maecenas sapien felis, venenatis ac neque vitae, vestibulum iaculis orci. Aenean eu facilisis purus, ut imperdiet dui. Integer molestie diam et sapien congue, sed interdum risus auctor. Nam ut dolor at mauris tempus porttitor ac et odio. Curabitur turpis nisl, ornare ac odio sed, rutrum viverra lacus. Aliquam dictum nisl eu est condimentum, sed auctor nisi aliquet.")
    paragraph7=Paragraph("Ut gravida, eros in sodales pulvinar, urna metus tincidunt nisi, non auctor urna leo in orci. Duis sagittis ante sed neque lobortis ullamcorper eu ut dui. Nullam tincidunt justo vitae sapien elementum, vel maximus leo malesuada. Vestibulum magna risus, ultricies sit amet consequat sed, faucibus in mi. Nullam convallis sem ut ultricies sollicitudin. Curabitur dolor risus, rutrum quis accumsan sed, mattis id massa. Vivamus ullamcorper accumsan sem vel molestie.")
    paragraph8=Paragraph("Suspendisse commodo iaculis dui, non pellentesque diam. In mollis libero ut lectus eleifend semper. Aliquam a diam euismod odio sagittis ultricies nec nec quam. Morbi ut consectetur lacus, vel consectetur risus. Curabitur justo felis, luctus eget turpis eget, viverra aliquet justo. Proin vestibulum, tellus eget tempor dictum, velit augue tincidunt metus, quis euismod.")
    paragraphs=[paragraph1,paragraph2,paragraph3,paragraph4,paragraph5,paragraph6,paragraph7,paragraph8]
    app.process_paragraphs(paragraphs)



# class GUI:
#     chr_esc="\n"
#     filename=''
#     # gui related
#     root=[]
#     lbl_filename=[]
#     lbl_par1=[]
#     lbl_par2=[]
#     lbl_wordlen=[]
#     lbl_total=[]
#     tree=[]
#     # word related
#     word=[]
#     doc=[]
#     wb=[]
#     paragraphs=[]
#     kstart=0
#     sentence_rem=""
#     word_limit=920
#     app_title="Application"

#     #find-replace
#     str_find=""
#     str_replace=""

#     #basliklar
#     basliklar=[]
#     basliklar32=[]
#     i32=0

#     marka="Bahisdiyo"

#     def alert(self,msg):
#         self.root.title(self.app_title+":"+msg)
#         return self

#     def word_initialize(self):
#         init()      
#         self.word=win32com.client.Dispatch("Word.Application")
#         self.word.visible=False
#         self.word.DisplayAlerts=False
#         self.kstart=0
#         self.alert("Word initialized")
#         self.root.update()
#         return self

#     def grab_paragraphs(self):
#         if len(self.filename)>0:
#             self.wb=self.word.Documents.Open(self.filename)
#             self.doc=self.word.ActiveDocument
#             # get paragraphs from word                         
#             for par in self.doc.Paragraphs:
#                 self.paragraphs.append(par.Range.Text)
#             # self.doc.Close(True)
#             # self.doc=[]
#             self.word_deinit()
#             self.i32=0
#             for x in range(len(self.paragraphs)-1,0,-1):
#                 temp=self.paragraphs[x].split()
#                 if temp!=[]:
#                     self.tree.insert('', 0, values=(str(x)+":"+temp[0], str(len(temp))))
#         return self

#     def word_deinit(self):
#         # self.alert("Word saved.")
#         if self.doc is not []:
#             self.doc.Save()
#             self.doc.Close(True)
#             self.doc=[]
#         self.word.Quit()
#         self.word=[]
#         return self

#     def open_file(self,e):
#         self.filename=""
#         self.lbl_filename.config(text="")

#         filetypes = (('Word files', '*.docx'),('All files', '*.*'))
#         self.filename = fd.askopenfilename(
#             title='Open a file',
#             filetypes=filetypes)
#         self.filename=self.filename.replace("\\","")
#         self.filename=self.filename.replace("/","\\\\")
#         print(self.filename)

#         if len(self.filename)>0:
#             self.lbl_filename.config(text=self.filename)
#             if self.word is []:
#                 self.word_initialize()
#             self.grab_paragraphs()
#             self.lbl_filename.config(fg="green",bg="white")
#         else:
#             self.lbl_filename.config(fg="black",bg="red")
#         return self

#     def cut_paragraph(self,e):
#         if len(self.paragraphs)>0:
#             self.work()
#         else:
#             self.root.title("Application:First open a Word file.")
#             self.root.update()
#         return self
    
#     def work(self):
#         # baslik_index=random.randint(0,len(self.basliklar)-1)
#         word_count=len(self.sentence_rem.split())
#         kalan_metin = ''
        
#         metin=self.sentence_rem
#         kcrit=None
#         delta=0
#         for k in range(self.kstart,len(self.paragraphs),1):
#             paragraph=self.paragraphs[k]
            
#             if word_count+len(paragraph.split())>=self.word_limit:
#                 kcrit=k
#                 delta=0
#                 kelimeler=paragraph.split()
                
#                 while(not ((kelimeler[delta][-1]=='.') and word_count+delta>=self.word_limit)):
#                     delta=delta+1 
#                     if delta>=len(kelimeler):
#                         delta=len(kelimeler)-1
#                         break
#                 break
#             else:
#                 word_count=word_count+len(paragraph.split())

#         #print(Fore.BLUE + str(word_count+delta)+">=920 olmalı")
#         if kcrit is not None:
#             parsayisi=kcrit-self.kstart-1
#             dpar=math.floor(parsayisi/4)
#             # print(parsayisi)
#             # print(dpar)
#             for k in range(self.kstart,kcrit,1):
#                 paragraph=self.paragraphs[k]
#                 if k==self.kstart+1:
#                     metin=metin+"<h2><strong>"+self.marka+" "+self.basliklar[self.i32]["h2"]+"</strong></h2>&nbsp;"
#                     paragraph2=""
#                     vec=paragraph.split(".")
#                     ixx=len(vec)-2
#                     if ixx>len(vec)-1:
#                         ixx=len(vec)-1
#                     if ixx<0:
#                         ixx=0
                                                                                                                               

#                     for i in range(0,len(vec)):
#                         sentence=vec[i]
#                         if i==ixx:
#                             paragraph2=paragraph2+"&nbsp;<em>"+self.marka+" "+self.basliklar[self.i32]["h2"].lower()+"</em>&nbsp;"
#                         paragraph2=paragraph2+sentence+". "

#                     metin=metin+paragraph2+self.chr_esc+self.chr_esc
#                 elif k==self.kstart+dpar*2:
#                     # italic h31
#                     metin=metin+"<h3><strong>"+self.marka+" "+self.basliklar[self.i32]["h31"]+"</strong></h3>&nbsp;"
#                     paragraph2=""
#                     vec=paragraph.split(".")
#                     ixx=len(vec)-2
#                     if ixx>len(vec)-1:
#                         ixx=len(vec)-1
#                     if ixx<0:
#                         ixx=0

#                     for i in range(0,len(vec)):
#                         sentence=vec[i]

#                         if i==ixx:
#                             paragraph2=paragraph2+"&nbsp;<em>"+self.marka+" "+self.basliklar[self.i32]["h31"].lower()+"</em>&nbsp;"
#                         paragraph2=paragraph2+sentence+". "

#                     metin=metin+paragraph2+self.chr_esc+self.chr_esc
#                 elif k==self.kstart+dpar*3:
#                     metin=metin+"<h3><strong>"+self.marka+" "+self.basliklar32[self.i32]["h32"]+"</strong></h3>&nbsp;"
                    
#                     paragraph2=""
#                     vec=paragraph.split(".")
#                     ixx=len(vec)-2
#                     if ixx>len(vec)-1:
#                         ixx=len(vec)-1
#                     if ixx<0:
#                         ixx=0

#                     for i in range(0,len(vec)):
#                         sentence=vec[i]
#                         if i==ixx:
#                             paragraph2=paragraph2+"&nbsp;<em>"+self.marka+" "+self.basliklar32[self.i32]["h32"].lower()+"</em>&nbsp;"
#                         paragraph2=paragraph2+sentence+". "

                    
#                     metin=metin+paragraph2+self.chr_esc+self.chr_esc
#                 elif k==self.kstart+dpar*4:
#                     metin=metin+"<h4><strong>"+self.marka+" "+self.basliklar[self.i32]["h4"]+"</strong></h4>&nbsp;"
                                        
#                     paragraph2=""
#                     vec=paragraph.split(".")
#                     ixx=len(vec)-2
#                     if ixx>len(vec)-1:
#                         ixx=len(vec)-1
#                     if ixx<0:
#                         ixx=0

#                     for i in range(0,len(vec)):
#                         sentence=vec[i]
#                         if i==ixx:
#                             paragraph2=paragraph2+"&nbsp;<em>"+self.marka+" "+self.basliklar[self.i32]["h4"].lower()+"</em>&nbsp;"
#                         paragraph2=paragraph2+sentence+". "
                    
#                     self.i32=self.i32+1
#                     if self.i32==29:
#                         self.i32=0
#                     metin=metin+paragraph2+self.chr_esc+self.chr_esc
#                 else:
#                     metin=metin+paragraph+self.chr_esc+self.chr_esc
             
#             # önceki paragraf
#             paragraph=self.paragraphs[kcrit-1]
#             #print(Fore.BLUE + str(kcrit-1)+":")
#             #print(Fore.GREEN+paragraph+self.chr_esc)

#             # kritik paragraf
#             paragraph=self.paragraphs[kcrit]
#             kelimeler=paragraph.split()
#             metin = metin +' '.join(kelimeler[:delta+1])+self.chr_esc+self.chr_esc
#             kalan_metin = kalan_metin +' '.join(kelimeler[delta+1:])+self.chr_esc
#             self.sentence_rem=' '.join(kelimeler[delta+1:])+self.chr_esc
#             #print(Fore.BLUE + str(kcrit)+":")
#             #print(Fore.GREEN+' '.join(kelimeler[:delta+1])+self.chr_esc)
#             #print(Fore.RED+' '.join(kelimeler[delta+1:])+self.chr_esc)

#             # sonraki paragraf
#             self.kstart=kcrit+1 #python index kcrit+1
#             self.alert("Starting index "+str(self.kstart))
#             paragraph=self.paragraphs[kcrit+1]
#             #print(Fore.BLUE + str(kcrit+1)+":")
#             #print(Fore.RED+paragraph)
#             #print(Style.RESET_ALL)

#             for k in range(kcrit+1,len(self.paragraphs),1):
#                 paragraph=self.paragraphs[k]
#                 kalan_metin=kalan_metin+paragraph+self.chr_esc
                
#             #print(str(len(metin.split()))+" Kelime Kesildi")
#             #print(str(len(kalan_metin.split()))+" Kelime Kaldı")
#             # print(metin)   
#             self.lbl_par1.delete('1.0', END)                                                                           
#             self.lbl_par2.delete('1.0', END)

#             self.lbl_par1.insert('1.0',metin)                      
#             self.lbl_par2.insert('1.0',kalan_metin)
#             self.root.update()

#             self.lbl_total.config(text=str(len(metin.split()))+"/"+str(len(kalan_metin.split())))
#             pyperclip.copy(metin)
#             # self.doc.Content.Text = kalan_metin
#             # self.doc.Save()
#         else:
#             self.lbl_total.config(text="Anan!")
#             self.lbl_total.config(bg="red")
      
#         self.is_heading()
#         return self
    
#     def on_change(self,e):
#         if e.char.isnumeric():
#             self.word_limit=int(self.lbl_wordlen.get("1.0",END))
#             print(self.word_limit)
#         else:
#             pass
#         return self
    
#     def on_change_find(self,e):
#         self.str_find=self.lbl_find.get("1.0",END)
#         self.str_find=self.str_find.replace("\n","")
#         return self
    
#     def on_change_replace(self,e):
#         self.str_replace=self.lbl_replace.get("1.0",END)
#         self.str_replace=self.str_replace.replace("\n","")
#         return self

#     def on_btn_replace_click(self):
#         str_find=self.str_find
#         str_replace=self.str_replace
#         print(str_find+"->"+str_replace)
#         for i in range(0,len(self.paragraphs)):
#             self.paragraphs[i]=self.paragraphs[i].replace(str_find,str_replace)
#         return self
    
#     def is_heading(self,par):
#         vec=par.split(".")
#         lenn=len(vec)
#         return lenn==1

#     def __init__(self):
#         self.root = Tk()
#         self.root.title("Application")
#         self.root.geometry('800x600')

#         # Menu
#         menu_bar = Menu(self.root)
#         file_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="File",underline=0, menu=file_menu)
#         file_menu.add_command(label="Open", command=lambda: self.open_file([]),underline=1,accelerator="Ctrl+O")
#         file_menu.add_command(label="Cut", command=lambda: self.cut_paragraph([]),underline=1,accelerator="Ctrl+X")

#         self.root.config(menu=menu_bar)                                                                                                                                   
#         self.root.bind("<Control-o>",self.open_file)
#         self.root.bind("<Control-x>",self.cut_paragraph)

#         # GUI
#         self.root.columnconfigure(0,weight=1)
#         self.root.columnconfigure(1,weight=1)
#         self.root.columnconfigure(2,weight=1)

#         self.root.rowconfigure(0,weight=1)
#         self.root.rowconfigure(1,weight=1)
#         self.root.rowconfigure(2,weight=1)

#         self.lbl_par1 =Text(self.root, fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
#         self.lbl_par1.grid(row=0,columnspan=2,sticky="ew")

#         self.lbl_par2 =Text(self.root,  fg="black", bd=1, width=40,font="TkFixedFont") #,state="disabled"
#         self.lbl_par2.grid(row=1,columnspan=2,sticky="ew") 

#         lbl_filename_holder = Label(self.root, text = "File:",fg = "black",width=4,justify="left")
#         lbl_filename_holder.grid(column=0,row=3,sticky="w")
#         self.lbl_filename = Label(self.root, text = self.filename,justify="left")
#         self.lbl_filename.grid(column=1,row=3,sticky="w")
                                                      
#         lbl_wordlen_holder= Label(self.root, text = "Word limit:",fg = "black",width=10)
#         lbl_wordlen_holder.grid(column=2,row=3,sticky="e")
#         self.lbl_wordlen =Text(self.root,  fg="black", width=5,height=1)
#         self.lbl_wordlen.grid(column=3,row=3,sticky="e")         
#         self.lbl_wordlen.bind("<KeyRelease>", self.on_change)   
#         self.lbl_wordlen.insert('1.0',str(self.word_limit))                                            

#         self.lbl_total= Label(self.root, text = "./.",fg = "black",width=10)
#         self.lbl_total.grid(column=3,row=4,sticky="w")
#         self.lbl_total.config(bg="green",fg="white")


#         frame1=Frame(None,height=30)
#         # find
#         frame1.grid(column=0,row=4,sticky="we")
#         lbl_find_holder= Label(frame1, text = "Find:",fg = "black")
#         lbl_find_holder.grid(column=0,row=0,sticky="w")
#         self.lbl_find =Text(frame1,  fg="black", width=10,height=1)
#         self.lbl_find.grid(column=1,row=0,sticky="w")         
#         self.lbl_find.bind("<KeyRelease>", self.on_change_find)   
#         #replace                          
#         lbl_replace_holder= Label(frame1, text = "Replace:",fg = "black")
#         lbl_replace_holder.grid(column=3,row=0,sticky="e")
#         self.lbl_replace =Text(frame1,  fg="black", width=10,height=1)
#         self.lbl_replace.grid(column=4,row=0,sticky="e")         
#         self.lbl_replace.bind("<KeyRelease>", self.on_change_replace)   
#         #button
#         self.btn_replace=Button(frame1,text="Ok",command=self.on_btn_replace_click)
#         self.btn_replace.grid(row=0,column=5)


#         self.tree=ttk.Treeview(None, columns=("paragraph","word_count"), show='headings')
#         self.tree.heading('paragraph', text='Paragraph')
#         self.tree.column('paragraph', minwidth=0, width=120, stretch=NO)
#         self.tree.heading('word_count', text='Words')
#         self.tree.column('word_count', minwidth=0, width=80, stretch=NO)
#         self.tree.grid(row=0, column=2,rowspan=2,columnspan=2,sticky="nswe")

#         self.root.update()
#         self.word_initialize()
#         self.load_basliklar()

#         self.root.mainloop()

#     def load_basliklar(self):
#         with open("basliklar.json","r",encoding="utf8") as file:
#             self.basliklar=json.loads(''.join(file.readlines()))
#         with open("basliklar32.json","r",encoding="utf8") as file:
#             self.basliklar32=json.loads(''.join(file.readlines()))
#         return self
    

#     def __del__(self):
#         # self.word_deinit()
#         pass
    
# gui=GUI()

