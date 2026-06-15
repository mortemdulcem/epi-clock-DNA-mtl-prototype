"""
Reproducibility (Tekrarlanabilirlik) Altyapisi
EpiClock v4.0

Bilimsel tekrarlanabilirlik standartlari:
- Seed sabitleme
- Versiyon kilitleme
- Hash-based verification
- Environment capture
- Deterministic pipelines

Referanslar:
- Sandve et al. (2013) Ten Simple Rules for Reproducible Computational Research
- Peng (2011) Reproducible Research in Computational Science
"""

import numpy as np
import pandas as pd
import random
import os
import sys
import hashlib
import json
import platform
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import wraps
import warnings


# ============================================================================
# GLOBAL SEED MANAGER
# ============================================================================

class SeedManager:
    """
    Global Seed Yonetimi
    
    Tum random number generator'lari tutarli sekilde seed'ler
    """
    
    _instance = None
    _seed: int = 42
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_global_seed(cls, seed: int = 42):
        """Tum RNG'leri seed'le"""
        cls._seed = seed
        cls._initialized = True
        
        # Python random
        random.seed(seed)
        
        # NumPy
        np.random.seed(seed)
        
        # OS environment (for subprocess reproducibility)
        os.environ['PYTHONHASHSEED'] = str(seed)
        
        # Try to seed PyTorch if available
        try:
            import torch
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        except ImportError:
            pass
        
        # Try to seed TensorFlow if available
        try:
            import tensorflow as tf
            tf.random.set_seed(seed)
        except ImportError:
            pass
        
        return seed
    
    @classmethod
    def get_seed(cls) -> int:
        """Mevcut seed'i getir"""
        return cls._seed
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Seed ayarlanmis mi?"""
        return cls._initialized
    
    @classmethod
    def get_random_state(cls) -> Dict[str, Any]:
        """RNG durumlarini kaydet"""
        return {
            'seed': cls._seed,
            'python_random': random.getstate(),
            'numpy_random': np.random.get_state()[1].tolist()[:10]  # First 10 values
        }


def set_reproducibility_seed(seed: int = 42):
    """Convenience function for setting global seed"""
    return SeedManager.set_global_seed(seed)


# ============================================================================
# ENVIRONMENT CAPTURE
# ============================================================================

@dataclass
class EnvironmentSnapshot:
    """Calisma ortami snapshot'i"""
    timestamp: str
    python_version: str
    platform: str
    architecture: str
    packages: Dict[str, str]
    environment_variables: Dict[str, str]
    working_directory: str
    seed: int
    git_hash: Optional[str] = None


