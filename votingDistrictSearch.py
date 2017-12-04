import csv
import collections,util

"""
class redistrictingProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        return 0

def isEnd(self, state):
    return state == len(self.query)
    
    def succAndCost(self, state):
        results = []
        for i in range(state + 1, len(self.query) + 1):
            successor = self.query[state:i]
            transitionCost = self.unigramCost(successor)
            results.append((successor, i, transitionCost))
        return results
"""

def redistricting_csp(precincts,n, sumTarget, sumRange):
    minSum = sumTarget - sumRange
    maxSum = sumTarget + sumRange
    variables = []
    csp = util.CSP()
    for precinct in precincts.keys():
        numVoters = precincts.get(precinct)[0] #adapt
        neighbors #to do: get neighbors
        domain = [(i,numVoters,neighbors) for i in range(1,n+2)]
        variables.append((precinct))
        csp.add_variable((precinct),domain)
    for district in range(0,n):
        sum_variable = get_sum_variable(csp, district, variables, maxSum)
        csp.add_unary_factor(sum_variable, lambda numVoters: numVoters >= minSum and numVoters <= maxSum)
    add_neighbor_constraints(precincts)
    return csp

def add_neighbor_constraints(csp,precincts): #how??
    #for precinct in precincts.keys():
    #   neighbors # = get neighbors
    #   for neighbor in neighbors:


def get_or_variable(csp, name, variables, value):
    """
        Create a new variable with domain [True, False] that can only be assigned to
        True iff at least one of the |variables| is assigned to |value|. You should
        add any necessary intermediate variables, unary factors, and binary
        factors to achieve this. Then, return the name of this variable.
        
        @param name: Prefix of all the variables that are going to be added.
        Can be any hashable objects. For every variable |var| added in this
        function, it's recommended to use a naming strategy such as
        ('or', |name|, |var|) to avoid conflicts with other variable names.
        @param variables: A list of variables in the CSP that are participating
        in this OR function. Note that if this list is empty, then the returned
        variable created should never be assigned to True.
        @param value: For the returned OR variable being created to be assigned to
        True, at least one of these variables must have this value.
        
        @return result: The OR variable's name. This variable should have domain
        [True, False] and constraints s.t. it's assigned to True iff at least
        one of the |variables| is assigned to |value|.
        """
    result = ('or', name, 'aggregated')
    csp.add_variable(result, [True, False])
    
    # no input variable, result should be False
    if len(variables) == 0:
        csp.add_unary_factor(result, lambda val: not val)
        return result

    # Let the input be n variables X0, X1, ..., Xn.
    # After adding auxiliary variables, the factor graph will look like this:
    #
    # ^--A0 --*-- A1 --*-- ... --*-- An --*-- result--^^
    #    |        |                  |
    #    *        *                  *
    #    |        |                  |
    #    X0       X1                 Xn
    #
    # where each "--*--" is a binary constraint and "--^" and "--^^" are unary
    # constraints. The "--^^" constraint will be added by the caller.
    for i, X_i in enumerate(variables):
        # create auxiliary variable for variable i
        # use systematic naming to avoid naming collision
        A_i = ('or', name, i)
        # domain values:
        # - [ prev ]: condition satisfied by some previous X_j
        # - [equals]: condition satisfied by X_i
        # - [  no  ]: condition not satisfied yet
        csp.add_variable(A_i, ['prev', 'equals', 'no'])
        
        # incorporate information from X_i
        def factor(val, b):
            if (val == value): return b == 'equals'
            return b != 'equals'
        csp.add_binary_factor(X_i, A_i, factor)
        
        if i == 0:
            # the first auxiliary variable, its value should never
            # be 'prev' because there's no X_j before it
            csp.add_unary_factor(A_i, lambda b: b != 'prev')
        else:
            # consistency between A_{i-1} and A_i
            def factor(b1, b2):
                if b1 in ['equals', 'prev']: return b2 != 'no'
                return b2 != 'prev'
            csp.add_binary_factor(('or', name, i - 1), A_i, factor)

    # consistency between A_n and result
    # hacky: reuse A_i because of python's loose scope
    csp.add_binary_factor(A_i, result, lambda val, res: res == (val != 'no'))
    return result

class BacktrackingSearch():
    
    def reset_results(self):
        """
            This function resets the statistics of the different aspects of the
            CSP solver. We will be using the values here for grading, so please
            do not make any modification to these variables.
            """
        # Keep track of the best assignment and weight found.
        self.optimalAssignment = {}
        self.optimalWeight = 0
        
        # Keep track of the number of optimal assignments and assignments. These
        # two values should be identical when the CSP is unweighted or only has binary
        # weights.
        self.numOptimalAssignments = 0
        self.numAssignments = 0
        
        # Keep track of the number of times backtrack() gets called.
        self.numOperations = 0
        
        # Keep track of the number of operations to get to the very first successful
        # assignment (doesn't have to be optimal).
        self.firstAssignmentNumOperations = 0
        
        # List of all solutions found.
        self.allAssignments = []
    
    def print_stats(self):
        """
            Prints a message summarizing the outcome of the solver.
            """
        if self.optimalAssignment:
            print "Found %d optimal assignments with weight %f in %d operations" % \
                (self.numOptimalAssignments, self.optimalWeight, self.numOperations)
            print "First assignment took %d operations" % self.firstAssignmentNumOperations
        else:
            print "No solution was found."

