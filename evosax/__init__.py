from .strategy import Strategy
from .strategies import (
    Simple_GA,
    Simple_ES,
    CMA_ES,
    Differential_ES,
    PSO_ES,
    Open_ES,
    PGPE_ES,
    PBT_ES,
    Persistent_ES,
    xNES,
    Augmented_RS,
    Sep_CMA_ES,
)


Strategies = {
    "Simple_GA": Simple_GA,
    "Simple_ES": Simple_ES,
    "CMA_ES": CMA_ES,
    "Differential_ES": Differential_ES,
    "PSO_ES": PSO_ES,
    "Open_ES": Open_ES,
    "PGPE_ES": PGPE_ES,
    "PBT_ES": PBT_ES,
    "Persistent_ES": Persistent_ES,
    "xNES": xNES,
    "Augmented_RS": Augmented_RS,
    "Sep_CMA_ES": Sep_CMA_ES,
}

from .utils import FitnessShaper, ParameterReshaper, ESLog
from .networks import NetworkMapper
from .problems import ProblemMapper

__all__ = [
    "Strategy",
    "Simple_GA",
    "Simple_ES",
    "CMA_ES",
    "Differential_ES",
    "PSO_ES",
    "Open_ES",
    "PGPE_ES",
    "PBT_ES",
    "Persistent_ES",
    "xNES",
    "Augmented_RS",
    "Sep_CMA_ES",
    "Strategies",
    "FitnessShaper",
    "ParameterReshaper",
    "ESLog",
    "NetworkMapper",
    "ProblemMapper",
]
