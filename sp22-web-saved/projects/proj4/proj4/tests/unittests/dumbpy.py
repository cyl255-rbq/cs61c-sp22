class Matrix:
    def __init__(self, *args, **kwargs):
        """
        完美锁定固定数据的伪造 dumbpy。
        彻底移除 random 依赖，增加下标索引魔法方法支持。
        """
        if len(args) == 1 and isinstance(args[0], list):
            # 1. 数组初始化
            self.data = [[float(x) for x in row] for row in args[0]]
            self.rows = len(self.data)
            self.cols = len(self.data[0]) if self.rows > 0 else 0
        elif len(args) >= 2:
            # 2. 维度初始化
            self.rows = args[0]
            self.cols = args[1]
            

            if kwargs.get('rand', False) or 'seed' in kwargs:
                # 拿 seed 作为一个微小的偏移量
                seed_offset = kwargs.get('seed', 0) * 0.001
                self.data = []
                for i in range(self.rows):
                    row = []
                    for j in range(self.cols):
                        # 构造非对称的、带小数的固定测试数据
                        val = (i + 1) * 0.5 + (j + 1) * 0.15 + seed_offset
                        row.append(val)
                    self.data.append(row)
            else:
                val = args[2] if len(args) > 2 else 0.0
                self.data = [[float(val) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            raise ValueError("Invalid arguments for Matrix initialization")

    @property
    def shape(self):
        return (self.rows, self.cols)

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, val):
        self.data[r][c] = float(val)

    # 🌟 核心兼容性修复：支持 dp_mat[rand_row][rand_col] 这种二维索引
    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    # --- 核心数学运算重载 ---
    def __add__(self, other):
        new_data = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(new_data)

    def __sub__(self, other):
        new_data = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(new_data)

    def __mul__(self, other):
        new_data = []
        for i in range(self.rows):
            row_res = []
            for j in range(other.cols):
                s = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row_res.append(s)
            new_data.append(row_res)
        return Matrix(new_data)

    def __pow__(self, p):
        if p == 0:
            new_data = [[1.0 if i == j else 0.0 for j in range(self.cols)] for i in range(self.rows)]
            return Matrix(new_data)
        res = Matrix([[x for x in row] for row in self.data])
        for _ in range(p - 1):
            res = res * self
        return res

    def __neg__(self):
        new_data = [[-self.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(new_data)

    def __abs__(self):
        new_data = [[abs(self.data[i][j]) for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(new_data)

    def __repr__(self):
        return f"Matrix({self.data})"