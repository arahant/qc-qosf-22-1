# A Tic-tac-toe Quantum algorithm

## Logic

Given any state, the goal of the algorithm is to find win states with the highest probabilities.

### Classical logic:

1. generate states for all possible moves, for both the player and the bot.
1. Calculate the probability for each move
1. Repeat the process, for each of this state,
    1. by passing the new state
    1. and passing in the corresponding probability * passed probability
1. When we reach the end state, which is
    1. when the bot wins
    1. when the player wins
    1. the stats is a draw
    1. calculate the probability of this state, and return it
1. for every return value from the recursion call for a state
    1. update the probability,
    1. the state with the highest new probability is the best move

### Quantum logic:

1. Consider each state as a qubit of size 9
1. The given qubit is as follows
    1. the filled cells have values `|1⟩` or `|0⟩`
    1. the empty cells/qubits are borrowed as:
        1. `|0⟩`, if the assumption is that bot is going to win by default
        1. `|1⟩`, if the assumption is that player is going to win by default
1. Each bot move sets that particular qubit as `|0⟩`
1. Based on the logic above, the player sets the qubit with the highest probability as `|1⟩`
    1. Setting the qubit is another logic, which involves quantum gates

### Player's move (setting qubit to `|1⟩`):

1. We know that from the previous move the latest qubit which was set to `|1⟩`
1. We then use an extra carryover qubit (`|0⟩`) and perform a `CX` on it
1. This sets the extra qubit to `|1⟩`

### Notes

1. The classical and quantum algorithm are the same
1. Where the quantum algorithm differes is in the player move, which sets a qubit to `|1⟩`
1. The challenge is in setting a qubit to `|1⟩`, becase the actual state of the rest of the qubits is unknown apriori
    1. To make process this simpler, we make the assumption that the extra carry over qubit is of state `|0⟩`
1. If the extra qubits were in a mixed state, i.e., (p1 x `|1⟩` + p2 x `|0⟩`)
    1. then we would have to perform a rotation operation on this qubit, to get `|1⟩`
    1. We, of course, need to know the values, p1 and p2
    1. to make this simpler, and have p1=p2, in which case, the extra qubit would be in a hadamard state
1. So, the player move, which sets the extra qubit to `|1⟩`, depends on the state of the extra qubit
    1. if it's `|0⟩`, the player move is a CX operation
    1. if it's a mixed state, the player move is a rotation operation

## Optimization

### Optimization in logic:

1. For every state, the current logic is a brute force, which iterates through every possible state
1. This can be optimized as follows:
    1. For a state, we match with every win state, which is basically an AND operation
    1. the bigger the match, larger is the score
    1. we can rank the possible states based on this score, and choose the one with the highest score
    1. this optimizes considerably, because we're not iterating through every possible state, but the one with the highest match
1. However, it might not result in a win, as a match doesn't mean a potential win
    1. this optimization algorithm can be improved upon
    1. but the brute force guarantees the win, with the best probability

### Optimization in player's move:

To optimize the qubit setting algorithm, we can make these assumptions:

1. The extra qubits are all set to `|0⟩` each, which would make player move a `CX` operation
1. The extra qubits are each in a mixed state, which would make the player move an `Rx` operation

Depending on the complexity of both of these operators we can choose the one that results in better optimization.

### Optimization in the end circuit

Finally, at the end of the game, we get a quantum circuit.
Now, we can also perform circuit optimization on this, without affecting the end result too much

## Implementation

### Current implementation

1. I've primarily implemented the logic, both the classical version and the quantum version for setting a qubit to `|1⟩`
    1. Every quantum gate operation is added in a sequence, which is passed in every recursive call.
    1. At the end, **when** the player wins, we apply the operators (gates) to the qubits in the initial circuit, and get the final circuit.
    1. We only have to apply the operators to the moves with the best probability, instead of at every stage.
1. The result stores the following data:
    1. **best_wins** = this stores the win states with the best probabilities
    1. **win_moves** = this stores the player's moves for *those* win states
    1. **win_circuits** = this generates the final circuit for those win states and moves required to get there.
