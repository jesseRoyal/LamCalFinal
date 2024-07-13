import tkinter as tk
from tkinter import messagebox, scrolledtext

class LambdaCalcView:
    def __init__(self, root):
        self.root = root
        self.root.title("Lambda Calculus Interpreter")
        self.root.geometry("800x600")  # Default size
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        self.expr_label = tk.Label(input_frame, text="Lambda Expression:")
        self.expr_label.grid(row=0, column=0, padx=5, pady=5)

        self.expr_entry = tk.Entry(input_frame)
        self.expr_entry.grid(row=0, column=1, sticky="ew", padx=5)

        self.eval_button = tk.Button(input_frame, text="Evaluate")
        self.eval_button.grid(row=0, column=2, padx=5)

        self.alpha_button = tk.Button(input_frame, text="Alpha Convert")
        self.alpha_button.grid(row=0, column=3, padx=5)

        self.clear_button = tk.Button(input_frame, text="Clear", command=self.clear_all_fields)
        self.clear_button.grid(row=0, column=4, padx=5)

        # Output frame
        output_frame = tk.Frame(root)
        output_frame.grid(row=1, sticky="nsew")
        output_frame.grid_rowconfigure(5, weight=1)
        output_frame.grid_columnconfigure(1, weight=1)

        self.tokens_label = tk.Label(output_frame, text="Tokens:")
        self.tokens_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.tokens_text = scrolledtext.ScrolledText(output_frame, height=5)
        self.tokens_text.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)

        self.ast_label = tk.Label(output_frame, text="AST:")
        self.ast_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.ast_text = scrolledtext.ScrolledText(output_frame, height=5)
        self.ast_text.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5)

        self.evaluation_label = tk.Label(output_frame, text="Evaluation Steps:")
        self.evaluation_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.evaluation_text = scrolledtext.ScrolledText(output_frame, height=10)
        self.evaluation_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5)

        self.explanation_label = tk.Label(output_frame, text="Explanations:")
        self.explanation_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.explanation_text = scrolledtext.ScrolledText(output_frame, height=10)
        self.explanation_text.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5)

    def set_eval_button_command(self, command):
        """Set the command for the evaluate button."""
        self.eval_button.config(command=command)

    def set_alpha_button_command(self, command):
        """Set the command for the alpha convert button."""
        self.alpha_button.config(command=command)

    def get_expression(self) -> str:
        """Get the lambda expression from the input field."""
        return self.expr_entry.get()

    def display_tokens(self, tokens):
        """Display the tokens in the output area."""
        self.tokens_text.delete('1.0', tk.END)
        self.tokens_text.insert(tk.END, "\n".join(map(str, tokens)))

    def display_ast(self, ast):
        """Display the abstract syntax tree (AST) in the output area."""
        self.ast_text.delete('1.0', tk.END)
        self.ast_text.insert(tk.END, str(ast))

    def display_evaluation(self, evaluation_steps):
        """Display the evaluation steps in the output area."""
        self.evaluation_text.delete('1.0', tk.END)
        self.evaluation_text.insert(tk.END, "\n".join(evaluation_steps))

    def display_explanations(self, explanations):
        """Display the explanations from ChatGPT in the output area."""
        self.explanation_text.delete('1.0', tk.END)
        self.explanation_text.insert(tk.END, "\n".join(explanations))

    def show_error(self, message):
        """Show an error message in a messagebox."""
        messagebox.showerror("Error", message)

    def clear_all_fields(self):
        """Clear all input and output fields."""
        self.expr_entry.delete(0, tk.END)
        self.tokens_text.delete('1.0', tk.END)
        self.ast_text.delete('1.0', tk.END)
        self.evaluation_text.delete('1.0', tk.END)
        self.explanation_text.delete('1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    view = LambdaCalcView(root)
    root.mainloop()
