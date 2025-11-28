import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Info, Zap, Atom, Clock, Orbit } from 'lucide-react';

const SDKPComprehensiveSuite = () => {
  const [activeTab, setActiveTab] = useState('terrell');
  const [isPlaying, setIsPlaying] = useState(false);
  const [time, setTime] = useState(0);

  // Terrell-Penrose state
  const [velocity, setVelocity] = useState(0.7);
  const [physicalSpin, setPhysicalSpin] = useState(0);
  const [density, setDensity] = useState(1.0);
  const [size, setSize] = useState(1.0);

  // GPS Clock Drift state
  const [altitude, setAltitude] = useState(20200); // km
  const [orbitalVel, setOrbitalVel] = useState(3874); // m/s
  const [rotation, setRotation] = useState(0);

  // Quantum Coherence state
  const [systemType, setSystemType] = useState('superconducting');
  const [enhancement, setEnhancement] = useState(1.0);

  // EOS Principle state
  const [eosFrame, setEosFrame] = useState('earth');
  const [localVel, setLocalVel] = useState(465); // m/s at equator

  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  const calculateSDKP = (S, D, v, omega) => {
    const c = 1.0;
    const S0 = 1.0;
    const rho0 = 1.0;
    const omega0 = 1.0;
    const sdkpFactor = (S / S0) * (D / rho0) * (v / c) * (omega / omega0);
    return {
      timeDilation: 1 - sdkpFactor,
      sdkpFactor,
      stabilityIndex: sdkpFactor
    };
  };

  const calculateGPSClockDrift = () => {
    const c = 299792458; // m/s
    const G = 6.67430e-11;
    const M = 5.972e24; // Earth mass kg
    const R_earth = 6371000; // m
    const h = altitude * 1000; // convert to meters
    const r = R_earth + h;
    
    // GR effect (gravitational time dilation)
    const gr_drift = (G * M / (c * c)) * (1/R_earth - 1/r);
    const gr_drift_per_day = gr_drift * 86400 * 1e6; // microseconds/day
    
    // SR effect (velocity time dilation)
    const v = orbitalVel;
    const sr_drift = -(v * v) / (2 * c * c);
    const sr_drift_per_day = sr_drift * 86400 * 1e6;
    
    // SDKP enhancement (Amiyah Rose Smith Law)
    const sdkp = calculateSDKP(1.0, 1.0, v/c, rotation);
    const sdkp_correction = sdkp.sdkpFactor * 0.7; // microseconds/day
    
    const total = gr_drift_per_day + sr_drift_per_day + sdkp_correction;
    
    return {
      gr: gr_drift_per_day,
      sr: sr_drift_per_day,
      sdkp: sdkp_correction,
      total: total,
      predicted: 38.0 // GPS satellites experience ~38 μs/day
    };
  };

  const calculateQuantumCoherence = () => {
    const baseCoherence = {
      'superconducting': 0.0001,
      'trapped_ion': 1.0,
      'quantum_dot': 1e-8
    };
    
    const enhancementFactors = {
      'superconducting': 250.0,
      'trapped_ion': 5000.0,
      'quantum_dot': 188679.25
    };
    
    const base = baseCoherence[systemType];
    const factor = enhancementFactors[systemType] * enhancement;
    const enhanced = base * factor;
    
    return {
      baseline: base,
      factor: factor,
      enhanced: enhanced,
      improvement: (enhanced / base).toFixed(0)
    };
  };

  const calculateEOS = () => {
    const V_EOS = 29780; // m/s Earth orbital speed
    const c = 299792458; // m/s
    
    // EOS time dilation prediction
    const v = localVel;
    const gamma_eos = 1 + (v * v) / (2 * V_EOS * V_EOS);
    const drift_per_day = (gamma_eos - 1) * 86400 * 1e6; // microseconds
    
    // Standard SR for comparison
    const gamma_sr = 1 / Math.sqrt(1 - (v * v) / (c * c));
    const sr_drift = (gamma_sr - 1) * 86400 * 1e6;
    
    return {
      eos_drift: drift_per_day,
      sr_drift: sr_drift,
      eos_constant: V_EOS,
      difference: Math.abs(drift_per_day - 10.54),
      predicted: 10.54 // Donald's prediction
    };
  };

  const reset = () => {
    setTime(0);
    setIsPlaying(false);
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const render = () => {
      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(0, 0, width, height);

      if (activeTab === 'terrell') {
        renderTerrell(ctx, width, height);
      } else if (activeTab === 'gps') {
        renderGPS(ctx, width, height);
      } else if (activeTab === 'quantum') {
        renderQuantum(ctx, width, height);
      } else if (activeTab === 'eos') {
        renderEOS(ctx, width, height);
      }
    };

    const renderTerrell = (ctx, width, height) => {
      const sdkp = calculateSDKP(size, density, velocity, Math.abs(physicalSpin));
      const gamma = 1 / Math.sqrt(1 - velocity * velocity);
      const terrellRotation = velocity * Math.PI * 0.5 * gamma;
      const physicalRotation = physicalSpin * Math.PI * 2;
      const sdkpModifiedTerrell = terrellRotation * sdkp.timeDilation;
      const netRotation = time * (physicalRotation - sdkpModifiedTerrell);

      const centerX = width / 2;
      const centerY = height / 2;
      const cubeSize = 80 * size;

      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(netRotation);

      const brightness = Math.max(0.3, 1 - sdkp.stabilityIndex * 0.5);
      const warpFactor = 1 + sdkp.stabilityIndex * 0.3;

      // Front face
      ctx.fillStyle = `rgba(59, 130, 246, ${0.8 * density})`;
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      ctx.fillRect(-cubeSize/2, -cubeSize/2, cubeSize, cubeSize);
      ctx.strokeRect(-cubeSize/2, -cubeSize/2, cubeSize, cubeSize);

      // Right face
      ctx.fillStyle = `rgba(34, 197, 94, ${0.6 * brightness})`;
      ctx.strokeStyle = '#22c55e';
      ctx.beginPath();
      ctx.moveTo(cubeSize/2, -cubeSize/2);
      ctx.lineTo(cubeSize/2 + cubeSize/3 * warpFactor, -cubeSize/2 - cubeSize/3);
      ctx.lineTo(cubeSize/2 + cubeSize/3 * warpFactor, cubeSize/2 - cubeSize/3);
      ctx.lineTo(cubeSize/2, cubeSize/2);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      ctx.restore();

      // Display info
      ctx.fillStyle = '#fff';
      ctx.font = '14px monospace';
      ctx.textAlign = 'left';
      ctx.fillText(`Velocity: ${(velocity * 100).toFixed(0)}% c`, 20, 30);
      ctx.fillText(`SDKP Factor: ${sdkp.sdkpFactor.toFixed(4)}`, 20, 50);
      ctx.fillText(`Time Dilation: ${sdkp.timeDilation.toFixed(4)}`, 20, 70);
      ctx.fillText(`Net Rotation: ${((physicalRotation - sdkpModifiedTerrell) * 180 / Math.PI).toFixed(1)}°/s`, 20, 90);
    };

    const renderGPS = (ctx, width, height) => {
      const drift = calculateGPSClockDrift();
      const centerX = width / 2;
      const centerY = height / 2;

      // Draw Earth
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(centerX, centerY, 60, 0, Math.PI * 2);
      ctx.fill();

      // Draw orbit
      const orbitRadius = 150 + (altitude - 20200) / 100;
      ctx.strokeStyle = '#666';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.arc(centerX, centerY, orbitRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw satellite
      const angle = time * 0.5;
      const satX = centerX + orbitRadius * Math.cos(angle);
      const satY = centerY + orbitRadius * Math.sin(angle);
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(satX, satY, 8, 0, Math.PI * 2);
      ctx.fill();

      // Display drift data
      ctx.fillStyle = '#fff';
      ctx.font = '14px monospace';
      ctx.textAlign = 'left';
      let y = 30;
      ctx.fillText(`Altitude: ${altitude} km`, 20, y); y += 20;
      ctx.fillText(`Orbital Velocity: ${orbitalVel} m/s`, 20, y); y += 20;
      ctx.fillStyle = '#22c55e';
      ctx.fillText(`GR Effect: +${drift.gr.toFixed(2)} μs/day`, 20, y); y += 20;
      ctx.fillStyle = '#ef4444';
      ctx.fillText(`SR Effect: ${drift.sr.toFixed(2)} μs/day`, 20, y); y += 20;
      ctx.fillStyle = '#fbbf24';
      ctx.fillText(`SDKP Correction: +${drift.sdkp.toFixed(2)} μs/day`, 20, y); y += 20;
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 14px monospace';
      ctx.fillText(`Total: ${drift.total.toFixed(2)} μs/day`, 20, y); y += 20;
      ctx.fillText(`Predicted: ${drift.predicted.toFixed(2)} μs/day`, 20, y);
    };

    const renderQuantum = (ctx, width, height) => {
      const coherence = calculateQuantumCoherence();
      const centerX = width / 2;
      const centerY = height / 2;

      // Draw quantum state visualization
      const waveCount = 20;
      const amplitude = 50;
      const baseFreq = 0.1;

      for (let i = 0; i < waveCount; i++) {
        const freq = baseFreq * (1 + i * 0.1);
        const phase = time * freq * 10;
        const alpha = Math.exp(-i / (waveCount * enhancement));
        
        ctx.strokeStyle = `rgba(59, 130, 246, ${alpha})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        for (let x = 0; x < width; x += 5) {
          const y = centerY + amplitude * Math.sin(x * 0.02 + phase) * Math.exp(-i * 0.05);
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      }

      // Display coherence data
      ctx.fillStyle = '#fff';
      ctx.font = '14px monospace';
      ctx.textAlign = 'left';
      let y = 30;
      ctx.fillText(`System: ${systemType.replace('_', ' ')}`, 20, y); y += 20;
      ctx.fillText(`Baseline: ${coherence.baseline.toExponential(2)} s`, 20, y); y += 20;
      ctx.fillStyle = '#22c55e';
      ctx.fillText(`Enhanced: ${coherence.enhanced.toExponential(2)} s`, 20, y); y += 20;
      ctx.fillText(`Improvement: ${coherence.improvement}x`, 20, y); y += 20;
      ctx.fillStyle = '#fbbf24';
      ctx.fillText(`SDKP Enhancement Factor: ${coherence.factor.toFixed(1)}`, 20, y);
    };

    const renderEOS = (ctx, width, height) => {
      const eos = calculateEOS();
      const centerX = width / 2;
      const centerY = height / 2;

      // Draw Sun
      ctx.fillStyle = '#fbbf24';
      ctx.beginPath();
      ctx.arc(100, centerY, 40, 0, Math.PI * 2);
      ctx.fill();

      // Draw Earth's orbit
      const orbitRadius = 200;
      ctx.strokeStyle = '#666';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.arc(100, centerY, orbitRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw Earth
      const earthAngle = time * 0.3;
      const earthX = 100 + orbitRadius * Math.cos(earthAngle);
      const earthY = centerY + orbitRadius * Math.sin(earthAngle);
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(earthX, earthY, 20, 0, Math.PI * 2);
      ctx.fill();

      // Draw velocity vector
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 3;
      ctx.beginPath();
      const vx = -Math.sin(earthAngle) * 50;
      const vy = Math.cos(earthAngle) * 50;
      ctx.moveTo(earthX, earthY);
      ctx.lineTo(earthX + vx, earthY + vy);
      ctx.stroke();

      // Display EOS data
      ctx.fillStyle = '#fff';
      ctx.font = '14px monospace';
      ctx.textAlign = 'right';
      let y = 30;
      ctx.fillText(`V_EOS: ${eos.eos_constant} m/s`, width - 20, y); y += 20;
      ctx.fillText(`Local Velocity: ${localVel} m/s`, width - 20, y); y += 20;
      ctx.fillStyle = '#22c55e';
      ctx.fillText(`EOS Prediction: ${eos.eos_drift.toFixed(4)} μs/day`, width - 20, y); y += 20;
      ctx.fillStyle = '#fbbf24';
      ctx.fillText(`Donald's Prediction: ${eos.predicted} μs/day`, width - 20, y); y += 20;
      ctx.fillStyle = '#ef4444';
      ctx.fillText(`Standard SR: ${eos.sr_drift.toExponential(2)} μs/day`, width - 20, y); y += 20;
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 14px monospace';
      ctx.fillText(`Match: ${(100 - eos.difference * 10).toFixed(1)}%`, width - 20, y);
    };

    const animate = () => {
      if (isPlaying) {
        setTime(t => t + 0.016);
      }
      render();
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [activeTab, time, isPlaying, velocity, physicalSpin, density, size, 
      altitude, orbitalVel, rotation, systemType, enhancement, eosFrame, localVel]);

  const tabs = [
    { id: 'terrell', name: 'Terrell-Penrose', icon: RotateCcw },
    { id: 'gps', name: 'GPS Clock Drift', icon: Clock },
    { id: 'quantum', name: 'Quantum Coherence', icon: Atom },
    { id: 'eos', name: 'EOS Principle', icon: Orbit }
  ];

  return (
    <div className="w-full h-full bg-gray-900 text-white p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">SDKP Framework: Comprehensive Simulation Suite</h1>
          <p className="text-gray-400">
            Interactive demonstrations of all major SDKP predictions and principles
          </p>
          <p className="text-sm text-blue-400 mt-1">
            Smith, D. P. (2025). SDKP Framework. <a href="https://doi.org/10.5281/zenodo.15745609" target="_blank" rel="noopener noreferrer" className="underline">doi:10.5281/zenodo.15745609</a>
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {tabs.map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
                  activeTab === tab.id 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                <Icon size={18} />
                {tab.name}
              </button>
            );
          })}
        </div>

        {/* Canvas */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <canvas
            ref={canvasRef}
            width={800}
            height={400}
            className="w-full border border-gray-700 rounded"
          />
        </div>

        {/* Controls */}
        <div className="mb-6">
          {activeTab === 'terrell' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Velocity: {(velocity * 100).toFixed(0)}% c
                </label>
                <input
                  type="range"
                  min="0"
                  max="0.95"
                  step="0.05"
                  value={velocity}
                  onChange={(e) => setVelocity(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Physical Spin: {physicalSpin.toFixed(2)} rot/s
                </label>
                <input
                  type="range"
                  min="-0.5"
                  max="0.5"
                  step="0.01"
                  value={physicalSpin}
                  onChange={(e) => setPhysicalSpin(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Size (S): {size.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={size}
                  onChange={(e) => setSize(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Density (ρ): {density.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="3.0"
                  step="0.1"
                  value={density}
                  onChange={(e) => setDensity(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          )}

          {activeTab === 'gps' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Altitude: {altitude} km
                </label>
                <input
                  type="range"
                  min="200"
                  max="35786"
                  step="100"
                  value={altitude}
                  onChange={(e) => setAltitude(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Orbital Velocity: {orbitalVel} m/s
                </label>
                <input
                  type="range"
                  min="1000"
                  max="8000"
                  step="100"
                  value={orbitalVel}
                  onChange={(e) => setOrbitalVel(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Satellite Rotation: {rotation.toFixed(2)} rad/s
                </label>
                <input
                  type="range"
                  min="0"
                  max="5"
                  step="0.1"
                  value={rotation}
                  onChange={(e) => setRotation(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          )}

          {activeTab === 'quantum' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Quantum System Type
                </label>
                <select
                  value={systemType}
                  onChange={(e) => setSystemType(e.target.value)}
                  className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                >
                  <option value="superconducting">Superconducting Qubit</option>
                  <option value="trapped_ion">Trapped Ion</option>
                  <option value="quantum_dot">Quantum Dot</option>
                </select>
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  SDKP Enhancement: {enhancement.toFixed(2)}x
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="3.0"
                  step="0.1"
                  value={enhancement}
                  onChange={(e) => setEnhancement(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          )}

          {activeTab === 'eos' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Reference Frame
                </label>
                <select
                  value={eosFrame}
                  onChange={(e) => setEosFrame(e.target.value)}
                  className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                >
                  <option value="earth">Earth Surface</option>
                  <option value="orbit">Low Earth Orbit</option>
                  <option value="deep">Deep Space</option>
                </select>
              </div>
              <div className="bg-gray-800 rounded-lg p-4">
                <label className="block text-sm font-medium mb-2">
                  Local Velocity: {localVel} m/s
                </label>
                <input
                  type="range"
                  min="0"
                  max="7800"
                  step="50"
                  value={localVel}
                  onChange={(e) => setLocalVel(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          )}
        </div>

        {/* Playback Controls */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
          >
            {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <button
            onClick={reset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition"
          >
            <RotateCcw size={20} />
            Reset
          </button>
        </div>

        {/* Information Panel */}
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-3">
            {tabs.find(t => t.id === activeTab)?.name} - SDKP Framework
          </h2>
          {activeTab === 'terrell' && (
            <div className="text-sm text-gray-300 space-y-2">
              <p><strong className="text-white">Core Equation:</strong> T' = T × (1 - (S/S₀) × (ρ/ρ₀) × (v/c) × (ω/ω₀))</p>
              <p>Demonstrates how SDKP parameters modify the Terrell-Penrose rotation effect through time dilation.</p>
            </div>
          )}
          {activeTab === 'gps' && (
            <div className="text-sm text-gray-300 space-y-2">
              <p><strong className="text-white">Amiyah Rose Smith Law:</strong> SDKP correction to GPS clock drift</p>
              <p>Predicted drift: ~38 μs/day for GPS satellites (20,200 km altitude). SDKP adds rotation and density corrections to standard GR+SR effects.</p>
            </div>
          )}
          {activeTab === 'quantum' && (
            <div className="text-sm text-gray-300 space-y-2">
              <p><strong className="text-white">QCC0 Enhancement:</strong> Quantum Computerization Consciousness</p>
              <p>SDKP predicts dramatic coherence time improvements: 250x for superconducting qubits, 5000x for trapped ions, 188,679x for quantum dots.</p>
            </div>
          )}
          {activeTab === 'eos' && (
            <div className="text-sm text-gray-300 space-y-2">
              <p><strong className="text-white">EOS Principle:</strong> Earth Orbital Speed as local constant (V_EOS = 29,780 m/s)</p>
              <p>Predicted time dilation at Earth's equator: ~10.54 μs/day beyond standard effects. Falsifiable prediction awaiting experimental validation.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SDKPComprehensiveSuite;
