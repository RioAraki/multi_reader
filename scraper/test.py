def install():
    print ("In install")

methods = {'install': install}

method_name = 'install' # set by the command line options
if method_name in methods:
    methods[method_name]() # + argument list of course
else:
    raise Exception("Method %s not implemented" % method_name)