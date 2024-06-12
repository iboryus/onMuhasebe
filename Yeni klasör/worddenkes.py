import pyperclip
import re
import win32com.client
from colorama import Fore, Back, Style, init
from docx import Document

chr_esc="\n"

def word2string(dosya):
    init()
    word=win32com.client.Dispatch("Word.Application")
    word.visible=False
    word.DisplayAlerts=False
    wb=word.Documents.Open(dosya)
    doc=word.ActiveDocument

    len_par=len(doc.Paragraphs)
    print("Paragraf sayısı:"+str(len_par))
    
    word_count=0
    kalan_metin = ''
    metin=''
    kcrit=-1
    delta=0
    for k in range(1,len_par,1):
        paragraph=doc.Paragraphs(k)
        
        if word_count+len(paragraph.Range.Text.split())>=920:
            kcrit=k
            delta=0
            kelimeler=paragraph.Range.Text.split()
            
            while(not ((kelimeler[delta][-1]=='.') and word_count+delta>=920)):
                delta=delta+1 
                if delta>=len(kelimeler):
                    delta=len(kelimeler)-1
                    break
            break
        else:
            word_count=word_count+len(paragraph.Range.Text.split())

    print(Fore.BLUE + str(word_count+delta)+">=920 olmalı")
    print(Fore.BLUE + str(kcrit)+". paragraf")
    print(Style.RESET_ALL)
    
    for k in range(1,kcrit,1):
        paragraph=doc.Paragraphs(k)
        metin=metin+paragraph.Range.Text+chr_esc+chr_esc

    # önceki paragraf
    paragraph=doc.Paragraphs(kcrit-1)
    print(Fore.BLUE + str(kcrit-1)+":")
    print(Fore.GREEN+paragraph.Range.Text+chr_esc)

    # kritik paragraf
    paragraph=doc.Paragraphs(kcrit)
    kelimeler=paragraph.Range.Text.split()
    metin = metin +' '.join(kelimeler[:delta+1])+chr_esc
    kalan_metin = kalan_metin +' '.join(kelimeler[delta+1:])+chr_esc+chr_esc
    print(Fore.BLUE + str(kcrit)+":")
    print(Fore.GREEN+' '.join(kelimeler[:delta+1])+chr_esc)
    print(Fore.RED+' '.join(kelimeler[delta+1:])+chr_esc)

    # sonraki paragraf
    paragraph=doc.Paragraphs(kcrit+1)
    print(Fore.BLUE + str(kcrit+1)+":")
    print(Fore.RED+paragraph.Range.Text)
    print(Style.RESET_ALL)

    for k in range(kcrit+1,len_par,1):
        paragraph=doc.Paragraphs(k)
        kalan_metin=kalan_metin+paragraph.Range.Text+chr_esc
        
    print(str(len(metin.split()))+" Kelime Kesildi")
    print(str(len(kalan_metin.split()))+" Kelime Kaldı")
    
    pyperclip.copy(metin)
    doc.Content.Text = kalan_metin
    doc.Save()
    doc.Close(False)
    word.Quit()
    
    
word2string("C:/Dev/belge.docx")



# def kopyala_ve_devam_et(dosya_adi):
#     with open(dosya_adi, 'r', encoding='UTF-8') as dosya:
#         tam_metin = dosya.read()

#         # Kelimeleri ayır
#         kelimeler = tam_metin.split()

#         # İlk 920 kelimeyi al
#         kisilmis_metin = ' '.join(kelimeler[:920])

#         # Son cümlenin sonuna kadar al
#         son_cumle = ' '.join(re.split(r'(?<=\.)\s', kisilmis_metin)[-1:])
        
#         # Kırpılmış metni ve son cümleyi panoya kopyala
#         pyperclip.copy(kisilmis_metin + son_cumle)

# dosya_adi = "C:/Dev/belge.docx"  # Dosya adını değiştirin
# kopyala_ve_devam_et(dosya_adi)