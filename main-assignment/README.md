# Main assignment

CVaR portfolio optimization on scenario data. The notebooks live in `src/main_assignment/` and pass data to each other through JSON files in `data/`.

## Architecture

```mermaid
flowchart TD

raw([raw input data<br><i>init_all.xlsx, ticker_currencies.json, exchange_rates.json</i>])

clean[datacleaning.ipynb]:::python
stats([expected_returns_covariance_matrix.json<br><i>weekly avg geometric returns + covariance matrix</i>])

scen[scenario_generation.ipynb]:::python
scen_out([scenario_cumulative_returns.json<br><i>1-year cumulative return per scenario and ticker</i>])

latex[solver-latex.md<br><i>CVaR model written in LaTeX</i>]
solver[main_solver.ipynb<br>Pyomo model, solved with HiGHS]:::python
solver_out([solver.output.json<br><i>one optimal portfolio per target return</i>])

plot[plot_frontier.ipynb]:::python
plot_out([efficient_frontier.png])

raw --> clean
clean --> stats
stats --> scen
scen --> scen_out
stats --> solver
scen_out --> solver
latex -. "Implemented in" .-> solver
solver --> solver_out
solver_out --> plot
plot --> plot_out

classDef python fill:#3776AB,stroke:#FFD43B,stroke-width:3px,color:#FFD43B
```

## Core logic

1. **Cleaning** (`datacleaning.ipynb`): convert all prices to EUR, drop tickers with missing or negative values, then compute each ticker's average weekly geometric return and the covariance matrix of weekly percentage changes.
2. **Scenarios** (`scenario_generation.ipynb`): for each of 100 scenarios, draw 52 weeks of returns for all tickers from a multivariate normal (mean = expected returns, covariance = the cleaned matrix). Multiplying the 52 weeks gives the one-year growth multiplier per ticker, e.g. `1.02` means +2%.
3. **Solver** (`main_solver.ipynb`): `solve_cvar` minimizes CVaR at `alpha = 0.95` (model in `solver-latex.md`).
   - The weights sum to 1, and the portfolio's expected return must land within a small band (`±tolerance`) around the target return.
   - The expected returns are annualized (`weekly ** 52`) to match the one-year scenarios.
   - At most `K = 30` stocks are held, enforced with binary variables and a big-M link (`w <= M * x`).
   - The notebook sweeps the target return from `1.0` up to the highest annual expected return. Each target gives one optimal portfolio, and together they trace the frontier.
4. **Plot** (`plot_frontier.ipynb`): target return (y) against CVaR (x). Points where the solver hit its time limit are marked.
