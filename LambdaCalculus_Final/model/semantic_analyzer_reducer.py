import random
import string
from model.parser_p import Lambda, Var, App, Num

# Depth limit to avoid infinite recursion
DEPTH_LIMIT = 200

class Logger:
    def __init__(self):
        self.steps = []

    def log(self, message):
        self.steps.append(message)

    def get_steps(self):
        return self.steps

def fresh_var(used_vars):

    
    # Create a list of all lowercase letters
    available_vars = list(string.ascii_lowercase)
    
    # Iterate over each used variable
    for var in used_vars:
        
        # If the variable is in the list of available variables, remove it
        if var in available_vars:
            available_vars.remove(var)
    
    # Check if there are any available variables left
    if not available_vars:
        
        # If there are no available variables, raise an exception
        raise Exception("Ran out of fresh variables")
    
    # Select a random variable from the list of available variables and return it
    return random.choice(available_vars)

def alpha_convert(expr, old_var, new_var, logger):


    # Case when the expression is a variable
    if isinstance(expr, Var):
        # If the variable name matches old_var, create a new Var instance with new_var,
        # otherwise, keep the expression unchanged.
        result = Var(new_var) if expr.name == old_var else expr

    # Case when the expression is a lambda abstraction
    elif isinstance(expr, Lambda):
        # Recursively perform alpha conversion on the body of the lambda.
        # If the variable of the lambda matches old_var, replace it with new_var.
        # This ensures that we rename the bound variable and its occurrences in the body.
        new_body = alpha_convert(expr.body, old_var, new_var, logger)
        result = Lambda(new_var if expr.var == old_var else expr.var, new_body)

    # Case when the expression is a function application
    elif isinstance(expr, App):
        # Recursively perform alpha conversion on both the function part (func)
        # and the argument part (arg) of the application.
        result = App(alpha_convert(expr.func, old_var, new_var, logger), alpha_convert(expr.arg, old_var, new_var, logger))

    # If the expression is of another type, leave it unchanged
    else:
        result = expr

    # Log the details of the alpha conversion process
    logger.log(f"Alpha Conversion: {old_var} -> {new_var} in {expr} = {result}")

    return result

def substitute(body, var, value, logger):

    # If `body` is a number, it is immutable and does not participate in substitution
    if isinstance(body, Num):
        return body

    # If `body` is a variable, check if it matches `var` and replace it with `value`
    if isinstance(body, Var):
        result = value if body.name == var else body

    # If `body` is a lambda abstraction, check if the variable of the lambda matches `var`
    elif isinstance(body, Lambda):
        if body.var == var:
            result = body
        else:
            # Recursively perform substitution on the body of the lambda.
            # This ensures that we rename the bound variable and its occurrences in the body.
            result = Lambda(body.var, substitute(body.body, var, value, logger))

    # If `body` is a function application, recursively perform substitution on both the function part (func)
    # and the argument part (arg) of the application.
    elif isinstance(body, App):
        result = App(substitute(body.func, var, value, logger), substitute(body.arg, var, value, logger))

    # If `body` is of another type, leave it unchanged
    else:
        result = body

    # Log the details of the substitution process
    logger.log(f"Substitution: {var} -> {value} in {body} = {result}")

    return result

from functools import lru_cache

@lru_cache(maxsize=None)
def reduce_to_normal_form(expr, logger, depth=0):

    if depth > DEPTH_LIMIT:
        raise Exception("Exceeded depth limit during reduction")

    while True:
        # Log the current expression
        logger.log(f"Reducing: {expr}")

        if isinstance(expr, App):
            if isinstance(expr.func, Lambda):
                # If the function part of the application is a lambda, perform beta reduction.
                result = substitute(expr.func.body, expr.func.var, expr.arg, logger)
                logger.log(f"Beta Reduction: ({expr.func}) ({expr.arg}) -> {result}")
                expr = result
            else:
                # Otherwise, recursively reduce the function and argument parts of the application.
                # If the result expression is different, we have made a reduction, so create a new App
                # with the reduced arguments and log the reduction.
                reduced_func = reduce_to_normal_form(expr.func, logger, depth + 1)
                reduced_arg = reduce_to_normal_form(expr.arg, logger, depth + 1)
                if reduced_func != expr.func or reduced_arg != expr.arg:
                    result = App(reduced_func, reduced_arg)
                    logger.log(f"App Reduction: ({expr.func}) ({expr.arg}) -> ({reduced_func}) ({reduced_arg})")
                    expr = result
                else:
                    # Otherwise, we have reached a normal form or a leaf, so break out of the loop.
                    break
        elif isinstance(expr, Lambda):
            # Recursively reduce the body of the lambda. If the result is different, we have made a reduction,
            # so create a new Lambda with the same variable and the reduced body, and log the reduction.
            reduced_body = reduce_to_normal_form(expr.body, logger, depth + 1)
            if reduced_body != expr.body:
                result = Lambda(expr.var, reduced_body)
                logger.log(f"Lambda Reduction: (#{expr.var}.{expr.body}) -> (#{expr.var}.{reduced_body})")
                expr = result
            else:
                # Otherwise, we have reached a normal form or a leaf, so break out of the loop.
                break

def free_vars(expr):
 
    if isinstance(expr, Var):
        # If the expression is a variable, return a set containing the variable name.
        return {expr.name}
    elif isinstance(expr, Lambda):
        # If the expression is a lambda abstraction, recursively compute the set of
        # free variables in the body of the lambda, and subtract the bound variable
        # from the result. This ensures that the bound variable is not included in the
        # set of free variables.
        return free_vars(expr.body) - {expr.var}
    elif isinstance(expr, App):
        # If the expression is a function application, recursively compute the sets of
        # free variables in the function part (func) and the argument part (arg), and
        # take the union of the two sets. This ensures that all variables that are not
        # bound by a lambda abstraction are included in the set of free variables.
        return free_vars(expr.func) | free_vars(expr.arg)
    else:
        # If the expression is of another type, return an empty set.
        return set()

# Example
if __name__ == "__main__":
    from model.parser_p import Parser

    expr_string = "((((# f . (# g . (# x . (f x (g x))))) (# m . (# n . (n m)))) (# n . z)) p)"
    parser = Parser()
    parsed_expr = parser.parse(expr_string)
    print(f"Parsed expression: {parsed_expr}")

    logger = Logger()
    reduced_expr = reduce_to_normal_form(parsed_expr, logger)
    print(f"Reduced expression: {reduced_expr}")

    print("Reduction steps:")
    for step in logger.get_steps():
        print(step)
