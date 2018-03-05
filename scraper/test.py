import logging

def install():
    print ("In install")
    logging.basicConfig(filename='example.log', level=logging.DEBUG)  # will create a file to record all logging info
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')


methods = {'install': install}

method_name = 'install' # set by the command line options
if method_name in methods:
    methods[method_name]() # + argument list of course
else:
    raise Exception("Method %s not implemented" % method_name)