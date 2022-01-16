import random
import sys


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


def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_clause, omega=0.4):
    break_min = float('inf')
    best_literals = []
    for literal in clause:

        break_score = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    if break_min != 0 and random.random() < omega:
        best_literals = clause

    return random.choice(best_literals)


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    count = 0
    target = len(clauses)
    while 1:
        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation)
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:
                return interpretation, (len(clauses) - len(unsatisfied_clauses_index))

            if len(clauses) - len(unsatisfied_clauses_index) >= target:
                return interpretation, (len(clauses) - len(unsatisfied_clauses_index))

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1
        if count == 10:
            target = target -(len(clauses)//1500)
            count = 0
        else:
            count +=1
            


def main():

    clauses, n_vars, lit_clause = parse("input_group172.txt")

    solution,num_sat_clauses = run_sat(clauses, n_vars, lit_clause)

    with open("output_group172.txt", 'a') as out:
        out.write(str(num_sat_clauses))
        out.write("\n")
        for var in solution[1:]:
            if(var > 0):
                out.write("1")
            elif(var < 0):
                out.write("0")
            if not (var == solution[len(solution)-1]):
                out.write("\n")
        out.close()


if __name__ == '__main__':
    main()
