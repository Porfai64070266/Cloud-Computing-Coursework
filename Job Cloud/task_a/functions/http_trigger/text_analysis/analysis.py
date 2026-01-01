from __future__ import annotations
import re
import statistics
from typing import List, Tuple, Dict, Set

SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+")
WORD_REGEX = re.compile(r"[A-Za-z']+")

def _normalize_text(text: str) -> str:
    return text.replace("\r", " ").strip()

def _extract_words(text: str) -> List[str]:
    return [w.lower() for w in WORD_REGEX.findall(text)]

def _split_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]

def analyze_word_frequency(text: str, stop_words: Set[str], top_n: int = 20) -> List[Tuple[str,int]]:
    words = _extract_words(_normalize_text(text))
    freq: Dict[str,int] = {}
    for w in words:
        if w in stop_words or w == "'":
            continue
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return ranked[:top_n]

def analyze_sentence_start_words(text: str, top_n: int = 10) -> List[Tuple[str,int]]:
    sentences = _split_sentences(_normalize_text(text))
    counts: Dict[str,int] = {}
    for s in sentences:
        cleaned = re.sub(r"^[\"'()\[\]]+", "", s).strip()
        first_match = WORD_REGEX.search(cleaned)
        if not first_match:
            continue
        first_word = first_match.group(0).lower()
        counts[first_word] = counts.get(first_word, 0) + 1
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return ranked[:top_n]

def analyze_sentence_length_distribution(text: str) -> Dict[str,float]:
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

STOP_WORDS = set([
"i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"
])
