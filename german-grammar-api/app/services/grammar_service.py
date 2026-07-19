import json
import re

from app.core.config import get_settings
from app.schemas.response_schemas import AnalysisResponse, GrammarError
from app.services.translation_service import translate_to_english


def _heuristic_analysis(text: str) -> AnalysisResponse:
    errors: list[GrammarError] = []
    corrected = text.strip()
    # German preposition "mit" always governs the dative. This covers a common learner error.
    match = re.search(r"\bmit den (Mann|Kind|Hund)\b", corrected, re.IGNORECASE)
    if match:
        original = match.group(0)
        noun = match.group(1)
        replacement = f"mit dem {noun}"
        corrected = corrected[:match.start()] + replacement + corrected[match.end():]
        errors.append(GrammarError(
            type="case_error", original_fragment=original, corrected_fragment=replacement,
            rule_violated="Dative after 'mit'",
            explanation="The preposition 'mit' always requires the dative case.",
        ))
    if re.search(r"\bIch sein\b", corrected, re.IGNORECASE):
        errors.append(GrammarError(
            type="verb_conjugation", original_fragment="Ich sein", corrected_fragment="Ich bin",
            rule_violated="Conjugation of sein", explanation="With 'ich', the verb 'sein' is conjugated as 'bin'.",
        ))
        corrected = re.sub(r"\bIch sein\b", "Ich bin", corrected, flags=re.IGNORECASE)

    return AnalysisResponse(
        original_german=text,
        english_translation=translate_to_english(text),
        is_correct=not errors,
        errors=errors,
        corrected_sentence=corrected,
        difficulty_level="A2" if errors else "A1",
        overall_explanation=("No grammar issues found by the offline checker." if not errors
                             else "The sentence contains grammar issues. See the error list for corrections."),
        analysis_provider="heuristic",
    )


def analyze_grammar(text: str) -> AnalysisResponse:
    """Use OpenAI structured JSON when configured; otherwise run reliable local rules."""
    settings = get_settings()
    if not settings.openai_api_key:
        return _heuristic_analysis(text)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = '''Analyze this German learner text. Return JSON only with keys:
original_german, english_translation, is_correct, errors, corrected_sentence,
difficulty_level, overall_explanation. Each error needs type, original_fragment,
corrected_fragment, rule_violated, explanation. Check cases, articles, adjective
endings, conjugation, verb placement, and word order. Text: ''' + text
        result = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "system", "content": "You are a precise German grammar tutor."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}, temperature=0,
        )
        data = json.loads(result.choices[0].message.content or "{}")
        data["analysis_provider"] = "openai"
        return AnalysisResponse.model_validate(data)
    except Exception:
        return _heuristic_analysis(text)
