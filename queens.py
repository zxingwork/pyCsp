from csp import CSP, Constraint
from typing import *



if __name__ == '__main__':
    columns = [1, 2, 3, 4, 5, 6, 7, 8]
    rows = {}
    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]

    csp = CSP(columns, rows)








# 解析出来的width为字符串表达式