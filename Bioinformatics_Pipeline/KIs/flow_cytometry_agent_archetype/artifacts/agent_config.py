# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# AROS Agent Archetype Configuration
# File: ~/.gemini/antigravity/knowledge/flow_cytometry_agent_archetype/artifacts/agent_config.py

AGENT_ARCHETYPE = {
    'name': 'flow_cytometry_specialist',
    'description': (
        'An agent archetype specializing in flow cytometry (FACS) data analysis and '
        'computational simulation. It performs gating, compensation, visualization, and '
        'generates synthetic FCS data using the FlowCyPy physics engine.'
    ),
    'category': 'Bioinformatics',
    'author': 'AROS-GEPA-System',

    # -- Core Skills & Tool Bindings --
    # Defines the set of capabilities this agent can reliably execute.
    'skills': [
        {
            'name': 'flowcypy',
            'description': 'For simulating virtual flow cytometry experiments and modeling hardware.'
        },
        {
            'name': 'facs-gating-viz-style',
            'description': 'For creating publication-quality visualizations of gating strategies.'
        },
        {
            'name': 'dynamic-plot-code-generation',
            'description': 'For dynamically generating Python plotting code tailored to the data.'
        },
        # General purpose skills for file handling and execution
        {
            'name': 'core.file_system',
            'description': 'For reading and writing FCS files, simulation scripts, and plot outputs.'
        },
        {
            'name': 'core.code_interpreter',
            'description': 'For executing Python scripts for data analysis and simulation.'
        }
    ],

    # -- System Prompt --
    # The full system prompt is loaded from the adjacent markdown file.
    'system_prompt_file': 'system_prompt.md',

    # -- Knowledge & Grounding --
    # This agent should be grounded in knowledge related to immunology, cell biology,
    # and optics to better fulfill GEPA-Rule-BIO-003.
    'knowledge_dependencies': [
        'ki-immunology-markers',
        'ki-optics-fundamentals',
        'ki-cell-biology-basics'
    ]
}

def get_archetype_config():
    """Returns the agent archetype configuration dictionary."""
    return AGENT_ARCHETYPE

