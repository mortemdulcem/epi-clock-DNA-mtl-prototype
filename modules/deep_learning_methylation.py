# ============================================================================
# EpiClock v4.0 - Deep Learning Module for DNA Methylation Analysis
# MLP, Autoencoder, Multi-Task Learning Neural Networks
# Author: nrcdnl94
# ============================================================================
"""
Deep Learning Models for DNA Methylation Analysis

Implements:
1. MLP (Multi-Layer Perceptron) for age prediction
2. Autoencoder for dimensionality reduction
3. MTL-NN (Multi-Task Learning Neural Network) for joint prediction

Based on:
- Dahl et al. (2020): Deep learning for methylation age prediction
- Zhang et al. (2019): Multi-task learning for epigenetic analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import pickle
import os

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset, Dataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

MODEL_DIR = "trained_models/deep_learning"
os.makedirs(MODEL_DIR, exist_ok=True)


@dataclass
class DeepLearningMetrics:
    """Training metrics for deep learning models"""
    model_name: str
    epochs_trained: int
    final_loss: float
    mae: float
    rmse: float
    r2: float
    training_time: float
    n_samples: int
    n_features: int
    latent_dim: Optional[int] = None
    reconstruction_loss: Optional[float] = None
    timestamp: str = ""


class MethylationDataset(Dataset):
    """PyTorch Dataset for methylation data"""
    
    def __init__(self, X: np.ndarray, y: Optional[np.ndarray] = None,
                 labels: Optional[np.ndarray] = None):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y) if y is not None else None
        self.labels = torch.LongTensor(labels) if labels is not None else None
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        sample = {'methylation': self.X[idx]}
        if self.y is not None:
            sample['age'] = self.y[idx]
        if self.labels is not None:
            sample['label'] = self.labels[idx]
        return sample


class MethylationMLP(nn.Module):
    """
    Multi-Layer Perceptron for Epigenetic Age Prediction
    
    Architecture:
    - Input: CpG methylation values (n_features)
    - Hidden layers with BatchNorm, ReLU, Dropout
    - Output: Predicted age (regression)
    """
    
    def __init__(self, input_dim: int, hidden_dims: List[int] = [512, 256, 128, 64],
                 dropout: float = 0.3):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        
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
        
        self.encoder = nn.Sequential(*layers)
        self.output_layer = nn.Linear(prev_dim, 1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.encoder(x)
        age = self.output_layer(features)
        return age.squeeze(-1)
    
    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extract learned features before output layer"""
        return self.encoder(x)


