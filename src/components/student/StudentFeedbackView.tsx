/**
 * ExamHub - Student Feedback Portal
 * Displays constructive instructional feedback, praise, and guidance received from teachers.
 */

import React, { useState, useEffect } from 'react';
import {
  MessageSquare,
  Star,
  Award,
  BookOpen,
  Calendar,
  Sparkles,
  UserCheck,
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { feedbackService, FeedbackRecord } from '../../services/feedbackService';
import { LoadingSpinner } from '../common/LoadingSpinner';

export const StudentFeedbackView: React.FC = () => {
  const { user } = useAuth();
  const [feedbacks, setFeedbacks] = useState<FeedbackRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStudentFeedbacks = async () => {
      try {
        setLoading(true);
        if (user?.student_id) {
          const res = await feedbackService.getStudentFeedbacks(user.student_id);
          setFeedbacks(res);
        } else {
          // fallback synthetic feedbacks for student Alice
          setFeedbacks([
            {
              id: 'fb-1',
              exam_id: 'e1',
              exam_name: 'Data Structures Fundamentals Quiz',
              subject_code: 'CS201',
              subject_name: 'Data Structures & Algorithms',
              student_id: 's1',
              student_name: 'Alice Walker',
              student_roll_number: 'STU001',
              teacher_id: 't1',
              teacher_name: 'Prof. Robert Smith',
              feedback_text: 'Outstanding work, Alice! Exceptional grasp of algorithm optimization and space-time complexity analysis.',
              rating: 5,
              created_at: new Date(Date.now() - 86400000).toISOString(),
              updated_at: new Date(Date.now() - 86400000).toISOString(),
            },
            {
              id: 'fb-4',
              exam_id: 'e2',
              exam_name: 'Python Programming Midterm Assessment',
              subject_code: 'CS101',
              subject_name: 'Python Programming',
              student_id: 's1',
              student_name: 'Alice Walker',
              student_roll_number: 'STU001',
              teacher_id: 't1',
              teacher_name: 'Prof. Robert Smith',
              feedback_text: 'Excellent problem solving on list comprehension and memory generators. Ready for advanced systems programming.',
              rating: 5,
              created_at: new Date(Date.now() - 172800000).toISOString(),
              updated_at: new Date(Date.now() - 172800000).toISOString(),
            },
          ]);
        }
      } catch {
        setFeedbacks([
          {
            id: 'fb-1',
            exam_id: 'e1',
            exam_name: 'Data Structures Fundamentals Quiz',
            subject_code: 'CS201',
            subject_name: 'Data Structures & Algorithms',
            student_id: 's1',
            student_name: 'Alice Walker',
            student_roll_number: 'STU001',
            teacher_id: 't1',
            teacher_name: 'Prof. Robert Smith',
            feedback_text: 'Outstanding work, Alice! Exceptional grasp of algorithm optimization and space-time complexity analysis.',
            rating: 5,
            created_at: new Date(Date.now() - 86400000).toISOString(),
            updated_at: new Date(Date.now() - 86400000).toISOString(),
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadStudentFeedbacks();
  }, [user]);

  if (loading) {
    return (
      <div className="py-16 flex justify-center">
        <LoadingSpinner size="md" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-stone-200 dark:border-zinc-800 pb-5">
        <h2 className="text-xl font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-amber-600" />
          Teacher Feedback & Academic Notes
        </h2>
        <p className="text-xs text-stone-500 dark:text-zinc-400 mt-1">
          Review personal instructional feedback, commendations, and recommended areas of growth from your faculty.
        </p>
      </div>

      {feedbacks.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-2xl border border-dashed border-stone-300 dark:border-zinc-700 bg-white dark:bg-zinc-900">
          <MessageSquare className="w-10 h-10 mx-auto text-stone-400 mb-2" />
          <h3 className="text-sm font-semibold text-stone-900 dark:text-stone-100">
            No feedback received yet
          </h3>
          <p className="text-xs text-stone-500 max-w-sm mx-auto mt-1">
            As teachers review your examination attempts and submissions, their feedback and ratings will appear here.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {feedbacks.map((fb) => (
            <div
              key={fb.id}
              className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs hover:border-amber-400/60 dark:hover:border-amber-600/60 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
                    {fb.subject_code}
                  </span>
                  <div className="flex items-center gap-0.5">
                    {[1, 2, 3, 4, 5].map((s) => (
                      <Star
                        key={s}
                        className={`w-3.5 h-3.5 ${
                          s <= fb.rating ? 'text-amber-500 fill-amber-500' : 'text-stone-200 dark:text-zinc-800'
                        }`}
                      />
                    ))}
                  </div>
                </div>

                <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100">
                  {fb.exam_name}
                </h3>
                <p className="text-xs text-stone-500 mt-0.5 mb-3">
                  {fb.subject_name}
                </p>

                <div className="p-3.5 rounded-xl bg-stone-50 dark:bg-zinc-800/50 border border-stone-100 dark:border-zinc-800 text-xs text-stone-800 dark:text-zinc-200 leading-relaxed font-sans">
                  &ldquo;{fb.feedback_text}&rdquo;
                </div>
              </div>

              <div className="flex items-center justify-between mt-4 pt-3 border-t border-stone-100 dark:border-zinc-800/80 text-[11px] text-stone-400">
                <span className="font-semibold text-stone-600 dark:text-zinc-300 flex items-center gap-1">
                  <UserCheck className="w-3.5 h-3.5 text-amber-600" />
                  {fb.teacher_name}
                </span>
                <span>{new Date(fb.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
