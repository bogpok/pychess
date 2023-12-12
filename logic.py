class chessrules:
	def canmove(x1, y1, x2, y2, name, team = "black", take = False):
		if name == "pawn":
			yn = 1
			if (team == "black" and y1 == 2) or (team == "white" and y1 == 7):				
				yn = 2 # first move			
			if x1 == x2 or (abs(x1-x2)==1 and take): 
				if (-yn <= y2 - y1 < 0 and team == "white") or (0 < y2 - y1 <= yn and team == "black"):					
					return True
				else:
					return False
			else:
				return False
		elif name == "knight":
			if (abs(y1 - y2) == 2 and abs(x1-x2)==1) or (abs(x1 - x2) == 2 and abs(y1-y2)==1):
				return True
			else:
				return False
		elif name == "rook":
			if x1==x2 or y1==y2:
				return True			
			else:
				return False
		elif name == "king":
			if abs(x1-x2) <= 1 and abs(y1-y2) <= 1:
				return True
			else:
				return False
		elif name == "bishop":
			if abs(x1-x2) == abs(y1-y2):
				return True
			else:
				return False			
		elif name == "queen":
			if abs(x1-x2) == abs(y1-y2) or (x1==x2 or y1==y2):
				return True
			else:
				return False
		else:
			return None
