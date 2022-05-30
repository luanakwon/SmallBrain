# smallbrain
Made some garbage changes here  
some more changes here  
and here  
Trying shallow RNN on reinforcement learning

The goel of this project is to make the model learn without backpropagation nor reinforcement.

The idea behind this is that brain doesn't work like  
INPUT > MIDDLE > OUTPUT.  
Rather, it works like  
INPUT + PAST_MEMORY > MIDDLE > OUTPUT.

To mimic this, I designed the network like this:
![image](https://user-images.githubusercontent.com/93167577/148670634-8fb666fb-4e38-4815-8ebd-a7b799a4b7f6.png)

I'm hoping for this model to pass the Skinner's box test, but it has to learn the concept of prize. 
To teach "food is good", I've created an reinforcement learning environment with foods and fishes. 
