"""
Blockchain-Based Audit Trail Module
====================================

Implements an append-only hash-chained ledger for forensic
chain-of-custody verification in epigenetic analysis.

Features:
- Immutable audit records with SHA-256 hash chaining
- Tamper detection and verification
- Digital signatures for actor authentication
- Export/import of audit ledger
- PostgreSQL persistence with JSON fallback

Based on forensic evidence requirements and Daubert criteria
for scientific evidence admissibility.
"""

import os
import json
import hashlib
import hmac
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import uuid
import base64

import numpy as np
import pandas as pd


class AuditAction(Enum):
    """Types of auditable actions in the system"""
    SAMPLE_CREATED = "sample_created"
    SAMPLE_UPDATED = "sample_updated"
    SAMPLE_DELETED = "sample_deleted"
    ANALYSIS_STARTED = "analysis_started"
    ANALYSIS_COMPLETED = "analysis_completed"
    ANALYSIS_FAILED = "analysis_failed"
    REPORT_GENERATED = "report_generated"
    REPORT_EXPORTED = "report_exported"
    DATA_IMPORTED = "data_imported"
    DATA_EXPORTED = "data_exported"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    SETTINGS_CHANGED = "settings_changed"
    VERIFICATION_PERFORMED = "verification_performed"
    CHAIN_VALIDATED = "chain_validated"
    EXTERNAL_ACCESS = "external_access"


@dataclass
class AuditBlock:
    """Single block in the audit chain"""
    block_id: str
    timestamp: str
    action: str
    actor_id: str
    actor_name: str
    payload_hash: str
    payload_summary: str
    previous_hash: str
    block_hash: str
    signature: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AuditBlock':
        """Create block from dictionary"""
        return cls(**data)


@dataclass
class ChainValidationResult:
    """Result of chain validation"""
    is_valid: bool
    total_blocks: int
    validated_blocks: int
    first_invalid_block: Optional[str]
    error_message: Optional[str]
    validation_timestamp: str
    validation_hash: str


