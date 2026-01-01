"""Core text analysis functions for Task A1.

Functions:
    analyze_word_frequency(text: str, stop_words: set[str], top_n: int = 20) -> list[tuple[str,int]]
    analyze_sentence_start_words(text: str, top_n: int = 10) -> list[tuple[str,int]]
    analyze_sentence_length_distribution(text: str) -> dict[str,float|int]
    run_selected_analyses(text: str, stop_words: set[str], modes: list[str]) -> dict

All tokenization kept simple & transparent for coursework explanation.
"""
from __future__ import annotations
import re
import statistics
from typing import List, Tuple, Dict, Set

SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+")
WORD_REGEX = re.compile(r"[A-Za-z']+")

# Fallback: if NLTK not allowed, we keep manual simple splitting.

def _normalize_text(text: str) -> str:
    return text.replace("\r", " ").strip()

def _extract_words(text: str) -> List[str]:
    return [w.lower() for w in WORD_REGEX.findall(text)]

def _split_sentences(text: str) -> List[str]:
    # Split on period/question/exclamation boundaries while preserving basic sentence content.
    # Use regex with lookbehind for punctuation followed by whitespace.
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    # Filter out empty strings
    return [s.strip() for s in sentences if s.strip()]

def analyze_word_frequency(text: str, stop_words: Set[str], top_n: int = 20) -> List[Tuple[str,int]]:
    """Return top N words excluding given stop words.

    Steps:
        1. Extract words via regex (letters & apostrophes).
        2. Lowercase all words.
        3. Filter out stop words and purely apostrophe artifacts.
        4. Count using dict.
        5. Sort by frequency desc then alphabet asc for determinism.
    """
    words = _extract_words(_normalize_text(text))
    freq: Dict[str,int] = {}
    for w in words:
        if w in stop_words or w == "'":
            continue
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return ranked[:top_n]

def analyze_sentence_start_words(text: str, top_n: int = 10) -> List[Tuple[str,int]]:
    """Return the most common first words starting sentences.

    Sentence detection is naive: split on punctuation (.!?).
    Leading quotes or parentheses removed. Not excluding stop words by spec.
    """
    sentences = _split_sentences(_normalize_text(text))
    counts: Dict[str,int] = {}
    for s in sentences:
        # Remove leading quotes/brackets
        cleaned = re.sub(r"^[\"'()\[\]]+", "", s).strip()
        first_match = WORD_REGEX.search(cleaned)
        if not first_match:
            continue
        first_word = first_match.group(0).lower()
        counts[first_word] = counts.get(first_word, 0) + 1
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return ranked[:top_n]

def analyze_sentence_length_distribution(text: str) -> Dict[str,float]:
    """Compute mean, median, stdev of sentence lengths (in words).

    Use statistics module; stdev requires >=2 sentences else 0.0.
    """
    sentences = _split_sentences(_normalize_text(text))
    lengths = []
    for s in sentences:
        words = _extract_words(s)
        if words:
            lengths.append(len(words))
    if not lengths:
        return {"mean": 0.0, "median": 0.0, "stdev": 0.0, "count": 0}
    mean = statistics.mean(lengths)
    median = statistics.median(lengths)
    stdev = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    return {"mean": mean, "median": median, "stdev": stdev, "count": len(lengths)}

VALID_MODES = {"word_freq", "sentence_starts", "sentence_length"}

def run_selected_analyses(text: str, stop_words: Set[str], modes: List[str]) -> Dict:
    """Run chosen analyses and combine results.

    modes: list of identifiers among VALID_MODES.
    """
    results = {}
    for m in modes:
        if m == "word_freq":
            results[m] = analyze_word_frequency(text, stop_words)
        elif m == "sentence_starts":
            results[m] = analyze_sentence_start_words(text)
        elif m == "sentence_length":
            results[m] = analyze_sentence_length_distribution(text)
    return results

STOP_WORDS = set([
"i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"
])

if __name__ == "__main__":
    sample = "Hello world! This is a simple test. Testing sentence starts. Hello again?"
    print(run_selected_analyses(sample, STOP_WORDS, ["word_freq","sentence_starts","sentence_length"]))
