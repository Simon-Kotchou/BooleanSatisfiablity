def parse(filename):
    clauses = []
    count = 0
    first = 0
    for line in open(filename):

        if first==0:
            n_vars = int(line.split()[1])
            lit_clause = [[] for _ in range(n_vars * 2 + 1)]
            first = 1
            continue

        clause = []
        for literal in line.split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause

def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit

def verify(interpretation):
    clauses, n_vars, lit_clause = parse("input.txt")
    true_sat_lit = get_true_sat_lit(clauses, interpretation)
    unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]
    print(len(clauses) - len(unsatisfied_clauses_index))

def main():
    verify([0,-1,-2,3,-4,-5])

if __name__ == "__main__":
    main()

