from ortools.sat.python import cp_model

class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print('可行解 %i' % self.__solution_count)
        print(' 目标函数值 %i' % self.ObjectiveValue())
        for v in self.__variables:
            print(' %s = %i' % (v, self.Value(v)), end=' ')
        print()
        print()

    def solution_count(self):
        return self.__solution_count


def main():
    model = cp_model.CpModel()

    num_vals = 3
    x = model.NewIntVar(0, 2, 'x')
    y = model.NewIntVar(0, 2, 'y')
    z = model.NewIntVar(0, 2, 'z')

    model.Add(x != y)
    model.Add(x != z)
    model.Add(y != z)
    model.Add(x < y)
    model.Add(y < z)

    model.Maximize(x + 2 * y + 3 * z)

    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter([x, y, z])
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    print('求解状态 = %s' % solver.StatusName(status))
    print('可行解数量 = %i' % solution_printer.solution_count())

main()