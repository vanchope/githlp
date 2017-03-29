from Tkinter import *
import subprocess

def prepare_cmd(s):
  return s.split(' ')

def prepare_str(s):
  return s[s.find(':') + 1:].strip()

def cmd_out_lines(cmd):
  return subprocess.check_output(prepare_cmd(cmd)).split('\n')  

def render():
  listbox.delete(0, END)  
  lines = cmd_out_lines('git status')
  to_commit = [x[1:].strip() for x in cmd_out_lines('git diff --name-status --cached') if len(x)>0]
  lines = [x for x in lines if len(x)>1 and x[0]=='\t']
  for line in lines:
    vis = line[1:].strip()  
    if prepare_str(vis) in to_commit:
      vis = '> ' + vis
    listbox.insert(END, vis)

def handler(event):
  selected = listbox.curselection()[0]
  selected_text = listbox.get(selected)  
  git_cmd = 'git {} {}'.format('reset' if selected_text[0] == '>' else 'add', prepare_str(selected_text))
  subprocess.check_output(prepare_cmd(git_cmd))
  render()  

master = Tk()
master.title(cmd_out_lines('pwd')[0])
master.geometry('640x480')
scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(master, yscrollcommand=scrollbar.set)
listbox.bind('<Double-Button-1>', handler)
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=listbox.yview)
render()
mainloop()
