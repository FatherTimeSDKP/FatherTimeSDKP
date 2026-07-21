export const SDN_SOLIDS = {

 tetrahedron:{
  F:4,
  V:4,
  E:6
 },

 cube:{
  F:6,
  V:8,
  E:12
 },

 octahedron:{
  F:8,
  V:6,
  E:12
 },

 dodecahedron:{
  F:12,
  V:20,
  E:30
 },

 icosahedron:{
  F:20,
  V:12,
  E:30
 }

};


export function euler(F,V,E){

 return F-E+V;

}


export function phi(F,V,E){

 return (F*V)/E;

}
