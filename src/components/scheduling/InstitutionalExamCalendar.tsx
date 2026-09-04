import React, { useState } from 'react';
import {
  Calendar as CalendarIcon,
  Clock,
  MapPin,
  Users,
  AlertTriangle,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Plus,
  Filter
} from 'lucide-react';

interface ExamSlot {
  id: string;
  time: string;
  courseCode: string;
  courseName: string;
  room: string;
  candidatesCount: number;
  invigilators: string[];
  hasConflict: boolean;
  conflictDetails?: string;
}

export const InstitutionalExamCalendar: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState('2026-09-14');
  const [filterRoom, setFilterRoom] = useState('ALL');

  const slots: ExamSlot[] = [
    {
      id: 'slot-1',
      time: '09:00 – 11:00',
      courseCode: 'CS201',
      courseName: 'Algorithms & Data Structures',
      room: 'Hall A (Auditorium)',
      candidatesCount: 120,
      invigilators: ['Prof. Alan Turing', 'Dr. Grace Hopper'],
      hasConflict: false
    },
    {
      id: 'slot-2',
      time: '09:00 – 11:00',
      courseCode: 'EE102',
      courseName: 'Digital Logic & Circuit Design',
      room: 'Lab 3 (Computer Lab)',
      candidatesCount: 45,
      invigilators: ['Dr. Claude Shannon'],
      hasConflict: false
    },
    {
      id: 'slot-3',
      time: '11:30 – 13:30',
      courseCode: 'CS301',
      courseName: 'Distributed Systems & Cloud Computing',
      room: 'Hall A (Auditorium)',
      candidatesCount: 110,
      invigilators: ['Prof. Leslie Lamport', 'Dr. Barbara Liskov'],
      hasConflict: false
    },
    {
      id: 'slot-4',
      time: '14:30 – 16:30',
      courseCode: 'CS401',
      courseName: 'Applied Cryptography & Cyber Security',
      room: 'Hall B (Science Block)',
      candidatesCount: 85,
      invigilators: ['Prof. Ron Rivest'],
      hasConflict: true,
      conflictDetails: 'Invigilator Prof. Rivest double-booked with Faculty Senate meeting at 15:00.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <CalendarIcon className="w-4 h-4" />
            <span>Facility Timetabling & Conflict Resolution</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Institutional Examination Timetable & Seating
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Automated conflict-free room allocation, invigilator duty assignments, and candidate seating matrices.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
            <button className="p-1.5 text-gray-600 dark:text-gray-300 hover:text-gray-900 rounded">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold px-2 text-gray-800 dark:text-gray-200">
              Week 3: Sep 14 – Sep 18, 2026
            </span>
            <button className="p-1.5 text-gray-600 dark:text-gray-300 hover:text-gray-900 rounded">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <button className="inline-flex items-center space-x-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm">
            <Plus className="w-4 h-4" />
            <span>Schedule Session</span>
          </button>
        </div>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs text-gray-400 font-medium">Scheduled Exams (Day)</span>
          <div className="text-2xl font-black text-gray-900 dark:text-white font-mono mt-1">4 Sessions</div>
          <span className="text-[11px] text-green-600 font-semibold">Across 3 physical venues</span>
        </div>

        <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs text-gray-400 font-medium">Total Seated Candidates</span>
          <div className="text-2xl font-black text-gray-900 dark:text-white font-mono mt-1">360 Students</div>
          <span className="text-[11px] text-blue-600 font-semibold">Checkerboard spacing applied</span>
        </div>

        <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs text-gray-400 font-medium">Assigned Invigilators</span>
          <div className="text-2xl font-black text-gray-900 dark:text-white font-mono mt-1">6 Faculty</div>
          <span className="text-[11px] text-teal-600 font-semibold">Neutral department roster</span>
        </div>

        <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs text-gray-400 font-medium">CSP Conflict Engine</span>
          <div className="text-2xl font-black text-amber-600 dark:text-amber-400 font-mono mt-1">1 Warning</div>
          <span className="text-[11px] text-amber-600 font-semibold">Faculty availability clash</span>
        </div>
      </div>

      {/* Timetable Session Cards */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
          Sessions for Monday, September 14, 2026
        </h3>

        <div className="space-y-3">
          {slots.map((slot) => (
            <div
              key={slot.id}
              className={`p-4 rounded-xl border transition-all ${
                slot.hasConflict
                  ? 'border-amber-300 dark:border-amber-800 bg-amber-50/40 dark:bg-amber-950/20'
                  : 'border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/30'
              }`}
            >
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300 font-bold font-mono text-xs">
                      {slot.courseCode}
                    </span>
                    <span className="text-xs font-semibold text-gray-500 flex items-center space-x-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{slot.time}</span>
                    </span>
                    <span className="text-xs font-semibold text-gray-500 flex items-center space-x-1">
                      <MapPin className="w-3.5 h-3.5 text-red-500" />
                      <span>{slot.room}</span>
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-gray-900 dark:text-white">
                    {slot.courseName}
                  </h4>
                </div>

                <div className="flex items-center space-x-6 text-xs text-gray-600 dark:text-gray-300">
                  <div className="flex items-center space-x-1.5">
                    <Users className="w-4 h-4 text-gray-400" />
                    <span><strong>{slot.candidatesCount}</strong> Candidates</span>
                  </div>
                  <div>
                    <span className="text-gray-400 block text-[10px]">Invigilators</span>
                    <span className="font-semibold">{slot.invigilators.join(', ')}</span>
                  </div>
                  <div>
                    <button className="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-xs font-semibold hover:bg-gray-50">
                      Seating Map
                    </button>
                  </div>
                </div>
              </div>

              {slot.hasConflict && (
                <div className="mt-3 pt-3 border-t border-amber-200 dark:border-amber-800 text-xs text-amber-800 dark:text-amber-300 flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                  <span><strong>Schedule Conflict:</strong> {slot.conflictDetails}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
