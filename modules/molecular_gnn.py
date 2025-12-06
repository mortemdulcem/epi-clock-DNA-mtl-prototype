"""
Molecular Graph Neural Network Module - EpiClock v4.0
Graph Neural Network for Molecular Property Prediction

Uses PyTorch and RDKit to:
1. Convert SMILES to molecular graphs
2. Learn molecular representations via message passing
3. Predict addiction potential, toxicity, metabolism

Author: Dr. Nurcan Denli Bayir (nrcdnl94)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import hashlib
from datetime import datetime
import json

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
    from rdkit.Chem import Draw
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

import networkx as nx


# Atom Features Configuration
ATOM_FEATURES = {
    'atomic_num': list(range(1, 119)),  # H to Og
    'degree': [0, 1, 2, 3, 4, 5, 6],
    'formal_charge': [-3, -2, -1, 0, 1, 2, 3],
    'hybridization': ['SP', 'SP2', 'SP3', 'SP3D', 'SP3D2'],
    'is_aromatic': [False, True],
    'num_hs': [0, 1, 2, 3, 4],
    'is_in_ring': [False, True],
}

BOND_FEATURES = {
    'bond_type': ['SINGLE', 'DOUBLE', 'TRIPLE', 'AROMATIC'],
    'is_conjugated': [False, True],
    'is_in_ring': [False, True],
    'stereo': ['STEREONONE', 'STEREOANY', 'STEREOZ', 'STEREOE'],
}


@dataclass
class MolecularGraph:
    """Molecular graph representation"""
    smiles: str
    node_features: torch.Tensor  # [num_atoms, feature_dim]
    edge_index: torch.Tensor     # [2, num_edges]
    edge_features: torch.Tensor  # [num_edges, edge_feature_dim]
    global_features: torch.Tensor  # [global_feature_dim]
    num_atoms: int
    num_bonds: int
    molecular_formula: str
    molecular_weight: float


@dataclass
class GNNPrediction:
    """GNN prediction result"""
    smiles: str
    addiction_potential: float
    addiction_ci: Tuple[float, float]
    toxicity_score: float
    toxicity_class: str
    metabolism_liability: float
    metabolic_sites: List[int]
    bbb_permeability: float
    herg_risk: float
    cyp_inhibition: Dict[str, float]
    uncertainty: float
    node_importance: List[float]
    hash_chain: str
    timestamp: str


class MoleculeFeaturizer:
    """Convert SMILES to molecular graph with features"""
    
    def __init__(self):
        self.atom_feature_dim = self._calculate_atom_feature_dim()
        self.bond_feature_dim = self._calculate_bond_feature_dim()
        self.global_feature_dim = 200  # RDKit descriptors
    
    def _calculate_atom_feature_dim(self) -> int:
        """Calculate total atom feature dimension"""
        dim = 0
        dim += len(ATOM_FEATURES['atomic_num'])  # One-hot atomic number
        dim += len(ATOM_FEATURES['degree'])      # One-hot degree
        dim += len(ATOM_FEATURES['formal_charge'])
        dim += len(ATOM_FEATURES['hybridization'])
        dim += len(ATOM_FEATURES['is_aromatic'])
        dim += len(ATOM_FEATURES['num_hs'])
        dim += len(ATOM_FEATURES['is_in_ring'])
        return dim
    
    def _calculate_bond_feature_dim(self) -> int:
        """Calculate total bond feature dimension"""
        dim = 0
        dim += len(BOND_FEATURES['bond_type'])
        dim += len(BOND_FEATURES['is_conjugated'])
        dim += len(BOND_FEATURES['is_in_ring'])
        dim += len(BOND_FEATURES['stereo'])
        return dim
    
    def _one_hot(self, value, choices: list) -> List[int]:
        """Create one-hot encoding"""
        encoding = [0] * len(choices)
        try:
            idx = choices.index(value)
            encoding[idx] = 1
        except ValueError:
            pass  # Unknown value
        return encoding
    
    def featurize_atom(self, atom) -> List[float]:
        """Extract features from an atom"""
        if not RDKIT_AVAILABLE:
            return [0.0] * self.atom_feature_dim
        
        features = []
        
        # Atomic number (one-hot)
        features.extend(self._one_hot(atom.GetAtomicNum(), ATOM_FEATURES['atomic_num']))
        
        # Degree (one-hot)
        features.extend(self._one_hot(atom.GetDegree(), ATOM_FEATURES['degree']))
        
        # Formal charge (one-hot)
        features.extend(self._one_hot(atom.GetFormalCharge(), ATOM_FEATURES['formal_charge']))
        
        # Hybridization (one-hot)
        hyb = str(atom.GetHybridization()).split('.')[-1]
        features.extend(self._one_hot(hyb, ATOM_FEATURES['hybridization']))
        
        # Is aromatic
        features.extend(self._one_hot(atom.GetIsAromatic(), ATOM_FEATURES['is_aromatic']))
        
        # Number of hydrogens
        features.extend(self._one_hot(atom.GetTotalNumHs(), ATOM_FEATURES['num_hs']))
        
        # Is in ring
        features.extend(self._one_hot(atom.IsInRing(), ATOM_FEATURES['is_in_ring']))
        
        return features
    
    def featurize_bond(self, bond) -> List[float]:
        """Extract features from a bond"""
        if not RDKIT_AVAILABLE:
            return [0.0] * self.bond_feature_dim
        
        features = []
        
        # Bond type
        bt = str(bond.GetBondType()).split('.')[-1]
        features.extend(self._one_hot(bt, BOND_FEATURES['bond_type']))
        
        # Is conjugated
        features.extend(self._one_hot(bond.GetIsConjugated(), BOND_FEATURES['is_conjugated']))
        
        # Is in ring
        features.extend(self._one_hot(bond.IsInRing(), BOND_FEATURES['is_in_ring']))
        
        # Stereo
        stereo = str(bond.GetStereo()).split('.')[-1]
        features.extend(self._one_hot(stereo, BOND_FEATURES['stereo']))
        
        return features
    
    def get_global_features(self, mol) -> List[float]:
        """Extract global molecular descriptors"""
        if not RDKIT_AVAILABLE:
            return [0.0] * self.global_feature_dim
        
        features = []
        
        try:
            # Physicochemical properties
            features.append(Descriptors.MolWt(mol))
            features.append(Descriptors.MolLogP(mol))
            features.append(Descriptors.TPSA(mol))
            features.append(Descriptors.NumHDonors(mol))
            features.append(Descriptors.NumHAcceptors(mol))
            features.append(Descriptors.NumRotatableBonds(mol))
            features.append(Descriptors.NumAromaticRings(mol))
            features.append(Descriptors.NumAliphaticRings(mol))
            features.append(Descriptors.FractionCSP3(mol))
            features.append(Descriptors.HeavyAtomCount(mol))
            
            # Electronic properties
            features.append(Descriptors.NumValenceElectrons(mol))
            features.append(Descriptors.MaxPartialCharge(mol) if Descriptors.MaxPartialCharge(mol) else 0)
            features.append(Descriptors.MinPartialCharge(mol) if Descriptors.MinPartialCharge(mol) else 0)
            
            # Ring descriptors
            features.append(Descriptors.RingCount(mol))
            features.append(rdMolDescriptors.CalcNumHeterocycles(mol))
            features.append(rdMolDescriptors.CalcNumSpiroAtoms(mol))
            features.append(rdMolDescriptors.CalcNumBridgeheadAtoms(mol))
            
            # Complexity
            features.append(Descriptors.BertzCT(mol))
            features.append(Descriptors.Ipc(mol) if Descriptors.Ipc(mol) else 0)
            
            # Pad to fixed size
            while len(features) < self.global_feature_dim:
                features.append(0.0)
            
            # Normalize
            features = features[:self.global_feature_dim]
            max_val = max(abs(f) for f in features) if features else 1.0
            if max_val > 0:
                features = [f / max_val for f in features]
            
        except Exception:
            features = [0.0] * self.global_feature_dim
        
        return features
    
    def smiles_to_graph(self, smiles: str) -> Optional[MolecularGraph]:
        """Convert SMILES string to molecular graph"""
        if not RDKIT_AVAILABLE:
            return self._generate_dummy_graph(smiles)
        
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return None
            
            # Add hydrogens for better representation
            mol = Chem.AddHs(mol)
            
            # Get atoms and bonds
            num_atoms = mol.GetNumAtoms()
            num_bonds = mol.GetNumBonds()
            
            # Node features
            node_features = []
            for atom in mol.GetAtoms():
                node_features.append(self.featurize_atom(atom))
            node_features = torch.tensor(node_features, dtype=torch.float32)
            
            # Edge index and features (bidirectional)
            edge_index = []
            edge_features = []
            for bond in mol.GetBonds():
                i = bond.GetBeginAtomIdx()
                j = bond.GetEndAtomIdx()
                
                # Add both directions
                edge_index.append([i, j])
                edge_index.append([j, i])
                
                bf = self.featurize_bond(bond)
                edge_features.append(bf)
                edge_features.append(bf)
            
            if edge_index:
                edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
                edge_features = torch.tensor(edge_features, dtype=torch.float32)
            else:
                edge_index = torch.zeros((2, 0), dtype=torch.long)
                edge_features = torch.zeros((0, self.bond_feature_dim), dtype=torch.float32)
            
            # Global features
            global_features = torch.tensor(self.get_global_features(mol), dtype=torch.float32)
            
            # Molecular info
            mol_formula = rdMolDescriptors.CalcMolFormula(mol)
            mol_weight = Descriptors.MolWt(mol)
            
            return MolecularGraph(
                smiles=smiles,
                node_features=node_features,
                edge_index=edge_index,
                edge_features=edge_features,
                global_features=global_features,
                num_atoms=num_atoms,
                num_bonds=num_bonds,
                molecular_formula=mol_formula,
                molecular_weight=mol_weight
            )
            
        except Exception as e:
            print(f"Error processing SMILES {smiles}: {e}")
            return None
    
    def _generate_dummy_graph(self, smiles: str) -> MolecularGraph:
        """Generate dummy graph when RDKit not available"""
        num_atoms = len(smiles) // 2  # Rough estimate
        num_bonds = num_atoms - 1
        
        node_features = torch.randn(num_atoms, self.atom_feature_dim)
        edge_index = torch.randint(0, num_atoms, (2, num_bonds * 2))
        edge_features = torch.randn(num_bonds * 2, self.bond_feature_dim)
        global_features = torch.randn(self.global_feature_dim)
        
        return MolecularGraph(
            smiles=smiles,
            node_features=node_features,
            edge_index=edge_index,
            edge_features=edge_features,
            global_features=global_features,
            num_atoms=num_atoms,
            num_bonds=num_bonds,
            molecular_formula="C?H?N?O?",
            molecular_weight=300.0
        )


class MessagePassingLayer(nn.Module):
    """Message Passing Neural Network Layer"""
    
    def __init__(self, node_dim: int, edge_dim: int, hidden_dim: int):
        super().__init__()
        
        # Message function
        self.message_mlp = nn.Sequential(
            nn.Linear(2 * node_dim + edge_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Update function (GRU-style)
        self.update_gru = nn.GRUCell(hidden_dim, node_dim)
        
        # Attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(2 * node_dim + edge_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, node_features: torch.Tensor, edge_index: torch.Tensor, 
                edge_features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with attention-weighted message passing
        
        Args:
            node_features: [num_nodes, node_dim]
            edge_index: [2, num_edges]
            edge_features: [num_edges, edge_dim]
        
        Returns:
            Updated node features: [num_nodes, node_dim]
        """
        num_nodes = node_features.size(0)
        num_edges = edge_index.size(1)
        
        if num_edges == 0:
            return node_features
        
        # Get source and target nodes
        src_idx = edge_index[0]
        dst_idx = edge_index[1]
        
        src_features = node_features[src_idx]  # [num_edges, node_dim]
        dst_features = node_features[dst_idx]  # [num_edges, node_dim]
        
        # Concatenate for message computation
        edge_input = torch.cat([src_features, dst_features, edge_features], dim=1)
        
        # Compute messages
        messages = self.message_mlp(edge_input)  # [num_edges, hidden_dim]
        
        # Compute attention weights
        attention_scores = self.attention(edge_input)  # [num_edges, 1]
        attention_scores = F.leaky_relu(attention_scores, 0.2)
        
        # Aggregate messages per node with attention
        aggregated = torch.zeros(num_nodes, messages.size(1), device=node_features.device)
        attention_sum = torch.zeros(num_nodes, 1, device=node_features.device)
        
        for i in range(num_edges):
            dst = dst_idx[i]
            aggregated[dst] += attention_scores[i] * messages[i]
            attention_sum[dst] += attention_scores[i]
        
        # Normalize
        attention_sum = attention_sum.clamp(min=1e-6)
        aggregated = aggregated / attention_sum
        
        # Update node features
        updated = self.update_gru(aggregated, node_features)
        
        return updated


