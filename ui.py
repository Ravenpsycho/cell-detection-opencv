import tkinter as tk
from tkinter import messagebox
from outlier_remover import OutlierRemover


def dir_btn_click():
    out_remover.set_dir()
    label_dir.config(text="Chosen dir:\n" + out_remover.get_dir())
    label_dir.config(fg='green')
    return None


def expr_btn_click():
    # getting the values minus the last character ('\n')
    val_dapi = text_input_expr1.get('1.0', 'end-1c')
    val_other = text_input_expr2.get('1.0', 'end-1c')

    # setting them in the OutlierRemover object
    try:
        out_remover.set_labels(val_dapi,
                               val_other)
        # filling the lists
        out_remover.find_matches()
        lists = out_remover.get_lists(True)
        dapi_pretty_print = '\n'.join(['DAPI Files:'] + lists[0])
        other_pretty_print = '\n'.join([f'{out_remover.get_expr()[1]} Files:'] + lists[1])
        label_list1.config(text=dapi_pretty_print)
        label_list2.config(text=other_pretty_print)

        text_input_expr1.config(fg='green')
        text_input_expr2.config(fg='green')
        btn_run.config(state=tk.NORMAL, text='RUN')

    except Exception as e:
        messagebox.showerror("error", str(e))

    return None


def btn_run_click():
    pass


out_remover = OutlierRemover()

root = tk.Tk()

# root design
frame_dir_selector = tk.Frame(root)
frame_dir_selector.pack()

frame_expression_selector = tk.Frame(root)
frame_expression_selector.pack()

frame_list_display = tk.Frame(root)
frame_list_display.pack()

# dir selection
label_dir = tk.Label(frame_dir_selector, height=2, width=60, text='Choose Directory',
                     bd=1, relief=tk.SOLID)
label_dir.pack(side=tk.LEFT, expand=True)

btn_dir = tk.Button(frame_dir_selector, height=2, width=12, text='Choose directory', command=dir_btn_click)
btn_dir.pack(side=tk.RIGHT)

# expressions selection
text_input_expr1 = tk.Text(frame_expression_selector, height=2, width=30)
text_input_expr1.pack(side=tk.LEFT)
text_input_expr2 = tk.Text(frame_expression_selector, height=2, width=30)
text_input_expr2.pack(side=tk.LEFT)
btn_expr = tk.Button(frame_expression_selector, height=2, width=12,
                     text='Validate Features', command=expr_btn_click)
btn_expr.pack(side=tk.RIGHT)
# display list
label_list1 = tk.Label(frame_list_display, width=30, text='',
                       bd=1, relief=tk.SOLID)
label_list1.pack(side=tk.LEFT, expand=True)

label_list2 = tk.Label(frame_list_display, width=30, text='',
                       bd=1, relief=tk.SOLID)
label_list2.pack(side=tk.LEFT, expand=True)

btn_run = tk.Button(frame_list_display, width=12, height=2, text='Not Ready',
                    command=btn_run_click, state=tk.DISABLED)
btn_run.pack(side=tk.LEFT)

if __name__ == '__main__':
    root.mainloop()
