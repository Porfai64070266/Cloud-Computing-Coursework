# Quick local test for analysis functions
from task_a.text_analysis.analysis import run_selected_analyses, STOP_WORDS
from pathlib import Path

if __name__ == '__main__':
    text = Path('sample_data/sample1.txt').read_text(encoding='utf-8')
    result = run_selected_analyses(text, STOP_WORDS, ["word_freq","sentence_starts","sentence_length"])
    print(result)
