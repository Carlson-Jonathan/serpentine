import cx_Freeze

executables = [cx_Freeze.Executable("Serpentine.py")]

cx_Freeze.setup(
    name="Serpentine",
    options={"build_exe":{"packages":["pygame"],"include_files":["Apple.png","flower.png","grass.png","snake.gif",
    "SnakeHead.png","WaterTile.png","WaterTile2.png","Snake_icon.ico",
    "splash.wav","splat.wav","bite.wav","music.mp3"]}},
    
    description = "Serpentine",
    executables = executables
    )
    
'''
to build a distribution package, go to your command prompt or Powershell or whatever compiler you are using...
    enter the script path (eg:  C:\Python27\JonPython\Notes\Scripts\Serpentine> )
    then enter >> python setup.py build    or
    python setup.py bdist_msi   <-- to create an installer package for your program
'''