import WumpusLib
import random
import sys


class SimpleReflex(object):
    """
    Define a basic simple reflecx object that plays the game.
    """
    def __init__(self, GameBoard):
        """
        Initialize with the working Game Board.
        We don't use this but it is fine to have.
        """
        self.Game = GameBoard

    def agent_func(self, Percepts):
        """
        This is a simple agent function that
        we can deal with.
        Obviously this will play very badly.
        """
        # If the percepts are empty go west.
        if (len(Percepts) == 0):
            goDirection = random.randint(1,4)
            if goDirection==1:
                return "GoEast"
            elif goDirection==2:
                return "GoWest"
            elif goDirection==3:
                return "GoNorth"
            else:
                return "GoSouth"
        # we are either in pit or wumpus ate us. game ends.
        elif ("inThreat" in Percepts):
            return 'StopGame'
        # If we see the gold pick it up.
        elif ("glint" in Percepts):
            return("PickupGold")
        # Otherwise just run north.
        elif ("exit" in Percepts):
            return("Exit")

        else:
            goDirection = random.randint(1,4)
            if goDirection==1:
                return "GoEast"
            elif goDirection==2:
                return "GoWest"
            elif goDirection==3:
                return "GoNorth"
            else:
                return "GoSouth"
            """implementation of more percepts"""
    def get_all_Percepts(self):
        Percepts = self.Game.get_percepts()
        # if the current position is a threat position, then no point in iterating and end the game.
        if self.Game.player_pos ==-1:
            Percepts.add("inThreat")
        return Percepts

    def play_game(self):
        """
        This function provides a simple loop to play the
        using this agent.  It assumes that the agent has
        been made and loaded with a board.  It then iteratively
        calls the method and repeats.
        Note that this pays no attention to the outcome of the
        action or check whether the agent is dead (i.e. did
        a move action that returns false) so it will play
        blindly indefinitely.
        """

        
        # Iterate the max number of steps.
        for I in range (100):           
            # Get the current percepts.
            Percepts = self.get_all_Percepts()
          # Call the agent function to get the action.
            NewAction = self.agent_func(Percepts)
            Last_action = NewAction
            if NewAction== 'StopGame':
                print("Stopping the game as we hit a threat")
                self.Game.printBoard()
                break
            # Now do the wrapper for the steps.
            statusOfAction = self.Game.action_wrapper(NewAction)
            if NewAction=="Exit":
                self.Game.printBoard()
                break
            self.Game.printBoard()


