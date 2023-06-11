#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows,num_cols),bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    
    return dig_nd(game,(row,col))

def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    return render_nd(game,xray)

def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    board=render_2d_locations(game,xray)
    str_rep=''
    for row in range(len(board)):
        for col in range(len(board[row])):
            str_rep=str_rep+board[row][col]
        if row==len(board)-1:
            break
        str_rep=str_rep+'\n'
    return str_rep


# N-D IMPLEMENTATION
def deep_copy_clone(arr):
    '''
    creates a new instance passed through with items in new locations in memeory
    '''
    temp=[]
    if type(arr[0])==list:
        for lists in arr:
            temp.append(deep_copy_clone(lists))
    else:
        temp=arr[:]
    return temp
def truth_search(arr,item_search,intial=True):
    '''
    return the total number of False booleans in the hidden lists
    '''
    truth_count=0
    if type(arr[0])==list:
        for lists in arr:
            truth_count+=truth_search(lists,item_search,False)
        return truth_count
    if intial==False:
        small_count=0
        for item in arr:
            if item==item_search:
                small_count+=1 
        return small_count
    else:
        return truth_count
        



def create_nested_lists(dimensions,lists=[],current_depth=1,item=0):
    '''
    creates a nested list of lists of etc. for the n-dimensional board
    '''
    newList=[]
    if not lists:
        for _ in range(dimensions[-1]):
            newList.append(item)
    else: 
        for _ in range(dimensions[-current_depth]):
            newList.append(lists)
    if current_depth==len(dimensions):
        return newList
    else:
        return create_nested_lists(dimensions,newList,current_depth+1)
    
def edit_value(map,locations,item):
    '''
    loops through the list of locations to make changes to specific locations
    '''
    for location in locations:
        mutable_pointer=map
        #print(location)
        for i,coordinate in enumerate(location):
            if i==len(location)-1:
                break
            #print(mutable_pointer)
            #print(coordinate)
            mutable_pointer=mutable_pointer[coordinate]
            
        if type(item)==str or type(item)==bool:
            mutable_pointer[location[len(location)-1]]=item
        else:
            try:
                mutable_pointer[location[len(location)-1]]=(int(mutable_pointer[location[len(location)-1]])+item)
            except:
                pass
    return map
def get_value(map,location):
    '''
    returns the value at a certain location on the board
    '''
    mutable_pointer=map
    for i,coordinate in enumerate(location):
            if i==len(location)-1:
                break
            #print(mutable_pointer)
            #print(coordinate)
            mutable_pointer=mutable_pointer[coordinate]
        
    return mutable_pointer[location[len(location)-1]]
def compute_neighbor_function(n):
    '''
    returns a list of lists containing values between -1 and 1 for neighboring coordinates
    '''
    increment=[[]]
    def modify(current=[]):
        new=[current[:],current[:],current[:]]
        for i in range(-1,2):
            new[i].append(i)
        return new
    while len(increment[0])!=n:
        temp=increment.pop(0)
        increment.extend(modify(temp))
    same=[]
    for _ in range(n):
        same.append(0)
    increment.remove(same)
    return increment
def compute_neighbor(coor,dimensions):
    '''
    takes the list of lists generated above and applies it to the coordinate
    '''
    neighbor=[]
    increment_list=compute_neighbor_function(len(coor))
    for increment in increment_list:
        new_coor= tuple(v1+v2 for v1,v2 in zip(increment,coor))
        valid_coor=True
        for i,val in enumerate(new_coor):
            if val<0 or val>=dimensions[i]:
                valid_coor=False
                break
        if valid_coor:
            neighbor.append(new_coor)
    return neighbor







        



def add_bombs(empty_map,bombs,dimensions):
    '''
    add bombs and numbers to the map
    '''
    bomb_neighbors=[]
    for bomb in bombs:
        bomb_neighbors.extend(compute_neighbor(bomb,dimensions))
    #print(bomb_neighbors)
    map_with_bombs=edit_value(empty_map,bombs,'.')
    map_with_warnings_and_bombs=edit_value(map_with_bombs,bomb_neighbors,1)
    return map_with_warnings_and_bombs
    



    
    
    



def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    game={
        'board':[],
        'dimensions':dimensions,
        'state': 'ongoing',
        'hidden':[]
    }
    empty_board=deep_copy_clone(create_nested_lists(dimensions))
    filled_board=add_bombs(empty_board,bombs,dimensions)
    game['board']=filled_board
    hidden_board=deep_copy_clone(create_nested_lists(dimensions,item=True))
    game['hidden']=hidden_board
    return game


    




def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """
    total_square=1
    for num in game['dimensions']:
            total_square*=num
    non_bombs=total_square-truth_search(game['board'],'.')
    def recursive_helper(game,coordinates):
        if game['state']=='victory' or game['state']=='defeat' or get_value(game['hidden'],coordinates)==False:
            return 0
        edit_value(game['hidden'],[(coordinates)],False)
        current_val=get_value(game['board'],coordinates)
        if current_val=='.':
            game['state']='defeat'
            return 1
        if current_val==0:
            neighbors=compute_neighbor(coordinates,game['dimensions'])
            total=1
            for nearby in neighbors:
                if get_value(game['hidden'],nearby)==True:
                    total+=recursive_helper(game,nearby)
            return total
        return 1
    squares_dug=recursive_helper(game,coordinates)
    if truth_search(game['hidden'],False)==non_bombs:
            game['state']='victory'
    return squares_dug
    

def create_board(arr,truth_list,xray):
    '''
    creates a rendered board
    '''
    temp=[]
    if type(arr[0])==list:
        for lists,truth in zip(arr,truth_list):
            temp.append(create_board(lists,truth,xray))
    else:
        if xray:
            for val in arr:
                if val==0:
                    temp.append(' ')
                else:
                    temp.append(str(val))
        else:
            for val,truth in zip(arr,truth_list):
                if truth==True:
                    temp.append('_')
                else:
                    if val==0:
                        temp.append(' ')
                    else:
                        temp.append(str(val))
    return temp

    

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    return create_board(game['board'],game['hidden'],xray)


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    '''
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    '''
    g = {'dimensions': (2, 4, 2),
          'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
                    [['.', 3], [3, '.'], [1, 1], [0, 0]]],
          'hidden': [[[True, True], [True, False], [False, False],
                    [False, False]],
                   [[True, True], [True, True], [False, False],
                    [False, False]]],
          'state': 'ongoing'}
    print(render_nd(g,True)==[[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]])


    

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
