"""
Assignment starter: backtracking CSP solver for map colouring.

Read ../guide.md and ../worked_example.md BEFORE you start coding here.

The required functions are implemented below. Do not change their signatures
(the tests in test_csp_map_coloring.py rely on them).

The problem: colour a map of Australia's 7 regions so that no two adjacent
regions share a colour, using only 3 colours.
"""

VARIABLES = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]

# Adjacency list: which regions border which. T (Tasmania) is an island --
# it has no neighbours, so it's unconstrained.
NEIGHBOURS = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "Q"],
    "SA":  ["WA", "NT", "Q", "NSW", "V"],
    "Q":   ["NT", "SA", "NSW"],
    "NSW": ["SA", "Q", "V"],
    "V":   ["SA", "NSW"],
    "T":   [],
}

DOMAIN = ["Red", "Green", "Blue"]


def is_consistent(assignment, var, value):
    """Return True if assigning `value` to `var` does not conflict
    with any already-assigned neighbour of `var`.

    `assignment` is a dict {variable: value} of variables assigned so far.
    Use NEIGHBOURS[var] to find which variables to check against.
    """
    return all(
        neighbour not in assignment or assignment[neighbour] != value
        for neighbour in NEIGHBOURS[var]
    )


def select_unassigned_variable(assignment):
    """Return the first variable from VARIABLES that is not assigned.

    Return None if all variables are assigned.

    A simple valid strategy: return the first unassigned variable in
    VARIABLES order. (Bonus/optional: implement the MRV heuristic instead
    -- see ../guide.md section 3.)
    """
    return next((var for var in VARIABLES if var not in assignment), None)


def backtracking_search(variables, domain):
    """Return a complete, consistent assignment using backtracking.

    Return a dict {variable: value}, or None if no solution exists.

    Follow the pseudocode in ../guide.md section 2:
      1. If the assignment is complete, return it.
      2. Otherwise pick an unassigned variable (select_unassigned_variable).
      3. Try each value in `domain` for that variable, in order.
      4. If is_consistent(), tentatively assign it and recurse.
      5. If the recursive call succeeds, return its result.
      6. If it fails, undo the assignment (backtrack) and try the next
         value.
      7. If no value works, return None (failure) so the caller backtracks
         further.

    Tip: write a helper function backtrack(assignment) and call it with
    an empty dict to start.
    """
    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment.copy()

        var = next(var for var in variables if var not in assignment)
        for value in domain:
            if is_consistent(assignment, var, value):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    return backtrack({})


if __name__ == "__main__":
    solution = backtracking_search(VARIABLES, DOMAIN)
    if solution:
        print("Solution found:")
        for region in VARIABLES:
            print(f"  {region}: {solution[region]}")
    else:
        print("No solution exists with this domain.")
