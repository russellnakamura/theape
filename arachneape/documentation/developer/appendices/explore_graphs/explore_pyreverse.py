
# python standard library
import subprocess
import shlex

# third-party
from pylint.pyreverse.main import Run


class SampleCase(object):
    def __init__(self):
        return


args = shlex.split('-o png -p example explore_pyreverse.py')
#Run(args)


subprocess.call(['pyreverse'] + args)


import arachneape.infrastructure.hortator as hortator
file_name = hortator.__file__.rstrip('c')
command = 'pyreverse -o png -p hortator {0}'.format(file_name)
subprocess.call(shlex.split(command))


command = 'pyreverse -o png -ASmy -k {0} -p hortator'.format(file_name)
subprocess.call(shlex.split(command))


command = 'pyreverse -c TheHortator -mn -a1 -s1 -f ALL -o png {0}'.format(file_name)
subprocess.call(shlex.split(command))


try:
    print subprocess.check_output(shlex.split("dot '-T*'"), stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as error:
    output =  error.output
    o = output.replace('Format: "*" not recognized. Use one of: ', '')
    for item in o.split():
        print "   * {0}".format(item)
    