class GraphAttentionPooling(nn.Module):
    """Attention-based graph pooling"""
    
    def __init__(self, node_dim: int, hidden_dim: int):
        super().__init__()
        
        self.attention = nn.Sequential(
            nn.Linear(node_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, node_features: torch.Tensor) -> torch.Tensor:
        """
        Pool node features to graph-level representation
        
        Args:
            node_features: [num_nodes, node_dim]
        
        Returns:
            Graph embedding: [node_dim]
        """
        attention_weights = self.attention(node_features)  # [num_nodes, 1]
        attention_weights = F.softmax(attention_weights, dim=0)
        
        graph_embedding = (attention_weights * node_features).sum(dim=0)
        
        return graph_embedding


class MolecularGNN(nn.Module):
    """
    Graph Neural Network for Molecular Property Prediction
    
    Architecture:
    - Input embedding layers
    - Multiple message passing layers with attention
    - Attention-based graph pooling
    - Multi-task prediction heads
    """
    
    def __init__(
        self,
        atom_feature_dim: int = 158,
        bond_feature_dim: int = 11,
        global_feature_dim: int = 200,
        hidden_dim: int = 256,
        num_layers: int = 4,
        dropout: float = 0.2
    ):
        super().__init__()
        
        self.atom_feature_dim = atom_feature_dim
        self.hidden_dim = hidden_dim
        
        # Input embeddings
        self.node_embedding = nn.Sequential(
            nn.Linear(atom_feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.edge_embedding = nn.Sequential(
            nn.Linear(bond_feature_dim, hidden_dim // 2),
            nn.ReLU()
        )
        
        self.global_embedding = nn.Sequential(
            nn.Linear(global_feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Message passing layers
        self.mp_layers = nn.ModuleList([
            MessagePassingLayer(hidden_dim, hidden_dim // 2, hidden_dim)
            for _ in range(num_layers)
        ])
        
        # Layer normalization
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(hidden_dim)
            for _ in range(num_layers)
        ])
        
        # Graph pooling
        self.pooling = GraphAttentionPooling(hidden_dim, hidden_dim)
        
        # Combine graph and global features
        self.combine = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Multi-task prediction heads
        
        # Addiction potential (regression, 0-1)
        self.addiction_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 2)  # mean and log_var for uncertainty
        )
        
        # Toxicity (multi-class)
        self.toxicity_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 4)  # Low, Medium, High, Severe
        )
        
        # Metabolism liability (regression)
        self.metabolism_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        # BBB permeability (regression)
        self.bbb_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        # hERG risk (regression)
        self.herg_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        # CYP inhibition (multi-output regression)
        self.cyp_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 5)  # CYP1A2, 2C9, 2C19, 2D6, 3A4
        )
        
        # Node importance for interpretability
        self.node_importance = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 4),
            nn.ReLU(),
            nn.Linear(hidden_dim // 4, 1),
            nn.Sigmoid()
        )
    
    def forward(self, graph: MolecularGraph) -> Dict[str, torch.Tensor]:
        """
        Forward pass
        
        Args:
            graph: MolecularGraph object
        
        Returns:
            Dictionary of predictions
        """
        # Embed inputs
        node_h = self.node_embedding(graph.node_features)
        edge_h = self.edge_embedding(graph.edge_features) if graph.edge_features.size(0) > 0 else None
        global_h = self.global_embedding(graph.global_features)
        
        # Message passing with residual connections
        for i, (mp_layer, ln) in enumerate(zip(self.mp_layers, self.layer_norms)):
            if edge_h is not None:
                node_h_new = mp_layer(node_h, graph.edge_index, edge_h)
            else:
                node_h_new = node_h
            node_h = ln(node_h + node_h_new)  # Residual connection
        
        # Graph pooling
        graph_h = self.pooling(node_h)
        
        # Combine with global features
        combined = self.combine(torch.cat([graph_h, global_h], dim=0))
        
        # Multi-task predictions
        addiction_out = self.addiction_head(combined)
        addiction_mean = torch.sigmoid(addiction_out[0])
        addiction_var = F.softplus(addiction_out[1])
        
        toxicity_logits = self.toxicity_head(combined)
        toxicity_probs = F.softmax(toxicity_logits, dim=0)
        
        metabolism = torch.sigmoid(self.metabolism_head(combined))
        bbb = torch.sigmoid(self.bbb_head(combined))
        herg = torch.sigmoid(self.herg_head(combined))
        cyp = torch.sigmoid(self.cyp_head(combined))
        
        # Node importance scores
        importance = self.node_importance(node_h).squeeze(-1)
        
        return {
            'addiction_mean': addiction_mean,
            'addiction_var': addiction_var,
            'toxicity_logits': toxicity_logits,
            'toxicity_probs': toxicity_probs,
            'metabolism': metabolism,
            'bbb': bbb,
            'herg': herg,
            'cyp': cyp,
            'node_importance': importance,
            'graph_embedding': combined
        }


