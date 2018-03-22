'''   SPEAKERBOX SYNTHETIC VOICES
      --------------------------
    | Basic voice synthesis using NSSpeechSynthesiser in a Tkinter GUI
'''

from  AppKit import NSSpeechSynthesizer
from Tkinter import *

# inits
text = ''
entry_str = ''
entry_length = 0
default_voice = 'com.apple.speech.synthesis.voice.Alex'

def say(text, voice_id=default_voice):
   '''
   |  Read text in user-selected voice, or use default voice if no voice argument is passed in.
   |  It is possible to enter a voice name anywhere in the text entry window using the format: <VoiceName>
   '''
   text_temp = text
   ve = NSSpeechSynthesizer.alloc().init()
   ve.setVoice_(voice_id)
   if ('<' in text and '>' in text
       and text.index('<') < text.index('>')
       and text[text.index('<')+1:text.index('>')] in voices):
      ve.setVoice_(voices[text[text.index('<')+1:text.index('>')]])
      text_temp = text[0:text.index('<')] + text[text.index('>')+1:]
   ve.startSpeakingString_(text_temp)
   return

def voice_menu():
   '''
   |  Generate TopLevel window and populate with voice-name buttons.
   |  Any mouse click on a button will read text with that voice.
   '''
   select = Toplevel()
   select.title('Voices')
   select.geometry('375x400+800+200')
   select.resizable(0,0)
   select.config(background=bg)
   xpos = 5
   ypos = 5
   for item in sorted(voices):
      widget = Button(select, font=ButtonFont1, fg=fg, name=item.lower(), text=item, background=bg)
      widget.place(x=xpos, y=ypos, width=120, height=45)
      xpos += 122
      if xpos == 371:
         xpos = 5
         ypos += 47
   def mouse_select(event):
      widget = str(event.widget)[12:]
      if widget in voices_list and entry_str:
         voice_key = widget.title()
         if voice_key == 'Goodnews': voice_key = 'GoodNews'
         elif voice_key == 'Badnews': voice_key = 'BadNews'
         voice_sel = voices[voice_key]
         say(entry_str, voice_sel)
   select.bind('<Button-1>', mouse_select)
   select.bind('<Double-Button-1>', mouse_select)
   root.wait_window(select)
   return
   
def read_keys(event):
   '''
   | Interpret and display keystrokes.
   '''
   global entry_str, entry_length
   k = event.keysym
   if k == 'Tab': say(entry_str)
   no_keys = ('BackSpace', 'Return', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R',
               'Super_L', 'Meta_L', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Tab', 'Clear',
               'Pause', 'Scroll_Lock', 'Escape', 'Home', 'Up', 'Down', 'Left', 'Right',
               'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
               'F12', 'space', 'less', 'greater')
   if k not in no_keys and entry_length < 500:
      entry_str += event.char
      entry_length += 1
   if k == 'less' and '<' not in entry_str and entry_length < 500:
      entry_str += '<'
   if k == 'greater' and '>' not in entry_str and entry_length < 500:
      entry_str += '>'
   if k == 'space' and entry_str[-1:] != ' ' and entry_length < 500:  
      entry_str += event.char                              
      entry_length += 1
   if k == 'BackSpace' and len(entry_str) > 0:
      entry_str = entry_str[:-1]
      entry_length = 0
      for x in range (0, len(entry_str)):
         if entry_str[x:x+1] == '\n':
            entry_length += (70-(entry_length%70))
         else:
            entry_length +=1
   if k == 'Return' and entry_length < 500:
      if entry_str[-1:] == ' ':
         entry_str = entry_str[:-1]
      entry_str = entry_str + '\n'
      entry_length += (70-(entry_length%70))
   screen_Live.config(text = (entry_str + '_'))
   return

# voice names
voices = {}
for voice in NSSpeechSynthesizer.availableVoices():
	voices.update({str(voice[33:]):str(voice)})
voices_list = []
for item in voices.keys():
   voices_list.append(item.lower())

#fonts & colours
TextFont1 = ('Menlo', 17)
ButtonFont1 = ('Helvetica Neue', 18)
CounterFont = ('Helvetica Neue', 14, 'bold')
Statusfont = ('Helvetica Neue', 14)
LogoFont = ('Menlo', 24, 'bold', 'italic')
bg = 'gainsboro'
fg = 'black'

#window
root = Tk()
root.title('speakerbox')
root.geometry('770x300+250+250')
root.resizable(0,0)
root.config(background=bg)

#text-entry frame & logo
screen_Frame=Frame(root, bg=fg)
screen_Frame.place(x=10, y=10, width=750, height=200)
screen_Live = Label(root, bg=fg, fg=bg, wraplength=725, justify=LEFT)
screen_Live.config(font=TextFont1, text='_')
screen_Live.place(x=25, y=20)
Logo = Label(text='speakerbox', font=LogoFont, bg=bg, fg='darkgrey')
Logo.place(x=10, y=250)

# text entry bind
screen_Live.focus_force()
screen_Live.bind('<Key>', read_keys)

voice_menu()
root.mainloop()

