import sys
import shlex
import os
from constants import *
from builtin import *
#from cd import *

built_in_cmds = {}

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0

def tokenize(string):
	return shlex.split(string)

def execute(cmd_tokens):

	cmd_name = cmd_tokens[0]
	cmd_args = cmd_tokens[1:]

	if cmd_name in built_in_cmds:
		return built_in_cmds[cmd_name](cmd_args)

	#create a child shell process, if the current process is child, its pis set as 0
	#else if the current process is parent process, pid set as its child's pid
	pid = os.fork()

	if pid == 0:
		#execute child process
		os.execvp(cmd_tokens[0], cmd_tokens)
	elif pid > 0:
		#
		while True:
			#waiting for the status of its chile process
			wpid, status = os.waitpid(pid, 0)

			#child exist normally or stop the waiting status
			if os.WIFEXITED(status) or os.WIFIGNALED(status):
				break
	#os.execvp(cmd_tokens[0], cmd_tokens)

	return SHELL_STATUS_RUN

def shell_loop():
	status = SHELL_STATUS_RUN

	while status == SHELL_STATUS_RUN:
		#show the command line
		sys.stdout.write('>')
		sys.stdout.flush()

		#read the command line
		cmd = sys.stdin.readline()

		#slide the command
		cmd_tokens = tokenize(cmd)

		#execute the command and update the status
		status = execute(cmd_tokens)

def register_command(name, func):
	built_in_cmds[name] = func

def init():
	register_command("cd", cd)
	register_command("exit", exit)


def main():
	init()
	shell_loop()

if __name__ == "__main__":
	main()
