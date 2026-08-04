import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from group_project.evaluation import eval_pipeline as ep
from src import task10_generation as t10

class P:
    def generate_with_citation(self, q, **k):
        return t10.generate_with_citation(q)

if __name__ == '__main__':
    G = P()
    DS = ep.load_golden_dataset()
    res = ep.evaluate_with_ragas(G, DS)
    comp = ep.compare_configs(G, DS)
    out = ep.export_results(res, comp)
    print('Wrote', out)
