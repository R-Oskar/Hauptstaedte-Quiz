import tkinter as tk
import ttkbootstrap as ttk
import random
from laender import *

window = ttk.Window(themename="darkly")
window.title("Hauptstädte Quiz")
window.geometry("600x400")

current_question = ()
question_type = 0
right_guesses = []
wrong_guesses = []
last_guess = None
country_list = []
solution = None
index = 0

label_show_text = tk.StringVar()
entry_text = tk.StringVar()
score_label_text = tk.StringVar()
label_output_text = tk.StringVar()

nordamerika = tk.IntVar()
europa = tk.IntVar(value=1)
südamerika = tk.IntVar()
asien = tk.IntVar()
afrika = tk.IntVar()
ozeanien = tk.IntVar()

def main():
    create_widgets()

    update_country_list()
    ask_question()

    window.mainloop()

def create_widgets():
    label_show = ttk.Label(
        master=window, textvariable=label_show_text, font=("Helvetica", 14, "bold")
    )
    label_show.pack(pady=10)

    main_frame = tk.Frame(window)
    main_frame.pack()

    create_region_frame(main_frame, "Nordamerika", nordamerika, nordamerika_laender, 1, 0)
    create_region_frame(main_frame, "Europa", europa, europa_laender, 1, 1)
    create_region_frame(main_frame, "Südamerika", südamerika, suedamerika_laender, 2, 0)
    create_region_frame(main_frame, "Asien", asien, asien_laender, 2, 1)
    create_region_frame(main_frame, "Ozeanien", ozeanien, ozeanien_laender, 3, 0)
    create_region_frame(main_frame, "Afrika", afrika, afrika_laender, 3, 1)

    # Eingabefeld
    entry = ttk.Entry(master=window, textvariable=entry_text)
    entry.pack(pady=10)
    entry.bind("<Return>", lambda event: button_clicked())

    # Button Frame
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    # Buttons
    button_submit = ttk.Button(master=button_frame, text="Submit", command=button_clicked)
    button_submit.grid(row=0, column=1, padx=10)

    style = ttk.Style()
    style.configure("Custom.TButton", font=("Helvetica", 10))
    button_refresh = ttk.Button(master=button_frame, text="🔄", command=refresh, style = "Custom.TButton")
    button_refresh.grid(row=0, column=0, padx=10)


    # Punktestand
    score_label = ttk.Label(master=button_frame, textvariable=score_label_text)
    score_label.grid(row=0, column=2, padx=10)

    # Ausgabe
    label_output = ttk.Label(
        master=window, textvariable=label_output_text, justify="center", font=("Helvetica", 12)
    )
    label_output.pack(pady=10)

def create_region_frame(master, text, variable, laender_list, row, column):
    frame = tk.Frame(master=master)
    frame.grid(row=row, column=column, sticky="w")
    check_button = tk.Checkbutton(frame, variable=variable, command=update_country_list)
    check_button.pack(side="left")
    label = tk.Label(frame, text=f"{text} ({len(laender_list)})")
    label.pack(side="left")

def update_country_list():
    global country_list
    country_list = []

    if nordamerika.get():
        country_list.extend(nordamerika_laender)
    if europa.get():
        country_list.extend(europa_laender)
    if südamerika.get():
        country_list.extend(suedamerika_laender)
    if asien.get():
        country_list.extend(asien_laender)
    if afrika.get():
        country_list.extend(afrika_laender)
    if ozeanien.get():
        country_list.extend(ozeanien_laender)

    if not country_list:
        label_output_text.set("Du musst mindestens eine Region auswählen!")
        europa.set(1)
        update_country_list()

    update_score_label_text()

def ask_question():
    global current_question, question_type, right_guesses, solution, wrong_guesses

    print(right_guesses)

    # Flattened list of all country-capital pairs
    flattened_list = [element for sublist in country_list for element in sublist]

    # List of unanswered questions, which are those that are not in `right_guesses`
    unanswered = [item for item in flattened_list if item not in right_guesses]

    if not unanswered:
        label_output_text.set("Du hast alle Fragen korrekt beantwortet!")
        right_guesses = []
        wrong_guesses = []
        update_country_list()
        ask_question()
        return

    current_question = random.choice(unanswered)
    
    # Find the index of the country-capital pair containing `current_question`
    index = next((i for i, sublist in enumerate(country_list) if current_question in sublist), None)
    
    if index is not None:
        question_type = 0 if country_list[index][0] == current_question else 1

        if question_type == 0:
            label_show_text.set(f"Was ist die Hauptstadt von {country_list[index][0]}?")
            solution = country_list[index][1]
        else:
            label_show_text.set(f"Von welchem Land ist {current_question} die Hauptstadt?")
            solution = country_list[index][0]

def button_clicked():
    global right_guesses, wrong_guesses, solution, current_question, index, question_type
    guess = entry_text.get().strip()

    if guess.lower().casefold() == solution.lower().casefold():
        label_output_text.set("Das ist richtig!")
        right_guesses.append(solution)
    else:
        label_output_text.set(
            f"Falsch! Die Lösung ist {solution}/{current_question}."
        )
        wrong_guesses.append(solution)

    update_score_label_text()
    ask_question()
    entry_text.set("")



def update_score_label_text():
    all_answers = set(item for tupel in country_list for item in tupel)
    correct_count = len(set(right_guesses) & all_answers)
    score_label_text.set(
        f"Richtig: {correct_count}/{len(country_list) * 2}\nFalsch: {len(wrong_guesses)}"
    )

def refresh():
    global right_guesses, wrong_guesses
    right_guesses = []
    wrong_guesses = []
    update_country_list()
    label_output_text.set("")
    ask_question()

def check_button_clicked():
    update_country_list()

    if not country_list:
        label_output_text.set("Du musst mindestens eine Region auswählen!")
        europa.set(1)
        
    if current_question in country_list:
        update_score_label_text()
    else:
        ask_question()


if __name__ == "__main__":
    main()
