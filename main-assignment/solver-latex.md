
## sets

$S$ : set of scenarios  
T : set of tickers (stocks)
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
$K$ : Maximum number of stocks in portfolio
$M$ : Big-M constant (set to 1.0) 
## main model
$$
\begin{aligned}
\min_{w,\,z,\,\gamma} \quad & \gamma + \frac{1}{(1-\alpha)S} \sum_{s=1}^{S} z_s\\
\text{s.t.} \quad & z_s,w_t \ge 0, && s \in S, t \in T \quad & \text{Non-negativity}\\
& \sum_{t \in T} w_t = 1, && & \text{Budget constraint}\\
& \sum_{t \in T} w_t \mu_t \ge \mu^* - \epsilon, && & \text{Target return lower bound}\\
& \sum_{t \in T} w_t \mu_t \le \mu^* + \epsilon, && & \text{Target return upper bound}\\
& z_s \ge 1 - \sum_{t \in T}( w_t r_{s,t}) - \gamma, && s \in S \quad &\text{Loss constraint}\\
& x_t \in \{0, 1\}, && t \in T \quad & \text{Binary domain}\\
& \sum_{t \in T} x_t \le K, && & \text{Cardinality constraint}\\
& w_t \le M \cdot x_t, && t \in T \quad & \text{Big-M linkage}
\end{aligned}$$
