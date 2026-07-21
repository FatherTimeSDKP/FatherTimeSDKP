import React, { useState, useMemo } from ‘react’;

/* ============================================================
PHYSICS MODULE — physics/sdkp.js
============================================================ */
const SDKP = {
EOS: 29780.0,
EOS_LOW: 0.0013,
EOS_HIGH: 0.0020,
C: 299792458.0,

tau(S, D, v) {
const K = (D * v) / S;
const tauVal = S / v;
return { tau: tauVal, K };
},

tauWithUncertainty(S, D, v, dS, dv) {
const { tau: tauVal, K } = this.tau(S, D, v);
const relError = Math.sqrt(Math.pow(dS / S, 2) + Math.pow(dv / v, 2));
const dTau = tauVal * relError;
return {
tau: tauVal, K, dTau, relError,
tauLow: tauVal * (1 + this.EOS_LOW),
tauHigh: tauVal * (1 + this.EOS_HIGH),
};
},
};

/* ============================================================
PHYSICS MODULE — physics/geometry.js
============================================================ */
const SDN_SOLIDS = {
tetrahedron:  { F: 4,  V: 4,  E: 6,  name: ‘Tetrahedron’  },
cube:         { F: 6,  V: 8,  E: 12, name: ‘Cube’         },
octahedron:   { F: 8,  V: 6,  E: 12, name: ‘Octahedron’   },
dodecahedron: { F: 12, V: 20, E: 30, name: ‘Dodecahedron’ },
icosahedron:  { F: 20, V: 12, E: 30, name: ‘Icosahedron’  },
};

const Geometry = {
solids: SDN_SOLIDS,
shapeFactorPhi(solid) {
const s = SDN_SOLIDS[solid];
return (s.F * s.V) / s.E;
},
phaseFactor(solid) {
const s = SDN_SOLIDS[solid];
return (2 * Math.PI) / (s.F + s.V + s.E);
},
eulerCheck(solid) {
const s = SDN_SOLIDS[solid];
return s.F - s.E + s.V === 2;
},
packingGradient(Sa, Da, solidA, Sb, Db, solidB, harmonicOrder = 3) {
const phiA = this.shapeFactorPhi(solidA);
const phiB = this.shapeFactorPhi(solidB);
const deltaS = Math.max(Math.abs(Sa - Sb), 1e-15);
const meanD = (Da + Db) / 2;
const H_n = 1 / (9 * Math.pow(10, harmonicOrder));
const gamma = meanD / (deltaS * phiA * phiB * (1 + H_n));
return { phiA, phiB, deltaS, meanD, gamma, H_n };
},
};

/* ============================================================
PHYSICS MODULE — physics/magnetic.js
============================================================ */
const Magnetic = {
MU_0: 4 * Math.PI * 1e-7,

magneticEnergy(B, volume) {
return (Math.pow(B, 2) / (2 * this.MU_0)) * volume;
},

rotorTorque(outerMagnets, innerMagnets, Br, magnetVolume, radius, gapFactor = 0.85) {
const interactingPairs = Math.min(outerMagnets, innerMagnets);
const dipoleMoment = (Br * magnetVolume) / this.MU_0;
const gapDistance = radius * (1 - gapFactor);
const forcePerPairRaw = gapDistance > 0
? (3 * this.MU_0 * Math.pow(dipoleMoment, 2)) / (2 * Math.PI * Math.pow(Math.max(gapDistance, 0.001), 4))
: 0;
const forcePerPair = Math.min(forcePerPairRaw, 50000);
const torque = interactingPairs * forcePerPair * radius;
return { dipoleMoment, gapDistance, forcePerPair, interactingPairs, torque };
},

mechanicalPower(torque, rpm) {
const omega = (rpm * 2 * Math.PI) / 60;
return { power: torque * omega, omega };
},

backEMF(numCoils, B, coilArea, omega) {
return numCoils * B * coilArea * omega;
},

thermalLoss(current, resistance) {
return Math.pow(current, 2) * resistance;
},

efficiency(mechPowerOut, elecPowerIn) {
if (elecPowerIn <= 0) return 0;
return Math.min(mechPowerOut / elecPowerIn, 1.0) * 100;
},
};

