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
		if ch == '.':
			input[-1] = 92
		elif ch == '/':
			input[-1] = 100
f.close()
# 0~18: 한글 자음. 0x1100~0x1112.
# input: 0-ㄱ, 2-ㄴ, 3-ㄷ, 7-ㅂ, 9-ㅅ, 11-ㅇ, 12-ㅈ 
# 48: ㅡ, 92: 아래아(.), 50: ㅣ 

print(cho)