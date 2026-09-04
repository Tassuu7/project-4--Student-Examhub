import React, { useState } from 'react';
import {
  Fingerprint,
  Eye,
  ShieldCheck,
  AlertTriangle,
  Activity,
  CheckCircle2,
  Lock,
  UserCheck,
  RotateCw,
  Compass
} from 'lucide-react';

export const BiometricVerificationConsole: React.FC = () => {
  const [activeSession, setActiveSession] = useState('SESS-PROCTOR-882');

  const [telemetry, setTelemetry] = useState({
    candidateName: 'Alex Vance',
    enrollmentId: 'ENR-9982',
    keystrokeSimilarity: 0.92,
    meanDwellTimeMs: 114,
    meanFlightTimeMs: 132,
    headYawDegrees: 4.5,
    headPitchDegrees: -2.1,
    headRollDegrees: 1.2,
    gazeAttentionPct: 98.2,
    overallTrustIndex: 94.5,
    faceDetected: true,
    multipleFacesDetected: false,
    anomaliesCount: 0
  });

  const digraphLatencies = [
    { pair: 'th', baselineMs: 95, currentMs: 92, diff: '-3ms' },
    { pair: 'he', baselineMs: 110, currentMs: 114, diff: '+4ms' },
    { pair: 'in', baselineMs: 85, currentMs: 88, diff: '+3ms' },
    { pair: 'er', baselineMs: 125, currentMs: 122, diff: '-3ms' },
    { pair: 'an', baselineMs: 90, currentMs: 94, diff: '+4ms' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-cyan-600 dark:text-cyan-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Fingerprint className="w-4 h-4" />
            <span>Behavioral Biometrics & Identity Verification</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Continuous Biometric Verification Console
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Real-time candidate authentication via keystroke flight rhythms and webcam 3D pose telemetry.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-green-50 dark:bg-green-950/40 border border-green-200 dark:border-green-800 px-3 py-1.5 rounded-lg text-xs font-bold text-green-700 dark:text-green-300">
            <ShieldCheck className="w-4 h-4" />
            <span>Candidate Verified: {telemetry.candidateName}</span>
          </div>
        </div>
      </div>

      {/* Main Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-2">
          <span className="text-xs uppercase font-bold text-gray-400">Continuous Trust Index</span>
          <div className="text-3xl font-black text-cyan-600 font-mono">
            {telemetry.overallTrustIndex}%
          </div>
          <div className="w-full bg-gray-100 dark:bg-gray-700 h-1.5 rounded-full overflow-hidden">
            <div className="bg-cyan-500 h-full" style={{ width: `${telemetry.overallTrustIndex}%` }} />
          </div>
          <span className="text-[11px] text-green-600 font-semibold block">High Authenticity Confidence</span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-2">
          <span className="text-xs uppercase font-bold text-gray-400">Keystroke Dynamics Fit</span>
          <div className="text-3xl font-black text-indigo-600 font-mono">
            {(telemetry.keystrokeSimilarity * 100).toFixed(1)}%
          </div>
          <span className="text-[11px] text-gray-500 block">
            Mean Dwell: {telemetry.meanDwellTimeMs}ms • Flight: {telemetry.meanFlightTimeMs}ms
          </span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-2">
          <span className="text-xs uppercase font-bold text-gray-400">Head Pose Orientation</span>
          <div className="text-2xl font-black text-gray-900 dark:text-white font-mono">
            Yaw: {telemetry.headYawDegrees}°
          </div>
          <span className="text-[11px] text-gray-500 block">
            Pitch: {telemetry.headPitchDegrees}° • Roll: {telemetry.headRollDegrees}° (Centered)
          </span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-2">
          <span className="text-xs uppercase font-bold text-gray-400">Gaze Focus Index</span>
          <div className="text-3xl font-black text-emerald-600 font-mono">
            {telemetry.gazeAttentionPct}%
          </div>
          <span className="text-[11px] text-emerald-600 font-semibold block">Attentive to Exam Screen</span>
        </div>
      </div>

      {/* Keystroke Profile & Digraph Latency Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-gray-100 dark:border-gray-700">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
              Enrolled Keystroke Digraph Signatures
            </h3>
            <span className="text-xs text-cyan-600 font-semibold font-mono">Profile: ACTIVE</span>
          </div>

          <p className="text-xs text-gray-500 leading-relaxed">
            Measures inter-key transition flight times across frequent character digraphs compared to enrolled baseline.
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-gray-50 dark:bg-gray-700/50 text-gray-500 font-semibold uppercase">
                <tr>
                  <th className="py-2 px-3">Digraph Pair</th>
                  <th className="py-2 px-3 text-right">Enrolled Latency</th>
                  <th className="py-2 px-3 text-right">Current Session</th>
                  <th className="py-2 px-3 text-center">Variance</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700 font-mono">
                {digraphLatencies.map((d) => (
                  <tr key={d.pair} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/20">
                    <td className="py-2 px-3 font-bold text-gray-900 dark:text-white font-sans">
                      "{d.pair}"
                    </td>
                    <td className="py-2 px-3 text-right text-gray-600 dark:text-gray-300">{d.baselineMs} ms</td>
                    <td className="py-2 px-3 text-right font-bold text-cyan-600">{d.currentMs} ms</td>
                    <td className="py-2 px-3 text-center">
                      <span className="text-green-600 font-bold">{d.diff}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Head Pose & Gaze Compass */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-gray-100 dark:border-gray-700">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
              Webcam 3D Pose Compass & Gaze Tracking
            </h3>
            <span className="text-xs text-emerald-600 font-semibold font-mono">Single Face: LOCKED</span>
          </div>

          <div className="p-8 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-200 dark:border-gray-700 flex flex-col items-center justify-center space-y-4">
            <div className="w-32 h-32 rounded-full border-4 border-dashed border-cyan-500/40 flex items-center justify-center relative">
              <Compass className="w-16 h-16 text-cyan-600 animate-spin-slow" />
              <div className="absolute w-3 h-3 bg-cyan-600 rounded-full" />
            </div>

            <div className="text-center space-y-1">
              <span className="text-xs font-bold text-gray-900 dark:text-white block">
                Direct Screen Gaze Confirmed
              </span>
              <span className="text-[11px] text-gray-500 block">
                Horizontal Yaw: {telemetry.headYawDegrees}° (Threshold: ±30°)
              </span>
            </div>
          </div>

          <div className="flex justify-between text-xs text-gray-500 pt-1">
            <span>Face mesh landmarks: 68 points</span>
            <span>Sampling: 30 fps</span>
          </div>
        </div>
      </div>
    </div>
  );
};
