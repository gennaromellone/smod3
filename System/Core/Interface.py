from System.Core.Global import *
sys.path.append(mainPath + '/System/')
import readline
import re
from System.Core.Loader import plugins as pg
from System.Core.Colors import bcolors
from System.Core.Banner import Banner
from System.Lib import prettytable


class Command:
	COMMANDS 	= ['back', 'exit', 'exploit', 'help', 'modules', 'options', 'set', 'use']
	helpCommand 	= [
		['back', 'Move back from the current context'],
		['exit', 'Exit the console'],
		['exploit', 'Run module'],
		['help', 'Help menu'],
		['modules', 'Displays modules of a given type, or all modules'],
		['options', 'Displays all options of a given module'],
		['set', 'Sets a variable to a value'],
		['use', 'Selects a module by name']
	]

	def help(self, args,pointer = None):
		table = prettytable.PrettyTable([bcolors.BOLD + 'Command' + bcolors.ENDC,bcolors.BOLD + 'Description' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*7,'-'*11])
		for i in self.helpCommand:
			table.add_row([bcolors.OKBLUE + i[0] + bcolors.ENDC,i[1]])

		print(table)
	def exit(self,args,pointer = None):
		sys.exit(0)

	def back(self,args,pointer = None):
		global POINTER
		POINTER = None

	def options(self, args, pointer=None):
		if len(args) > 0:
			if pointer:
				table = prettytable.PrettyTable([bcolors.BOLD + 'Name' + bcolors.ENDC,bcolors.BOLD + 'Current Setting' + bcolors.ENDC,bcolors.BOLD + 'Required' + bcolors.ENDC,bcolors.BOLD + 'Description' + bcolors.ENDC])
				table.border = False
				table.align = 'l'
				table.add_row(['-'*4,'-'*15,'-'*8,'-'*11])
				for i in sorted(modules[pointer].options):
					table.add_row([bcolors.OKBLUE +  i + bcolors.ENDC,modules[pointer].options[i][0],modules[pointer].options[i][1],modules[pointer].options[i][2]])
				print(table)
			else:
				print(bcolors.FAIL + '[-] Before using "options" command you need to use a module.' + bcolors.ENDC)


	def modules(self, args):
		if len(args) > 0:
			table = prettytable.PrettyTable(
				[bcolors.BOLD + 'Modules' + bcolors.ENDC, bcolors.BOLD + 'Description' + bcolors.ENDC])
			table.border = False
			table.align = 'l'
			table.add_row(['-' * 7, '-' * 11])
			for i in sorted(modules):
				table.add_row([bcolors.OKBLUE + i + bcolors.ENDC, modules[i].info['Description']])

			print(table)

	def use(self, args, pointer=None):
		global POINTER
		POINTER = args[1]
		moduleName = args[1].split('/')
		if len(moduleName) != 3:
			print(bcolors.FAIL + '[-] ' + bcolors.BOLD + str(args[1]) +bcolors.ENDC + bcolors.FAIL + ' module not found !' + bcolors.ENDC)
			Command.show(self, ['','modules'])
		else:
			comp = Completer()
			readline.set_completer_delims(' \t\n;')
			readline.parse_and_bind("tab: complete")
			readline.set_completer(comp.complete)
			while True:
				inp = input('SMOD-3 ' + moduleName[0] + '(' + bcolors.OKBLUE + moduleName[-1] + bcolors.ENDC + ') >').strip().split()
				result 	= getattr(globals()['Command'](), inp[0])(inp, args[1])

				if POINTER == None:
					break

	def set(self,args,pointer = None):
		if pointer:
			modules[pointer].options[args[1]][0] = args[2]

	def exploit(self, args, pointer=None):
		if pointer:
			flag = True
			for i in modules[pointer].options:
				if modules[pointer].options[i][1] and modules[pointer].options[i][0] == '':
					print(bcolors.FAIL + '[-]' + bcolors.ENDC + ' set ' + i)
					flag = False
			if flag:
				modules[pointer].exploit()


class Completer(object):
	RE_SPACE = re.compile('.*\s+$', re.M)

	def _listdir(self, root):
		res = []
		for name in os.listdir(root):
			path = os.path.join(root, name)
			if os.path.isdir(path):
				name += os.sep
				res.append(name[:-1])
			else:
				if name.endswith('.py'):
					res.append(name[:-3])
		return res

	def _complete_path(self, path):
		dirname, rest = os.path.split(path)
		tmp = dirname if dirname else '.'
		res = [os.path.join(dirname, p) for p in self._listdir(tmp) if p.startswith(rest)]

		if len(res) > 1 or not os.path.exists(path):
				return res

		if os.path.isdir(path):
				return [os.path.join(path, p) for p in self._listdir(path)]

		return [path + ' ']

	def complete_use(self, args):
		if not args:
			return self._complete_path(modulesPath)

		result = self._complete_path(modulesPath + args[-1])
		for i in range(len(result)):
			result[i] = result[i].replace(modulesPath,'')
		return result

	def complete_show(self, args):
		if args[0] == '':
			return ['modules','options']
		if 'modules'.find(args[0]) == 0:
			return ['modules']
		elif 'options'.find(args[0]) == 0:
			return ['options']

	def complete_set(self, args):
		if POINTER:
			result 	= list()
			for i in modules[POINTER].options:
				if i.find(args[0]) == 0:
					result.append(i)
			return result

	def complete(self, text, state):
		buffer = readline.get_line_buffer()
		line = readline.get_line_buffer().split()

		if self.RE_SPACE.match(buffer):
			line.append('')

		cmd = line[0].strip()
		if cmd in Command.COMMANDS:
			impl = getattr(self, 'complete_%s' % cmd)
			args = line[1:]
			if args:
				return (impl(args) + [None])[state]
			return [cmd + ' '][state]

		results = [c + ' ' for c in Command.COMMANDS if c.startswith(cmd)] + [None]
		return results[state]

def init():
	global pluginNumber
	global modules
	plugins = pg(modulesPath)
	plugins.crawler()
	plugins.load()
	pluginNumber = len(plugins.pluginTree)
	modules = plugins.modules
	Banner(VERSION, pluginNumber)

def mainLoop():
	comp = Completer()
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(comp.complete)
	while True:
		inp = input('SMOD-3 >').strip().split()
		if len(inp) > 0:
			if inp[0] in Command.COMMANDS:
				result = getattr(globals()['Command'](), inp[0])(inp)
			else:
				print(bcolors.FAIL + '[-] ' + bcolors.BOLD + str(inp[0]) + bcolors.ENDC + bcolors.FAIL + ' command not found! (use "help" to show all commands)' + bcolors.ENDC)