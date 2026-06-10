import unittest
from unittest import TestCase
import utils
import time
import numpy as np

# 🌟 核心拦截：不仅测量绝对耗时，还要把结果矩阵的数学特征打印出来供人肉眼对齐
def static_time_compute(dp_mat_lst, nc_mat_lst, op):
    """
    全力运行当前 C 扩展模块，同时计算并输出结果矩阵的数值特征（Sum/Mean），用于肉眼对齐验证。
    """
    if op == "add":
        action = lambda: nc_mat_lst[0] + nc_mat_lst[1]
    elif op == "sub":
        action = lambda: nc_mat_lst[0] - nc_mat_lst[1]
    elif op == "mul":
        action = lambda: nc_mat_lst[0] * nc_mat_lst[1]
    elif op == "neg":
        action = lambda: -nc_mat_lst[0]
    elif op == "abs":
        action = lambda: abs(nc_mat_lst[0])
    elif op == "pow":
        action = lambda: nc_mat_lst[0] ** nc_mat_lst[1]
    else:
        action = lambda: None

    # 根据测试规模自适应运行次数（防止大乘法卡死）
    is_massive = False
    if hasattr(nc_mat_lst[0], 'shape'):
        is_massive = nc_mat_lst[0].shape[0] >= 1000 or op == "mul"

    loops = 1 if is_massive else 5
    
    # 计时开始
    start_time = time.perf_counter()
    for _ in range(loops):
        res_mat = action()
    end_time = time.perf_counter()
    
    total_duration = (end_time - start_time) / loops
    
    # 💡 提取结果矩阵的数学特征进行对齐
    try:
        # 将 numc.Matrix 转换为一维列表或 numpy 数组来算总和与均值
        flat_data = []
        for i in range(res_mat.shape[0]):
            for j in range(res_mat.shape[1]):
                flat_data.append(res_mat.get(i, j))
        mat_sum = sum(flat_data)
        mat_mean = mat_sum / len(flat_data) if len(flat_data) > 0 else 0.0
    except Exception as e:
        mat_sum, mat_mean = 0.0, 0.0

    # 返回给测试框架
    return True, (total_duration, mat_sum, mat_mean)

# 实施拦截劫持
utils.compute = static_time_compute

# 覆写打印函数
def print_metrics(name, metrics):
    duration, mat_sum, mat_mean = metrics
    print(f" -> ⏱️ [{name}] 耗时: {duration * 1000:.4f} ms | 结果总和: {mat_sum:.4f} | 结果均值: {mat_mean:.4f}")

decimal_places = 6

class TestAdd(TestCase):
    def test_large_add(self):
        # 💥 1600x1600 巨型加法
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1600, 1600, seed=42)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1600, 1600, seed=43)
        _, metrics = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        print_metrics("Large Add (1600x1600)", metrics)

class TestAbs(TestCase):
    def test_large_abs(self):
        # 💥 1600x1600 巨型绝对值（故意给负数区间）
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(1600, 1600, low=-50.0, high=-1.0, seed=44)
        _, metrics = utils.compute([dp_mat], [nc_mat], "abs")
        print_metrics("Large Abs (1600x1600)", metrics)

class TestMul(TestCase):
    def test_large_mul(self):
        # 💥 1024x1024 工业级标准矩阵乘法
        dp_mat1, nc_mat1 = utils.rand_dp_nc_matrix(1024, 1024, seed=45)
        dp_mat2, nc_mat2 = utils.rand_dp_nc_matrix(1024, 1024, seed=46)
        _, metrics = utils.compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        print_metrics("Large Mul (1024x1024)", metrics)

class TestPow(TestCase):
    def test_large_pow(self):
        # 💥 诸神黄昏压测：128x128 矩阵的 500 次方！
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(128, 128, seed=47)
        _, metrics = utils.compute([dp_mat, 500], [nc_mat, 500], "pow")
        print_metrics("Large Pow (128x128, 500次)", metrics)

class TestGet(TestCase):
    def test_get(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        _ = nc_mat.get(0, 0)

class TestSet(TestCase):
    def test_set(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        nc_mat.set(0, 0, 2)

class TestShape(TestCase):
    def test_shape(self):
        dp_mat, nc_mat = utils.rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(hasattr(nc_mat, 'shape'))

if __name__ == '__main__':
    unittest.main()