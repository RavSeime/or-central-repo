
## sets

$S$ : set of scenarios  
T : set of tickers (stocks)
## decision vars

$\gamma$ : CVar measured in pct points
$w_t$ : Proportion of portfolio invested into stock $t$ 
$z_s$ : Helper variable for minimizing CVar

## parameter definitons

$\alpha$ : Probabilty level for CVar 
## main model
$$
\begin{aligned}
\min_{w,\,z,\,\gamma} \quad & \gamma + \frac{1}{(1-\alpha)S} \sum_{s=1}^{S} z_s \\
\text{s.t.} \quad & z_s \ge 0, && s = 1, \dots, S, \\
& z_s \ge f(w, y_s) - \gamma, && s = 1, \dots, S, \\
\end{aligned}$$
