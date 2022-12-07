.data

endl: .asciiz "\n"
x: .word	0:1
y: .word	0:1
z: .word	0:1

.text

main:
li $a0 1
sw $a0 x
li $a0 2
sw $a0 y
lw $a0 x
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 y
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 z
//imprimir z
lw $a0 z
li $v0 1
syscall
li $v0 4
la $a0 endl
syscall

//imprimir z
li $v0 10
syscall
