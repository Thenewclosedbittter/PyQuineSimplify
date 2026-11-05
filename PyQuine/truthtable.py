def truthtable(expression, is_pos):
    # Will return all letters in the expression (for our truth table to generate). This generates a list
    parse_letters = lambda: sorted(list(set(char for char in expression if char.isalpha())))
    inputs = parse_letters()
    expression_len = len(inputs)
    def clean_string(expr):
        # Create a dictionary that maps each of these to their 'and' or 'or', etc. equivalent
        # Cleans our expression so it is readable to our program 
        expr = expr.upper().replace(" ", "")
        for v in inputs:
            for ov in inputs:
                if v != ov:
                    expr = expr.replace(v + ov, f"{v} and {ov}")
        expr_clean = {
            "+" : " or ",
            "." : " and ", 
            "*" : " and ", 
            "()" : " and ",
        }

        for v in inputs:
            expr_clean[v + "'"] = f"(not {v})"
            expr_clean[f"{v}("] = f"{v} and ("
            expr_clean[f"){v}"] = f") and {v}"

        expr_clean[")("] = ") and ("
        for operator, replacement in expr_clean.items():
            expr = expr.replace(operator, replacement)

        return expr 
   
    clean_expr = clean_string(expression)
    # WE DON'T KNOW IF WE NEED TO USE MINTERMS OR MAX TERMS
    terms = []
    # Objective: generate a table that creates every possible output for each given input for each function
    def generatetable():
        total_rows = 1 << expression_len

        for row in range(total_rows):
            binary_str = f"{row:0{expression_len}b}"
            context = {}

            for index, var in enumerate(inputs):
                context[var] = int(binary_str[index])

            try:
                eval_result = bool(eval(clean_expr, {}, context))
                if eval_result == (not is_pos):
                    terms.append(binary_str)
            except Exception as e:
                print(f"Error evaluating at state {binary_str}: {e}")
                return []
        return terms

    return generatetable(), inputs