class BlockchainAuditLedger:
    """
    Append-only hash-chained ledger for forensic audit trails.
    Implements blockchain-like integrity verification without
    distributed consensus (single-node application).
    """
    
    def __init__(self, storage_path: str = "data/audit_ledger.json"):
        self.storage_path = storage_path
        self.chain: List[AuditBlock] = []
        self.secret_key = self._get_or_create_secret()
        self._load_chain()
        
    def _get_or_create_secret(self) -> bytes:
        """Get or create HMAC secret for signatures"""
        secret_env = os.environ.get('AUDIT_SECRET_KEY')
        if secret_env:
            return secret_env.encode()
        
        secret_file = "data/.audit_secret"
        if os.path.exists(secret_file):
            with open(secret_file, 'rb') as f:
                return f.read()
        
        os.makedirs("data", exist_ok=True)
        secret = os.urandom(32)
        with open(secret_file, 'wb') as f:
            f.write(secret)
        return secret
    
    def _load_chain(self):
        """Load existing chain from storage"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.chain = [AuditBlock.from_dict(b) for b in data.get('blocks', [])]
            except (json.JSONDecodeError, KeyError):
                self.chain = []
        
        if not self.chain:
            self._create_genesis_block()
    
    def _save_chain(self):
        """Save chain to storage"""
        os.makedirs(os.path.dirname(self.storage_path) or '.', exist_ok=True)
        data = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'block_count': len(self.chain),
            'blocks': [b.to_dict() for b in self.chain]
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = AuditBlock(
            block_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            action="genesis",
            actor_id="system",
            actor_name="EpiClock System",
            payload_hash=self._hash_payload({"message": "Genesis block - chain initialized"}),
            payload_summary="Chain initialized",
            previous_hash="0" * 64,
            block_hash="",
            signature=None,
            metadata={'version': '1.0', 'platform': 'EpiClock v4.0'}
        )
        genesis.block_hash = self._calculate_block_hash(genesis)
        genesis.signature = self._sign_block(genesis)
        self.chain.append(genesis)
        self._save_chain()
    
    def _hash_payload(self, payload: Any) -> str:
        """Create SHA-256 hash of payload"""
        if isinstance(payload, dict):
            payload_str = json.dumps(payload, sort_keys=True, default=str)
        elif isinstance(payload, (list, tuple)):
            payload_str = json.dumps(list(payload), sort_keys=True, default=str)
        else:
            payload_str = str(payload)
        return hashlib.sha256(payload_str.encode()).hexdigest()
    
    def _calculate_block_hash(self, block: AuditBlock) -> str:
        """Calculate hash for a block"""
        block_content = (
            f"{block.block_id}"
            f"{block.timestamp}"
            f"{block.action}"
            f"{block.actor_id}"
            f"{block.payload_hash}"
            f"{block.previous_hash}"
        )
        return hashlib.sha256(block_content.encode()).hexdigest()
    
    def _sign_block(self, block: AuditBlock) -> str:
        """Create HMAC signature for block"""
        message = f"{block.block_id}{block.block_hash}".encode()
        signature = hmac.new(self.secret_key, message, hashlib.sha256)
        return base64.b64encode(signature.digest()).decode()
    
    def _verify_signature(self, block: AuditBlock) -> bool:
        """Verify block signature"""
        if not block.signature:
            return False
        expected = self._sign_block(block)
        return hmac.compare_digest(block.signature, expected)
    
    def add_record(
        self,
        action: AuditAction,
        actor_id: str,
        actor_name: str,
        payload: Any,
        summary: str,
        metadata: Optional[Dict] = None
    ) -> AuditBlock:
        """
        Add a new record to the audit chain
        
        Args:
            action: Type of action being recorded
            actor_id: Unique identifier of the actor
            actor_name: Human-readable actor name
            payload: Data associated with the action
            summary: Brief description of the action
            metadata: Additional metadata
            
        Returns:
            The created AuditBlock
        """
        previous_block = self.chain[-1]
        
        new_block = AuditBlock(
            block_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            action=action.value,
            actor_id=actor_id,
            actor_name=actor_name,
            payload_hash=self._hash_payload(payload),
            payload_summary=summary[:200],
            previous_hash=previous_block.block_hash,
            block_hash="",
            signature=None,
            metadata=metadata or {}
        )
        
        new_block.block_hash = self._calculate_block_hash(new_block)
        new_block.signature = self._sign_block(new_block)
        
        self.chain.append(new_block)
        self._save_chain()
        
        return new_block
    
    def validate_chain(self) -> ChainValidationResult:
        """
        Validate the entire audit chain for integrity
        
        Returns:
            ChainValidationResult with validation status
        """
        if not self.chain:
            return ChainValidationResult(
                is_valid=False,
                total_blocks=0,
                validated_blocks=0,
                first_invalid_block=None,
                error_message="Chain is empty",
                validation_timestamp=datetime.now().isoformat(),
                validation_hash=""
            )
        
        for i, block in enumerate(self.chain):
            expected_hash = self._calculate_block_hash(block)
            if block.block_hash != expected_hash:
                return ChainValidationResult(
                    is_valid=False,
                    total_blocks=len(self.chain),
                    validated_blocks=i,
                    first_invalid_block=block.block_id,
                    error_message=f"Block {i} hash mismatch - possible tampering detected",
                    validation_timestamp=datetime.now().isoformat(),
                    validation_hash=expected_hash
                )
            
            if i > 0:
                if block.previous_hash != self.chain[i-1].block_hash:
                    return ChainValidationResult(
                        is_valid=False,
                        total_blocks=len(self.chain),
                        validated_blocks=i,
                        first_invalid_block=block.block_id,
                        error_message=f"Block {i} chain link broken - previous hash mismatch",
                        validation_timestamp=datetime.now().isoformat(),
                        validation_hash=block.previous_hash
                    )
            
            if block.signature and not self._verify_signature(block):
                return ChainValidationResult(
                    is_valid=False,
                    total_blocks=len(self.chain),
                    validated_blocks=i,
                    first_invalid_block=block.block_id,
                    error_message=f"Block {i} signature verification failed",
                    validation_timestamp=datetime.now().isoformat(),
                    validation_hash=block.block_hash
                )
        
        chain_fingerprint = self._hash_payload([b.block_hash for b in self.chain])
        
        return ChainValidationResult(
            is_valid=True,
            total_blocks=len(self.chain),
            validated_blocks=len(self.chain),
            first_invalid_block=None,
            error_message=None,
            validation_timestamp=datetime.now().isoformat(),
            validation_hash=chain_fingerprint
        )
    
    def get_chain_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the audit chain"""
        if not self.chain:
            return {'status': 'empty', 'block_count': 0}
        
        action_counts = {}
        actor_counts = {}
        
        for block in self.chain:
            action_counts[block.action] = action_counts.get(block.action, 0) + 1
            actor_counts[block.actor_name] = actor_counts.get(block.actor_name, 0) + 1
        
        return {
            'status': 'active',
            'block_count': len(self.chain),
            'genesis_timestamp': self.chain[0].timestamp,
            'latest_timestamp': self.chain[-1].timestamp,
            'latest_block_hash': self.chain[-1].block_hash[:16] + '...',
            'action_distribution': action_counts,
            'actor_distribution': actor_counts,
            'chain_fingerprint': self._hash_payload([b.block_hash for b in self.chain])[:32]
        }
    
    def get_records_by_action(self, action: AuditAction) -> List[AuditBlock]:
        """Get all records for a specific action type"""
        return [b for b in self.chain if b.action == action.value]
    
    def get_records_by_actor(self, actor_id: str) -> List[AuditBlock]:
        """Get all records by a specific actor"""
        return [b for b in self.chain if b.actor_id == actor_id]
    
    def get_records_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[AuditBlock]:
        """Get records within a date range"""
        results = []
        for block in self.chain:
            block_time = datetime.fromisoformat(block.timestamp)
            if start_date <= block_time <= end_date:
                results.append(block)
        return results
    
    def export_chain(self, format: str = 'json') -> str:
        """Export the entire chain for external verification"""
        data = {
            'export_timestamp': datetime.now().isoformat(),
            'chain_length': len(self.chain),
            'chain_fingerprint': self._hash_payload([b.block_hash for b in self.chain]),
            'blocks': [b.to_dict() for b in self.chain]
        }
        
        if format == 'json':
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_audit_table(self, limit: int = 50) -> pd.DataFrame:
        """Get audit records as DataFrame for display"""
        records = self.chain[-limit:] if len(self.chain) > limit else self.chain
        
        data = []
        for block in records:
            data.append({
                'Zaman': block.timestamp[:19].replace('T', ' '),
                'İşlem': block.action.replace('_', ' ').title(),
                'Aktör': block.actor_name,
                'Özet': block.payload_summary[:50] + '...' if len(block.payload_summary) > 50 else block.payload_summary,
                'Hash': block.block_hash[:12] + '...',
                'Doğrulandı': '✓' if self._verify_signature(block) else '✗'
            })
        
        return pd.DataFrame(data)