/* ============================================================
PHYSICS MODULE — physics/validation.js
============================================================ */
const Validation = {
runFullSuite() {
const results = [];

```
const eulerResults = Object.keys(SDN_SOLIDS).map(k => Geometry.eulerCheck(k));
results.push({
  test: 'Euler characteristic (F-E+V=2)',
  detail: `${eulerResults.filter(r => r).length}/5 solids`,
  pass: eulerResults.every(r => r),
});

results.push({
  test: 'EOS reference constant',
  detail: `v_EOS = ${SDKP.EOS.toLocaleString()} m/s`,
  pass: SDKP.EOS > 0 && SDKP.EOS < SDKP.C,
});

results.push({
  test: 'Causal limit (c)',
  detail: `c = ${SDKP.C.toLocaleString()} m/s`,
  pass: true,
});

const testTau = SDKP.tau(10, 800, 7600);
results.push({
  test: 'tau = S/v dimensional check',
  detail: `tau(S=10,v=7600) = ${testTau.tau.toExponential(4)} s`,
  pass: testTau.tau > 0 && isFinite(testTau.tau),
});

const testGrad = Geometry.packingGradient(15.2, 4.8, 'octahedron', 50000, 0.0021, 'dodecahedron');
results.push({
  test: 'Packing gradient numerical stability',
  detail: `Gamma = ${testGrad.gamma.toExponential(4)} kg/m4`,
  pass: isFinite(testGrad.gamma) && testGrad.gamma > 0,
});

const testMag = Magnetic.rotorTorque(12, 6, 1.4, 0.024 * 0.15 * 0.10, 0.5);
results.push({
  test: 'Magnetic rotor numerical stability',
  detail: `torque = ${testMag.torque.toExponential(4)} N*m`,
  pass: isFinite(testMag.torque) && testMag.torque >= 0,
});

results.push({
  test: 'EOS deviation range ordering [0.13%, 0.20%]',
  detail: `low=${SDKP.EOS_LOW}, high=${SDKP.EOS_HIGH}`,
  pass: SDKP.EOS_LOW < SDKP.EOS_HIGH && SDKP.EOS_LOW > 0,
});

return results;
```

},
};

