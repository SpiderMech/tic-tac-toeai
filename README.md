# tic-tac-toeai
Currently this project consist of the q learning agent and the game environment
Q-learing is a form of reinforcement learning, which means it learns by observing results, and improving its course of actions based on the results
The Q function, which the Q-learning player (agent) bases its course of action upon, and is stored tabularly.

<!!!> Q-Learning is not perfect, in that it is only as good as the player it trains against, and it has to play many games until it gets good (so it has seen all the game states)

Nonetheless, this script trains the agent against a random player, then plays against you the human player.

**********How to Play**********

7|8|9<br>
4|5|6<br>
1|2|3<br>

The above are the key mappings, i.e. centre of the board is key 5
your default symbol is cross (x)

Remeber that the agent is only as good as the player trains against, so for the q agent to be as good as you, you have to play many many games with it, sounds pretty useless right now? Yeah it is... so stay tuned for more sophisticated agents
