from solver import solve_minterms
from truthtable import truthtable


def main():
    expression = input("Enter an expression to simplify: ")
    minterms, inputs = truthtable(expression)

    solve = solve_minterms(minterms, inputs)

    print("Simplified Expression:", solve)


if __name__ == "__main__":
    main()
