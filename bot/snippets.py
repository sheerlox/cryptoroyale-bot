################################
# Click Play
################################
button_play = driver.find_element_by_xpath("//button[contains(text(), ' Play ')]")

action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(button_play, 5, 5)
action.click()
action.perform()

################################
# Get JS variable
################################
game_state = driver.execute_script("return game_state")


################################
# Get direction and angle
################################
posFrom = [-3, 2]
posTo = [2, 3]

direction = [posTo[0] - posFrom[0], posTo[1] - posFrom[1]]
angle = math.atan2(direction[1], direction[0]) * 180 / math.pi

print(direction, angle)