class MolecularGNNPredictor:
    """
    High-level interface for molecular property prediction
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.featurizer = MoleculeFeaturizer()
        self.model = MolecularGNN(
            atom_feature_dim=self.featurizer.atom_feature_dim,
            bond_feature_dim=self.featurizer.bond_feature_dim,
            global_feature_dim=self.featurizer.global_feature_dim
        )
        
        if model_path and torch.cuda.is_available():
            self.model.load_state_dict(torch.load(model_path))
        
        self.model.eval()
        
        self.toxicity_classes = ['Dusuk', 'Orta', 'Yuksek', 'Siddetli']
        self.cyp_enzymes = ['CYP1A2', 'CYP2C9', 'CYP2C19', 'CYP2D6', 'CYP3A4']
    
    def predict(self, smiles: str) -> Optional[GNNPrediction]:
        """
        Predict molecular properties from SMILES
        
        Args:
            smiles: SMILES string
        
        Returns:
            GNNPrediction object or None if invalid
        """
        # Convert to graph
        graph = self.featurizer.smiles_to_graph(smiles)
        if graph is None:
            return None
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(graph)
        
        # Extract predictions
        addiction_mean = outputs['addiction_mean'].item()
        addiction_std = np.sqrt(outputs['addiction_var'].item())
        
        toxicity_class_idx = outputs['toxicity_probs'].argmax().item()
        toxicity_score = outputs['toxicity_probs'].max().item()
        
        metabolism = outputs['metabolism'].item()
        bbb = outputs['bbb'].item()
        herg = outputs['herg'].item()
        
        cyp_values = outputs['cyp'].numpy()
        cyp_inhibition = {
            enzyme: float(val) 
            for enzyme, val in zip(self.cyp_enzymes, cyp_values)
        }
        
        node_importance = outputs['node_importance'].numpy().tolist()
        
        # Identify metabolic sites (high importance nodes)
        metabolic_sites = [
            i for i, imp in enumerate(node_importance) 
            if imp > 0.7
        ]
        
        # Calculate uncertainty
        uncertainty = addiction_std + (1 - toxicity_score)
        
        # Generate hash
        hash_input = f"{smiles}_{datetime.now().isoformat()}"
        hash_chain = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        return GNNPrediction(
            smiles=smiles,
            addiction_potential=addiction_mean,
            addiction_ci=(
                max(0, addiction_mean - 1.96 * addiction_std),
                min(1, addiction_mean + 1.96 * addiction_std)
            ),
            toxicity_score=toxicity_score,
            toxicity_class=self.toxicity_classes[toxicity_class_idx],
            metabolism_liability=metabolism,
            metabolic_sites=metabolic_sites,
            bbb_permeability=bbb,
            herg_risk=herg,
            cyp_inhibition=cyp_inhibition,
            uncertainty=uncertainty,
            node_importance=node_importance,
            hash_chain=hash_chain,
            timestamp=datetime.now().isoformat()
        )
    
    def predict_batch(self, smiles_list: List[str]) -> List[GNNPrediction]:
        """Predict properties for multiple molecules"""
        results = []
        for smiles in smiles_list:
            pred = self.predict(smiles)
            if pred:
                results.append(pred)
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model architecture information"""
        return {
            'model_type': 'MPNN with Attention',
            'num_layers': 4,
            'hidden_dim': 256,
            'atom_feature_dim': self.featurizer.atom_feature_dim,
            'bond_feature_dim': self.featurizer.bond_feature_dim,
            'global_feature_dim': self.featurizer.global_feature_dim,
            'num_parameters': sum(p.numel() for p in self.model.parameters()),
            'prediction_heads': [
                'Bagimlilik Potansiyeli',
                'Toksisite Sinifi',
                'Metabolizma Yukunlulugu',
                'BBB Gecirgenlik',
                'hERG Riski',
                'CYP Inhibisyonu'
            ]
        }


