class Matrix():
    '''описание матрицы'''
    def __init__(self):
        '''свойства матрицы'''
        self.data = []
        self.size = 0

    def input_size(self):
        size = int(input('Введите размерность матрицы:'))
        self.size = size
        for i in range(self.size):
            self.data.append([0]*size)


    def input_data(self):
        for i in range(self.size):
            for j in range(self.size):
                num = int(input(f"Введите значение ячейки: [{i}][{j}]"))
                self.data[i][j] = num

    def output_data(self):
        for i in range(self.size):
            st = f""
            for j in range(self.size):
                st += f"{self.data[i][j]: >5}"
            print(st)


matrix = Matrix()
matrix.input_size()
matrix.input_data()
matrix.output_data()