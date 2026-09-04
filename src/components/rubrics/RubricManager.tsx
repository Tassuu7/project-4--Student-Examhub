import React, { useState } from 'react';
import {
  ListChecks,
  Plus,
  Trash2,
  CheckCircle2,
  Users,
  BarChart2,
  AlertTriangle,
  Scale,
  Sparkles
} from 'lucide-react';

interface Level {
  id: string;
  name: string;
  points: number;
  description: string;
}

interface Criterion {
  id: string;
  title: string;
  weight: number;
  levels: Level[];
}

export const RubricManager: React.FC = () => {
  const [rubricTitle, setRubricTitle] = useState('Software Engineering Capstone Design Rubric');
  const [activeTab, setActiveTab] = useState<'designer' | 'inter_rater'>('designer');

  const [criteria, setCriteria] = useState<Criterion[]>([
    {
      id: 'crit-1',
      title: 'Distributed System Architecture & Modularity',
      weight: 1.5,
      levels: [
        { id: 'l1', name: 'Exemplary', points: 20, description: 'Microservices decoupled via asynchronous message bus, strict failure domain boundaries.' },
        { id: 'l2', name: 'Proficient', points: 15, description: 'Clear separation of concerns with minor coupling in shared persistence stores.' },
        { id: 'l3', name: 'Developing', points: 10, description: 'Monolithic leakage, synchronous inter-service blocking calls.' },
        { id: 'l4', name: 'Novice', points: 5, description: 'Single monolithic executable with global mutable shared state.' }
      ]
    },
    {
      id: 'crit-2',
      title: 'Automated Test Coverage & Verification',
      weight: 1.0,
      levels: [
        { id: 'l1', name: 'Exemplary', points: 20, description: 'Over 85% branch coverage with unit, integration, and end-to-end regression suites.' },
        { id: 'l2', name: 'Proficient', points: 15, description: 'Comprehensive unit tests (70-85% coverage), lacking stress/chaos tests.' },
        { id: 'l3', name: 'Developing', points: 10, description: 'Sparse happy-path test cases only, missing error boundary tests.' },
        { id: 'l4', name: 'Novice', points: 5, description: 'Zero automated test cases.' }
      ]
    }
  ]);

  const [kappaStats, setKappaStats] = useState({
    cohensKappa: 0.74,
    fleissKappa: 0.68,
    agreementLabel: 'Substantial Agreement',
    numSubmissions: 30,
    numRaters: 3,
    flaggedDiscrepancies: 2
  });

  const handleAddCriterion = () => {
    const newCrit: Criterion = {
      id: `crit-${Date.now()}`,
      title: 'New Evaluation Criterion',
      weight: 1.0,
      levels: [
        { id: 'l1', name: 'Exemplary', points: 20, description: 'Demonstrates mastery of criterion.' },
        { id: 'l2', name: 'Proficient', points: 15, description: 'Satisfies primary standards.' },
        { id: 'l3', name: 'Developing', points: 10, description: 'Partial fulfillment with minor errors.' },
        { id: 'l4', name: 'Novice', points: 5, description: 'Fails to meet basic expectations.' }
      ]
    };
    setCriteria([...criteria, newCrit]);
  };

  const handleRemoveCriterion = (id: string) => {
    setCriteria(criteria.filter((c) => c.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Top Bar */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Scale className="w-4 h-4" />
            <span>Grading Calibration & Consensus</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Analytic Rubrics & Inter-Rater Reliability
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Standardize subjective essay and project grading across multiple faculty evaluators.
          </p>
        </div>

        <div className="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('designer')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              activeTab === 'designer'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            Rubric Builder
          </button>
          <button
            onClick={() => setActiveTab('inter_rater')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              activeTab === 'inter_rater'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            Inter-Rater Consensus (κ)
          </button>
        </div>
      </div>

      {activeTab === 'designer' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Rubric Title
              </label>
              <input
                type="text"
                value={rubricTitle}
                onChange={(e) => setRubricTitle(e.target.value)}
                className="w-full text-base font-bold p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            {criteria.map((crit, cIdx) => (
              <div
                key={crit.id}
                className="p-5 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/30 space-y-4"
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-3 flex-1 mr-4">
                    <span className="text-xs font-bold text-gray-400">#{cIdx + 1}</span>
                    <input
                      type="text"
                      value={crit.title}
                      onChange={(e) => {
                        const updated = [...criteria];
                        updated[cIdx].title = e.target.value;
                        setCriteria(updated);
                      }}
                      className="text-sm font-semibold p-1.5 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white flex-1"
                    />
                    <div className="flex items-center space-x-1 shrink-0">
                      <span className="text-xs text-gray-500">Weight:</span>
                      <input
                        type="number"
                        step="0.1"
                        value={crit.weight}
                        onChange={(e) => {
                          const updated = [...criteria];
                          updated[cIdx].weight = parseFloat(e.target.value) || 1.0;
                          setCriteria(updated);
                        }}
                        className="w-16 text-xs p-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-center font-mono"
                      />
                    </div>
                  </div>

                  <button
                    onClick={() => handleRemoveCriterion(crit.id)}
                    className="p-1.5 text-gray-400 hover:text-red-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  {crit.levels.map((lvl, lIdx) => (
                    <div
                      key={lvl.id}
                      className="p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 text-xs space-y-2"
                    >
                      <div className="flex justify-between items-center font-bold">
                        <span className="text-indigo-600 dark:text-indigo-400">{lvl.name}</span>
                        <span className="font-mono text-gray-700 dark:text-gray-300">{lvl.points} pts</span>
                      </div>
                      <textarea
                        value={lvl.description}
                        onChange={(e) => {
                          const updated = [...criteria];
                          updated[cIdx].levels[lIdx].description = e.target.value;
                          setCriteria(updated);
                        }}
                        rows={3}
                        className="w-full text-xs p-1.5 rounded border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 resize-none"
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div className="flex justify-between items-center pt-2">
              <button
                onClick={handleAddCriterion}
                className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-lg border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 text-xs font-semibold"
              >
                <Plus className="w-4 h-4" />
                <span>Add Criterion</span>
              </button>

              <button className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm">
                Save Rubric Definition
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'inter_rater' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              Inter-Rater Reliability Audit (Multi-Marker Consensus)
            </h3>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-indigo-50 dark:bg-indigo-950/30 rounded-xl border border-indigo-100 dark:border-indigo-800">
                <span className="text-xs uppercase font-bold text-indigo-700 dark:text-indigo-300">
                  Fleiss' Kappa (κ)
                </span>
                <div className="text-3xl font-extrabold text-indigo-900 dark:text-indigo-100 my-1 font-mono">
                  {kappaStats.fleissKappa.toFixed(2)}
                </div>
                <span className="text-xs text-indigo-700 dark:text-indigo-300 font-medium">
                  {kappaStats.agreementLabel} across {kappaStats.numRaters} raters
                </span>
              </div>

              <div className="p-4 bg-emerald-50 dark:bg-emerald-950/30 rounded-xl border border-emerald-100 dark:border-emerald-800">
                <span className="text-xs uppercase font-bold text-emerald-700 dark:text-emerald-300">
                  Pairwise Cohen's Kappa
                </span>
                <div className="text-3xl font-extrabold text-emerald-900 dark:text-emerald-100 my-1 font-mono">
                  {kappaStats.cohensKappa.toFixed(2)}
                </div>
                <span className="text-xs text-emerald-700 dark:text-emerald-300 font-medium">
                  Rater 1 vs Rater 2 Baseline Agreement
                </span>
              </div>
            </div>

            <div>
              <h4 className="text-xs font-bold text-gray-700 dark:text-gray-300 uppercase mb-3 flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <span>Flagged Grading Discrepancies Requiring Reconciliation</span>
              </h4>

              <div className="space-y-2 text-xs">
                <div className="p-3 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="font-bold text-amber-900 dark:text-amber-200">Submission #SUB-4912</span>
                    <p className="text-[11px] text-amber-800/80 dark:text-amber-300/80 mt-0.5">
                      Rater A assigned "Exemplary" (20 pts), Rater C assigned "Developing" (10 pts). Variance: 5.0
                    </p>
                  </div>
                  <button className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded text-xs font-medium">
                    Reconcile
                  </button>
                </div>

                <div className="p-3 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg flex justify-between items-center">
                  <div>
                    <span className="font-bold text-amber-900 dark:text-amber-200">Submission #SUB-5034</span>
                    <p className="text-[11px] text-amber-800/80 dark:text-amber-300/80 mt-0.5">
                      Rater B assigned "Proficient" (15 pts), Rater C assigned "Novice" (5 pts). Variance: 4.8
                    </p>
                  </div>
                  <button className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded text-xs font-medium">
                    Reconcile
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 dark:bg-gray-900/40 p-6 rounded-xl border border-gray-200 dark:border-gray-700 space-y-4">
            <h4 className="text-xs uppercase font-bold text-gray-500 dark:text-gray-400">
              Landis & Koch Kappa Scale
            </h4>
            <div className="space-y-1.5 text-xs">
              <div className="flex justify-between p-2 rounded bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <span>0.81 – 1.00</span>
                <span className="font-bold text-emerald-600">Almost Perfect</span>
              </div>
              <div className="flex justify-between p-2 rounded bg-indigo-50 dark:bg-indigo-900/40 border border-indigo-200 dark:border-indigo-800 font-semibold text-indigo-800 dark:text-indigo-200">
                <span>0.61 – 0.80</span>
                <span>Substantial (Current: 0.68)</span>
              </div>
              <div className="flex justify-between p-2 rounded bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <span>0.41 – 0.60</span>
                <span className="text-amber-600">Moderate</span>
              </div>
              <div className="flex justify-between p-2 rounded bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <span>0.21 – 0.40</span>
                <span className="text-orange-600">Fair</span>
              </div>
              <div className="flex justify-between p-2 rounded bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <span>&lt; 0.20</span>
                <span className="text-red-600">Slight / Poor</span>
              </div>
            </div>
            <p className="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">
              Standard accreditation protocols require Fleiss' Kappa &gt; 0.60 to confirm grading impartiality across exam panels.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
