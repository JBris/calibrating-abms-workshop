"""Contains the Mesa implementation of the Wolf Sheep Predation model.

An implementation of a Wolf Sheep Predation example model.

"""

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from numba import njit


@njit
def _neighbors(
	x: float, y: float, width: int, height: int
) -> tuple[np.ndarray, np.ndarray]:
	"""Return Von Neumann neighbours on a toroidal grid.

	Args:
	    x (float): The x coordinate of the cell.
	    y (float): The y coordinate of the cell.
	    width (int): The width of the grid.
	    height (int): The height of the grid.

	Returns:
	    tuple[np.ndarray, np.ndarray]: The neighbouring x and y coordinates.
	"""
	xs = np.empty(4, dtype=np.int32)
	ys = np.empty(4, dtype=np.int32)

	xs[0] = (x + 1) % width
	ys[0] = y

	xs[1] = (x - 1) % width
	ys[1] = y

	xs[2] = x
	ys[2] = (y + 1) % height

	xs[3] = x
	ys[3] = (y - 1) % height

	return xs, ys


@njit
def _move_sheep(
	x: float,
	y: float,
	wolf_grid: np.ndarray,
	grass: np.ndarray,
	width: int,
	height: int,
) -> tuple[np.ndarray, np.ndarray]:
	"""Move a sheep based on its surroundings.

	Args:
	    x (float): The x coordinate of the sheep.
	    y (float): The y coordinate of the sheep.
	    wolf_grid (np.ndarray): A grid indicating the presence of wolves.
	    grass (np.ndarray): A grid indicating the presence of grass.
	    width (int): The width of the grid.
	    height (int): The height of the grid.

	Returns:
	    tuple[np.ndarray, np.ndarray]: The new x and y coordinates of the sheep.
	"""
	xs, ys = _neighbors(x, y, width, height)

	safe = np.empty(4, dtype=np.int32)
	grassy = np.empty(4, dtype=np.int32)

	n_safe = 0
	n_grassy = 0

	for k in range(4):
		nx = xs[k]
		ny = ys[k]

		if wolf_grid[ny, nx] == 0:
			safe[n_safe] = k
			n_safe += 1

			if grass[ny, nx]:
				grassy[n_grassy] = k
				n_grassy += 1

	if n_safe == 0:
		return x, y

	if n_grassy > 0:
		choice = grassy[np.random.randint(n_grassy)]
	else:
		choice = safe[np.random.randint(n_safe)]

	return xs[choice], ys[choice]


@njit
def _move_wolf(
	x: float,
	y: float,
	sheep_grid: np.ndarray,
	width: int,
	height: int,
) -> tuple[np.ndarray, np.ndarray]:
	"""Move a wolf based on its surroundings.

	Args:
	    x (float): The x coordinate of the wolf.
	    y (float): The y coordinate of the wolf.
	    sheep_grid (np.ndarray): The grid representing the presence of sheep.
	    width (int): The width of the grid.
	    height (int): The height of the grid.

	Returns:
	    tuple[np.ndarray, np.ndarray]: The new x and y coordinates of the wolf.
	"""
	xs, ys = _neighbors(x, y, width, height)

	prey_cells = np.empty(4, dtype=np.int32)
	n_prey_cells = 0

	for k in range(4):
		nx = xs[k]
		ny = ys[k]

		if sheep_grid[ny, nx] > 0:
			prey_cells[n_prey_cells] = k
			n_prey_cells += 1

	if n_prey_cells > 0:
		choice = prey_cells[np.random.randint(n_prey_cells)]
	else:
		choice = np.random.randint(4)

	return xs[choice], ys[choice]


