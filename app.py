import tkinter
import winsound

color_bg = "#0D0D14"
color_white = "#FFFFFF"
color_purple = "#7C3AED"
color_blue = "#3B82F6"
color_purple_hover = "#9D5CF6"
color_blue_hover = "#60A5FA"
color_dark = "#1A1A2E"
color_dark_hover = "#252540"
color_gray = "#2A2A3E"
color_gray_hover = "#353550"
color_accent = "#A78BFA"

button_values = [
    ["AC", "+/-", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="]
]

operators = ["/", "*", "-", "+"]
top_buttons = ["AC", "+/-", "%"]
history = []

window = tkinter.Tk()
window.title("Calc")
window.resizable(False, False)
window.configure(bg=color_bg)

main_frame = tkinter.Frame(window, bg=color_bg)
main_frame.pack(padx=12, pady=12)

# =====================
# HISTORICO
# =====================
history_frame = tkinter.Frame(main_frame, bg=color_bg, width=160)
history_frame.grid(row=0, column=1, rowspan=20, sticky="ns", padx=(10, 0))
history_frame.grid_propagate(False)

history_title = tkinter.Label(
    history_frame,
    text="Histórico",
    font=("Helvetica Neue", 11, "bold"),
    bg=color_bg,
    fg=color_accent,
    pady=8
)
history_title.pack()

history_listbox = tkinter.Listbox(
    history_frame,
    bg=color_bg,          # ✅ mesma cor do fundo
    fg="#8888AA",
    font=("Helvetica Neue", 10),
    selectbackground=color_purple,
    selectforeground=color_white,
    borderwidth=0,
    highlightthickness=0,
    width=18,
    height=20
)
history_listbox.pack(fill="both", expand=True, padx=6, pady=4)

clear_hist_btn = tkinter.Button(
    history_frame,
    text="Limpar",
    font=("Helvetica Neue", 9),
    bg=color_gray,
    fg=color_accent,
    relief="flat",
    cursor="hand2",
    borderwidth=0,
    command=lambda: (history.clear(), history_listbox.delete(0, tkinter.END))
)
clear_hist_btn.pack(pady=6)

# =====================
# CALCULADORA
# =====================
calc_frame = tkinter.Frame(main_frame, bg=color_bg)
calc_frame.grid(row=0, column=0)

# =====================
# DISPLAY
# =====================
display_frame = tkinter.Frame(
    calc_frame, bg=color_bg, pady=6)  # ✅ mesma cor do fundo
display_frame.grid(row=0, column=0, columnspan=4, sticky="we", pady=(0, 8))

label = tkinter.Label(
    display_frame,
    text="0",
    font=("Helvetica Neue", 42, "normal"),
    background=color_bg,   # ✅ mesma cor do fundo
    foreground=color_white,
    width=9,
    anchor="e",
    padx=14,
    pady=8
)
label.pack()

expression_label = tkinter.Label(
    display_frame,
    text="",
    font=("Helvetica Neue", 11),
    background=color_bg,   # ✅ mesma cor do fundo
    foreground="#555577",
    width=9,
    anchor="e",
    padx=14
)
expression_label.pack()

expression = ""


def play_click():
    """som de tecla suave — frequencia baixa e duracao curtissima"""
    try:
        winsound.Beep(300, 20)  # ✅ frequencia 300hz, 20ms (bem suave)
    except:
        pass


def add_to_history(expr, result):
    entry = f"{expr} = {result}"
    history.append(entry)
    history_listbox.insert(0, entry)


def button_click(value):
    global expression
    current = label.cget("text")
    play_click()

    if value == "AC":
        label.config(text="0")
        expression = ""
        expression_label.config(text="")
    elif value == "=":
        try:
            result = eval(expression if expression else current)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            add_to_history(expression, result)
            expression_label.config(text=expression)
            expression = str(result)
            label.config(text=str(result))
        except:
            label.config(text="Erro")
            expression = ""
    elif value == "+/-":
        try:
            number = float(current)
            result = int(-number) if float(-number).is_integer() else -number
            label.config(text=str(result))
            expression = str(result)
        except:
            label.config(text="Erro")
    elif value == "%":
        try:
            number = float(current)
            result = number / 100
            if result.is_integer():
                result = int(result)
            label.config(text=str(result))
            expression = str(result)
        except:
            label.config(text="Erro")
    else:
        if current == "0" and value not in ["+", "-", "*", "/"]:
            expression = value
        else:
            expression += value
        label.config(text=expression)


def get_colors(text):
    if text == "=":
        return color_purple, color_purple_hover, color_white
    elif text in operators:
        return color_blue, color_blue_hover, color_white
    elif text in top_buttons:
        return color_gray, color_gray_hover, color_accent
    else:
        return color_dark, color_dark_hover, color_white


def make_rounded_button(parent, text, bg, hover, fg, cmd, wide=False):
    """cria botao arredondado com canvas"""
    w = 130 if wide else 62  # ✅ tamanho fixo e uniforme
    h = 62
    r = 20  # ✅ raio uniforme para todos os botoes

    canvas = tkinter.Canvas(parent, width=w, height=h,
                            bg=color_bg, highlightthickness=0, cursor="hand2")

    def draw(color):
        canvas.delete("all")
        x1, y1, x2, y2 = 2, 2, w-2, h-2
        # ✅ desenho mais limpo com create_rounded usando arcos
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90,
                          extent=90, fill=color, outline=color)
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0,
                          extent=90, fill=color, outline=color)
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180,
                          extent=90, fill=color, outline=color)
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270,
                          extent=90, fill=color, outline=color)
        canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline=color)
        canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline=color)
        tx = w // 2
        canvas.create_text(tx, h//2, text=text,
                           font=("Helvetica Neue", 20), fill=fg)

    draw(bg)

    canvas.bind("<Enter>", lambda e: draw(hover))
    canvas.bind("<Leave>", lambda e: draw(bg))
    canvas.bind(
        "<Button-1>", lambda e: [draw(hover), window.after(80, lambda: draw(bg)), cmd()])

    return canvas


# =====================
# CRIACAO DOS BOTOES
# =====================
for row in range(len(button_values)):
    for column in range(len(button_values[row])):
        text = button_values[row][column]
        bg, hover, fg = get_colors(text)

        if text == "0":
            btn = make_rounded_button(calc_frame, text, bg, hover, fg,
                                      cmd=lambda: button_click("0"), wide=True)
            btn.grid(row=row+1, column=0, columnspan=2, padx=4, pady=4)
        elif text == ".":
            btn = make_rounded_button(calc_frame, text, bg, hover, fg,
                                      cmd=lambda: button_click("."))
            btn.grid(row=row+1, column=2, padx=4, pady=4)
        elif text == "=":
            btn = make_rounded_button(calc_frame, text, bg, hover, fg,
                                      cmd=lambda: button_click("="))
            btn.grid(row=row+1, column=3, padx=4, pady=4)
        else:
            btn = make_rounded_button(calc_frame, text, bg, hover, fg,
                                      cmd=lambda v=text: button_click(v))
            btn.grid(row=row+1, column=column, padx=4, pady=4)

window.mainloop()
