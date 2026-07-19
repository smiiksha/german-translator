from pydantic import BaseModel, Field


class GrammarError(BaseModel):
    type: str
    original_fragment: str
    corrected_fragment: str
    rule_violated: str
    explanation: str


class AnalysisResponse(BaseModel):
    original_german: str
    english_translation: str
    is_correct: bool
    errors: list[GrammarError] = Field(default_factory=list)
    corrected_sentence: str
    difficulty_level: str
    overall_explanation: str
    analysis_provider: str = "heuristic"
