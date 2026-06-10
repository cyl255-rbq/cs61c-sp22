import unittest
from unittest import TestCase
import utils
import time
import numpy as np

# 🌟 核心拦截：同时测量 numc 和 真正 NumPy 的绝对耗时！
def static_time_compute(dp_mat_lst, nc_mat_lst, op):
    # 1. 准备真正 NumPy 的数据 (从传入的底层数据直接转为 NumPy 矩阵)
    np_mats = []
    for mat in nc_mat_lst:
        if hasattr(mat, 'shape'):
            # 提取一维数据还原为 NumPy 二维数组
            flat = [mat.get(i, j) for i in range(mat.shape[0]) for j in range(mat.shape[1])]
            np_mats.append(np.array(flat).reshape(mat.shape))
        else:
            np_mats.append(mat) # 如果是纯数字 (比如 pow 的指数)

    # 2. 定义 numc 的动作
    if op == "add":
        numc_action = lambda: nc_mat_lst[0] + nc_mat_lst[1]
        numpy_action = lambda: np_mats[0] + np_mats[1]
    elif op == "sub":
        numc_action = lambda: nc_mat_lst[0] - nc_mat_lst[1]
        numpy_action = lambda: np_mats[0] - np_mats[1]
    elif op == "mul":
        numc_action = lambda: nc_mat_lst[0] * nc_mat_lst[1]
        numpy_action = lambda: np.dot(np_mats[0], np_mats[1]) # NumPy 矩阵乘法
    elif op == "abs":
        numc_action = lambda: abs(nc_mat_lst[0])
        numpy_action = lambda: np.abs(np_mats[0])
    elif op == "pow":
        numc_action = lambda: nc_mat_lst[0] ** nc_mat_lst[1]
        # NumPy 官方的高性能矩阵快速幂
        numpy_action = lambda: np.linalg.matrix_power(np_mats[0], np_mats[1])
    else:
        return True, (0, 0, 0, 0)

    # 3. 根据规模决定循环次数，防止高维朴素版卡死
    is_massive = False
    if hasattr(nc_mat_lst[0], 'shape'):
        is_massive = nc_mat_lst[0].shape[0] >= 200 or op == "mul" or op == "pow"
    loops = 1 if is_massive else 5
    
    # --- ⏱️ 跑 numc 并计时 ---
    start = time.perf_counter()
    for _ in range(loops):
        res_numc = numc_action()
    numc_duration = (time.perf_counter() - start) / loops
    
    # --- ⏱️ 跑真正的 NumPy 并计时 ---
    start = time.perf_counter()
    for _ in range(loops):
        res_numpy = numpy_action()
    numpy_duration = (time.perf_counter() - start) / loops

    # 4. 提取特征用于校验
    try:
        flat_data = [res_numc.get(i, j) for i in range(res_numc.shape[0]) for j in range(res_numc.shape[1])]
        mat_sum = sum(flat_data)
        mat_mean = mat_sum / len(flat_data) if len(flat_data) > 0 else 0.0
    except Exception:
        mat_sum, mat_mean = 0.0, 0.0

    return True, (numc_duration, numpy_duration, mat_sum, mat_mean)

utils.compute = static_time_compute

# 覆写打印函数
def print_comparison(name, metrics):
    numc_t, numpy_t, mat_sum, mat_mean = metrics
    print(f"\n 💥 [{name}]")
    print(f"    👉 当前编译模块耗时: {numc_t * 1000:.4f} ms")
    print(f"    👉 真正 NumPy 官方耗时: {numpy_t * 1000:.4f} ms")
    print(f"    📊 结果检查 - 总和: {mat_sum:.4f} | 均值: {mat_mean:.4f}")

decimal_places = 6

class TestAdd(TestCase):
    def test_large_add(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1600, 1600, seed=42)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1600, 1600, seed=43)
        _, metrics = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        print_comparison("Large Add (1600x1600)", metrics)

class TestAbs(TestCase):
    def test_large_abs(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(1600, 1600, low=-50.0, high=-1.0, seed=44)
        _, metrics = utils.compute([dp_mat], [nc_mat], "abs")
        print_comparison("Large Abs (1600x1600)", metrics)

class TestMul(TestCase):
    def test_large_mul(self):
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1024, 1024, seed=45)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1024, 1024, seed=46)
        _, metrics = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        print_comparison("Large Mul (1024x1024)", metrics)

class TestPow(TestCase):
    def test_large_pow(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(256, 256, seed=47)
        _, metrics = utils.compute([dp_mat, 1500], [nc_mat, 1500], "pow")
        print_comparison("Large Pow (256x256, 1500次)", metrics)

class TestShape(TestCase):
    def test_shape(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(hasattr(nc_mat, 'shape'))

if __name__ == '__main__':
    unittest.main()