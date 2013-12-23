from gui import *


def main():
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()