import re
class InfixPostfixError(ValueError):
    pass
class InfixToPostfixConverter:
    OPERATORS = {
        '^': {'prec': 4, 'right_assoc': True},
        '*': {'prec': 3, 'right_assoc': False},
        '/': {'prec': 3, 'right_assoc': False},
        '%': {'prec': 3, 'right_assoc': False},
        '+': {'prec': 2, 'right_assoc': False},
        '-': {'prec': 2, 'right_assoc': False},
    }
    @classmethod
    def is_operator(cls, token: str) -> bool:
        return token in cls.OPERATORS
    @classmethod
    def is_operand(cls, token: str) -> bool:
        return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?", token))
    @classmethod
    def tokenize(cls, expression: str) -> list[str]:
        if not expression or not expression.strip():
            raise InfixPostfixError("Expression cannot be empty.")
        if len(expression) > 300:
            raise InfixPostfixError("Expression exceeds maximum allowed length of 300 characters.")
        token_pattern = re.compile(r"\d+(?:\.\d+)?|[a-zA-Z_][a-zA-Z0-9_]*|[-+*/%^()]|\S")
        tokens = token_pattern.findall(expression)
        for token in tokens:
            if not (cls.is_operator(token) or token in "()" or cls.is_operand(token)):
                raise InfixPostfixError(f"Invalid character or unrecognized symbol: '{token}'.")
        return tokens
    @classmethod
    def validate_syntax(cls, tokens: list[str]) -> None:
        if not tokens:
            raise InfixPostfixError("Expression contains no valid tokens.")
        if cls.is_operator(tokens[0]):
            raise InfixPostfixError(f"Expression cannot start with an operator: '{tokens[0]}'.")
        if cls.is_operator(tokens[-1]):
            raise InfixPostfixError(f"Expression cannot end with an operator: '{tokens[-1]}'.")
        paren_depth = 0
        prev_token = None
        for idx, token in enumerate(tokens):
            if token == '(':
                paren_depth += 1
                if prev_token is not None and (cls.is_operand(prev_token) or prev_token == ')'):
                    raise InfixPostfixError(
                        f"Missing operator between '{prev_token}' and opening parenthesis '(' at position {idx + 1}."
                    )
            elif token == ')':
                paren_depth -= 1
                if paren_depth < 0:
                    raise InfixPostfixError(f"Mismatched parentheses: unexpected closing ')' at position {idx + 1}.")
                if prev_token == '(':
                    raise InfixPostfixError(f"Empty parentheses '()' detected at position {idx}.")
                if prev_token is not None and cls.is_operator(prev_token):
                    raise InfixPostfixError(
                        f"Operator '{prev_token}' cannot immediately precede closing parenthesis ')'."
                    )
            elif cls.is_operator(token):
                if prev_token == '(':
                    raise InfixPostfixError(
                        f"Operator '{token}' cannot immediately follow an opening parenthesis '('."
                    )
                if prev_token is not None and cls.is_operator(prev_token):
                    raise InfixPostfixError(
                        f"Consecutive operators detected: '{prev_token}' followed by '{token}'."
                    )
            elif cls.is_operand(token):
                if prev_token == ')':
                    raise InfixPostfixError(
                        f"Missing operator between closing parenthesis ')' and operand '{token}'."
                    )
                if prev_token is not None and cls.is_operand(prev_token):
                    raise InfixPostfixError(
                        f"Missing operator between adjacent operands '{prev_token}' and '{token}'."
                    )
            prev_token = token
        if paren_depth > 0:
            raise InfixPostfixError(
                f"Mismatched parentheses: {paren_depth} unclosed opening parenthesis '(' detected."
            )
    @classmethod
    def convert_with_steps(cls, expression: str) -> tuple[str, list[dict]]:
        tokens = cls.tokenize(expression)
        cls.validate_syntax(tokens)
        stack: list[str] = []
        postfix: list[str] = []
        steps: list[dict] = []
        step_num = 1
        def record_step(sym: str, action: str):
            nonlocal step_num
            steps.append({
                'step': step_num,
                'symbol': sym,
                'action': action,
                'stack': ' '.join(stack) if stack else '(empty)',
                'output': ' '.join(postfix) if postfix else '(empty)'
            })
            step_num += 1
        for token in tokens:
            if cls.is_operand(token):
                postfix.append(token)
                record_step(token, f"Append operand '{token}' to output")
            elif token == '(':
                stack.append(token)
                record_step(token, "Push '(' onto stack")
            elif token == ')':
                while stack and stack[-1] != '(':
                    top_op = stack.pop()
                    postfix.append(top_op)
                    record_step(token, f"Pop '{top_op}' to output (matching ')')")
                if not stack:
                    raise InfixPostfixError("Mismatched parentheses during conversion.")
                stack.pop()
                record_step(token, "Discard matching '(' from stack")
            elif cls.is_operator(token):
                curr_prec = cls.OPERATORS[token]['prec']
                curr_right_assoc = cls.OPERATORS[token]['right_assoc']
                while stack and stack[-1] != '(':
                    top_op = stack[-1]
                    if not cls.is_operator(top_op):
                        break
                    top_prec = cls.OPERATORS[top_op]['prec']
                    if (not curr_right_assoc and top_prec >= curr_prec) or \
                       (curr_right_assoc and top_prec > curr_prec):
                        popped = stack.pop()
                        postfix.append(popped)
                        record_step(token, f"Pop '{popped}' due to precedence and push '{token}'")
                    else:
                        break
                stack.append(token)
                record_step(token, f"Push operator '{token}' onto stack")
        while stack:
            op = stack.pop()
            if op in "()":
                raise InfixPostfixError("Mismatched parentheses remaining in stack.")
            postfix.append(op)
            record_step('(end)', f"Pop remaining operator '{op}' to output")
        result_str = ' '.join(postfix)
        return result_str, steps
    @classmethod
    def convert(cls, expression: str) -> str:
        postfix_str, _ = cls.convert_with_steps(expression)
        return postfix_str
