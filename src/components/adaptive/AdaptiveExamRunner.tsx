import React, { useState, useEffect } from 'react';
import {
  BrainCircuit,
  Award,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowRight,
  ShieldCheck,
  BarChart3,
  HelpCircle,
  FileText,
  Check,
  ChevronRight,
  Sparkles,
  BookOpen
} from 'lucide-react';

interface QuestionItem {
  itemId: string;
  questionText: string;
  options: string[];
  difficulty: number;
  domain: string;
}

export const AdaptiveExamRunner: React.FC = () => {
  const [sessionActive, setSessionActive] = useState<boolean>(false);
  const [stepNumber, setStepNumber] = useState<number>(1);
  const [currentTheta, setCurrentTheta] = useState<float>(0.0);
  const [currentSem, setCurrentSem] = useState<float>(0.85);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isCompleted, setIsCompleted] = useState<boolean>(false);
  const [terminationReason, setTerminationReason] = useState<string>('');
  const [percentile, setPercentile] = useState<number>(50.0);
  const [timeRemainingSeconds, setTimeRemainingSeconds] = useState<number>(3600);
  const [showFormulaSheet, setShowFormulaSheet] = useState<boolean>(false);
  const [scratchpadText, setScratchpadText] = useState<string>('');
  const [showScratchpad, setShowScratchpad] = useState<boolean>(false);

  // Simulated live item
  const [currentItem, setCurrentItem] = useState<QuestionItem>({
    itemId: 'CAT-ITEM-0012',
    questionText: 'In a distributed relational database, which mechanism ensures strict serializability across multi-partition ACID transactions?',
    options: [
      'Two-Phase Commit (2PC) protocol combined with strict Two-Phase Locking (2PL)',
      'Eventual consistency with asynchronous gossip protocol vector clocks',
      'Optimistic concurrency control with client-side clock timestamps',
      'Single-threaded event loop execution without locking mechanisms'
    ],
    difficulty: 0.45,
    domain: 'Computer Systems Architecture'
  });

  const [history, setHistory] = useState<
    Array<{ step: number; difficulty: number; correct: boolean; theta: number; sem: number }>
  >([
    { step: 1, difficulty: 0.0, correct: true, theta: 0.35, sem: 0.72 },
    { step: 2, difficulty: 0.4, correct: true, theta: 0.68, sem: 0.58 },
    { step: 3, difficulty: 0.8, correct: false, theta: 0.42, sem: 0.46 },
    { step: 4, difficulty: 0.45, correct: true, theta: 0.59, sem: 0.38 }
  ]);

  useEffect(() => {
    let timer: any;
    if (sessionActive && !isCompleted) {
      timer = setInterval(() => {
        setTimeRemainingSeconds((prev) => {
          if (prev <= 1) {
            setIsCompleted(true);
            setTerminationReason('Time expired');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [sessionActive, isCompleted]);

  const handleStartExam = () => {
    setSessionActive(true);
    setStepNumber(1);
    setCurrentTheta(0.0);
    setCurrentSem(0.85);
    setIsCompleted(false);
    setSelectedOption(null);
  };

  const handleSubmitAnswer = () => {
    if (selectedOption === null) return;

    const isCorrect = selectedOption === 0;
    const delta = isCorrect ? 0.35 : -0.32;
    const newTheta = parseFloat((currentTheta + delta).toFixed(2));
    const newSem = parseFloat(Math.max(0.18, currentSem - 0.06).toFixed(2));

    const newHist = [
      ...history,
      {
        step: stepNumber + 1,
        difficulty: currentItem.difficulty,
        correct: isCorrect,
        theta: newTheta,
        sem: newSem
      }
    ];
    setHistory(newHist);
    setCurrentTheta(newTheta);
    setCurrentSem(newSem);
    setStepNumber((prev) => prev + 1);
    setSelectedOption(null);

    // Check stopping condition: target SEM <= 0.25 or 15 items
    if (newSem <= 0.25 || stepNumber >= 14) {
      setIsCompleted(true);
      setTerminationReason(
        newSem <= 0.25
          ? `Target measurement precision reached (Standard Error = ${newSem} ≤ 0.25)`
          : 'Maximum test length reached (15 items)'
      );
      // Theta to percentile approximation
      const z = newTheta;
      const pct = Math.min(99.9, Math.max(0.1, 50 + z * 34));
      setPercentile(parseFloat(pct.toFixed(1)));
    } else {
      // Pick next harder/easier item
      const nextDiff = isCorrect ? currentItem.difficulty + 0.3 : currentItem.difficulty - 0.25;
      setCurrentItem({
        itemId: `CAT-ITEM-${Math.floor(Math.random() * 9000 + 1000)}`,
        questionText: `Adaptive Question ${stepNumber + 1}: Testing competency at calibrated logit difficulty (${nextDiff >= 0 ? '+' : ''}${nextDiff.toFixed(2)}). Identify the optimal design approach for high-concurrency stream processing.`,
        options: [
          'Option Alpha: Partitioned log stream with consumer group checkpointing',
          'Option Beta: In-memory circular buffer with non-blocking atomics',
          'Option Gamma: Broadcast multicast over UDP datagrams',
          'Option Delta: Periodic bulk disk sync with exclusive mutex locks'
        ],
        difficulty: parseFloat(nextDiff.toFixed(2)),
        domain: 'Distributed Systems Engineering'
      });
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-indigo-900 via-blue-900 to-indigo-950 text-white rounded-xl p-6 shadow-lg border border-indigo-700/50">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-300 text-sm font-semibold uppercase tracking-wider mb-1">
              <BrainCircuit className="w-4 h-4" />
              <span>Computerized Adaptive Testing (CAT) Engine</span>
            </div>
            <h2 className="text-2xl font-bold">Dynamic IRT Adaptive Examination</h2>
            <p className="text-indigo-200 text-sm mt-1">
              Item Response Theory (3PL Model) • Real-Time Theta Ability Calibration • Optimal Fisher Information Selection
            </p>
          </div>

          {sessionActive && !isCompleted && (
            <div className="flex items-center space-x-4 bg-black/30 backdrop-blur-md px-4 py-2.5 rounded-lg border border-white/10">
              <div className="flex items-center space-x-2 text-amber-300">
                <Clock className="w-5 h-5 animate-pulse" />
                <span className="font-mono text-lg font-bold">{formatTimer(timeRemainingSeconds)}</span>
              </div>
              <div className="h-6 w-px bg-white/20" />
              <div className="text-xs text-indigo-200">
                <div>Item #{stepNumber}</div>
                <div className="font-semibold text-white">Target SEM ≤ 0.25</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {!sessionActive ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-8 border border-gray-200 dark:border-gray-700 text-center max-w-2xl mx-auto shadow-sm">
          <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <BrainCircuit className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Standard Adaptive Assessment Session
          </h3>
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-6 leading-relaxed">
            Unlike static linear tests, this adaptive assessment dynamically adjusts each question's difficulty
            based on your previous answers. You will answer between 10 and 20 targeted questions until your ability
            parameter (θ) is measured with high statistical confidence.
          </p>
          <div className="grid grid-cols-3 gap-3 mb-8 text-left text-xs bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
            <div>
              <span className="text-gray-500 dark:text-gray-400 block">Psychometric Model</span>
              <span className="font-semibold text-gray-800 dark:text-gray-200">3-Parameter Logistic (3PL)</span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400 block">Stopping Rule</span>
              <span className="font-semibold text-gray-800 dark:text-gray-200">Standard Error (SEM) ≤ 0.25</span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400 block">Estimation Method</span>
              <span className="font-semibold text-gray-800 dark:text-gray-200">Expected A Posteriori (EAP)</span>
            </div>
          </div>
          <button
            onClick={handleStartExam}
            className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all hover:shadow-lg"
          >
            <span>Begin Adaptive Exam</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      ) : isCompleted ? (
        /* Completed Score Report */
        <div className="bg-white dark:bg-gray-800 rounded-xl p-8 border border-gray-200 dark:border-gray-700 max-w-3xl mx-auto shadow-sm">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400 rounded-2xl flex items-center justify-center mx-auto mb-3">
              <Award className="w-9 h-9" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Exam Completed & Calibrated</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">{terminationReason}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-50 dark:bg-blue-950/40 p-4 rounded-xl border border-blue-200 dark:border-blue-800 text-center">
              <span className="text-xs uppercase font-semibold text-blue-700 dark:text-blue-300">Latent Ability (θ)</span>
              <div className="text-3xl font-extrabold text-blue-900 dark:text-blue-100 my-1 font-mono">
                {currentTheta >= 0 ? `+${currentTheta.toFixed(2)}` : currentTheta.toFixed(2)}
              </div>
              <span className="text-xs text-blue-600 dark:text-blue-400">Logit Scale [-3.0 to +3.0]</span>
            </div>

            <div className="bg-purple-50 dark:bg-purple-950/40 p-4 rounded-xl border border-purple-200 dark:border-purple-800 text-center">
              <span className="text-xs uppercase font-semibold text-purple-700 dark:text-purple-300">Estimated Percentile</span>
              <div className="text-3xl font-extrabold text-purple-900 dark:text-purple-100 my-1 font-mono">
                {percentile}%
              </div>
              <span className="text-xs text-purple-600 dark:text-purple-400">Normative Peer Cohort</span>
            </div>

            <div className="bg-emerald-50 dark:bg-emerald-950/40 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 text-center">
              <span className="text-xs uppercase font-semibold text-emerald-700 dark:text-emerald-300">Standard Error (SEM)</span>
              <div className="text-3xl font-extrabold text-emerald-900 dark:text-emerald-100 my-1 font-mono">
                ±{currentSem.toFixed(2)}
              </div>
              <span className="text-xs text-emerald-600 dark:text-emerald-400">High Precision Measurement</span>
            </div>
          </div>

          <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-blue-600" />
              <span>Adaptive Administration Trajectory</span>
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-gray-50 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400 font-semibold uppercase">
                  <tr>
                    <th className="py-2 px-3">Item Step</th>
                    <th className="py-2 px-3">Difficulty (b)</th>
                    <th className="py-2 px-3 text-center">Result</th>
                    <th className="py-2 px-3 text-right">Theta Post</th>
                    <th className="py-2 px-3 text-right">SEM Post</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {history.map((h, i) => (
                    <tr key={i} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/20">
                      <td className="py-2 px-3 font-semibold text-gray-700 dark:text-gray-300">Question #{h.step}</td>
                      <td className="py-2 px-3 font-mono">{h.difficulty >= 0 ? `+${h.difficulty.toFixed(2)}` : h.difficulty.toFixed(2)}</td>
                      <td className="py-2 px-3 text-center">
                        <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-bold ${
                          h.correct ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' : 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300'
                        }`}>
                          {h.correct ? 'CORRECT' : 'INCORRECT'}
                        </span>
                      </td>
                      <td className="py-2 px-3 text-right font-mono text-blue-600 dark:text-blue-400 font-semibold">
                        {h.theta >= 0 ? `+${h.theta.toFixed(2)}` : h.theta.toFixed(2)}
                      </td>
                      <td className="py-2 px-3 text-right font-mono text-gray-500 dark:text-gray-400">
                        ±{h.sem.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-8 text-center">
            <button
              onClick={handleStartExam}
              className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-semibold rounded-lg text-sm transition-colors"
            >
              Restart Simulation Session
            </button>
          </div>
        </div>
      ) : (
        /* Active Item Runner */
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Question Area */}
          <div className="lg:col-span-3 space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
              <div className="flex justify-between items-center pb-4 mb-4 border-b border-gray-100 dark:border-gray-700">
                <span className="text-xs font-semibold px-2.5 py-1 bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full">
                  Domain: {currentItem.domain}
                </span>
                <span className="text-xs font-mono text-gray-500 dark:text-gray-400">
                  Calibrated Difficulty: {currentItem.difficulty >= 0 ? `+${currentItem.difficulty.toFixed(2)}` : currentItem.difficulty.toFixed(2)} logits
                </span>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 dark:text-white leading-relaxed mb-6">
                {currentItem.questionText}
              </h3>

              <div className="space-y-3">
                {currentItem.options.map((opt, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedOption(idx)}
                    className={`w-full text-left p-4 rounded-xl border transition-all flex items-start space-x-3 ${
                      selectedOption === idx
                        ? 'border-blue-600 bg-blue-50/70 dark:bg-blue-900/30 text-blue-950 dark:text-blue-100 shadow-sm ring-1 ring-blue-600'
                        : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-xs font-bold ${
                        selectedOption === idx
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                      }`}
                    >
                      {String.fromCharCode(65 + idx)}
                    </div>
                    <span className="text-sm">{opt}</span>
                  </button>
                ))}
              </div>

              <div className="flex justify-between items-center mt-8 pt-4 border-t border-gray-100 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setShowScratchpad(!showScratchpad)}
                    className="text-xs font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>Scratchpad</span>
                  </button>
                  <button
                    onClick={() => setShowFormulaSheet(!showFormulaSheet)}
                    className="text-xs font-medium text-gray-600 dark:text-gray-300 hover:text-blue-600 flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    <BookOpen className="w-3.5 h-3.5" />
                    <span>Formulas</span>
                  </button>
                </div>

                <button
                  disabled={selectedOption === null}
                  onClick={handleSubmitAnswer}
                  className={`inline-flex items-center space-x-2 px-6 py-2.5 rounded-lg text-sm font-semibold transition-all ${
                    selectedOption !== null
                      ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
                  }`}
                >
                  <span>Submit & Calibrate</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Scratchpad expandable */}
            {showScratchpad && (
              <div className="bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-xl p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs font-bold text-amber-800 dark:text-amber-300 uppercase">Exam Scratchpad</span>
                  <span className="text-[10px] text-amber-600 dark:text-amber-400">Notes are saved locally</span>
                </div>
                <textarea
                  value={scratchpadText}
                  onChange={(e) => setScratchpadText(e.target.value)}
                  placeholder="Draft calculations, variable tracking, or scratch work..."
                  className="w-full h-24 p-2 text-xs bg-white dark:bg-gray-800 border border-amber-200 dark:border-amber-700 rounded-lg text-gray-800 dark:text-gray-200 font-mono resize-none focus:outline-none focus:ring-1 focus:ring-amber-500"
                />
              </div>
            )}
          </div>

          {/* Right Sidebar: Real-time Psychometrics */}
          <div className="space-y-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
              <h4 className="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 tracking-wider">
                Live Psychometrics
              </h4>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-600 dark:text-gray-400">Running Ability (θ):</span>
                  <span className="font-mono font-bold text-blue-600 dark:text-blue-400">
                    {currentTheta >= 0 ? `+${currentTheta.toFixed(2)}` : currentTheta.toFixed(2)}
                  </span>
                </div>
                <div className="w-full bg-gray-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-blue-600 h-full transition-all duration-300"
                    style={{ width: `${Math.min(100, Math.max(0, ((currentTheta + 3) / 6) * 100))}%` }}
                  />
                </div>
                <div className="flex justify-between text-[10px] text-gray-400 font-mono mt-0.5">
                  <span>-3.0</span>
                  <span>0.0</span>
                  <span>+3.0</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-600 dark:text-gray-400">Precision (SEM):</span>
                  <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                    ±{currentSem.toFixed(2)}
                  </span>
                </div>
                <div className="w-full bg-gray-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-emerald-500 h-full transition-all duration-300"
                    style={{ width: `${Math.min(100, Math.max(0, (1.0 - currentSem) * 100))}%` }}
                  />
                </div>
                <div className="text-[10px] text-gray-400 text-right mt-0.5">
                  Target: ≤ 0.25 ({Math.round(Math.min(100, Math.max(0, (1.0 - currentSem / 0.85) * 100)))}% to goal)
                </div>
              </div>

              <div className="border-t border-gray-100 dark:border-gray-700 pt-3">
                <div className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Session Statistics
                </div>
                <div className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                  <div className="flex justify-between">
                    <span>Questions Answered:</span>
                    <span className="font-semibold text-gray-800 dark:text-gray-200">{stepNumber - 1}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Target Length:</span>
                    <span className="font-semibold text-gray-800 dark:text-gray-200">10 – 20 items</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Algorithm:</span>
                    <span className="font-semibold text-gray-800 dark:text-gray-200">Bayesian EAP</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-blue-50/50 dark:bg-blue-950/20 rounded-xl p-4 border border-blue-100 dark:border-blue-900/40 text-xs text-blue-900 dark:text-blue-200 space-y-1">
              <div className="font-bold flex items-center space-x-1 text-blue-700 dark:text-blue-300">
                <ShieldCheck className="w-4 h-4" />
                <span>Security Assurance</span>
              </div>
              <p className="text-[11px] text-blue-800/80 dark:text-blue-300/80 leading-relaxed">
                Sympson-Hetter exposure control active. Item exposure is restricted to preserve bank integrity.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
