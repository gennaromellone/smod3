from System.Core.Colors import bcolors


def Banner(version, modulesNum):

	print(' _______ ')
	print('< '+bcolors.OKGREEN+'SMOD-' + bcolors.BOLD +'3'+bcolors.ENDC+' >')
	print(' ------- ')
	print('        \   ^__^')
	print('         \  (xx)\_______')
	print('            (__)\\       )\\/\\')
	print('             U  ||----w |' )
	print('                ||     ||')
	print(' '*10 + '--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + bcolors.BOLD + 'MODBUS' + bcolors.ENDC +' Penetration Test FrameWork')
	print(' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + bcolors.BOLD + bcolors.OKGREEN + 'Python 3 Edition' + bcolors.ENDC + bcolors.ENDC)
	print(' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'Version : ' + bcolors.OKGREEN + bcolors.BOLD + version + bcolors.ENDC + bcolors.ENDC)
	print(' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'Modules : ' + bcolors.OKGREEN + bcolors.BOLD + str(modulesNum) + bcolors.ENDC + bcolors.ENDC)
	print(' '*7 + '--+--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'Coders   : ' + bcolors.OKGREEN + bcolors.BOLD + 'Gennaro Mellone, Farzin Enddo' + bcolors.ENDC + bcolors.ENDC)
	print(' '*10 + '--=' + bcolors.OKBLUE + '[' + bcolors.ENDC + 'github  : ' + bcolors.OKGREEN + bcolors.BOLD + 'www.github.com/gennaromellone, www.github.com/enddo' + bcolors.ENDC + bcolors.ENDC)
	print(' ')