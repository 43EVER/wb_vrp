'''
Min x + y

0 <= y <= 2, 0 <= x <= 1
'''

from ortools.linear_solver import pywraplp

def minxplusy():
    solver = pywraplp.Solver('SolveSimpleSystem', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    x = solver.NumVar(0, 1, 'x')
    y = solver.NumVar(0, 2, 'y')

    objective = solver.Objective()
    objective.SetCoefficient(x, 1)
    objective.SetCoefficient(y, 1)
    
    objective.SetMinimization()
    
    solver.Solve()
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())


def max3xplus4y():
    solver = pywraplp.Solver('LinearExample', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

    # x + 2y <= 14
    constraint1 = solver.Constraint(-solver.infinity(), 14)
    constraint1.SetCoefficient(x, 1)
    constraint1.SetCoefficient(y, 2)

    # 3x - y >= 0
    constraint2 = solver.Constraint(0, solver.infinity())
    constraint2.SetCoefficient(x, 3)
    constraint2.SetCoefficient(y, -1)

    # x - y <= 2
    constraint3 = solver.Constraint(-solver.infinity(), 2)
    constraint3.SetCoefficient(x, 1)
    constraint3.SetCoefficient(y, -1)

    # Objective function: 3x + 4y
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    objective.SetMaximization()

    # result
    solver.Solve()
    out_solution = 3 * x.solution_value() + 4 * y.solution_value()
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    print('value = ', out_solution)

if __name__ == '__main__':
    max3xplus4y()