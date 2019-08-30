from pulp import *
import gc
import numpy as np

class PathletLearningClass :
    def __init__(self, trajectories) :

        self.Pathlets, IndexesForConstraints= self.FindAllPossiblePathlets(trajectories)

        gc.collect()

        PathletResults,self.TrajsResults = self.SolvePathletLearningLinearly(trajectories, IndexesForConstraints)
        #print(IndexesForConstraints)

        gc.collect()
        
        self.MinimizePathletLearningResults(PathletResults)

        #print("\nAAA\n",self.Pathlets,self.TrajsResults)
        

    def FindAllPossiblePathlets(self, trajectories) :
        print("STARTFINDPOSSIBLEPATHLETS")
        AllPossiblePathlets = []
        TrajsIndexesNeededForPathletLearning = []

        seen = dict()

        for traj in trajectories :
            trajIndexTemp = []
            for i in range(len(traj)) :
                trajIndexTemp.append([])

            for i in range(len(traj) + 1): 

                for j in range(i + 1, len(traj) + 1): 

                    sub = tuple(traj[i:j])
                    #print(sub)
                    if (sub not in seen) :
                        for k in range(i,j) :
                            trajIndexTemp[k].append(len(AllPossiblePathlets))

                        seen[sub] = len(AllPossiblePathlets)
                        AllPossiblePathlets.append(sub)
                    else :
                        #print("FINDINDEX")
                        index = seen[sub]
                        #print("FOUNDINDEX")
                        for k in range(i,j) :
                            trajIndexTemp[k].append(index)

            #print(trajIndexTemp)
            TrajsIndexesNeededForPathletLearning.append(trajIndexTemp)
            #print("FINISHED A TRAJECTORY")
     
        print("FoundAllPossiblePathlets")
        return AllPossiblePathlets, TrajsIndexesNeededForPathletLearning


    def ExistsIndexesInPathlets(self,traj,e) :
        indexes = []
        for i in range(len(self.Pathlets)) :
            flag = False
            for j in self.Pathlets[i] :
                if j not in traj :
                    flag = True
                    break

            if flag :
                continue
            if e in self.Pathlets[i] :
                indexes.append(i)
        return indexes

    def SolvePathletLearningLinearly(self,trajectories,IndexesForConstraints) :
        problem = LpProblem("PathletLearning", LpMinimize)

        Xp = LpVariable.dicts("Xp", list(range(len(self.Pathlets))), cat="Binary")

        Xtp = []
        #-------------------
        #Constraints
        print("Adding Constraints\n1st Set Of Constraints")
        for i in range(len(trajectories)) :
            Xtp.append(LpVariable.dicts("Xtp"+str(i), list(range(len(self.Pathlets))), cat="Binary"))
            
            for j in range(len(Xtp[i])) :
                problem += Xtp[i][j] <= Xp[j]

            print(i)

        print("2nd Set Of Constraints")


        #print(IndexesForConstraints)
        for i in range(len(trajectories)) :

            for j in range(len(trajectories[i])) :
                #indexes = []
                #indexes = self.ExistsIndexesInPathlets(trajectories[i],j)
                #print(len(indexes))
                temp = 0
                for k in IndexesForConstraints[i][j] :
                    temp += Xtp[i][k]

                problem += temp == 1

            print(i)
        #-------------------
        #objective function
        print("Adding Objective Function")
        temp = 0
        for i in range(len(Xp)) :
            temp += Xp[i]

        l = 0.0001; #lamda
        for i in range(len(Xtp)) :
            for j in range(len(Xtp[i])) :
                temp += l*Xtp[i][j]

        problem += temp
        #print(problem)
        print("SolvingStarts!")

        problem.solve() #!!!

        PathletResults = []
        for i in range(len(self.Pathlets)) :
            PathletResults.append(Xp[i].varValue)
        #print(PathletResults)

        TrajsResults = []
        for i in range(len(trajectories)) :
            trajResult = []
            for j in range(len(self.Pathlets)) :
                trajResult.append(Xtp[i][j].varValue)
            TrajsResults.append(trajResult)
        #print(TrajsResults)
        
        return PathletResults,TrajsResults

    def MinimizePathletLearningResults(self,PathletResults) :
        #----------------------------------------------
        #Parakatw meiwnw to megethos twn dedomenwn mas
        indexes = []
        for i in range(len(PathletResults)) :
            if PathletResults[i] == 0 :
                indexes.append(i)

        #print("\nIndexes to Remove: ",indexes)

        self.Pathlets = np.array(self.Pathlets)
        PathletResults = np.array(PathletResults)
        self.TrajsResults = np.array(self.TrajsResults)

        self.Pathlets = np.delete(self.Pathlets, indexes)
        PathletResults = np.delete(PathletResults, indexes)
        self.TrajsResults = np.delete(self.TrajsResults, indexes, 1)


        NewTrajsResults = []
        for traj in self.TrajsResults :
            NewTraj = []
            counter = 1
            currentValue = traj[0]
            for i in traj[1:] :
                if currentValue == i :
                    counter = counter + 1
                else :
                    NewTraj.append((int(currentValue),counter))
                    counter = 1
                    currentValue = i
            NewTraj.append((int(currentValue),counter))
            NewTrajsResults.append(NewTraj)

        self.TrajsResults = NewTrajsResults


    def ReturnRealTraj(self,TrajResult) :
        RealTraj = []
        TotalTimes = 0
        for i in range(len(TrajResult)) :
            (Value,times) = TrajResult[i]
            if Value == 1 :
                for j in range(times) :
                    RealTraj = RealTraj + list(self.Pathlets[TotalTimes + j])

            TotalTimes = TotalTimes + times

        return RealTraj

    def ReturnAllTrajectoriesInAList(self) :
        RealTrajs = []
        for i in range(len(self.TrajsResults)) :
            RealTrajs.append(self.ReturnRealTraj(self.TrajsResults[i]))

        return RealTrajs

    def ReturnSpecificTrajectoryByIndex(self, index) :
        if index > len(self.TrajsResults) - 1 or index < 0:
            print("There are",len(self.TrajsResults),"trajectories but you asked for the",index)
        else :
            return self.ReturnRealTraj(self.TrajsResults[index])