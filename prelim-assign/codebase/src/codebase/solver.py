import json
import pyomo.environ as pyo
import numpy as np


def main_optimization_model(mu, cov, tickers, target_return, allow_short=False):
    n = len(mu)
    assets = range(n)
    tolerance = 0.0010 #This is important!

    model = pyo.ConcreteModel()
    model.w = pyo.Var(assets, domain=pyo.Reals if allow_short else pyo.NonNegativeReals)

    model.budget = pyo.Constraint(expr=sum(model.w[i] for i in assets) == 1)


    # Allow target return +/- tolerance
    model.target = pyo.Constraint(
        expr=sum(model.w[i] * mu[i] for i in assets) >= target_return - tolerance
    )
    model.target_max = pyo.Constraint(
        expr=sum(model.w[i] * mu[i] for i in assets) <= target_return + tolerance
    )


    model.obj = pyo.Objective(
        expr=sum(model.w[i] * cov[i][j] * model.w[j] for i in assets for j in assets), 
        sense=pyo.minimize,
    )

    solver = pyo.SolverFactory("highs")
    result = solver.solve(model)
    objective_value = pyo.value(model.obj)

    weights = {tickers[i]: pyo.value(model.w[i]) for i in assets}
    return weights, result, objective_value


def max_3_optimization_model(mu, cov, tickers, target_return, allow_short=False):
    n = len(mu)
    assets = range(n)
    tolerance = 0.0010 #This is important!

    model = pyo.ConcreteModel()
    model.w = pyo.Var(assets, domain=pyo.Reals if allow_short else pyo.NonNegativeReals)

    model.budget = pyo.Constraint(expr=sum(model.w[i] for i in assets) == 1)


    # Allow target return +/- tolerance
    model.target = pyo.Constraint(
        expr=sum(model.w[i] * mu[i] for i in assets) >= target_return - tolerance
    )
    model.target_max = pyo.Constraint(
        expr=sum(model.w[i] * mu[i] for i in assets) <= target_return + tolerance
    )


    model.obj = pyo.Objective(
        expr=sum(model.w[i] * cov[i][j] * model.w[j] for i in assets for j in assets), 
        sense=pyo.minimize,
    )

    solver = pyo.SolverFactory("highs")
    result = solver.solve(model)
    objective_value = pyo.value(model.obj)

    weights = {tickers[i]: pyo.value(model.w[i]) for i in assets}
    return weights, result, objective_value


with open("data_cleaned.json") as f:
    data = json.load(f)
    tickers = data["ticker_list"]
    mu = data["exp_ret_list"]
    cov = data["cov_nested_list"]

print("Test run with target return of 1.2, just to print in terminal and see")
weights, result, objective_value = main_optimization_model(mu, cov, tickers, target_return=1.2, allow_short=True)
print("Solver status:", result.solver.status, result.solver.termination_condition)
print("Weights:", weights)
print("Portfolio variance", objective_value)


#### Efficient frontier no short selling

min_mu = min(mu)
max_mu = max(mu)
increment = 0.001 #Adjust to desired granularity

range_mu_no_short = np.arange(min_mu, max_mu, increment).tolist()

no_short_results = list()

print("Start main optimization for loop run (no short selling)")

for given_mu in range_mu_no_short:
    weights, result, objective_value = main_optimization_model(mu, cov, tickers, target_return=given_mu, allow_short=False)
    no_short_results.append({
        "target_return": given_mu,
        "weights": weights,
        "variance": objective_value,
        "solver_status": str(result.solver.status),
        "termination_condition": str(result.solver.termination_condition)
    })
    print("Solver no short finished")


#### Efficient frontier short selling allowed

short_results = list()

range_mu_yes_short = np.arange(min_mu, max_mu+0.01, increment).tolist()
print("Start short selling optimization")
for given_mu in range_mu_yes_short:
    weights, result, objective_value = main_optimization_model(mu, cov, tickers, target_return=given_mu, allow_short=True)
    short_results.append({
        "target_return": given_mu,
        "weights": weights,
        "variance": objective_value,
        "solver_status": str(result.solver.status),
        "termination_condition": str(result.solver.termination_condition)
    })
    print("Solver short finished")

nr_runs_done = len(no_short_results) + len(short_results)
print("Done")
print("Nr solver runs: " + str(nr_runs_done))

#### Write results to JSON
frontier_output = {
    "no_short_selling": no_short_results,
    "short_selling": short_results,
    "summary": {
        "total_solves": nr_runs_done,
        "no_short_count": len(no_short_results),
        "short_count": len(short_results)
    }
}

with open("solver.output.json", "w") as f:
    json.dump(frontier_output, f, indent=2)

print("Results written to solver.output.json")