1. The log prints out the possible win states, their individual probability, and the quantum circuit to reach that state
1. I've implemented the **brute force algorithm**, which generates the entire decision tree for a given state.
1. This program works for _any_ given state, which includes the example state 1, bonus state, and others.


### Running the program:

```
git clone https://github.com/arahant/qc-qosf-22-1.git
cd qc-qosf-22-1
pip install -r requirements.txt
python main.py 1001xx0xx 2
```

1. Run each command sequentially, in a terminal. Below are some configuration options.   
1. `1001xx0xx` is the state of the game board in the 1st example in the task document.
    1. `1` represents 'X', and `0` represents 'O', and `x` represents uninitialized states.
    1. The 2nd example in the document will be `1001xxxxx`
    1. Replace `1001xx0xx` with any state
1. `2` is the maximum number of steps allowed; replace it with any positive value
1. Change `LOGGING = True` in `models.py`, to see the log of the entire decision tree.
    1. The log outputs for example 1, example 2 and example 3 are in `output1.txt`, `output2.txt`, and `output3.txt`, respectively.

### Next steps

1. One of the next steps would be to optimize the brute force method which gets *all possible* next states, and replace it with an algorithm that only gets **most probabilistic** next steps.
    1. This would prune the decision tree, and reduce the runtime complexity of the algorithm considerably
1. Test the current program with the quantum operator, `Rx` gate, for when the state of the extra, borrowed qubit is in a mixed state
1. Attempt quantum circuit optimization (if the circuit is too long and complex).

## Result

### Example 1: `1001xx0xx`

```
python main.py 1001xx0xx 2

Given Inputs:
 Initial qubit state: |1001..0..⟩
 Player's initial positions: {1, 4}
 Bot's initial positions: {2, 3, 7}
 Empty cells at:  {8, 9, 5, 6}

Final Qubits 	Resultant Qubit    Probability   Steps   Player's moves
|100111000⟩ 	 |....11.00⟩ 	   0.125 	 2 	 [(1, 4, 6, 5), (1, 4, 5, 6)]
|100110001⟩ 	 |....10.01⟩ 	   0.125     	 2 	 [(1, 4, 9, 5), (1, 4, 5, 9)]

Resultant Quantum Circuits for:  |100110001⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤┌─┴─┐     
q0_4: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘  │  
q0_5: ┤ Initialize(1,0) ├───────┼──
      ├─────────────────┤       │  
q0_6: ┤ Initialize(1,0) ├───────┼──
      ├─────────────────┤       │  
q0_7: ┤ Initialize(1,0) ├───────┼──
      ├─────────────────┤     ┌─┴─┐
q0_8: ┤ Initialize(1,0) ├─────┤ X ├
      └─────────────────┘     └───┘
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100111000⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │  ┌───┐
q0_4: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤┌─┴─┐└─┬─┘
q0_5: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘     
q0_6: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_7: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════

```

### Example 2 (bonus question): `1001xxxxx`

