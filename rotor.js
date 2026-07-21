export class MagneticRotor {

constructor({
outerMagnets,
innerMagnets,
magnetLength,
magnetWidth,
magnetHeight,
fieldStrength,
radius,
rpm
}){

this.outerMagnets = outerMagnets;
this.innerMagnets = innerMagnets;

this.magnetLength = magnetLength;
this.magnetWidth = magnetWidth;
this.magnetHeight = magnetHeight;

this.fieldStrength = fieldStrength;
this.radius = radius;
this.rpm = rpm;

}

}
