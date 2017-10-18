from enum import Enum
global_vals = globals()
states = Enum('states', 'cho, jung, dot, dotl, dotll, dotm, dotml, dotmldot, dotmldotl, dotdot, dotdotl, dotdotll, dotdotm, l, ldot, ldotl, ldotdot, ldotdotl, m, ml, mdot, mdotl, mdotdot, mdotdotl, mdotdotll, r, s, f, bot1, bot2')

for i, en in enumerate(states):
	global_vals[en.name] = i