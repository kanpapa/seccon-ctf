import socket
import time

# Z80
z80asm = [ \
"NOP",      "LD BC,n'n", "LD (BC),A",  "INC BC",    "INC B", "DEC B", "LD B,n",  "RLCA", "EX AF,AF'", "ADD HL,BC", "LD A,(BC)", "DEC BC", "INC C", "DEC C", "LD C,n", "RRCA", \
"DJNZ",     "LD DE,n'n", "LD (DE),A",  "INC DE",    "INC D", "DEC D", "LD D,n",  "RLA","JR e","ADD HL,DE","LD A,(DE)","DEC DE","INC E","DEC E","LD E,n","RRA", \
"JR NZ,e",  "LD HL,n'n", "LD (n'n),HL","INC HL",   "INC H","DEC H","LD H,n","DAA","JR Z,e","ADD HL,HL","LD HL,(n'n)","DEC HL","INC L","DEC L","LD L,n","CPL", \
"JR NC,e",  "LD SP,n'n", "LD (n'n),A", "INC SP",   "INC (HL)","DEC (HL)","LD (HL),n","SCF","JR C,n'n","ADD HL,SP","LD A,(n'n)","DEC SP","INC A","DEC A","LD A,n","CCF", \
"LD B,B",   "LD B,C",    "LD B,D",     "LD B,E",   "LD B,H","LD B,L","LD B,(HL)","LD B,A","LD C,B","LD C,C","LD C,D","LD C,E","LD C,H","LD C,L","LD C,(HL)","LD C,A", \
"LD D,B",   "LD D,C",    "LD D,D",     "LD D,E",   "LD D,H","LD D,L","LD D,(HL)","LD D,A","LD E,B","LD E,C","LD E,D","LD E,E","LD E,H","LD E,L","LD E,(HL)","LD E,A", \
"LD H,B",   "LD H,C",    "LD H,D",     "LD H,E",   "LD H,H","LD H,L","LD H,(HL)","LD H,A","LD L,B","LD L,C","LD L,D","LD L,E","LD L,H","LD L,L","LD L,(HL)","LD L,A", \
"LD (HL),B","LD (HL),C", "LD (HL),D",  "LD (HL),E","LD (HL),H","LD (HL),L","HALT","LD (HL),A","LD A,B","LD A,C","LD A,D","LD A,E","LD A,H","LD A,L","LD A,(HL)","LD A,A", \
"ADD A,B",  "ADD A,C",   "ADD A,D",    "ADD A,E",  "ADD A,H","ADD A,L","ADD A,(HL)","ADD A,A","ADC A,B","ADC A,C","ADC A,D","ADC A,E","ADC A,H","ADC A,L","ADC A,(HL)","ADC A,A", \
"SUB B",    "SUB C",     "SUB D",      "SUB E",    "SUB H","SUB L","SUB (HL)","SUB A","SBC A,B","SBC A,C","SBC A,D","SBC A,E","SBC A,H", "SBC A,L", "SBC A,(HL)", "SBC A,A", \
"AND B",    "AND C",     "AND D",      "AND E",    "AND H","AND L","AND (HL)","AND A","XOR B","XOR C","XOR D","XOR E","XOR H","XOR L","XOR (HL)","XOR A", \
"OR B",     "OR C",      "OR D",       "OR E",     "OR H","OR L","OR (HL)","OR A","CP B","CP C","CP D","CP E","CP H","CP L","CP (HL)","CP A", \
"RET NZ",   "POP BC",    "JP NZ,n'n",  "JP n'n",   "CALL NZ,n'n","PUSH BC","ADD A,n","RST 00H","RET Z","RET", "JP Z,n'n","CB-CODE","CALL Z,n'n","CALL n'n","ADC A,n","RST 08H", \
"RET NC",   "POP DE",    "JP NC,n'n",  "OUT (n),A","CALL NC,n'n","PUSH DE","SUB n","RST 10H","RET C","EXX","JP C,n'n","IN A,(n)","CALL C,n'n","DD-CODE","SBC A,n","RST 18H", \
"RET PO",   "POP HL",    "JP PO,n'n",  "EX (SP),HL","CALL PO,n'n","PUSH HL","AND n","RST 20H","RET PE","JP (HL)","JP PE,n'n","EX DE,HL","CALL PE,n'n","ED-CODE","XOR n","RST 28H", \
"RET P",    "POP AF",    "JP P,n'n",   "DI",        "CALL P,n'n","PUSH AF","OR n","RST 30H","RET M","LD SP,HL","JP M,n'n","EI","CALL M,n'n","FD-CODE","CP n","RST 38H"]


