import itertools
import time

#DL = DescriptionLength
def DLTraj(trajectory, PathletDic,MinResult) :
    MinNewTraj = [0] * 1000000

    #Pithanes kathgories gia to trajectory se sxesh me to PathletDic
    NewTrajs = list(itertools.product([0, 1], repeat=len(PathletDic)))
    
    for NewTraj in NewTrajs :
        
        #Pairnw olous tous dunatous sundiasmous twn Pathlets
        PathletIndexesToCheck = []
        index = 0
        for i in NewTraj :
            if i == 1 :
                PathletIndexesToCheck.append(index)
            index += 1
        
        #An exoume vrei me ligotera tote dn xreiazetai na to psaksoume kai pame sto epomeno
        if MinResult < len(PathletIndexesToCheck) :
            continue
        
        for i in range(0,len(PathletIndexesToCheck)) :
            #pairnoume ola ta combinations gia na vroume an sumplhrwnete to trajectory
            CertainIndexes = list(itertools.combinations(PathletIndexesToCheck, i + 1))
       
            for indexes in CertainIndexes :
                CheckPathlet = []

                #Ftiaxnw gia na dw an dhmiourgite to idio Path me to trajectory
                for index in indexes :
                    CheckPathlet = CheckPathlet + PathletDic[index]
                
                #Elegxos omoiothtas me to trajectory
                if len(CheckPathlet) != len(trajectory) :
                    continue
                else :
                    if trajectory == CheckPathlet :
                        
                        if MinResult > i + 1 :
                            
                            MinNewTraj = NewTraj
                            MinResult = i + 1

    #Epistrefw to allagmeno Trajectory me 0/1 gia kathe Pathlet tou dictionary
    #kai ton arithmo twn 1
    return MinNewTraj,MinResult

#Epistrefei to DL tou Pathdic
def DLPathlDic(PathletDic) :
    dl = 0
    for pathlet in PathletDic :
        dl += len(pathlet)
    return dl


#Vasikh sunarthsh Vriskw PathletDic kai NewTrajectories
def MakePathletDicAndNewTrajs(trajectories) :
    PathletDic = []

    for trajectory in trajectories :

        #Parakatw prosthetw sto PathletDic ola ta puthana subpathes
        for i in range(len(trajectory)) :
            for j in range(i + 1,len(trajectory) + 1) :
                if (trajectory[i:j] not in PathletDic) :
                    PathletDic.append(trajectory[i:j])

                    
    NewTrajectories = []
    MinPathletDic = []
    MinResult = 1000000

    for i in range(0,len(PathletDic)) :
        #Pairnw ola ta Combinations gia to PathletDic sumfwna me to oliko
        CertainPathletDics = list(itertools.combinations(PathletDic, i + 1))
        for PathletD in CertainPathletDics :
            NewTrajs = []
            #Sumfwna me ton algorithmo to DL tou PathletDic
            Result = DLPathlDic(PathletD)
            #An exoume hdh kalutero apotelesma psaxnoume to epomeno PathletDic
            if (Result > MinResult) :
                continue
            #Parakatw trexoume to DLtraj gia kathe trajectory
            for j in range(len(trajectories)) :
                NewTraj,res = DLTraj(trajectories[j],PathletD,MinResult)
                NewTrajs.append(NewTraj)
                #Prosthetoume to apotelesma sumfwna me ton tupo
                Result += res
                #An opoiadhpote stigmh exoume kalutero result pame sto epomeno
                if (Result > MinResult) :
                    break

            if (Result < MinResult) :
                NewTrajectories = NewTrajs
                MinPathletDic = PathletD
                MinResult = Result

    #Epistrefw ta kalutera Newtrajectories kai To PathletDic
    return NewTrajectories,MinPathletDic

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

start = time.time()

#Thewroume oti Grid 4x4
trajectories=[]

trajectories.append([(0,0),(1,1),(1,2),(3,2)])
trajectories.append([(0,0),(1,1),(1,3)])
trajectories.append([(1,2),(3,2),(3,3)])

NewTrajectories,MinPathletDic = MakePathletDicAndNewTrajs(trajectories)

print(NewTrajectories)
print(MinPathletDic)

end = time.time()
print(end - start)
