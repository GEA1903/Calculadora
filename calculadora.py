import tkinter as tk
from PIL import Image, ImageTk

def evaluate():
    global expression
    try:
        if mode.get() == "Decimal":
            result = str(eval(expression))
        else: # Binário
            if any(c not in '01+-*/()' for c in expression):
                label_text.set("Erro Binário")
                expression_var.set("")
                return

            parsed = ""
            current = ""
            for ch in expression:
                if ch in "01":
                    current += ch
                else:
                    if current:
                        parsed += str(int(current, 2))
                        current = ""
                    parsed += ch
            if current:
                parsed += str(int(current, 2))

            result_decimal = eval(parsed)
            result = bin(int(result_decimal))[2:]

        label_text.set(result)
        expression_var.set(result)
        adjust_display_font_for_overflow() # Ajusta a fonte APENAS se houver estouro
    except Exception as e:
        print(f"Erro na avaliação: {e}")
        label_text.set("Erro")
        expression_var.set("")


def calculate(char):
    expr = expression_var.get()

    if mode.get() == "Binário":
        if char not in ('0', '1', 'C', 'B', '=', '+', '-', '*', '/', '( )', 'x²', '±'):
            return

    if char == 'C':
        expression_var.set("")
        label_text.set("")
    elif char == 'B':
        expression_var.set(expr[:-1])
        label_text.set(expression_var.get())
    elif char == 'x²':
        try:
            if mode.get() == "Binário":
                num = int(expr, 2)
                result = bin(num ** 2)[2:]
            else: # Decimal
                result = str(eval(expr + '**2'))
            expression_var.set(result)
            label_text.set(result)
            adjust_display_font_for_overflow() # Ajusta a fonte
        except:
            label_text.set("Erro")
            expression_var.set("")
    elif char == '( )':
        if expr and expr[-1] in '0123456789':
            expression_var.set(expr + '*()')
        else:
            expression_var.set(expr + '()')
        label_text.set(expression_var.get())
        adjust_display_font_for_overflow() # Ajusta a fonte
    elif char == '±':
        try:
            if expr.startswith('-'):
                expression_var.set(expr[1:])
            else:
                expression_var.set('-' + expr)
            label_text.set(expression_var.get())
            adjust_display_font_for_overflow() # Ajusta a fonte
        except:
            label_text.set("Erro")
            expression_var.set("")
    elif char == '.':
        if mode.get() == "Decimal":
            expression_var.set(expr + '.')
            label_text.set(expression_var.get())
            adjust_display_font_for_overflow() # Ajusta a fonte
    else:
        expression_var.set(expr + str(char))
        label_text.set(expression_var.get())
        adjust_display_font_for_overflow() # Ajusta a fonte


def update_expression(*args):
    global expression
    expression = expression_var.get()


def on_enter(event):
    mode_button.config(bg="lightblue")


def on_leave(event):
    mode_button.config(bg="green")


def switch_mode(*args):
    current_text = expression_var.get()

    try:
        if current_text != '':
            if mode.get() == "Binário":
                if all(c in '01' for c in current_text):
                    converted = current_text
                elif all(c.isdigit() or c in '+-*/().' for c in current_text):
                    converted = bin(int(eval(current_text)))[2:]
                else:
                    converted = ""
                    label_text.set("Conteúdo Inválido")
            else:
                if all(c in '01' for c in current_text):
                    converted = str(int(current_text, 2))
                elif any(c not in '01' for c in current_text) and current_text:
                    converted = current_text
                else:
                    converted = ""

            expression_var.set(converted)
            label_text.set(converted)
        else:
            expression_var.set("")
            label_text.set("")
    except Exception as e:
        print(f"Erro ao trocar modo: {e}")
        expression_var.set("")
        label_text.set("Erro")

    render_buttons()
    adjust_display_font_for_overflow() # Ajusta a fonte ao trocar o modo