class EnvironmentCapture:
    """
    Calisma Ortami Yakalama
    
    Reproducibility icin ortam bilgilerini kaydet
    """
    
    @staticmethod
    def capture() -> EnvironmentSnapshot:
        """Mevcut ortami yakala"""
        
        # Package versions
        packages = {}
        critical_packages = [
            'numpy', 'pandas', 'scipy', 'scikit-learn', 
            'statsmodels', 'plotly', 'matplotlib', 'seaborn',
            'torch', 'xgboost', 'streamlit'
        ]
        
        for pkg in critical_packages:
            try:
                module = __import__(pkg)
                packages[pkg] = getattr(module, '__version__', 'unknown')
            except ImportError:
                packages[pkg] = 'not installed'
        
        # Git hash
        git_hash = None
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                git_hash = result.stdout.strip()[:8]
        except:
            pass
        
        # Environment variables (safe subset)
        safe_env_vars = ['PATH', 'PYTHONPATH', 'VIRTUAL_ENV', 'CONDA_PREFIX']
        env_vars = {k: os.environ.get(k, '')[:100] for k in safe_env_vars}
        
        return EnvironmentSnapshot(
            timestamp=datetime.now().isoformat(),
            python_version=sys.version,
            platform=platform.platform(),
            architecture=platform.machine(),
            packages=packages,
            environment_variables=env_vars,
            working_directory=os.getcwd(),
            seed=SeedManager.get_seed(),
            git_hash=git_hash
        )
    
    @staticmethod
    def save_snapshot(snapshot: EnvironmentSnapshot, filepath: str = "environment_snapshot.json"):
        """Snapshot'i kaydet"""
        with open(filepath, 'w') as f:
            json.dump(asdict(snapshot), f, indent=2)
    
    @staticmethod
    def load_snapshot(filepath: str) -> EnvironmentSnapshot:
        """Snapshot'i yukle"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return EnvironmentSnapshot(**data)
    
    @staticmethod
    def compare_environments(snapshot1: EnvironmentSnapshot, 
                            snapshot2: EnvironmentSnapshot) -> Dict[str, Any]:
        """Iki ortami karsilastir"""
        
        differences = {
            'python_version_match': snapshot1.python_version == snapshot2.python_version,
            'platform_match': snapshot1.platform == snapshot2.platform,
            'seed_match': snapshot1.seed == snapshot2.seed,
            'package_differences': {}
        }
        
        all_packages = set(snapshot1.packages.keys()) | set(snapshot2.packages.keys())
        
        for pkg in all_packages:
            v1 = snapshot1.packages.get(pkg, 'missing')
            v2 = snapshot2.packages.get(pkg, 'missing')
            if v1 != v2:
                differences['package_differences'][pkg] = {'env1': v1, 'env2': v2}
        
        differences['compatible'] = (
            differences['python_version_match'] and 
            len(differences['package_differences']) == 0
        )
        
        return differences


# ============================================================================
# DATA CHECKSUMS
# ============================================================================

class DataChecksum:
    """
    Veri Butunlugu Kontrolu
    
    Hash-based veri dogrulama
    """
    
    @staticmethod
    def compute_dataframe_hash(df: pd.DataFrame, algorithm: str = 'sha256') -> str:
        """DataFrame hash'i hesapla"""
        
        # Convert to bytes
        content = df.to_csv(index=True).encode('utf-8')
        
        if algorithm == 'sha256':
            return hashlib.sha256(content).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(content).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def compute_array_hash(arr: np.ndarray, algorithm: str = 'sha256') -> str:
        """NumPy array hash'i hesapla"""
        
        content = arr.tobytes()
        
        if algorithm == 'sha256':
            return hashlib.sha256(content).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(content).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def compute_file_hash(filepath: str, algorithm: str = 'sha256') -> str:
        """Dosya hash'i hesapla"""
        
        hasher = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    @staticmethod
    def verify_checksum(data: Any, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """Hash dogrula"""
        
        if isinstance(data, pd.DataFrame):
            actual_hash = DataChecksum.compute_dataframe_hash(data, algorithm)
        elif isinstance(data, np.ndarray):
            actual_hash = DataChecksum.compute_array_hash(data, algorithm)
        elif isinstance(data, str) and os.path.isfile(data):
            actual_hash = DataChecksum.compute_file_hash(data, algorithm)
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
        
        return actual_hash == expected_hash


# ============================================================================
# REPRODUCIBLE PIPELINE
# ============================================================================

@dataclass
class PipelineStep:
    """Pipeline adimi"""
    name: str
    function_name: str
    parameters: Dict[str, Any]
    input_hash: str
    output_hash: str
    duration_seconds: float
    timestamp: str


class ReproduciblePipeline:
    """
    Tekrarlanabilir Pipeline
    
    Tum adimlari kayit altina alir
    """
    
    def __init__(self, name: str, seed: int = 42):
        self.name = name
        self.seed = seed
        self.steps: List[PipelineStep] = []
        self.start_time = datetime.now()
        self.environment = EnvironmentCapture.capture()
        
        # Set seed
        set_reproducibility_seed(seed)
    
    def add_step(self, 
                 name: str,
                 function: Callable,
                 input_data: Any,
                 **kwargs) -> Any:
        """Pipeline adimi ekle ve calistir"""
        
        import time
        
        # Input hash
        if isinstance(input_data, pd.DataFrame):
            input_hash = DataChecksum.compute_dataframe_hash(input_data)
        elif isinstance(input_data, np.ndarray):
            input_hash = DataChecksum.compute_array_hash(input_data)
        else:
            input_hash = "N/A"
        
        # Execute
        start = time.time()
        result = function(input_data, **kwargs)
        duration = time.time() - start
        
        # Output hash
        if isinstance(result, pd.DataFrame):
            output_hash = DataChecksum.compute_dataframe_hash(result)
        elif isinstance(result, np.ndarray):
            output_hash = DataChecksum.compute_array_hash(result)
        else:
            output_hash = "N/A"
        
        # Record step
        step = PipelineStep(
            name=name,
            function_name=function.__name__,
            parameters=kwargs,
            input_hash=input_hash[:16],
            output_hash=output_hash[:16],
            duration_seconds=round(duration, 4),
            timestamp=datetime.now().isoformat()
        )
        
        self.steps.append(step)
        
        return result
    
    def get_pipeline_manifest(self) -> Dict[str, Any]:
        """Pipeline manifest'i olustur"""
        
        return {
            'name': self.name,
            'seed': self.seed,
            'start_time': self.start_time.isoformat(),
            'environment': asdict(self.environment),
            'steps': [asdict(step) for step in self.steps],
            'total_duration': sum(s.duration_seconds for s in self.steps)
        }
    
    def save_manifest(self, filepath: str = "pipeline_manifest.json"):
        """Manifest'i kaydet"""
        
        manifest = self.get_pipeline_manifest()
        
        with open(filepath, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return filepath
    
    def verify_reproducibility(self, other_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Baska bir manifest ile karsilastir"""
        
        current = self.get_pipeline_manifest()
        
        results = {
            'seed_match': current['seed'] == other_manifest.get('seed'),
            'steps_match': len(current['steps']) == len(other_manifest.get('steps', [])),
            'hash_matches': [],
            'reproducible': True
        }
        
        for i, (step1, step2) in enumerate(zip(current['steps'], other_manifest.get('steps', []))):
            hash_match = step1['output_hash'] == step2.get('output_hash')
            results['hash_matches'].append({
                'step': i + 1,
                'name': step1['name'],
                'match': hash_match
            })
            if not hash_match:
                results['reproducible'] = False
        
        return results


# ============================================================================
# REPRODUCIBILITY DECORATORS
# ============================================================================

def reproducible(seed: int = None):
    """Fonksiyonu reproducible yap"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if seed is not None:
                set_reproducibility_seed(seed)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_execution(log_file: str = "execution_log.jsonl"):
    """Fonksiyon calismasini logla"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            log_entry = {
                'function': func.__name__,
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': round(duration, 4),
                'args_count': len(args),
                'kwargs': list(kwargs.keys())
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            return result
        return wrapper
    return decorator


# ============================================================================
# VERSION CONTROL
# ============================================================================

class VersionControl:
    """
    Versiyon Kontrolu
    
    Kod ve veri versiyonlarini takip et
    """
    
    @staticmethod
    def get_git_info() -> Dict[str, Any]:
        """Git bilgilerini al"""
        
        info = {
            'available': False,
            'commit_hash': None,
            'branch': None,
            'dirty': None,
            'remote_url': None
        }
        
        try:
            import subprocess
            
            # Commit hash
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['commit_hash'] = result.stdout.strip()
                info['available'] = True
            
            # Branch
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['branch'] = result.stdout.strip()
            
            # Dirty status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['dirty'] = len(result.stdout.strip()) > 0
            
            # Remote URL
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info['remote_url'] = result.stdout.strip()
                
        except Exception:
            pass
        
        return info
    
    @staticmethod
    def generate_version_stamp() -> str:
        """Versiyon damgasi olustur"""
        
        git_info = VersionControl.get_git_info()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if git_info['available']:
            short_hash = git_info['commit_hash'][:8] if git_info['commit_hash'] else 'unknown'
            dirty = '_dirty' if git_info['dirty'] else ''
            return f"v{timestamp}_{short_hash}{dirty}"
        else:
            return f"v{timestamp}_nogit"


# ============================================================================
# REQUIREMENTS GENERATOR
# ============================================================================

class RequirementsGenerator:
    """
    Requirements Dosyasi Olusturucu
    
    Pip/conda uyumlu requirements dosyasi
    """
    
    CORE_PACKAGES = [
        'numpy', 'pandas', 'scipy', 'scikit-learn',
        'matplotlib', 'seaborn', 'plotly',
        'statsmodels', 'xgboost',
        'streamlit', 'requests',
        'sqlalchemy', 'psycopg2-binary',
        'reportlab', 'openpyxl'
    ]
    
    OPTIONAL_PACKAGES = [
        'torch', 'rdkit', 'biopython'
    ]
    
    @classmethod
    def generate_requirements_txt(cls, include_versions: bool = True) -> str:
        """requirements.txt icerigi olustur"""
        
        lines = [
            "# EpiClock v4.0 Requirements",
            "# Generated for reproducibility",
            f"# Date: {datetime.now().isoformat()}",
            ""
        ]
        
        for pkg in cls.CORE_PACKAGES:
            try:
                module = __import__(pkg.replace('-', '_'))
                version = getattr(module, '__version__', None)
                
                if include_versions and version:
                    lines.append(f"{pkg}=={version}")
                else:
                    lines.append(pkg)
            except ImportError:
                lines.append(f"# {pkg}  # not installed")
        
        lines.append("")
        lines.append("# Optional packages")
        
        for pkg in cls.OPTIONAL_PACKAGES:
            try:
                module = __import__(pkg)
                version = getattr(module, '__version__', None)
                
                if include_versions and version:
                    lines.append(f"# {pkg}=={version}")
                else:
                    lines.append(f"# {pkg}")
            except ImportError:
                lines.append(f"# {pkg}  # not installed")
        
        return "\n".join(lines)
    
    @classmethod
    def save_requirements(cls, filepath: str = "requirements_frozen.txt"):
        """Requirements dosyasini kaydet"""
        
        content = cls.generate_requirements_txt(include_versions=True)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def get_statistics() -> Dict[str, Any]:
    """Modul istatistikleri"""
    return {
        "module": "Reproducibility Infrastructure",
        "version": "1.0",
        "capabilities": {
            "seed_management": True,
            "environment_capture": True,
            "data_checksums": True,
            "pipeline_tracking": True,
            "version_control": True,
            "requirements_generation": True
        },
        "seed": SeedManager.get_seed(),
        "seed_initialized": SeedManager.is_initialized(),
        "references": [
            "Sandve et al. (2013) PLoS Comput Biol",
            "Peng (2011) Science"
        ]
    }


def ensure_reproducibility(seed: int = 42) -> Dict[str, Any]:
    """
    Tek fonksiyon ile tam reproducibility
    
    Args:
        seed: Global seed value
        
    Returns:
        Reproducibility report
    """
    
    # Set seed
    set_reproducibility_seed(seed)
    
    # Capture environment
    env = EnvironmentCapture.capture()
    
    # Get git info
    git_info = VersionControl.get_git_info()
    
    # Version stamp
    version = VersionControl.generate_version_stamp()
    
    return {
        'seed': seed,
        'version_stamp': version,
        'git_commit': git_info.get('commit_hash', 'N/A')[:8] if git_info.get('commit_hash') else 'N/A',
        'python_version': env.python_version.split()[0],
        'platform': env.platform,
        'timestamp': env.timestamp,
        'reproducibility_ready': True
    }


def test_reproducibility():
    """Test fonksiyonu"""
    
    print("=" * 80)
    print("REPRODUCIBILITY MODULE - TEST")
    print("=" * 80)
    
    # 1. Seed management
    print("\n[1] Seed Yonetimi:")
    set_reproducibility_seed(42)
    print(f"  Global seed: {SeedManager.get_seed()}")
    
    # Test determinism
    np.random.seed(42)
    arr1 = np.random.rand(5)
    np.random.seed(42)
    arr2 = np.random.rand(5)
    print(f"  Deterministic: {np.allclose(arr1, arr2)}")
    
    # 2. Environment capture
    print("\n[2] Ortam Yakalama:")
    env = EnvironmentCapture.capture()
    print(f"  Python: {env.python_version.split()[0]}")
    print(f"  Platform: {env.platform[:40]}...")
    print(f"  Packages: {len(env.packages)} tracked")
    
    # 3. Data checksums
    print("\n[3] Veri Checksum:")
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    hash1 = DataChecksum.compute_dataframe_hash(df)
    hash2 = DataChecksum.compute_dataframe_hash(df)
    print(f"  Hash tutarliligi: {hash1 == hash2}")
    print(f"  Hash (ilk 16): {hash1[:16]}")
    
    # 4. Pipeline
    print("\n[4] Reproducible Pipeline:")
    pipeline = ReproduciblePipeline("test_pipeline", seed=42)
    
    def normalize(x):
        return (x - x.mean()) / x.std()
    
    data = np.random.rand(100)
    result = pipeline.add_step("normalize", normalize, data)
    
    manifest = pipeline.get_pipeline_manifest()
    print(f"  Pipeline adimlari: {len(manifest['steps'])}")
    print(f"  Toplam sure: {manifest['total_duration']:.4f}s")
    
    # 5. Version control
    print("\n[5] Versiyon Kontrolu:")
    git_info = VersionControl.get_git_info()
    print(f"  Git mevcut: {git_info['available']}")
    if git_info['available']:
        print(f"  Commit: {git_info['commit_hash'][:8] if git_info['commit_hash'] else 'N/A'}")
        print(f"  Branch: {git_info['branch']}")
    
    version = VersionControl.generate_version_stamp()
    print(f"  Versiyon damgasi: {version}")
    
    # 6. Full reproducibility
    print("\n[6] Tam Reproducibility Raporu:")
    report = ensure_reproducibility(42)
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    return True


if __name__ == "__main__":
    test_reproducibility()
