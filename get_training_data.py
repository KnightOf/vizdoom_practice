from vizdoom import *
import random, time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# left   239.97654724121094
# right -175.97657775878906

def main():
    training_data_answer = np.zeros([movement_count,pic_per_episode_count],dtype= np.uint8)
    shoot_time = 0
    for move_step in range(movement_count):
        game.init()
        game.new_episode()
        for pic_per_episode in range(pic_per_episode_count):

            obj = game.get_state().labels
            distance = obj[0].object_position_y - obj[1].object_position_y
           
            #monster - player
            print(abs(distance))
            if abs(distance) > 10:
                if distance > 0:
                    #print("left",left)
                    training_data_answer[move_step,pic_per_episode] = 0b0100
                elif distance < 0:
                    #print("right",right)
                    training_data_answer[move_step,pic_per_episode] = 0b0010
            else:
                #print("shoot",shoot)
                training_data_answer[move_step,pic_per_episode] = 0b0001
                shoot_time+1

            s1 = game.get_state().screen_buffer
            
            current_name = './training_data/'+str(move_step)+'-'+str(pic_per_episode)
            plt.imshow(s1)
            plt.axis('OFF')
            plt.savefig(current_name,bbox_inches='tight')
            for randomlyWalk in range(50):
                game.make_action(random.choice([right,left]))
            
            if game.is_episode_finished():
                game.new_episode() 
    np.save('answer',training_data_answer)
    print(np.load('answer.npy'))      
    print(shoot_time)

if __name__ == '__main__':
    game = DoomGame()
    game.load_config("D:/Users/user/Anaconda3/envs/vizdoom/Lib/site-packages/vizdoom/scenarios/basic.cfg")
    game.set_screen_format(ScreenFormat.GRAY8)
    game.set_labels_buffer_enabled(True)
    #game.set_window_visible(False)
    game.init()
    
    #game.add_available_game_variable(GameVariable.POSITION_X)
    game.add_available_game_variable(GameVariable.POSITION_Y)
    
    left  = [1,0,0]
    right = [0,1,0]
    shoot = [0,0,1]

    movement_count = 10
    pic_per_episode_count = 20

    main()