"""  before exiting the game this model verifies if the gold is picked in the last action. """
class ModelBasedReflex(object):
    """
    Define a basic simple reflecx object that plays the game.
    """

    def __init__(self, GameBoard):
        """
        Initialize with the working Game Board.
        We don't use this but it is fine to have.
        """
        self.Game = GameBoard
    def update_state(self,Curr_State, Last_Action,Percepts, Model):
        new_State =  dict(Curr_State)
        currentRoom = self.Game.player_pos
        new_State["currentRoom"]=currentRoom
        if "breeze" in Percepts:
            if not "breezeRooms" in new_State.keys():
                new_State["breezeRooms"]=[currentRoom]
            else:
                rooms =  new_State["breezeRooms"]    
                rooms.append(currentRoom)         
        if "stench" in Percepts:
            if not "stenchRooms" in new_State.keys():
                new_State["stenchRooms"]=[currentRoom]
            else:
                rooms =  new_State["stenchRooms"]    
                rooms.append(currentRoom)                            
        if Last_Action=='PickupGold':
            new_State["pickedUpGold"] =True
        elif Last_Action=='ShootNorth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead'] =True
            new_State["ArrowUsed"] =True
        elif Last_Action=='ShootEast':
            # not 100% sure if we get this feedback if wumpus is dead or not.
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead'] =True
            new_State["ArrowUsed"] =True
        elif Last_Action=='ShootWest':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead'] =True
            new_State["ArrowUsed"] =True
        elif Last_Action=='ShootSouth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead'] =True
            new_State["ArrowUsed"] =True
        return new_State

    def agent_func(self,Percepts, Curr_State, Last_Action):
        Model="transistion"

        New_State = self.update_state(Curr_State, Last_Action,Percepts, Model)
        """
        This is a simple agent function that
        we can deal with.
        Obviously this will play very badly.
        """
        # If the percepts are empty go west.
        if (len(Percepts) == 0):
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"
        # we are either in pit or wumpus ate us. game ends.
        elif ("inThreat" in Percepts):
            Action= 'StopGame'
        # If we see the gold pick it up.
        elif ("glint" in Percepts):
            Action=("PickupGold")
        # if we have stench and have not used arrow, shoot.
        elif ("stench" in Percepts) and 'ArrowUsed' not in New_State.keys():
            arrowDirections = ['ShootEast','ShootWest','ShootNorth','ShootSouth']
            shootArrowDirection = random.choice(arrowDirections)
            Action=(shootArrowDirection)
        # if gold is picked up and you are in exit box, then exit. otherwise continue
        elif ("exit" in Percepts) and ('pickedUpGold' in New_State.keys()):
            Action=("Exit")

        else:
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"

        return (Action,New_State)

    def get_all_Percepts(self):
        Percepts = self.Game.get_percepts()
        # if the current position is a threat position, then no point in iterating and end the game.
        if self.Game.player_pos ==-1:
            Percepts.add("inThreat")
        return Percepts

    def play_game(self):
        """
        This function provides a simple loop to play the
        using this agent.  It assumes that the agent has
        been made and loaded with a board.  It then iteratively
        calls the method and repeats.
        Note that this pays no attention to the outcome of the
        action or check whether the agent is dead (i.e. did
        a move action that returns false) so it will play
        blindly indefinitely.
        """
        
        Last_action='Begining'
        Curr_State= {}
        Model=set([])
        # Iterate the max number of steps.
        for I in range (100):
            # Get the current percepts.
            Percepts = self.get_all_Percepts()

            # Call the agent function to get the action.
            NewAction,Curr_State = self.agent_func(Percepts,Curr_State,Last_action)
            Last_action = NewAction
            if NewAction== 'StopGame':
                print("Stopping the game as we hit a threat")
                self.Game.printBoard()
                break
            # Now do the wrapper for the steps.
            statusOfAction = self.Game.action_wrapper(NewAction)
            if NewAction=="Exit":
                self.Game.printBoard()
                break
        self.Game.printBoard()
