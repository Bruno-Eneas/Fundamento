"""Modos *exclusivamente demonstrativos*, nunca acesso a pacientes reais.

A execução local de apresentação usa localhost. A vitrine pública é
somente leitura e contém apenas dados fictícios.
"""
import os


def mode():
    """Retorna 'local', 'publico' ou None."""
    if os.environ.get('FUNDAMENTO_PUBLIC_SHOWCASE') == '1':
        return 'publico'
    if os.environ.get('FUNDAMENTO_PRESENTATION_MODE') == '1':
        return 'local'
    return None


def sample_account(role):
    """Identidade de vitrine, sem autenticação; usar apenas quando mode() ativo."""
    if role == 'doctor':
        return {'login': 'MED-DEMO', 'role': 'doctor', 'patient_id': None}
    if role == 'patient':
        return {'login': 'DEMO-001', 'role': 'patient', 'patient_id': 'DEMO-001'}
    raise ValueError('Papel demonstrativo inválido.')
