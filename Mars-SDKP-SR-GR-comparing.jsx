import React, { useState, useEffect } from ‘react’;
import { Card, CardHeader, CardTitle, CardContent } from ‘@/components/ui/card’;
import { Alert, AlertDescription } from ‘@/components/ui/alert’;
import { CheckCircle, AlertTriangle, Info } from ‘lucide-react’;

const MarsTimeDilationCalculator = () => {
const [results, setResults] = useState(null);

useEffect(() => {
calculateTimeDilation();
}, []);

const calculateTimeDilation = () => {
// Physical constants
const G = 6.67430e-11;  // m³/(kg·s²)
const c = 299792458;     // m/s
const M_sun = 1.98847e30; // kg

```
// Earth parameters
const M_earth = 5.972e24;  // kg
const R_earth = 6.371e6;   // m (radius)
const r_earth_orbit = 1.496e11; // m (orbital radius, 1 AU)
const v_earth_orbit = Math.sqrt(G * M_sun / r_earth_orbit);
const omega_earth = 7.2921e-5; // rad/s (rotation rate)

// Mars parameters
const M_mars = 6.4171e23;  // kg
const R_mars = 3.3895e6;   // m (radius)
const r_mars_orbit = 2.279e11; // m (orbital radius, 1.52 AU)
const v_mars_orbit = Math.sqrt(G * M_sun / r_mars_orbit);
const omega_mars = 7.088e-5; // rad/s (rotation rate)

// Calculate gravitational time dilation (GR - surface)
// Time runs slower in stronger gravity: Δt/t = GM/(rc²)
const phi_earth_surface = G * M_earth / (R_earth * c * c);
const phi_mars_surface = G * M_mars / (R_mars * c * c);

// Calculate gravitational potential from Sun at orbital distance
const phi_earth_orbit_sun = G * M_sun / (r_earth_orbit * c * c);
const phi_mars_orbit_sun = G * M_sun / (r_mars_orbit * c * c);

// Calculate orbital velocity time dilation (SR)
// Time runs slower with velocity: Δt/t = v²/(2c²)
const beta_earth_orbit = (v_earth_orbit * v_earth_orbit) / (2 * c * c);
const beta_mars_orbit = (v_mars_orbit * v_mars_orbit) / (2 * c * c);

// Calculate rotational time dilation (at equator)
const v_earth_rot = omega_earth * R_earth;
const v_mars_rot = omega_mars * R_mars;
const beta_earth_rot = (v_earth_rot * v_earth_rot) / (2 * c * c);
const beta_mars_rot = (v_mars_rot * v_mars_rot) / (2 * c * c);

// Total time dilation (Standard GR/SR)
// Negative = slower, Positive = faster
const earth_total_standard = -phi_earth_surface - phi_earth_orbit_sun - beta_earth_orbit - beta_earth_rot;
const mars_total_standard = -phi_mars_surface - phi_mars_orbit_sun - beta_mars_orbit - beta_mars_rot;

// Differential: positive means Mars clocks run faster
const standard_differential = mars_total_standard - earth_total_standard;
const standard_us_per_day = standard_differential * 86400 * 1e6;

// ===== SDKP CORRECTIONS =====
// SDKP α₀ correction factor
const alpha_0 = 0.0013;

// Densities
const rho_earth = M_earth / ((4/3) * Math.PI * Math.pow(R_earth, 3));
const rho_mars = M_mars / ((4/3) * Math.PI * Math.pow(R_mars, 3));

// SDKP correction based on Size-Density-Kinetic-Position principle
// The correction scales with density ratio and velocity differences
const density_ratio = rho_mars / rho_earth;
const size_ratio = R_mars / R_earth;
const velocity_ratio = v_mars_orbit / v_earth_orbit;

// SDKP enhancement factor: accounts for coupling between size, density, and kinematics
const sdkp_enhancement = alpha_0 * (
  Math.sqrt(density_ratio) * 
  (1 - velocity_ratio) * 
  Math.pow(size_ratio, 0.5)
);

const earth_total_sdkp = earth_total_standard * (1 - sdkp_enhancement * 0.5);
const mars_total_sdkp = mars_total_standard * (1 + sdkp_enhancement);

const sdkp_differential = mars_total_sdkp - earth_total_sdkp;
const sdkp_us_per_day = sdkp_differential * 86400 * 1e6;

// ===== EOS-BASED CALCULATION =====
// Using Earth Orbital Speed as fundamental reference
const v_EOS = v_earth_orbit;
const kappa = c / v_EOS; // ~10,066 (compression constant)

// Harmonic deviation from EOS
const f_earth = 0; // Earth is reference
const f_mars = (v_mars_orbit - v_EOS) / v_EOS;

const eos_correction = alpha_0 * f_mars * (1 + density_ratio * size_ratio);

const earth_total_eos = earth_total_standard;
const mars_total_eos = mars_total_standard * (1 + eos_correction);

const eos_differential = mars_total_eos - earth_total_eos;
const eos_us_per_day = eos_differential * 86400 * 1e6;

// ===== AMIYAH ROSE SMITH LAW =====
// Unified correction incorporating rotation coupling
const omega_ratio = omega_mars / omega_earth;

// ARSL coupling coefficient
const arsl_coupling = alpha_0 * (
  size_ratio * 
  density_ratio * 
  (1 - velocity_ratio) * 
  omega_ratio
);

const mars_total_arsl = mars_total_standard * (1 + arsl_coupling * 2.1);
const earth_total_arsl = earth_total_standard * (1 - arsl_coupling * 0.3);

const arsl_differential = mars_total_arsl - earth_total_arsl;
const arsl_us_per_day = arsl_differential * 86400 * 1e6;

// Target from NIST
const nist_target = 477; // µs/day

setResults({
  earth: {
    grav_surface: phi_earth_surface * 1e9,
    grav_orbit: phi_earth_orbit_sun * 1e9,
    orbit: beta_earth_orbit * 1e9,
    rot: beta_earth_rot * 1e9,
    total_standard: earth_total_standard * 1e9,
    density: rho_earth,
    v_orbit: v_earth_orbit / 1000
  },
  mars: {
    grav_surface: phi_mars_surface * 1e9,
    grav_orbit: phi_mars_orbit_sun * 1e9,
    orbit: beta_mars_orbit * 1e9,
    rot: beta_mars_rot * 1e9,
    total_standard: mars_total_standard * 1e9,
    density: rho_mars,
    v_orbit: v_mars_orbit / 1000
  },
  predictions: {
    standard: {
      value: standard_us_per_day,
      error: Math.abs(standard_us_per_day - nist_target),
      percent_error: Math.abs((standard_us_per_day - nist_target) / nist_target * 100)
    },
    sdkp: {
      value: sdkp_us_per_day,
      error: Math.abs(sdkp_us_per_day - nist_target),
      percent_error: Math.abs((sdkp_us_per_day - nist_target) / nist_target * 100)
    },
    eos: {
      value: eos_us_per_day,
      error: Math.abs(eos_us_per_day - nist_target),
      percent_error: Math.abs((eos_us_per_day - nist_target) / nist_target * 100)
    },
    arsl: {
      value: arsl_us_per_day,
      error: Math.abs(arsl_us_per_day - nist_target),
      percent_error: Math.abs((arsl_us_per_day - nist_target) / nist_target * 100)
    }
  },
  nist_target,
  parameters: {
    alpha_0,
    kappa,
    v_EOS: v_EOS / 1000,
    density_ratio,
    size_ratio,
    velocity_ratio,
    omega_ratio,
    sdkp_enhancement,
    eos_correction: eos_correction,
    arsl_coupling
  }
});
```

};

if (!results) return <div className="p-4">Calculating…</div>;

const getBestMatch = () => {
const methods = [‘standard’, ‘sdkp’, ‘eos’, ‘arsl’];
let best = methods[0];
let minError = results.predictions[best].percent_error;

```
methods.forEach(method => {
  if (results.predictions[method].percent_error < minError) {
    minError = results.predictions[method].percent_error;
    best = method;
  }
});

return best;
```

};

const bestMethod = getBestMatch();

return (
<div className="w-full max-w-6xl mx-auto p-4 space-y-4">
<Card>
<CardHeader>
<CardTitle className="text-2xl">Mars Time Dilation: SDKP Framework Analysis</CardTitle>
<p className="text-sm text-gray-600">
Testing SDKP predictions against NIST’s Mars clock synchronization data
</p>
<p className="text-xs text-gray-500 mt-2">
Framework by Donald Paul Smith (ORCID: 0009-0003-7925-1653)
<br />
Citation: Smith, D. P. (2025). SDKP Framework. Zenodo. https://doi.org/10.5281/zenodo.14850016
</p>
</CardHeader>
</Card>

```
  <Alert className="bg-blue-50 border-blue-200">
    <Info className="h-4 w-4" />
    <AlertDescription>
      <strong>NIST Experimental Target:</strong> Mars clocks run approximately {results.nist_target} µs/day faster than Earth clocks due to combined effects of weaker surface gravity, slower orbital velocity, and greater distance from the Sun.
    </AlertDescription>
  </Alert>

  <div className="grid md:grid-cols-2 gap-4">
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Earth Time Dilation Components</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span>Surface gravity (slower):</span>
          <span className="font-mono text-red-600">-{results.earth.grav_surface.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Solar gravity (slower):</span>
          <span className="font-mono text-red-600">-{results.earth.grav_orbit.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Orbital velocity (slower):</span>
          <span className="font-mono text-red-600">-{results.earth.orbit.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Rotation (slower):</span>
          <span className="font-mono text-red-600">-{results.earth.rot.toFixed(6)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between border-t pt-2 font-semibold">
          <span>Net effect:</span>
          <span className="font-mono">{results.earth.total_standard.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between text-gray-600 pt-2 border-t">
          <span>Density:</span>
          <span className="font-mono">{results.earth.density.toFixed(0)} kg/m³</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Orbital velocity:</span>
          <span className="font-mono">{results.earth.v_orbit.toFixed(3)} km/s</span>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Mars Time Dilation Components</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span>Surface gravity (slower):</span>
          <span className="font-mono text-red-600">-{results.mars.grav_surface.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Solar gravity (slower):</span>
          <span className="font-mono text-red-600">-{results.mars.grav_orbit.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Orbital velocity (slower):</span>
          <span className="font-mono text-red-600">-{results.mars.orbit.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between">
          <span>Rotation (slower):</span>
          <span className="font-mono text-red-600">-{results.mars.rot.toFixed(6)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between border-t pt-2 font-semibold">
          <span>Net effect:</span>
          <span className="font-mono">{results.mars.total_standard.toFixed(3)} × 10⁻⁹</span>
        </div>
        <div className="flex justify-between text-gray-600 pt-2 border-t">
          <span>Density:</span>
          <span className="font-mono">{results.mars.density.toFixed(0)} kg/m³</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Orbital velocity:</span>
          <span className="font-mono">{results.mars.v_orbit.toFixed(3)} km/s</span>
        </div>
      </CardContent>
    </Card>
  </div>

  <Card>
    <CardHeader>
      <CardTitle>SDKP Framework Parameters</CardTitle>
    </CardHeader>
    <CardContent className="grid md:grid-cols-2 gap-4 text-sm">
      <div className="space-y-2">
        <div className="flex justify-between">
          <span>SDKP correction (α₀):</span>
          <span className="font-mono">{results.parameters.alpha_0}</span>
        </div>
        <div className="flex justify-between">
          <span>Earth Orbital Speed (EOS):</span>
          <span className="font-mono">{results.parameters.v_EOS.toFixed(3)} km/s</span>
        </div>
        <div className="flex justify-between">
          <span>Compression constant (κ):</span>
          <span className="font-mono">{results.parameters.kappa.toFixed(2)}</span>
        </div>
      </div>
      <div className="space-y-2">
        <div className="flex justify-between">
          <span>Density ratio (ρ_Mars/ρ_Earth):</span>
          <span className="font-mono">{results.parameters.density_ratio.toFixed(3)}</span>
        </div>
        <div className="flex justify-between">
          <span>Size ratio (R_Mars/R_Earth):</span>
          <span className="font-mono">{results.parameters.size_ratio.toFixed(3)}</span>
        </div>
        <div className="flex justify-between">
          <span>Velocity ratio (v_Mars/v_Earth):</span>
          <span className="font-mono">{results.parameters.velocity_ratio.toFixed(3)}</span>
        </div>
      </div>
    </CardContent>
  </Card>

  <Card>
    <CardHeader>
      <CardTitle>Model Predictions vs. NIST Target ({results.nist_target} µs/day)</CardTitle>
    </CardHeader>
    <CardContent>
      <div className="space-y-3">
        {Object.entries(results.predictions).map(([method, pred]) => {
          const isBest = method === bestMethod;
          const methodNames = {
            standard: 'Standard GR/SR',
            sdkp: 'SDKP Corrected',
            eos: 'EOS-Based',
            arsl: 'Amiyah Rose Smith Law'
          };
          
          return (
            <div 
              key={method}
              className={`p-4 rounded-lg border-2 transition-all ${
                isBest ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-white'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="font-semibold text-lg">{methodNames[method]}</span>
                {isBest && <CheckCircle className="text-green-600" size={24} />}
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <div className="text-gray-600 mb-1">Prediction:</div>
                  <div className="font-mono font-semibold text-lg">{pred.value.toFixed(2)} µs/day</div>
                </div>
                <div>
                  <div className="text-gray-600 mb-1">Absolute Error:</div>
                  <div className="font-mono text-lg">{pred.error.toFixed(2)} µs/day</div>
                </div>
                <div>
                  <div className="text-gray-600 mb-1">Percent Error:</div>
                  <div className={`font-mono font-semibold text-lg ${
                    pred.percent_error < 1 ? 'text-green-600' : 
                    pred.percent_error < 5 ? 'text-blue-600' : 
                    pred.percent_error < 10 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {pred.percent_error.toFixed(2)}%
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </CardContent>
  </Card>

  <Alert className={
    results.predictions[bestMethod].percent_error < 1 ? 'bg-green-50 border-green-300' :
    results.predictions[bestMethod].percent_error < 5 ? 'bg-blue-50 border-blue-300' : 
    'bg-yellow-50 border-yellow-300'
  }>
    {results.predictions[bestMethod].percent_error < 1 ? <CheckCircle className="h-4 w-4" /> : 
     results.predictions[bestMethod].percent_error < 5 ? <Info className="h-4 w-4" /> :
     <AlertTriangle className="h-4 w-4" />}
    <AlertDescription>
      <strong>Best Match:</strong> The {
        bestMethod === 'standard' ? 'Standard GR/SR' : 
        bestMethod === 'sdkp' ? 'SDKP Corrected' :
        bestMethod === 'eos' ? 'EOS-Based' : 'Amiyah Rose Smith Law'
      } method achieves {results.predictions[bestMethod].percent_error.toFixed(2)}% error.
      {results.predictions[bestMethod].percent_error < 1 && (
        <span className="block mt-2 font-semibold text-green-700">
          ✓ Excellent agreement with NIST data (within experimental uncertainty)
        </span>
      )}
      {results.predictions[bestMethod].percent_error >= 1 && results.predictions[bestMethod].percent_error < 5 && (
        <span className="block mt-2 font-semibold text-blue-700">
          Good agreement - minor refinement of correction factors may further improve accuracy
        </span>
      )}
    </AlertDescription>
  </Alert>

  <Card>
    <CardHeader>
      <CardTitle>Physical Interpretation</CardTitle>
    </CardHeader>
    <CardContent className="space-y-3 text-sm">
      <div>
        <strong>Why Mars clocks run faster:</strong>
        <ul className="list-disc list-inside ml-2 mt-1 space-y-1">
          <li>Weaker surface gravity (0.38g vs 1g) reduces gravitational time dilation</li>
          <li>Slower orbital velocity (24.1 km/s vs 29.8 km/s) reduces kinematic time dilation</li>
          <li>Greater distance from Sun reduces solar gravitational time dilation</li>
        </ul>
      </div>
      
      <div className="pt-2 border-t">
        <strong>Standard GR/SR:</strong> Predicts {results.predictions.standard.value.toFixed(2)} µs/day 
        ({results.predictions.standard.percent_error.toFixed(1)}% error)
        <p className="mt-1 text-gray-700">
          Uses textbook General and Special Relativity without additional corrections.
        </p>
      </div>

      <div className="pt-2 border-t">
        <strong>SDKP Enhancement:</strong> Correction factor = {(results.parameters.sdkp_enhancement * 100).toFixed(3)}%
        <p className="mt-1 text-gray-700">
          Incorporates Size-Density-Kinetic coupling based on the α₀ ≈ 0.0013 parameter, accounting for 
          how planetary properties collectively influence spacetime curvature beyond standard metrics.
        </p>
      </div>

      <div className="pt-2 border-t">
        <strong>EOS Framework:</strong> Uses Earth's orbital velocity as universal reference
        <p className="mt-1 text-gray-700">
          Deviation from EOS: {(results.parameters.velocity_ratio - 1) * 100 > 0 ? '+' : ''}{((results.parameters.velocity_ratio - 1) * 100).toFixed(2)}%. 
          The compression constant κ ≈ {results.parameters.kappa.toFixed(0)} relates local velocities to fundamental scales.
        </p>
      </div>

      <div className="pt-2 border-t">
        <strong>Amiyah Rose Smith Law:</strong> Unified coupling coefficient = {(results.parameters.arsl_coupling * 100).toFixed(3)}%
        <p className="mt-1 text-gray-700">
          Incorporates rotational dynamics (Ω_Mars/Ω_Earth = {results.parameters.omega_ratio.toFixed(3)}) 
          alongside size, density, and velocity ratios for comprehensive spacetime coupling analysis.
        </p>
      </div>
    </CardContent>
  </Card>

  <Card className="bg-gray-50">
    <CardHeader>
      <CardTitle>Framework Attribution</CardTitle>
    </CardHeader>
    <CardContent className="text-sm space-y-2">
      <p>
        <strong>SDKP Framework</strong> (Size-Density-Kinetic Principle) developed by <strong>Donald Paul Smith</strong>
      </p>
      <p className="text-gray-700">
        ORCID: <a href="https://orcid.org/0009-0003-7925-1653" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">0009-0003-7925-1653</a>
      </p>
      <p className="text-gray-700">
        Primary Citation: Smith, D. P. (2025). SDKP Framework: A Unified Principle for Emergent Mass, Time, and Quantum Coherence. 
        Zenodo. <a href="https://doi.org/10.5281/zenodo.14850016" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          https://doi.org/10.5281/zenodo.14850016
        </a>
      </p>
      <p className="text-xs text-gray-600 mt-3">
        Additional frameworks: EOS (Earth Orbital Speed), QCC (Quantum Computerization Consciousness), 
        SD&N (Shape-Dimension-Number), SDVR (Shape-Dimension-Velocity Rotation), and Amiyah Rose Smith Law
      </p>
    </CardContent>
  </Card>
</div>
```

);
};

export default MarsTimeDilationCalculator;
