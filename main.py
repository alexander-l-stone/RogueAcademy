import tdl

if __name__ == "__main__":
    tdl.set_font("arial12x12.png", greyscale=True, altLayout=True)
    console = tdl.Console(20, 10)
    main_window = tdl.init(20, 10, title="Rogue Academy", fullscreen=False)
    