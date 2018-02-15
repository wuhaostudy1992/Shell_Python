import os
import sys
sys.path.append("..")
from constants import *

def cd(args):
	if len(args) > 0:
		try:
			os.chdir(args[0])
		except:
			print("Cannot open the direction")
	else:
		os.chdir(os.getenv('HOME'))

	return SHELL_STATUS_RUN


