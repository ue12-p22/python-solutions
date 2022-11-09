
##################################################
# postfix_eval_typed
##################################################
def postfix_eval_typed(chaine, result_type):
    """
    a postfix evaluator, using a parametric type
    that can be either `int`, `float` or `Fraction` or similars
    """
    operators = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x//y if issubclass(result_type, int) else x/y,
    }

    stack = []
    for token in chaine.split():
        if token in operators:
            # compute operation on last 2 entries
            try:
                rhs = stack.pop()
                lhs = stack.pop()
            except:
                return "error-empty-stack"
            result = operators[token](lhs, rhs)
            stack.append(result)
        else:
            try:
                stack.append(result_type(token))
            except:
                return 'error-syntax'
            # parse as int and stack up
    if len(stack) != 1:
        return 'error-unfinished'
    return stack.pop()

