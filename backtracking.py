"""
A class that we introduced to store each backtracking branch's associated copy of the data (variables, domains, ...)
The data members are the variables of the KenKen board, the domains corresponding to each variable, each variables
neighbors and the functions that represent the present constraints
"""
class Backtrack:  # todo testing with Imre
    def __init__ (self, variables, domains, neighbors, constraints):
        """Construct a backtrack problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        # the remaining consisting values domains
        self.curr_domains = None
        # self.nassigns = 0

    """Number of conflicts board[var] has with other variables."""
    def number_of_conflicting_vars (self, var, val, board):
        return count(v in board and not self.constraints(var, val, v, board[v])
                     for v in self.neighbors[var])

    def init_curr_domains (self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    # Remove value from curr_domains[var] and add it to removals list
    def remove_from_curr_domain (self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    # Make the supposition that value is in curr_domains[var] and return the remaining possible values for other vars
    def suppose (self, var, value):
        self.init_curr_domains()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    # All values that are not excluded yet for var
    def possible_values (self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    # Restore the curr_domains of the variables in removals
    def restore (self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)


# __________ Optimizing algorithms ____________

# AC3

# Forward checking


# ________ Helper functions __________


# Count the number of items in sequence
def count (seq):
    return sum(bool(x) for x in seq)