def get_delta_weight(self, assignment, var, val):
    """
        Given a CSP, a partial assignment, and a proposed new value for a variable,
        return the change of weights after assigning the variable with the proposed
        value.
        
        @param assignment: A dictionary of current assignment. Unassigned variables
        do not have entries, while an assigned variable has the assigned value
        as value in dictionary. e.g. if the domain of the variable A is [5,6],
        and 6 was assigned to it, then assignment[A] == 6.
        @param var: name of an unassigned variable.
        @param val: the proposed value.
        
        @return w: Change in weights as a result of the proposed assignment. This
        will be used as a multiplier on the current weight.
        """
    assert var not in assignment
    w = 1.0
    if self.csp.unaryFactors[var]:
        w *= self.csp.unaryFactors[var][val]
        if w == 0: return w
    for var2, factor in self.csp.binaryFactors[var].iteritems():
        if var2 not in assignment: continue  # Not assigned yet
        w *= factor[val][assignment[var2]]
        if w == 0: return w
    return w

def solve(self, csp, mcv = False, ac3 = False):
    """
        Solves the given weighted CSP using heuristics as specified in the
        parameter. Note that unlike a typical unweighted CSP where the search
        terminates when one solution is found, we want this function to find
        all possible assignments. The results are stored in the variables
        described in reset_result().
        
        @param csp: A weighted CSP.
        @param mcv: When enabled, Most Constrained Variable heuristics is used.
        @param ac3: When enabled, AC-3 will be used after each assignment of an
        variable is made.
        """
        # CSP to be solved.
    self.csp = csp
                
        # Set the search heuristics requested asked.
    self.mcv = mcv
    self.ac3 = ac3
                        
        # Reset solutions from previous search.
    self.reset_results()
                            
        # The dictionary of domains of every variable in the CSP.
    self.domains = {var: list(self.csp.values[var]) for var in self.csp.variables}
                                
        # Perform backtracking search.
    self.backtrack({}, 0, 1)
        # Print summary of solutions.
    self.print_stats()
def backtrack(self, assignment, numAssigned, weight):
    """
        Perform the back-tracking algorithms to find all possible solutions to
        the CSP.
        
        @param assignment: A dictionary of current assignment. Unassigned variables
        do not have entries, while an assigned variable has the assigned value
        as value in dictionary. e.g. if the domain of the variable A is [5,6],
        and 6 was assigned to it, then assignment[A] == 6.
        @param numAssigned: Number of currently assigned variables
        @param weight: The weight of the current partial assignment.
        """
    self.numOperations += 1
    assert weight > 0
    if numAssigned == self.csp.numVars:
    # A satisfiable solution have been found. Update the statistics.
        self.numAssignments += 1
        newAssignment = {}
        for var in self.csp.variables:
            newAssignment[var] = assignment[var]
        self.allAssignments.append(newAssignment)
                                            
        if len(self.optimalAssignment) == 0 or weight >= self.optimalWeight:
            if weight == self.optimalWeight:
                self.numOptimalAssignments += 1
            else:
                self.numOptimalAssignments = 1
            self.optimalWeight = weight
                                                                    
            self.optimalAssignment = newAssignment
            if self.firstAssignmentNumOperations == 0:
                self.firstAssignmentNumOperations = self.numOperations
        return
                                                                                    
        # Select the next variable to be assigned.
    var = self.get_unassigned_variable(assignment)
        # Get an ordering of the values.
    ordered_values = self.domains[var]
                                                                                            
        # Continue the backtracking recursion using |var| and |ordered_values|.
    if not self.ac3:
            # When arc consistency check is not enabled.
        for val in ordered_values:
            deltaWeight = self.get_delta_weight(assignment, var, val)
            if deltaWeight > 0:
                assignment[var] = val
                self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                del assignment[var]
    else:
            # Arc consistency check is enabled.
            # Problem 1c: skeleton code for AC-3
            # You need to implement arc_consistency_check().
        for val in ordered_values:
            deltaWeight = self.get_delta_weight(assignment, var, val)
            if deltaWeight > 0:
                assignment[var] = val
                    # create a deep copy of domains as we are going to look
                    # ahead and change domain values
                localCopy = copy.deepcopy(self.domains)
                    # fix value for the selected variable so that hopefully we
                    # can eliminate values for other variables
                self.domains[var] = [val]
                    
                    # enforce arc consistency
                self.arc_consistency_check(var)
                    
                self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                    # restore the previous domains
                self.domains = localCopy
                del assignment[var]

