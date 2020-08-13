# AI Flappy Bird with NeuroEvolution of Augmenting Topologies <strong>(NEAT)</strong>
NeuroEvolution of Augmenting Topologies is a method for evolving artificial neural networks with a **Genetic Algorithm**. NEAT implements the idea that it is most effective to start evolution with small, simple neural networks and allow them to become increasingly complex over generations.
<br>
NEAT and Genetic Algorithm has the ability to add or remove a neural node hence making the network complex over time and improving the result, by analyzing the fitness of the population of each generation.

# Running the Algorithm
Clone the Repository by running
<br>
<code>git clone "https://github.com/thatfreakcoder/FlappyBird-NEAT-AI"</code>
<br>
or downloading it via the <code>DOWNLOAD</code> button
<br>
Install the dependencies by running
<br>
<code>pip install -r requirements.txt</code>
<br>
and then finally run the game by running
<br>
<code>python main.py</code>


# My NEAT Configuration
Configuration File for Genetic Algorith can be found <a href="NEAT-CONFIG.txt">here</a>
<br>
<ul>
  <li>I am using a population size of 10 because of the simplicity of the task, more population might mean the desired network will be randomly formed in the first generation, without any training or `learning` from the parent genomes</li>
  <li> Default Activation Function used is <strong>ReLU</strong>, with a switch option of <b>TanH</b> and <b>Sigmoid</b> functions, with a mutability rate of 0.7</li>
  <li> Network Type is a Fully Connected <b>Feed Forward Neural Network</b>. Genomes Information is passed on the the mutated offsprings for better understanding of the network and imporving fitness score.</li>
  <li> Neural Network is of shape <b>[3, 1]</b> with 3 input layers and 1 output layer with no Hidden Layers.</li>
  <li> <b>Connection Add / Remove Probability</b> is set to 0.6 / 0.4 </li>
</ul>

# OUTCOME
I was able to get a very well trained outcome in the **2nd Generation** and was able to achieve a score of 196 (screenshot was taken before the game ended).
<img src="score1.jpg" style="heigh: 30%; width : 30%" />

# if you liked the project, please star ⭐ the repo :)
