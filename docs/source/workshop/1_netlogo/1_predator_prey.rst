Predator-Prey Modelling
=======================

Predator-prey systems describe interactions between species where one species hunts another. A classic example is the relationship between **wolves and sheep**: sheep provide food for wolves, while wolves reduce the sheep population through predation. Changes in one population can therefore affect the other, often producing repeating cycles.

Why Model Predator-Prey Systems?
--------------------------------

Mathematical and computational models allow us to explore how simple interactions can produce complex population dynamics. For example, a model can help us ask:

* What happens when there are many more sheep than wolves?
* How does increasing the reproduction rate of wolves affect the system?
* Under what conditions can wolves and sheep coexist?
* What conditions could cause one population to disappear?

One of the simplest mathematical descriptions of predator-prey dynamics is the **Lotka-Volterra model**. Rather than representing individual animals, it describes how the *size of the wolf and sheep populations* changes over time.

Agent-Based Predator-Prey Models
--------------------------------

An alternative is to represent the system using an **agent-based model (ABM)**. Instead of modelling the populations directly, an ABM represents individual animals as agents.

Each agent can have its own:

* location
* energy
* behaviour
* interactions with other agents

The overall population dynamics then **emerge from the interactions between individual agents**.

For example, in a wolf-sheep model:

* sheep move around the environment and reproduce;
* wolves move around the environment and hunt sheep;
* wolves gain energy when they eat sheep;
* wolves reproduce when they have sufficient energy;
* animals may die when they run out of energy.

No rule needs to explicitly say that "the wolf population should oscillate". Population-level patterns can emerge from these individual-level rules.

The Wolf-Sheep Model in NetLogo
-------------------------------

In this workshop, we will use the **Wolf Sheep Predation** model in `NetLogo` as a simple example of an ABM.

The model provides a useful way to explore how changing model parameters affects the behaviour of the system. For example, we can change parameters controlling reproduction, movement, predation, and energy gain and observe how the wolf and sheep populations respond.

This gives us a simple experimental setup:

.. code-block:: bash

    Model parameters
    |
    v
    Wolf-Sheep
    ABM
    |
    v
    Individual interactions
    |
    v
    Population dynamics

The important point is that we can observe the **outputs** of the model, but we may not know which parameter values provide the best representation of a real-world system.

This leads to the central question of this workshop:

**How can we choose the parameters of an agent-based model so that its behaviour is consistent with observations?**

That is the problem of **calibration**.
