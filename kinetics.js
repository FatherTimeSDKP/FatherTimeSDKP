export function tau(size, velocity){

 if(velocity===0)
 return Infinity;

 return size/velocity;

}


export function eosAdjustedTau(value){

 return {

 low:value*1.0013,

 high:value*1.0020

 };

}
