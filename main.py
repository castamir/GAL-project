from gui import *


def main():
    root = Tk()
    root.geometry("900x500+150+150")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()