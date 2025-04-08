Developed a Python-based tool for analyzing Linear Time-Invariant (LTI) resistive electrical networks by computing the equivalent resistance between two arbitrary nodes using nodal analysis.
•	Implemented a robust function that takes:
•	a node list (N×1 vector),
•	an edge list (M×3 matrix defining resistors between nodes), and
•	a port (2×1 vector specifying input/output nodes).
•	Calculated resistance by simulating a test voltage source and solving the resulting linear system of equations.
•	Extended functionality to support linear dependent sources such as VCCS (Voltage-Controlled Current Sources) by integrating Modified Nodal Analysis (MNA).
•	Designed with modularity and extensibility in mind to support future inclusion of VCVS, CCCS, and CCVS components.
•	Ensured numerical stability and correctness by handling singular matrices and edge cases.