"""Goal set to avoid the pits and Wompus"""
class GoalBasedAgent(object):
    """
    Define a basic simple reflecx object that plays the game.
    """

    def __init__(self, GameBoard):
        """
        Initialize with the working Game Board.
        We don't use this but it is fine to have.
        """
        self.Game = GameBoard
    def update_state(self,Curr_State, Last_Action,Percepts):
        new_State =  dict(Curr_State)
        currentRoom = self.Game.player_pos
        new_State["player_pos"]=currentRoom
        if "breeze" in Percepts:
            if not "breezeRooms" in new_State.keys():
                new_State["breezeRooms"]=[currentRoom]
            else:
                rooms =  new_State["breezeRooms"]    
                rooms.append(currentRoom)         
        if "stench" in Percepts:
            if not "stenchRooms" in new_State.keys():
                new_State["stenchRooms"]=[currentRoom]
            else:
                rooms =  new_State["stenchRooms"]    
                rooms.append(currentRoom)                 
        if Last_Action=='PickupGold':
            new_State["pickedUpGold"]=True
        elif Last_Action=='ShootNorth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootEast':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootWest':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootSouth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        return new_State
    def check_pitDirection(self,New_State,Direction):
        game = self.Game
        if "breezeRooms" not in New_State.keys():
            potentialPits=[]
        else :
            potentialPits=[]    
            # the else will get the potential pits.
        player_pos = New_State['player_pos']
        if   (Direction == "GoNorth"):
           targetPosition = player_pos - 5
        elif (Direction == "GoSouth"):
             targetPosition = player_pos + 5
        elif (Direction == "GoEast"):
             targetPosition = player_pos + 1
        elif (Direction == "GoWest"):
            targetPosition = player_pos - 1
        if targetPosition not in potentialPits:
            return 'PitAvoided'
        else:
            print('avoid this direction: ',targetPosition,Direction)
            return 'Pit'

  

    def agent_func(self,Percepts, Curr_State, Last_Action):
        Model="transistion"

        New_State = self.update_state(Curr_State, Last_Action,Percepts)
        # goal will be set based on the current state and Percepts. for example if there is breeze, then goal is to avoid pit

        allDirections = ['GoEast','GoWest','GoNorth','GoSouth']

        # If the percepts are empty go west.
        if (len(Percepts) == 0):
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"
        # we are either in pit or wumpus ate us. game ends.
        elif ("inThreat" in Percepts):
            Action= 'StopGame'
        # If we see the gold pick it up.
        elif ("glint" in Percepts):
            Action=("PickupGold")
        # if we have breeze then avoid the pits
        elif ('breeze' in Percepts) or ('stench' in Percepts and 'ArrowUsed'  in New_State.keys()):
            goal_state = 'PitAvoided'
            for direction in allDirections:
                possible_state = self.check_pitDirection(New_State,direction)
                if possible_state==goal_state:
                   Action = direction
                   break
        # if we have stench and have not used arrow, shoot.
        elif ("stench" in Percepts) and 'ArrowUsed' not in New_State.keys():
            arrowDirections = ['ShootEast','ShootWest','ShootNorth','ShootSouth']
            shootArrowDirection = random.choice(arrowDirections)
            Action=(shootArrowDirection)
        # if gold is picked up and you are in exit box, then exit. otherwise continue
        elif ("exit" in Percepts) and ('pickedUpGold' in New_State.keys()):
            Action=("Exit")

        else:
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"

        return (Action,New_State)

    def get_all_Percepts(self):
        Percepts = self.Game.get_percepts()
        # if the current position is a threat position, then no point in iterating and end the game.
        if self.Game.player_pos ==-1:
            Percepts.add("inThreat")

        return Percepts

    def play_game(self):
        """
        This function provides a simple loop to play the
        using this agent.  It assumes that the agent has
        been made and loaded with a board.  It then iteratively
        calls the method and repeats.
        Note that this pays no attention to the outcome of the
        action or check whether the agent is dead (i.e. did
        a move action that returns false) so it will play
        blindly indefinitely.
        """

        Last_action='Begining'
        Curr_State= {}
        Model=set([])
        # Iterate the max number of steps.
        for I in range (100):
            # Get the current percepts.
            Percepts = self.get_all_Percepts()

            # Call the agent function to get the action.
            NewAction,Curr_State = self.agent_func(Percepts,Curr_State,Last_action)
            Last_action = NewAction
            if NewAction== 'StopGame':
                print("Stopping the game as we hit a threat")
                self.Game.printBoard()
                break
            # Now do the wrapper for the steps.
            statusOfAction = self.Game.action_wrapper(NewAction)
            if NewAction=="Exit":
                self.Game.printBoard()
                break
        self.Game.printBoard()

