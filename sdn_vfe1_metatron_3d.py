"""
FatherTimeSDKP - Module: 3D Visualization & VFE1 Engine
Demonstrates SD&N (Shape, Dimension, Number) spherical packing
and Vibrational Field Equations (VFE1) in 3D Python.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SDNMetatronVFE1Simulator:
    def __init__(self):
        # Shape (S): Spherical baseline radius
        self.r_sphere = 1.0
        
        # Number (N): Generate 13 Nodal Center Coordinates (Metatron 3D Array)
        self.nodes = self._generate_13_nodes()
        self.num_nodes = len(self.nodes)  # 13
        
        # Dimension (D): 3D Spatial Grid
        self.dim = 3

    def _generate_13_nodes(self) -> np.ndarray:
        """Generates 13 nodes: 1 center + 12 outer vertices (Cuboctahedron / FCC packing)."""
        center = [0.0, 0.0, 0.0]
        # 12 symmetric outer boundary nodes at distance 2 * r_sphere
        d = 2.0 * self.r_sphere
        outer_12 = [
            [ d,  d,  0], [ d, -d,  0], [-d,  d,  0], [-d, -d,  0],
            [ d,  0,  d], [ d,  0, -d], [-d,  0,  d], [-d,  0, -d],
            [ 0,  d,  d], [ 0,  d, -d], [ 0, -d,  d], [ 0, -d, -d]
        ]
        # Normalize outer node distances to uniform radial shell
        outer_12 = np.array(outer_12) / np.sqrt(2)
        return np.vstack([center, outer_12])

    def compute_vfe1_field(self, t: float, spatial_point: np.ndarray) -> float:
        """
        Vibrational Field Equation 1 (VFE1):
        Calculates local field density perturbation by superimposing wave contributions.
        Returns a normalized scalar multiplier for the local node radius.
        """
        vfe1_val = 0.0
        frequency_omega = 432.0  # Base harmonic frequency [Hz]
        
        for i, node in enumerate(self.nodes):
            dist = np.linalg.norm(spatial_point - node)
            # Digital root phase offset derived from node index
            phase = (i + 1) % 9
            # Phase-locked wave propagation with inverse distance attenuation
            vfe1_val += (1.0 / (dist + 0.1)) * np.cos(frequency_omega * t - dist + phase)
            
        # Normalize and dampen the output to prevent visual geometry inversion
        return 1.0 + (0.05 * vfe1_val)

    def visualize_3d_system(self, time_t: float = 0.0):
        """Renders 13 Spheres, 78 Vector Paths, and VFE1 Field Displacements."""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Dark background highlights the wave interference better
        ax.set_facecolor('#111111')
        fig.patch.set_facecolor('#111111')

        # 1. Plot 78 Inter-nodal Channels (Number N)
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                p1, p2 = self.nodes[i], self.nodes[j]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                        color='#00ffff', alpha=0.15, linewidth=0.8)

        # 2. Plot 13 Nodal Spheres (Shape S) with ACTIVE VFE1 Time Displacement
        for idx, node in enumerate(self.nodes):
            # Compute VFE1 displacement scalar
            dynamic_scale = self.compute_vfe1_field(t=time_t, spatial_point=node)
            effective_radius = self.r_sphere * dynamic_scale
            
            # Draw sphere wireframe using the VFE1 modulated radius
            u = np.linspace(0, 2 * np.pi, 15)
            v = np.linspace(0, np.pi, 15)
            x = node[0] + effective_radius * np.outer(np.cos(u), np.sin(v))
            y = node[1] + effective_radius * np.outer(np.sin(u), np.sin(v))
            z = node[2] + effective_radius * np.outer(np.ones(np.size(u)), np.cos(v))

            color = '#ffd700' if idx == 0 else '#ff00ff'
            ax.plot_wireframe(x, y, z, color=color, alpha=0.3, linewidth=0.5)
            ax.scatter(node[0], node[1], node[2], color=color, s=50)

        # Axis styling
        ax.set_title(f"SD&N Metatron Topology & VFE1 Active Field (t={time_t:.2f}s)\n"
                     f"13 Nodes | 78 Vector Channels | Dim: {self.dim}", 
                     fontsize=12, color='white')
                     
        ax.set_xlabel("X (Spatial Scale)", color='white')
        ax.set_ylabel("Y (Spatial Scale)", color='white')
        ax.set_zlabel("Z (Spatial Scale)", color='white')
        ax.tick_params(colors='white')
        
        # Unify aspect ratio to prevent sphere distortion
        ax.set_box_aspect([1,1,1])
        
        plt.tight_layout()
        plt.show()


# --- Execution Run ---
if __name__ == "__main__":
    sim = SDNMetatronVFE1Simulator()
    print("=== EXECUTING 3D SD&N / VFE1 PYTHON SIMULATOR ===")
    print(f"Nodes Loaded (Shape S)        : {sim.num_nodes}")
    print(f"Vector Channels Rendered (N)  : {sim.num_nodes * (sim.num_nodes - 1) // 2}")
    
    # Render static snapshot at an advanced time phase
    sim.visualize_3d_system(time_t=1.44)
