import unittest
from unittest import TestCase
import utils
import numpy as np
import time

# 🌟 终极强行汉化注入：彻底废除 utils 库原生的不靠谱随机数生成
def safe_static_matrix_generator(rows, cols, low=0, high=1, seed=0):
    import dumbpy as dp
    import numc as nc
    
    seed_offset = seed * 0.001
    raw_list = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # 制造带有丰富小数特征的非对称固定数据，防止乘法消去
            val = ((i + 1) * 0.13 + (j + 1) * 0.07 + seed_offset) % 2.0
            if low < 0 and high <= 0:
                val = -abs(val)
            row.append(val)
        raw_list.append(row)
        
    return dp.Matrix(raw_list), nc.Matrix(raw_list)

# 实施注入劫持
utils.rand_dp_nc_matrix = safe_static_matrix_generator

decimal_places = 4  # 大矩阵允许微小的浮点数累积误差

def print_speedup(name, rows, cols, speed_up):
    print(f" -> 💥 [{name}] ({rows}x{cols}) 提速比 (Speedup): {speed_up:.4f} 倍")

class TestAdd(TestCase):
    def test_small_add(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup("Small Add", 2, 2, speed_up)

    def test_medium_add(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(256, 256, seed=2)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(256, 256, seed=3)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup("Medium Add", 256, 256, speed_up)

    def test_large_add(self):
        # 🔥 压测：1600x1600 巨型加法
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1600, 1600, seed=4)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1600, 1600, seed=5)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup("Large Add", 1600, 1600, speed_up)

class TestSub(TestCase):
    def test_small_sub(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        print_speedup("Small Sub", 2, 2, speed_up)

    def test_medium_sub(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(256, 256, seed=6)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(256, 256, seed=7)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        print_speedup("Medium Sub", 256, 256, speed_up)

    def test_large_sub(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1600, 1600, seed=8)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1600, 1600, seed=9)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        print_speedup("Large Sub", 1600, 1600, speed_up)

class TestAbs(TestCase):
    def test_small_abs(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, low=-10.0, high=-1.0, seed=0)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup("Small Abs", 2, 2, speed_up)

    def test_medium_abs(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(256, 256, low=-50.0, high=-1.0, seed=10)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup("Medium Abs", 256, 256, speed_up)

    def test_large_abs(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(1600, 1600, low=-100.0, high=-1.0, seed=11)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup("Large Abs", 1600, 1600, speed_up)

class TestNeg(TestCase):
    def test_small_neg(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup("Small Neg", 2, 2, speed_up)

    def test_medium_neg(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(256, 256, seed=12)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup("Medium Neg", 256, 256, speed_up)

    def test_large_neg(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(1600, 1600, seed=13)
        is_correct, speed_up = utils.compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup("Large Neg", 1600, 1600, speed_up)

class TestMul(TestCase):
    def test_small_mul(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup("Small Mul", 2, 2, speed_up)

    def test_medium_mul(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(128, 128, seed=14)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(128, 128, seed=15)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup("Medium Mul", 128, 128, speed_up)

    def test_large_mul(self):
        # 🔥 压测：从 500 提到 800x800 乘法！让 $O(N^3)$ 彻底惩罚纯 Python
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(800, 800, seed=16)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(800, 800, seed=17)
        is_correct, speed_up = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup("Large Mul", 800, 800, speed_up)

class TestPow(TestCase):
    def test_small_pow(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = utils.compute([dp_mat, 3], [nc_mat, 3], "pow")
        self.assertTrue(is_correct)
        print_speedup("Small Pow", 2, 2, speed_up)

    def test_medium_pow(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(4, 4, seed=18)
        is_correct, speed_up = utils.compute([dp_mat, 0], [nc_mat, 0], "pow")
        self.assertTrue(is_correct)
        print_speedup("Medium Pow (0次)", 4, 4, speed_up)

    def test_large_pow(self):
        # 🔥 诸神黄昏压测：将 16x16 25次方，提升到 64x64 矩阵的 120 次方！
        # 纯 Python 的 dumbpy 需要硬连乘 119 次，每次都是 64x64 的矩阵乘法
        # 你的 C 语言快速幂只需要做不到 8 次矩阵乘法！
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(64, 64, seed=19)
        is_correct, speed_up = utils.compute([dp_mat, 120], [nc_mat, 120], "pow")
        self.assertTrue(is_correct)
        print_speedup("Large Pow (120次)", 64, 64, speed_up)

class TestGet(TestCase):
    def test_get(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertEqual(round(dp_mat.get(1, 1), decimal_places),
            round(nc_mat.get(1, 1), decimal_places))

class TestSet(TestCase):
    def test_set(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat.set(1, 1, 2.0)
        nc_mat.set(1, 1, 2.0)
        self.assertTrue(utils.cmp_dp_nc_matrix(dp_mat, nc_mat))

class TestShape(TestCase):
    def test_shape(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(dp_mat.shape == nc_mat.shape)

class TestIndexGet(TestCase):
    def test_index_get(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertEqual(round(dp_mat[1][1], decimal_places),
            round(nc_mat[1][1], decimal_places))

class TestIndexSet(TestCase):
    def test_set(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat[1][1] = 2.0
        nc_mat[1][1] = 2.0
        self.assertTrue(utils.cmp_dp_nc_matrix(dp_mat, nc_mat))

class TestSlice(TestCase):
    def test_slice(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertEqual(dp_mat[0].shape[1], nc_mat[0].shape[1])
        self.assertTrue(utils.cmp_dp_nc_matrix(dp_mat[0], nc_mat[0]))

class TestInvalidDimensions(TestCase):
    def test_invalid_dims(self):
        import numc as nc
        try:
            nc.Matrix(0, 5)
            self.assertTrue(False)
        except ValueError:
            pass

if __name__ == '__main__':
    unittest.main()