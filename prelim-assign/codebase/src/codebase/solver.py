import pyomo.environ as pyo


def solve_min_variance(mu, cov, target_return, allow_short=False):
    n = len(mu)
    assets = range(n)

    model = pyo.ConcreteModel()
    model.w = pyo.Var(assets, domain=pyo.Reals if allow_short else pyo.NonNegativeReals)

    model.budget = pyo.Constraint(expr=sum(model.w[i] for i in assets) == 1)
    model.target = pyo.Constraint(expr=sum(model.w[i] * mu[i] for i in assets) == target_return)

    model.obj = pyo.Objective(
        expr=sum(model.w[i] * cov[i][j] * model.w[j] for i in assets for j in assets),
        sense=pyo.minimize,
    )

    solver = pyo.SolverFactory("highs")
    result = solver.solve(model)

    weights = {i: pyo.value(model.w[i]) for i in assets}
    return weights, result


def main():
    # Hardcoded stub data - 3 assets, made up numbers, just to prove the pipe works.
    mu = [0.08, 0.12, 0.05]
    cov = [
        [0.10, 0.02, 0.01],
        [0.02, 0.20, 0.03],
        [0.01, 0.03, 0.05],
    ]

    weights, result = solve_min_variance(mu, cov, target_return=0.08, allow_short=False)

    print("Solver status:", result.solver.status, result.solver.termination_condition)
    print("Weights:", weights)


if __name__ == "__main__":
    main()
