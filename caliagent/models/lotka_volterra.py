"""Contains an implementation of the Lotka Volterra model.

An implementation of a Lotka Volterra example model.

"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


def simulate_lotka_volterra(
	alpha: float = 0.52,
	beta: float = 0.024,
	gamma: float = 0.84,
	delta: float = 0.026,
	h0: float = 34.0,
	l0: float = 5.9,
	years: np.ndarray | None = None,
) -> pd.DataFrame:
	"""Run the Lotka-Volterra simulation.

	Args:
	    alpha (float): Sheep reproduction rate.
	    beta (float): Predation rate.
	    gamma (float): Wolf mortality rate.
	    delta (float): Wolf growth rate from predation.
	    h0 (float): Initial sheep population.
	    l0 (float): Initial wolf population.
	    years (array-like | None): Time points at which to evaluate the solution.

	Returns:
	    pd.DataFrame: The simulated sheep and wolf populations.
	"""
	if years is None:
		years = np.arange(1900, 1921, 1)

	def dX_dt(t: np.ndarray, X: np.ndarray) -> list[float]:
		hare, lynx = X

		d_hare = alpha * hare - beta * hare * lynx
		d_lynx = -gamma * lynx + delta * hare * lynx

		return [d_hare, d_lynx]

	solution = solve_ivp(
		dX_dt,
		t_span=(years.min(), years.max()),
		y0=[h0, l0],
		t_eval=years,
	)

	return pd.DataFrame(
		{
			"year": years,
			"sheep": solution.y[0],
			"wolf": solution.y[1],
		}
	)
