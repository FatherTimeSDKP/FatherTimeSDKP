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
