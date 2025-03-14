import importlib.metadata, subprocess, sys, matplotlib
matplotlib.use('WXAgg',warn=False, force=True)
from matplotlib import pyplot as plt

required  = {'networkx', 'matplotlib'} # This code is from the Stack Overflow page https://stackoverflow.com/questions/46419607/how-to-automatically-install-required-packages-from-a-python-script-as-necessary contributed by Serge Stroobandt and edited by Wrenchpilot
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])