"""If the Wumpus is killed then that increases the happiness index and arrow is not wasted"""
class UtilityBasedAgent(object):
    """
    Define a basic simple reflecx object that plays the game.
    """

    def __init__(self, GameBoard):
        """
        Initialize with the working Game Board.
        We don't use this but it is fine to have.
        """
        self.Game = GameBoard
    def update_state(self,Curr_State, Last_Action,Percepts):
        new_State =  {}
        new_State = dict(Curr_State)
        if Last_Action=='PickupGold':
            new_State["pickedUpGold"]=True
        elif Last_Action=='ShootNorth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootEast':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootWest':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        elif Last_Action=='ShootSouth':
            if self.Game.wumpus_pos==-1:
                new_State['wumpusDead']=True
            new_State["ArrowUsed"]=True
        return new_State
    def check_pitDirection(self,New_State,Direction):
        game = self.Game
        if   (Direction == "GoNorth"):
           targetPosition = game.player_pos - 5
        elif (Direction == "GoSouth"):
             targetPosition = game.player_pos + 5
        elif (Direction == "GoEast"):
             targetPosition = game.player_pos + 1
        elif (Direction == "GoWest"):
            targetPosition = game.player_pos - 1
        if targetPosition in game._get_safe_rooms():
            return 'PitAvoided'
        else:
            print('avoid this direction: ',targetPosition,Direction)
            return 'Pit'

    def findWumpusDirection(self,New_State,Direction):

        game = self.Game
        if   (Direction == "ShootNorth"):
           targetPosition = game.player_pos - 5
        elif (Direction == "ShootSouth"):
             targetPosition = game.player_pos + 5
        elif (Direction == "ShootEast"):
             targetPosition = game.player_pos + 1
        elif (Direction == "ShootWest"):
            targetPosition = game.player_pos - 1
        if targetPosition == game.wumpus_pos:
            return Direction
        else:
            return 'SkipShoot'



    def agent_func(self,Percepts, Curr_State, Last_Action):
        Model="transistion"

        New_State = self.update_state(Curr_State, Last_Action,Percepts)
        # goal will be set based on the current state and Percepts. for example if there is breeze, then goal is to avoid pit

        allDirections = ['GoEast','GoWest','GoNorth','GoSouth']

        # If the percepts are empty go west.
        if (len(Percepts) == 0):
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"
        # we are either in pit or wumpus ate us. game ends.
        elif ("inThreat" in Percepts):
            Action= 'StopGame'
        # If we see the gold pick it up.
        elif ("glint" in Percepts):
            Action=("PickupGold")
        # if we have breeze then avoid the pits
        elif ('breeze' in Percepts) or ('stench' in Percepts and 'ArrowUsed'  in New_State.keys()):
            goal_state = 'PitAvoided'
            for direction in allDirections:
                possible_state = self.check_pitDirection(New_State,direction)
                if possible_state==goal_state:
                   Action = direction
                   break
        # if we have stench and have not used arrow, shoot in the direction of Wumpus to get the utility of killing the Wumpus
        elif ("stench" in Percepts) and 'ArrowUsed' not in New_State.keys():
            Potentials = ['ShootEast','ShootWest','ShootNorth','ShootSouth']

            shootArrowDirection = [self.findWumpusDirection(New_State,A) for A in Potentials]
            shootArrowDirection.sort()
            Action=(shootArrowDirection[0])
        # if gold is picked up and you are in exit box, then exit. otherwise continue
        elif ("exit" in Percepts) and ('pickedUpGold' in New_State.keys()):
            Action=("Exit")

        else:
            goDirection = random.randint(1,4)
            if goDirection==1:
                Action= "GoEast"
            elif goDirection==2:
                Action= "GoWest"
            elif goDirection==3:
                Action= "GoNorth"
            else:
                Action= "GoSouth"

        return (Action,New_State)

    def get_all_Percepts(self):
        Percepts = self.Game.get_percepts()
        # if the current position is a threat position, then no point in iterating and end the game.
        if self.Game.player_pos ==-1:
            Percepts.add("inThreat")
        return Percepts

    def play_game(self):
        """
        This function provides a simple loop to play the
        using this agent.  It assumes that the agent has
        been made and loaded with a board.  It then iteratively
        calls the method and repeats.
        Note that this pays no attention to the outcome of the
        action or check whether the agent is dead (i.e. did
        a move action that returns false) so it will play
        blindly indefinitely.
        """

        Last_action='Begining'
        Curr_State= {}
        Model=set([])
        # Iterate the max number of steps.
        for I in range (100):
            # Get the current percepts.
            Percepts = self.get_all_Percepts()

            # Call the agent function to get the action.
            NewAction,Curr_State = self.agent_func(Percepts,Curr_State,Last_action)
            Last_action = NewAction
            if NewAction== 'StopGame':
                print("Stopping the game as we hit a threat")
                self.Game.printBoard()
                break
            # Now do the wrapper for the steps.
            statusOfAction = self.Game.action_wrapper(NewAction)
            if NewAction=="Exit":
                self.Game.printBoard()
                break
        self.Game.printBoard()



def main():
    agent = sys.argv[1]
    iterations = int(sys.argv[2])
    print("running Agent : ",agent)
    print("Iterations running Agent : ",iterations)
    for  i in range(iterations):
        print("************************* game Iteration :",i,"*************************")                        
        NewGame = WumpusLib.WumpusGame(PrintMessages=True)
        NewGame.printBoard()
        if agent == 'Reflex':
            Agent = SimpleReflex(NewGame)
            Agent.play_game()
        elif agent == 'Model':
            Agent = ModelBasedReflex(NewGame)
            Agent.play_game()
        elif agent == 'Goal':
            Agent = GoalBasedAgent(NewGame)
            Agent.play_game()
        elif agent == 'Utility':
            Agent = UtilityBasedAgent(NewGame)
            Agent.play_game()
        elif agent == 'Learning':
            print("Learning Agent not Impelemented")
            exit
        NewGame.printBoard()
main()
