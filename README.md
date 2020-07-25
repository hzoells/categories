# Categories
This is an API to manage the data for multiplayer online scattergories games.
Request bodies are expected in JSON
A typical game would follow the following basic format:
#### 1. Create a game
post to /games with a game_name specified in the request body.
#### 2. Player creations
Players are created by posting to /players with a name specified in the body. The first player created for a game is the host and has the ability to submit scores. Players receive IDs when they are created.
#### 3. Get Questions
In order to play, each player sends a get request to games/<game_name>/questions. This retrieves a list of questions for the current round with IDs.
#### 4. Submit response
Each player sends in a list of answers with corresponding question ID's by posting to answers/<player ID>
#### 5. Group scoring
All players request a full list of player responses. They recieve a list of questions and a list of answers for each player in order to determine scores. This happens at games/<game_name>/answers
#### 6. Scoring
The host post scores to /games/<game_name>/scores
#### 7. View scores
Players can view cumulative scores by sending a get request to /games/<game_name>/scores