z80_cbasm = [ \
"RLC B","RLC C","RLC D","RLC E","RCL H","RLC L","RLC (HL)","RLC A","RRC B","RRC C","RRC D","RRC E","RRC H","RRC L","RRC (HL)","RRC A", \
"RL B","RL C","RL D","RL E","RL H","RL L","RL (HL)","RL A","RR B","RR C","RR D","RR E","RR H","RR L","RR (HL)","RR A", \
"SLA B","SLA C","SLA D","SLA E","SLA H","SLA L","SLA (HL)","SLA A","SRA B","SRA C","SRA D","SRA E","SRA H","SRA L","SRA (HL)","SRA A", \
"ng","ng","ng","ng","ng","ng","ng","ng","SRL B","SRL C","SRL D","SRL E","SRL H","SRL L","SRL (HL)","SRL A", \
"BIT 0,B","BIT 0,C","BIT 0,D","BIT 0,E","BIT 0,H","BIT 0,L","BIT 0,(HL)","BIT 0,A","BIT 1,B","BIT 1,C","BIT 1,D","BIT 1,E","BIT 1,H","BIT 1,L","BIT 1,(HL)","BIT 1,A", \
"BIT 2,B","BIT 2,C","BIT 2,D","BIT 2,E","BIT 2,H","BIT 2,L","BIT 2,(HL)","BIT 2,A","BIT 3,B","BIT 3,C","BIT 3,D","BIT 3,E","BIT 3,H","BIT 3,L","BIT 3,(HL)","BIT 3,A", \
"BIT 4,B","BIT 4,C","BIT 4,D","BIT 4,E","BIT 4,H","BIT 4,L","BIT 4,(HL)","BIT 4,A","BIT 5,B","BIT 5,C","BIT 5,D","BIT 5,E","BIT 5,H","BIT 5,L","BIT 5,(HL)","BIT 5,A", \
"BIT 6,B","BIT 6,C","BIT 6,D","BIT 6,E","BIT 6,H","BIT 6,L","BIT 6,(HL)","BIT 6,A","BIT 7,B","BIT 7,C","BIT 7,D","BIT 7,E","BIT 7,H","BIT 7,L","BIT 7,(HL)","BIT 7,A", \
"RES 0,B","RES 0,C","RES 0,D","RES 0,E","RES 0,H","RES 0,L","RES 0,(HL)","RES 0,A","RES 1,B","RES 1,C","RES 1,D","RES 1,E","RES 1,H","RES 1,L","RES 1,(HL)","RES 1,A", \
"RES 2,B","RES 2,C","RES 2,D","RES 2,E","RES 2,H","RES 2,L","RES 2,(HL)","RES 2,A","RES 3,B","RES 3,C","RES 3,D","RES 3,E","RES 3,H","RES 3,L","RES 3,(HL)","RES 3,A", \
"RES 4,B","RES 4,C","RES 4,D","RES 4,E","RES 4,H","RES 4,L","RES 4,(HL)","RES 4,A","RES 5,B","RES 5,C","RES 5,D","RES 5,E","RES 5,H","RES 5,L","RES 5,(HL)","RES 5,A", \
"RES 6,B","RES 6,C","RES 6,D","RES 6,E","RES 6,H","RES 6,L","RES 6,(HL)","RES 6,A","RES 7,B","RES 7,C","RES 7,D","RES 7,E","RES 7,H","RES 7,L","RES 7,(HL)","RES 7,A", \
"SET 0,B","SET 0,C","SET 0,D","SET 0,E","SET 0,H","SET 0,L","SET 0,(HL)","SET 0,A","SET 1,B","SET 1,C","SET 1,D","SET 1,E","SET 1,H","SET 1,L","SET 1,(HL)","SET 1,A", \
"SET 2,B","SET 2,C","SET 2,D","SET 2,E","SET 2,H","SET 2,L","SET 2,(HL)","SET 2,A","SET 3,B","SET 3,C","SET 3,D","SET 3,E","SET 3,H","SET 3,L","SET 3,(HL)","SET 3,A", \
"SET 4,B","SET 4,C","SET 4,D","SET 4,E","SET 4,H","SET 4,L","SET 4,(HL)","SET 4,A","SET 5,B","SET 5,C","SET 5,D","SET 5,E","SET 5,H","SET 5,L","SET 5,(HL)","SET 5,A", \
"SET 6,B","SET 6,C","SET 6,D","SET 6,E","SET 6,H","SET 6,L","SET 6,(HL)","SET 6,A","SET 7,B","SET 7,C","SET 7,D","SET 7,E","SET 7,H","SET 7,L","SET 7,(HL)","SET 7,A"]


