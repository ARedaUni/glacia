import os
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Any


class VaultLoader:
    """Load secrets from Ansible Vault files"""
    
    def __init__(self, vault_file: str = "secrets.yml", password_file: str = ".vault_password"):
        self.vault_file = Path(vault_file)
        self.password_file = Path(password_file)
        
        # Make paths relative to the project root
        if not self.vault_file.is_absolute():
            # Assuming this file is in elysia/api/utils/, go up 3 levels to project root
            project_root = Path(__file__).parent.parent.parent.parent
            self.vault_file = project_root / vault_file
            
        if not self.password_file.is_absolute():
            project_root = Path(__file__).parent.parent.parent.parent
            self.password_file = project_root / password_file
    
    def load_secrets(self) -> Dict[str, Any]:
        """Load and decrypt secrets from Ansible Vault"""
        if not self.vault_file.exists():
            raise FileNotFoundError(f"Vault file not found: {self.vault_file}")
        
        if not self.password_file.exists():
            raise FileNotFoundError(f"Vault password file not found: {self.password_file}")
        
        try:
            # Use ansible-vault to decrypt the file
            result = subprocess.run([
                "ansible-vault", "view", str(self.vault_file),
                "--vault-password-file", str(self.password_file)
            ], capture_output=True, text=True, check=True)
            
            # Parse the YAML content
            secrets = yaml.safe_load(result.stdout)
            return secrets if secrets else {}
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to decrypt vault file: {e.stderr}")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Failed to parse vault YAML: {e}")
    
    def load_to_env(self) -> None:
        """Load secrets into environment variables"""
        secrets = self.load_secrets()
        
        for key, value in secrets.items():
            # Convert to uppercase for environment variable naming
            env_key = key.upper()
            os.environ[env_key] = str(value)


# Global vault loader instance
vault_loader = VaultLoader()


def load_secrets_from_vault() -> Dict[str, Any]:
    """Load secrets from vault - convenience function"""
    return vault_loader.load_secrets()


def setup_vault_env() -> None:
    """Load vault secrets into environment variables"""
    vault_loader.load_to_env()