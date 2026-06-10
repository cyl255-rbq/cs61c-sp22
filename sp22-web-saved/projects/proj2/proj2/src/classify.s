.globl classify

.text
# =====================================
# COMMAND LINE ARGUMENTS
# =====================================
# Args:
#   a0 (int)        argc
#   a1 (char**)     argv
#   a1[1] (char*)   pointer to the filepath string of m0
#   a1[2] (char*)   pointer to the filepath string of m1
#   a1[3] (char*)   pointer to the filepath string of input matrix
#   a1[4] (char*)   pointer to the filepath string of output file
#   a2 (int)        silent mode, if this is 1, you should not print
#                   anything. Otherwise, you should print the
#                   classification and a newline.
# Returns:
#   a0 (int)        Classification
# Exceptions:
#   - If there are an incorrect number of command line args,
#     this function terminates the program with exit code 31
#   - If malloc fails, this function terminates the program with exit code 26
#
# Usage:
#   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>
classify:
    li t0, 5
    bne a0, t0, error_arguments
    addi sp, sp -52
    sw ra, 0(sp)
    sw s0, 4(sp)#h
    sw s1, 8(sp)#pointer argv
    sw s2, 12(sp)#print
    sw s3, 16(sp)#pointer m0 filename
    sw s4, 20(sp)#pointer m1 filename
    sw s5, 24(sp)#pointer input filename
    sw s7, 28(sp)#m0 row pointer
    sw s8, 32(sp)#m0 column pointer
    sw s9, 36(sp)#m1 row pointer
    sw s10, 40(sp)#m1 column pointer
    sw s6, 44(sp)#input row pointer
    sw s11, 48(sp)#input column pointer
    mv s1, a1
    mv s2, a2
	# Read pretrained m0
    li a0, 4
    jal ra malloc
    beq a0, x0, error_malloc
    mv s7, a0
    li a0, 4
    jal ra malloc
    beq a0, x0, error_malloc
    mv s8, a0
    lw s3, 4(s1)
    mv a0, s3
    mv a1, s7
    mv a2, s8
    jal ra, read_matrix
    mv s3, a0#pointer memory m0 
	# Read pretrained m1
    li a0, 4
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s9, a0
    li a0, 4
    jal ra malloc
    beq a0, x0, error_malloc
    mv s10, a0
    lw s4, 8(s1)
    mv a0, s4
    mv a1, s9
    mv a2, s10
    jal ra, read_matrix
    mv s4, a0#pointer memory m1
	# Read input matrix
    li a0, 4
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s6, a0
    li a0, 4
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s11, a0
    lw s5, 12(s1)
    mv a0, s5
    mv a1, s6
    mv a2, s11
    jal ra read_matrix
    mv s5, a0#pointer memory input
	# Compute h = matmul(m0, input)
    lw t2, 0(s7)
    lw t3, 0(s11)
    mul t0, t2, t3
    li t1, 4
    mul a0, t0, t1
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s0, a0#pointer memory h
    mv a0, s3
    lw a1, 0(s7)
    lw a2, 0(s8)
    mv a3, s5
    lw a4, 0(s6)
    lw a5, 0(s11)
    mv a6, s0
    jal ra, matmul
    # free m0
    mv a0, s3
    jal ra, free
    lw s3, 0(s7)#h row
    mv a0, s7
    jal ra, free
    mv a0, s8
    jal ra, free
    # free input
    mv a0, s5
    jal ra, free
    lw s5, 0(s11)#h col
    mv a0, s6
    jal ra, free
    mv a0, s11
    jal ra, free
	# Compute h = relu(h)
    mul a1, s3, s5
    mv a0, s0
    jal ra, relu
	# Compute o = matmul(m1, h)
    lw t2, 0(s9)
    mul t0, t2, s5
    li t1, 4
    mul a0, t1, t0
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s11, a0#pointer memory o
    mv a0, s4
    lw a1, 0(s9)
    lw a2, 0(s10)
    mv a3, s0
    mv a4, s3
    mv a5, s5
    mv a6, s11
    jal ra, matmul
    # free m1
    mv a0, s4
    jal ra, free
    lw s4, 0(s9)#o row
    mv a0, s9
    jal ra, free
    mv a0, s10
    jal ra, free
    # free h
    mv a0, s0
    jal ra, free
	# Write output matrix o
    lw a0, 16(s1)
    mv a1, s11
    mv a2, s4
    mv a3, s5
    jal ra, write_matrix
	# Compute and return argmax(o)
    mv a0, s11
    mul a1, s4, s5
    jal ra, argmax
    mv s0, a0
    # free o
    mv a0, s11
    jal ra, free
	# If enabled, print argmax(o) and newline
    beq s2, x0, print
return:    
    mv a0, s0
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    lw s7, 28(sp)
    lw s8, 32(sp)
    lw s9, 36(sp)
    lw s10, 40(sp)
    lw s6, 44(sp)
    lw s11, 48(sp)
    addi sp, sp 52
	ret
error_malloc:
    li a0, 26
    j exit
error_arguments:
    li a0, 31
    j exit
print:
    mv a0, s0
    jal ra, print_int
    li a0, '\n'
    jal ra, print_char
    j return
    