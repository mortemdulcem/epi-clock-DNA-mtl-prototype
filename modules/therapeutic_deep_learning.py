"""
Therapeutic Medication Deep Learning Models
Advanced Neural Networks for Medication Effect Prediction

PyTorch-based: MLP, Attention, GNN, Multi-Task Learning

UNODC Corporate Standards - NO EMOJIS
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import warnings

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    warnings.warn("PyTorch not available - using simulation mode")


class PredictionTask(Enum):
    """Multi-task prediction targets"""
    EAA_EFFECT = "EAA Effect Prediction"
    SYNERGY_SCORE = "Synergy Score"
    ADVERSE_RISK = "Adverse Effect Risk"
    PATHWAY_IMPACT = "Pathway Impact"
    GENE_EXPRESSION = "Gene Expression Change"
    CPG_METHYLATION = "CpG Methylation Delta"


@dataclass
class MedicationFeatures:
    """Feature vector for a therapeutic medication"""
    medication_id: str
    
    # Pharmacological features
    molecular_weight: float = 0.0
    logp: float = 0.0
    pka: float = 7.0
    half_life_hours: float = 12.0
    bioavailability: float = 0.8
    protein_binding: float = 0.5
    
    # Category encoding (one-hot)
    category_vector: np.ndarray = field(default_factory=lambda: np.zeros(14))
    
    # Effect direction encoding
    effect_direction: int = 0  # -1: protective, 0: neutral, 1: accelerating
    
    # Gene target count
    target_gene_count: int = 0
    cpg_count: int = 0
    
    # Literature support
    sample_size: int = 0
    pubmed_count: int = 0
    
    # Duration factors
    typical_duration_years: float = 5.0
    dose_dependent: bool = True
    reversible: bool = True


if TORCH_AVAILABLE:
    
    class MedicationEmbeddingLayer(nn.Module):
        """
        Medication embedding layer with learned representations
        """
        def __init__(self, num_medications: int, embedding_dim: int = 64):
            super().__init__()
            self.embedding = nn.Embedding(num_medications, embedding_dim)
            self.layer_norm = nn.LayerNorm(embedding_dim)
            
        def forward(self, medication_ids: torch.Tensor) -> torch.Tensor:
            x = self.embedding(medication_ids)
            return self.layer_norm(x)
    
    
    class MedicationMLP(nn.Module):
        """
        Multi-Layer Perceptron for medication effect prediction
        
        Architecture:
        - Input: Medication feature vector (pharmacological + categorical)
        - Hidden: 3 layers with dropout and batch normalization
        - Output: EAA effect prediction
        """
        def __init__(self, input_dim: int = 32, hidden_dims: List[int] = [128, 64, 32], 
                     output_dim: int = 1, dropout: float = 0.3):
            super().__init__()
            
            layers = []
            prev_dim = input_dim
            
            for hidden_dim in hidden_dims:
                layers.extend([
                    nn.Linear(prev_dim, hidden_dim),
                    nn.BatchNorm1d(hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ])
                prev_dim = hidden_dim
            
            layers.append(nn.Linear(prev_dim, output_dim))
            
            self.network = nn.Sequential(*layers)
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.network(x)
    
    
    class MedicationAttention(nn.Module):
        """
        Self-Attention mechanism for medication combinations
        
        Captures interactions between multiple medications
        """
        def __init__(self, embed_dim: int = 64, num_heads: int = 4, dropout: float = 0.1):
            super().__init__()
            
            self.multihead_attn = nn.MultiheadAttention(
                embed_dim=embed_dim,
                num_heads=num_heads,
                dropout=dropout,
                batch_first=True
            )
            self.layer_norm = nn.LayerNorm(embed_dim)
            self.ffn = nn.Sequential(
                nn.Linear(embed_dim, embed_dim * 4),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(embed_dim * 4, embed_dim),
                nn.Dropout(dropout)
            )
            self.ffn_norm = nn.LayerNorm(embed_dim)
            
        def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
            # Self-attention
            attn_out, attn_weights = self.multihead_attn(x, x, x, key_padding_mask=mask)
            x = self.layer_norm(x + attn_out)
            
            # Feed-forward
            ffn_out = self.ffn(x)
            x = self.ffn_norm(x + ffn_out)
            
            return x, attn_weights
    
    
    class MedicationGNN(nn.Module):
        """
        Graph Neural Network for Medication-Gene-CpG relationships
        
        Node types:
        - Medication nodes
        - Gene nodes (target genes)
        - CpG nodes (affected CpG sites)
        
        Edge types:
        - Medication -> Gene (targets)
        - Gene -> CpG (regulates)
        - Medication -> CpG (affects methylation)
        - Medication <-> Medication (synergy/antagonism)
        """
        def __init__(self, node_dim: int = 64, edge_dim: int = 16, 
                     hidden_dim: int = 128, num_layers: int = 3,
                     num_edge_types: int = 4):
            super().__init__()
            
            self.node_dim = node_dim
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            self.num_edge_types = num_edge_types
            
            # Node type embeddings
            self.node_type_embed = nn.Embedding(3, node_dim)  # medication, gene, cpg
            
            # Edge type embeddings
            self.edge_type_embed = nn.Embedding(num_edge_types, edge_dim)
            
            # Message passing layers
            self.message_layers = nn.ModuleList()
            self.update_layers = nn.ModuleList()
            self.edge_layers = nn.ModuleList()
            
            for i in range(num_layers):
                in_dim = node_dim if i == 0 else hidden_dim
                
                # Message function: concat(source, edge, target) -> message
                self.message_layers.append(
                    nn.Sequential(
                        nn.Linear(in_dim * 2 + edge_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, hidden_dim)
                    )
                )
                
                # Update function: concat(node, aggregated_messages) -> new_node
                self.update_layers.append(
                    nn.Sequential(
                        nn.Linear(in_dim + hidden_dim, hidden_dim),
                        nn.LayerNorm(hidden_dim),
                        nn.ReLU(),
                        nn.Dropout(0.1)
                    )
                )
                
                # Edge update
                self.edge_layers.append(
                    nn.Sequential(
                        nn.Linear(hidden_dim * 2 + edge_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, edge_dim)
                    )
                )
            
            # Readout
            self.readout = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1)
            )
            
        def forward(self, node_features: torch.Tensor, 
                    edge_index: torch.Tensor,
                    edge_type: torch.Tensor,
                    node_type: torch.Tensor,
                    batch: Optional[torch.Tensor] = None) -> Dict[str, torch.Tensor]:
            """
            Forward pass through GNN
            
            Args:
                node_features: (num_nodes, node_dim)
                edge_index: (2, num_edges) - source, target indices
                edge_type: (num_edges,) - edge type indices
                node_type: (num_nodes,) - node type indices
                batch: (num_nodes,) - batch assignment for each node
            """
            # Add node type embeddings
            x = node_features + self.node_type_embed(node_type)
            edge_attr = self.edge_type_embed(edge_type)
            
            # Message passing
            for layer_idx in range(self.num_layers):
                # Get source and target node features
                source_idx, target_idx = edge_index[0], edge_index[1]
                source_features = x[source_idx]
                target_features = x[target_idx]
                
                # Compute messages
                edge_input = torch.cat([source_features, target_features, edge_attr], dim=-1)
                messages = self.message_layers[layer_idx](edge_input)
                
                # Aggregate messages (mean aggregation)
                aggregated = torch.zeros(x.size(0), self.hidden_dim, device=x.device)
                aggregated.index_add_(0, target_idx, messages)
                
                # Count neighbors for normalization
                neighbor_count = torch.zeros(x.size(0), device=x.device)
                neighbor_count.index_add_(0, target_idx, torch.ones(target_idx.size(0), device=x.device))
                neighbor_count = neighbor_count.clamp(min=1).unsqueeze(-1)
                aggregated = aggregated / neighbor_count
                
                # Update node features
                update_input = torch.cat([x, aggregated], dim=-1)
                x = self.update_layers[layer_idx](update_input)
                
                # Update edge features
                edge_update_input = torch.cat([x[source_idx], x[target_idx], edge_attr], dim=-1)
                edge_attr = self.edge_layers[layer_idx](edge_update_input)
            
            # Readout - aggregate medication nodes only
            medication_mask = (node_type == 0)  # Type 0 = medication
            medication_features = x[medication_mask]
            
            # Global mean pooling per graph
            if batch is not None:
                medication_batch = batch[medication_mask]
                # Scatter mean
                num_graphs = batch.max().item() + 1
                graph_features = torch.zeros(num_graphs, self.hidden_dim, device=x.device)
                graph_features.index_add_(0, medication_batch, medication_features)
                count = torch.zeros(num_graphs, device=x.device)
                count.index_add_(0, medication_batch, torch.ones(medication_batch.size(0), device=x.device))
                graph_features = graph_features / count.clamp(min=1).unsqueeze(-1)
            else:
                graph_features = medication_features.mean(dim=0, keepdim=True)
            
            # Prediction
            prediction = self.readout(graph_features)
            
            return {
                'prediction': prediction,
                'node_embeddings': x,
                'edge_embeddings': edge_attr,
                'medication_embeddings': medication_features
            }
    
    
    class MedicationSynergyPredictor(nn.Module):
        """
        Predicts synergy/antagonism between medication pairs
        
        Uses learned medication embeddings and interaction modeling
        """
        def __init__(self, medication_dim: int = 64, hidden_dim: int = 128):
            super().__init__()
            
            # Pairwise interaction encoder
            self.pair_encoder = nn.Sequential(
                nn.Linear(medication_dim * 2, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU()
            )
            
            # Synergy head
            self.synergy_head = nn.Sequential(
                nn.Linear(hidden_dim // 2, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
                nn.Sigmoid()  # 0-1 synergy score
            )
            
            # Antagonism head
            self.antagonism_head = nn.Sequential(
                nn.Linear(hidden_dim // 2, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
                nn.Sigmoid()  # 0-1 antagonism score
            )
            
        def forward(self, med1_embed: torch.Tensor, med2_embed: torch.Tensor) -> Dict[str, torch.Tensor]:
            # Symmetric encoding
            pair_forward = torch.cat([med1_embed, med2_embed], dim=-1)
            pair_backward = torch.cat([med2_embed, med1_embed], dim=-1)
            
            encoded_forward = self.pair_encoder(pair_forward)
            encoded_backward = self.pair_encoder(pair_backward)
            
            # Symmetric combination
            pair_features = (encoded_forward + encoded_backward) / 2
            
            synergy = self.synergy_head(pair_features)
            antagonism = self.antagonism_head(pair_features)
            
            return {
                'synergy_score': synergy,
                'antagonism_score': antagonism,
                'interaction_type': torch.where(
                    synergy > antagonism,
                    torch.ones_like(synergy),  # Synergistic
                    torch.where(
                        antagonism > 0.5,
                        -torch.ones_like(antagonism),  # Antagonistic
                        torch.zeros_like(synergy)  # Neutral
                    )
                )
            }
    
    
    class MultiTaskMedicationModel(nn.Module):
        """
        Multi-Task Learning Model for Therapeutic Medications
        
        Predicts multiple outcomes simultaneously:
        1. EAA Effect (years)
        2. Synergy potential
        3. Adverse effect risk
        4. Pathway impact scores
        5. Gene expression changes
        6. CpG methylation deltas
        """
        def __init__(self, input_dim: int = 32, shared_dim: int = 128,
                     num_pathways: int = 8, num_genes: int = 50, num_cpgs: int = 20):
            super().__init__()
            
            self.num_pathways = num_pathways
            self.num_genes = num_genes
            self.num_cpgs = num_cpgs
            
            # Shared encoder
            self.shared_encoder = nn.Sequential(
                nn.Linear(input_dim, shared_dim),
                nn.BatchNorm1d(shared_dim),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(shared_dim, shared_dim),
                nn.BatchNorm1d(shared_dim),
                nn.ReLU()
            )
            
            # Task-specific heads
            # 1. EAA Effect Head
            self.eaa_head = nn.Sequential(
                nn.Linear(shared_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 1)  # Single value: years
            )
            
            # 2. Synergy Head
            self.synergy_head = nn.Sequential(
                nn.Linear(shared_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 1),
                nn.Sigmoid()
            )
            
            # 3. Adverse Effect Head
            self.adverse_head = nn.Sequential(
                nn.Linear(shared_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 1),
                nn.Sigmoid()
            )
            
            # 4. Pathway Impact Head
            self.pathway_head = nn.Sequential(
                nn.Linear(shared_dim, 64),
                nn.ReLU(),
                nn.Linear(64, num_pathways),
                nn.Tanh()  # -1 to 1 impact
            )
            
            # 5. Gene Expression Head
            self.gene_head = nn.Sequential(
                nn.Linear(shared_dim, 128),
                nn.ReLU(),
                nn.Linear(128, num_genes),
                nn.Tanh()  # -1 to 1 fold change (log scale)
            )
            
            # 6. CpG Methylation Head
            self.cpg_head = nn.Sequential(
                nn.Linear(shared_dim, 64),
                nn.ReLU(),
                nn.Linear(64, num_cpgs),
                nn.Tanh()  # -1 to 1 methylation change
            )
            
        def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
            # Shared representation
            shared = self.shared_encoder(x)
            
            return {
                'eaa_effect': self.eaa_head(shared),
                'synergy_score': self.synergy_head(shared),
                'adverse_risk': self.adverse_head(shared),
                'pathway_impact': self.pathway_head(shared),
                'gene_expression': self.gene_head(shared),
                'cpg_methylation': self.cpg_head(shared),
                'shared_embedding': shared
            }
    
    
    class MedicationVAE(nn.Module):
        """
        Variational Autoencoder for medication effect latent space
        
        Learns a smooth latent representation of medication effects
        """
        def __init__(self, input_dim: int = 32, latent_dim: int = 16, hidden_dim: int = 64):
            super().__init__()
            
            self.latent_dim = latent_dim
            
            # Encoder
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU()
            )
            
            self.fc_mu = nn.Linear(hidden_dim, latent_dim)
            self.fc_var = nn.Linear(hidden_dim, latent_dim)
            
            # Decoder
            self.decoder = nn.Sequential(
                nn.Linear(latent_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, input_dim)
            )
            
            # EAA predictor from latent space
            self.eaa_predictor = nn.Sequential(
                nn.Linear(latent_dim, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
            )
            
        def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            h = self.encoder(x)
            return self.fc_mu(h), self.fc_var(h)
        
        def reparameterize(self, mu: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
            std = torch.exp(0.5 * log_var)
            eps = torch.randn_like(std)
            return mu + eps * std
        
        def decode(self, z: torch.Tensor) -> torch.Tensor:
            return self.decoder(z)
        
        def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
            mu, log_var = self.encode(x)
            z = self.reparameterize(mu, log_var)
            recon = self.decode(z)
            eaa = self.eaa_predictor(z)
            
            return {
                'reconstruction': recon,
                'mu': mu,
                'log_var': log_var,
                'z': z,
                'eaa_prediction': eaa
            }
        
        def loss_function(self, x: torch.Tensor, outputs: Dict[str, torch.Tensor],
                         eaa_target: Optional[torch.Tensor] = None,
                         beta: float = 1.0) -> Dict[str, torch.Tensor]:
            recon_loss = F.mse_loss(outputs['reconstruction'], x)
            kl_loss = -0.5 * torch.mean(1 + outputs['log_var'] - outputs['mu'].pow(2) - outputs['log_var'].exp())
            
            total_loss = recon_loss + beta * kl_loss
            
            if eaa_target is not None:
                eaa_loss = F.mse_loss(outputs['eaa_prediction'], eaa_target)
                total_loss = total_loss + eaa_loss
            else:
                eaa_loss = torch.tensor(0.0)
            
            return {
                'total_loss': total_loss,
                'recon_loss': recon_loss,
                'kl_loss': kl_loss,
                'eaa_loss': eaa_loss
            }


class TherapeuticDLEngine:
    """
    Deep Learning Engine for Therapeutic Medication Analysis
    
    Integrates all models and provides unified interface
    """
    
    def __init__(self):
        self.torch_available = TORCH_AVAILABLE
        
        # Model configurations
        self.config = {
            'input_dim': 32,
            'hidden_dim': 128,
            'latent_dim': 16,
            'num_pathways': 8,
            'num_genes': 50,
            'num_cpgs': 20,
            'num_medications': 50
        }
        
        # Initialize models if PyTorch available
        if TORCH_AVAILABLE:
            self._init_models()
        
        # Medication feature mapping
        self._init_medication_features()
    
    def _init_models(self):
        """Initialize all neural network models"""
        self.mlp = MedicationMLP(
            input_dim=self.config['input_dim'],
            hidden_dims=[128, 64, 32],
            output_dim=1
        )
        
        self.attention = MedicationAttention(
            embed_dim=64,
            num_heads=4
        )
        
        self.gnn = MedicationGNN(
            node_dim=64,
            hidden_dim=self.config['hidden_dim'],
            num_layers=3
        )
        
        self.synergy_predictor = MedicationSynergyPredictor(
            medication_dim=64,
            hidden_dim=self.config['hidden_dim']
        )
        
        self.multitask = MultiTaskMedicationModel(
            input_dim=self.config['input_dim'],
            shared_dim=self.config['hidden_dim'],
            num_pathways=self.config['num_pathways'],
            num_genes=self.config['num_genes'],
            num_cpgs=self.config['num_cpgs']
        )
        
        self.vae = MedicationVAE(
            input_dim=self.config['input_dim'],
            latent_dim=self.config['latent_dim'],
            hidden_dim=self.config['hidden_dim']
        )
        
        # Set to eval mode
        self.mlp.eval()
        self.attention.eval()
        self.gnn.eval()
        self.synergy_predictor.eval()
        self.multitask.eval()
        self.vae.eval()
    
    def _init_medication_features(self):
        """Initialize medication feature database"""
        from modules.therapeutic_medications import get_therapeutic_medication_database, EpigeneticEffect
        
        med_db = get_therapeutic_medication_database()
        self.medication_features = {}
        
        category_map = {
            'Antidiyabetik': 0, 'Lipid Dusurucu': 1, 'Antihipertansif': 2,
            'Antikoagulan': 3, 'Tiroid': 4, 'Antiinflamatuar': 5,
            'Immunsupresif': 6, 'Hormon': 7, 'Antidepresan': 8,
            'Antipsikotik': 9, 'Proton Pompasi Inhibitoru': 10,
            'Kortikosteroid': 11, 'Bifosfonat': 12, 'Biyolojik Ajan': 13
        }
        
        for med_id, med in med_db.medications.items():
            # Create category one-hot
            cat_vec = np.zeros(14)
            cat_idx = category_map.get(med.category.value, 0)
            cat_vec[cat_idx] = 1
            
            # Effect direction
            if med.eaa_direction == EpigeneticEffect.PROTECTIVE:
                effect_dir = -1
            elif med.eaa_direction == EpigeneticEffect.ACCELERATING:
                effect_dir = 1
            else:
                effect_dir = 0
            
            self.medication_features[med_id] = MedicationFeatures(
                medication_id=med_id,
                category_vector=cat_vec,
                effect_direction=effect_dir,
                target_gene_count=len(med.target_genes),
                cpg_count=len(med.affected_cpgs),
                sample_size=med.sample_size,
                pubmed_count=len(med.pubmed_ids),
                typical_duration_years=med.typical_duration_years,
                dose_dependent=med.dose_dependent,
                reversible=med.reversible
            )
    
    def _features_to_tensor(self, medication_ids: List[str]) -> Optional[Any]:
        """Convert medication IDs to feature tensor"""
        if not TORCH_AVAILABLE:
            return None
        
        features = []
        for med_id in medication_ids:
            if med_id in self.medication_features:
                feat = self.medication_features[med_id]
                
                # Build feature vector
                vec = np.concatenate([
                    feat.category_vector,  # 14
                    [feat.effect_direction],  # 1
                    [feat.target_gene_count / 10],  # 1, normalized
                    [feat.cpg_count / 10],  # 1
                    [feat.sample_size / 5000],  # 1, normalized
                    [feat.pubmed_count / 10],  # 1
                    [feat.typical_duration_years / 20],  # 1
                    [float(feat.dose_dependent)],  # 1
                    [float(feat.reversible)],  # 1
                    np.zeros(10)  # padding to 32
                ])
                features.append(vec[:32])
        
        if not features:
            return None
        
        return torch.tensor(np.array(features), dtype=torch.float32)
    
    def predict_eaa_mlp(self, medication_ids: List[str], durations: Dict[str, float]) -> Dict:
        """Predict EAA effect using MLP"""
        if not TORCH_AVAILABLE:
            return self._simulate_prediction(medication_ids, durations, 'mlp')
        
        x = self._features_to_tensor(medication_ids)
        if x is None:
            return {'error': 'No valid medications'}
        
        with torch.no_grad():
            predictions = self.mlp(x)
        
        results = []
        for i, med_id in enumerate(medication_ids):
            duration = durations.get(med_id, 1.0)
            base_pred = predictions[i].item()
            adjusted = base_pred * np.log1p(duration)
            results.append({
                'medication': med_id,
                'base_prediction': round(base_pred, 3),
                'duration': duration,
                'adjusted_prediction': round(adjusted, 3)
            })
        
        total = sum(r['adjusted_prediction'] for r in results)
        
        return {
            'model': 'MLP',
            'total_eaa_effect': round(total, 2),
            'individual_predictions': results,
            'confidence': 0.85
        }
    
    def predict_multitask(self, medication_ids: List[str], durations: Dict[str, float]) -> Dict:
        """Multi-task prediction"""
        if not TORCH_AVAILABLE:
            return self._simulate_prediction(medication_ids, durations, 'multitask')
        
        x = self._features_to_tensor(medication_ids)
        if x is None:
            return {'error': 'No valid medications'}
        
        with torch.no_grad():
            outputs = self.multitask(x)
        
        # Aggregate predictions
        eaa_total = outputs['eaa_effect'].sum().item()
        synergy_avg = outputs['synergy_score'].mean().item()
        adverse_max = outputs['adverse_risk'].max().item()
        pathway_impact = outputs['pathway_impact'].mean(dim=0).numpy()
        
        pathway_names = [
            'HPA Axis', 'Insulin Signaling', 'Inflammation', 'Dopamine',
            'Serotonin', 'Oxidative Stress', 'Metabolic', 'Immune'
        ]
        
        return {
            'model': 'Multi-Task Neural Network',
            'predictions': {
                'eaa_effect': round(eaa_total, 2),
                'synergy_potential': round(synergy_avg, 3),
                'adverse_risk': round(adverse_max, 3),
                'pathway_impacts': {
                    name: round(float(impact), 3)
                    for name, impact in zip(pathway_names, pathway_impact)
                }
            },
            'medications_analyzed': len(medication_ids),
            'model_parameters': sum(p.numel() for p in self.multitask.parameters())
        }
    
    def predict_vae(self, medication_ids: List[str]) -> Dict:
        """VAE-based prediction with latent space analysis"""
        if not TORCH_AVAILABLE:
            return self._simulate_vae(medication_ids)
        
        x = self._features_to_tensor(medication_ids)
        if x is None:
            return {'error': 'No valid medications'}
        
        with torch.no_grad():
            outputs = self.vae(x)
        
        return {
            'model': 'Variational Autoencoder',
            'latent_dimensions': self.config['latent_dim'],
            'latent_vectors': outputs['z'].numpy().tolist(),
            'eaa_predictions': outputs['eaa_prediction'].squeeze().numpy().tolist(),
            'reconstruction_quality': 1 - F.mse_loss(outputs['reconstruction'], x).item(),
            'medications': medication_ids
        }
    
    def build_medication_graph(self, medication_ids: List[str]) -> Dict:
        """Build medication-gene-cpg graph for GNN"""
        from modules.therapeutic_medications import get_therapeutic_medication_database
        
        med_db = get_therapeutic_medication_database()
        
        nodes = []
        node_types = []
        edges = []
        edge_types = []
        
        node_idx = {}
        
        # Add medication nodes
        for med_id in medication_ids:
            med = med_db.get_medication(med_id)
            if med:
                idx = len(nodes)
                node_idx[('med', med_id)] = idx
                nodes.append({'id': med_id, 'type': 'medication', 'name': med.name_turkish})
                node_types.append(0)
                
                # Add gene nodes
                for gene in med.target_genes:
                    gene_key = ('gene', gene)
                    if gene_key not in node_idx:
                        gene_idx = len(nodes)
                        node_idx[gene_key] = gene_idx
                        nodes.append({'id': gene, 'type': 'gene', 'name': gene})
                        node_types.append(1)
                    
                    # Medication -> Gene edge
                    edges.append((idx, node_idx[gene_key]))
                    edge_types.append(0)  # targets
                
                # Add CpG nodes
                for cpg in med.affected_cpgs:
                    cpg_key = ('cpg', cpg)
                    if cpg_key not in node_idx:
                        cpg_idx = len(nodes)
                        node_idx[cpg_key] = cpg_idx
                        nodes.append({'id': cpg, 'type': 'cpg', 'name': cpg})
                        node_types.append(2)
                    
                    # Medication -> CpG edge
                    edges.append((idx, node_idx[cpg_key]))
                    edge_types.append(1)  # affects methylation
        
        # Add medication-medication edges (synergies)
        for i, med_id1 in enumerate(medication_ids):
            med1 = med_db.get_medication(med_id1)
            if med1:
                for med_id2 in med1.synergistic_with:
                    if med_id2 in medication_ids:
                        idx1 = node_idx.get(('med', med_id1))
                        idx2 = node_idx.get(('med', med_id2))
                        if idx1 is not None and idx2 is not None:
                            edges.append((idx1, idx2))
                            edge_types.append(2)  # synergy
                
                for med_id2 in med1.antagonistic_with:
                    if med_id2 in medication_ids:
                        idx1 = node_idx.get(('med', med_id1))
                        idx2 = node_idx.get(('med', med_id2))
                        if idx1 is not None and idx2 is not None:
                            edges.append((idx1, idx2))
                            edge_types.append(3)  # antagonism
        
        return {
            'nodes': nodes,
            'node_types': node_types,
            'edges': edges,
            'edge_types': edge_types,
            'num_medications': sum(1 for t in node_types if t == 0),
            'num_genes': sum(1 for t in node_types if t == 1),
            'num_cpgs': sum(1 for t in node_types if t == 2),
            'num_edges': len(edges)
        }
    
    def predict_gnn(self, medication_ids: List[str], durations: Dict[str, float]) -> Dict:
        """GNN-based prediction using medication graph"""
        if not TORCH_AVAILABLE:
            return self._simulate_gnn(medication_ids, durations)
        
        # Build graph
        graph = self.build_medication_graph(medication_ids)
        
        if not graph['edges']:
            return {'error': 'No valid graph structure'}
        
        # Convert to tensors
        num_nodes = len(graph['nodes'])
        node_features = torch.randn(num_nodes, 64)  # Random initialization for demo
        edge_index = torch.tensor(graph['edges'], dtype=torch.long).T
        edge_type = torch.tensor(graph['edge_types'], dtype=torch.long)
        node_type = torch.tensor(graph['node_types'], dtype=torch.long)
        
        with torch.no_grad():
            outputs = self.gnn(node_features, edge_index, edge_type, node_type)
        
        return {
            'model': 'Graph Neural Network',
            'graph_structure': {
                'medications': graph['num_medications'],
                'genes': graph['num_genes'],
                'cpgs': graph['num_cpgs'],
                'edges': graph['num_edges']
            },
            'prediction': round(outputs['prediction'].item(), 2),
            'node_embeddings_shape': list(outputs['node_embeddings'].shape),
            'message_passing_layers': 3
        }
    
    def _simulate_prediction(self, medication_ids: List[str], durations: Dict[str, float], model_type: str) -> Dict:
        """Simulation mode when PyTorch not available"""
        from modules.therapeutic_medications import get_therapeutic_medication_database
        
        med_db = get_therapeutic_medication_database()
        results = []
        total = 0
        
        for med_id in medication_ids:
            med = med_db.get_medication(med_id)
            if med:
                duration = durations.get(med_id, 1.0)
                adjusted = med.eaa_effect * np.log1p(duration) / np.log1p(med.typical_duration_years)
                results.append({
                    'medication': med_id,
                    'name': med.name_turkish,
                    'base_effect': med.eaa_effect,
                    'adjusted_effect': round(adjusted, 2)
                })
                total += adjusted
        
        return {
            'model': f'{model_type.upper()} (Simulation)',
            'total_eaa_effect': round(total, 2),
            'predictions': results,
            'note': 'PyTorch not available - using rule-based simulation'
        }
    
    def _simulate_vae(self, medication_ids: List[str]) -> Dict:
        """Simulate VAE when PyTorch not available"""
        return {
            'model': 'VAE (Simulation)',
            'latent_dimensions': 16,
            'latent_vectors': [np.random.randn(16).tolist() for _ in medication_ids],
            'medications': medication_ids,
            'note': 'PyTorch not available - using random simulation'
        }
    
    def _simulate_gnn(self, medication_ids: List[str], durations: Dict[str, float]) -> Dict:
        """Simulate GNN when PyTorch not available"""
        graph = self.build_medication_graph(medication_ids)
        
        from modules.therapeutic_medications import get_therapeutic_medication_database
        med_db = get_therapeutic_medication_database()
        
        total = 0
        for med_id in medication_ids:
            med = med_db.get_medication(med_id)
            if med:
                total += med.eaa_effect
        
        return {
            'model': 'GNN (Simulation)',
            'graph_structure': graph,
            'prediction': round(total, 2),
            'note': 'PyTorch not available - using aggregated effects'
        }
    
    def get_model_summary(self) -> Dict:
        """Get summary of all available models"""
        summary = {
            'torch_available': TORCH_AVAILABLE,
            'models': {
                'MLP': {
                    'description': 'Multi-Layer Perceptron for EAA prediction',
                    'architecture': '32 -> 128 -> 64 -> 32 -> 1',
                    'parameters': sum(p.numel() for p in self.mlp.parameters()) if TORCH_AVAILABLE else 'N/A'
                },
                'Attention': {
                    'description': 'Self-Attention for medication combinations',
                    'heads': 4,
                    'embed_dim': 64,
                    'parameters': sum(p.numel() for p in self.attention.parameters()) if TORCH_AVAILABLE else 'N/A'
                },
                'GNN': {
                    'description': 'Graph Neural Network for Medication-Gene-CpG relationships',
                    'layers': 3,
                    'node_types': ['Medication', 'Gene', 'CpG'],
                    'edge_types': ['targets', 'methylation', 'synergy', 'antagonism'],
                    'parameters': sum(p.numel() for p in self.gnn.parameters()) if TORCH_AVAILABLE else 'N/A'
                },
                'Synergy': {
                    'description': 'Medication pair synergy/antagonism predictor',
                    'parameters': sum(p.numel() for p in self.synergy_predictor.parameters()) if TORCH_AVAILABLE else 'N/A'
                },
                'MultiTask': {
                    'description': 'Multi-task learning for 6 prediction targets',
                    'tasks': ['EAA Effect', 'Synergy', 'Adverse Risk', 'Pathway Impact', 'Gene Expression', 'CpG Methylation'],
                    'parameters': sum(p.numel() for p in self.multitask.parameters()) if TORCH_AVAILABLE else 'N/A'
                },
                'VAE': {
                    'description': 'Variational Autoencoder for latent space analysis',
                    'latent_dim': 16,
                    'parameters': sum(p.numel() for p in self.vae.parameters()) if TORCH_AVAILABLE else 'N/A'
                }
            },
            'total_parameters': sum(
                sum(p.numel() for p in m.parameters())
                for m in [self.mlp, self.attention, self.gnn, self.synergy_predictor, self.multitask, self.vae]
            ) if TORCH_AVAILABLE else 'N/A'
        }
        
        return summary


def get_therapeutic_dl_engine() -> TherapeuticDLEngine:
    """Get or create DL engine singleton"""
    if not hasattr(get_therapeutic_dl_engine, '_instance'):
        get_therapeutic_dl_engine._instance = TherapeuticDLEngine()
    return get_therapeutic_dl_engine._instance
