![logo.png](static/logo.png)

Nature has a cost function. It is a scalar function called the action whose stationary points, often minima, represent physically valid dynamics for any physics problem. Given how fundamental the action is, it is surprising that it is never minimized in a computational setting. The purpose of this work is to explore whether this is possible. We show that, in fact, it is possible and can be used to simulate a body in free fall, a pendulum, a double pendulum, the three body problem, a simple gas, and the planetary ephemerides. In closing, we visualize how multiple paths interfere with one another at the quantum scale, forcing us to take into account many paths at once and giving rise to the path integral formulation of quantum mechanics.

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
