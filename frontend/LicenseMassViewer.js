import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';

export default function LicenseMassViewer({ contractAddress, tokenId, provider }) {
    const [mass, setMass] = useState('0');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchMass() {
            try {
                const abi = [
                    "function getCalculatedMass(uint256 id) external view returns (uint256)"
                ];
                const contract = new ethers.Contract(contractAddress, abi, provider);
                const calculatedMass = await contract.getCalculatedMass(tokenId);
                setMass(ethers.formatUnits(calculatedMass, 18));
            } catch (err) {
                console.error("Error fetching calculated mass:", err);
            } finally {
                setLoading(false);
            }
        }
        if (contractAddress && tokenId && provider) {
            fetchMass();
        }
    }, [contractAddress, tokenId, provider]);

    return (
        <div style={{ padding: '16px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>SDKP License Mass Viewer</h3>
            {loading ? (
                <p>Calculating real-time mass...</p>
            ) : (
                <p style={{ fontSize: '1.25rem', fontFamily: 'monospace' }}>Calculated Mass: {mass} units</p>
            )}
        </div>
    );
}
