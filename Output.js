export function densityGradient(
densityA,
densityB,
distance,
phiA,
phiB
){

const mean =
(densityA+densityB)/2;


return mean /
(
distance *
phiA *
phiB
);

}
Continuing the rebuild.

Step 2 — Build the Core Data Model

Before adding calculations, we define what every object in the simulator is.

The solver needs a common structure:

// object.js
export class PhysicalObject {
constructor({
name,
size,
density,
velocity,
geometry
}){
this.name = name;
this.size = size;          // meters
this.density = density;    // kg/m3
this.velocity = velocity;  // m/s
this.geometry = geometry;
}
}

Now every simulated object has the same format.

Example:

const spacecraft = new PhysicalObject({
name:"LEO Test Body",
size:10,
density:800,
velocity:7600,
geometry:"octahedron"
});

⸻

Step 3 — Create the Solver Core

The solver takes an object and processes it.

// kapnack.js
import {tau} from "./kinetics";
import {phi,SDN_SOLIDS} from "./geometry";
export function solve(object){
const shape =
SDN_SOLIDS[object.geometry];
const shapeFactor =
phi(
shape.F,
shape.V,
shape.E
);
const time =
tau(
object.size,
object.velocity
);
return {
name:object.name,
tau:time,
phi:shapeFactor,
Euler:
shape.F -
shape.E +
shape.V
};
}

⸻

Step 4 — First Test Case

Input:

LEO Test Body
Size:
10 m
Density:
800 kg/m³
Velocity:
7600 m/s
Geometry:
Octahedron

The solver returns:

Geometry

F=8

V=6

E=12

Euler:

8-12+6=2

✓ Valid

Shape factor:

\phi=
\frac{8\times6}{12}

\phi=4

⸻

Kinetic result

\tau=\frac{S}{v}

\tau=\frac{10}{7600}

\tau=0.0013158s

or:

1.3158ms

⸻

Step 5 — Add the Validation Layer

Now the solver should not only calculate; it should check.

// validation.js
export function validate(result){
return {
euler:
result.Euler===2,
finite:
Number.isFinite(result.tau),
positive:
result.tau>0
};
}

Output:

KAPNACK VALIDATION
Euler geometry:
PASS
Time solution:
PASS
Numerical stability:
PASS

⸻

At this point we have the first working core:

Input
 ↓
Physical Object
 ↓
Kapnack Solver
 ↓
Geometry + Kinetics
 ↓
Validation
 ↓
Output

Step 6 — Add the Density Field Engine

Now we move from one object to interacting systems.

The idea is to create a field between two bodies:

Body A                 Density Field              Body B
(size, density)  →  gradient calculation  →  (size, density)

⸻

1. Create the Density Field module

density.js

import { phi, SDN_SOLIDS } from "./geometry";
export function densityGradient(bodyA, bodyB){
const shapeA =
SDN_SOLIDS[bodyA.geometry];
const shapeB =
SDN_SOLIDS[bodyB.geometry];
const phiA =
phi(
shapeA.F,
shapeA.V,
shapeA.E
);
const phiB =
phi(
shapeB.F,
shapeB.V,
shapeB.E
);
const distance =
Math.abs(bodyA.size - bodyB.size);
const meanDensity =
(bodyA.density + bodyB.density) / 2;
const gradient =
meanDensity /
(
distance *
phiA *
phiB
);
return {
phiA,
phiB,
distance,
meanDensity,
gradient
};
}

⸻

2. Example: Two-body system

Body A

Name:
Orbital Vehicle
Size:
15.2 m
Density:
4.8 kg/m³
Geometry:
Octahedron

Body B

Name:
Large Field Body
Size:
50,000 m
Density:
0.0021 kg/m³
Geometry:
Dodecahedron

⸻

3. Solver output

Geometry:

Octahedron:

\phi_A=4

Dodecahedron:

\phi_B=8

Distance:

\Delta S=
50000-15.2

\Delta S=49984.8m

Mean density:

D_m=
\frac{4.8+0.0021}{2}

D_m=2.40105

Gradient:

\Gamma=
\frac{D_m}
{\Delta S\phi_A\phi_B}

\Gamma
=
\frac{2.40105}
{49984.8(4)(8)}

\Gamma
\approx1.50\times10^{-6}

⸻

4. Add field evolution

Now we add how the field changes:

export function evolveDensity(
current,
baseline,
rate=0.7
){
return baseline +
(current-baseline)*rate;
}

This gives a convergence model:

Step 0:

\rho=1.080

Step 1:

\rho=1.0578

Step 2:

\rho=1.0423

Eventually:

\rho\rightarrow\rho_{baseline}

⸻

5. New solver pipeline

We now have:

Physical Object
        |
        v
Geometry Engine
        |
        v
Kinetic Engine
        |
        v
Density Field Engine
        |
        v
Validation Layer
        |
        v
Simulation Output

The next major module is Step 7: Field Interaction Engine — where we connect the density field to the magnetic-cylinder concept:

* rotating cylinders
* inner/outer magnet arrays
* torque
* angular velocity
* energy flow
* losses

