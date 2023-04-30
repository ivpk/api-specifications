import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

import github_action_utils as gha_utils
import requests
import yaml
from dataclass_wizard import YAMLWizard


@dataclass
class Specification:
    """Represents an OpenAPI specification."""
    id: str
    label: str
    url: str


@dataclass
class Organization:
    """Represents an organization that provides OpenAPI specifications."""
    id: str
    label: str
    specifications: List[Specification]


@dataclass
class SpecificationsFile(YAMLWizard):
    """Represents a file containing a list of organizations with their OpenAPI specifications."""
    organizations: List[Organization]


def download_specification(url: str) -> str:
    """Downloads an OpenAPI specification from a given URL and returns its content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to download specification from {url}: {e}")


def parse_specification(spec: str) -> str:
    """Parses a given OpenAPI specification content and returns it in JSON format."""
    try:
        parsed_spec = yaml.safe_load(spec)
        return json.dumps(parsed_spec, indent=4)
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse specification: {e}")


def save_specification(spec: str, filepath: Path) -> None:
    """Saves a given OpenAPI specification content to a file at the given path."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(spec)
    except OSError as e:
        raise ValueError(f"Failed to save specification to {filepath}: {e}")


def download_format_and_save_specs(organizations: List[Organization]) -> None:
    """
    Downloads, formats and saves OpenAPI specifications for the given organizations.

    For each organization and its specifications, the function downloads the content
    of each specification, parses it and saves it in JSON format to a file with a name
    that includes the organization and specification IDs. If any errors occur during this
    process, a warning is logged.
    """
    for organization in organizations:
        for spec in organization.specifications:
            try:
                spec_content = download_specification(spec.url)
                validated_spec = parse_specification(spec_content)

                path = Path('../../') / 'openapi' / f'{organization.id}_{spec.id}.json'
                save_specification(validated_spec, path)

                gha_utils.debug(f"Saved specification for {organization.label}: {spec.label} ({path})")
            except (ValueError, requests.exceptions.RequestException, OSError) as exp:
                with gha_utils.group("Warnings while downloading, formatting and saving OpenApi specs"):
                    gha_utils.warning(str(exp), title="Warning")


if __name__ == "__main__":
    # Load the OpenAPI specifications file and extract the list of organizations.
    specifications_yaml_file = '../../specifications.json'
    parsed_specification_file = SpecificationsFile.from_yaml_file(specifications_yaml_file)

    # Download, format and save the OpenAPI specifications for the organizations.
    download_format_and_save_specs(parsed_specification_file.organizations)
