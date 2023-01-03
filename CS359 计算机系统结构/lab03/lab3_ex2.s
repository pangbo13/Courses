	.file	1 "lab3_ex2.c"
	.section .mdebug.abi32
	.previous
	.nan	legacy
	.module	fp=32
	.module	nooddspreg
	.text
	.section	.text.startup,"ax",@progbits
	.align	2
	.globl	main
	.set	nomips16
	.set	nomicromips
	.ent	main
	.type	main, @function
main:
	.frame	$sp,0,$31		# vars= 0, regs= 0/0, args= 0, gp= 0
	.mask	0x00000000,0
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	lui	$2,%hi(source)
	lw	$4,%lo(source)($2)
	nop
	beq	$4,$0,$L2
	nop

	lui	$3,%hi(dest)
	lui	$2,%hi(source+4)
	addiu	$3,$3,%lo(dest)
	addiu	$2,$2,%lo(source+4)
$L3:
	sw	$4,0($3)
	lw	$4,0($2)
	addiu	$3,$3,4
	addiu	$2,$2,4
	bne	$4,$0,$L3
	nop

$L2:
	move	$2,$0
	jr	$31
	nop

	.set	macro
	.set	reorder
	.end	main
	.size	main, .-main

	.comm	dest,40,4
	.globl	source
	.data
	.align	2
	.type	source, @object
	.size	source, 28
source:
	.word	3
	.word	1
	.word	4
	.word	1
	.word	5
	.word	9
	.word	0
	.ident	"GCC: (GNU) 9.1.0"
