#!/usr/bin/python

import sys, math
from time import sleep
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/usr/bin/brave-browser"
driver = webdriver.Chrome(options=options, executable_path="/usr/bin/chromedriver")

def show_mouse(driver):
    driver.execute_script("""var seleniumFollowerImg=document.createElement('img');
    seleniumFollowerImg.setAttribute('src', 'data:image/png;base64,'
    + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
    + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
    + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
    + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
    + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
    + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
    + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
    + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
    + 'dAAAAABJRU5ErkJggg==');
    seleniumFollowerImg.setAttribute('id', 'selenium_mouse_follower');
    seleniumFollowerImg.setAttribute('style', 'position: absolute; z-index: 99999999999; pointer-events: none;');
    document.body.appendChild(seleniumFollowerImg);
    jQuery(document).mousemove(function(e){
    jQuery("#selenium_mouse_follower").css('left', e.pageX - 3);
    jQuery("#selenium_mouse_follower").css('top', e.pageY - 5);
    });""")

def clean_players(players):
    names = ['id', 'username', 'HP', 'class', 'mode_int', 'place', 'pos_x', 'pos_y', 'to_x', 'to_y', 'inertia_x', 'inertia_y']
    # formats = ['u4', 'U3', 'f8', 'U1', 'i', 'i', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8']

    buffer = pd.DataFrame(columns=names)

    for id, player in players.items():
        new_player = {
            'id': id,
            'username': player['username'],
            'HP': player['HP'],
            'class': player['class'],
            'mode_int': player['mode_int'],
            'place': player['place'],
            'pos_x': None,
            'pos_y': None,
            'to_x': None,
            'to_y': None,
            'inertia_x': None,
            'inertia_y': None,
        }

        if 'pos' in player and not pd.isnull(player['pos']):
            new_player['pos_x'] = player['pos']['x']
            new_player['pos_y'] = player['pos']['y']

        if 'pos' in player and not pd.isnull(player['to']):
            new_player['to_x'] = player['to']['x']
            new_player['to_y'] = player['to']['y']

        if 'pos' in player and not pd.isnull(player['inertia']):
            new_player['inertia_x'] = player['inertia']['x']
            new_player['inertia_y'] = player['inertia']['y']
        
        buffer = buffer.append(pd.DataFrame([tuple(new_player.values())], columns=names), ignore_index=True)
    
    return buffer

def clean_loots(loots):
    names = ['id', 'class', 'abouttodie', 'pos_x', 'pos_y']
    # formats = ['U4', 'U1', 'u1', 'f8', 'f8']

    buffer = pd.DataFrame(columns=names)

    for id, loot in loots.items():
        new_loot = {
            'id': id,
            'class': loot['t'],
            'abouttodie': loot['abouttodie'],
            'pos_x': None,
            'pos_y': None,
        }

        if 'pos' in loot and not pd.isnull(loot['pos']):
            new_loot['pos_x'] = loot['pos']['x']
            new_loot['pos_y'] = loot['pos']['y']

        buffer = buffer.append(pd.DataFrame([tuple(new_loot.values())], columns=names), ignore_index=True)
    
    return buffer

calc_distance = lambda e1, e2: math.sqrt(math.pow(e1['pos_x'] - e2['pos_x'], 2) + math.pow(e1['pos_y'] - e2['pos_y'], 2))

calc_angle = lambda e1, e2: math.atan(e2['pos_y'] - e1['pos_y'] / e2['pos_x'] - e1['pos_x'])

calc_size = lambda e: math.log2(max(20, e['HP'])) * 7.5

try:
    driver.get("https://cryptoroyale.one/training/")

    # button_play = driver.find_element_by_xpath("//button[contains(text(), ' Play ')]")
    button_play = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), ' Play ')]")))

    # show_mouse(driver)

    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(button_play, 10, 10)
    action.pause(2).click().perform()

    sleep(3)

    while True:
        sleep(1)

        game_state = driver.execute_script("return game_state")
        user_state = driver.execute_script("return user_state")

        print('--------------------------------------------------')
        print('stage: ' + game_state['cycle']['stage'])
        print('timer: ' + str(int(game_state['cycle']['timer'])))

        if (game_state['cycle']['stage'] == 'pre-game' or
            game_state['cycle']['stage'] == 'post-game' or
            len(game_state['players']) == 0 or
            len(game_state['loot']) == 0):
            continue

        players_df = clean_players(game_state['players'])
        loots_df = clean_loots(game_state['loot'])

        players_df['size'] = players_df.apply(lambda x: calc_size(x), axis=1)

        # if we are playing, select our player. else take the first one
        if user_state['cloud']['playing'] == True and user_state['cloud']['pid']:
            print('PLAYING, PLAYER ID FOUND: %s' % user_state['cloud']['pid'])
            our_player = players_df.loc[players_df['id'] == str(user_state['cloud']['pid'])].iloc[0]
            players_df = players_df.drop(players_df.loc[players_df['id'] == str(user_state['cloud']['pid'])].index)
        else:
            our_player = players_df.iloc[0]
            players_df = players_df.drop(players_df.iloc[0].index)

        players_df['distance'] = players_df.apply(lambda x: calc_distance(our_player, x), axis=1)
        players_df['angle'] = players_df.apply(lambda x: calc_angle(our_player, x), axis=1)

        loots_df['distance'] = loots_df.apply(lambda x: calc_distance(our_player, x), axis=1)
        loots_df['angle'] = loots_df.apply(lambda x: calc_angle(our_player, x), axis=1)

        # print('--------------')
        # print('OUR PLAYER')
        # print(our_player)
        # print('--------------')
        # print('OTHER PLAYERS')
        # print(players_df)
        # print('--------------')
        # print('LOOTS')
        # print(loots_df)
        # print('--------------')


        nearest_loot = loots_df.loc[loots_df['distance'] == loots_df['distance'].min()].iloc[0]
        # print('--------------')
        # print('NEAREST LOOT')
        # print(nearest_loot)
        # print('--------------')

        mouse_position_x = ((our_player['size']) * math.cos(nearest_loot['angle']) + our_player['pos_x'])
        mouse_position_y = ((our_player['size']) * math.sin(nearest_loot['angle']) + our_player['pos_y'])

        print('--------------')
        print('MOUSE POSITION')
        print(" Loot position: %f / %f" % (nearest_loot['pos_x'], nearest_loot['pos_y']))
        print("Mouse position: %f / %f" % (mouse_position_x, mouse_position_y))
        print('--------------')
        
        driver.execute_script("user_state.local.mousecoords = { 'x': %f, 'y': %f }" % (nearest_loot['pos_x'] * 0.73, nearest_loot['pos_y'] * 0.73))

        # boost every tick
        action = webdriver.common.action_chains.ActionChains(driver)
        action.click().perform()

    driver.close()
except:
    driver.close()
    raise sys.exc_info()[0]

# posFrom = [0, 0]
# posTo = [1, -1]

# # print(math.atan2(posFrom[1] - posTo[1], posFrom[0] - posTo[0]))
# # print(math.atan2(posFrom[1] - posTo[1], posFrom[0] - posTo[0]) * 360 / math.pi)

# print(math.atan((posFrom[1] - posTo[1]) / (posFrom[0] - posTo[0])))
# print(math.degrees(math.atan((posFrom[1] - posTo[1]) / (posFrom[0] - posTo[0]))))