z80_ddasm = [
"","","","","","","","","","ADD IX,BC","","","","","","", \
"","","","","","","","","","ADD IX,DE","","","","","","", \
"","LD IX,n'n","LD (n'n),IX","INC IX","INC IXh","DEC IXh","LD IXh,n","","","ADD IX,HL","LD IX,(n'n)","DEC IX","INC IXl","DEC IXl","LD IXl,n","", \
"","","","","INC (IX+d)","DEC (IX+d)","LD (IX+d),n","","","ADD IX,SP","","","","","","", \
"","","","","LD B,IXh","LD B,IXl","LD B,(IX+d)","","","","","","LD C,IXh","LD C,IXl","LD C,(IX+d)","", \
"","","","","LD D,IXh","LD D,IXl","LD D,(IX+d)","","","","","","LD E,IXh","LD E,IXl","LD E,(IX+d)","", \
"LD IXh,B","LD IXh,C","LD IXh,D","LD IXh,E","LD IXh,H","LD IXh,L","LD H,(IX+d)","LD IXh,A","LD IXl,B","LD IXl,C","LD IXl,D","LD IXl,E","LD IXl,H","LD IXl,L","LD L,(IX+d)","LD IXl,A", \
"LD (IX+d),B","LD (IX+d),C","LD (IX+d),D","LD (IX+d),E","LD (IX+d),H","LD (IX+d),L","","LD (IX+d),A","","","","","LD A,IXh","LD A,IXl","LD A,(IX+d)","", \
"","","","","ADD A,IXh","ADD A,IXl","ADD A,(IX+d)","","","","","","ADC A,IXh","ADC A,IXl","ADC A,(IX+d)","", \
"","","","","SUB A,IXh","SUB A,IXl","SUB (IX+d)","","","","","","SBC A,IXh","SBC A,IXl","SBC A,(IX+d)","", \
"","","","","AND IXh","AND IXl","AND (IX+d)","","","","","","XOR IXh","XOR IXl","XOR (IX+d)","", \
"","","","","OR IXh","OR IXl","OR (IX+d)","","","","","","CP IXh","CP IXl","CP (IX+d)","", \
"","","","","","","","","","","","DD-CB-CODE","","","","", \
"","","","","","","","","","","","","","","","", \
"","POP IX","","EX (SP),IX","","PUSH IX","","","","JP (IX)","","","","","","", \
"","","","","","","","","","LD SP,IX","","","","","",""]