@njit
def wolf_sheep_step(
	sheep_x: np.ndarray,
	sheep_y: np.ndarray,
	sheep_energy: np.ndarray,
	sheep_alive: np.ndarray,
	sheep_slots: int,
	wolf_x: np.ndarray,
	wolf_y: np.ndarray,
	wolf_energy: np.ndarray,
	wolf_alive: np.ndarray,
	wolf_slots: int,
	grass: np.ndarray,
	grass_timer: np.ndarray,
	width: int,
	height: int,
	sheep_reproduce: float,
	wolf_reproduce: float,
	sheep_gain_from_food: float,
	wolf_gain_from_food: float,
	grass_regrowth_time: int,
) -> tuple[int, int, int, int, int]:
	"""Perform a single step of the wolf-sheep predation model.

	Args:
	    sheep_x (np.ndarray): The x coordinates of the sheep.
	    sheep_y (np.ndarray): The y coordinates of the sheep.
	    sheep_energy (np.ndarray): The energy levels of the sheep.
	    sheep_alive (np.ndarray): A boolean array indicating which sheep are alive.
	    sheep_slots (int): The number of sheep slots.
	    wolf_x (np.ndarray): The x coordinates of the wolves.
	    wolf_y (np.ndarray): The y coordinates of the wolves.
	    wolf_energy (np.ndarray): The energy levels of the wolves.
	    wolf_alive (np.ndarray): A boolean array indicating which wolves are alive.
	    wolf_slots (int): The number of wolf slots.
	    grass (np.ndarray): The grass grid.
	    grass_timer (np.ndarray): The timer for each grass cell.
	    width (int): The width of the grid.
	    height (int): The height of the grid.
	    sheep_reproduce (float): The probability of sheep reproducing.
	    wolf_reproduce (float): The probability of wolves reproducing.
	    sheep_gain_from_food (float): The energy gained by sheep from eating grass.
	    wolf_gain_from_food (float): The energy gained by wolves from eating sheep.
	    grass_regrowth_time (int):
			The time it takes for grass to regrow after being eaten.

	Returns:
	    tuple[int, int, int, int, int]:
			The updated number of slots and counts.
	"""

	for y in range(height):
		for x in range(width):
			if not grass[y, x]:
				grass_timer[y, x] -= 1

				if grass_timer[y, x] <= 0:
					grass[y, x] = True
					grass_timer[y, x] = 0

	wolf_grid = np.zeros((height, width), dtype=np.int32)

	for i in range(wolf_slots):
		if wolf_alive[i]:
			wolf_grid[
				wolf_y[i],
				wolf_x[i],
			] += 1

	sheep_order = np.empty(sheep_slots, dtype=np.int32)
	n_active_sheep = 0

	for i in range(sheep_slots):
		if sheep_alive[i]:
			sheep_order[n_active_sheep] = i
			n_active_sheep += 1

	np.random.shuffle(sheep_order[:n_active_sheep])

	for a in range(n_active_sheep):
		i = sheep_order[a]

		if not sheep_alive[i]:
			continue

		# Move
		nx, ny = _move_sheep(
			sheep_x[i],
			sheep_y[i],
			wolf_grid,
			grass,
			width,
			height,
		)

		sheep_x[i] = nx
		sheep_y[i] = ny

		# Energy cost
		sheep_energy[i] -= 1.0

		# Eat grass
		if grass[ny, nx]:
			sheep_energy[i] += sheep_gain_from_food

			grass[ny, nx] = False
			grass_timer[ny, nx] = grass_regrowth_time

		# Death
		if sheep_energy[i] < 0:
			sheep_alive[i] = False
			continue

		if np.random.random() < sheep_reproduce:
			offspring_energy = sheep_energy[i] / 2.0
			sheep_energy[i] = offspring_energy

			offspring = -1

			# Reuse dead slot
			for j in range(sheep_slots):
				if not sheep_alive[j]:
					offspring = j
					break

			if offspring == -1:
				if sheep_slots >= sheep_alive.shape[0]:
					# No available capacity
					continue

				offspring = sheep_slots
				sheep_slots += 1

			sheep_x[offspring] = sheep_x[i]
			sheep_y[offspring] = sheep_y[i]
			sheep_energy[offspring] = offspring_energy
			sheep_alive[offspring] = True

	sheep_grid = np.zeros((height, width), dtype=np.int32)

	for i in range(sheep_slots):
		if sheep_alive[i]:
			sheep_grid[
				sheep_y[i],
				sheep_x[i],
			] += 1

	wolf_order = np.empty(wolf_slots, dtype=np.int32)
	n_active_wolves = 0

	for i in range(wolf_slots):
		if wolf_alive[i]:
			wolf_order[n_active_wolves] = i
			n_active_wolves += 1

	np.random.shuffle(wolf_order[:n_active_wolves])

	for a in range(n_active_wolves):
		i = wolf_order[a]

		if not wolf_alive[i]:
			continue

		# Move
		nx, ny = _move_wolf(
			wolf_x[i],
			wolf_y[i],
			sheep_grid,
			width,
			height,
		)

		wolf_x[i] = nx
		wolf_y[i] = ny

		wolf_energy[i] -= 1.0
		if sheep_grid[ny, nx] > 0:
			n_here = sheep_grid[ny, nx]

			prey_indices = np.empty(
				n_here,
				dtype=np.int32,
			)

			n_prey = 0

			for j in range(sheep_slots):
				if sheep_alive[j] and sheep_x[j] == nx and sheep_y[j] == ny:
					prey_indices[n_prey] = j
					n_prey += 1

			if n_prey > 0:
				prey = prey_indices[np.random.randint(n_prey)]

				sheep_alive[prey] = False

				sheep_grid[ny, nx] -= 1

				wolf_energy[i] += wolf_gain_from_food

		if wolf_energy[i] < 0:
			wolf_alive[i] = False
			continue

		if np.random.random() < wolf_reproduce:
			offspring_energy = wolf_energy[i] / 2.0
			wolf_energy[i] = offspring_energy

			offspring = -1

			for j in range(wolf_slots):
				if not wolf_alive[j]:
					offspring = j
					break

			if offspring == -1:
				if wolf_slots >= wolf_alive.shape[0]:
					continue

				offspring = wolf_slots
				wolf_slots += 1

			wolf_x[offspring] = wolf_x[i]
			wolf_y[offspring] = wolf_y[i]
			wolf_energy[offspring] = offspring_energy
			wolf_alive[offspring] = True

	sheep_count = 0

	for i in range(sheep_slots):
		if sheep_alive[i]:
			sheep_count += 1

	wolf_count = 0

	for i in range(wolf_slots):
		if wolf_alive[i]:
			wolf_count += 1

	grass_count = 0

	for y in range(height):
		for x in range(width):
			if grass[y, x]:
				grass_count += 1

	return (
		sheep_slots,
		wolf_slots,
		sheep_count,
		wolf_count,
		grass_count,
	)