```
python main.py 1001xxxxx 2

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

Resultant Quantum Circuits for:  |100101100⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤┌─┴─┐     
q0_5: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘┌─┴─┐
q0_6: ┤ Initialize(1,0) ├─────┤ X ├
      ├─────────────────┤     └───┘
q0_7: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100100100⟩
      ┌─────────────────┐     
q0_0: ┤ Initialize(0,1) ├─────
      ├─────────────────┤     
q0_1: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_2: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_3: ┤ Initialize(0,1) ├──■──
      ├─────────────────┤  │  
q0_4: ┤ Initialize(1,0) ├──┼──
      ├─────────────────┤  │  
q0_5: ┤ Initialize(1,0) ├──┼──
      ├─────────────────┤┌─┴─┐
q0_6: ┤ Initialize(1,0) ├┤ X ├
      ├─────────────────┤└───┘
q0_7: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_8: ┤ Initialize(1,0) ├─────
      └─────────────────┘     
c0: 9/════════════════════════


Resultant Quantum Circuits for:  |100100110⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │       
q0_5: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │  ┌───┐
q0_6: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤┌─┴─┐└─┬─┘
q0_7: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘     
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100100101⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │       
q0_5: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │  ┌───┐
q0_6: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤  │  └─┬─┘
q0_7: ┤ Initialize(1,0) ├──┼────┼──
      ├─────────────────┤┌─┴─┐  │  
q0_8: ┤ Initialize(1,0) ├┤ X ├──■──
      └─────────────────┘└───┘     
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100110001⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │  ┌───┐
q0_4: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤  │  └─┬─┘
q0_5: ┤ Initialize(1,0) ├──┼────┼──
      ├─────────────────┤  │    │  
q0_6: ┤ Initialize(1,0) ├──┼────┼──
      ├─────────────────┤  │    │  
q0_7: ┤ Initialize(1,0) ├──┼────┼──
      ├─────────────────┤┌─┴─┐  │  
q0_8: ┤ Initialize(1,0) ├┤ X ├──■──
      └─────────────────┘└───┘     
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100110100⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤┌─┴─┐     
q0_4: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘  │  
q0_5: ┤ Initialize(1,0) ├───────┼──
      ├─────────────────┤     ┌─┴─┐
q0_6: ┤ Initialize(1,0) ├─────┤ X ├
      ├─────────────────┤     └───┘
q0_7: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100111000⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │  ┌───┐
q0_4: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤┌─┴─┐└─┬─┘
q0_5: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘     
q0_6: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_7: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════
```

### Example state 3: `10010xxxx`

```
python main.py 10010xxxx 2

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

Resultant Quantum Circuits for:  |100100110⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │       
q0_5: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │  ┌───┐
q0_6: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤┌─┴─┐└─┬─┘
q0_7: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘     
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100100101⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │       
q0_5: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤  │  ┌───┐
q0_6: ┤ Initialize(1,0) ├──┼──┤ X ├
      ├─────────────────┤  │  └─┬─┘
q0_7: ┤ Initialize(1,0) ├──┼────┼──
      ├─────────────────┤┌─┴─┐  │  
q0_8: ┤ Initialize(1,0) ├┤ X ├──■──
      └─────────────────┘└───┘     
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100101100⟩
      ┌─────────────────┐          
q0_0: ┤ Initialize(0,1) ├──────────
      ├─────────────────┤          
q0_1: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_2: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_3: ┤ Initialize(0,1) ├──■───────
      ├─────────────────┤  │       
q0_4: ┤ Initialize(1,0) ├──┼───────
      ├─────────────────┤┌─┴─┐     
q0_5: ┤ Initialize(1,0) ├┤ X ├──■──
      ├─────────────────┤└───┘┌─┴─┐
q0_6: ┤ Initialize(1,0) ├─────┤ X ├
      ├─────────────────┤     └───┘
q0_7: ┤ Initialize(1,0) ├──────────
      ├─────────────────┤          
q0_8: ┤ Initialize(1,0) ├──────────
      └─────────────────┘          
c0: 9/═════════════════════════════


Resultant Quantum Circuits for:  |100100100⟩
      ┌─────────────────┐     
q0_0: ┤ Initialize(0,1) ├─────
      ├─────────────────┤     
q0_1: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_2: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_3: ┤ Initialize(0,1) ├──■──
      ├─────────────────┤  │  
q0_4: ┤ Initialize(1,0) ├──┼──
      ├─────────────────┤  │  
q0_5: ┤ Initialize(1,0) ├──┼──
      ├─────────────────┤┌─┴─┐
q0_6: ┤ Initialize(1,0) ├┤ X ├
      ├─────────────────┤└───┘
q0_7: ┤ Initialize(1,0) ├─────
      ├─────────────────┤     
q0_8: ┤ Initialize(1,0) ├─────
      └─────────────────┘     
c0: 9/════════════════════════
```
