I started off the project by making a comparison between the number recognition model in the source code and our current problem. They seemed pretty similar, so initially I started testing on the same model that worked for number recognition. Initially I got a very low accuracy. Continuing with experimentation I did the following things which did not work -

1. Added another hidden layer with relU activation.
2. Changed the hidden layer's activation to softmax.
3. Adding more convolution filters.

The following things worked well for tuning the model -

1. Increasing the number of nodes in hidden layer.
2. Increasing the pool size.

I noticed that while some changes had no positive effect at all, like adding another layer, on the other hand some changes had a positive effect upto a certain extent. As an example, increasing the pooling size worked well till (4, 4) but on going to higher values it didn't increase the accuracy by a lot. The positive effect in accuracy by increasing the number of nodes maxed out at 1024 nodes, going higher did not make the accuracy any better.