class WolfSheep(Model):
	"""An implementation of the Wolf Sheep Predation model."""

	def __init__(
		self,
		width: int = 20,
		height: int = 20,
		initial_sheep: int = 100,
		initial_wolves: int = 50,
		sheep_reproduce: float = 0.04,
		wolf_reproduce: float = 0.05,
		wolf_gain_from_food: float = 20.0,
		grass: bool = True,
		grass_regrowth_time: int = 30,
		sheep_gain_from_food: float = 4.0,
		seed: int | None = None,
		sheep_capacity: int = 100_000,
		wolf_capacity: int = 50_000,
	) -> None:
		"""
		WolfSheep constructor.
		Create a new Wolf Sheep Predation model with the given parameters.

		Args:
		    width (int, optional): The width of the grid. Defaults to 20.
		    height (int, optional): The height of the grid. Defaults to 20.
		    initial_sheep (int, optional): The initial number of sheep. Defaults to 100.
		    initial_wolves (int, optional): The initial number of wolves. Defaults to 50.
		    sheep_reproduce (float, optional): The probability of sheep reproduction.
				Defaults to 0.04.
		    wolf_reproduce (float, optional): The probability of wolf reproduction.
				Defaults to 0.05.
		    wolf_gain_from_food (float, optional):
				The energy gain for wolves from eating sheep. Defaults to 20.0.
		    grass (bool, optional): Whether grass is enabled. Defaults to True.
		    grass_regrowth_time (int, optional):
				The time it takes for grass to regrow. Defaults to 30.
		    sheep_gain_from_food (float, optional):
				The energy gain for sheep from eating grass. Defaults to 4.0.
		    seed (int | None, optional): The random seed. Defaults to None.
		    sheep_capacity (int, optional):
				The maximum number of sheep that can be simulated. Defaults to 100_000.
		    wolf_capacity (int, optional):
				The maximum number of wolves that can be simulated. Defaults to 50_000.
		"""

		super().__init__(seed=seed)

		self.width = width
		self.height = height

		self.sheep_reproduce = sheep_reproduce
		self.wolf_reproduce = wolf_reproduce

		self.wolf_gain_from_food = wolf_gain_from_food
		self.sheep_gain_from_food = sheep_gain_from_food

		self.grass_enabled = grass
		self.grass_regrowth_time = grass_regrowth_time

		if seed is None:
			numba_seed = np.random.randint(
				0,
				2**31 - 1,
			)
		else:
			numba_seed = int(seed)

		np.random.seed(numba_seed)

		self.sheep_x = np.zeros(
			sheep_capacity,
			dtype=np.int32,
		)

		self.sheep_y = np.zeros(
			sheep_capacity,
			dtype=np.int32,
		)

		self.sheep_energy = np.zeros(
			sheep_capacity,
			dtype=np.float64,
		)

		self.sheep_alive = np.zeros(
			sheep_capacity,
			dtype=np.bool_,
		)

		self.sheep_slots = initial_sheep

		self.sheep_x[:initial_sheep] = self.rng.integers(
			0,
			width,
			size=initial_sheep,
		)

		self.sheep_y[:initial_sheep] = self.rng.integers(
			0,
			height,
			size=initial_sheep,
		)

		self.sheep_energy[:initial_sheep] = (
			self.rng.random(initial_sheep) * 2.0 * sheep_gain_from_food
		)

		self.sheep_alive[:initial_sheep] = True

		self.wolf_x = np.zeros(
			wolf_capacity,
			dtype=np.int32,
		)

		self.wolf_y = np.zeros(
			wolf_capacity,
			dtype=np.int32,
		)

		self.wolf_energy = np.zeros(
			wolf_capacity,
			dtype=np.float64,
		)

		self.wolf_alive = np.zeros(
			wolf_capacity,
			dtype=np.bool_,
		)

		self.wolf_slots = initial_wolves

		self.wolf_x[:initial_wolves] = self.rng.integers(
			0,
			width,
			size=initial_wolves,
		)

		self.wolf_y[:initial_wolves] = self.rng.integers(
			0,
			height,
			size=initial_wolves,
		)

		self.wolf_energy[:initial_wolves] = (
			self.rng.random(initial_wolves) * 2.0 * wolf_gain_from_food
		)

		self.wolf_alive[:initial_wolves] = True

		self.grass = np.ones(
			(height, width),
			dtype=np.bool_,
		)

		self.grass_timer = np.zeros(
			(height, width),
			dtype=np.int32,
		)

		if grass:
			initial_growth = self.rng.random((height, width)) < 0.5

			self.grass[:, :] = initial_growth

			for y in range(height):
				for x in range(width):
					if not self.grass[y, x]:
						self.grass_timer[y, x] = self.rng.integers(
							0,
							grass_regrowth_time,
						)

		else:
			self.grass[:, :] = True

		self.sheep_count = initial_sheep
		self.wolf_count = initial_wolves
		self.grass_count = int(np.count_nonzero(self.grass))

		self.datacollector = DataCollector(
			model_reporters={
				"Sheep": lambda m: m.sheep_count,
				"Wolves": lambda m: m.wolf_count,
				"Grass": lambda m: m.grass_count,
			}
		)

		self.running = True

		self.datacollector.collect(self)

	def step(self) -> None:
		(
			self.sheep_slots,
			self.wolf_slots,
			self.sheep_count,
			self.wolf_count,
			self.grass_count,
		) = wolf_sheep_step(
			self.sheep_x,
			self.sheep_y,
			self.sheep_energy,
			self.sheep_alive,
			self.sheep_slots,
			self.wolf_x,
			self.wolf_y,
			self.wolf_energy,
			self.wolf_alive,
			self.wolf_slots,
			self.grass,
			self.grass_timer,
			self.width,
			self.height,
			self.sheep_reproduce,
			self.wolf_reproduce,
			self.sheep_gain_from_food,
			self.wolf_gain_from_food,
			self.grass_regrowth_time,
		)

		self.datacollector.collect(self)

		if self.sheep_count == 0 and self.wolf_count == 0:
			self.running = False
