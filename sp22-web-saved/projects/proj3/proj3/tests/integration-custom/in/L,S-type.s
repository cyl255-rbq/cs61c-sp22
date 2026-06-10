# 准备基地址和测试数据
addi t0, x0, 1024    # t0 = 0x400 (基地址，大于 0x3E8)
addi t1, x0, -1      # t1 = 0xFFFFFFFF (测试数据)

# 测试 SW 和 LW
sw t1, 0(t0)         # 把 -1 存入内存 0x400
addi t2, x0, 0       # 清空 t2
lw t2, 0(t0)         # 从 0x400 读回 t2，t2 应为 -1

# 测试 SB 和 LB (最容易出错的地方)
addi s0, x0, 0x7B    # s0 = 123
sb s0, 4(t0)         # 存一个字节到 0x404
lb a0, 4(t0)         # 有符号读回，s1 仍应为 123 (0x7B)

# 测试符号扩展的 LB
addi s0, x0, 0xFF    # s0 = 255 (作为字节是 -1)
sb s0, 8(t0)
lb a0, 8(t0)         # a0 应为 0xFFFFFFFF (-1)