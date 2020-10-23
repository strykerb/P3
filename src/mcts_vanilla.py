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


    if node.untried_actions:
        return (node, state)
    else:
        favorite_child = choice(list(node.child_nodes.values()))
        highest_UCT = uct(favorite_child, identity)
        if identity == 'red':
            identity = 'blue'
        else:
            identity = 'red'
        for child in node.child_nodes:
            if (uct(node.child_nodes[child], identity) > highest_UCT):
               highest_UCT = uct(node.child_nodes[child], identity);
               favorite_child = node.child_nodes[child];
        return traverse_nodes(favorite_child, board, board.next_state(state, favorite_child.parent_action), identity)
    pass
    # Hint: return leaf_node


def uct(node, identity):
    win_rate = 0
    if identity == 'red':
        win_rate = 1 - (node.wins / node.visits)
    else:
        win_rate = node.wins / node.visits
    return win_rate + explore_faction * sqrt(log(node.parent.visits, 2) / node.visits)


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
    notTried = choice(node.untried_actions)
    newState = board.next_state(state, notTried)
    newNode = MCTSNode(parent=node, parent_action=notTried, action_list=board.legal_actions(newState))
    node.untried_actions.remove(notTried)
    node.child_nodes[notTried] = newNode
    return (newNode, newState)

    pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """

    if board.is_ended(state):
        return board.points_values(state)
    else:
        return rollout(board, board.next_state(state, choice(board.legal_actions(state))))
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    node.wins += won
    node.visits += 1
    if node.parent is not None:
        backpropagate(node.parent, won)
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """

    identity_of_bot = board.current_player(state)

    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        explore = traverse_nodes(node, board, sampled_game, board.current_player(sampled_game))
        newNode = expand_leaf(explore[0], board, explore[1])
        result = rollout(board, newNode[1])
        backpropagate(newNode[0], result[identity_of_bot])

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    rand_choice = choice(list(root_node.child_nodes.values()))
    best_move = rand_choice.parent_action
    best_win_rate = rand_choice.wins
    for next_node in root_node.child_nodes:
        if root_node.child_nodes[next_node].wins > best_win_rate:
            best_move = root_node.child_nodes[next_node].parent_action
            best_win_rate = root_node.child_nodes[next_node].wins
    return best_move