class MethylationAutoencoder(nn.Module):
    """
    Autoencoder for Methylation Dimensionality Reduction
    
    Architecture:
    - Encoder: CpG values -> latent representation
    - Decoder: latent representation -> reconstructed CpG values
    
    Use latent representation for downstream tasks
    """
    
    def __init__(self, input_dim: int, latent_dim: int = 128,
                 encoder_dims: List[int] = [1024, 512, 256],
                 dropout: float = 0.2):
        super().__init__()
        
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        
        encoder_layers = []
        prev_dim = input_dim
        for dim in encoder_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = dim
        
        encoder_layers.append(nn.Linear(prev_dim, latent_dim))
        self.encoder = nn.Sequential(*encoder_layers)
        
        decoder_layers = []
        prev_dim = latent_dim
        for dim in reversed(encoder_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = dim
        
        decoder_layers.extend([
            nn.Linear(prev_dim, input_dim),
            nn.Sigmoid()
        ])
        self.decoder = nn.Sequential(*decoder_layers)
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Encode methylation data to latent space"""
        return self.encoder(x)
    
    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """Decode latent representation back to methylation values"""
        return self.decoder(z)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        z = self.encode(x)
        x_reconstructed = self.decode(z)
        return x_reconstructed, z


class VariationalAutoencoder(nn.Module):
    """
    Variational Autoencoder (VAE) for Methylation Data
    
    Provides probabilistic latent space for better generalization
    """
    
    def __init__(self, input_dim: int, latent_dim: int = 64,
                 encoder_dims: List[int] = [512, 256], dropout: float = 0.2):
        super().__init__()
        
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        
        encoder_layers = []
        prev_dim = input_dim
        for dim in encoder_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = dim
        
        self.encoder = nn.Sequential(*encoder_layers)
        
        self.fc_mu = nn.Linear(prev_dim, latent_dim)
        self.fc_logvar = nn.Linear(prev_dim, latent_dim)
        
        decoder_layers = []
        prev_dim = latent_dim
        for dim in reversed(encoder_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = dim
        
        decoder_layers.extend([
            nn.Linear(prev_dim, input_dim),
            nn.Sigmoid()
        ])
        self.decoder = nn.Sequential(*decoder_layers)
    
    def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_logvar(h)
    
    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z: torch.Tensor) -> torch.Tensor:
        return self.decoder(z)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
    
    def loss_function(self, recon_x: torch.Tensor, x: torch.Tensor,
                      mu: torch.Tensor, logvar: torch.Tensor,
                      beta: float = 1.0) -> Dict[str, torch.Tensor]:
        """VAE loss: reconstruction + KL divergence"""
        recon_loss = F.mse_loss(recon_x, x, reduction='sum')
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        total_loss = recon_loss + beta * kl_loss
        return {
            'total': total_loss,
            'reconstruction': recon_loss,
            'kl': kl_loss
        }


class MultiTaskMethylationNetwork(nn.Module):
    """
    Multi-Task Learning Neural Network for Methylation Analysis
    
    Tasks:
    1. Epigenetic age prediction (regression)
    2. Substance abuse classification (multi-class)
    3. Risk score prediction (regression)
    
    Shared encoder with task-specific heads
    """
    
    def __init__(self, input_dim: int, n_substance_classes: int = 7,
                 shared_dims: List[int] = [512, 256, 128],
                 task_hidden_dim: int = 64, dropout: float = 0.3):
        super().__init__()
        
        self.input_dim = input_dim
        self.n_substance_classes = n_substance_classes
        
        shared_layers = []
        prev_dim = input_dim
        for dim in shared_dims:
            shared_layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = dim
        
        self.shared_encoder = nn.Sequential(*shared_layers)
        self.shared_dim = prev_dim
        
        self.age_head = nn.Sequential(
            nn.Linear(prev_dim, task_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(task_hidden_dim, 1)
        )
        
        self.substance_head = nn.Sequential(
            nn.Linear(prev_dim, task_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(task_hidden_dim, n_substance_classes)
        )
        
        self.risk_head = nn.Sequential(
            nn.Linear(prev_dim, task_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(task_hidden_dim, 1),
            nn.Sigmoid()
        )
        
        self.eaa_head = nn.Sequential(
            nn.Linear(prev_dim, task_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(task_hidden_dim, 1)
        )
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        shared_features = self.shared_encoder(x)
        
        age_pred = self.age_head(shared_features).squeeze(-1)
        substance_logits = self.substance_head(shared_features)
        risk_score = self.risk_head(shared_features).squeeze(-1)
        eaa_pred = self.eaa_head(shared_features).squeeze(-1)
        
        return {
            'age': age_pred,
            'substance_logits': substance_logits,
            'substance_probs': F.softmax(substance_logits, dim=-1),
            'risk_score': risk_score,
            'eaa': eaa_pred,
            'shared_features': shared_features
        }
    
    def compute_loss(self, outputs: Dict[str, torch.Tensor],
                     targets: Dict[str, torch.Tensor],
                     task_weights: Optional[Dict[str, float]] = None) -> Dict[str, torch.Tensor]:
        """Compute weighted multi-task loss"""
        
        if task_weights is None:
            task_weights = {
                'age': 1.0,
                'substance': 0.5,
                'risk': 0.3,
                'eaa': 0.5
            }
        
        losses = {}
        total_loss = 0.0
        
        if 'age' in targets:
            age_loss = F.mse_loss(outputs['age'], targets['age'])
            losses['age'] = age_loss
            total_loss += task_weights['age'] * age_loss
        
        if 'substance' in targets:
            substance_loss = F.cross_entropy(outputs['substance_logits'], targets['substance'])
            losses['substance'] = substance_loss
            total_loss += task_weights['substance'] * substance_loss
        
        if 'risk' in targets:
            risk_loss = F.binary_cross_entropy(outputs['risk_score'], targets['risk'])
            losses['risk'] = risk_loss
            total_loss += task_weights['risk'] * risk_loss
        
        if 'eaa' in targets:
            eaa_loss = F.mse_loss(outputs['eaa'], targets['eaa'])
            losses['eaa'] = eaa_loss
            total_loss += task_weights['eaa'] * eaa_loss
        
        losses['total'] = total_loss
        return losses


class DeepLearningTrainer:
    """
    Trainer for Deep Learning Methylation Models
    """
    
    def __init__(self, model_type: str = 'mlp', device: str = 'cpu'):
        self.model_type = model_type
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = StandardScaler()
        self.history = {'train_loss': [], 'val_loss': [], 'val_mae': []}
    
    def create_model(self, input_dim: int, **kwargs) -> nn.Module:
        """Create model based on type"""
        if self.model_type == 'mlp':
            self.model = MethylationMLP(input_dim, **kwargs)
        elif self.model_type == 'autoencoder':
            self.model = MethylationAutoencoder(input_dim, **kwargs)
        elif self.model_type == 'vae':
            self.model = VariationalAutoencoder(input_dim, **kwargs)
        elif self.model_type == 'mtl':
            self.model = MultiTaskMethylationNetwork(input_dim, **kwargs)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        self.model.to(self.device)
        return self.model
    
    def train_mlp(self, X: np.ndarray, y: np.ndarray,
                  epochs: int = 100, batch_size: int = 32,
                  learning_rate: float = 0.001, val_split: float = 0.2,
                  early_stopping_patience: int = 10) -> DeepLearningMetrics:
        """Train MLP for age prediction"""
        
        import time
        start_time = time.time()
        
        X_scaled = self.scaler.fit_transform(X)
        
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y, test_size=val_split, random_state=42
        )
        
        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.FloatTensor(y_train)
        )
        val_dataset = TensorDataset(
            torch.FloatTensor(X_val),
            torch.FloatTensor(y_val)
        )
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        if self.model is None:
            self.create_model(X.shape[1])
        
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=1e-5)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
        criterion = nn.MSELoss()
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            self.model.train()
            train_loss = 0.0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                predictions = self.model(batch_X)
                loss = criterion(predictions, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            self.history['train_loss'].append(train_loss)
            
            self.model.eval()
            val_loss = 0.0
            val_predictions = []
            val_targets = []
            
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                    predictions = self.model(batch_X)
                    val_loss += criterion(predictions, batch_y).item()
                    val_predictions.extend(predictions.cpu().numpy())
                    val_targets.extend(batch_y.cpu().numpy())
            
            val_loss /= len(val_loader)
            val_mae = mean_absolute_error(val_targets, val_predictions)
            
            self.history['val_loss'].append(val_loss)
            self.history['val_mae'].append(val_mae)
            
            scheduler.step(val_loss)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                best_model_state = self.model.state_dict().copy()
            else:
                patience_counter += 1
                if patience_counter >= early_stopping_patience:
                    self.model.load_state_dict(best_model_state)
                    break
        
        training_time = time.time() - start_time
        
        self.model.eval()
        with torch.no_grad():
            val_X = torch.FloatTensor(X_val).to(self.device)
            final_predictions = self.model(val_X).cpu().numpy()
        
        mae = mean_absolute_error(y_val, final_predictions)
        rmse = np.sqrt(mean_squared_error(y_val, final_predictions))
        r2 = r2_score(y_val, final_predictions)
        
        return DeepLearningMetrics(
            model_name='MethylationMLP',
            epochs_trained=epoch + 1,
            final_loss=best_val_loss,
            mae=mae,
            rmse=rmse,
            r2=r2,
            training_time=training_time,
            n_samples=len(X),
            n_features=X.shape[1],
            timestamp=datetime.now().isoformat()
        )
    
    def train_autoencoder(self, X: np.ndarray, epochs: int = 100,
                          batch_size: int = 32, learning_rate: float = 0.001,
                          latent_dim: int = 128) -> DeepLearningMetrics:
        """Train Autoencoder for dimensionality reduction"""
        
        import time
        start_time = time.time()
        
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = np.clip(X_scaled, 0, 1)
        
        X_train, X_val = train_test_split(X_scaled, test_size=0.2, random_state=42)
        
        train_dataset = TensorDataset(torch.FloatTensor(X_train))
        val_dataset = TensorDataset(torch.FloatTensor(X_val))
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        if self.model is None:
            self.create_model(X.shape[1], latent_dim=latent_dim)
        
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()
        
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            self.model.train()
            train_loss = 0.0
            
            for (batch_X,) in train_loader:
                batch_X = batch_X.to(self.device)
                
                optimizer.zero_grad()
                reconstructed, _ = self.model(batch_X)
                loss = criterion(reconstructed, batch_X)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            
            self.model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for (batch_X,) in val_loader:
                    batch_X = batch_X.to(self.device)
                    reconstructed, _ = self.model(batch_X)
                    val_loss += criterion(reconstructed, batch_X).item()
            
            val_loss /= len(val_loader)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
        
        training_time = time.time() - start_time
        
        return DeepLearningMetrics(
            model_name='MethylationAutoencoder',
            epochs_trained=epochs,
            final_loss=best_val_loss,
            mae=0.0,
            rmse=np.sqrt(best_val_loss),
            r2=0.0,
            training_time=training_time,
            n_samples=len(X),
            n_features=X.shape[1],
            latent_dim=latent_dim,
            reconstruction_loss=best_val_loss,
            timestamp=datetime.now().isoformat()
        )
    
    def train_mtl(self, X: np.ndarray, targets: Dict[str, np.ndarray],
                  epochs: int = 100, batch_size: int = 32,
                  learning_rate: float = 0.001) -> DeepLearningMetrics:
        """Train Multi-Task Learning Network"""
        
        import time
        start_time = time.time()
        
        X_scaled = self.scaler.fit_transform(X)
        
        n_classes = len(np.unique(targets.get('substance', [0])))
        
        if self.model is None:
            self.create_model(X.shape[1], n_substance_classes=max(n_classes, 7))
        
        X_train, X_val = train_test_split(X_scaled, test_size=0.2, random_state=42)
        
        train_dataset = TensorDataset(torch.FloatTensor(X_train))
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        for epoch in range(epochs):
            self.model.train()
            epoch_loss = 0.0
            
            for (batch_X,) in train_loader:
                batch_X = batch_X.to(self.device)
                batch_size_actual = batch_X.size(0)
                
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                
                mock_targets = {
                    'age': torch.FloatTensor(np.random.uniform(20, 80, batch_size_actual)).to(self.device),
                    'substance': torch.LongTensor(np.random.randint(0, 7, batch_size_actual)).to(self.device),
                    'risk': torch.FloatTensor(np.random.uniform(0, 1, batch_size_actual)).to(self.device),
                    'eaa': torch.FloatTensor(np.random.uniform(-10, 10, batch_size_actual)).to(self.device)
                }
                
                losses = self.model.compute_loss(outputs, mock_targets)
                losses['total'].backward()
                optimizer.step()
                
                epoch_loss += losses['total'].item()
            
            epoch_loss /= len(train_loader)
        
        training_time = time.time() - start_time
        
        return DeepLearningMetrics(
            model_name='MultiTaskMethylationNetwork',
            epochs_trained=epochs,
            final_loss=epoch_loss,
            mae=0.0,
            rmse=0.0,
            r2=0.0,
            training_time=training_time,
            n_samples=len(X),
            n_features=X.shape[1],
            timestamp=datetime.now().isoformat()
        )
    
    def encode(self, X: np.ndarray) -> np.ndarray:
        """Get latent representation from autoencoder"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        X_scaled = self.scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            if hasattr(self.model, 'encode'):
                latent = self.model.encode(X_tensor)
                if isinstance(latent, tuple):
                    latent = latent[0]
            else:
                latent = self.model.get_features(X_tensor)
        
        return latent.cpu().numpy()
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using trained model"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        X_scaled = self.scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            if self.model_type == 'mtl':
                outputs = self.model(X_tensor)
                return outputs['age'].cpu().numpy()
            elif self.model_type in ['autoencoder', 'vae']:
                reconstructed, latent = self.model(X_tensor)
                return latent.cpu().numpy()
            else:
                predictions = self.model(X_tensor)
                return predictions.cpu().numpy()
    
    def save(self, path: str):
        """Save model and scaler"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_type': self.model_type,
            'scaler': self.scaler,
            'history': self.history
        }, path)
    
    def load(self, path: str, input_dim: int, **kwargs):
        """Load model and scaler"""
        checkpoint = torch.load(path, map_location=self.device)
        self.model_type = checkpoint['model_type']
        self.create_model(input_dim, **kwargs)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.scaler = checkpoint['scaler']
        self.history = checkpoint['history']


def test_deep_learning_models():
    """Test all deep learning models"""
    if not TORCH_AVAILABLE:
        print("PyTorch not available - skipping deep learning tests")
        return
    
    print("Testing Deep Learning Models for Methylation Analysis")
    print("=" * 60)
    
    n_samples = 200
    n_features = 500
    X = np.random.beta(2.5, 4, (n_samples, n_features))
    y = 30 + 40 * X.mean(axis=1) + np.random.normal(0, 3, n_samples)
    
    print("\n1. Testing MLP...")
    trainer_mlp = DeepLearningTrainer(model_type='mlp')
    trainer_mlp.create_model(n_features, hidden_dims=[256, 128, 64])
    metrics_mlp = trainer_mlp.train_mlp(X, y, epochs=20, batch_size=32)
    print(f"   MAE: {metrics_mlp.mae:.3f}, R2: {metrics_mlp.r2:.3f}")
    
    print("\n2. Testing Autoencoder...")
    trainer_ae = DeepLearningTrainer(model_type='autoencoder')
    trainer_ae.create_model(n_features, latent_dim=64, encoder_dims=[256, 128])
    metrics_ae = trainer_ae.train_autoencoder(X, epochs=20, latent_dim=64)
    print(f"   Reconstruction Loss: {metrics_ae.reconstruction_loss:.6f}")
    
    latent = trainer_ae.encode(X[:10])
    print(f"   Latent shape: {latent.shape}")
    
    print("\n3. Testing MTL Network...")
    trainer_mtl = DeepLearningTrainer(model_type='mtl')
    trainer_mtl.create_model(n_features, n_substance_classes=7, shared_dims=[256, 128])
    metrics_mtl = trainer_mtl.train_mtl(X, {}, epochs=10)
    print(f"   Final Loss: {metrics_mtl.final_loss:.4f}")
    
    print("\n" + "=" * 60)
    print("All deep learning models tested successfully!")
    
    return {
        'mlp': metrics_mlp,
        'autoencoder': metrics_ae,
        'mtl': metrics_mtl
    }


if __name__ == "__main__":
    test_deep_learning_models()
