# Hive Project
## Minimax Algorithm with Alpha-Beta Pruning with iterative deepening:
The AI system implements a sophisticated decision-making process through an enhanced minimax algorithm with alpha-beta pruning. The system includes:
### Move Generation Optimization
  •	Efficient legal move enumeration
  •	Move ordering for better pruning
  •	Position caching system
### Evaluation System
  •	Static position evaluation
  •	Piece-square table implementation
  •	Mobility assessment
  •	Threat detection algorithms
  ## AI Heuristics for Hive Game

This section describes the heuristic evaluation system utilized in the AI to analyze board positions and make strategic decisions during the Hive game. The heuristics are designed to evaluate the board dynamically and provide guidance to optimize gameplay.

## Heuristic Evaluation Components

### 1. Base Position Evaluation
The system begins with fundamental piece valuations:

- **Queen:** Highest strategic value (1000 points).
- **Beetle:** Strong tactical value (80 points).
- **Ant:** High mobility value (60 points).
- **Spider:** Moderate positional value (40 points).
- **Grasshopper:** Support piece value (30 points).

### 2. Queen Safety Analysis
Queen safety is a critical aspect of evaluation, ensuring the queen is well-protected while maintaining tactical flexibility.

#### Surrounding Piece Configuration
- **Exposure:** Severely penalizes exposure (≤1 surrounding piece: -200 points).
- **Optimal Protection:** Rewards two surrounding pieces (+50 points).
- **Friendly Protection:** Encourages three friendly pieces (+40 points per friendly piece).
- **Overcrowding:** Heavily penalizes overcrowding (≥4 surrounding pieces: -150 points per extra piece).

#### Attack Potential Evaluation
- **Beetle Positioning:** Awards up to 200 points based on proximity to the enemy queen.
- **Ant Presence:** Flat bonus of 50 points for creating mobility threats.
- **Spider Positioning:** Awards up to 100 points based on its distance to the enemy queen.

### 3. Strategic Position Evaluation
Evaluates the broader tactical and strategic elements of the game.

#### Blocking Tactics
- Awards 50 points for pieces positioned between enemy pieces and their queen.
- Values Beetles and Spiders highly in blocking positions.
- Considers relative distances and positioning.

#### Space Control
- Awards 30 points for pieces controlling multiple adjacent spaces.
- Emphasizes board control and territory dominance.
- Values pieces that restrict enemy movement.

### 4. Early Game Considerations
Special evaluation adjustments are applied during the early game:
- **Queen Placement:** Severe penalty (-500 points) for not placing the queen by turn 4.
- **Development Bonus:** Awards 20 points per piece for early deployment.
- Encourages proper game development and timing.

### 5. Terminal Position Detection
Recognizes and evaluates decisive positions:
- Returns maximum positive score (+Infinity) for surrounding the enemy queen.
- Returns maximum negative score (-Infinity) for the friendly queen being surrounded.
- Ensures immediate recognition of winning and losing scenarios.

## Piece-Specific Strategy Implementation

### Queen Management
- Early-game positioning strategy.
- Mid-game protection protocols.
- Late-game survival tactics.

### Beetle Tactical System
- Evaluates climbing opportunities.
- Focuses on queen coverage positioning.
- Implements piece pinning strategies.

### Ant Strategy
- Maximizes mobility.
- Implements position control tactics.
- Plans surrounding maneuvers.

### Spider Positioning
- Focuses on three-step movement planning.
- Optimizes blocking positions.
- Executes tactical pins.

### Grasshopper Utilization
- Identifies jump opportunities.
- Exploits gaps in the opponent’s positioning.
- Plans surprise attacks.
## UML Diagrams
### Class Diagram
![mmm](https://github.com/user-attachments/assets/6da61d8a-44a9-4ba7-8524-dd471df33092)
### Sequence Diagram
![mmmm](https://github.com/user-attachments/assets/15a68ff4-75fc-49de-8ed2-22a0b9ba0675)
### State Diagram
![stateDiagram](https://github.com/user-attachments/assets/081b8e8e-f97d-4287-bc4c-ee2e94517523)
## Supported features:
### Game Modes:
•	Local multiplayer functionality
•	Single player vs AI capability
•	AI vs AI simulation mode
•	Interactive tutorial system
### UI Features:
  •	Interactive board system
  •	Dynamic move highlighting
  •	Clear turn indication
  •	Real-time move validation
  •	Comprehensive game state display
## Difficulty Levels:
### Easy (Level 1)
  •	Search depth: 2 ply
  •	Basic evaluation implementation
  •	Simplified piece values
  •	Limited heuristic application
### Medium (Level 2)
  •	Search depth: 4 ply
  •	Enhanced evaluation system
  •	Position scoring implementation
  •	Basic queen protection strategies
### Hard (Level 3)
  •	Search depth: 6 ply
  •	Full heuristic utilization
  •	Tactical combination analysis
  •	Advanced strategic planning
### Impossible (Level 4)
  •	Search depth: 8 ply
  •	Maximum evaluation complexity
  •	Advanced strategy implementation
  •	Sophisticated endgame techniques




