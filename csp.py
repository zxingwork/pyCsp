from typing import *
from abc import ABC, abstractmethod

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# base class for all constrains
class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, D]):
        self.variables = variables
        self.domains: Dict[V, D] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}

        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable is not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D]=None):
        if assignment is None:
            assignment = {}

        if len(assignment) == self.constraints:
            return assignment

        unsigned: List[V] = [i for i in self.variables if i not in assignment]
        local = unsigned[0]
        for value in self.domains[local]:
            local_assignment = assignment.copy()
            local_assignment.update({local: value})
            if self.consistent(local, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None

