import React, { useState } from 'react';
import {
  FileText,
  Download,
  Printer,
  Search,
  CheckCircle2,
  Calendar,
  Building,
  GraduationCap,
  Sparkles,
  ExternalLink
} from 'lucide-react';

export const InstitutionalReportsView: React.FC = () => {
  const [candidateId, setCandidateId] = useState('cand_001');
  const [examId, setExamId] = useState('exam_cs301_final');
  const [previewActive, setPreviewActive] = useState(true);

  const transcriptItems = [
    { code: 'CS101', name: 'Data Structures & Algorithms', credits: 4.0, grade: 'A', points: 4.0, score: 94.5, status: 'PASS' },
    { code: 'CS202', name: 'Computer Systems Architecture', credits: 4.0, grade: 'A', points: 4.0, score: 91.0, status: 'PASS' },
    { code: 'CS303', name: 'Distributed Cloud Computing', credits: 4.0, grade: 'A-', points: 3.7, score: 88.5, status: 'PASS' },
    { code: 'CS404', name: 'Cryptography & Cyber Security', credits: 4.0, grade: 'A', points: 4.0, score: 96.0, status: 'PASS' },
    { code: 'MA201', name: 'Discrete Applied Mathematics', credits: 4.0, grade: 'B+', points: 3.3, score: 83.0, status: 'PASS' },
    { code: 'SE499', name: 'Senior Capstone Project', credits: 4.0, grade: 'A', points: 4.0, score: 98.0, status: 'PASS' }
  ];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <GraduationCap className="w-4 h-4" />
            <span>Official Academic Records & SIS Transcripts</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Institutional Reporting & Transcripts
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Official verifiable academic transcripts, statistical response matrix exports, and exam audit registries.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handlePrint}
            className="inline-flex items-center space-x-1.5 px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 text-xs font-semibold rounded-lg transition-colors"
          >
            <Printer className="w-4 h-4" />
            <span>Print Official Transcript</span>
          </button>
          <a
            href={`/api/reports/exam/${examId}/matrix-csv`}
            download
            className="inline-flex items-center space-x-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm"
          >
            <Download className="w-4 h-4" />
            <span>Download Responses Matrix (CSV)</span>
          </a>
        </div>
      </div>

      {/* Candidate Search Bar */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex items-center space-x-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
          <input
            type="text"
            value={candidateId}
            onChange={(e) => setCandidateId(e.target.value)}
            placeholder="Search candidate by ID or enrollment number (e.g. cand_001)..."
            className="w-full text-xs pl-9 pr-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200"
          />
        </div>
        <button className="px-4 py-2 bg-gray-800 dark:bg-gray-700 text-white text-xs font-semibold rounded-lg">
          Fetch Record
        </button>
      </div>

      {/* Printable Transcript Card */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 shadow-sm max-w-4xl mx-auto">
        <div className="border-b-2 border-blue-600 pb-6 mb-6 flex justify-between items-start">
          <div>
            <span className="text-xs uppercase font-bold text-blue-600 tracking-wider">Office of the Registrar</span>
            <h3 className="text-2xl font-black text-gray-900 dark:text-white uppercase tracking-wide mt-0.5">
              Apex Polytechnic Institute
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Accredited by the National Board of Accreditation & Higher Education Council
            </p>
          </div>
          <div className="text-right">
            <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-200 text-xs font-bold rounded-full">
              OFFICIAL TRANSCRIPT
            </span>
            <div className="text-xs text-gray-500 mt-2 font-mono">Date: September 04, 2026</div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-gray-50 dark:bg-gray-900/40 p-4 rounded-xl mb-6 text-xs">
          <div>
            <span className="text-gray-400 block text-[11px]">Candidate Name</span>
            <span className="font-bold text-gray-800 dark:text-gray-200">Alex Vance</span>
          </div>
          <div>
            <span className="text-gray-400 block text-[11px]">Enrollment Number</span>
            <span className="font-bold font-mono text-gray-800 dark:text-gray-200">ENR-9982-CAND001</span>
          </div>
          <div>
            <span className="text-gray-400 block text-[11px]">Degree Program</span>
            <span className="font-bold text-gray-800 dark:text-gray-200">B.S. Computer Engineering</span>
          </div>
          <div>
            <span className="text-gray-400 block text-[11px]">Transcript Serial</span>
            <span className="font-bold font-mono text-blue-600">TRX-2026-CAND001</span>
          </div>
        </div>

        <div className="overflow-x-auto mb-6">
          <table className="w-full text-xs text-left">
            <thead className="bg-gray-100 dark:bg-gray-700/50 text-gray-600 dark:text-gray-300 font-bold uppercase">
              <tr>
                <th className="py-2.5 px-3">Subject Code</th>
                <th className="py-2.5 px-3">Subject Description</th>
                <th className="py-2.5 px-3 text-center">Credits</th>
                <th className="py-2.5 px-3 text-center">Grade</th>
                <th className="py-2.5 px-3 text-center">Points</th>
                <th className="py-2.5 px-3 text-center">Score</th>
                <th className="py-2.5 px-3 text-center">Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {transcriptItems.map((it) => (
                <tr key={it.code} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/20">
                  <td className="py-3 px-3 font-bold font-mono text-gray-800 dark:text-gray-200">{it.code}</td>
                  <td className="py-3 px-3 text-gray-900 dark:text-white">{it.name}</td>
                  <td className="py-3 px-3 text-center font-mono">{it.credits.toFixed(1)}</td>
                  <td className="py-3 px-3 text-center font-bold font-mono">{it.grade}</td>
                  <td className="py-3 px-3 text-center font-mono">{it.points.toFixed(1)}</td>
                  <td className="py-3 px-3 text-center font-mono">{it.score.toFixed(1)}%</td>
                  <td className="py-3 px-3 text-center">
                    <span className="font-bold text-green-600 dark:text-green-400">{it.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="flex justify-between items-center bg-blue-50 dark:bg-blue-950/30 p-4 rounded-xl border border-blue-200 dark:border-blue-800 mb-8">
          <div className="text-center">
            <span className="text-[10px] uppercase font-bold text-blue-700 dark:text-blue-300">Total Credits Earned</span>
            <div className="text-2xl font-black text-blue-900 dark:text-blue-100 font-mono">24.0</div>
          </div>
          <div className="text-center">
            <span className="text-[10px] uppercase font-bold text-blue-700 dark:text-blue-300">Semester Grade Point (SGPA)</span>
            <div className="text-2xl font-black text-blue-900 dark:text-blue-100 font-mono">3.85</div>
          </div>
          <div className="text-center">
            <span className="text-[10px] uppercase font-bold text-blue-700 dark:text-blue-300">Cumulative GPA (CGPA)</span>
            <div className="text-2xl font-black text-blue-900 dark:text-blue-100 font-mono">3.92</div>
          </div>
        </div>

        <div className="flex justify-between items-end border-t border-gray-200 dark:border-gray-700 pt-6 text-xs text-gray-500">
          <div>
            <div className="font-semibold text-gray-700 dark:text-gray-300">Cryptographic Verification Hash:</div>
            <div className="font-mono text-[10px] bg-gray-100 dark:bg-gray-700/50 p-1.5 rounded mt-1 break-all max-w-sm">
              e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
            </div>
          </div>
          <div className="text-center">
            <div className="h-10 border-b border-gray-400 w-40 mb-1" />
            <span className="font-semibold text-gray-800 dark:text-gray-200">Controller of Examinations</span>
          </div>
        </div>
      </div>
    </div>
  );
};
