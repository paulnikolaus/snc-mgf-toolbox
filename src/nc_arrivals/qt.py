"""Typical Queueing Theory Processes"""

from math import exp, log
from abc import abstractmethod

from nc_arrivals.arrival_distribution import ArrivalDistribution
from utils.exceptions import ParameterOutOfBounds


class IID(ArrivalDistribution):
    """Abstract class for arrival processes that are of
        iid."""

    def sigma(self, theta=0.0) -> float:
        """

        :param theta: mgf parameter
        :return:      sigma(theta)
        """
        return 0.0

    @abstractmethod
    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        pass

    def is_discrete(self) -> bool:
        """
        :return True if the arrival distribution is discrete, False if not
        """
        return True

    @abstractmethod
    def average_rate(self) -> float:
        pass

    @abstractmethod
    def to_value(self, number=1, show_n=False) -> str:
        pass


class DM1(IID):
    """Corresponds to D/M/1 queue."""

    def __init__(self, lamb: float, n=1) -> None:
        self.lamb = lamb
        self.n = n

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        if theta >= self.lamb:
            raise ParameterOutOfBounds(
                f"theta = {theta} must be < lambda = {self.lamb}")

        return (self.n / theta) * log(self.lamb / (self.lamb - theta))

    def average_rate(self) -> float:
        return self.n / self.lamb

    def __str__(self) -> str:
        return f"D/M/1_lambda={self.lamb}_n={self.n}"

    def to_value(self, number=1, show_n=False) -> str:
        if show_n:
            return "lambda{0}={1}_n{0}={2}".format(str(number), str(self.lamb),
                                                   str(self.n))
        else:
            return "lambda{0}={1}".format(str(number), str(self.lamb))


class MD1(ArrivalDistribution):
    """Corresponds to M/D/1 queue."""

    def __init__(self, lamb: float, mu: float, n=1) -> None:
        self.lamb = lamb
        self.mu = mu
        self.n = n

    def sigma(self, theta=0.0) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        return (self.n / theta) * self.lamb * (exp(theta / self.mu) - 1)

    def is_discrete(self) -> bool:
        return False

    def average_rate(self):
        return self.n * self.lamb / self.mu

    def __str__(self) -> str:
        return f"M/D/1_lambda={self.lamb}_mu={self.mu}_n={self.n}"

    def to_value(self, number=1, show_n=False) -> str:
        if show_n:
            return "lambda{0}={1}_mu{0}={2}_n{0}={3}".format(
                str(number), str(self.lamb), str(self.mu), str(self.n))
        else:
            return "lambda{0}={1}_mu{0}={2}".format(str(number),
                                                    str(self.lamb),
                                                    str(self.mu))


class MM1(ArrivalDistribution):
    """Corresponds to M/M/1 queue."""

    def __init__(self, lamb: float, mu: float, n=1) -> None:
        self.lamb = lamb
        self.mu = mu
        self.n = n

    def sigma(self, theta=0.0) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        if theta >= self.mu:
            raise ParameterOutOfBounds(f"theta = {theta} must"
                                       f"be < mu = {self.mu}")

        return self.n * self.lamb / (self.mu - theta)

    def is_discrete(self) -> bool:
        return False

    def average_rate(self):
        return self.n * self.lamb / self.mu

    def __str__(self) -> str:
        return f"M/M/1_lambda={self.lamb}_mu={self.mu}_n={self.n}"

    def to_value(self, number=1, show_n=False) -> str:
        if show_n:
            return "lambda{0}={1}_mu{0}={2}_n{0}={3}".format(
                str(number), str(self.lamb), str(self.mu), str(self.n))
        else:
            return "lambda{0}={1}_mu{0}={2}".format(str(number),
                                                    str(self.lamb),
                                                    str(self.mu))


class DPoisson1(IID):
    """Corresponds to D/Poisson/1 queue."""

    def __init__(self, lamb: float, n=1) -> None:
        self.lamb = lamb
        self.n = n

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        return (self.n / theta) * self.lamb * (exp(theta) - 1)

    def average_rate(self) -> float:
        return self.n * self.lamb

    def __str__(self) -> str:
        return f"Poisson_lambda={self.lamb}_n={self.n}"

    def to_value(self, number=1, show_n=False) -> str:
        if show_n:
            return "lambda{0}={1}_n{0}={2}".format(str(number), str(self.lamb),
                                                   str(self.n))
        else:
            return "lambda{0}={1}".format(str(number), str(self.lamb))
