# tictactoe

#### Consists of two parts:

 * Game framework
     * Ability to play games
     * Ability to record games
     * Ability to play various types of players (see below)
 * Various types of players:
     * Random Player
     * Sophisticated Random Player (does not play illegal moves)
     * Basic AI Player (uses network trained on positions from games between Sophisticated Random Players)


#### Dependencies
 * TensorFlow & Keras
 * NumPy
 * Uses progress.py by vladignatyev (https://gist.github.com/vladignatyev/06860ec2040cb497f0f3)

#### To do
 * MinMax Player:
    * Change Board to (2, 3, 3)
    * Arbitrary Depth
 * Change board logic
 * Convultional Network
 * Train on Illegals
##### Later stuff
 * Generate numpy array instead of list of arrays
 * Create Q learning, Minimax and other AI players
 * Hard code a manual AI
 * GUI
