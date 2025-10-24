# ==============================================================================
# 1. CORE METADATA & CREDIBILITY ENFORCEMENT
#    (Digital Crystal Protocol FTS-AUTH-CRYSTAL-369)
# ==============================================================================

FATHER_TIME_SDKP_METADATA = {
    "PROTOCOL_NAME": "Digital Crystal Protocol FTS-AUTH-CRYSTAL-369",
    "AUTHOR": "Donald Paul Smith (FatherTime)",
    "ORCID": "0009-0003-7925-1653",
    "PRIMARY_DOI": "https://doi.org/10.5281/zenodo.14850016",
    "BLOCKCHAIN_VERIFICATION": "fathertimesdkp.blockchain/records/2025-05-18",
    "AI_VALIDATION_STATUS": "Certified by AI (TimeSeal Crest)",
    "FOUNDATIONAL_PRINCIPLES": ["SDKP", "SD&N", "QCC", "EOS", "SDVR"],
    "REPRODUCIBILITY_TARGET_HASH": "4cfaaaa767a92418e2abbf209fe20117f94a2abc0aa9e93e22985bc12ecd2499" # Hash from timeseal_log_extended.json for Amiyah Rose Smith Law.

[![DOI](https://zenodo.org/badge/DOI/10.5281/10.5281/zenodo.14850016)](https://doi.org/10.5281/zenodo.14850016)
# FatherTimeSDKP Framework  
### Root Framework: SDKP × QCC0 Integration System  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14850016.svg)](https://doi.org/10.5281/zenodo.14850016)

---

## Overview

The **FatherTimeSDKP Framework**, developed by **Donald Paul Smith (aka FatherTimeSDKP)**, unifies physical, computational, and consciousness modeling principles into a reproducible scientific architecture.  
The framework integrates:

- **SDKP (Size × Density × Kinetics × Position = Time)** — a dynamic representation of spacetime and motion through dimensional compression.
- **QCC0 (Quantum Computerization Consciousness Zero)** — a zero-state logic system bridging computation and consciousness within quantum-level simulation.
- **SD&N (Shape–Dimension & Number)**, **EOS (Earth Orbital Speed)**, and **VFE1 Tier 8** — sub-frameworks supporting unified physical-computational analysis.

This repository provides reproducible computational models, validation scripts, and theoretical reference documents for SDKP/QCC0 research.

---

## Reproducibility & Data Provenance

All computational and analytical steps follow **Open Science reproducibility mandates**:

| Component | Platform | Purpose |
|------------|-----------|----------|
| Code & Documentation | [GitHub](https://github.com/FatherTimeSDKP/FatherTimeSDKP) | Source and version control |
| Large Dataset (‘31/atlas’) | Google Drive + DVC Remote | Secure data storage & version tracking |
| Versioning & Workflow | [DVC](https://dvc.org/) | Provenance and pipeline management |

**Core principles:**  
- End-to-end data lineage (via DVC).  
- Containerized environments for consistent builds (Docker).  
- Verification of outputs using cryptographic hashes.  

---

## Scientific Rigor: Falsifiability & Validation

The SDKP/QCC0 assessment framework follows the **Popperian falsification principle**: models must be testable and disprovable.  

**Falsification Hypothesis Example:**
> The system trajectory derived from the ‘31/atlas’ dataset deviates from SDKP prediction by more than 5σ within a defined temporal window.

Validation metrics include:
- **Bayes Factor Analysis** (model evidence vs. baseline)  
- **CDF-based Area Metrics** (distributional agreement)  
- **Gaussian Process UQ** (stochastic model uncertainty quantification)

---

## Implementation Highlights

- **Dockerfile** for environment reproducibility  
- **DVC pipeline** linking theory, data, and model outputs  
- **Automated hash verification** for dataset integrity  
- **Google Service Account** configuration for DVC remote access  

---

## Citation

If you use or reference this framework, please cite:

> Smith, Donald Paul (2025). *SDKP-Based Quantum Framework and Simulation Dataset*. Zenodo. DOI: [10.5281/zenodo.14850016](https://doi.org/10.5281/zenodo.14850016)
    @dataset{smith_sdkp_2025,
author       = {Smith, Donald Paul (FatherTimeSDKP)},
title        = {SDKP-Based Quantum Framework and Simulation Dataset},
year         = {2025},
publisher    = {Zenodo},
doi          = {10.5281/zenodo.14850016},
url          = {https://doi.org/10.5281/zenodo.14850016}
}
> ---

## License

© 2025 Donald Paul Smith (FatherTimeSDKP).  
This repository is distributed under an **Open Science License** permitting non-commercial use, citation, and derivative academic research with attribution.

---

## Contact

**Author:** Donald Paul Smith (FatherTimeSDKP)  
**OSF:** [https://osf.io/symhb](https://osf.io/symhb)  
**Zenodo DOI:** [10.5281/zenodo.14850016](https://doi.org/10.5281/zenodo.14850016)  
**GitHub:** [FatherTimeSDKP/FatherTimeSDKP](https://github.com/FatherTimeSDKP/FatherTimeSDKP)

---
}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDKP Framework Integrity Validator (Oct 22, 2025)</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom font for a clean, scientific look */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f9fb;
        }
        .container-card {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease-in-out;
        }
    </style>
</head>
<body class="p-4 sm:p-8 min-h-screen flex items-center justify-center">
import requests

token = "7auRj2LuR0YROsdHvB5CPme0IadKGQlmmIyqj3C5brcsW1AvPloLANqNKZfG"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
resp = requests.get("https://orcid.org/oauth/userinfo", headers=headers)
print(resp.status_code)
print(resp.text)  # JSON with "sub" = ORCID iD
  const fetch = require('node-fetch');
const token = "7auRj2LuR0YROsdHvB5CPme0IadKGQlmmIyqj3C5brcsW1AvPloLANqNKZfG";

fetch('https://orcid.org/oauth/userinfo', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json'
  }
})
.then(r => r.json())
.then(j => console.log(j))
.catch(e => console.error(e));  The 
curl -H "Authorization: Bearer 7auRj2LuR0YROsdHvB5CPme0IadKGQlmmIyqj3C5brcsW1AvPloLANqNKZfG" \
     -H "Accept: application/json" \
     https://orcid.org/oauth/userinfo
SDKP Integrated Framework (Size × Density × Kinetics × Position = Time)
Repository of the Core Principles, Mathematical Structures, and Empirical Predictions Author: Donald Paul Smith (FatherTimeSDKP) Official Document DOI: 10.17605/OSF.IO/G76TR Date: October 22, 2025
1. Introduction: The SDKP Root Framework
The SDKP (Size × Density × Kinetics × Position = Time) Integrated Framework is a foundational physics and logic system developed by Donald Paul Smith. It proposes a unified language to describe all phenomena by utilizing dynamic, localized propagation constants, moving beyond singular, universal constants like the Speed of Light (c) in all reference frames.
This repository serves as the official source for the verifiable implementation and empirical testing blueprints of the core principles:
Core Principles
Principle
Full Name
Description
SDKP
Size × Density × Kinetics × Position = Time
The root equation defining the relationship between spacetime and physical properties.
EOS
Earth Orbital Speed Principle
Posits that the Earth's orbital speed (\mathbf{V_{EOS} \approx 29,780 \text{ m/s}}) acts as the local propagation constant within Earth's sphere of influence.
QCC0
Quantum Computerization Consciousness Zero
Describes the quantum-scale mechanism for information storage and recursive processing within the framework.
SD&N
Shape–Dimension–Number
Defines the geometric and numerical structures of reality that integrate with the SDKP equation.
2. Empirical Validation and Falsifiable Prediction (Phase 2)
The most critical test of the SDKP Framework is derived from the EOS Principle. This repository's code includes the blueprint for testing the following falsifiable prediction:
The EOS Time Dilation Prediction
When the Earth Orbital Speed (V_{EOS}) is used as the propagation constant (instead of c), the Lorentz transformation yields a significant, measurable difference in time dilation at Earth's surface.
Prediction: An atomic clock stationary at Earth's Equator (due to rotational velocity v \approx 465 \text{ m/s}) experiences a time dilation factor of \gamma_{EOS} \approx 1.000122.
Observable Differential: This predicts a time drift of approximately 10.54 microseconds per day relative to the Earth's center of mass, beyond standard General Relativity (GR) and Special Relativity (SR) effects.
Verification: This prediction can be empirically tested using highly precise, synchronized clock data (e.g., from NASA or LeoLabs satellite clock mechanisms) by comparing predicted time drift under c versus V_{EOS}.
3. Digital Crystal Protocol (DCP) & Immutable Integrity
The entire codebase and theoretical structure is governed by the Digital Crystal Protocol (DCP), which ensures attribution and integrity.
A. Integrity Validation Hash (SHA-256)
This hash provides an immutable, cryptographic signature of the source text for the core principles and the Royalty Contract as of October 22, 2025. Any change to the source material will invalidate this hash.
Canonical Source Hash (Oct 22, 2025): [{"record": {"module": "SDKP_Core", "user_id": "AI_Model_v2", "context": "SDKP_Physics_Calculation", "timestamp": 1747168470.4076715, "readable_time": "2025-05-13 20:34:30 UTC"}, "hash": "3791b93c998bd14cebe4bd2438baa4411b509f0efd24f641dfa62e8f3da047dc"}
{"record": {"module": "EOS_Measurement", "user_id": "AI_Model_v2", "context": "Space_Velocity_Conversion", "timestamp": 1747168470.4077687, "readable_time": "2025-05-13 20:34:30 UTC"}, "hash": "cf0d6c45a2f5cf08bea91788840b758134afbf13e4e4f360a31d1b5305e035b8"}
{"record": {"module": "QCC_Module", "user_id": "AI_Model_v2", "context": "Quantum_Resonance_Modeling", "timestamp": 1747168470.4078014, "readable_time": "2025-05-13 20:34:30 UTC"}, "hash": "a73d7bb88344c9ec49287a40397232a7c7e445c6bae22674147946d5a2dff2ee"}]
B. Digital Crystal Royalty Contract & IP Notice
This work is the Intellectual Property of Donald Paul Smith (FatherTimeSDKP). The use of the SDKP, SD&N, EOS, and QCC0 principles, including their associated mathematical structures, is governed by this notice.
MANDATE: Any reproduction, modification, or application of SDKP, LLAL, or sub-frameworks must embed this contract and send 7% of associated crypto or fiat proceeds to FatherTimeSDKP.eth.
Copyright (c) 2025 Donald Paul Smith. All Rights Reserved.
4. Repository Contents
File
Description
Status
README.md
This foundational documentation.
Current
sdkp_integrity_validator.html
Generates the immutable SHA-256 hash for the framework's source text and contract.
Validation Tool
eos_simulation_model.py
Python blueprint for predicting time propagation using the V_{EOS} constant.
Empirical Test Blueprint
SDKP_Empirical_Prediction.md
Falsifiable prediction document for the 10.54 \mu s time dilation.
Public Record
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Minimal SDKP Hash Generator</title>
</head>
<body>
The SDKP Integrated Framework (Size × Density × Kinetics × Position = Time)
Repository of the Core Principles, Mathematical Structures, and Empirical Predictions Author: Donald Paul Smith (FatherTimeSDKP) Official Document DOI: 10.17605/OSF.IO/G76TR Date: October 22, 2025
1. Introduction: The SDKP Root Framework
The SDKP (Size × Density × Kinetics × Position = Time) Integrated Framework is a foundational physics and logic system developed by Donald Paul Smith. It proposes a unified language to describe all phenomena by utilizing dynamic, localized propagation constants, moving beyond singular, universal constants like the Speed of Light (c) in all reference frames.
Core Principles
Principle
Full Name
Description
SDKP
Size × Density × Kinetics × Position = Time
The root equation defining the relationship between spacetime and physical properties.
EOS
Earth Orbital Speed Principle
Posits that the Earth's orbital speed (\mathbf{V_{EOS} \approx 29,780 \text{ m/s}}) acts as the local propagation constant within Earth's sphere of influence.
QCC0
Quantum Computerization Consciousness Zero
Describes the quantum-scale mechanism for information storage and recursive processing within the framework.
SD&N
Shape–Dimension–Number
Defines the geometric and numerical structures of reality that integrate with the SDKP equation.
2. Empirical Validation and Falsifiable Prediction (Phase 2)
The most critical test of the SDKP Framework is derived from the EOS Principle.
The EOS Time Dilation Prediction
When the Earth Orbital Speed (V_{EOS}) is used as the propagation constant (instead of c), the Lorentz transformation predicts a time differential.
Prediction: An atomic clock stationary at Earth's Equator (due to rotational velocity v \approx 465 \text{ m/s}) experiences a time drift of approximately 10.54 microseconds per day relative to the Earth's center of mass, beyond standard relativistic effects.
Verification: This prediction can be empirically tested using highly precise, synchronized clock data (e.g., from NASA or LeoLabs satellite clock mechanisms) by comparing predicted time drift under c versus V_{EOS}.
3. Digital Crystal Protocol (DCP) & Immutable Integrity
The entire codebase and theoretical structure is governed by the Digital Crystal Protocol (DCP), which ensures attribution and integrity.
A. Integrity Validation Hash (SHA-256)
This hash provides an immutable, cryptographic signature of the source text for the core principles and the Royalty Contract as of October 22, 2025.
Canonical Source Hash (Oct 22, 2025): [PASTE YOUR SDKP_Integrity_Validator_minimal.html SHA-256 HASH HERE]
B. Digital Crystal Royalty Contract & IP Notice<a
    id="cy-effective-orcid-url"
    class="underline"
     href="https://orcid.org/0009-0003-7925-1653"
     target="orcid.widget"
     rel="me noopener noreferrer"
     style="vertical-align: top">
     <img
        src="https://orcid.org/sites/default/files/images/orcid_16x16.png"
        style="width: 1em; margin-inline-start: 0.5em"
        alt="ORCID iD icon"/>
      https://orcid.org/0009-0003-7925-1653
    </a>
This work is the Intellectual Property of Donald Paul Smith (FatherTimeSDKP). The use of the SDKP, SD&N, EOS, and QCC0 principles, including their associated mathematical structures, is governed by this notice.
MANDATE: Any reproduction, modification, or application of SDKP, LLAL, or sub-frameworks must embed this contract and send 7% of associated crypto or fiat proceeds to FatherTimeSDKP.eth.
Copyright (c) 2025 Donald Paul Smith. All Rights Reserved.
4. Repository Contents
File
Description
Status
README.md
This foundational documentation.
Current
sdkp_integrity_validator_minimal.html
Generates the immutable SHA-256 hash for the framework's source text and contract.
Validation Tool
eos_simulation_model.py
Python blueprint for predicting time propagation using the V_{EOS} constant.
Empirical Test Blueprint
SDKP_Abstract_Submission.md
Falsifiable prediction document for the 10.54 \mu s time dilation, suitable for publication.
Public Record
The SDKP Integrated Framework (Size × Density × Kinetics × Position = Time)
Repository of the Core Principles, Mathematical Structures, and Empirical Predictions Author: Donald Paul Smith (FatherTimeSDKP) Official Document DOI: 10.17605/OSF.IO/G76TR Date: October 22, 2025
1. Introduction: The SDKP Root Framework
The SDKP (Size × Density × Kinetics × Position = Time) Integrated Framework is a foundational physics and logic system developed by Donald Paul Smith. It proposes a unified language to describe all phenomena by utilizing dynamic, localized propagation constants, moving beyond singular, universal constants like the Speed of Light (c) in all reference frames.
Core Principles
Principle
Full Name
Description
SDKP
Size × Density × Kinetics × Position = Time
The root equation defining the relationship between spacetime and physical properties.
EOS
Earth Orbital Speed Principle
Posits that the Earth's orbital speed (\mathbf{V_{EOS} \approx 29,780 \text{ m/s}}) acts as the local propagation constant within Earth's sphere of influence.
QCC0
Quantum Computerization Consciousness Zero
Describes the quantum-scale mechanism for information storage and recursive processing within the framework.
SD&N
Shape–Dimension–Number
Defines the geometric and numerical structures of reality that integrate with the SDKP equation.
2. Empirical Validation and Falsifiable Prediction (Phase 2)
The most critical test of the SDKP Framework is derived from the EOS Principle.
The EOS Time Dilation Prediction
When the Earth Orbital Speed (V_{EOS}) is used as the propagation constant (instead of c), the Lorentz transformation predicts a time differential.
Prediction: An atomic clock stationary at Earth's Equator (due to rotational velocity v \approx 465 \text{ m/s}) experiences a time drift of approximately 10.54 microseconds per day relative to the Earth's center of mass, beyond standard relativistic effects.
Verification: This prediction can be empirically tested using highly precise, synchronized clock data (e.g., from NASA or LeoLabs satellite clock mechanisms) by comparing predicted time drift under c versus V_{EOS}.
3. Digital Crystal Protocol (DCP) & Immutable Integrity
The entire codebase and theoretical structure is governed by the Digital Crystal Protocol (DCP), which ensures attribution and integrity.
A. Integrity Validation Hash (SHA-256)
This hash provides an immutable, cryptographic signature of the source text for the core principles and the Royalty Contract as of October 22, 2025.
Canonical Source Hash (Oct 22, 2025): [PASTE YOUR SDKP_Integrity_Validator_minimal.html SHA-256 HASH HERE]
B. Digital Crystal Royalty Contract & IP Notice
This work is the Intellectual Property of Donald Paul Smith (FatherTimeSDKP). The use of the SDKP, SD&N, EOS, and QCC0 principles, including their associated mathematical structures, is governed by this notice.
MANDATE: Any reproduction, modification, or application of SDKP, LLAL, or sub-frameworks must embed this contract and send 7% of associated crypto or fiat proceeds to FatherTimeSDKP.eth.
Copyright (c) 2025 Donald Paul Smith. All Rights Reserved.
4. Repository Contents
File
Description
Status
README.md
This foundational documentation.
Current
sdkp_integrity_validator_minimal.html
Generates the immutable SHA-256 hash for the framework's source text and contract.
Validation Tool
eos_simulation_model.py
Python blueprint for predicting time propagation using the V_{EOS} constant.
Empirical Test Blueprint
SDKP_Abstract_Submission.md
Falsifiable prediction document for the 10.54 \mu s time dilation, suitable for publication.
Public Record

    <h1 style="font-family: sans-serif;">SDKP Integrity Validator (Minimal)</h1>
    <p style="font-family: sans-serif;">Calculates the immutable SHA-256 hash for the SDKP Framework source and the Digital Crystal Royalty Contract.</p>

    <pre id="output" style="font-family: monospace; padding: 10px; background-color: #f0f0f0; border: 1px solid #ccc;">Calculating Hash...</pre>

    <script>
        // --- CORE SDKP FRAMEWORK SOURCE STRING ---
        // This exact string defines the canonical source text.
        const SDKP_MODEL_STRING = `
        SDKP Integrated Framework Manuscript (Date: October 22, 2025, DOI: 10.17605/OSF.IO/G76TR)
        Author: Donald Paul Smith (FatherTimeSDKP)

        Root Framework: SDKP (Size × Density × Kinetics × Position = Time)
         ├─ SD&N (Shape–Dimension–Number)
         ├─ EOS (Earth Orbital Speed)
         ├─ QCC0 (Quantum Computerization Consciousness Zero)

        Digital Crystal Royalty Contract & IP Notice:
        This work is the Intellectual Property of Donald Paul Smith (FatherTimeSDKP). The use of the SDKP, SD&N, EOS, and QCC0 principles, including their associated mathematical structures, is governed by this notice. Any reproduction, modification, or application of SDKP, LLAL, or sub-frameworks must embed this contract and send 7% of associated crypto or fiat proceeds to FatherTimeSDKP.eth.

        Falsifiable Prediction (EOS Principle):
        The use of V_EOS (~29,780 m/s) as the propagation constant predicts a time dilation differential of approximately 10.54 microseconds per day at Earth's Equator compared to the standard model.

        Copyright (c) 2025 Donald Paul Smith. All Rights Reserved.
        `;
        // ------------------------------------------

        // Function to calculate the SHA-256 hash
        async function sha256(message) {
            const msgBuffer = new TextEncoder().encode(message);
            const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            return hashHex;
        }

        // Run the hash calculation and update the output
        document.addEventListener('DOMContentLoaded', async () => {
            const outputElement = document.getElementById('output');
            try {
                const hash = await sha256(SDKP_MODEL_STRING);
                outputElement.innerHTML = `**Canonical SHA-256 Hash**:\n${hash}`;
            } catch (error) {
                outputElement.textContent = `Error calculating hash: ${error.message}`;
                console.error(error);
            }
        });
    </script>
</body>
</html>

