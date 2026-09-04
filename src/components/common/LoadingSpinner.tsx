import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', label, className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  }[size];

  return (
    <div id="loading-spinner-container" className={`flex flex-col items-center justify-center gap-3 p-4 ${className}`}>
      <div
        id="loading-spinner-circle"
        className={`${sizeClasses} border-stone-200 border-t-amber-600 rounded-full animate-spin`}
      />
      {label && <p id="loading-spinner-label" className="text-xs font-medium text-stone-600 tracking-wide">{label}</p>}
    </div>
  );
};
