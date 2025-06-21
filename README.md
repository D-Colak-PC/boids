# Boids
This is a python pygame implementation of the boids algorithm which simulates flocking behavior and emergent group dynamics. With three simple rules and only the ability to see local neighbors, the boids create realistic, flock-like movement. Most of the code is based off of this paper by Craig Reynolds: [Flocks, Herds, and Schools: A Distributed Behavioral Model](https://www.red3d.com/cwr/papers/1987/boids.html).

## Overview

There are three main rules that govern the behavior of each boid in the simulation. Every boid interacts with only local neighbors within a certain radius.
## 1. Separation
**Principle**: Avoid crowding local flockmates.

For each boid $i$ and its neighbors $S$, the separation force is calculated as follows:
$$
\mathbf{F}_{\text{sep}} = \omega_{\text{sep}} \sum_{j \in S} \frac{\widehat{\mathbf{p}_i-\mathbf{p}_j}}{\lVert\mathbf{p}_i-\mathbf{p}_j\rVert^{2}}
$$
Where:
* $j$ = member of the set of neighbors $S$
* $\mathbf p_i$ = the position of boid $i$
* $\mathbf p_j$ = the position of boid $j$

**Derivation**:
1. We want to move away from $j$. The vector pointing away from $j$ is $\mathbf{p}_i-\mathbf{p}_j$. We only want the direction so we can normalize it to get $\widehat{\mathbf{p}_i-\mathbf{p}_j}$.

2. We want to move away from $j$ with a strength that drops off with distance. A common way to do this is to use the inverse square law. \
We know that due to the inverse square law,
$$
\text{strength} \propto \frac{1}{\text{distance}^2}
$$
or, better for our purposes,
$$
\text{strength} = \omega_{\text{sep}} \frac{1}{\text{distance}^2}
$$
where $\omega_{\text{sep}}$ is a constant that controls the strength of the force.

We can substitute the distance with the norm of the vector $\mathbf{p}_i-\mathbf{p}_j$ to get:
$$
\text{strength} = \omega_{\text{sep}} \frac{1}{\lVert\mathbf{p}_i-\mathbf{p}_j\rVert^{2}}
$$
3. We can combine direction and magnitude (strength) to get the force vector from $j$ to $i$:
$$
\begin{align*}
\mathbf F_{i\leftarrow j} &= \underbrace{\widehat{\mathbf p_i-\mathbf p_j}}_{\text{direction}} \; \underbrace{\left(\omega_{\text{sep}}\,\frac{1}{\lVert\mathbf p_i-\mathbf p_j\rVert^{2}}\right)}_{\text{magnitude}} \\
&= \omega_{\text{sep}} \frac{\widehat{\mathbf p_i-\mathbf p_j}} {\lVert\mathbf p_i-\mathbf p_j\rVert^{2}}
\end{align*}
$$
4. To aggregate the forces from all neighbors, we sum over all $j$ in the set of neighbors $S$. \
   The total separation force on boid $i$ is
$$
\begin{align*}
\mathbf F_{\text{sep}} &= \sum_{j\in S} \mathbf F_{i\leftarrow j} \\
&= \sum_{j\in S} \omega_{\text{sep}} \frac{\widehat{\mathbf p_i-\mathbf p_j}} {\lVert\mathbf p_i-\mathbf p_j\rVert^{2}}\
\end{align*}
$$
Factoring out the constant $\omega_{\text{sep}}$ gives us the final formula:
$$
\boxed {\mathbf F_{\text{sep}} = \omega_{\text{sep}} \sum_{j \in S} \frac{\widehat{\mathbf{p}_i-\mathbf{p}_j}}{\lVert\mathbf{p}_i-\mathbf{p}_j\rVert^{2}}}
$$

### 2. Alignment
**Principle**: Steer toward the average heading of local flock-mates.

For each boid $i$ and its neighbors $S$, the alignment force is calculated as follows:

$$
\mathbf F_{\text{align}} = \omega_{\text{align}}\Bigl(v_{\max}\,\widehat{\bar{\mathbf v}} - \mathbf v_i\Bigr)\,,\;
\bar{\mathbf v} = \frac1{|S|}\sum_{j\in S}\mathbf v_j
$$

Where

* $\mathbf v_j$ = velocity of neighbour $j$
* $v_{\max}$ = maximum speed (scalar)
* $\omega_{\text{align}}$ = alignment weight (tunable gain)
* $\widehat{\bar{\mathbf v}}$ = unit vector in the direction of the mean velocity.

**Derivation**

1. We want to align ourselves with our neighbors. The first step is to compute the average velocity of all visible neighbours $S$:

$$
\bar{\mathbf v}=\frac1{|S|}\sum_{j\in S}\mathbf v_j .
$$

And then get only the direction from it.

$$
\widehat{\bar{\mathbf v}}=\frac{\bar{\mathbf v}}{\lVert\bar{\mathbf v}\rVert}.
$$

2. The desired velocity is the maximum speed in the direction of the average velocity of the neighbours:

$$
\mathbf v_{\text{des}} = v_{\max}\,\widehat{\bar{\mathbf v}}
$$

So we want to steer towards this desired velocity.
3. The difference between the desired velocity and the current velocity gives us the steering force $\mathbf{v}_{\text{des}} - \mathbf v_i$.
We multiply by a tuneable gain the form of $\omega_{\text{align}}$ to control the strength of the alignment force to get:

$$
\mathbf F_{\text{align}}= \omega_{\text{align}}\bigl(\mathbf v_{\text{des}} - \mathbf v_i\bigr).
$$

Substituting, we get
$$
\boxed {\mathbf F_{\text{align}} = \omega_{\text{align}}\Bigl(v_{\max}\,\widehat{\bar{\mathbf v}} - \mathbf v_i\Bigr)}\,,\;
\bar{\mathbf v} = \frac1{|S|}\sum_{j\in S}\mathbf v_j
$$

This $\mathbf F_{\text{align}}$ nudges boid $i$ so its heading aligns with its visible neighbours, generating the coherent, sheet-like motion typical of real flocks.


### 3. Cohesion
**Principle**: Steer towards the average position of local flockmates.

For each boid $i$ and its neighbors $S$, the cohesion force is calculated as follows:

$$
\mathbf{F}_{\text{coh}} = \omega_{\text{coh}}\Bigl(v_{\max}\,\widehat{\bar{\mathbf p}-\mathbf{p}_i} - \mathbf{v}_i\Bigr)\,,\;
\bar{\mathbf p} = \frac{1}{|S|}\sum_{j\in S}\mathbf{p}_j
$$

Where:
* $\mathbf{p}_j$ = position of neighbor $j$
* $\bar{\mathbf p}$ = center of mass of neighbors
* $v_{\max}$ = maximum speed (scalar)
* $\omega_{\text{coh}}$ = cohesion weight (tunable gain)

**Derivation**

1. We want to move toward the center of mass of our neighbors. The formula for the center of mass for discrete points is

$$
\bar{\mathbf p} = \frac{\sum_{j\in S} m_j \mathbf{p}_j}{\sum_{j\in S} m_j}
$$

Where $m_j$ is the mass of neighbor $j$. In our case, we assume all boids have equal mass, so we can simplify this to:
$$
\bar{\mathbf p} = \frac{1}{|S|}\sum_{j\in S}\mathbf{p}_j
$$

Where $|S|$ is the number of neighbors in set $S$. This also happens to be the average position of the neighbors.

2. Next, we find the direction from our current position to the center of mass:

$$
\bar{\mathbf p} - \mathbf{p}_i
$$

And normalize it to get the unit direction vector:

$$
\widehat {\bar{\mathbf p} - \mathbf{p}_i}
$$

3. The desired velocity is the maximum speed in the direction toward the center of mass:

$$
\mathbf{v}_{\text{des}} = v_{\max}\,\widehat{\bar{\mathbf p}-\mathbf{p}_i}
$$

So we want to steer towards this desired velocity.

4. The difference between the desired velocity and the current velocity gives us the steering force $\mathbf{v}_{\text{des}} - \mathbf{v}_i$. We multiply by a tunable gain $\omega_{\text{coh}}$ to control the strength of the cohesion force:

$$
\mathbf{F}_{\text{coh}} = \omega_{\text{coh}}\bigl(\mathbf{v}_{\text{des}} - \mathbf{v}_i\bigr)
$$

Substituting, we get:

$$
\boxed{\mathbf{F}_{\text{coh}} = \omega_{\text{coh}}\Bigl(v_{\max}\,\widehat{\bar{\mathbf p}-\mathbf{p}_i} - \mathbf{v}_i\Bigr)}\,,\;
\bar{\mathbf p} = \frac{1}{|S|}\sum_{j\in S}\mathbf{p}_j
$$