# `evosax`: JAX-Based Evolution Strategies 🦎
[![Pyversions](https://img.shields.io/pypi/pyversions/evosax.svg?style=flat-square)](https://pypi.python.org/pypi/evosax) [![PyPI version](https://badge.fury.io/py/evosax.svg)](https://badge.fury.io/py/evosax)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/RobertTLange/evosax/branch/main/graph/badge.svg?token=5FUSX35KWO)](https://codecov.io/gh/RobertTLange/evosax)
[![Paper](http://img.shields.io/badge/paper-arxiv.2212.04180-B31B1B.svg)](http://arxiv.org/abs/2212.04180)
<a href="https://github.com/RobertTLange/evosax/blob/main/docs/logo.png?raw=true"><img src="https://github.com/RobertTLange/evosax/blob/main/docs/logo.png?raw=true" width="170" align="right" /></a>

Tired of having to handle asynchronous processes for neuroevolution? Do you want to leverage massive vectorization and high-throughput accelerators for evolution strategies (ES)? `evosax` allows you to leverage JAX, XLA compilation and auto-vectorization/parallelization to scale ES to your favorite accelerators. The API is based on the classical `ask`, `evaluate`, `tell` cycle of ES. Both `ask` and `tell` calls are compatible with `jit`, `vmap`/`pmap` and `lax.scan`. It includes a vast set of both classic (e.g. CMA-ES, Differential Evolution, etc.) and modern neuroevolution (e.g. OpenAI-ES, Augmented RS, etc.) strategies. You can get started here 👉 [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/00_getting_started.ipynb)

## Basic `evosax` API Usage 🍲

```python
import jax
from evosax import CMA_ES

# Instantiate the search strategy
rng = jax.random.PRNGKey(0)
strategy = CMA_ES(popsize=20, num_dims=2, elite_ratio=0.5)
es_params = strategy.default_params
state = strategy.initialize(rng, es_params)

# Run ask-eval-tell loop - NOTE: By default minimization!
for t in range(num_generations):
    rng, rng_gen, rng_eval = jax.random.split(rng, 3)
    x, state = strategy.ask(rng_gen, state, es_params)
    fitness = ...  # Your population evaluation fct 
    state = strategy.tell(x, fitness, state, es_params)

# Get best overall population member & its fitness
state.best_member, state.best_fitness
```

## Implemented Evolution Strategies 🦎

| Strategy | Reference | Import | Example |
| --- | --- | ---  | --- |
| OpenES | [Salimans et al. (2017)](https://arxiv.org/pdf/1703.03864.pdf) | [`OpenES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/open_es.py) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/03_cnn_mnist.ipynb)
| PGPE | [Sehnke et al. (2010)](https://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=A64D1AE8313A364B814998E9E245B40A?doi=10.1.1.180.7104&rep=rep1&type=pdf) | [`PGPE`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/pgpe.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/02_mlp_control.ipynb)
| ARS | [Mania et al. (2018)](https://arxiv.org/pdf/1803.07055.pdf) | [`ARS`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/ars.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/00_getting_started.ipynb)
| ESMC | [Merchant et al. (2021)](https://proceedings.mlr.press/v139/merchant21a.html) | [`ESMC`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/esmc.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Persistent ES | [Vicol et al. (2021)](http://proceedings.mlr.press/v139/vicol21a.html) | [`PersistentES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/persistent_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/04_lrate_pes.ipynb)
| xNES | [Wierstra et al. (2014)](https://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf) | [`XNES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/xnes.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| SNES | [Wierstra et al. (2014)](https://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf) | [`SNES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/sxnes.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| CR-FM-NES | [Nomura & Ono (2022)](https://arxiv.org/abs/2201.11422) | [`CR_FM_NES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/cr_fm_nes.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Guided ES | [Maheswaranathan et al. (2018)](https://arxiv.org/abs/1806.10230) | [`GuidedES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/guided_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| ASEBO | [Choromanski et al. (2019)](https://arxiv.org/abs/1903.04268) | [`ASEBO`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/asebo.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| CMA-ES | [Hansen & Ostermeier (2001)](http://www.cmap.polytechnique.fr/~nikolaus.hansen/cmaartic.pdf) | [`CMA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/cma_es.py) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Sep-CMA-ES | [Ros & Hansen (2008)](https://hal.inria.fr/inria-00287367/document) | [`Sep_CMA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/sep_cma_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| BIPOP-CMA-ES | [Hansen (2009)](https://hal.inria.fr/inria-00382093/document) | [`BIPOP_CMA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/bipop_cma_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/06_restart_es.ipynb)
| IPOP-CMA-ES | [Auer & Hansen (2005)](http://www.cmap.polytechnique.fr/~nikolaus.hansen/cec2005ipopcmaes.pdf) | [`IPOP_CMA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/ipop_cma_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/06_restart_es.ipynb)
| Full-iAMaLGaM | [Bosman et al. (2013)](https://tinyurl.com/y9fcccx2) | [`Full_iAMaLGaM`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/full_iamalgam.py)  |[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Independent-iAMaLGaM | [Bosman et al. (2013)](https://tinyurl.com/y9fcccx2) | [`Indep_iAMaLGaM`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/indep_iamalgam.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| MA-ES | [Bayer & Sendhoff (2017)](https://www.honda-ri.de/pubs/pdf/3376.pdf) | [`MA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/ma_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| LM-MA-ES | [Loshchilov et al. (2017)](https://arxiv.org/pdf/1705.06693.pdf) | [`LM_MA_ES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/lm_ma_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| RmES | [Li & Zhang (2017)](https://ieeexplore.ieee.org/document/8080257) | [`RmES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/rm_es.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Simple Genetic | [Such et al. (2017)](https://arxiv.org/abs/1712.06567) | [`SimpleGA`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/simple_ga.py) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| SAMR-GA | [Clune et al. (2008)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000187) | [`SAMR_GA`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/samr_ga.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| GESMR-GA | [Kumar et al. (2022)](https://arxiv.org/abs/2204.04817) | [`GESMR_GA`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/gesmr_ga.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| MR15-GA | [Rechenberg (1978)](https://link.springer.com/chapter/10.1007/978-3-642-81283-5_8) | [`MR15_GA`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/mr15_ga.py) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Simple Gaussian | [Rechenberg (1978)](https://link.springer.com/chapter/10.1007/978-3-642-81283-5_8) | [`SimpleES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/simple_es.py) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| DES | [Lange et al. (2023)](https://arxiv.org/abs/2211.11260) | [`DES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/des.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| LES | [Lange et al. (2023)](https://arxiv.org/abs/2211.11260) | [`LES`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/les.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Particle Swarm Optimization | [Kennedy & Eberhart (1995)](https://ieeexplore.ieee.org/document/488968) | [`PSO`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/pso.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Differential Evolution | [Storn & Price (1997)](https://www.metabolic-economics.de/pages/seminar_theoretische_biologie_2007/literatur/schaber/Storn1997JGlobOpt11.pdf) | [`DE`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/de.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| GLD | [Golovin et al. (2019)](https://arxiv.org/pdf/1911.06317.pdf) | [`GLD`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/gld.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Simulated Annealing | [Rasdi Rere et al. (2015)](https://www.sciencedirect.com/science/article/pii/S1877050915035759) | [`SimAnneal`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/sim_anneal.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb)
| Population-Based Training | [Jaderberg et al. (2017)](https://arxiv.org/abs/1711.09846) | [`PBT`](https://github.com/RobertTLange/evosax/tree/main/evosax/strategies/pbt.py)  | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/evosax/blob/main/examples/05_quadratic_pbt.ipynb)





## Installation ⏳

The latest `evosax` release can directly be installed from PyPI:

```
pip install evosax
```

If you want to get the most recent commit, please install directly from the repository:

```
pip install git+https://github.com/RobertTLange/evosax.git@main
```

In order to use JAX on your accelerators, you can find more details in the [JAX documentation](https://github.com/google/jax#installation).

## Examples 📖
* 📓 [Classic ES Tasks](https://github.com/RobertTLange/evosax/blob/main/examples/01_classic_benchmark.ipynb): API introduction on Rosenbrock function (CMA-ES, Simple GA, etc.).
* 📓 [CartPole-Control](https://github.com/RobertTLange/evosax/blob/main/examples/02_mlp_control.ipynb): OpenES & PEPG on the `CartPole-v1` gym task (MLP/LSTM controller).
* 📓 [MNIST-Classifier](https://github.com/RobertTLange/evosax/blob/main/examples/03_cnn_mnist.ipynb): OpenES on MNIST with CNN network.
* 📓 [LRateTune-PES](https://github.com/RobertTLange/evosax/blob/main/examples/04_lrate_pes.ipynb): Persistent ES on meta-learning problem as in [Vicol et al. (2021)](http://proceedings.mlr.press/v139/vicol21a.html).
* 📓 [Quadratic-PBT](https://github.com/RobertTLange/evosax/blob/main/examples/05_quadratic_pbt.ipynb): PBT on toy quadratic problem as in [Jaderberg et al. (2017)](https://arxiv.org/abs/1711.09846).
* 📓 [Restart-Wrappers](https://github.com/RobertTLange/evosax/blob/main/examples/06_restart_es.ipynb): Custom restart wrappers as e.g. used in (B)IPOP-CMA-ES.
* 📓 [Brax Control](https://github.com/RobertTLange/evosax/blob/main/examples/07_brax_control.ipynb): Evolve Tanh MLPs on Brax tasks using the `EvoJAX` wrapper.
* 📓 [BBOB Visualizer](https://github.com/RobertTLange/evosax/blob/main/examples/08_bbo_visualizer.ipynb): Visualize evolution rollouts on 2D fitness landscapes.

## Key Features 💵

- **Strategy Diversity**: `evosax` implements more than 30 classical and modern neuroevolution strategies. All of them follow the same simple `ask`/`eval` API and come with tailored tools such as the [ClipUp](https://arxiv.org/abs/2008.02387) optimizer, parameter reshaping into PyTrees and fitness shaping (see below).

- **Vectorization/Parallelization of `ask`/`tell` Calls**: Both `ask` and `tell` calls can leverage `jit`, `vmap`/`pmap`. This enables vectorized/parallel rollouts of different evolution strategies.

```Python
from evosax.strategies.ars import ARS, EvoParams
# E.g. vectorize over different initial perturbation stds
strategy = ARS(popsize=100, num_dims=20)
es_params = EvoParams(sigma_init=jnp.array([0.1, 0.01, 0.001]), sigma_decay=0.999, ...)

# Specify how to map over ES hyperparameters 
map_dict = EvoParams(sigma_init=0, sigma_decay=None, ...)

# Vmap-composed batch initialize, ask and tell functions 
batch_init = jax.vmap(strategy.init, in_axes=(None, map_dict))
batch_ask = jax.vmap(strategy.ask, in_axes=(None, 0, map_dict))
batch_tell = jax.vmap(strategy.tell, in_axes=(0, 0, 0, map_dict))
```

- **Scan Through Evolution Rollouts**: You can also `lax.scan` through entire `init`, `ask`, `eval`, `tell` loops for fast compilation of ES loops:

```Python
@partial(jax.jit, static_argnums=(1,))
def run_es_loop(rng, num_steps):
    """Run evolution ask-eval-tell loop."""
    es_params = strategy.default_params
    state = strategy.initialize(rng, es_params)

    def es_step(state_input, tmp):
        """Helper es step to lax.scan through."""
        rng, state = state_input
        rng, rng_iter = jax.random.split(rng)
        x, state = strategy.ask(rng_iter, state, es_params)
        fitness = ...
        state = strategy.tell(y, fitness, state, es_params)
        return [rng, state], fitness[jnp.argmin(fitness)]

    _, scan_out = jax.lax.scan(es_step,
                               [rng, state],
                               [jnp.zeros(num_steps)])
    return jnp.min(scan_out)
```

- **Population Parameter Reshaping**: We provide a `ParamaterReshaper` wrapper to reshape flat parameter vectors into PyTrees. The wrapper is compatible with JAX neural network libraries such as Flax/Haiku and makes it easier to afterwards evaluate network populations.

```Python
from flax import linen as nn
from evosax import ParameterReshaper

class MLP(nn.Module):
    num_hidden_units: int
    ...

    @nn.compact
    def __call__(self, obs):
        ...
        return ...

network = MLP(64)
net_params = network.init(rng, jnp.zeros(4,), rng)

# Initialize reshaper based on placeholder network shapes
param_reshaper = ParameterReshaper(net_params)

# Get population candidates & reshape into stacked pytrees
x = strategy.ask(...)
x_shaped = param_reshaper.reshape(x)
```


- **Flexible Fitness Shaping**: By default `evosax` assumes that the fitness objective is to be minimized. If you would like to maximize instead, perform rank centering, z-scoring or add weight regularization you can use the `FitnessShaper`: 

```Python
from evosax import FitnessShaper

# Instantiate jittable fitness shaper (e.g. for Open ES)
fit_shaper = FitnessShaper(centered_rank=True,
                           z_score=False,
                           weight_decay=0.01,
                           maximize=True)

# Shape the evaluated fitness scores
fit_shaped = fit_shaper.apply(x, fitness) 
```
<details>
  <summary>Additonal Work-In-Progress</summary>
    **Strategy Restart Wrappers**: *Work-in-progress*. You can also choose from a set of different restart mechanisms, which will relaunch a strategy (with e.g. new population size) based on termination criteria. Note: For all restart strategies which alter the population size the ask and tell methods will have to be re-compiled at the time of change. Note that all strategies can also be executed without explicitly providing `es_params`. In this case the default parameters will be used.

    ```Python
    from evosax import CMA_ES
    from evosax.restarts import BIPOP_Restarter

    # Define a termination criterion (kwargs - fitness, state, params)
    def std_criterion(fitness, state, params):
        """Restart strategy if fitness std across population is small."""
        return fitness.std() < 0.001

    # Instantiate Base CMA-ES & wrap with BIPOP restarts
    # Pass strategy-specific kwargs separately (e.g. elite_ration or opt_name)
    strategy = CMA_ES(num_dims, popsize, elite_ratio)
    re_strategy = BIPOP_Restarter(
                    strategy,
                    stop_criteria=[std_criterion],
                    strategy_kwargs={"elite_ratio": elite_ratio}
                )
    state = re_strategy.initialize(rng)

    # ask/tell loop - restarts are automatically handled 
    rng, rng_gen, rng_eval = jax.random.split(rng, 3)
    x, state = re_strategy.ask(rng_gen, state)
    fitness = ...  # Your population evaluation fct 
    state = re_strategy.tell(x, fitness, state)
    ```

    - **Batch Strategy Rollouts**: *Work-in-progress*. We are currently also working on different ways of incorporating multiple subpopulations with different communication protocols.

    ```Python
    from evosax.experimental.subpops import BatchStrategy

    # Instantiates 5 CMA-ES subpops of 20 members
    strategy = BatchStrategy(
            strategy_name="CMA_ES",
            num_dims=4096,
            popsize=100,
            num_subpops=5,
            strategy_kwargs={"elite_ratio": 0.5},
            communication="best_subpop",
        )

    state = strategy.initialize(rng)
    # Ask for evaluation candidates of different subpopulation ES
    x, state = strategy.ask(rng_iter, state)
    fitness = ...
    state = strategy.tell(x, fitness, state)
    ```

    - **Indirect Encodings**: *Work-in-progress*. ES can struggle with high-dimensional search spaces (e.g. due to harder estimation of covariances). One potential way to alleviate this challenge, is to use indirect parameter encodings in a lower dimensional space. So far we provide JAX-compatible encodings with random projections (Gaussian/Rademacher) and Hypernetworks for MLPs. They act as drop-in replacements for the `ParameterReshaper`:

    ```Python
    from evosax.experimental.decodings import RandomDecoder, HyperDecoder

    # For arbitrary network architectures / search spaces
    num_encoding_dims = 6
    param_reshaper = RandomDecoder(num_encoding_dims, net_params)
    x_shaped = param_reshaper.reshape(x)

    # For MLP-based models we also support a HyperNetwork en/decoding
    reshaper = HyperDecoder(
            net_params,
            hypernet_config={
                "num_latent_units": 3,  # Latent units per module kernel/bias
                "num_hidden_units": 2,  # Hidden dimensionality of a_i^j embedding
            },
        )
    x_shaped = param_reshaper.reshape(x)
    ```
</details>


## Resources & Other Great JAX-ES Tools 📝
* 📺 [Rob's MLC Research Jam Talk](https://www.youtube.com/watch?v=Wn6Lq2bexlA&t=51s): Small motivation talk at the ML Collective Research Jam.
* 📝 [Rob's 02/2021 Blog](https://roberttlange.github.io/posts/2021/02/cma-es-jax/): Tutorial on CMA-ES & leveraging JAX's primitives.
* 💻 [Evojax](https://github.com/google/evojax): JAX-ES library by Google Brain with great rollout wrappers.
* 💻 [QDax](https://github.com/adaptive-intelligent-robotics/QDax): Quality-Diversity algorithms in JAX.

## Acknowledgements & Citing `evosax` ✏️

If you use `evosax` in your research, please cite the following [paper](https://arxiv.org/abs/2212.04180):

```
@article{evosax2022github,
  author = {Robert Tjarko Lange},
  title = {evosax: JAX-based Evolution Strategies},
  journal={arXiv preprint arXiv:2212.04180},
  year = {2022},
}
```

We acknowledge financial support by the [Google TRC](https://sites.research.google/trc/about/) and the Deutsche
Forschungsgemeinschaft (DFG, German Research Foundation) under Germany's Excellence Strategy - EXC 2002/1 ["Science of Intelligence"](https://www.scienceofintelligence.de/) - project number 390523135.

## Development 👷

You can run the test suite via `python -m pytest -vv --all`. If you find a bug or are missing your favourite feature, feel free to create an issue and/or start [contributing](CONTRIBUTING.md) 🤗.

## Disclaimer ⚠️

This repository contains an independent reimplementation of LES and DES based on the corresponding ICLR 2023 publication [(Lange et al., 2023)](https://arxiv.org/abs/2211.11260). It is unrelated to Google or DeepMind. The implementation has been tested to roughly reproduce the official results on a range of tasks.