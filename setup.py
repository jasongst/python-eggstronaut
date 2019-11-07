from cx_Freeze import setup, Executable

setup(
    name= "EggStronaute",
    version="1.0.2",
    executables=[Executable("game.py")]
)