.data

endl: .asciiz "\n"
x: .word	0:1
y: .word	0:1
z: .word	0:1

.text

main:
li $a0 7
sw $a0 x
li $a0 8
sw $a0 y
lw $a0 x
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 y
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 z
lw $a0 z
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 10
lw $t1 4($sp)
beq $a0 $t1 label_true
label_false:
li $a0 2
sw $a0 z
b label_end
label_true:
li $a0 1
sw $a0 z
label_end:

lw $a0 z
li $v0 1
syscall
li $v0 4
la $a0 endl
syscall
li $v0 10
syscall
