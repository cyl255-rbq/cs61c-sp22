# 测试正数立即数
addi t0, x0, 500     # t0 = 500
# 测试负数立即数 (关键：检查符号扩展)
# 如果符号扩展坏了，t1 会变成 0x00000FFF (4095) 而不是 -1
addi t1, x0, -1      # t1 = 0xFFFFFFFF
# 测试 SLTI (Set Less Than Immediate)
slti t2, t1, 0       # t2 = (-1 < 0) ? 1 : 0 -> 应为 1
slti s0, t0, 0       # s0 = (500 < 0) ? 1 : 0 -> 应为 0

# 测试逻辑右移 SRLI vs 算术右移 SRAI
addi s1, x0, -10     # s1 = 0xFFFFFFF6
srli a0, s1, 4       # a0 = 0x0FFFFFFF (高位补0)
srai a0, s1, 4       # a0 = 0xFFFFFFFF (高位补符号位)