class QuantumTechError(Exception):
    pass

class DatosInvalidosError(QuantumTechError):
    pass

class EquipoNoAptoError(QuantumTechError):
    pass

class CertificacionInvalidaError(QuantumTechError):
    pass

class TransicionInvalidaError(QuantumTechError):
    pass

class InspeccionNoDisponibleError(QuantumTechError):
    pass
class ArchivoInvalidoError(QuantumTechError):
    pass