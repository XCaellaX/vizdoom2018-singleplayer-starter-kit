#!/usr/bin/env python3

import vizdoom as vzd
from random import choice
import os
import itertools

# Name your agent
#
# Note: The grading infrastructure will provide the expected agent name
# in the environment variable `CROWDAI_AGENT_NAME`
# If your agent does not use this environment variable then the score
# will not be counted against your crowdai user.
agent_name = "RandomDude"
server_agent_name = os.getenv("CROWDAI_AGENT_NAME", agent_name)

DEFAULT_WAD_FILE = "mock.wad"


def run_game():
    game = vzd.DoomGame()
    game.load_config("config/custom_config.cfg")
    # and select color
    # colors: 0 - green, 1 - gray, 2 - brown, 3 - red, 4 - light gray, 5 - light brown, 6 - light red, 7 - light blue
    color = 0
    game.set_doom_scenario_path(DEFAULT_WAD_FILE)
    # This will be internally overriden in the grading environment with the relevant WAD file

    game.add_game_args("-join localhost +name {agent_name} +colorset {colorset}".format(
        agent_name=server_agent_name,
        colorset=color
    ))

    game.set_console_enabled(True)
    game.set_window_visible(False)

    game.init()

    # 5 buttons:
    # MOVE_FORWARD
    # MOVE_RIGHT
    # MOVE_LEFT
    # TURN_LEFT
    # TURN_RIGHT
    # ATTACK

    buttons_num = game.get_available_buttons_size()
    actions = [list(action) for action in itertools.product([1, 0], repeat=buttons_num)]

    # Play until the game (episode) is over.
    while not game.is_episode_finished():

        if game.is_player_dead():
            # Use this to respawn immediately after death, new state will be available.
            game.respawn_player()

            # Or observe the game until automatic respawn.
            # game.advance_action();
            # continue;

        # Analyze the state ... or not
        s = game.get_state()
        # print(s)

        # Make your action.
        game.make_action(choice(actions))

        # Log time and frags/kills every ~10 seconds
        if s and s.number % 350 == 0:
            print("Time: {}, Kills: {}, Frags: {}",
                  game.get_episode_time(),
                  game.get_game_variable(vzd.GameVariable.KILLCOUNT),
                  game.get_game_variable(vzd.GameVariable.FRAGCOUNT))

    print("Episode FINISHED !")
    game.close()


if __name__ == "__main__":
    """
    The `run_game` function plays a single DoomGame, and the submitted agent
    should continue to try to join and play a new game as long as the server
    doesnot actively kill it.
    """
    while True:
        print("Connecting to Game Episode....")
        run_game()
