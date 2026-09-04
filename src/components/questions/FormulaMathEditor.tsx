import React, { useState } from 'react';
import {
  Sigma,
  Code,
  Check,
  Copy,
  Eye,
  Sparkles,
  HelpCircle
} from 'lucide-react';

export const FormulaMathEditor: React.FC = () => {
  const [latexInput, setLatexInput] = useState<string>('P(\\theta) = c_i + \\frac{1 - c_i}{1 + e^{-D \\cdot a_i (\\theta - b_i)}}');
  const [copied, setCopied] = useState<boolean>(false);

  const symbolGroups = [
    {
      category: 'Psychometrics & Statistics',
      symbols: [
        { label: 'θ (Ability)', code: '\\theta' },
        { label: 'b (Difficulty)', code: 'b_i' },
        { label: 'a (Discrimination)', code: 'a_i' },
        { label: 'c (Guessing)', code: 'c_i' },
        { label: 'r_pbis', code: 'r_{pbis}' },
        { label: 'SEM', code: 'SEM = \\frac{1}{\\sqrt{I(\\theta)}}' },
        { label: 'Cronbach α', code: '\\alpha = \\frac{K}{K - 1} \\left( 1 - \\frac{\\sum \\sigma_i^2}{\\sigma_X^2} \\right)' }
      ]
    },
    {
      category: 'Calculus & Algebra',
      symbols: [
        { label: 'Sum Σ', code: '\\sum_{i=1}^{n}' },
        { label: 'Integral ∫', code: '\\int_{a}^{b} f(x) \\, dx' },
        { label: 'Fraction', code: '\\frac{a}{b}' },
        { label: 'Square Root', code: '\\sqrt{x}' },
        { label: 'Limit', code: '\\lim_{x \\to \\infty}' },
        { label: 'Infinity', code: '\\infty' },
        { label: 'Partial d', code: '\\frac{\\partial y}{\\partial x}' }
      ]
    }
  ];

  const handleInsertSymbol = (code: string) => {
    setLatexInput((prev) => `${prev} ${code} `);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(latexInput);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Sigma className="w-4 h-4" />
            <span>STEM Formula & Symbolic Equation Studio</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            LaTeX Mathematical Expression Studio
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Author and preview KaTeX/LaTeX mathematical formulas for STEM assessments and question stems.
          </p>
        </div>

        <button
          onClick={handleCopy}
          className="inline-flex items-center space-x-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-sm"
        >
          {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? 'Copied to Clipboard' : 'Copy LaTeX String'}</span>
        </button>
      </div>

      {/* Editor & Preview Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <div className="flex justify-between items-center">
            <label className="text-xs font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
              LaTeX Equation Source
            </label>
            <span className="text-[11px] text-gray-400 font-mono">KaTeX Compliant</span>
          </div>

          <textarea
            value={latexInput}
            onChange={(e) => setLatexInput(e.target.value)}
            rows={6}
            className="w-full p-4 font-mono text-xs bg-gray-900 text-emerald-400 rounded-xl border border-gray-700 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
            placeholder="Type LaTeX math equation here..."
          />

          {/* Symbol Quick Palette */}
          <div className="space-y-3 pt-2">
            {symbolGroups.map((group) => (
              <div key={group.category} className="space-y-1.5">
                <span className="text-[11px] font-bold text-gray-500 uppercase tracking-wider block">
                  {group.category}
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {group.symbols.map((sym) => (
                    <button
                      key={sym.label}
                      type="button"
                      onClick={() => handleInsertSymbol(sym.code)}
                      className="px-2.5 py-1 text-xs rounded border border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-600 bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 transition-colors"
                    >
                      {sym.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Preview Panel */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-xs font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-4 pb-2 border-b border-gray-100 dark:border-gray-700">
              <Eye className="w-4 h-4 text-indigo-600" />
              <span>Typeset Mathematical Render Preview</span>
            </div>

            <div className="p-8 bg-indigo-50/40 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/40 rounded-xl flex items-center justify-center min-h-[160px] text-center">
              <div className="font-serif text-lg text-indigo-950 dark:text-indigo-100 leading-relaxed font-semibold">
                {latexInput}
              </div>
            </div>
          </div>

          <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg text-xs text-gray-500 space-y-1">
            <span className="font-semibold text-gray-700 dark:text-gray-300 block">Rendering Compatibility</span>
            <p>
              Formulas are embedded into SVG vectors during printable certificate and PDF transcript export to preserve crisp rendering at 600 DPI.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
