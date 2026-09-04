"""
ExamHub Collusion Detector
Performs cross-candidate pairwise submission comparison within cohorts,
analyzing textual overlap, temporal proximity, and source collusion.
"""

from typing import List, Dict, Tuple, Any
from backend.app.plagiarism.schemas import CandidateCollusionRecord, PlagiarismScanRequest
from backend.app.plagiarism.fingerprint_engine import WinnowingEngine


class CollusionDetector:
    """
    Identifies unauthorized collaboration, shared answers, and mutual copying
    across all candidate submissions for a specific exam item.
    """

    @classmethod
    def analyze_cohort_submissions(
        cls,
        submissions: List[Dict[str, Any]],
        request: PlagiarismScanRequest
    ) -> List[CandidateCollusionRecord]:
        """
        Runs O(N^2) pairwise fingerprint comparison across cohort submissions.
        """
        # Precompute fingerprints
        fingerprint_map = {}
        for sub in submissions:
            cid = sub["candidate_id"]
            text = sub.get("content", "")
            fps = WinnowingEngine.compute_fingerprints(
                text=text,
                k=request.k_gram_length,
                w=request.window_size
            )
            fingerprint_map[cid] = (fps, sub)

        results: List[CandidateCollusionRecord] = []
        candidate_ids = list(fingerprint_map.keys())

        for i in range(len(candidate_ids)):
            for j in range(i + 1, len(candidate_ids)):
                cid_a = candidate_ids[i]
                cid_b = candidate_ids[j]

                fps_a, sub_a = fingerprint_map[cid_a]
                fps_b, sub_b = fingerprint_map[cid_b]

                jaccard, shared_count = WinnowingEngine.calculate_jaccard_similarity(fps_a, fps_b)
                similarity_pct = round(jaccard * 100.0, 1)

                if jaccard >= request.similarity_threshold:
                    ip_match = (sub_a.get("ip_address") and sub_a.get("ip_address") == sub_b.get("ip_address"))
                    
                    verdict = "Clear"
                    if similarity_pct >= 80.0:
                        verdict = "Severe Collusion / Direct Plagiarism"
                    elif similarity_pct >= 50.0:
                        verdict = "Suspicious Substantial Overlap"
                    elif similarity_pct >= 30.0:
                        verdict = "Moderate Similarity (Common Template)"

                    rec = CandidateCollusionRecord(
                        candidate_id_a=cid_a,
                        candidate_id_b=cid_b,
                        similarity_percentage=similarity_pct,
                        shared_fingerprints_count=shared_count,
                        total_fingerprints_a=len(fps_a),
                        total_fingerprints_b=len(fps_b),
                        temporal_proximity_seconds=abs(sub_a.get("timestamp", 0) - sub_b.get("timestamp", 0)),
                        ip_match=bool(ip_match),
                        verdict=verdict
                    )
                    results.append(rec)

        results.sort(key=lambda r: r.similarity_percentage, reverse=True)
        return results
