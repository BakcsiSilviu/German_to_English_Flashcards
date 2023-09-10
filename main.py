from tkinter import *
import pandas
from random import choice
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
german_dictionary = {}

with open("ger_eng.csv", "r", encoding='utf-8') as ger_eng:
    read_file = pandas.read_csv(ger_eng)
    for index in range(0, len(read_file)):
        german_dictionary[read_file.German[index]]= read_file.English[index]

# Search for a random german word 
def random_word():
    canvas.itemconfig(word_label, text= choice(list(german_dictionary.keys())))

# Verify if you knew the german word in english
def button_pressed(button):
    if button == 'wrong':
        pass
    elif button == 'right':
        current_word = [i for i in german_dictionary if german_dictionary[i] == canvas.itemcget(word_label, "text")]
        german_dictionary.pop(current_word[0])
    canvas.itemconfig(card, image=front_image)
    canvas.itemconfig(language_label, text= "German")
    random_word()
    window.after(4000, flip_card)

# Flip the card
def flip_card():
    canvas.itemconfig(card, image=back_image)
    canvas.itemconfig(language_label, text= "English")
    canvas.itemconfig(word_label, text= german_dictionary[canvas.itemcget(word_label,'text')])

# Save progress function
def save_function():
    new_data = pandas.DataFrame(german_dictionary.items(), columns=['German', 'English'])
    new_data = new_data.explode('English')
    new_data.to_csv("ger_eng.csv", index=False)
    messagebox.showinfo(title='Save', message="Progress saved!")

# Generate window
window = Tk()
window.title("Germany to English")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Add canvas to window

canvas = Canvas(width=800, height=526, bg= BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file=".\images\card_front.png")
back_image = PhotoImage(file=".\images\card_back.png")

card = canvas.create_image(400, 263, image = front_image)
canvas.grid(column=1, row=0)

# Add 3 buttons, wrong, right and save progress

wrong_button_image = PhotoImage(file=".\images\wrong.png")
wrong = Button(image=wrong_button_image, command=lambda button="wrong": button_pressed(button), highlightthickness=0)
wrong.grid(column=0,row=1)

right_button_image = PhotoImage(file=".\\images\\right.png")
right = Button(image=right_button_image, command=lambda button="right": button_pressed(button), highlightthickness=0)
right.grid(column=2,row=1)

save_button_image = PhotoImage(file=".\\images\\save.png")
save = Button(image=save_button_image, command= save_function)
save.grid(column=1,row=1)

# Add the 2 labels with language and word

language_label = canvas.create_text(400, 150,text="German", font=("Ariel", 40, "italic"))

word_label = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

random_word()
window.after(4000, flip_card)

window.mainloop()