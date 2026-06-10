.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
#   - If malloc returns an error,
#     this function terminates the program with error code 26
#   - If you receive an fopen error or eof,
#     this function terminates the program with error code 27
#   - If you receive an fclose error or eof,
#     this function terminates the program with error code 28
#   - If you receive an fread error or eof,
#     this function terminates the program with error code 29
# ==============================================================================
read_matrix:
    addi sp, sp, -28
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)#file descriptor
    sw s4, 20(sp)#pointer allocated memory
    sw s5, 24(sp)#matrix byte size
	# Prologue
    mv s0, a0
    mv s1, a1
    mv s2, a2
    mv a0, s0
    li a1, 0
    jal ra fopen
    li t0 -1
    beq a0 t0 error_fopen
    mv s3, a0
    mv a0, s3
    mv a1, s1
    li a2, 4
    jal ra fread
    li t0, 4
    bne a0, t0, error_fread
    mv a0, s3
    mv a1, s2
    li a2, 4
    jal ra fread
    li t0, 4
    bne a0, t0, error_fread
    lw t0, 0(s1)
    lw t1, 0(s2)
    mul t3, t0, t1
    li t4, 4
    mul s5, t3, t4
    mv a0, s5
    jal ra, malloc
    beq a0, x0, error_malloc
    mv s4, a0
    mv a0, s3
    mv a1, s4
    mv a2, s5
    jal ra fread
    bne a0, s5, error_fread
    mv a0, s3
    jal ra, fclose
    li t0, -1
    beq a0, t0, error_fclose
    mv a0, s4
	# Epilogue
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s4, 20(sp)
    lw s5, 24(sp)
    addi sp, sp, 28
	ret
error_malloc:
    li a0, 26
    j exit
error_fopen:
    li a0, 27
    j exit
error_fclose:
    li a0, 28
    j exit
error_fread:
    li a0, 29
    j exit
