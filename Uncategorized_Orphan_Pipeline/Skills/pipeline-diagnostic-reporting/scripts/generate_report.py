
from dataclasses import dataclass, field
from typing import List, Dict, Any
import json
import uuid
import random
import argparse
from enum import Enum

class Status(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    SKIPPED = "SKIPPED"

@dataclass
class StepResult:
    """Represents the result of a single pipeline step."""
    step_name: str
    status: Status
    duration_seconds: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticReport:
    """
    Defines the structured report for a pipeline run.
    This schema structurally enforces the presence of all required components.
    """
    pipeline_name: str
    run_id: str
    execution_status: Status
    successes: List[StepResult] = field(default_factory=list)
    failures: List[StepResult] = field(default_factory=list)
    actionable_recommendations: List[str] = field(default_factory=list)

    def to_json(self):
        """Serializes the report to a JSON string."""
        # Custom encoder to handle Enum objects
        class EnumEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Enum):
                    return obj.value
                return super().default(obj)
        return json.dumps(self.__dict__, cls=EnumEncoder, indent=2)

def generate_simulated_report(pipeline_name: str) -> DiagnosticReport:
    """
    Simulates a pipeline run and generates a diagnostic report.
    """
    run_id = str(uuid.uuid4())
    steps = [
        "Data Ingestion",
        "Data Validation",
        "Feature Engineering",
        "Model Training",
        "Model Evaluation",
        "Deployment Pre-check",
        "Model Deployment"
    ]
    
    report = DiagnosticReport(pipeline_name=pipeline_name, run_id=run_id, execution_status=Status.SUCCESS)

    for step_name in steps:
        # Simulate a random failure for demonstration
        if random.random() < 0.2 and step_name in ["Model Training", "Model Deployment"]:
            duration = round(random.uniform(5, 120), 2)
            result = StepResult(
                step_name=step_name,
                status=Status.FAILURE,
                duration_seconds=duration,
                details={"error_log": f"Error during {step_name.lower().replace(' ', '_')}. Check logs for details."}
            )
            report.failures.append(result)
            report.execution_status = Status.FAILURE # Mark the whole pipeline as failed
        else:
            duration = round(random.uniform(10, 300), 2)
            result = StepResult(
                step_name=step_name,
                status=Status.SUCCESS,
                duration_seconds=duration,
                details={"output_artifacts": f"/mnt/pipelines/data/{run_id}/{step_name.lower().replace(' ', '_')}.pkl"}
            )
            report.successes.append(result)

    # Generate recommendations based on failures
    if report.execution_status == Status.FAILURE:
        for failure in report.failures:
            if failure.step_name == "Model Training":
                report.actionable_recommendations.append("Investigate model training logs. The failure might be due to incompatible data shapes or resource exhaustion.")
            elif failure.step_name == "Model Deployment":
                report.actionable_recommendations.append("Check deployment environment configuration and permissions. Ensure the target service is healthy and has capacity.")
            else:
                report.actionable_recommendations.append(f"Review the logs for the failed step: '{failure.step_name}'.")

    if not report.actionable_recommendations and report.execution_status == Status.SUCCESS:
         report.actionable_recommendations.append("Pipeline executed successfully. No immediate action required.")

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Pipeline Diagnostic Report.")
    parser.add_argument("--pipeline-name", type=str, default="Sales-Forecasting-Q3", help="The name of the pipeline to simulate.")
    args = parser.parse_args()

    diagnostic_report = generate_simulated_report(args.pipeline_name)
    print(diagnostic_report.to_json())
