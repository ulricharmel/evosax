import jax
import jax.numpy as jnp
import chex
from typing import Tuple, Optional, Union
from ..strategy import Strategy
from ..utils import GradientOptimizer, OptState, OptParams, exp_decay
from flax import struct


@struct.dataclass
class EvoState:
    mean: chex.Array
    sigma: float
    opt_state: OptState
    best_member: chex.Array
    best_fitness: float = jnp.finfo(jnp.float32).max
    gen_counter: int = 0


@struct.dataclass
class EvoParams:
    opt_params: OptParams
    sigma_init: float = 0.03
    sigma_decay: float = 0.999
    sigma_limit: float = 0.01
    init_min: float = 0.0
    init_max: float = 0.0
    clip_min: float = -jnp.finfo(jnp.float32).max
    clip_max: float = jnp.finfo(jnp.float32).max


class ARS(Strategy):
    def __init__(
        self,
        popsize: int,
        num_dims: Optional[int] = None,
        pholder_params: Optional[Union[chex.ArrayTree, chex.Array]] = None,
        elite_ratio: float = 0.1,
        opt_name: str = "sgd",
        lrate_init: float = 0.05,
        lrate_decay: float = 1.0,
        lrate_limit: float = 0.001,
        sigma_init: float = 0.03,
        sigma_decay: float = 1.0,
        sigma_limit: float = 0.01,
        mean_decay: float = 0.0,
        n_devices: Optional[int] = None,
        **fitness_kwargs: Union[bool, int, float]
    ):
        """Augmented Random Search (Mania et al., 2018)
        Reference: https://arxiv.org/pdf/1803.07055.pdf"""
        super().__init__(
            popsize,
            num_dims,
            pholder_params,
            mean_decay,
            n_devices,
            **fitness_kwargs
        )
        assert not self.popsize & 1, "Population size must be even"
        # ARS performs antithetic sampling & allows you to select
        # "b" elite perturbation directions for the update
        assert 0 <= elite_ratio <= 1
        self.elite_ratio = elite_ratio
        self.elite_popsize = max(1, int(self.popsize / 2 * self.elite_ratio))
        assert opt_name in ["sgd", "adam", "rmsprop", "clipup", "adan"]
        self.optimizer = GradientOptimizer[opt_name](self.num_dims)
        self.strategy_name = "ARS"

        # Set core kwargs es_params (lrate/sigma schedules)
        self.lrate_init = lrate_init
        self.lrate_decay = lrate_decay
        self.lrate_limit = lrate_limit
        self.sigma_init = sigma_init
        self.sigma_decay = sigma_decay
        self.sigma_limit = sigma_limit

    @property
    def params_strategy(self) -> EvoParams:
        """Return default parameters of evolution strategy."""
        opt_params = self.optimizer.default_params.replace(
            lrate_init=self.lrate_init,
            lrate_decay=self.lrate_decay,
            lrate_limit=self.lrate_limit,
        )
        return EvoParams(
            opt_params=opt_params,
            sigma_init=self.sigma_init,
            sigma_decay=self.sigma_decay,
            sigma_limit=self.sigma_limit,
        )

    def initialize_strategy(
        self, rng: chex.PRNGKey, params: EvoParams
    ) -> EvoState:
        """`initialize` the evolution strategy."""
        initialization = jax.random.uniform(
            rng,
            (self.num_dims,),
            minval=params.init_min,
            maxval=params.init_max,
        )

        state = EvoState(
            mean=initialization,
            sigma=params.sigma_init,
            opt_state=self.optimizer.initialize(params.opt_params),
            best_member=initialization,
        )
        return state

    def ask_strategy(
        self, rng: chex.PRNGKey, state: EvoState, params: EvoParams
    ) -> Tuple[chex.Array, EvoState]:
        """`ask` for new parameter candidates to evaluate next."""
        # Antithetic sampling of noise
        z_plus = jax.random.normal(
            rng,
            (int(self.popsize / 2), self.num_dims),
        )
        z = jnp.concatenate([z_plus, -1.0 * z_plus])
        x = state.mean + state.sigma * z
        return x, state

    def tell_strategy(
        self,
        x: chex.Array,
        fitness: chex.Array,
        state: EvoState,
        params: EvoParams,
    ) -> EvoState:
        """`tell` performance data for strategy state update."""
        # Reconstruct noise from last mean/std estimates
        noise = (x - state.mean) / state.sigma
        noise_1 = noise[: int(self.popsize / 2)]
        fit_1 = fitness[: int(self.popsize / 2)]
        fit_2 = fitness[int(self.popsize / 2) :]
        elite_idx = jnp.minimum(fit_1, fit_2).argsort()[: self.elite_popsize]

        fitness_elite = jnp.concatenate([fit_1[elite_idx], fit_2[elite_idx]])
        # Add small constant to ensure non-zero division stability
        sigma_fitness = jnp.std(fitness_elite) + 1e-05
        fit_diff = fit_1[elite_idx] - fit_2[elite_idx]
        fit_diff_noise = jnp.dot(noise_1[elite_idx].T, fit_diff)
        theta_grad = 1.0 / (self.elite_popsize * sigma_fitness) * fit_diff_noise

        # Grad update using optimizer instance - decay lrate if desired
        mean, opt_state = self.optimizer.step(
            state.mean, theta_grad, state.opt_state, params.opt_params
        )
        opt_state = self.optimizer.update(opt_state, params.opt_params)
        sigma = exp_decay(state.sigma, params.sigma_decay, params.sigma_limit)
        return state.replace(mean=mean, sigma=sigma, opt_state=opt_state)
