from truthtable import truthtable

# We need to convert the minterms into binary for our algorithm works 
def convert_minterms(minterms, var_count):
    minterms = list(minterms)
    if not minterms: return []
    # Gets the variable with the largest binary number to get correct padding for each variable 
    var_count = max(minterms).bit_length()
    binary_minterms = [f"{m:0{var_count}b}" for m in minterms]
    return binary_minterms

def binary_to_lttrs(binary_terms, inputs):
    final_terms = []
    for term in binary_terms:
        string_build = ""
        for idx, char in enumerate(term):
            if char == "1":
                string_build += inputs[idx]
            elif char == "0":
                string_build += inputs[idx] + "'"
            else:
                continue 

        if string_build == "":
            string_build = "1"
        final_terms.append(string_build)

    return " + ".join(final_terms)


# Both of these functions are part of our algorithm
# This will compare two terms and drop whatever terms are changing 
def compare_terms(str1, str2):
    '''Will be used by our main function to combine grouped terms'''
    diff_count = 0 
    merged = [] # This is what is left from compare_terms
    for x, y in zip(str1, str2):
        if x != y: 
            diff_count += 1
            merged.append("-") # Dash goes where they don't match 
        else:
            merged.append(x) # a character is kept where they do match 
    
    if diff_count == 1:
        # Combines what we merged
        return "".join(merged)
    
    return None

def combine_generation(groups, var_count):
    # Creates empty boxes for next round of combinations
    next_gen = {i: [] for i in range(var_count + 1)}
    combined_terms = set()

    for i in range(var_count):
        group1 = groups.get(i, [])
        group2 = groups.get(i + 1, [])

        # The first combined loop perhpas 
        for term1 in group1:
            for term2 in group2:
                result = compare_terms(term1, term2)
                if result is not None:
                    combined_terms.add(term1)
                    combined_terms.add(term2)
                    if result not in next_gen[result.count('1')]:
                        next_gen[result.count('1')].append(result)                  
    return next_gen, combined_terms

def solve_minterms(minterms, inputs):
    # Get length of any of the variables
    var_count = len(inputs)
    binary_terms = convert_minterms(minterms, var_count)


    # Create groups now 
    groups = {i: [] for i in range(var_count + 1)}


    # Loop through each string and dump it into a bucket 
    for b_term in binary_terms:
        ones_count = b_term.count('1')
        groups[ones_count].append(b_term)
    current_groups = groups
    prime_implicits = set()
    while True: 
        all_current = [term for g in current_groups.values() for term in g]

        next_gen, combined_terms = combine_generation(current_groups, var_count)

        for term in all_current:
            if term not in combined_terms:
                prime_implicits.add(term)

        if all(len(terms) == 0 for terms in next_gen.values()):
            break 

        current_groups = next_gen
    final_reduction = []
    uncovered = set(binary_terms)
    while uncovered:
        best = max(prime_implicits, key=lambda pi: sum(1 for m in uncovered if all(p == '-' or p == c for p, c in zip(pi, m))))
        final_reduction.append(best)
        uncovered = {m for m in uncovered if not all(p == '-' or p == c for p, c in zip(best, m))}

    readable_solution = binary_to_lttrs(final_reduction, inputs)

    return readable_solution
