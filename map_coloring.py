from csp import CSP, Constraint
from typing import *


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str):
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True

        return assignment[self.place1] != assignment[self.place2]


if __name__ == '__main__':
    variables: List[str] = ["WesternAustralia", "NorthernTerritory", "SouthAustralia", "Queensland", "NewSouthWales",
                            "Victoria", "Tasmania"]

    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ['red', 'green', 'blue']

    csp = CSP(variables=variables, domains=domains)
    csp.add_constraint(MapColoringConstraint("WesternAustralia", "NorthernTerritory"))
    csp.add_constraint(MapColoringConstraint("WesternAustralia", "SouthAustralia"))
    csp.add_constraint(MapColoringConstraint("SouthAustralia", "NorthernTerritory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "NorthernTerritory"))
    csp.add_constraint(MapColoringConstraint("Queensland", "SouthAustralia"))
    csp.add_constraint(MapColoringConstraint("Queensland", "NewSouthWales"))
    csp.add_constraint(MapColoringConstraint("NewSouthWales", "SouthAustralia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "SouthAustralia"))
    csp.add_constraint(MapColoringConstraint("Victoria", "NewSouthWales"))
    csp.add_constraint(MapColoringConstraint("Victoria", "Tasmania"))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if not solution:
        print('no solution found!')

    else:
        print(solution)
