from tkinter import Tk
from view.gui import LambdaCalcView
from controller.controller import LambdaCalcController

def main():
    root = Tk()
    view = LambdaCalcView(root)
    controller = LambdaCalcController(view)
    root.mainloop()

if __name__ == "__main__":
    main()