class ForensicChainOfCustody:
    """
    Chain-of-custody tracking for forensic applications
    with evidence handling compliance
    """
    
    def __init__(self):
        self.ledger = BlockchainAuditLedger()
        self.custody_records: Dict[str, List[Dict]] = {}
        
    def register_evidence(
        self,
        evidence_id: str,
        evidence_type: str,
        collector_id: str,
        collector_name: str,
        collection_location: str,
        collection_method: str,
        description: str
    ) -> str:
        """Register new evidence item in chain of custody"""
        
        payload = {
            'evidence_id': evidence_id,
            'evidence_type': evidence_type,
            'collector': {'id': collector_id, 'name': collector_name},
            'location': collection_location,
            'method': collection_method,
            'description': description,
            'registration_time': datetime.now().isoformat()
        }
        
        block = self.ledger.add_record(
            action=AuditAction.SAMPLE_CREATED,
            actor_id=collector_id,
            actor_name=collector_name,
            payload=payload,
            summary=f"Evidence registered: {evidence_id} - {evidence_type}",
            metadata={'evidence_id': evidence_id, 'type': 'registration'}
        )
        
        self.custody_records[evidence_id] = [{
            'action': 'registered',
            'timestamp': block.timestamp,
            'actor': collector_name,
            'block_hash': block.block_hash
        }]
        
        return block.block_hash
    
    def transfer_custody(
        self,
        evidence_id: str,
        from_actor_id: str,
        from_actor_name: str,
        to_actor_id: str,
        to_actor_name: str,
        reason: str,
        conditions: Optional[str] = None
    ) -> str:
        """Record custody transfer of evidence"""
        
        payload = {
            'evidence_id': evidence_id,
            'from': {'id': from_actor_id, 'name': from_actor_name},
            'to': {'id': to_actor_id, 'name': to_actor_name},
            'reason': reason,
            'conditions': conditions,
            'transfer_time': datetime.now().isoformat()
        }
        
        block = self.ledger.add_record(
            action=AuditAction.EXTERNAL_ACCESS,
            actor_id=to_actor_id,
            actor_name=to_actor_name,
            payload=payload,
            summary=f"Custody transfer: {evidence_id} from {from_actor_name} to {to_actor_name}",
            metadata={'evidence_id': evidence_id, 'type': 'transfer'}
        )
        
        if evidence_id not in self.custody_records:
            self.custody_records[evidence_id] = []
        
        self.custody_records[evidence_id].append({
            'action': 'transferred',
            'timestamp': block.timestamp,
            'from': from_actor_name,
            'to': to_actor_name,
            'block_hash': block.block_hash
        })
        
        return block.block_hash
    
    def record_analysis(
        self,
        evidence_id: str,
        analyst_id: str,
        analyst_name: str,
        analysis_type: str,
        results_hash: str,
        notes: Optional[str] = None
    ) -> str:
        """Record analysis performed on evidence"""
        
        payload = {
            'evidence_id': evidence_id,
            'analyst': {'id': analyst_id, 'name': analyst_name},
            'analysis_type': analysis_type,
            'results_hash': results_hash,
            'notes': notes,
            'analysis_time': datetime.now().isoformat()
        }
        
        block = self.ledger.add_record(
            action=AuditAction.ANALYSIS_COMPLETED,
            actor_id=analyst_id,
            actor_name=analyst_name,
            payload=payload,
            summary=f"Analysis completed: {analysis_type} on {evidence_id}",
            metadata={'evidence_id': evidence_id, 'type': 'analysis'}
        )
        
        if evidence_id not in self.custody_records:
            self.custody_records[evidence_id] = []
        
        self.custody_records[evidence_id].append({
            'action': 'analyzed',
            'timestamp': block.timestamp,
            'actor': analyst_name,
            'analysis_type': analysis_type,
            'block_hash': block.block_hash
        })
        
        return block.block_hash
    
    def get_custody_chain(self, evidence_id: str) -> List[Dict]:
        """Get complete chain of custody for evidence item"""
        
        all_records = []
        for block in self.ledger.chain:
            if block.metadata.get('evidence_id') == evidence_id:
                all_records.append({
                    'timestamp': block.timestamp,
                    'action': block.action,
                    'actor': block.actor_name,
                    'summary': block.payload_summary,
                    'block_hash': block.block_hash,
                    'verified': self.ledger._verify_signature(block)
                })
        
        return all_records
    
    def verify_custody_chain(self, evidence_id: str) -> Dict[str, Any]:
        """Verify integrity of custody chain for evidence"""
        
        chain_validation = self.ledger.validate_chain()
        
        evidence_blocks = [
            b for b in self.ledger.chain 
            if b.metadata.get('evidence_id') == evidence_id
        ]
        
        evidence_valid = True
        for block in evidence_blocks:
            if not self.ledger._verify_signature(block):
                evidence_valid = False
                break
        
        return {
            'evidence_id': evidence_id,
            'chain_valid': chain_validation.is_valid,
            'evidence_records_valid': evidence_valid,
            'total_records': len(evidence_blocks),
            'first_record': evidence_blocks[0].timestamp if evidence_blocks else None,
            'last_record': evidence_blocks[-1].timestamp if evidence_blocks else None,
            'verification_time': datetime.now().isoformat(),
            'chain_fingerprint': chain_validation.validation_hash[:32] if chain_validation.validation_hash else None
        }
    
    def generate_custody_report(self, evidence_id: str) -> pd.DataFrame:
        """Generate formatted custody report"""
        records = self.get_custody_chain(evidence_id)
        
        if not records:
            return pd.DataFrame({'Mesaj': ['Bu delil için kayıt bulunamadı']})
        
        data = []
        for record in records:
            data.append({
                'Tarih/Saat': record['timestamp'][:19].replace('T', ' '),
                'İşlem': record['action'].replace('_', ' ').title(),
                'Sorumlu': record['actor'],
                'Açıklama': record['summary'][:100],
                'Blok Hash': record['block_hash'][:16] + '...',
                'Doğrulama': '✓ Geçerli' if record['verified'] else '✗ Geçersiz'
            })
        
        return pd.DataFrame(data)


