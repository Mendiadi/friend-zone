
from explore import run_app

def main():
    print("client start.")
    run_app()
    print("client quit.")

#
# if __name__ == '__main__':
#     main()

import tkinter as tk
import tkinter.ttk as ttk
from ctypes import windll

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

# def set_appwindow(root):
#     windll.user32
#     hwnd = windll.user32.GetParent(root.winfo_id())
#     style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
#     style = style & ~WS_EX_TOOLWINDOW
#     style = style | WS_EX_APPWINDOW
#     res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
#     # re-assert the new window style
#     root.withdraw()
#     root.after(10, root.deiconify)
#
# def main():
#     root = tk.Tk()
#     root.wm_title("AppWindow Test")
#     button = ttk.Button(root, text='Exit', command=root.destroy)
#     button.place(x=10, y=10)
#     root.overrideredirect(True)
#     root.after(10, set_appwindow, root)
#     root.mainloop()

if __name__ == '__main__':
    main()