def get_unassigned_variable(self, assignment):
    """
    Given a partial assignment, return a currently unassigned variable.
                                
    @param assignment: A dictionary of current assignment. This is the same as
    what you've seen so far.
                                
    @return var: a currently unassigned variable.
    """
    if not self.mcv:
        # Select a variable without any heuristics.
        for var in self.csp.variables:
            if var not in assignment: return var
    else:
    # Problem 1b
    # Heuristic: most constrained variable (MCV)
    # Select a variable with the least number of remaining domain values.
    # Hint: given var, self.domains[var] gives you all the possible values
    # Hint: get_delta_weight gives the change in weights given a partial
    #       assignment, a variable, and a proposed value to this variable
    # Hint: for ties, choose the variable with lowest index in self.csp.variables
    # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        mcv = None
        mcv_num = float('inf')
        for var in self.csp.variables:
            if var not in assignment:
                values = self.domains[var]
                num = 0
                for a in values:
                    if self.get_delta_weight(assignment,var,a) != 0:
                        num += 1
            if num < mcv_num:
                mcv = var
                mcv_num = num
        return mcv

# END_YOUR_CODE


def arc_consistency_check(self, var):
    """
    Perform the AC-3 algorithm. The goal is to reduce the size of the
    domain values for the unassigned variables based on arc consistency.
        
    @param var: The variable whose value has just been set.
    """

    import Queue
    q = Queue.Queue()
    q.put(var)
    while not q.empty():
        var1 = q.get()
        for var2 in self.csp.get_neighbor_vars(var1):
            inconsistentValues = []
            for val2 in self.domains[var2]:
                inconsistent = True
                for val1 in self.domains[var1]:
                    if self.csp.binaryFactors[var1][var2][val1][val2] != 0:
                        inconsistent = False
                if inconsistent:
                    inconsistentValues.append(val2)
            for xVal in inconsistentValues:
                self.domains[var2].remove(xVal)
            if len(inconsistentValues) > 0:
                q.put(var2)

def get_sum_variable(csp, name, variables, maxSum):
    """
        Given a list of |variables| each with non-negative integer domains,
        returns the name of a new variable with domain range(0, maxSum+1), such that
        it's consistent with the value |n| iff the assignments for |variables|
        sums to |n|.
        
        @param name: Prefix of all the variables that are going to be added.
        Can be any hashable objects. For every variable |var| added in this
        function, it's recommended to use a naming strategy such as
        ('sum', |name|, |var|) to avoid conflicts with other variable names.
        @param variables: A list of variables that are already in the CSP that
        have non-negative integer values as its domain.
        @param maxSum: An integer indicating the maximum sum value allowed. You
        can use it to get the auxiliary variables' domain
        
        @return result: The name of a newly created variable with domain range
        [0, maxSum] such that it's consistent with an assignment of |n|
        iff the assignment of |variables| sums to |n|.
        """
    # BEGIN_YOUR_CODE (our solution is 18 lines of code, but don't worry if you deviate from this)
    result = ('sum', name, 'aggregated')
    domain = [i for i in range(0,maxSum + 1)]
    csp.add_variable(result, domain)
    district = int(name)
    if len(variables) == 0:
        csp.add_unary_factor(result, lambda val: val == 0)
        return result
    tuples_init = []
    for i in domain:
        tuples_init.append((0,i))
    tuples = []
    for i in domain:
        for j in range(i, maxSum + 1):
            tuples.append((i,j))
    for i, X_i in enumerate(variables):
        B_i = ('sum', name, i)
        if i == 0: csp.add_variable(B_i,tuples_init)
        else: csp.add_variable(B_i,tuples)
        
        def factor(xVal,bVal):
            if xVal[0] == district:
                return (bVal[1] == bVal[0] + xVal[1]) #xVal[1])#where xVal = (district,numVoters,neighbors)
            else: return bVal[1] == bVal[0]
    
        csp.add_binary_factor(X_i,B_i,factor)
        if i == 0:
            csp.add_unary_factor(B_i,lambda bVal: bVal[0] == 0)
        else:
            def factor(b1,b2):
                return b1[1] == b2[0]
            csp.add_binary_factor(('sum', name, i - 1), B_i, factor)
    csp.add_binary_factor(B_i, result, lambda val, res: val[1] == res)
    return result

def main():
    data = loadCsvData('ncvoter34.csv')
    
    numDistricts = 8
    targetVoters = 410,976
    range = 1000
    csp = redistricting_csp(precincts,numDistricts,targetVoters,range)


def loadCsvData(filename):
    matrix = []
    raceCode = 25
    party = 27
    gender = 28
    precinct = 33
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            parsedRow = []
            itemIndex = 0
            for value in row:
                if itemIndex == raceCode:
                    parsedRow.append(value)
                if itemIndex == party:
                    parsedRow.append(value)
                if itemIndex == gender:
                    parsedRow.append(value)
                if itemIndex == precinct:
                    parsedRow.append(value)
                itemIndex += 1
            if parsedRow[3] != '':
                    matrix.append(parsedRow)
    return matrix

# Prints out a 2d array
def printData(matrix):
    for row in matrix:
        print row

# This if statement passes if this
# was the file that was executed
if __name__ == '__main__':
    main()
