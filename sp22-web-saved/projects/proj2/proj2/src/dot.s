.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int arrays
# Arguments:
#   a0 (int*) is the pointer to the start of arr0
#   a1 (int*) is the pointer to the start of arr1
#   a2 (int)  is the number of elements to use
#   a3 (int)  is the stride of arr0
#   a4 (int)  is the stride of arr1
# Returns:
#   a0 (int)  is the dot product of arr0 and arr1
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
#   - If the stride of either array is less than 1,
#     this function terminates the program with error code 37
# =======================================================
dot:
    li t0, 1
    blt a2, t0, error_len
    blt a3, t0, error_step
    blt a4, t0, error_step
	# Prologue
    addi sp, sp, -4
    sw ra, 0(sp)
    li t0, 0#count time
    li t1, 0#sum
    slli t2, a3, 2#a0 adress move
    slli t3, a4, 2#a1 adress move
loop_start:
    beq t0, a2, loop_end
    lw t4, 0(a0)
    lw t5, 0(a1)
    mul t6, t4, t5
    add t1, t1, t6
    add a0, a0, t2
    add a1, a1, t3
    addi t0, t0, 1
    j loop_start
loop_end:
    lw ra, 0(sp)
    addi sp, sp, 4
	# Epilogue
    mv a0, t1
	ret
error_len:
    li a0, 36
    j exit
error_step:
    li a0, 37
    j exit
    