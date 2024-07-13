import requests
import tkinter as tk
from view.gui import LambdaCalcView
from model.lexer import lexer
from model.parser_p import parser, Lambda, Var, App, Num
from model.semantic_analyzer_reducer import alpha_convert, Logger, fresh_var, reduce_to_normal_form
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

class LambdaCalcController:
    def __init__(self, view):
        self.view = view
        self.view.set_eval_button_command(self.evaluate_expression)
        self.view.set_alpha_button_command(self.alpha_convert_expression)

    def evaluate_expression(self) -> None:
        """Evaluate lambda calculus expression."""
        print("Evaluating expression...")
        expression = self.view.get_expression()
        try:
            # Lexical analysis
            print("Lexical analysis...")
            lexer.input(expression)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            self.view.display_tokens(tokens)

            # Parsing
            print("Parsing...")
            ast = parser.parse(expression)
            self.view.display_ast(ast)
            print(f"Parsed AST: {ast}")  # Debugging statement

            # Evaluation with capturing output
            print("Evaluation with capturing output...")
            logger = Logger()
            result = reduce_to_normal_form(ast, logger)
            evaluation_steps = logger.get_steps()
            evaluation_steps.append(f"Result: {result}")
            self.view.display_evaluation(evaluation_steps)
            print(f"Evaluation result: {result}")  # Debugging statement

            # Get explanations from ChatGPT
            print("Getting explanations from ChatGPT...")
            explanations = self.get_chatgpt_explanations(evaluation_steps)
            if explanations:
                self.view.display_explanations(explanations)
                print(f"Explanations: {explanations}")  # Debugging statement

        except Exception as e:
            print(f"Error during evaluation: {e}")
            self.view.show_error(str(e))

    def alpha_convert_expression(self) -> None:
        """Perform alpha conversion on the lambda calculus expression."""
        print("Performing alpha conversion...")
        expression = self.view.get_expression()
        try:
            # Lexical analysis
            print("Lexical analysis...")
            lexer.input(expression)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            self.view.display_tokens(tokens)

            # Parsing
            print("Parsing...")
            ast = parser.parse(expression)
            self.view.display_ast(ast)
            print(f"Parsed AST: {ast}")  # Debugging statement

            # Alpha conversion
            print("Alpha conversion...")
            logger = Logger()
            if isinstance(ast, Lambda):
                used_vars = {v.name for v in free_vars(ast)}
                new_var = fresh_var(used_vars)
                converted_ast = alpha_convert(ast, ast.var, new_var, logger)
                logger.log(f"Alpha conversion result: {converted_ast}")
                self.view.display_ast(converted_ast)
            else:
                logger.log("Alpha conversion not applicable to this expression")
                self.view.show_error("Alpha conversion not applicable to this expression.")
            
            # Display conversion steps and result
            self.view.display_evaluation(logger.get_steps())

        except Exception as e:
            print(f"Error during alpha conversion: {e}")
            self.view.show_error(str(e))

    def get_chatgpt_explanations(self, evaluation_steps):
        """Get explanations from ChatGPT for the evaluation steps."""
        url = "https://chatgpt-api.p.rapidapi.com/explain"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        payload = {
            "steps": evaluation_steps
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.json().get("explanations", [])
        except requests.RequestException as e:
            print(f"HTTP request error: {e}")
            raise Exception("Failed to get explanations from ChatGPT") from e

def free_vars(expr):
    """Compute the set of free variables in the expression."""
    if isinstance(expr, Var):
        return {expr}
    elif isinstance(expr, Lambda):
        return free_vars(expr.body) - {expr.var}
    elif isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
    else:
        return set()

if __name__ == "__main__":
    root = tk.Tk()
    view = LambdaCalcView(root)
    controller = LambdaCalcController(view)
    root.mainloop()