def interactive_demo():
    print("=" * 60)
    print("      INFIX TO POSTFIX CONVERTER (Interactive CLI)")
    print("=" * 60)
    print("Supports: +, -, *, /, %, ^, parentheses (), and variables/numbers.")
    print("Type 'examples' to see test cases, or 'exit' / 'quit' to quit.\n")
    examples = [
        "A + B * C",
        "(A + B) * C",
        "A + B * (C ^ D - E) ^ (F + G * H) - I",
        "((A + B) * C - (D - E)) ^ (F + G)",
        "(10 + 20) * 30 / 5",
        "A + * B",
        "(A + B",
        "A + B)",
        "A B + C"
    ]
    while True:
        try:
            user_input = input("\nEnter Infix Expression: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Exiting converter demo. Goodbye!")
            break
        if user_input.lower() == "examples":
            print("\n--- Preset Test Examples ---")
            for idx, ex in enumerate(examples, start=1):
                print(f"[{idx}] {ex}")
            continue
        try:
            postfix_result, steps = InfixToPostfixConverter.convert_with_steps(user_input)
            print("\n" + "-" * 75)
            print(f"Infix Input   : {user_input}")
            print(f"Postfix Result: {postfix_result}")
            print("-" * 75)
            view_steps = input("Show step-by-step conversion table? (y/n, default: y): ").strip().lower()
            if view_steps in ("", "y", "yes"):
                print("\n" + "=" * 75)
                print(f"{'Step':<5} | {'Symbol':<8} | {'Action':<32} | {'Stack':<12} | {'Output'}")
                print("-" * 75)
                for s in steps:
                    print(f"{s['step']:<5} | {s['symbol']:<8} | {s['action']:<32} | {s['stack']:<12} | {s['output']}")
                print("=" * 75)
        except InfixPostfixError as err:
            print("\n[SYNTAX ERROR]")
            print(f"-> {err}")
        except Exception as err:
            print(f"\n[UNEXPECTED ERROR]: {err}")
if __name__ == "__main__":
    interactive_demo()
