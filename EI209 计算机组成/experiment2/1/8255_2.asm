;-----------------------------------------------------------
;
;              Build this with the "Source" menu using
;                     "Build All" option
;
;-----------------------------------------------------------
;
;                           ʵ���ʾ������ 

;-----------------------------------------------------------
;                                                          |
;                                                          |
; ���ܣ�����7������ܵ���ʾ                                |
; ��д����Ƕ��ʽϵͳԭ����ʵ�顷�γ���                     |
;-----------------------------------------------------------
		DOSSEG
		.MODEL	SMALL		; �趨8086������ʹ��Small model
		.8086				; �趨����8086���ָ�
;-----------------------------------------------------------
;	���Ŷ���                                               |
;-----------------------------------------------------------
;
; 8255оƬ�˿ڵ�ַ ��Port number������:
PortA	EQU		90H			; Port A's port number in I/O space
PortB	EQU 	92H			; Port B's port number in I/O space
PortC	EQU 	94H			; Port C's port number in I/O space
CtrlPT	EQU 	96H			; 8255 Control Register's port number in I/O space
;
Patch_Protues	EQU		IN AL, 0	;	Simulation Patch for Proteus, please ignore this line


;-----------------------------------------------------------
;	�������ݶ�                                             |
;-----------------------------------------------------------
		.data					; �������ݶ�;

DelayShort	dw	4000   			; ����ʱ����	
DelayLong	dw	40000			; ����ʱ����

; ��ʾ����
DISCHAR DB 01,02,03,04

; SEGTAB����ʾ�ַ�0-F�������в������ݵĶ����д�������������
SEGTAB  	DB 3FH	; 7-Segment Tube, ���������͵�7�������ʾ��ͼ
		DB 06H	;
		DB 5BH	;            a a a
		DB 4FH	;         f         b
		DB 66H	;         f         b
		DB 6DH	;         f         b
		DB 7DH	;            g g g 
		DB 07H	;         e         c
		DB 7FH	;         e         c
		DB 6FH	;         e         c
        	DB 77H	;            d d d     h h h
		DB 7CH	; ----------------------------------
		DB 39H	;       b7 b6 b5 b4 b3 b2 b1 b0
		DB 5EH	;       DP  g  f  e  d  c  b  a
		DB 79H	;
		DB 71H	;


;-----------------------------------------------------------
;	��������                                             |
;-----------------------------------------------------------
		.code						; Code segment definition
		.startup					; ���������ִ����ڵ�
;------------------------------------------------------------------------
		Patch_Protues				; Simulation Patch for Proteus,
									; Please ignore the above code line.
;------------------------------------------------------------------------


; Init 8255 in Mode 0
; PortA Output, PortB Output
;
		MOV AL,10001001B
		OUT CtrlPT,AL	;

		MOV BH,0
		MOV BX,OFFSET SEGTAB
;
; ������1��2��3��4��ʾ���������
;

L1: 
		MOV AL,0h
		OUT PortB,AL
		IN AL,PortC
		MOV AH,AL
		AND AL,0F0h
		OR AL,05h
		OUT PortA,AL
		AND AH,0Fh
		MOV AL,AH
		XLAT
		OUT PortB,AL
		
		MOV AL,0h
		OUT PortB,AL
		MOV CL,4
		IN AL,PortC
		MOV AH,AL
		AND AL,0F0h
		OR AL,0Ah
		OUT PortA,AL
		AND AH,0F0h
		SHR AH,CL
		MOV AL,AH
		XLAT
		OUT PortB,AL
		
		;CALL DELAY			; ������ �˴�Ϊ����Ҫ����DELAY�ӳ���
		JMP L1  
		  

RET

;--------------------------------------------
;                                           |
; Delay system running for a while          |
; CX : contains time para.                  |
;                                           |
;--------------------------------------------

DELAY1 	PROC
    	PUSH CX
    	MOV CX,DelayLong	;
D0: 	LOOP D0
    	POP CX
    	RET
DELAY1 	ENDP


;--------------------------------------------
;                                           |
; Delay system running for a while          |
;                                           |
;--------------------------------------------

DELAY 	PROC
    	PUSH CX
    	MOV CX,DelayShort
D1: 	LOOP D1
    	POP CX
    	RET
DELAY 	ENDP


;-----------------------------------------------------------
;	�����ջ��                                             |
;-----------------------------------------------------------
		.stack 100h				; ����256�ֽ������Ķ�ջ


		END						;ָʾ�������������