from math import log, exp, sin, cos
SMALL_DENOM = 10**-10
EVAL_KEY = "eval"
NUM_ARGS_KEY = "args"

OPERATORS = {
    "+": {
        EVAL_KEY: lambda x, y: x + y,
        NUM_ARGS_KEY: 2
    }, 
    "-": {
        EVAL_KEY: lambda x, y: x - y, 
        NUM_ARGS_KEY: 2
    }, 
    
    "*": {
        EVAL_KEY: lambda x, y: x * y, 
        NUM_ARGS_KEY: 2
    } 
}
'''
    "/": {
        EVAL_KEY: lambda x, y: (x / SMALL_DENOM) if (abs(y) < SMALL_DENOM) else x / y,
        NUM_ARGS_KEY: 2
    }, 
    "log": {
        EVAL_KEY: lambda x: (1 / -SMALL_DENOM) if (x < 1) else log(x),   
        NUM_ARGS_KEY: 1
    },

    "exp": {
        EVAL_KEY: lambda x:  exp(300) if (x >= 300) else exp(x),
        NUM_ARGS_KEY: 1
    },


    "u_":{
        EVAL_KEY: lambda x: x if x > 0 else 0,
        NUM_ARGS_KEY: 1
    }


'''



''' "sin": {
        EVAL_KEY: lambda x: sin(x),
        NUM_ARGS_KEY: 1
    },
'''