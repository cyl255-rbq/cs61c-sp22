.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
#   - If you receive an fopen error or eof,
#     this function terminates the program with error code 27
#   - If you receive an fclose error or eof,
#     this function terminates the program with error code 28
#   - If you receive an fwrite error or eof,
#     this function terminates the program with error code 30
# ==============================================================================
write_matrix:
    addi sp, sp, -28
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)#file descriptor
    sw s3, 16(sp)
    sw s4, 20(sp)
    sw s5, 24(sp)
	# Prologue
    mv s0, a0
    mv s1, a1
    lw s3, 0(s1)
    lw s4, 4(s1)
    sw a2, 0(s1)
    sw a3, 4(s1)
    mul s5, a2, a3
    mv a0, s0
    li a1, 1
    jal ra, fopen
    li t0, -1
    beq a0 t0 error_fopen
    mv s2, a0
    mv a0, s2
    mv a1, s1
    li a2, 2
    li a3, 4
    jal ra, fwrite
    li t0, 2
    bne a0, t0, error_fwrite
    sw, s3, 0(s1)
    sw, s4, 4(s1)
    mv a0, s2
    mv a1, s1
    mv a2, s5
    li a3, 4
    jal ra fwrite
    bne a0, s5, error_fwrite
    mv a0, s2
    jal ra, fclose
    li t0, -1
    beq a0, t0, error_fclose
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
error_fopen:
    li a0, 27
    j exit
error_fclose:
    li a0, 28
    j exit
error_fwrite:
    li a0, 30
    j exit
