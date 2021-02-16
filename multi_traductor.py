#!/usr/bin/python3

import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import ttk
import tkinter.font as font

import requests


class LanguageTab(tk.Frame):
    def __init__(self, master, lang_name, lang_code):
        super().__init__(master)

        # fonts for all widgets
        self.option_add("*Font", ("courier",16, 'bold'))        
        # font to use for label widgets
        self.option_add("*Label.Font", ("arial",12))
        # font to use for label widgets
        self.option_add("*Button.Font", ("arial",14, 'bold'))
        self.option_add("*Tab.Font", ("arial",14, 'bold'))
        self.option_add("*Frame.Font", ("courier",14, 'bold'))
        self.lang_name = lang_name
        self.lang_code = lang_code
        self.translation_var = tk.StringVar(self)
        self.translation_var.set("")
        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard)
        #self.copy_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.translated_label = tk.Label(self, textvar=self.translation_var, bg="lightgrey", fg="black")        
        #self.translated_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def copy_to_clipboard(self):
        root = self.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(self.translation_var.get())
        msg.showinfo("Copied Successfully", "Text copied to clipboard")


class NewLanguageForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Add new Language")
        self.geometry("500x200")
        self.name_label = tk.Label(self, text="Language Name")
        self.name_entry = tk.Entry(self, bg="white", fg="black")
        self.code_label = tk.Label(self, text="Language Code")
        self.code_entry = tk.Entry(self, bg="white", fg="black")
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.name_label.pack(fill=tk.BOTH, expand=1)
        self.name_entry.pack(fill=tk.BOTH, expand=1)
        self.code_label.pack(fill=tk.BOTH, expand=1)
        self.code_entry.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.X)

    def submit(self):
        lang_name = self.name_entry.get()
        lang_code = self.code_entry.get()

        if lang_name and lang_code:
            new_tab = LanguageTab(self.master, lang_name, lang_code)
            self.master.languages_menu.add_command(label=lang_name, command=lambda: self.master.add_new_tab(new_tab))
            msg.showinfo("Language Option Added", "Language option " + lang_name + " added to menu")
            self.destroy()
        else:
            msg.showerror("Missing Information", "Please add both a name and code")


class TranslateBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Translation Book v3")
        self.geometry("1000x700")
   
        # fonts for all widgets
        self.option_add("*Font", ("courier",16, 'bold'))        
        # font to use for label widgets
        self.option_add("*Label.Font", ("arial",12))
        # font to use for label widgets
        self.option_add("*Button.Font", ("arial",14, 'bold'))
        self.option_add("*Tab.Font", ("arial",14, 'bold'))
        self.option_add("*Frame.Font", ("courier",14, 'bold'))

        self.notestyle = ttk.Style()
        self.notestyle.configure("TNotebook.Tab", borderwidth=2, font = ("times",18), padding=(15, 7))

        self.myFont2 = font.Font(size=16)
        self.menu = tk.Menu(self, bg="lightgrey", fg="black")
        self.languages_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.languages_menu.add_command(label="Add New", command=self.show_new_language_popup)
        self.languages_menu.add_command(label="Francés", command=lambda: self.add_new_tab(LanguageTab(self, "Francés", "fr")))
        self.languages_menu.add_command(label="Catalan", command=lambda: self.add_new_tab(LanguageTab(self, "Catalan", "ca")))
        self.languages_menu.add_command(label="Portugues", command=lambda: self.add_new_tab(LanguageTab(self, "Portugues", "pt")))
        self.languages_menu.add_command(label="Aleman", command=lambda: self.add_new_tab(LanguageTab(self, "Aleman", "de")))
        self.languages_menu['font'] = self.myFont2
        self.menu.add_cascade(label="Languages", menu=self.languages_menu)
        self.config(menu=self.menu)
        self.notebook = Notebook(self)
        self.language_tabs = []
        spanish_tab = tk.Frame(self.notebook)
        myFont = font.Font(family = 'courier', size=18, weight = 'bold')
        self.translate_button = tk.Button(spanish_tab, text="Translate", command=self.translate, height = 2) 
        self.translate_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.translate_button['font'] = myFont
        self.spanish_entry = tk.Text(spanish_tab, bg="white", fg="black")
        self.spanish_entry.pack(side=tk.TOP, expand=1)
        self.notebook.add(spanish_tab, text="Español")
        self.notebook.pack(fill=tk.BOTH, expand=1)

    def translate(self, text=None):
        if len(self.language_tabs) < 1:
            msg.showerror("No Languages", "No languages added. Please add some from the menu")
            return

        if not text:
            text = self.spanish_entry.get(1.0, tk.END).strip()

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}"

        try:
            for language in self.language_tabs:
                full_url = url.format("es", language.lang_code, text)
                r = requests.get(full_url)
                r.raise_for_status()
                translation = r.json()[0][0][0]
                language.translation_var.set(translation)
                msg.showinfo("translation", translation)
                #msg.showinfo("Translations Successful", "Text successfully translated")
        except Exception as e:
            msg.showerror("Translation Failed", str(e))
#        else:
#            msg.showinfo("Translations Successful", "Text successfully translated")

    def add_new_tab(self, tab):
        self.language_tabs.append(tab)
        self.notebook.add(tab, text=tab.lang_name)

        try:
            self.languages_menu.entryconfig(tab.lang_name, state="disabled")
        except:
            # language isn't in menu.
            pass

    def show_new_language_popup(self):
        NewLanguageForm(self)


if __name__ == "__main__":
    translatebook = TranslateBook()
    english_tab = LanguageTab(translatebook, "Inglés", "en")
    translatebook.add_new_tab(english_tab)

#    german_tab = LanguageTab(translatebook, "Alemán", "de")
#    translatebook.add_new_tab(german_tab)

    translatebook.mainloop()

# códigos de lenguages --> https://www.labnol.org/code/19899-google-translate-languages