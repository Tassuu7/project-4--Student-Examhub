import React, { useState } from 'react';
import {
  FileCode,
  Download,
  Upload,
  CheckCircle2,
  AlertCircle,
  Code2,
  Copy,
  Check,
  Package,
  Layers,
  Sparkles
} from 'lucide-react';

export const QTIManager: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'export' | 'import' | 'xml_editor'>('export');
  const [qtiVersion, setQtiVersion] = useState<'2.1' | '3.0'>('2.1');
  const [includeFeedback, setIncludeFeedback] = useState<boolean>(true);
  const [includeRubrics, setIncludeRubrics] = useState<boolean>(true);
  const [copied, setCopied] = useState<boolean>(false);
  const [exportSuccess, setExportSuccess] = useState<boolean>(false);

  const sampleXML = `<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
                identifier="ITEM-CS101-042"
                title="Distributed System Quorum Verification"
                adaptive="false"
                timeDependent="false">
    <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
        <correctResponse>
            <value>ChoiceB</value>
        </correctResponse>
    </responseDeclaration>
    <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
        <defaultValue>
            <value>0</value>
        </defaultValue>
    </outcomeDeclaration>
    <itemBody>
        <p>In a distributed consensus cluster of 5 nodes running Raft, what is the minimum quorum size required to elect a leader?</p>
        <choiceInteraction responseIdentifier="RESPONSE" shuffle="true" maxChoices="1">
            <simpleChoice identifier="ChoiceA">2 nodes</simpleChoice>
            <simpleChoice identifier="ChoiceB">3 nodes (Majority: ⌊N/2⌋ + 1)</simpleChoice>
            <simpleChoice identifier="ChoiceC">4 nodes</simpleChoice>
            <simpleChoice identifier="ChoiceD">All 5 nodes</simpleChoice>
        </choiceInteraction>
    </itemBody>
    <modalFeedback outcomeIdentifier="FEEDBACK" identifier="fb_correct" showHide="show" title="Correct">
        <p>A quorum requires strict majority ⌊5/2⌋ + 1 = 3 nodes to guarantee overlapping majorities.</p>
    </modalFeedback>
</assessmentItem>`;

  const [xmlContent, setXmlContent] = useState<string>(sampleXML);
  const [validationResult, setValidationResult] = useState<{
    valid: boolean;
    identifier?: string;
    choicesCount?: number;
    error?: string;
  } | null>(null);

  const handleCopyXML = () => {
    navigator.clipboard.writeText(xmlContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleValidateXML = () => {
    if (xmlContent.includes('<assessmentItem') && xmlContent.includes('identifier=')) {
      setValidationResult({
        valid: true,
        identifier: 'ITEM-CS101-042',
        choicesCount: 4
      });
    } else {
      setValidationResult({
        valid: false,
        error: 'Missing root <assessmentItem> declaration or required identifier attribute.'
      });
    }
  };

  const handleTriggerExport = () => {
    setExportSuccess(true);
    setTimeout(() => setExportSuccess(false), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Layers className="w-4 h-4" />
            <span>IMS Global Interoperability Standard</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            QTI 2.1 / 3.0 Package Manager
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Import, export, and validate Question and Test Interoperability XML packages for Canvas, Moodle, and Blackboard.
          </p>
        </div>

        <div className="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('export')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              activeTab === 'export'
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            Export Packages
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              activeTab === 'import'
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            Import ZIP
          </button>
          <button
            onClick={() => setActiveTab('xml_editor')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              activeTab === 'xml_editor'
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            XML Inspector
          </button>
        </div>
      </div>

      {activeTab === 'export' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              Configure QTI Export Package
            </h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Specification Version
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setQtiVersion('2.1')}
                    className={`py-2 px-3 text-xs font-semibold rounded-lg border text-center ${
                      qtiVersion === '2.1'
                        ? 'border-blue-600 bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-200'
                        : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    QTI 2.1 (LMS Universal)
                  </button>
                  <button
                    type="button"
                    onClick={() => setQtiVersion('3.0')}
                    className={`py-2 px-3 text-xs font-semibold rounded-lg border text-center ${
                      qtiVersion === '3.0'
                        ? 'border-blue-600 bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-200'
                        : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    QTI 3.0 (Modern W3C)
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Scope of Export
                </label>
                <select className="w-full p-2 text-xs border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200">
                  <option>Entire Institutional Item Bank (All Topics)</option>
                  <option>Computer Science & Engineering Bank (120 Items)</option>
                  <option>Midterm Examination 2026 Selection (40 Items)</option>
                </select>
              </div>
            </div>

            <div className="space-y-3 pt-2">
              <label className="flex items-center space-x-2 text-xs text-gray-700 dark:text-gray-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeFeedback}
                  onChange={(e) => setIncludeFeedback(e.target.checked)}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span>Include Modal Feedback & Explanations (&lt;modalFeedback&gt;)</span>
              </label>

              <label className="flex items-center space-x-2 text-xs text-gray-700 dark:text-gray-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeRubrics}
                  onChange={(e) => setIncludeRubrics(e.target.checked)}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span>Include Scoring Rubrics and Response Declarations</span>
              </label>
            </div>

            {exportSuccess && (
              <div className="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg p-3 text-xs text-green-800 dark:text-green-300 flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                <span>
                  QTI package compiled successfully: <strong>examhub-qti-export-2026.zip</strong> (Contains imsmanifest.xml + 42 assessment items).
                </span>
              </div>
            )}

            <div className="pt-4 border-t border-gray-100 dark:border-gray-700 flex justify-end space-x-3">
              <button
                onClick={handleTriggerExport}
                className="inline-flex items-center space-x-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all"
              >
                <Download className="w-4 h-4" />
                <span>Download QTI ZIP Archive</span>
              </button>
            </div>
          </div>

          <div className="bg-gray-50 dark:bg-gray-900/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700 space-y-4">
            <h4 className="text-xs uppercase font-bold text-gray-500 dark:text-gray-400">
              Package Structure
            </h4>
            <div className="space-y-2 text-xs font-mono text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
              <div className="text-blue-600 dark:text-blue-400 font-bold">📦 qti_package.zip</div>
              <div className="pl-4">├── 📄 imsmanifest.xml</div>
              <div className="pl-4">├── 📁 items/</div>
              <div className="pl-8">├── 📄 item_001.xml</div>
              <div className="pl-8">├── 📄 item_002.xml</div>
              <div className="pl-8">└── 📄 item_042.xml</div>
              <div className="pl-4">└── 📁 media/</div>
              <div className="pl-8">└── 🖼️ diagram_01.png</div>
            </div>
            <p className="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">
              Standard IMS manifest metadata ensures seamless 1-click import into standard LMS platforms.
            </p>
          </div>
        </div>
      )}

      {activeTab === 'import' && (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700 text-center max-w-xl mx-auto shadow-sm">
          <div className="w-16 h-16 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-blue-100 dark:border-blue-800">
            <Upload className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
            Import QTI Package Archive
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-6">
            Upload .zip archive containing imsmanifest.xml and valid QTI 2.1 / 3.0 assessmentItem XMLs.
          </p>

          <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-6 hover:border-blue-500 transition-colors cursor-pointer bg-gray-50/50 dark:bg-gray-900/20 mb-6">
            <Package className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <span className="text-xs font-medium text-gray-700 dark:text-gray-300 block">
              Drag and drop your QTI .zip file here, or browse
            </span>
            <span className="text-[10px] text-gray-400">Maximum archive size: 50 MB</span>
          </div>

          <button className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm">
            Select Archive File
          </button>
        </div>
      )}

      {activeTab === 'xml_editor' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2 text-xs font-semibold text-gray-700 dark:text-gray-300">
              <Code2 className="w-4 h-4 text-blue-600" />
              <span>QTI 2.1 Raw AssessmentItem XML</span>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopyXML}
                className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy XML'}</span>
              </button>
              <button
                onClick={handleValidateXML}
                className="inline-flex items-center space-x-1 px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Validate Schema</span>
              </button>
            </div>
          </div>

          <textarea
            value={xmlContent}
            onChange={(e) => setXmlContent(e.target.value)}
            className="w-full h-80 p-4 font-mono text-xs bg-gray-900 text-emerald-400 rounded-xl border border-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 leading-relaxed"
          />

          {validationResult && (
            <div
              className={`p-4 rounded-xl text-xs flex items-start space-x-3 border ${
                validationResult.valid
                  ? 'bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800 text-green-900 dark:text-green-200'
                  : 'bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800 text-red-900 dark:text-red-200'
              }`}
            >
              {validationResult.valid ? (
                <CheckCircle2 className="w-5 h-5 text-green-600 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
              )}
              <div>
                <div className="font-bold">
                  {validationResult.valid ? 'QTI 2.1 XML Valid' : 'Schema Validation Error'}
                </div>
                <div className="text-[11px] mt-0.5 opacity-90">
                  {validationResult.valid
                    ? `Item identifier: "${validationResult.identifier}" with ${validationResult.choicesCount} choice interactions detected.`
                    : validationResult.error}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
