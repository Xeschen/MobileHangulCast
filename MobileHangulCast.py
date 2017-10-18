import sys
from states import *

def make(cho, jung, jong):
	return cho*588 + (jung-30)*28 + jong + 0xAC00

def toCho(ja):
	dic = {0:0, 1:1, 3:2, 6:3, 7:4, 8:5, 16:6, 17:7, 18:8, 20:9, \
		   21:10, 22:11, 23:12, 24:13, 25:14, 26:15, 27:16, 28:17, 29:18}
	return dic[ja]

def toJong(ja):
	dic = {0:1, 1:2, 2:4, 3:7, 5:8, 6:16, 7:17, 9:19, \
		   10:20, 11:21, 12:22, 14:23, 15:24, 16:25, 17:26, 18:27}
	return dic[ja]
	
input = []
f = open('input.txt', 'r')
for line in f:	# only one line now
	for cnt in range(len(line)):
		ch = ord(line[cnt])
		if (0 <= ch-0x3131) and (ch-0x3131 <= 29):
			input.append(toCho(ch-0x3131))
		else:
			input.append(ch-0x3131)
		if ch == ord('.'):
			input[-1] = 92
		elif ch == ord('/'):
			input[-1] = 100
input.append(ord(';')-0x3131)	# terminator
f.close()

# 0~18: 한글 자음. 0x1100~0x1112.
# input: 0-ㄱ, 2-ㄴ, 3-ㄷ, 7-ㅂ, 9-ㅅ, 11-ㅇ, 12-ㅈ 
# 48: ㅡ, 92: 아래아(.), 50: ㅣ 

state = cho
c_char, c_cho, c_jung, c_jong = 0, 0, 0, 0
p_char = []
for z in range(100):
	p_char.append(0)
p = 0
temp_char = 0
temp_temp_char = 0

