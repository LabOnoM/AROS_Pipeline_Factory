
import enum
from dataclasses import dataclass, field
from typing import List, Optional

# GEPA Rule: Use enumerations to represent fixed choices for data types and designs.
# This prevents errors from typos and ensures inputs are from a controlled vocabulary.
class DataType(enum.Enum):
    """Enumeration for types of data variables."""
    CONTINUOUS = "continuous"
    ORDINAL = "ordinal"
    CATEGORICAL = "categorical"

class Design(enum.Enum):
    """Enumeration for experimental designs."""
    INDEPENDENT = "independent"
    PAIRED = "paired"
    REPEATED_MEASURES = "repeated_measures"
    ONE_SAMPLE = "one_sample"

@dataclass
class Recommendation:
    """Dataclass to hold the results of a recommendation."""
    primary_test: str
    non_parametric_alternative: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def __str__(self):
        output = f"Recommended Test: {self.primary_test}."
        if self.non_parametric_alternative:
            output += f"\nAlternative (non-parametric): {self.non_parametric_alternative}."
        for note in self.notes:
            output += f"\nNote: {note}"
        return output

def select_statistical_method(
    data_type: DataType,
    design: Design,
    num_groups: int = 2,
    is_association_test: bool = False
) -> Recommendation:
    """
    Implements the GEPA error prevention rule by routing experimental designs
    and data types to appropriate statistical tests.

    Args:
        data_type: The type of the dependent variable.
        design: The experimental design.
        num_groups: The number of groups being compared.
        is_association_test: Flag to indicate if testing for association between variables.

    Returns:
        A Recommendation object with the suggested statistical test.
    """
    # GEPA Rule: Explicit routing logic based on discrete inputs.
    # This prevents misapplication of statistical tests.

    # 1. Tests for Associations between two categorical variables
    if is_association_test and data_type == DataType.CATEGORICAL and design == Design.INDEPENDENT:
        notes = []
        if num_groups >= 2:
            notes.append("If cell counts are small (typically < 5), consider Fisher's Exact Test.")
            return Recommendation(
                primary_test="Chi-Square Test of Independence",
                notes=notes
            )

    # 2. Comparing groups based on data type
    if data_type == DataType.CONTINUOUS:
        if num_groups == 2:
            if design == Design.INDEPENDENT:
                return Recommendation(
                    primary_test="Independent Samples t-test",
                    non_parametric_alternative="Mann-Whitney U Test"
                )
            elif design in [Design.PAIRED, Design.REPEATED_MEASURES]:
                return Recommendation(
                    primary_test="Paired Samples t-test",
                    non_parametric_alternative="Wilcoxon Signed-Rank Test"
                )
        elif num_groups > 2:
            if design == Design.INDEPENDENT:
                return Recommendation(
                    primary_test="One-Way ANOVA",
                    non_parametric_alternative="Kruskal-Wallis Test"
                )
            elif design in [Design.PAIRED, Design.REPEATED_MEASURES]:
                return Recommendation(
                    primary_test="Repeated Measures ANOVA",
                    non_parametric_alternative="Friedman Test"
                )

    elif data_type == DataType.ORDINAL:
        if num_groups == 2:
            if design == Design.INDEPENDENT:
                return Recommendation(primary_test="Mann-Whitney U Test")
            elif design in [Design.PAIRED, Design.REPEATED_MEASURES]:
                return Recommendation(primary_test="Wilcoxon Signed-Rank Test")
        elif num_groups > 2:
            if design == Design.INDEPENDENT:
                return Recommendation(primary_test="Kruskal-Wallis Test")
            elif design in [Design.PAIRED, Design.REPEATED_MEASURES]:
                return Recommendation(primary_test="Friedman Test")

    # Default case if no specific rule matches
    return Recommendation(
        primary_test="No specific test found for this combination.",
        notes=["Please review the data type, experimental design, and number of groups.",
               "This combination may require a more specialized statistical model."]
    )

def main():
    """Main function to demonstrate the statistical method selection logic."""
    print("--- Statistical Method Selection Advisor ---")
    print("This script implements the GEPA error prevention rule by routing experimental designs to appropriate statistical tests.\n")

    # Example 1: Comparing blood pressure (continuous) between a treatment and control group (independent).
    print("Example 1: Comparing blood pressure (continuous) between a treatment and control group (independent).")
    rec1 = select_statistical_method(data_type=DataType.CONTINUOUS, design=Design.INDEPENDENT, num_groups=2)
    print(f"Recommendation: {rec1}\n")

    # Example 2: Comparing patient satisfaction scores (ordinal) for the same patients before and after treatment (paired).
    print("Example 2: Comparing patient satisfaction scores (ordinal) for the same patients before and after treatment (paired).")
    rec2 = select_statistical_method(data_type=DataType.ORDINAL, design=Design.PAIRED, num_groups=2)
    print(f"Recommendation: {rec2}\n")

    # Example 3: Testing for an association between two independent categorical variables (e.g., smoking status and lung cancer diagnosis).
    print("Example 3: Testing for an association between two independent categorical variables (e.g., smoking status and lung cancer diagnosis).")
    rec3 = select_statistical_method(data_type=DataType.CATEGORICAL, design=Design.INDEPENDENT, is_association_test=True)
    print(f"Recommendation: {rec3}\n")

    # Example 4: Comparing cholesterol levels (continuous) across three different drug dosage groups (independent).
    print("Example 4: Comparing cholesterol levels (continuous) across three different drug dosage groups (independent).")
    rec4 = select_statistical_method(data_type=DataType.CONTINUOUS, design=Design.INDEPENDENT, num_groups=3)
    print(f"Recommendation: {rec4}\n")

if __name__ == "__main__":
    main()
