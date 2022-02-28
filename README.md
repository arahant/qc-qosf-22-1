# A Tic-tac-toe Quantum algorithm

## Logic

Given any state, the goal of the algorithm is to find the best results with the highest probability.

### Classical logic:

1. generate states for all possible moves, for both the player and the bot.

2. Calculate the probability for each move

3. Repeat the process, for each of this state,

    a. by passing the new state

    b. and passing in the corresponding probability * passed probability

4. When we reach the end state, which is

    a. when the bot wins

    b. when the player wins

    c. the stats is a draw

    d. calculate the probability of this state, and return it

5. for every return value from the recursion call for a state

    a. update the probability,

    b. the state with the highest new probability is the best move

### Quantum logic:

1. Consider each state as a qubit of size 9

2. The given qubit is as follows:

    a. the filled cells have values |1⟩ or |0⟩

    b. the empty cells/qubits are borrowed as:

        i. |0⟩, if the assumption is that bot is going to win by default

        ii. |1⟩, if the assumption is that player is going to win by default

3. Each bot move sets that particular qubit as |0⟩

4. Based on the logic above, the player sets the qubit with the highest probability as |1⟩

    a. setting of the qubit is another logic, which involves quantum gates

### Algorithm for player move (setting qubit to |1⟩):

1. We know that from the previous move the latest qubit which was set to |1⟩

2. We then use an extra carryover qubit (|0⟩) and perform a CX on it

3. This sets the extra qubit to |1⟩

### Notes

1. The classical and quantum algorithm are the same

2. Where the quantum algorithm differes is in the player move, which sets a qubit to |1⟩

3. The challenge is in setting a qubit to |1⟩, becase the actual state of the rest of the qubits is unknown apriori

    a. To make process this simpler, we make the assumption that the extra carry over qubit is of state |0⟩

4. If the extra qubits were in a mixed state, i.e., (p1 x |1⟩ + p2 x |0⟩)

    a. then we would have to perform a rotation operation on this qubit, to get |1⟩

    b. We, of course, need to know the values, p1 and p2

    c. to make this simpler, and have p1=p2, in which case, the extra qubit would be in a hadamard state

5. So, the player move, which sets the extra qubit to |1⟩, depends on the state of the extra qubit

    a. if it's |0⟩, the player move is a CX operation

    b. if it's a mixed state, the player move is a rotation operation

## Optimization

### Optimization in logic:

1. For every state, the current logic is a brute force, which iterates through every possible state

2. This can be optimized as follows:

    a. For a state, we match with every win state, which is basically an AND operation

    b. the bigger the match, larger is the score

    c. we can rank the possible states based on this score, and choose the one with the highest score

    d. this optimizes considerably, because we're not iterating through every possible state, but the one with the highest match

3. However, it might not result in a win, as a match doesn't mean a potential win
    a. this optimization algorithm can be improved upon

    b. but the brute force guarantees the win, with the best probability

### Optimization in player's move:

To optimize the qubit setting algorithm, we can make these assumptions:

1. The extra qubits are all set to |0⟩ each, which would make player move a CX operation

2. The extra qubits are each in a mixed state, which would make the player move an Rx operation

Depending on the complexity of both of these we can choose the one that results in a better optimization.

### Optimization in the end circuit

Finally, at the end of the game, we get a quantum circuit.
Now, we can also perform circuit optimization on this, without affecting the end result too much

## Implementation

### Current implementation

1. I've primarily implemented the logic, but only the classical algorithm for setting a qubit to |1⟩

3. I've implemented the brute force algorithm, which generates the entire decision tree for a given state.

4. This program works for _any_ given state, which includes the example state 1, bonus state, and others.

5. To run the program, run each command individually:
    ```
    git clone https://github.com/arahant/qc-qosf-22-1.git
    cd qc-qosf-22-1
    python main.py 1001xx0xx 2
    ```
    a. Replace `1001xx0xx` with any state, and 2 with any value for maximum steps

    b. Change `LOGGING = True` in `models.py`, to see the log of the entire decision tree. The log outputs for example 1 and example 2 are in `output1.txt` and `output2.txt`, respectively.

### Next steps

1. One of the next steps would be to optimize the brute force method which gets _all possible_ next states, and replace it with an algorithm which only gets **most probabilistic** next steps.

2. The quantum version, as I mentioned before, can be implemented using a CX gate or a Rx gate, depending on the state of the extra, borrowed qubit.

3. Generate a circuit for the quantum version of the algorithm, and attempt quantum circuit optimization.

## Result

### Example 1: 1001xx0xx

```
Given Inputs:
 Initial qubit state: |1001..0..⟩
 Player's initial positions: {1, 4}
 Bot's initial positions: {2, 3, 7}
 Empty cells at:  {8, 9, 5, 6}

Final Qubits 	Resultant Qubit    Probability   Steps   Player's moves
|100111000⟩ 	 |....11.00⟩ 	   0.125 	 2 	 [(1, 4, 6, 5), (1, 4, 5, 6)]
|100110001⟩ 	 |....10.01⟩ 	   0.125     	 2 	 [(1, 4, 9, 5), (1, 4, 5, 9)]
```

### Example 2 (bonus question): 1001xxxxx

```
Given Inputs:
 Initial qubit state: |1001.....⟩
 Player's initial positions: {1, 4}
 Bot's initial positions: {2, 3}
 Empty cells at:  {5, 6, 7, 8, 9}

Final Qubits 	 Resultant Qubit   Probability   Steps   Player's moves
|100100100⟩ 	 |....00100⟩ 	   0.25 	 1 	 [(1, 4, 7)]
|100101100⟩ 	 |....01100⟩ 	   0.125 	 2 	 [(1, 4, 6, 7)]
|100100101⟩ 	 |....00101⟩ 	   0.125 	 2 	 [(1, 4, 9, 7)]
|100111000⟩ 	 |....11000⟩ 	   0.125 	 2 	 [(1, 4, 6, 5), (1, 4, 5, 6)]
|100110001⟩ 	 |....10001⟩ 	   0.125 	 2 	 [(1, 4, 5, 9), (1, 4, 9, 5)]
|100100110⟩ 	 |....00110⟩ 	   0.125 	 2 	 [(1, 4, 8, 7)]
|100110100⟩ 	 |....10100⟩ 	   0.125 	 2 	 [(1, 4, 5, 7)]
```

### Example state 3: 10010xxxx

```
Given Inputs:
 Initial qubit state: |10010....⟩
 Player's initial positions: {1, 4}
 Bot's initial positions: {2, 3, 5}
 Empty cells at:  {8, 9, 6, 7}

Final Qubits 	 Resultant Qubit   Probability   Steps   Player's moves
|100100100⟩ 	 |.....0100⟩ 	   0.25 	 1 	 [(1, 4, 7)]
|100100110⟩ 	 |.....0110⟩ 	   0.125 	 2 	 [(1, 4, 8, 7)]
|100101100⟩ 	 |.....1100⟩ 	   0.125 	 2 	 [(1, 4, 6, 7)]
|100100101⟩ 	 |.....0101⟩ 	   0.125 	 2 	 [(1, 4, 9, 7)]
```