# Pre-trained model weights (simulated for prototype)
PRETRAINED_WEIGHTS = {
    'addiction_bias': {
        'opioid_core': 0.85,
        'stimulant_core': 0.75,
        'depressant_core': 0.70,
        'cannabinoid_core': 0.45,
        'hallucinogen_core': 0.35,
        'default': 0.30
    },
    'toxicity_patterns': {
        'nitro_group': 'Yuksek',
        'halogen_heavy': 'Orta',
        'aromatic_fused': 'Orta',
        'default': 'Dusuk'
    }
}


# Singleton instance
_gnn_predictor = None

def get_gnn_predictor() -> MolecularGNNPredictor:
    """Get singleton GNN predictor instance"""
    global _gnn_predictor
    if _gnn_predictor is None:
        _gnn_predictor = MolecularGNNPredictor()
    return _gnn_predictor


# Reference substances for validation
REFERENCE_SUBSTANCES = {
    'morphine': {
        'smiles': 'CN1CC[C@]23c4c5ccc(O)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5',
        'expected_addiction': 0.92,
        'expected_toxicity': 'Yuksek'
    },
    'cocaine': {
        'smiles': 'COC(=O)[C@H]1[C@@H]2CC[C@H](C2)[N@@H]1C',
        'expected_addiction': 0.88,
        'expected_toxicity': 'Yuksek'
    },
    'caffeine': {
        'smiles': 'Cn1cnc2c1c(=O)n(c(=O)n2C)C',
        'expected_addiction': 0.25,
        'expected_toxicity': 'Dusuk'
    },
    'aspirin': {
        'smiles': 'CC(=O)Oc1ccccc1C(=O)O',
        'expected_addiction': 0.05,
        'expected_toxicity': 'Dusuk'
    },
    'fentanyl': {
        'smiles': 'CCC(=O)N(c1ccccc1)C2CCN(CC2)CCc3ccccc3',
        'expected_addiction': 0.98,
        'expected_toxicity': 'Siddetli'
    },
    'methamphetamine': {
        'smiles': 'CC(Cc1ccccc1)NC',
        'expected_addiction': 0.90,
        'expected_toxicity': 'Yuksek'
    },
    'diazepam': {
        'smiles': 'CN1C(=O)CN=C(c2ccccc2)c3cc(Cl)ccc13',
        'expected_addiction': 0.65,
        'expected_toxicity': 'Orta'
    },
    'thc': {
        'smiles': 'CCCCCc1cc(O)c2C3CC(C)=CC[C@H]3C(C)(C)Oc2c1',
        'expected_addiction': 0.45,
        'expected_toxicity': 'Dusuk'
    }
}


def validate_model() -> Dict[str, Any]:
    """Validate model against reference substances"""
    predictor = get_gnn_predictor()
    results = []
    
    for name, data in REFERENCE_SUBSTANCES.items():
        pred = predictor.predict(data['smiles'])
        if pred:
            addiction_error = abs(pred.addiction_potential - data['expected_addiction'])
            toxicity_match = pred.toxicity_class == data['expected_toxicity']
            
            results.append({
                'substance': name,
                'predicted_addiction': pred.addiction_potential,
                'expected_addiction': data['expected_addiction'],
                'addiction_error': addiction_error,
                'predicted_toxicity': pred.toxicity_class,
                'expected_toxicity': data['expected_toxicity'],
                'toxicity_match': toxicity_match
            })
    
    return {
        'results': results,
        'mean_addiction_error': np.mean([r['addiction_error'] for r in results]),
        'toxicity_accuracy': np.mean([r['toxicity_match'] for r in results])
    }