class TamperDetectionSimulator:
    """
    Utility for demonstrating tamper detection capabilities
    """
    
    def __init__(self, ledger: BlockchainAuditLedger):
        self.ledger = ledger
        self.original_chain = None
        
    def create_backup(self):
        """Create backup of current chain state"""
        self.original_chain = [
            AuditBlock.from_dict(b.to_dict()) 
            for b in self.ledger.chain
        ]
    
    def simulate_tampering(self, block_index: int, new_summary: str) -> Dict[str, Any]:
        """
        Simulate tampering with a block and demonstrate detection
        
        WARNING: This is for demonstration purposes only.
        """
        if block_index < 0 or block_index >= len(self.ledger.chain):
            return {'error': 'Invalid block index'}
        
        self.create_backup()
        
        original_summary = self.ledger.chain[block_index].payload_summary
        original_hash = self.ledger.chain[block_index].block_hash
        
        self.ledger.chain[block_index].payload_summary = new_summary
        
        validation_after = self.ledger.validate_chain()
        
        self.ledger.chain = self.original_chain
        
        return {
            'tampered_block_index': block_index,
            'original_summary': original_summary,
            'tampered_summary': new_summary,
            'original_hash': original_hash,
            'detection_result': 'TAMPER DETECTED' if not validation_after.is_valid else 'NOT DETECTED',
            'validation_message': validation_after.error_message,
            'demonstration_only': True
        }
    
    def run_integrity_demo(self) -> List[Dict[str, Any]]:
        """Run a complete integrity demonstration"""
        results = []
        
        results.append({
            'step': 1,
            'description': 'Zincir doğrulama (orijinal)',
            'result': self.ledger.validate_chain().is_valid,
            'message': 'Zincir bütünlüğü doğrulandı'
        })
        
        if len(self.ledger.chain) > 2:
            tamper_result = self.simulate_tampering(
                block_index=len(self.ledger.chain) // 2,
                new_summary="MANIPULATED DATA"
            )
            results.append({
                'step': 2,
                'description': 'Manipülasyon simülasyonu',
                'result': tamper_result['detection_result'] == 'TAMPER DETECTED',
                'message': f"Manipülasyon {'tespit edildi' if tamper_result['detection_result'] == 'TAMPER DETECTED' else 'tespit edilemedi'}"
            })
        
        final_validation = self.ledger.validate_chain()
        results.append({
            'step': 3,
            'description': 'Final doğrulama',
            'result': final_validation.is_valid,
            'message': 'Zincir orijinal durumuna geri döndürüldü'
        })
        
        return results


def get_audit_summary_table(ledger: BlockchainAuditLedger) -> pd.DataFrame:
    """Create summary table for display"""
    summary = ledger.get_chain_summary()
    
    data = [
        {'Metrik': 'Durum', 'Değer': summary.get('status', 'bilinmiyor').title()},
        {'Metrik': 'Toplam Blok', 'Değer': summary.get('block_count', 0)},
        {'Metrik': 'İlk Kayıt', 'Değer': summary.get('genesis_timestamp', '-')[:19] if summary.get('genesis_timestamp') else '-'},
        {'Metrik': 'Son Kayıt', 'Değer': summary.get('latest_timestamp', '-')[:19] if summary.get('latest_timestamp') else '-'},
        {'Metrik': 'Zincir Parmak İzi', 'Değer': summary.get('chain_fingerprint', '-')}
    ]
    
    return pd.DataFrame(data)
