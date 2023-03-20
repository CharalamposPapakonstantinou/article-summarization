import gensim
import re
from gensim.summarization.summarizer import summarize
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *



def clean_data(data):
  text = re.sub(r"\[[0-9]*\]"," ",data)
  text = text.lower()
  text = re.sub(r'\s+'," ",text)
  text = re.sub(r","," ",text)
  return text

def fetch_text(ratio_val=0):
    ratio_val=scale.get()
    link = entry_url.get()
    if link!='':
        res = requests.get(link)
        soup = BeautifulSoup(res.text,'html.parser')
        title=soup.select('title')[0].get_text().strip()

        paragraphs=soup.select('p:not([class*="PromoHeadline"])')[:-1]
        extracted_rows_content = []
        for i in range(len(paragraphs)):
            row_text = paragraphs[i].getText().strip()
            extracted_rows_content.append(row_text)
        raw_data = " ".join(extracted_rows_content)

        cleaned_article_content = clean_data(raw_data)
        summary = summarize(cleaned_article_content, ratio = float(ratio_val))
        summary = re.sub('\[[^\]]*\]','',summary)
        summary = '. '.join(map(lambda s: s.strip().capitalize(), summary.split('.'))) # capitilize

        text.delete('1.0', END)
        text.insert(INSERT, title+'\n \n'+summary)


# Create the main window
root = tk.Tk()
root.title("Summarizing BBC News")
root.configure(bg='white')
root.geometry("850x550")


label_intro = tk.Label(root,text='Just paste the url below to summarize!', font="arial 22 ", justify="center", fg='black',bg='white')
label_intro.pack()

entry_url = tk.Entry(root,bg='white', width=50,font= "arial 18 ", justify = "center", fg = "black",relief="flat",highlightthickness=0)
entry_url.place(relx = 0.25, rely = 0.05, relwidth = 0.9, relheight = 0.1)
entry_url.focus_set()
entry_url.pack()

def on_entry_changed(event):
    # get the current contents of the entry widget
    text = event.widget.get()
    fetch_text(text)


entry_url.bind("<KeyRelease>", on_entry_changed)
entry_url.bind("<Key>", on_entry_changed)



ratio_val = DoubleVar()
scale = Scale(root,showvalue=1,from_=0.3, to=0.95,resolution=0.1,variable = ratio_val,command=fetch_text,orient=VERTICAL,length=300,bg='white' )
scale.set(0.5)
scale.pack(side=LEFT)



v=Scrollbar(root, orient='vertical')
v.pack(side=RIGHT, fill='y')
text=Text(root, font=("Arial, 14"), yscrollcommand=v.set)
v.config(command=text.yview)
text.pack()


root.mainloop()