def render_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()

    current_mode = mode.get()

    if current_mode == "Decimal":
        number_buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 0)
        ]
        special_buttons_decimal = [
            ('.', 3, 1),
            ('( )', 3, 2),
            ('x²', 3, 3),
            ('C', 0, 3),
            ('B', 1, 3),
            ('±', 2, 3)
        ]
        operator_buttons = [
            ('+', 4, 0), ('-', 4, 1), ('*', 4, 2), ('/', 4, 3)
        ]
        equal_button_pos = (5, 0, 1, 4)
    else: # Binário
        number_buttons = [
            ('1', 0, 0), ('0', 0, 1)
        ]
        special_buttons_binary = [
            ('( )', 0, 2),
            ('x²', 0, 3),
            ('C', 1, 0),
            ('B', 1, 1),
            ('±', 1, 2)
        ]
        operator_buttons = [
            ('+', 2, 0), ('-', 2, 1), ('*', 2, 2), ('/', 2, 3)
        ]
        equal_button_pos = (3, 0, 1, 4)

    # Renderiza botões numéricos/binários
    for text, r, c in number_buttons:
        btn = tk.Button(button_frame, text=text, command=lambda x=text: calculate(x), font=('Arial', 20))
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    # Renderiza botões especiais
    buttons_to_render = []
    if current_mode == "Decimal":
        buttons_to_render.extend(special_buttons_decimal)
    else:
        buttons_to_render.extend(special_buttons_binary)

    for text, r, c in buttons_to_render:
        cmd = evaluate if text == '=' else lambda x=text: calculate(x)
        btn = tk.Button(button_frame, text=text, command=cmd, font=('Arial', 20), fg='blue')
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    # Renderiza botões de operador
    for text, r, c in operator_buttons:
        cmd = evaluate if text == '=' else lambda x=text: calculate(x)
        btn = tk.Button(button_frame, text=text, command=cmd, font=('Arial', 20), fg='red')
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    # Renderiza o botão de igual
    eq_text, eq_r, eq_c, eq_colspan = '=', equal_button_pos[0], equal_button_pos[1], equal_button_pos[3]
    btn_equal = tk.Button(button_frame, text=eq_text, command=evaluate, font=('Arial', 20), bg='orange', fg='white')
    btn_equal.grid(row=eq_r, column=eq_c, columnspan=eq_colspan, sticky="nsew", padx=2, pady=2)

    # Configura o redimensionamento das colunas do button_frame
    if current_mode == "Decimal":
        total_cols = 4
        total_rows = 6
    else:
        total_cols = 4
        total_rows = 4

    for r in range(total_rows):
        button_frame.rowconfigure(r, weight=1)
    for c in range(total_cols):
        button_frame.columnconfigure(c, weight=1)

def adjust_display_font_for_overflow():
    DEFAULT_FONT_SIZE = 39
    MIN_FONT_SIZE = 15

    current_text = label_text.get()

    if not current_text:
        label.config(font=('Arial', DEFAULT_FONT_SIZE))
        return

    label.update_idletasks()
    label_width_pixels = label.winfo_width()
    if label_width_pixels <= 1:
        root.after(100, adjust_display_font_for_overflow)
        return

    current_font_size = DEFAULT_FONT_SIZE
    label.config(font=('Arial', current_font_size))
    label.update_idletasks()
    text_width_pixels = label.winfo_reqwidth()

    while text_width_pixels > label_width_pixels and current_font_size > MIN_FONT_SIZE:
        current_font_size -= 1
        label.config(font=('Arial', current_font_size))
        label.update_idletasks()
        text_width_pixels = label.winfo_reqwidth()

    while text_width_pixels < label_width_pixels * 0.9 and current_font_size < DEFAULT_FONT_SIZE:
        current_font_size += 1
        label.config(font=('Arial', current_font_size))
        label.update_idletasks()
        text_width_pixels = label.winfo_reqwidth()
        if text_width_pixels > label_width_pixels:
            current_font_size -= 1
            label.config(font=('Arial', current_font_size))
            break


# ==== Interface ====
root = tk.Tk()
root.title("Calculadora Responsiva")

# Definir o tamanho mínimo da janela para controlar que ela não se expanda/contraia além do esperado
# Você pode ajustar esses valores para o tamanho que achar ideal para sua calculadora
root.minsize(width=400, height=600)
# Se você quiser que a janela tenha um tamanho fixo e não possa ser redimensionada pelo usuário:
# root.resizable(False, False)


# --- Inserindo a Logo ---
try:
    icon_image = Image.open("calculator_logo.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
except Exception as e:
    print(f"Erro ao carregar o ícone: {e}")

expression_var = tk.StringVar()
expression_var.trace_add("write", update_expression)
label_text = tk.StringVar()
expression = ""

mode = tk.StringVar(value="Decimal")
mode.trace_add("write", switch_mode)

# Display
label = tk.Label(root, textvariable=label_text, font=('Arial', 39),
                 bg='white', anchor='e', relief='sunken', bd=5, padx=10, pady=20)
label.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Menu de modo
mode_button = tk.Menubutton(root, textvariable=mode, font=('Arial', 18, 'bold'),
                            bg='green', relief="raised", direction="below", padx=10, pady=5)
menu = tk.Menu(mode_button, tearoff=0)
mode_button.config(menu=menu)
menu.add_radiobutton(label="Decimal", variable=mode, value="Decimal")
menu.add_radiobutton(label="Binário", variable=mode, value="Binário")
mode_button.grid(row=1, column=0, columnspan=4, sticky="nsew")

mode_button.bind("<Enter>", on_enter)
mode_button.bind("<Leave>", on_leave)

# Área dos botões
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

# Redimensionamento
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=6)

for j in range(4):
    root.columnconfigure(j, weight=1)

# Inicializar botões corretos e ajustar fonte
render_buttons()
root.after(100, adjust_display_font_for_overflow)

root.mainloop()