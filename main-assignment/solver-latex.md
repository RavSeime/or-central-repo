

# initial model

## sets

$S$ : set of scenarios  
T : set of tickers (stocks)
$T^{tech} \subset T$ : subset of tickers that are tech stocks

## decision vars

$\gamma$ : CVar measured in %
$w_t$ : Proportion of portfolio invested into stock $t$ 
$z_s$ : Helper variable for minimizing CVar
$x_t$ : Binary variable, 1 if stock $t$ is in portfolio, 0 otherwise

## parameter definitons

$\alpha$ : Probability level for CVar 
$r_{s,t}$ : Return of stock $t$ in scenario $s$ 
$\mu_t$ : Expected (geometric) return of stock $t$
$\mu^*$ : Target portfolio return
$\epsilon$ : Tolerance band around target return
$k$ : Maximum number of stocks in portfolio (set to 30)
$M$ : Big-M constant (set to 1.0) 
$j$ : Maximum share of portfolio in tech stocks (set to 0.3)
## main model
$$
\begin{aligned}
\min_{w,\,z,\,\gamma} \quad & \gamma + \frac{1}{(1-\alpha)|S|} \sum_{s \in S} z_s\\
\text{s.t.} \quad & z_s,w_t \ge 0, && s \in S, t \in T \quad & \text{Non-negativity}\\
& \sum_{t \in T} w_t = 1, && & \text{Budget constraint}\\
& \sum_{t \in T} w_t \mu_t \ge \mu^* - \epsilon, && & \text{Target return lower bound}\\
& \sum_{t \in T} w_t \mu_t \le \mu^* + \epsilon, && & \text{Target return upper bound}\\
& z_s \ge 1 - \sum_{t \in T}( w_t r_{s,t}) - \gamma, && s \in S \quad &\text{Loss constraint}\\
& x_t \in \{0, 1\}, && t \in T \quad & \text{Binary domain}\\
& \sum_{t \in T} x_t \le k, && & \text{Cardinality constraint}\\
& w_t \le M \cdot x_t, && t \in T \quad & \text{Big-M linkage} \\
& \sum_{t \in T^{tech}} w_t \le j \quad && & \text{Max share in tech stocks} 
\end{aligned}$$


# rebalancing model

The rebalancing model is an expansion of the main model. ie all sets, decision variables and model formulations in the main model are present in the rebalancing model. the rebalancing model simply adds new parameters and constrains


## variables
 $y_t^{sell}$ : Binary var that must be 1 if stock $t$ is sold
 $y_t^{buy}$ : Binary var that must be 1 if stock $t$ is bought
$w_t^{sell}$ : Variable that must be at least as large as the amount $t$ sold as a proportion of the portfolio
 $w_t^{buy}$ : Variable that must be at least as large as the amount $t$ bought as a proportion of the portfolio

## parameter definitions
$w_t^{old}$ : Proportion of portfolio invested in stock $t$ before current rebalancing
$g$ : Fixed cost of modifying a stock in EUR (set to 10)
$p$ : Proportional cost of transaction in % (set to 0.0005)
$v$ : The total value of the portfolio before rebalancing
$b$ : The total rebalancing budget in EUR (set to the free budget of 100)
$\delta$ : Small weight on the modification costs in the objective (set to $10^{-6}$)

Note : $w_t^{old}$ cannot be directly inferred from "last weeks" weights, since the prices, and thus the proportions, have changed. Before running the solver both $v$ and $w_t^{old}$ must be calculated
## modified objective
The CVaR objective of the main model is replaced by the one below. The extra term only breaks ties: all else equal, it pushes $w_t^{buy}$, $w_t^{sell}$, $y_t^{buy}$ and $y_t^{sell}$ down to the smallest values the constraints allow, instead of leaving them at arbitrary values when the budget is not binding.
$$
\min_{w,\,z,\,\gamma,\,\ldots} \quad \gamma + \frac{1}{(1-\alpha)|S|} \sum_{s \in S} z_s + \delta \left( FixedModCosts + VarModCosts \right)
$$

## additional constraints
$$
\begin{aligned}
\text{s.t.} \quad & w_t^{buy},w_t^{sell} \ge 0, && t \in T \quad & \text{Non-negativity}\\ 
& y_t^{buy},y_t^{sell}\in \{0, 1\}, && t \in T \quad & \text{Binary domain}\\ 
& y_t^{buy},w_t^{buy} \ge w_t-w_t^{old} && t \in T \quad & \text{Buy var enforcement} \\
& y_t^{sell},w_t^{sell} \ge w_t^{old}-w_t && t \in T \quad & \text{Sell var enforcement} \\
& FixedModCosts =\sum_{t \in T} g ( y_t^{sell} + y_t^{buy})  \\ 
& VarModCosts = \sum_{t \in T} v \cdot p (w_t^{sell} + w_t^{buy}) \\
& FixedModCosts + VarModCosts \le b && & \text{Modification Budget}
\end{aligned} 

$$