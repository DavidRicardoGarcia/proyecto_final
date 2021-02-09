class jobs:

    def __init__(self,j,o,i):
        self.job=j
        self.ope=o
        self.index=i

mymatrix=[[1,2,9],[4,9,6],[7,8,9]]
val = 9
[(index, row.index(val)) for index, row in enumerate(mymatrix) if val in row]