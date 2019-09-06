import time
from PathletLearningClass import *
from PathletLearningScalableClass import *
from PathletLearningScalableDynamicClass import *
import pandas as pd
from ast import literal_eval
import gc
import random
from collections import Counter


def main() :

        """
        num_of_trajectories = 1000
        trainSet = pd.read_csv(
                'newTrips.csv', # replace with the correct path
                converters={"barefootSegmentsSequence": literal_eval},
                index_col='newTripID')

        trajectories = []

        x = 0
        for y in trainSet['barefootSegmentsSequence'] :
                trajectories.append(y)

                x = x + 1
                if x == num_of_trajectories :
                        break

        del trainSet
        gc.collect()
        
        """
        trajectories = []

        #seed for random
        random.seed(1234)

        for i in range(100) :
                trajectory = random.sample(range(1, 10), 5)
                trajectory.sort()
                trajectories.append(trajectory)

        print(trajectories)
        

        RealTrajListCounter = 0
        for T in trajectories :
                RealTrajListCounter = RealTrajListCounter + len(T)



        start = time.time() #Den prosthetw sto RunTime thn wra p thelei na diavasei to csv file
        
        print("Starting PathletLearning")
        plclass = PathletLearningClass(trajectories,1)
        print("Done PathletLearning")
        end = time.time()
        print("\nRunTime:",(end - start))

        start = time.time()
        PercentageOptimizer = True
        print("Starting UsagePercentageOptimization")
        plclass.TimesPathletsUsed(PercentageOptimizer)

        end = time.time()
        print("\nRunTime:",(end - start))

        print("\n\n\n\n")

        PathlCounter = 0
        for P in plclass.Pathlets :
                PathlCounter = PathlCounter + len(P)
        

        TrajsCounter = 0
        for T in plclass.TrajsResults :
                TrajsCounter = TrajsCounter + len(T)
        for T in plclass.NormalTrajectories :
                TrajsCounter = TrajsCounter + len(T)
        


        print(plclass.Pathlets,"   ",len(plclass.Pathlets),"   ",plclass.TrajsResults)
        print(type(plclass.Pathlets),type(plclass.TrajsResults))
        print(PathlCounter)
        print(TrajsCounter)
        print(RealTrajListCounter)



        AllTrajs = plclass.ReturnAllTrajectoriesInAList()

        print(sorted(AllTrajs)," !!! ",sorted(trajectories))

        #TA KANW SORT GIATI AN KANAME PERCENTAGE OPTIMIZE DN PAIZEI NA EINAI ME THN SEIRA
        AllTrajs = sorted(AllTrajs)

        trajectories = sorted(trajectories)

        print(len(AllTrajs),"   ",len(trajectories))

        flag = False
        for i in range(len(AllTrajs)) :
                        if not(AllTrajs[i] == trajectories[i]) :
                                flag = True

        if flag :
                print("trajectories not the same")

        
        """
        num_of_trajectories = 100
        trainSet = pd.read_csv(
                'newTrips.csv', # replace with the correct path
                converters={"barefootSegmentsSequence": literal_eval},
                index_col='newTripID')

        trajectories = []
        x = 0
        for y in trainSet['barefootSegmentsSequence'] :
                trajectories.append(y)

                x = x + 1
                if x == num_of_trajectories :
                        break

        del trainSet
        gc.collect()

        start = time.time() #Den prosthetw sto RunTime thn wra p thelei na diavasei to csv file

        plclass = PathletLearningScalableDynamicClass(trajectories)

        end = time.time()
        print("\nRunTime:",(end - start))

        AllTrajs = plclass.ReturnAllTrajectoriessInAList()
        print(plclass.Pathlets)

        flag = False
        for i in range(len(AllTrajs)) :
                if not(set(AllTrajs[i]) == set(trajectories[i])) :
                        flag = True

        if flag :
                print("trajectories not the same")


        #Writing - Reading Results from files

        PathletFileName = "Pathlets_"+str(num_of_trajectories)+"_l1"
        with open(PathletFileName, 'wb') as f:
                pickle.dump(plclass.Pathlets, f)

        TrajsResultsFileName = "TrajsResults_"+str(num_of_trajectories)+"_l1"
        with open(TrajsResultsFileName, 'wb') as f:
                pickle.dump(plclass.TrajsResults, f)

        del AllTrajs
        plclassTemp = PathletLearningScalableDynamicClass()

        with open(PathletFileName, 'rb') as f:
                plclassTemp.Pathlets = pickle.load(f)

        with open(TrajsResultsFileName, 'rb') as f:
                plclassTemp.TrajsResults = pickle.load(f)

        AllTrajs = plclassTemp.ReturnAllTrajectoriessInAList()

        flag = False
        for i in range(len(AllTrajs)) :
                if not(set(AllTrajs[i]) == set(trajectories[i])) :
                        flag = True

        if flag :
                print("trajectories not the same")
                
        """

if __name__ == '__main__':
    main()