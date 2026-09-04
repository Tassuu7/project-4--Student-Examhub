import React, { useState } from 'react';
import {
  GraduationCap,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
  Download,
  Filter,
  FileSpreadsheet,
  Award,
  Layers
} from 'lucide-react';

interface COResult {
  coCode: string;
  description: string;
  targetScorePct: number;
  studentsAttainedPct: number;
  attainmentLevel: number; // 0 to 3
  targetMet: boolean;
}

interface MappingRow {
  coCode: string;
  po1: number | string;
  po2: number | string;
  po3: number | string;
  po4: number | string;
  po5: number | string;
}

export const AccreditationDashboard: React.FC = () => {
  const [selectedCourse, setSelectedCourse] = useState('CS301');
  const [selectedStandard, setSelectedStandard] = useState<'NBA' | 'NAAC' | 'ABET'>('NBA');

  const coResults: COResult[] = [
    {
      coCode: 'CO1',
      description: 'Analyze distributed consensus algorithms and partition tolerance properties.',
      targetScorePct: 60.0,
      studentsAttainedPct: 84.5,
      attainmentLevel: 3,
      targetMet: true
    },
    {
      coCode: 'CO2',
      description: 'Design highly available, horizontally scaled microservices with asynchronous queuing.',
      targetScorePct: 65.0,
      studentsAttainedPct: 76.2,
      attainmentLevel: 2,
      targetMet: true
    },
    {
      coCode: 'CO3',
      description: 'Implement ACID multi-partition transaction protocols with Two-Phase Locking.',
      targetScorePct: 60.0,
      studentsAttainedPct: 71.8,
      attainmentLevel: 2,
      targetMet: true
    },
    {
      coCode: 'CO4',
      description: 'Evaluate system vulnerability surfaces, network partition hazards, and replay attacks.',
      targetScorePct: 70.0,
      studentsAttainedPct: 62.4,
      attainmentLevel: 1,
      targetMet: false
    }
  ];

  const mappingRows: MappingRow[] = [
    { coCode: 'CO1', po1: 3, po2: 3, po3: 2, po4: 1, po5: '-' },
    { coCode: 'CO2', po1: 2, po2: 3, po3: 3, po4: 2, po5: 1 },
    { coCode: 'CO3', po1: 3, po2: 2, po3: 3, po4: 1, po5: '-' },
    { coCode: 'CO4', po1: 2, po2: 3, po3: 2, po4: 3, po5: 2 }
  ];

  const poAttainmentSummary = [
    { poCode: 'PO1', label: 'Engineering Knowledge', score: 2.65, max: 3.0, status: 'HIGH' },
    { poCode: 'PO2', label: 'Problem Analysis', score: 2.45, max: 3.0, status: 'MODERATE' },
    { poCode: 'PO3', label: 'Design & Architecture', score: 2.50, max: 3.0, status: 'HIGH' },
    { poCode: 'PO4', label: 'Investigation of Complex Problems', score: 1.85, max: 3.0, status: 'NEEDS_IMPROVEMENT' },
    { poCode: 'PO5', label: 'Modern Tool Usage', score: 2.10, max: 3.0, status: 'MODERATE' }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <GraduationCap className="w-4 h-4" />
            <span>Outcome-Based Education (OBE) & Compliance</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Accreditation & Attainment Analytics (NBA / NAAC / ABET)
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Course Outcome (CO) evaluations, Program Outcome (PO) mapping matrices, and continuous quality improvement loops.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <select
            value={selectedStandard}
            onChange={(e: any) => setSelectedStandard(e.target.value)}
            className="text-xs font-semibold p-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
          >
            <option value="NBA">NBA (Tier-I / Tier-II India)</option>
            <option value="NAAC">NAAC (Criterion 2.6)</option>
            <option value="ABET">ABET EAC (Student Outcomes 1-7)</option>
          </select>

          <button className="inline-flex items-center space-x-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm">
            <Download className="w-4 h-4" />
            <span>Export OBE Report</span>
          </button>
        </div>
      </div>

      {/* Program Outcome Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {poAttainmentSummary.map((po) => (
          <div
            key={po.poCode}
            className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm"
          >
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                {po.poCode}
              </span>
              <span
                className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                  po.status === 'HIGH'
                    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                    : po.status === 'MODERATE'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                    : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
                }`}
              >
                {po.status}
              </span>
            </div>
            <div className="text-xl font-black text-gray-900 dark:text-white font-mono my-1">
              {po.score.toFixed(2)} <span className="text-xs text-gray-400 font-normal">/ {po.max.toFixed(1)}</span>
            </div>
            <div className="text-[11px] text-gray-500 dark:text-gray-400 truncate" title={po.label}>
              {po.label}
            </div>
            <div className="w-full bg-gray-100 dark:bg-gray-700 h-1.5 rounded-full overflow-hidden mt-2">
              <div
                className={`h-full ${
                  po.status === 'HIGH' ? 'bg-emerald-500' : po.status === 'MODERATE' ? 'bg-blue-500' : 'bg-amber-500'
                }`}
                style={{ width: `${(po.score / po.max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* CO Attainment Table */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
          Direct Assessment Course Outcome (CO) Attainment
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-gray-50 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400 font-semibold uppercase">
              <tr>
                <th className="py-2.5 px-3">CO Code</th>
                <th className="py-2.5 px-3">Statement & Learning Outcome</th>
                <th className="py-2.5 px-3 text-center">Target Threshold</th>
                <th className="py-2.5 px-3 text-center">% Students ≥ Threshold</th>
                <th className="py-2.5 px-3 text-center">Attainment Level</th>
                <th className="py-2.5 px-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {coResults.map((co) => (
                <tr key={co.coCode} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/20">
                  <td className="py-3 px-3 font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                    {co.coCode}
                  </td>
                  <td className="py-3 px-3 text-gray-800 dark:text-gray-200 max-w-md">
                    {co.description}
                  </td>
                  <td className="py-3 px-3 text-center font-mono">{co.targetScorePct.toFixed(1)}% marks</td>
                  <td className="py-3 px-3 text-center font-mono font-bold">{co.studentsAttainedPct.toFixed(1)}%</td>
                  <td className="py-3 px-3 text-center font-mono">
                    <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded font-bold">
                      Level {co.attainmentLevel}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-center">
                    {co.targetMet ? (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-bold bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>MET</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
                        <AlertCircle className="w-3 h-3" />
                        <span>UNMET</span>
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* CO - PO Mapping Matrix */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
              CO – PO Correlation & Articulation Matrix
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
              Correlation Scale: 3 = High, 2 = Medium, 1 = Low, '-' = No Correlation
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-center border-collapse">
            <thead className="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-bold">
              <tr>
                <th className="py-2.5 px-4 text-left border border-emerald-200 dark:border-emerald-800">Course Outcome</th>
                <th className="py-2.5 px-4 border border-emerald-200 dark:border-emerald-800">PO1</th>
                <th className="py-2.5 px-4 border border-emerald-200 dark:border-emerald-800">PO2</th>
                <th className="py-2.5 px-4 border border-emerald-200 dark:border-emerald-800">PO3</th>
                <th className="py-2.5 px-4 border border-emerald-200 dark:border-emerald-800">PO4</th>
                <th className="py-2.5 px-4 border border-emerald-200 dark:border-emerald-800">PO5</th>
              </tr>
            </thead>
            <tbody>
              {mappingRows.map((row) => (
                <tr key={row.coCode} className="hover:bg-gray-50 dark:hover:bg-gray-700/20">
                  <td className="py-2 px-4 text-left font-bold font-mono border border-gray-200 dark:border-gray-700">
                    {row.coCode}
                  </td>
                  <td className="py-2 px-4 font-mono font-semibold border border-gray-200 dark:border-gray-700">{row.po1}</td>
                  <td className="py-2 px-4 font-mono font-semibold border border-gray-200 dark:border-gray-700">{row.po2}</td>
                  <td className="py-2 px-4 font-mono font-semibold border border-gray-200 dark:border-gray-700">{row.po3}</td>
                  <td className="py-2 px-4 font-mono font-semibold border border-gray-200 dark:border-gray-700">{row.po4}</td>
                  <td className="py-2 px-4 font-mono font-semibold border border-gray-200 dark:border-gray-700">{row.po5}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
