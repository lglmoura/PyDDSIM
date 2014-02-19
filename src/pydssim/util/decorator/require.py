'''
Created on 22/08/2009

@author: LGustavo
'''

#from pydssim.util.interface import implements

def require(arg_name, *allowed_types):
    def make_wrapper(f):
        if hasattr(f, "wrapped_args"):
            wrapped_args = getattr(f, "wrapped_args")
        else:
            code = f.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount])

        try:
            arg_index = wrapped_args.index(arg_name)
        except ValueError:
            raise NameError, arg_name

        def wrapper(*args, **kwargs):
            if len(args) > arg_index:
                arg = args[arg_index]
                flag = True
                for intf in allowed_types:
                    if not hasattr(intf, "implements"):
                        flag = False
                        break
                if flag:
                    if not implements(arg, *allowed_types):
                        raise TypeError()
                else:                    
                    if not isinstance(arg, allowed_types):
                        type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                        raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))
            else:
                if arg_name in kwargs:
                    arg = kwargs[arg_name]
                    for intf in allowed_types:
                        if not hasattr(intf, "implements"):
                            flag = False
                            break
                    if flag:
                        if not implements(arg, *allowed_types):
                            raise TypeError()
                    else:
                        if not isinstance(arg, allowed_types):
                            type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                            raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))

            return f(*args, **kwargs)

        wrapper.wrapped_args = wrapped_args
        return wrapper

    return make_wrapper