z80_edasm = [\
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"IN B,(C)","OUT (C),B","SBC HL,BC","LD (n'n),BC","NEG","RETN","IM 0","LD I,A","IN C,(C)","OUT (C),C","ADC HL,BC","LD BC,(n'n)","","RETI","","LD R,A", \
"IN D,(C)","OUT (C),D","SBC HL,DE","LD (n'n),DE","","","IM 1","LD A,I","IN E,(C)","OUT (C),E","ADC HL,DE","LD DE,(n'n)","","","IM 2","LD A,R", \
"IN H,(C)","OUT (C),H","SBC HL,HL","LD (n'n),HL","","","","RRD","IN L,(C)","OUT (C),L","ADC HL,HL","LD HL,(n'n)","","","","RLD", \
"","","SBC HL,SP","LD (n'n),SP","","","","","IN A,(C)","OUT (C),A","ADC HL,SP","LD SP,(n'n)","","","","", \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"LDI","CPI","INI","OUTI","","","","","LDD","CPD","IND","OUTD","","","","", \
"LDIR","CPIR","INIR","OTIR","","","","","LDDR","CPDR","INDR","OTDR","","","","" \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","","", \
"","","","","","","","","","","","","","","",""]

z80_ddcbasm = [\
"","","","","","","RLC (IX+d)","","","","","","","","RRC (IX+d)","", \
"","","","","","","RL (IX+d)","","","","","","","","RR (IX+d)","", \
"","","","","","","SLA (IX+d)","","","","","","","","SRA (IX+d)","", \
"","","","","","","","","","","","","","","SRL (IX+d)","", \
"","","","","","","BIT 0,(IX+d)","","","","","","","","BIT 1,(IX+d)","", \
"","","","","","","BIT 2,(IX+d)","","","","","","","","BIT 3,(IX+d)","", \
"","","","","","","BIT 4,(IX+d)","","","","","","","","BIT 5,(IX+d)","", \
"","","","","","","BIT 6,(IX+d)","","","","","","","","BIT 7,(IX+d)","", \
"","","","","","","RES 0,(IX+d)","","","","","","","","RES 1,(IX+d)","", \
"","","","","","","RES 2,(IX+d)","","","","","","","","RES 3,(IX+d)","", \
"","","","","","","RES 4,(IX+d)","","","","","","","","RES 5,(IX+d)","", \
"","","","","","","RES 6,(IX+d)","","","","","","","","RES 7,(IX+d)","", \
"","","","","","","SET 0,(IX+d)","","","","","","","","SET 1,(IX+d)","", \
"","","","","","","SET 2,(IX+d)","","","","","","","","SET 3,(IX+d)","", \
"","","","","","","SET 4,(IX+d)","","","","","","","","SET 5,(IX+d)","", \
"","","","","","","SET 6,(IX+d)","","","","","","","","SET 7,(IX+d)",""]

z80_fdcbasm = [\
"","","","","","","RLC (IY+d)","","","","","","","","RRC (IY+d)","", \
"","","","","","","RL (IY+d)","","","","","","","","RR (IY+d)","", \
"","","","","","","SLA (IY+d)","","","","","","","","SRA (IY+d)","", \
"","","","","","","","","","","","","","","SRL (IY+d)","", \
"","","","","","","BIT 0,(IY+d)","","","","","","","","BIT 1,(IY+d)","", \
"","","","","","","BIT 2,(IY+d)","","","","","","","","BIT 3,(IY+d)","", \
"","","","","","","BIT 4,(IY+d)","","","","","","","","BIT 5,(IY+d)","", \
"","","","","","","BIT 6,(IY+d)","","","","","","","","BIT 7,(IY+d)","", \
"","","","","","","RES 0,(IY+d)","","","","","","","","RES 1,(IY+d)","", \
"","","","","","","RES 2,(IY+d)","","","","","","","","RES 3,(IY+d)","", \
"","","","","","","RES 4,(IY+d)","","","","","","","","RES 5,(IY+d)","", \
"","","","","","","RES 6,(IY+d)","","","","","","","","RES 7,(IY+d)","", \
"","","","","","","SET 0,(IY+d)","","","","","","","","SET 1,(IY+d)","", \
"","","","","","","SET 2,(IY+d)","","","","","","","","SET 3,(IY+d)","", \
"","","","","","","SET 4,(IY+d)","","","","","","","","SET 5,(IY+d)","", \
"","","","","","","SET 6,(IY+d)","","","","","","","","SET 7,(IY+d)",""]

print "z80asm_len: ",len(z80asm)
print "z80_ddasm_len: ",len(z80_ddasm)
print "z80_ddcbasm_len: ",len(z80_ddcbasm)
print "z80_fdcbasm_len: ",len(z80_fdcbasm)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("disassemble.quals.seccon.jp",23168))

