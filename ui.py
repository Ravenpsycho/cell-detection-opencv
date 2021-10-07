import tkinter as tk
from outlier_remover import OutlierRemover


def dir_btn_click():
    out_remover.set_dir()
    label_dir.config(text="Chosen dir:\n" + out_remover.get_dir())
    return None


def expr_btn_click():
    val_dapi = text_input_expr1.get('1.0', tk.END)
    val_other = text_input_expr2.get('1.0', tk.END)
    out_remover.set_labels(val_dapi,
                           val_other)
    print(val_dapi, val_other)
    return None


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
label_list1 = tk.Label(frame_list_display, height=20, width=36, text='',
                       bd=1, relief=tk.SOLID)
label_list1.pack(side=tk.LEFT, expand=True)

label_list2 = tk.Label(frame_list_display, height=20, width=36, text='',
                       bd=1, relief=tk.SOLID)
label_list2.pack(side=tk.RIGHT, expand=True)


if __name__ == '__main__':
    root.mainloop()
