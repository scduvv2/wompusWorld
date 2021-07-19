from itertools import permutations
import WumpusLib
import random


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
        
    def play_game(self,iterations):
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
        iterationCount = int(iterations)
        self.Game.printBoard()
        # Iterate the max number of steps.
        for I in range (iterationCount):
            # Get the current percepts.
            Percepts = self.get_all_Percepts()
            # Call the agent function to get the action.
            NewAction = self.agent_func(Percepts)
            if NewAction== 'StopGame':
                print("Stopping the game as we hit a threat")
                break
            # Now do the wrapper for the steps.
            statusOfAction = self.Game.action_wrapper(NewAction)
            if NewAction=="Exit":
                break

def main():   
    agent = 'Reflex'
    iterations = 100
    NewGame = WumpusLib.WumpusGame(PrintMessages=True)
    if agent == 'Reflex':
        Agent = SimpleReflex(NewGame)
        Agent.play_game(iterations)
    elif agent == 'Model':
        Agent = ModelBasedReflex(NewGame)
        Agent.play_game(iterations)
    elif agent == 'Goal':
        Agent = GoalBasedAgent(NewGame)
        Agent.play_game(iterations)
    elif agent == 'Utility':
        Agent = UtilityBasedAgent(NewGame)
        Agent.play_game(iterations)
    elif agent == 'Learning':
        Agent = LearningAgent(NewGame)
        Agent.play_game(iterations)        
main()
