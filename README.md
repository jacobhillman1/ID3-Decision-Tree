# ID3 Decision Tree

This implementation of a decision uses the ID3 algorithm to determine the
subsequent nodes of the tree.

In summary, the program calculates the information gain of each remaining attribute in the dataset.
The attribute with the highest information gain is chosen.

Information gain is calculated using the formula for entropy, which determines the
predictability of the target value. (The target value, in this case, is whether or not to go outside)

Low Entropy -> High predictability -> High information gain, and vice versa.

Right now this implementation has only been tested to work with the included dataset, weather.json.
