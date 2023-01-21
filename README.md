![logo.png](static/logo.png)

## Summary

People often make ad-hoc analogies between physics and optimization. There certainly are some surface level mathematical similarities. But it turns out that there are deeper connections too. In physics, every path through space can be associated with a stationary value of a scalar called the action. The action is a well-studied quantity in theoretical physics, but it is never minimized directly as though it were the cost function of an optimization problem. In this paper, we do exactly that, obtaining physics simulations by writing the action in terms of paths from initial to final states. In this context, the act of simulation is _literally_ the act of optimization. We demonstrate our technique on simulations of: a particle in free fall, a pendulum, a double pendulum, the three body problem, a gas simulation, real ephemeris data from the inner planets of the solar system, and a quantum wave packet.

Out approach allows us to do some things we wouldn't be able to do otherwise. We can infill dynamics connecting two known observations. We can fine-tune an ODE solution post-hoc to increase its resolution. And we can cheaply obtain dynamics in scenarios where we don't care about the final state. We conclude by showing how, at the quantum scale, distributions of viable paths interfere with one another constructively and destructively, forcing us to take into account many simultaneous routes through space and giving rise to the path integral formulation of quantum mechanics.

## How to run

* Jupyter notebook
	* Open `main.ipnyb` which is located in this directory
* Command line
	* Navigate to the directory containing this README
	* Run, eg. `python main.py --experiment dblpend`
	* Note: `--experiment` is one of {`freebody`, `singlepend`, `doublepend`, `threebody`, `gas`, `ephemeris`}


## Simulations

* Free body
	* Minimal working example
* Single Pendulum
	* Minimal working example with nonlinearities and radial coordinates
* Double pendulum
	* A chaotic system with sharp nonlinear dynamics
* Three body problem
	* A chaotic system with sharp nonlinear dynamics and N=6 degrees of freedom
* Gas simulation
	* * A chaotic system with sharp nonlinear dynamics and N=400 degrees of freedom
* Ephemeris dataset
	* A real physics data taken from the JPL Horizons project
	* One year of orbital data for the sun and the inner planets of the solar system
	* Orbits are projected onto a 2D plane


## Depedencies

* PyTorch `pip install torch` <3
* Pandas `pip install pandas` <3
* Celluloid (making videos) `pip install celluloid` <3