for l in range(100):
    print l
    recvstr = s.recv(256)
    print "recvstr:",recvstr

    line = recvstr.splitlines()
    line1 = line[0]
    line2 = line[1]
    print "line1:",line1
    print "line2:",line2

    strlist = line1.split(' ')
    print "strlist:",strlist

    code_len = len(strlist) - 2
    print "code_len:",code_len

    if code_len == 1:
      # CODE1
      code1 = strlist[2]
      print "code1:",code1
      code1_num = int(code1, 16);
      print "code1_num:",code1_num
      code1_op  = z80asm[code1_num]
      print "code1_op:",code1_op
      asm_code = code1_op
    elif code_len == 2:
      # CODE2
      code1 = strlist[2]
      if code1 == "CB":
        # CB CODE
        code2 = strlist[3]
        code2_num = int(code2, 16);
        print "code2_num:",code2_num
        code2_op  = z80_cbasm[code2_num]
        print "code2_op:",code2_op
        asm_code = code2_op
      elif code1 == "DD":
        # DD CODE
        code2 = strlist[3]
        code2_num = int(code2, 16);
        print "code2_num:",code2_num
        code2_op  = z80_ddasm[code2_num]
        print "code2_op:",code2_op
        asm_code = code2_op
      elif code1 == "ED":
        # ED CODE
        code2 = strlist[3]
        code2_num = int(code2, 16);
        print "code2_num:",code2_num
        code2_op  = z80_edasm[code2_num]
        print "code2_op:",code2_op
        asm_code = code2_op
      else:
        code2 = strlist[3] + "H"
        print "code1:",code1
        code1_num = int(code1, 16);
        print "code1_num:",code1_num
        code1_op  = z80asm[code1_num]
        print "code1_op:",code1_op
        code2_op  = code1_op.replace('n',code2)
        print "code2_op:",code2_op 
        asm_code = code2_op
    elif code_len == 3:
         # CODE3
         code1 = strlist[2]
         if code1 == "DD":
            # DD CODE
            code2 = strlist[3]
            code2_num = int(code2, 16);
            print "code2_num:",code2_num
            code2_op  = z80_ddasm[code2_num]
            print "code2_op:",code2_op
            code3 = strlist[4] + "H"
            code3_op  = code2_op.replace("d",code3)
            print "code3_op:",code3_op
            asm_code = code3_op

         else:
            code2 = strlist[4] + strlist[3] + "H"
            print "code1:",code1
            code1_num = int(code1, 16);
            print "code1_num:",code1_num
            code1_op  = z80asm[code1_num]
            print "code1_op:",code1_op
            code2_op  = code1_op.replace("n'n",code2)
            print "code2_op:",code2_op 
            asm_code = code2_op

    elif code_len == 4:
         code1 = strlist[2]
         code2 = strlist[3]
         code3 = strlist[4]
         code4 = strlist[5]
         if code1 == "ED":
              code2_num = int(code2, 16)
              code2_op = z80_edasm[code2_num]
              print "code2_op:",code2_op
              asm_code = code2_op.replace("n'n",code4 + code3 + "H")
	 if code1 == "FD":
            if code2 == "CB":
              code4_num = int(code4, 16)
              print "code4_num:",code4_num
              code4_op = z80_fdcbasm[code4_num]
              print "code4_op:",code4_op
              asm_code = code4_op.replace("d",code3 + "H")
	 if code1 == "DD":
            if code2 == "CB":
              code4_num = int(code4, 16)
              print "code4_num:",code4_num
              code4_op = z80_ddcbasm[code4_num]
              print "code4_op:",code4_op
              asm_code = code4_op.replace("d",code3 + "H")
            else:
              code2_num = int(code2, 16)
              code2_op = z80_ddasm[code2_num]
              print "code2_op:",code2_op
              asm_code = code2_op.replace("n",code3 + "H")
              asm_code = asm_code.replace("d",code4 + "H")

    print "asm_code:",asm_code 
    sendstr = asm_code + '\n'
    print "sendstr:",sendstr

    s.sendall(sendstr)

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

s.close()