for i in range(len(input)):
	st = 0
	pp = p
	if ((state==dot) or (state==dotdot)) and (temp_char!=0):
		pp -= 1
	if state==cho:
		pp = 0
	while st<pp:
		sys.stdout.write("%c" % p_char[st])
		st += 1

	if state == cho:
		if (0<=input[i]) and (input[i]<=29):
			c_cho = input[i]
			state = jung
	elif state == jung:
		if input[i]==92:
			temp_char = 0
			state = dot
		elif input[i]==48:
			state = m
			c_jung = input[i]
		elif input[i]==50:
			state = l
			c_jung = input[i]
		elif input[i]==100:
			state = cho
			p_char[p] = c_cho+0x1100
			p += 1
		print("%c" % (c_cho+0x1100))
		if (0<=input[i]) and (input[i]<=29):
			state = jung
			if input[i]==0:       #ㄱ,ㅋ,ㄲ 
				if c_cho==0:
					c_cho = 15
				elif c_cho==15:
					c_cho = 1
				elif c_cho==1:
					c_cho = 0
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==8:                    #ㄺ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 9
						state = bot1
			elif input[i]==2:       #ㄴ,ㄹ 
				if c_cho==2:
					c_cho = 5
				elif c_cho==5:
					c_cho = 2
			elif input[i]==3:       #ㄷ,ㅌ,ㄸ 
				if c_cho==3:
					c_cho = 16
				elif c_cho==16:
					c_cho = 4
				elif c_cho==4:
					c_cho = 3
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==0:
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 3
						state = bot2
			elif input[i]==7:       #ㅂ,ㅍ,ㅃ 
				if c_cho==7:
					c_cho = 17
				elif c_cho==17:
					c_cho = 8
				elif c_cho==8:
					c_cho = 7
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==0:
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 7
						state = bot2
					elif temp_jong==8:        #ㄼ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 11
						state = bot1
			elif input[i]==9:       #ㅅ,ㅎ,ㅆ 
				if c_cho==9:
					c_cho = 18
				elif c_cho==18:
					c_cho = 10
				elif c_cho==10:
					c_cho = 9
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==1:             #ㄳ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 3
						state = bot1
					elif temp_jong==8:      #ㄽ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 12
						state = bot1
					elif temp_jong==17:      #ㅄ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 18
						state = bot1
			elif input[i]==12:       #ㅈ,ㅊ,ㅉ 
				if c_cho==12:
					c_cho = 14
				elif c_cho==14:
					c_cho = 13
				elif c_cho==13:
					c_cho = 12
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==0:
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 12
						state = bot2
					elif temp_jong==4:      #ㄵ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 5
						state = bot1
			elif input[i]==11:       #ㅇ,ㅁ 
				if c_cho==11:
					c_cho = 6
					temp_ch = p_char[p-1]%0x10000 - 0xAC00
					temp_jong = temp_ch%28
					if temp_jong==8:          #ㄻ 
						p_char[p-1] = 0
						p -= 1
						c_cho = temp_ch/(21*28)
						c_jung = (temp_ch/28)%21 + 30
						c_jong = 10
						state = bot1
				elif c_cho==6:
					c_cho = 11
	elif state == l:
		print("%c" % make(c_cho, c_jung, 0))
		if input[i]==92:
			state = ldot
			c_jung = 30
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == ldot:
		print("%c" % make(c_cho, c_jung, 0))
		if input[i]==92:
			state = ldotdot
			c_jung = 32
		elif input[i]==50:
			state = ldotl
			c_jung = 31
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == ldotdot:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==50:
			state = dotll
			c_jung = 33
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == m:
		print("%c" % make(c_cho, c_jung, 0))
		c_jong = 0
		if input[i]==50:
			state = ml
			c_jung = 49
		elif input[i]==92:
			state = mdot
			c_jung = 43
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == mdot:
		print("%c" % make(c_cho, c_jung, 0))
		if input[i]==92:
			state = mdotdot
			c_jung = 47
		elif input[i]==50:
			state = mdotl
			c_jung = 46
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == mdotdot:
		print("%c" % make(c_cho, c_jung, 0))
		if input[i]==50:
			state = mdotdotl
			c_jung = 44
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == mdotdotl:
		print("%c" % make(c_cho, c_jung, 0))
		if input[i]==50:
			state = mdotdotll
			c_jung = 45
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dot:
		if temp_char != 0:
			temp_temp_char = temp_char
			sys.stdout.write("%c" % temp_char)
			temp_char = 0
		else:
			temp_temp_char = 0
			sys.stdout.write("%c" % (c_cho + 0x1100))
		print("%c" % 0x119E)
		if input[i]==50:
			state = dotl
			c_jung = 34
		elif input[i]==48:
			state = dotm
			c_jung = 38
		elif input[i]==92:
			state = dotdot
			temp_char = temp_temp_char
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotl:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==50:
			state = dotll
			c_jung = 35
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotm:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==50:
			state = dotml
			c_jung = 41
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotml:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==92:
			state = dotmldot
			c_jung = 39
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotmldot:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==50:
			state = dotmldotl
			c_jung = 40
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotdot:
		if temp_char != 0:
			sys.stdout.write("%c" % temp_char)
			temp_char = 0
		else:
			sys.stdout.write("%c" % (c_cho + 0x1100))
		print("%c%c" % (0x119E, 0x119E))
		if input[i]==50:
			state = dotdotl
			c_jung = 36
		elif input[i]==48:
			state = dotm
			c_jung = 42
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
	elif state == dotdotl:
		print("%c" % make(c_cho, c_jung, 0))  
		if input[i]==50:
			state = dotdotll
			c_jung = 37
		elif (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
		
	elif state in [dotll, dotmldotl, dotdotm, ldotl, ldotdotl, ml, mdotl, mdotdotll, dotdotll]:
		print("%c" % make(c_cho, c_jung, 0))  
		if (0<=input[i]) and (input[i]<=18):
			if (input[i]==0) or (input[i]==7):              #ㄱ,ㅂ 
				state = r
				c_jong = input[i]
			elif input[i]==2:        #ㄴ 
				state = s
				c_jong = input[i]
			elif input[i]==5:        #ㄹ 
				state = f
				c_jong = input[i]
			elif (input[i]==4) or (input[i]==8) or (input[i]==13):    #ㄸ,ㅃ,ㅉ 
				p_char[p] = make(c_cho, c_jung, 0)
				p += 1
				state = jung
				c_cho = input[i]
			else:
				state = bot2
				c_jong = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = cho
		
	elif state == r:    #ㄱ,ㅂ 받침 
		print("%c" % make(c_cho, c_jung, toJong(c_jong)))
		if input[i]==9:              #ㅅ
			state = bot1
			if c_jong==0:
				c_jong = 3              #ㄳ 
			elif c_jong==7:
				c_jong = 18              #ㅄ 
		elif (input[i]==0) and (c_jong==0):         #ㄱ 받침에 ㄱ 
			state = bot2
			c_jong = 15
		elif (input[i]==7) and (c_jong==7):         #ㅂ 받침에 ㅂ  
			state = bot2
			c_jong = 17
		elif (0<=input[i]) and (input[i]<=18):        #다른 자음 
			state = jung
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = input[i]
		elif input[i]==92:
			p_char[p] = make(c_cho, c_jung, 0)
			temp_char = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = c_jong
			state = dot
		elif input[i]==48:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = m
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==50:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = l
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			state = cho
	elif state == s:
		print("%c" % make(c_cho, c_jung, toJong(c_jong)))
		if (input[i]==12) or (input[i]==18):          #ㅈ,ㅎ 
			state = bot1
			if input[i]==12:
				c_jong = 5              #ㄵ 
			if input[i]==18:
				c_jong = 6              #ㄶ 
		elif input[i]==2:         #ㄴ 받침에 ㄴ 
			state = f
			c_jong = 5
		elif (0<=input[i]) and (input[i]<=18):        #다른 자음 
			state = jung
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = input[i]
		elif input[i]==92:
			p_char[p] = make(c_cho, c_jung, 0)
			temp_char = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = c_jong
			state = dot
		elif input[i]==48:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = m
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==50:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = l
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			state = cho
	elif state == f:
		print("%c" % make(c_cho, c_jung, toJong(c_jong)))
		if input[i] in [0, 6, 7, 9, 16, 17, 18]:	#ㄱ,ㅁ,ㅂ,ㅅ,ㅌ,ㅍ,ㅎ 
			state = bot1
			if input[i]==0:
				c_jong = 9   #ㄺ 
			elif input[i]==6:
				c_jong = 10  #ㄻ 
			elif input[i]==7:
				c_jong = 11  #ㄼ 
			elif input[i]==9:
				c_jong = 12  #ㄽ 
			elif input[i]==16:
				c_jong = 13   #ㄾ 
			elif input[i]==17:
				c_jong = 14   #ㄿ 
			elif input[i]==18:
				c_jong = 15   #ㅀ 
		elif input[i]==2:         #ㄹ 받침에 ㄴ 
			state = s
			c_jong = 2
		elif (0<=input[i]) and (input[i]<=18):        #다른 자음 
			state = jung
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = input[i]
		elif input[i]==92:
			p_char[p] = make(c_cho, c_jung, 0)
			temp_char = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			c_cho = c_jong
			state = dot
		elif input[i]==48:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = m
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==50:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			state = l
			c_cho = c_jong
			c_jung = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			state = cho
	elif state == bot1: #ㄳ,ㄵ,ㄶ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅄ 
		temp_char = make(c_cho, c_jung, c_jong)
		print("%c" % temp_char)
		if (input[i]==9) and (c_jong==3):         #ㄳ 받침에 ㅅ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 1)
			p += 1
			c_cho = 18
		elif (input[i]==12) and (c_jong==5):         #ㄵ 받침에 ㅈ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 4)
			p += 1
			c_cho = 14
		elif (input[i]==9) and (c_jong==6):         #ㄶ 받침에 ㅅ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 4)
			p += 1
			c_cho = 10
		elif (input[i]==0) and (c_jong==9):         #ㄺ 받침에 ㄱ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 8)
			p += 1
			c_cho = 15
		elif (input[i]==11) and (c_jong==10):         #ㄻ 받침에 ㅇ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 8)
			p += 1
			c_cho = 11
		elif (input[i]==7) and (c_jong==11):         #ㄼ 받침에 ㅂ 
			state = bot1
			c_jong = 14
		elif (input[i]==9) and (c_jong==12):         #ㄽ 받침에 ㅅ 
			state = bot1
			c_jong = 15
		elif (input[i]==3) and (c_jong==13):         #ㄾ 받침에 ㄷ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 8)
			p += 1
			c_cho = 4
		elif (input[i]==7) and (c_jong==14):         #ㄿ 받침에 ㅂ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 8)
			p += 1
			c_cho = 8
		elif (input[i]==9) and (c_jong==15):         #ㅀ 받침에 ㅅ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 8)
			p += 1
			c_cho = 10
		elif (input[i]==9) and (c_jong==18):         #ㅄ 받침에 ㅅ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 17)
			p += 1
			c_cho = 18
		elif (0<=input[i]) and (input[i]<=18):        #다른 자음 
			p_char[p] = make(c_cho, c_jung, c_jong)
			p += 1
			state = jung
			c_cho = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, c_jong)
			p += 1
			state = cho
		else:
			if c_jong==3:              #ㄳ 
				p_char[p] = make(c_cho, c_jung, 1)
				c_cho = 9
			elif c_jong==5:        #ㄵ 
				p_char[p] = make(c_cho, c_jung, 4)
				c_cho = 12
			elif c_jong==6:        #ㄶ 
				p_char[p] = make(c_cho, c_jung, 4)
				c_cho = 18
			elif c_jong==9:        #ㄺ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 1
			elif c_jong==10:       #ㄻ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 6
			elif c_jong==11:       #ㄼ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 7
			elif c_jong==12:       #ㄽ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 9
			elif c_jong==13:       #ㄾ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 16
			elif c_jong==14:       #ㄿ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 17
			elif c_jong==15:       #ㅀ 
				p_char[p] = make(c_cho, c_jung, 8)
				c_cho = 18
			elif c_jong==18:       #ㅄ 
				p_char[p] = make(c_cho, c_jung, 17)
				c_cho = 9
			p += 1
			if input[i]==92:
				state = dot
			elif input[i]==48:
				state = m
				c_jung = 48
			elif input[i]==50:
				state = l
				c_jung = 50
	elif state == bot2: #ㄷ,ㅁ,ㅅ,ㅇ,ㅈ,ㅊ,ㅋ,ㄷ,ㅁ,ㅎ,ㄲ,ㅆ 
		temp_char = make(c_cho, c_jung, toJong(c_jong))
		print("%c" % temp_char)
		if (input[i]==0) and (c_jong==15):         #ㅋ 받침에 ㄱ 
			state = bot2
			c_jong = 1
		elif (input[i]==0) and (c_jong==1):         #ㄲ 받침에 ㄱ 
			state = r
			c_jong = 0
		elif (input[i]==3) and (c_jong==3):         #ㄷ 받침에 ㄷ 
			state = bot2
			c_jong = 16
		elif (input[i]==3) and (c_jong==16):         #ㅌ 받침에 ㄷ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			c_cho = 4
		elif (input[i]==7) and (c_jong==17):         #ㅍ 받침에 ㅂ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			c_cho = 8
		elif (input[i]==9) and (c_jong==9):         #ㅅ 받침에 ㅅ 
			state = bot2
			c_jong = 18
		elif (input[i]==9) and (c_jong==18):         #ㅎ 받침에 ㅅ 
			state = bot2
			c_jong = 10
		elif (input[i]==9) and (c_jong==10):         #ㅆ 받침에 ㅅ 
			state = bot2
			c_jong = 9
		elif (input[i]==11) and (c_jong==11):         #ㅇ 받침에 ㅇ 
			state = bot2
			c_jong = 6
		elif (input[i]==11) and (c_jong==6):         #ㅁ 받침에 ㅇ 
			state = bot2
			c_jong = 11
		elif (input[i]==12) and (c_jong==12):         #ㅈ 받침에 ㅈ 
			state = bot2
			c_jong = 14
		elif (input[i]==12) and (c_jong==14):         #ㅊ 받침에 ㅈ 
			state = jung
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			c_cho = 13
		elif (0<=input[i]) and (input[i]<=18):        #다른 자음 
			p_char[p] = make(c_cho, c_jung, toJong(c_jong))
			p += 1
			state = jung
			c_cho = input[i]
		elif input[i]==100:
			p_char[p] = make(c_cho, c_jung, c_jong)
			p += 1
			state = cho
		else:
			p_char[p] = make(c_cho, c_jung, 0)
			p += 1
			c_cho = c_jong
			if input[i]==92:
				state = dot
			elif input[i]==48:
				state = m
				c_jung = 48
			elif input[i]==50:
				state = l
				c_jung = 50

