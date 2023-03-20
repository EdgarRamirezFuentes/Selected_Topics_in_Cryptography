import math
from matplotlib import pyplot as plt

class EllipticCurve:
    """Class to represent an elliptic curve.

    Attributes:
        a (int): The a value of the equation.
        b (int): The b value of the equation.
        prime (int): The prime number.
        evaluation_results (list): Contains the evaluation results for the equation.
        quadratic_residues (set): Contains the quadratic residues for the prime.
        square_roots (dict): Contains the quadratic roots for each quadratic residue.
        curve_points (list): Contains the points on the curve.
    """

    def __init__(self, a: int, b: int, prime: int) -> None:
        """Initialize the EllipticCurve class.
        
        Args:
            a (int): The a value of the equation.
            b (int): The b value of the equation.
            prime (int): The prime number.
        """
        self.__a = a
        self.__b = b
        self.__prime = prime
        self.__evaluation_results = []
        self.__quadratic_residues = set()
        self.__square_roots = {}
        self.__curve_points = []

    def get_a(self) -> int:
        """Get the a value of the equation.

        Returns:
            int: The a value of the equation.
        """
        return self.__a
    
    def get_b(self) -> int:
        """Get the b value of the equation.

        Returns:
            int: The b value of the equation.
        """
        return self.__b
    
    def get_prime(self) -> int:
        """Get the prime number.

        Returns:
            int: The prime number.
        """
        return self.__prime
    
    def set_a(self, a: int) -> None:
        """Set the a value of the equation.

        Args:
            a (int): The a value of the equation.
        """
        self.__a = a
        self.__evaluation_results = []
        self.__quadratic_residues = set()
        self.__square_roots = {}

    def set_b(self, b: int) -> None:
        """Set the b value of the equation.

        Args:
            b (int): The b value of the equation.
        """
        self.__b = b
        self.__evaluation_results = []
        self.__quadratic_residues = set()
        self.__square_roots = {}

    def set_prime(self, prime: int) -> None:
        """Set the prime number.

        Args:
            prime (int): The prime number.
        """
        self.__prime = prime
        self.__evaluation_results = []
        self.__quadratic_residues = set()
        self.__square_roots = {}

    def get_evaluation_results(self) -> list:
        """Calculate and store the evaluation results for the equation.

        Returns:
            list: Contains the evaluation results for the equation.
        """
        if not self.__evaluation_results:
            self.__evaluation_results = [(x**3 + self.__a * x + self.__b) % self.__prime for x in range(self.__prime)]
        
        return self.__evaluation_results
    
    def get_quadratic_residues(self) -> set:
        """Calculate and store the quadratic residues for the prime.

        Returns:
            set: Contains the quadratic residues for the prime.
        """
        if not self.__quadratic_residues:
            self.__quadratic_residues = {(x**2) % self.__prime for x in range(1, self.__prime)}

        return self.__quadratic_residues
    
    def get_square_roots(self) -> dict:
        """Calculate and store the quadratic roots for each quadratic residue.

        Returns:
            dict: Contains the quadratic roots for each quadratic residue.
        """
        if not self.__square_roots:
            self.__square_roots = {x : [] for x in self.get_quadratic_residues()}
            for x in range(1, self.__prime):
                self.__square_roots[(x**2) % self.__prime].append(x)

        return self.__square_roots

    def get_curve_points(self) -> list:
        """Calculate the points on the curve.

        Returns:
            list: Contains the points on the curve.
        """
        if not self.__evaluation_results:
            self.get_evaluation_results()

        if not self.__curve_points:
            for i in range(0, self.__prime):
                evaluated_value = self.__evaluation_results[i]

                if evaluated_value in self.get_square_roots():
                    for root in self.__square_roots[evaluated_value]:
                        self.__curve_points.append((i, root))

            # Add the point at infinity
            self.__curve_points.append((math.inf, math.inf))

        return self.__curve_points
    
    def get_evaluation_table(self) -> str:
        """Get the evaluation table for the equation.

        Returns:
            str: The evaluation table for the equation.
        """
        if not self.__evaluation_results:
            self.get_evaluation_results()

        if not self.__square_roots:
            self.get_square_roots()

        table = f"a: {self.__a}, b: {self.__b}, prime: {self.__prime}\n"

        table += "|\tx\t|\tf(x)\t|\tQR\t|\tY\t|\n"

        for i in range(self.__prime):
            evaluated_value = self.__evaluation_results[i]
            table += f"|\t{i}\t|\t{evaluated_value}\t|\t{evaluated_value in self.__square_roots}\t|\t"
            table += "None\t|\n" if evaluated_value not in self.__square_roots else self.__square_roots[evaluated_value].__str__() + "\t|\n"
                   
        return table
    
    def plot_curve_points(self) -> None:
        """Plot the points on the curve."""
        if not self.__curve_points:
            self.get_curve_points()

        x_values = [x for x, y in self.__curve_points]
        y_values = [y for x, y in self.__curve_points]

        plt.title("Elliptic Curve")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.scatter(x_values, y_values)
        plt.show()
            

if __name__ == '__main__':
    curve = EllipticCurve(1, 6, 11)
    print(curve.get_evaluation_table())



