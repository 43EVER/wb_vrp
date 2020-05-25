from ortools.linear_solver import pywraplp

def main():

    # 创建求解器，对于一般的线性规划问题，我们使用 GLOP 求解器
    # GLOP 求解器会在下面的章节介绍
    solver = pywraplp.Solver('SolveSimpleSystem',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # 然后创建变量 x 和 y，同时指定变量的取值范围
    x = solver.NumVar(0, 1, 'x')
    y = solver.NumVar(0, 2, 'y')

    # 创建目标函数，通过设置系数的方式实现目标函数
    # 相比直接写数学方程式就没那么直观了
    # Create the objective function, x + y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 1)
    objective.SetCoefficient(y, 1)

    # 指定求最大值还是求最小值
    objective.SetMaximization()

    # 最后求解，打印结果
    solver.Solve()
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())

if __name__ == '__main__':
  main()