import argparse
import os
import random
import time
import numpy as np
import pandas as pd

def agent_move(agent, map_size) :
    available_move = []
    pos_y, pos_x = agent
    if pos_y > 0 : available_move.append('up')
    if pos_y < map_size-1 : available_move.append('down')
    if pos_x > 0 : available_move.append('left')
    if pos_x < map_size-1 : available_move.append('right')

    move = random.choice(available_move)
    if move == 'up' : pos_y -= 1
    elif move == 'down' : pos_y += 1
    elif move == 'left' : pos_x -= 1
    elif move == 'right' : pos_x += 1

    return (pos_y, pos_x)

def display(map, map_size, agent, try_count) :
    print(f'{try_count}번째 시도 중...')

    pos_y, pos_x = agent
    display_map = pd.DataFrame(np.round(map, 3))
    display_map.iloc[pos_y, pos_x] = '◎'
    display_map.iloc[map_size-1, map_size-1] = '★'

    print(display_map)

def erase_display(sleep) :
    time.sleep(sleep)
    os.system('cls' if os.name=='nt' else 'clear')

def update_reward(map, history, discount_rate) :
    reward = 1
    history.reverse()
    for hist in history :
        pos_y, pos_x = hist
        reward *= discount_rate
        map[pos_y, pos_x] = max(reward, map[pos_y, pos_x])

    return map

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='set parameters')
    parser.add_argument('--map_size', type=int, default=5, help='size of the map')
    parser.add_argument('--discount_rate', type=float, default=0.9, help='discount rate applied on reward')
    parser.add_argument('--display_sleep', type=float, default=0.1, help='sleep time when display')
    parser.add_argument('--update_sleep', type=float, default=1, help='sleep time when arrive at goal')
    args = parser.parse_args()

    map_size = args.map_size
    discount_rate = args.discount_rate
    display_sleep = args.display_sleep
    update_sleep = args.update_sleep

    try_count = 1
    map = np.zeros(shape=(map_size, map_size))
    while True :
        agent, history = (0,0), []
        while True : 
            display(map, map_size, agent, try_count)
            if agent == (map_size-1, map_size-1) : 
                print(f'\n목적지 도착! steps : {len(history)}')
                print('map에 reward 반영 중...')
                map = update_reward(map, history, discount_rate)
                time.sleep(update_sleep)
                erase_display(display_sleep)
                break

            erase_display(display_sleep)

            agent = agent_move(agent, map_size)
            history.append(agent)

        try_count += 1



        


