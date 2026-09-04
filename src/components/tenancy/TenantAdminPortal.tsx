import React, { useState } from 'react';
import {
  Building2,
  Globe,
  KeyRound,
  Database,
  Users,
  HardDrive,
  CheckCircle2,
  Shield,
  Palette,
  ExternalLink,
  Settings
} from 'lucide-react';

export const TenantAdminPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'general' | 'branding' | 'sso' | 'quotas'>('general');
  const [orgName, setOrgName] = useState('Apex Polytechnic Institute');
  const [customDomain, setCustomDomain] = useState('exams.apex.edu');
  const [primaryColor, setPrimaryColor] = useState('#0f766e');
  const [welcomeMessage, setWelcomeMessage] = useState('Welcome to Apex Secure Testing Portal.');
  const [ssoEnabled, setSsoEnabled] = useState(true);
  const [ssoIssuer, setSsoIssuer] = useState('https://login.microsoftonline.com/tenant-guid/v2.0');
  const [ssoClientId, setSsoClientId] = useState('azure-client-apex-01');

  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-teal-600 dark:text-teal-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Building2 className="w-4 h-4" />
            <span>Institutional Multi-Tenancy Engine</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Tenant Administration & White-Label Settings
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Configure custom domains, Single Sign-On (SAML 2.0 / Entra ID), institutional themes, and license quotas.
          </p>
        </div>

        <div className="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setActiveTab('general')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'general'
                ? 'bg-white dark:bg-gray-800 text-teal-600 dark:text-teal-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            General & Domain
          </button>
          <button
            onClick={() => setActiveTab('branding')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'branding'
                ? 'bg-white dark:bg-gray-800 text-teal-600 dark:text-teal-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Branding
          </button>
          <button
            onClick={() => setActiveTab('sso')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'sso'
                ? 'bg-white dark:bg-gray-800 text-teal-600 dark:text-teal-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            SSO / SAML
          </button>
          <button
            onClick={() => setActiveTab('quotas')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'quotas'
                ? 'bg-white dark:bg-gray-800 text-teal-600 dark:text-teal-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Usage & Quotas
          </button>
        </div>
      </div>

      {savedSuccess && (
        <div className="p-3 bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg text-xs text-green-800 dark:text-green-300 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
          <span>Tenant configuration updated and cached across gateway edge instances.</span>
        </div>
      )}

      {activeTab === 'general' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
          <h3 className="text-base font-bold text-gray-900 dark:text-white">
            Organization Identity & Domain Routing
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Institution Name
              </label>
              <input
                type="text"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                className="w-full text-sm p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Custom Domain (FQDN)
              </label>
              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={customDomain}
                  onChange={(e) => setCustomDomain(e.target.value)}
                  className="flex-1 text-sm p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono"
                />
                <span className="text-xs px-2.5 py-2 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 rounded-lg font-bold">
                  SSL Active
                </span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-400 space-y-1">
            <span className="font-semibold text-gray-800 dark:text-gray-200 block">DNS CNAME Delegation</span>
            <p>
              Point your subdomain DNS record (e.g. <code>exams.apex.edu</code>) to <code>cname.examhub.io</code>.
              Automated TLS certificate provisioning via Let's Encrypt with zero maintenance.
            </p>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={handleSave}
              className="px-5 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-semibold shadow-sm"
            >
              Save Organization Settings
            </button>
          </div>
        </div>
      )}

      {activeTab === 'branding' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
          <h3 className="text-base font-bold text-gray-900 dark:text-white">
            Portal Customization & Theming
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Primary Brand Color
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="color"
                  value={primaryColor}
                  onChange={(e) => setPrimaryColor(e.target.value)}
                  className="w-10 h-10 rounded cursor-pointer border border-gray-300 dark:border-gray-600"
                />
                <input
                  type="text"
                  value={primaryColor}
                  onChange={(e) => setPrimaryColor(e.target.value)}
                  className="text-xs p-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono uppercase"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Candidate Welcome Header
              </label>
              <input
                type="text"
                value={welcomeMessage}
                onChange={(e) => setWelcomeMessage(e.target.value)}
                className="w-full text-sm p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={handleSave}
              className="px-5 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-semibold shadow-sm"
            >
              Apply Brand Theme
            </button>
          </div>
        </div>
      )}

      {activeTab === 'sso' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-base font-bold text-gray-900 dark:text-white">
              SAML 2.0 / OpenID Connect Enterprise Federation
            </h3>
            <label className="flex items-center space-x-2 text-xs font-semibold cursor-pointer">
              <input
                type="checkbox"
                checked={ssoEnabled}
                onChange={(e) => setSsoEnabled(e.target.checked)}
                className="rounded text-teal-600"
              />
              <span>Enable SSO Authentication</span>
            </label>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Identity Provider (IdP) Issuer / Authority URL
              </label>
              <input
                type="text"
                value={ssoIssuer}
                onChange={(e) => setSsoIssuer(e.target.value)}
                className="w-full text-xs p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Application Client ID (Audience)
              </label>
              <input
                type="text"
                value={ssoClientId}
                onChange={(e) => setSsoClientId(e.target.value)}
                className="w-full text-xs p-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={handleSave}
              className="px-5 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-semibold shadow-sm"
            >
              Save Federation Credentials
            </button>
          </div>
        </div>
      )}

      {activeTab === 'quotas' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 text-teal-600 dark:text-teal-400">
              <Users className="w-5 h-5" />
              <span className="text-xs uppercase font-bold">Active Enrolled Candidates</span>
            </div>
            <div className="text-3xl font-extrabold text-gray-900 dark:text-white font-mono">
              2,840 <span className="text-sm font-normal text-gray-400">/ 10,000</span>
            </div>
            <div className="w-full bg-gray-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
              <div className="bg-teal-600 h-full" style={{ width: '28.4%' }} />
            </div>
            <span className="text-[11px] text-gray-500 block">Enterprise Tier License: 28% utilized</span>
          </div>

          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 text-blue-600 dark:text-blue-400">
              <HardDrive className="w-5 h-5" />
              <span className="text-xs uppercase font-bold">Encrypted Artifact Storage</span>
            </div>
            <div className="text-3xl font-extrabold text-gray-900 dark:text-white font-mono">
              42.6 <span className="text-sm font-normal text-gray-400">/ 500 GB</span>
            </div>
            <div className="w-full bg-gray-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
              <div className="bg-blue-600 h-full" style={{ width: '8.5%' }} />
            </div>
            <span className="text-[11px] text-gray-500 block">Proctoring video, audit logs, and PDF certificates</span>
          </div>

          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400">
              <Shield className="w-5 h-5" />
              <span className="text-xs uppercase font-bold">Concurrent Live Exams</span>
            </div>
            <div className="text-3xl font-extrabold text-gray-900 dark:text-white font-mono">
              12 <span className="text-sm font-normal text-gray-400">/ 100</span>
            </div>
            <div className="w-full bg-gray-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
              <div className="bg-indigo-600 h-full" style={{ width: '12%' }} />
            </div>
            <span className="text-[11px] text-gray-500 block">Live proctored candidate sessions concurrently active</span>
          </div>
        </div>
      )}
    </div>
  );
};