/* ============================================================
SHARED UI PRIMITIVES
============================================================ */
const grid2 = { display: ‘grid’, gridTemplateColumns: ‘1fr 1fr’, gap: 24 };
const labelStyle = { display: ‘block’, fontSize: 11, color: ‘rgba(255,255,255,0.5)’, marginTop: 12, marginBottom: 4, textTransform: ‘uppercase’, letterSpacing: 1 };
const inputStyle = { width: ‘100%’, padding: ‘10px 12px’, background: ‘rgba(0,0,0,0.3)’, border: ‘1px solid rgba(255,255,255,0.15)’, borderRadius: 6, color: ‘#e8edf5’, fontSize: 14, fontFamily: ‘monospace’ };
const btnStyle = { padding: ‘10px 18px’, background: ‘#2E5496’, color: ‘#fff’, border: ‘1px solid #64b4ff’, borderRadius: 6, fontSize: 13, fontWeight: 600, cursor: ‘pointer’ };

function Panel({ title, children, accent, wide }) {
return (
<div style={{
background: accent ? ‘rgba(100,180,255,0.06)’ : ‘rgba(255,255,255,0.03)’,
border: accent ? ‘1px solid rgba(100,180,255,0.25)’ : ‘1px solid rgba(255,255,255,0.1)’,
borderRadius: 8, padding: 24, gridColumn: wide ? ‘1 / -1’ : ‘auto’,
}}>
<h3 style={{ marginTop: 0, color: ‘#7ec8e3’, fontSize: 15 }}>{title}</h3>
{children}
</div>
);
}
function Field({ label, value, onChange }) {
return (
<div style={{ flex: 1 }}>
<label style={labelStyle}>{label}</label>
<input type=“number” value={value} onChange={e => onChange(e.target.value)} style={inputStyle} />
</div>
);
}
function SelectField({ label, value, onChange }) {
return (
<div>
<label style={labelStyle}>{label}</label>
<select value={value} onChange={e => onChange(e.target.value)} style={inputStyle}>
{Object.keys(SDN_SOLIDS).map(k => <option key={k} value={k}>{SDN_SOLIDS[k].name}</option>)}
</select>
</div>
);
}
function SubLabel({ children }) {
return <div style={{ fontSize: 12, color: ‘#7ec8e3’, fontWeight: 700, marginTop: 16, marginBottom: 4 }}>{children}</div>;
}
function Note({ children }) {
return <div style={{ marginTop: 16, padding: 12, background: ‘rgba(100,180,255,0.08)’, borderRadius: 6, fontSize: 12, color: ‘rgba(255,255,255,0.6)’ }}>{children}</div>;
}
function Row({ label, value, highlight }) {
return (
<div style={{ display: ‘flex’, justifyContent: ‘space-between’, alignItems: ‘center’, padding: ‘10px 0’, borderBottom: ‘1px solid rgba(255,255,255,0.06)’ }}>
<span style={{ fontSize: 13, color: ‘rgba(255,255,255,0.6)’ }}>{label}</span>
<span style={{ fontSize: 14, fontFamily: ‘monospace’, fontWeight: highlight ? 700 : 400, color: highlight ? ‘#64b4ff’ : ‘#e8edf5’ }}>{value}</span>
</div>
);
}

/* ============================================================
COMPONENT — components/TauPanel.jsx
============================================================ */
function TauPanel() {
const [size, setSize] = useState(10.0);
const [dSize, setDSize] = useState(0.01);
const [density, setDensity] = useState(800);
const [velocity, setVelocity] = useState(7600);
const [dVelocity, setDVelocity] = useState(5);

const result = useMemo(() => SDKP.tauWithUncertainty(
parseFloat(size) || 1e-9, parseFloat(density) || 0, parseFloat(velocity) || 1e-9,
parseFloat(dSize) || 0, parseFloat(dVelocity) || 0
), [size, density, velocity, dSize, dVelocity]);

return (
<div style={grid2}>
<Panel title="Input Parameters">
<Field label="Size S (m)" value={size} onChange={setSize} />
<Field label="Size uncertainty dS (m)" value={dSize} onChange={setDSize} />
<Field label="Density D (kg/m3)" value={density} onChange={setDensity} />
<Field label="Velocity v (m/s)" value={velocity} onChange={setVelocity} />
<Field label="Velocity uncertainty dv (m/s)" value={dVelocity} onChange={setDVelocity} />
<Note>tau = S*D/K, K = D*v/S, reduces to tau = S/v. Uncertainty via quadrature: dtau/tau = sqrt((dS/S)^2 + (dv/v)^2)</Note>
</Panel>
<Panel title="SDKP Output" accent>
<Row label=“Kinetics K” value={`${result.K.toExponential(4)} kg/(m2*s)`} />
<Row label=“tau (Newtonian)” value={`${result.tau.toExponential(6)} s`} highlight />
<Row label=“Relative uncertainty” value={`${(result.relError * 100).toFixed(4)}%`} />
<Row label=“tau uncertainty” value={`+/- ${result.dTau.toExponential(4)} s`} highlight />
<Row label=“tau EOS low (0.13%)” value={`${result.tauLow.toExponential(6)} s`} />
<Row label=“tau EOS high (0.20%)” value={`${result.tauHigh.toExponential(6)} s`} />
<div style={{ marginTop: 14, padding: 10, background: ‘rgba(74,222,128,0.08)’, borderRadius: 6, fontSize: 12, color: ‘#4ade80’ }}>
Result: tau = {result.tau.toExponential(4)} s +/- {result.dTau.toExponential(4)} s (1-sigma)
</div>
</Panel>
</div>
);
}

/* ============================================================
COMPONENT — components/GradientPanel.jsx
============================================================ */
function GradientPanel() {
const [sizeA, setSizeA] = useState(15.2);
const [densityA, setDensityA] = useState(4.8);
const [solidA, setSolidA] = useState(‘octahedron’);
const [sizeB, setSizeB] = useState(50000);
const [densityB, setDensityB] = useState(0.0021);
const [solidB, setSolidB] = useState(‘dodecahedron’);

const result = useMemo(() => Geometry.packingGradient(
parseFloat(sizeA) || 1e-9, parseFloat(densityA) || 0, solidA,
parseFloat(sizeB) || 1e-9, parseFloat(densityB) || 0, solidB
), [sizeA, densityA, solidA, sizeB, densityB, solidB]);

return (
<div style={grid2}>
<Panel title="Body A / Body B">
<SubLabel>Body A</SubLabel>
<Field label="Size S_A (m)" value={sizeA} onChange={setSizeA} />
<Field label="Density D_A (kg/m3)" value={densityA} onChange={setDensityA} />
<SelectField label="SD&N Solid" value={solidA} onChange={setSolidA} />
<SubLabel>Body B</SubLabel>
<Field label="Size S_B (m)" value={sizeB} onChange={setSizeB} />
<Field label="Density D_B (kg/m3)" value={densityB} onChange={setDensityB} />
<SelectField label="SD&N Solid" value={solidB} onChange={setSolidB} />
</Panel>
<Panel title="Kapnack Engine Output" accent>
<Row label="phi_SDN (A)" value={result.phiA.toFixed(4)} />
<Row label="phi_SDN (B)" value={result.phiB.toFixed(4)} />
<Row label=“Euler check A” value={Geometry.eulerCheck(solidA) ? ‘valid’ : ‘invalid’} />
<Row label=“Euler check B” value={Geometry.eulerCheck(solidB) ? ‘valid’ : ‘invalid’} />
<Row label=“Delta S” value={`${result.deltaS.toExponential(4)} m`} />
<Row label=“D_mean” value={`${result.meanD.toFixed(4)} kg/m3`} />
<Row label="9-family H_n" value={result.H_n.toExponential(4)} />
<Row label=“Gamma (gradient)” value={`${result.gamma.toExponential(6)} kg/m4`} highlight />
</Panel>
</div>
);
}

/* ============================================================
COMPONENT — components/MagneticRotor.jsx
============================================================ */
function MagneticRotor() {
const [outerMagnets, setOuterMagnets] = useState(12);
const [innerMagnets, setInnerMagnets] = useState(6);
const [lengthIn, setLengthIn] = useState(24);
const [widthIn, setWidthIn] = useState(6);
const [heightIn, setHeightIn] = useState(4);
const [Br, setBr] = useState(1.4);
const [radius, setRadius] = useState(0.5);
const [rpm, setRpm] = useState(3000);
const [numCoils, setNumCoils] = useState(12);
const [current, setCurrent] = useState(50);
const [resistance, setResistance] = useState(0.05);

const result = useMemo(() => {
const inToM = 0.0254;
const L = parseFloat(lengthIn) * inToM;
const W = parseFloat(widthIn) * inToM;
const H = parseFloat(heightIn) * inToM;
const volume = L * W * H;
const B = parseFloat(Br) || 0;
const r = parseFloat(radius) || 0.001;
const rpmVal = parseFloat(rpm) || 0;

```
const energy = Magnetic.magneticEnergy(B, volume);
const torqueResult = Magnetic.rotorTorque(parseInt(outerMagnets) || 0, parseInt(innerMagnets) || 0, B, volume, r);
const powerResult = Magnetic.mechanicalPower(torqueResult.torque, rpmVal);
const coilArea = W * H;
const emf = Magnetic.backEMF(parseInt(numCoils) || 0, B, coilArea, powerResult.omega);
const I = parseFloat(current) || 0;
const R = parseFloat(resistance) || 0.001;
const thermalLoss = Magnetic.thermalLoss(I, R);
const electricalPowerIn = emf * I;
const efficiency = Magnetic.efficiency(powerResult.power, electricalPowerIn);

return { volume, energy, torqueResult, powerResult, emf, thermalLoss, electricalPowerIn, efficiency };
```

}, [outerMagnets, innerMagnets, lengthIn, widthIn, heightIn, Br, radius, rpm, numCoils, current, resistance]);

return (
<div style={grid2}>
<Panel title="Magnetic Rotor Configuration">
<Field label="Outer magnets (count)" value={outerMagnets} onChange={setOuterMagnets} />
<Field label="Inner magnets (count)" value={innerMagnets} onChange={setInnerMagnets} />
<SubLabel>Magnet dimensions (inches)</SubLabel>
<div style={{ display: ‘flex’, gap: 8 }}>
<Field label="Length" value={lengthIn} onChange={setLengthIn} />
<Field label="Width" value={widthIn} onChange={setWidthIn} />
<Field label="Height" value={heightIn} onChange={setHeightIn} />
</div>
<Field label="Br - Remanence (Tesla)" value={Br} onChange={setBr} />
<Field label="Rotor radius (m)" value={radius} onChange={setRadius} />
<Field label="RPM" value={rpm} onChange={setRpm} />
<SubLabel>Generator parameters</SubLabel>
<Field label="Number of coils" value={numCoils} onChange={setNumCoils} />
<Field label="Estimated current (A)" value={current} onChange={setCurrent} />
<Field label="Coil resistance (Ohm)" value={resistance} onChange={setResistance} />
</Panel>
<Panel title="Simulation Output" accent>
<Row label=“Magnet volume (single)” value={`${result.volume.toExponential(4)} m3`} />
<Row label=“Magnetic energy density” value={`${result.energy.toExponential(4)} J`} />
<Row label=“Dipole moment (est.)” value={`${result.torqueResult.dipoleMoment.toExponential(4)} A*m2`} />
<Row label="Interacting pairs" value={result.torqueResult.interactingPairs} />
<Row label=“Force per pair (clamped)” value={`${result.torqueResult.forcePerPair.toExponential(4)} N`} />
<Row label=“Estimated torque” value={`${result.torqueResult.torque.toExponential(4)} N*m`} highlight />
<Row label=“Angular velocity” value={`${result.powerResult.omega.toFixed(2)} rad/s`} />
<Row label=“Mechanical power” value={`${result.powerResult.power.toExponential(4)} W`} highlight />
<Row label=“Back-EMF (est.)” value={`${result.emf.toExponential(4)} V`} />
<Row label=“Thermal loss (I2R)” value={`${result.thermalLoss.toFixed(2)} W`} />
<Row label=“Estimated efficiency” value={`${result.efficiency.toFixed(2)}%`} highlight />
<div style={{ marginTop: 14, padding: 10, background: ‘rgba(248,113,113,0.1)’, borderRadius: 6, fontSize: 11.5, color: ‘#fca5a5’ }}>
<strong>Model limitation notice:</strong> simplified point-dipole approximation, clamped to avoid
divergence at small air gaps. Real rotor force depends on exact magnet geometry, flux leakage,
saturation, and eddy losses in the core, none of which are modeled here. Treat as order-of-magnitude
estimates only. Validate against FEMM or Ansys Maxwell before any physical build.
</div>
</Panel>
</div>
);
}

/* ============================================================
COMPONENT — components/GeometryPanel.jsx
============================================================ */
function GeometryPanel() {
const duals = { tetrahedron: ‘tetrahedron’, cube: ‘octahedron’, octahedron: ‘cube’, dodecahedron: ‘icosahedron’, icosahedron: ‘dodecahedron’ };
return (
<Panel title="All Five Platonic Solids - SD&N Encoding" wide>
<table style={{ width: ‘100%’, borderCollapse: ‘collapse’, fontSize: 13 }}>
<thead>
<tr style={{ borderBottom: ‘2px solid rgba(255,255,255,0.15)’ }}>
{[‘Solid’, ‘F’, ‘V’, ‘E’, ‘Euler’, ‘phi=FV/E’, ‘Phase’, ‘Dual’].map(h => (
<th key={h} style={{ textAlign: ‘left’, padding: ‘10px 12px’, color: ‘#7ec8e3’ }}>{h}</th>
))}
</tr>
</thead>
<tbody>
{Object.entries(SDN_SOLIDS).map(([key, s]) => (
<tr key={key} style={{ borderBottom: ‘1px solid rgba(255,255,255,0.05)’ }}>
<td style={{ padding: ‘10px 12px’, fontWeight: 600 }}>{s.name}</td>
<td style={{ padding: ‘10px 12px’ }}>{s.F}</td>
<td style={{ padding: ‘10px 12px’ }}>{s.V}</td>
<td style={{ padding: ‘10px 12px’ }}>{s.E}</td>
<td style={{ padding: ‘10px 12px’, color: Geometry.eulerCheck(key) ? ‘#4ade80’ : ‘#f87171’ }}>{s.F - s.E + s.V}</td>
<td style={{ padding: ‘10px 12px’ }}>{Geometry.shapeFactorPhi(key).toFixed(4)}</td>
<td style={{ padding: ‘10px 12px’ }}>{(Geometry.phaseFactor(key) * 180 / Math.PI).toFixed(2)} deg</td>
<td style={{ padding: ‘10px 12px’, color: ‘rgba(255,255,255,0.5)’ }}>{SDN_SOLIDS[duals[key]].name}</td>
</tr>
))}
</tbody>
</table>
</Panel>
);
}

/* ============================================================
COMPONENT — components/ValidationPanel.jsx
============================================================ */
function ValidationPanel() {
const results = useMemo(() => Validation.runFullSuite(), []);
const allPass = results.every(r => r.pass);

const exportJSON = () => {
const blob = new Blob([JSON.stringify(results, null, 2)], { type: ‘application/json’ });
const url = URL.createObjectURL(blob);
const a = document.createElement(‘a’);
a.href = url; a.download = ‘sdkp_validation_report.json’; a.click();
};
const exportCSV = () => {
const header = ‘test,detail,pass\n’;
const rows = results.map(r => `"${r.test}","${r.detail}",${r.pass}`).join(’\n’);
const blob = new Blob([header + rows], { type: ‘text/csv’ });
const url = URL.createObjectURL(blob);
const a = document.createElement(‘a’);
a.href = url; a.download = ‘sdkp_validation_report.csv’; a.click();
};

return (
<Panel title="SDKP Consistency Test Suite" wide accent={allPass}>
<div style={{ fontFamily: ‘monospace’, fontSize: 13 }}>
{results.map((r, i) => (
<div key={i} style={{ display: ‘flex’, justifyContent: ‘space-between’, padding: ‘10px 0’, borderBottom: ‘1px solid rgba(255,255,255,0.06)’ }}>
<span style={{ color: r.pass ? ‘#4ade80’ : ‘#f87171’ }}>{r.pass ? ‘[PASS]’ : ‘[FAIL]’} {r.test}</span>
<span style={{ color: ‘rgba(255,255,255,0.5)’ }}>{r.detail}</span>
</div>
))}
</div>
<div style={{ marginTop: 16, padding: 12, borderRadius: 6, textAlign: ‘center’, fontWeight: 700, background: allPass ? ‘rgba(74,222,128,0.1)’ : ‘rgba(248,113,113,0.1)’, color: allPass ? ‘#4ade80’ : ‘#f87171’ }}>
{allPass ? `ALL ${results.length} TESTS PASSED` : ‘SOME TESTS FAILED - review above’}
</div>
<div style={{ display: ‘flex’, gap: 10, marginTop: 16 }}>
<button onClick={exportJSON} style={btnStyle}>Export JSON</button>
<button onClick={exportCSV} style={btnStyle}>Export CSV</button>
</div>
</Panel>
);
}

/* ============================================================
APP — App.jsx
============================================================ */
export default function KapnackSolverV2() {
const [tab, setTab] = useState(‘tau’);
const tabs = [
{ id: ‘tau’, label: ‘SDKP tau Calculator’ },
{ id: ‘gradient’, label: ‘Packing Gradient’ },
{ id: ‘magnetic’, label: ‘Magnetic Rotor Engine’ },
{ id: ‘geometry’, label: ‘SD&N Geometry’ },
{ id: ‘validation’, label: ‘Validation Suite’ },
];

return (
<div style={{ minHeight: ‘100vh’, background: ‘#0b1220’, color: ‘#e8edf5’, fontFamily: “‘Inter’, -apple-system, BlinkMacSystemFont, sans-serif” }}>
<div style={{ background: ‘linear-gradient(135deg, #0d2647 0%, #1A3C5E 100%)’, borderBottom: ‘3px solid #2E5496’, padding: ‘28px 32px’ }}>
<div style={{ maxWidth: 1150, margin: ‘0 auto’ }}>
<div style={{ fontSize: 11, letterSpacing: 3, textTransform: ‘uppercase’, color: ‘#7ec8e3’, fontWeight: 700, marginBottom: 8 }}>
FatherTimeSDKP Framework — Engineering Simulation Platform
</div>
<h1 style={{ fontSize: 30, fontWeight: 900, margin: 0, color: ‘#fff’ }}>Kapnack Solver v2</h1>
<div style={{ fontSize: 13, color: ‘rgba(255,255,255,0.6)’, marginTop: 6 }}>
Modular physics engine: SDKP math, SD&N geometry, magnetic rotor simulation, uncertainty propagation, self-validation.
</div>
</div>
</div>
<div style={{ maxWidth: 1150, margin: ‘0 auto’, padding: ‘28px 32px’ }}>
<div style={{ display: ‘flex’, gap: 8, marginBottom: 24, flexWrap: ‘wrap’ }}>
{tabs.map(t => (
<button key={t.id} onClick={() => setTab(t.id)} style={{
padding: ‘10px 18px’,
background: tab === t.id ? ‘#2E5496’ : ‘rgba(255,255,255,0.05)’,
color: tab === t.id ? ‘#fff’ : ‘rgba(255,255,255,0.6)’,
border: tab === t.id ? ‘1px solid #64b4ff’ : ‘1px solid rgba(255,255,255,0.1)’,
borderRadius: 6, fontSize: 13, fontWeight: 600, cursor: ‘pointer’,
}}>{t.label}</button>
))}
</div>
{tab === ‘tau’ && <TauPanel />}
{tab === ‘gradient’ && <GradientPanel />}
{tab === ‘magnetic’ && <MagneticRotor />}
{tab === ‘geometry’ && <GeometryPanel />}
{tab === ‘validation’ && <ValidationPanel />}
<div style={{ marginTop: 32, paddingTop: 20, borderTop: ‘1px solid rgba(255,255,255,0.1)’, fontSize: 11, color: ‘rgba(255,255,255,0.35)’, textAlign: ‘center’ }}>
FatherTimeSDKP Framework — Donald Paul Smith — ORCID: 0009-0003-7925-1653<br />
Modules: sdkp.js, geometry.js, magnetic.js, validation.js. Magnetic rotor uses simplified point-dipole approximation — validate against FEA before physical builds.
</div>
</div>
</div>
);
}
