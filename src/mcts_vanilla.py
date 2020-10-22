from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.


    Adversarial planning – the bot will be simulating both players’ turns. This
    requires you to alter the UCT function (during the tree traversal/selection phase) on the
    opponent’s turn. Remember: the opponent’s win rate (X¬j) = (1 – bot’s win rate).

    """
    """
    Pseudo code:
    highest_UCT = 0
    favorite_child = None
    if node.untried_actions:

        return node
    else
        if identity == 'red':
            indentity = 'blue'
        else:
            identity = 'red'
        for child in node.child_nodes:
            if (uct(child, identity) > highest_UCT):
                highest_UCT = uct(child, identity);
                favorite_child = child;
        traverse_nodes(favorite_child, identity)
    """


    pass
    # Hint: return leaf_node

def uct(node, identity):
    win_rate = 0
    if identity == 'red':
        win_rate = 1-(node.wins/node.visits)
    else:
        win_rate = node.wins/node.visits
    return win_rate + explore_faction*sqrt(log(node.parent.visits, 2)/node.visits)


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    """
    pseudo code
    untried action = node.untried_actions() && board.legal_actions(state)
    node.child = untried action
    return node.child
    """

    pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """

    """
    pseudo code
    while game not over:
        board.next_state(state, choice(board.legal_actions(state)))

        current_player = player1
    while not board.is_ended(state):
        last_action = current_player(board, state)
        state = board.next_state(state, last_action)
        current_player = player1 if current_player == player2 else player2
    print("Finished!")

    """
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if won:
        ++node.wins
    ++node.visits
    if node.parent != None:
        backpropagate(node.parent, won)
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    """
    pseudo code
    explore = traverse_nodes(root_node, board, sampled_game, board.current_player(sampled_game))
    expand_leaf(explore)



    rollout(board, state)


    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
