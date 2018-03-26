import os, sys, inspect

# realpath() will make your script run, even if you symlink it :)

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
print('init: ' + cmd_folder)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)