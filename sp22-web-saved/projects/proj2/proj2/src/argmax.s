.globl argmax

.text
# =================================================================
# FUNCTION: Given a int array, return the index of the largest
#   element. If there are multiple, return the one
#   with the smallest index.
# Arguments:
#   a0 (int*) is the pointer to the start of the array
#   a1 (int)  is the # of elements in the array
# Returns:
#   a0 (int)  is the first index of the largest element
# Exceptions:
#   - If the length of the array is less than 1,
#     this function terminates the program with error code 36
# =================================================================
argmax:
	# Prologue
    li t0, 1
    bge a1, t0, start_logic
    li a0, 36
    j exit
start_logic:
    addi sp, sp, -4
    sw ra, 0(sp)
    lw t1, 0(a0)#max
    li t2, 0#curr index
    li t3, 0#max index
loop_start:
    beq a1, x0, loop_end
    lw t0, 0(a0)#curr value
    bge t1, t0, loop_continue
    mv t1, t0
    mv t3, t2
loop_continue:
    addi a0, a0, 4
    addi t2, t2, 1
    addi a1, a1, -1
    j loop_start
loop_end:
	# Epilogue
    lw ra, 0(sp)
    addi sp, sp, 4
    mv a0, t3
	ret
