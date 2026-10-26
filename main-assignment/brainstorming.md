

*Overall philosophy* We want something that is both technically impressive (Rav can fix this) and financially sound (Brieuc). Why? We want a good grade (at LEAST 16/20) and to learn alot :)

### rav and br first chat
#### Do we use the Markowitz-Mean variance optimization framework?

No we use cvar as risk. 
~~I say yes, if we want something that is better it will quickly become way to complex (Bayesian statistics), our complexity is already high


#### What point on efficient frontier to pick

For what point on the efficient frontier to pick. There are a couple of approachses

##### explicitly define it in function
We use an approach where we explicitly define the tradeoff between variance and mean in the function, something akin to:

$$
MAX : \alpha \cdot E(Return) - (1-\alpha)E(Variance)
$$
(Will ofc have to add some extra params to make EV and VAR into more comparable sizes)


##### tangent porfolio

This will be an extra
~~We assume a risk free rate and pick the tangent porfolio. This is the most correct method from financial theory, and it should be prefered. We can include the other method in the appendix to flex

#### What other constraints to have

**Obligatory**
-Max 30 assets (this requires Integer programing)
-Estimated variance of portofolio must be lower than a portfolio that invest the same amount in each assets

Both of these constraints are simple

We can also add sector specifc constraints, but the more of this extra stuff we add the less we room we give the Solver. we can add one extra just to flex

We want a CVAR Constraint. For this one must read an understand 17.2 in book
#### Rebalancing

Open to your thoughts here Brieuc. 

How we can conceptually think about this is as follows:
-The optimal portfolio moves slighly each week.
-But our porfolio is defined by the past, and it costs to move it closer to the optimal porfolio

Draft of algorithm>

```
For each week:
	If there is a difference between optimal and current porfolio (which there will nearly always will be).
		Use the 100 EURO free budget to move to move as close as possible to the optimal porfolio, measured in some sort of distance (eucledian). #We should do this because it is a free giveaway
		SOME COMPLEX HUMAN IN THE LOOP ALGORITHM FOR REMAINING REBALANCING
		
	
```


Note: What is the most technically impressive is not always the most financially sound. Making a complex rebalancing function (which will be a little wrong either way) is cool, but often just holding a long position and not incurring rebalancing costs is better: Proposed idea: We make a complex function (Rav and Brieuc agree on something) and then we add a human in the loop element (we approve or reject the proposed costly re balancing): We do not fully trust the assumptions of our model to make costly and reactive adjustment autonomously


#### Extra financial bonuses

We can add a interactive dashboard on top that displays sharpe ratio, tangent porfolio, etc etc
This will be seperate from the solver. Vibe coded with Claude Code in 2 hours, eezy

#### Solver technicalities 

We want to push to formulations to be as easy to solve as possible. The QP can be solved by reformulating to linear. Need to read up on this. 

#### Notes from chat
-Convert it all to EU



### rav working on it himself notes


We use the same cleaning script (more or less), then we add a scenario generation script using https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_normal.html


$$
\begin{aligned}
\min_{x,\,z,\,\gamma} \quad & \gamma + \frac{1}{(1-\alpha)S} \sum_{s=1}^{S} z_s \\
\text{s.t.} \quad & z_s \ge 0, && s = 1, \dots, S, \\
& z_s \ge f(x, y_s) - \gamma, && s = 1, \dots, S, \\
& x \in X.
\end{aligned}
\tag{17.10}
$$

#### to do
hand trace generate scenarios function  
run a sanity check on the scenario cumalitvereturnds
check that choosen portfolio has lower variance than one invested in entire market