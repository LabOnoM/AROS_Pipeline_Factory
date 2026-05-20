## Bioinformatics Pipeline Design Policy Update

This policy outlines the updated guidelines for designing and implementing bioinformatics pipelines within the AROS ecosystem. All new and existing pipelines must adhere to these principles to ensure reproducibility, scalability, and data integrity. Key changes include enhanced data provenance tracking, mandatory containerization with Singularity or Docker, and integration with the AROS distributed computing framework. Special emphasis is placed on using standardized input/output formats and robust error handling mechanisms. This update aims to streamline development, reduce operational overhead, and improve the overall reliability of our bioinformatics analyses. Adherence to this policy is critical for all agents involved in biological data processing and analysis.

## Data Provenance and Containerization Standards

All bioinformatics pipelines must now implement strict data provenance tracking. This includes logging all input data sources, software versions, and configuration parameters used in each processing step. Containerization is mandatory for all pipeline components. Singularity containers are preferred for high-performance computing environments, while Docker can be used for local development and testing. Each container must include a manifest detailing its dependencies and build process. These standards ensure that every analytical result can be fully reproduced and audited, enhancing the scientific rigor of our research outcomes.

## Validation and Compliance Verification

Compliance with this Bioinformatics Pipeline Design Policy will be verified through regular audits of deployed pipelines. Verification steps include:
1.  **Code Review:** All new or updated pipeline code must undergo a peer review process to ensure adherence to containerization, provenance, and error handling standards.
2.  **Automated Testing:** Integration tests will be run against sample datasets to confirm functional correctness and adherence to standardized output formats.
3.  **Provenance Log Audits:** Periodic checks of provenance logs will be conducted to ensure complete and accurate tracking of data, software, and configuration.
4.  **Container Image Scans:** Automated security scans and dependency checks will be performed on all deployed container images.
Agents responsible for pipeline development and deployment are required to provide documentation demonstrating adherence to these validation criteria.
