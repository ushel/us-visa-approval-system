from dataclasses import dataclass

@dataclass
class DataInjectionArtifact:
    trained_file_path: str
    test_file_path:str