"""Abstract Leaky-Bucket class."""

from abc import abstractmethod
from math import exp, log

from utils.exceptions import ParameterOutOfBounds

from nc_arrivals.arrival_distribution import ArrivalDistribution


class RegulatedArrivals(ArrivalDistribution):
    """Abstract class for all leaky-bucket classes"""
    def __init__(self, sigma_single=0.0, rho_single=0.0, n=1) -> None:
        self.sigma_single = sigma_single
        self.rho_single = rho_single
        self.n = n
        self.arr_rate = n * rho_single

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """
        sigma(theta)
        :param theta: mgf parameter
        """
        pass

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        return self.n * self.rho_single

    def is_discrete(self) -> bool:
        """
        :return True if the arrival distribution is discrete, False if not
        """
        return True

    def average_rate(self) -> float:
        return self.rho(1.0)

    def to_value(self, number=1, show_n=True) -> str:
        """
        :return string
        """
        if show_n:
            return "sigma{0}={1}_rho{0}={2}_n{0}={3}".format(
                str(number), str(self.sigma_single), str(self.rho_single),
                str(self.n))
        else:
            return f"sigma={str(self.sigma_single)}_rho={str(self.rho_single)}"


class DetermTokenBucket(RegulatedArrivals):
    """Primitive TokenBucket (quasi deterministic and independent of theta)"""
    def __init__(self, sigma_single: float, rho_single: float, n=1) -> None:
        super().__init__(sigma_single=sigma_single, rho_single=rho_single, n=n)
        self.burst = self.n * self.sigma_single

    def sigma(self, theta: float) -> float:
        return self.n * self.sigma_single

    def __str__(self) -> str:
        return f"TBconst_sigma={self.sigma_single}_" \
            f"rho={self.rho_single}_n={self.n}"


class LeakyBucketMassoulie(RegulatedArrivals):
    """Leaky Bucket according to Massoulié using directly Lemma 2"""
    def __init__(self, sigma_single: float, rho_single: float, n=1) -> None:
        super().__init__(sigma_single=sigma_single, rho_single=rho_single, n=n)

    def sigma(self, theta: float) -> float:
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta={theta} must be > 0")

        return self.n * log(0.5 * (exp(theta * self.sigma_single) +
                                   exp(-theta * self.sigma_single))) / theta

    def __str__(self) -> str:
        return f"MassOne_sigma={self.sigma_single}_" \
            f"rho={self.rho_single}_n={self.n}"
