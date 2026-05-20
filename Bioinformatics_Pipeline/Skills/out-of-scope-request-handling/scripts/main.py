# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import re

def parse_skill_metadata(skill_md_path):
    """Parses the name and description from a SKILL.md file's front matter."""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Use regex to find the YAML front matter between --- tags
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None, None

        front_matter = match.group(1)
        name = None
        description = None

        for line in front_matter.split('\n'):
            if line.startswith('name:'):
                name = line.split(':', 1)[1].strip()
            elif line.startswith('description:'):
                description = line.split(':', 1)[1].strip()

        return name, description
    except FileNotFoundError:
        return None, None
    except Exception:
        # Gracefully handle any parsing errors
        return None, None


def get_available_skills():
    """Scans the skills directory and returns a dictionary of available skills."""
    skills_dir = os.path.expanduser('~/.gemini/skills/')
    supported_functions = {}

    if not os.path.isdir(skills_dir):
        return supported_functions

    for skill_dir_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_dir_name)
        if os.path.isdir(skill_path):
            skill_md_path = os.path.join(skill_path, 'SKILL.md')
            name, description = parse_skill_metadata(skill_md_path)
            if name and description:
                supported_functions[name] = description

    return supported_functions


def generate_fallback_message(user_request="your request"):
    """
    Generates a graceful fallback message listing available skills.

    This function is the core of the out-of-scope request handling.
    It simulates the failure to map a user request and provides a helpful
    list of alternatives.
    """
    skills = get_available_skills()

    if not skills:
        return "I am sorry, but I could not process your request. Furthermore, I was unable to retrieve a list of my available capabilities."

    message = f"I'm sorry, I cannot process '{user_request}' as it does not match any of my currently supported functions.\n\n"
    message += "Here is a list of my available capabilities:\n\n"

    # Sort skills by name for consistent output
    for name, desc in sorted(skills.items()):
        message += f"- **{name}**: {desc}\n"

    message += "\nPlease try rephrasing your request to align with one of the functions listed above, or ask your administrator to install a new skill."

    return message

if __name__ == "__main__":
    # This block simulates the script being called when a user request is determined
    # to be out of scope. The 'simulated_user_request' would be the actual
    # user query in a real-world scenario.
    simulated_user_request = "Can you order a pizza for me?"
    print(generate_fallback_message(simulated_user_request))
