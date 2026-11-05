from solver import solve_minterms
from truthtable import truthtable

# Remember to implement argument into function call
def main():
    expression = input("Enter an expression to simplify: ")
    print("Defaults to SOP")
    while (is_pos_or_sop := input("Do you want to display the final solution as a Sum of Products (SOP) or as a Product of Sums (POS)? ")) not in("POS", "SOP", ""):
        print("Pick a valid choice")
    if is_pos_or_sop == "POS":
        is_pos = True
    else:
        is_pos = False

    minterms, inputs = truthtable(expression, is_pos)

    solve = solve_minterms(minterms, inputs, is_pos)

    print("Simplified Expression:", solve)


if __name__ == "__main__":
    main()
