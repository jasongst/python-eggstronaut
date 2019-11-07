import networkx as nx
import matplotlib.pyplot as plt


# tab2 = [[
# ["1", " ", "o", "o", "o", " ", "o", "o", "o", " ", " ", " ", "2"],
# [" ", "X", " ", "X", "o", "X", "o", "X", "o", "X", "o", "X", " "], 
# [" ", " ", " ", " ", "o", " ", "o", " ", "o", " ", " ", " ", "o"], 
# ["o", "X", " ", "X", " ", "X", "o", "X", " ", "X", " ", "X", " "], 
# ["o", "o", "o", " ", " ", "o", "o", "o", " ", " ", "o", "o", "o"], 
# [" ", "X", "o", "X", " ", "X", " ", "X", "o", "X", " ", "X", "o"], 
# [" ", " ", " ", "o", "o", "o", " ", " ", " ", "o", "o", "o", "o"], 
# ["o", "X", "o", "X", " ", "X", "o", "X", " ", "X", "o", "X", " "], 
# [" ", "o", " ", "o", "o", "o", "o", " ", "o", "o", " ", "o", "o"], 
# [" ", "X", "o", "X", "o", "X", " ", "X", " ", "X", " ", "X", " "], 
# ["3", " ", " ", " ", "o", " ", "o", "o", " ", " ", "o", " ", "4"]
# ], 
# []]
# # acces tab carte[0][2]
# # (i,j) -> (2,2)
# tab= [[
# [" ", " ", "B"],
# [" ", " ", " "]
# ], 
# []]

class graphIA:
	
	def __init__(self,carte):
		self.caseAdmise = [" ","1","2","3","4","5"]
		self.carte = carte[0]
		self.nbTableaux = len(carte[0])
		self.tailleTableau = len(carte[0][0])
		self.graphe = self.tabToGraph(carte)
	
	def tabToGraph(self,carte):
		G = nx.Graph()
		
		for indice1 in range(self.nbTableaux-1):
			for indice2 in range(self.tailleTableau-1):
				if self.carte[indice1+1][indice2] in self.caseAdmise and self.carte[indice1][indice2] in self.caseAdmise:
					G.add_edge((indice1,indice2),(indice1+1,indice2))
				if self.carte[indice1][indice2+1] in self.caseAdmise and self.carte[indice1][indice2] in self.caseAdmise:
					G.add_edge((indice1,indice2),(indice1,indice2+1))
					
		for indice1 in range(self.nbTableaux-1):
			if self.carte[indice1+1][self.tailleTableau-1] in self.caseAdmise and self.carte[indice1][self.tailleTableau-1] in self.caseAdmise:
				print((indice1,self.tailleTableau-1),(indice1+1,self.tailleTableau-1))
				print(self.carte)
				print(self.carte[0][2])
				print(indice1+1,self.tailleTableau-1)
				G.add_edge((indice1,self.tailleTableau-1),(indice1+1,self.tailleTableau-1))
				
		for indice2 in range(self.tailleTableau-1):
			if self.carte[self.nbTableaux-1][indice2+1] in self.caseAdmise  and self.carte[self.nbTableaux-1][indice2] in self.caseAdmise:
				G.add_edge((self.nbTableaux-1,indice2),(self.nbTableaux-1,indice2+1))

		#print(G.edges())
		return G
	
	def cheminEchappeBombe(self,i0,j0):
		G = self.graphe
		chemin = nx.dfs_successors(G, source=(i0,j0),depth_limit=2)
		cle = list(chemin.keys())
		first = cle[0]
		sec = chemin[first][0]
		
		return first,sec
		
	
	def showGraph(self):
		nx.draw(self.graphe)
		plt.show()

# IA1 = graphIA(tab2)
# print(IA1.cheminEchappeBombe(0,0))

#IA1.showGraph()

