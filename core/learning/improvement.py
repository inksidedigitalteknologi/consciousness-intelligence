
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# IMPROVEMENT ENGINE
#
# Version: 2.0
#
# ============================================================
#
# RESPONSIBILITIES
#
# - Detect system weaknesses
# - Evaluate system performance
# - Analyze multiple metrics
# - Generate improvement recommendations
# - Score improvement opportunities
# - Create improvement plans
# - Track changes
# - Evaluate change outcomes
# - Compare before / after performance
# - Detect performance trends
# - Generate adaptive feedback
# - Generate lessons
# - Link improvements to goals
# - Track successful / failed improvements
# - Search improvement history
# - Improvement statistics
# - System status
# - Backward compatibility
#
# ============================================================

import logging
import re
from copy import deepcopy
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

VERSION = "2.0"


# ============================================================
#
# TIME HELPER
#
# ============================================================

def utc_now():
    """
    Return current UTC timestamp.
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ============================================================
#
# IMPROVEMENT ENGINE
#
# ============================================================

class ImprovementEngine:

    MAX_CHANGES = 2000
    MAX_SUGGESTIONS = 1000
    MAX_PERFORMANCE_HISTORY = 1000
    MAX_PLANS = 500

    # --------------------------------------------------------
    # PERFORMANCE THRESHOLDS
    # --------------------------------------------------------

    ACCURACY_CRITICAL = 40
    ACCURACY_WARNING = 60
    ACCURACY_GOOD = 80

    ERROR_CRITICAL = 25
    ERROR_WARNING = 10

    PERFORMANCE_CRITICAL = 40
    PERFORMANCE_WARNING = 60

    CONFIDENCE_WARNING = 55

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(
        self,
        max_changes=MAX_CHANGES,
        max_suggestions=MAX_SUGGESTIONS,
        max_performance_history=MAX_PERFORMANCE_HISTORY,
        max_plans=MAX_PLANS
    ):

        self.max_changes = max(
            1,
            int(max_changes)
        )

        self.max_suggestions = max(
            1,
            int(max_suggestions)
        )

        self.max_performance_history = max(
            1,
            int(max_performance_history)
        )

        self.max_plans = max(
            1,
            int(max_plans)
        )

        self.improvement_count = 0

        self.changes = []

        self.performance_history = []

        self.suggestions = []

        self.plans = []

        self.feedback_history = []

        self.lessons = []

        self.successful_changes = 0

        self.failed_changes = 0

        self.pending_changes = 0

        self.last_analysis = None

        self.last_change = None

        self.last_plan = None

        self.last_feedback = None

        logger.info(
            "Improvement Engine v%s initialized.",
            VERSION
        )

    # ========================================================
    #
    # NORMALIZE METRICS
    #
    # ========================================================

    def normalize_metrics(
        self,
        metrics
    ):
        """
        Normalize performance metrics into a safe dictionary.
        """

        if metrics is None:
            return {}

        if not isinstance(
            metrics,
            dict
        ):
            return {}

        result = {}

        for key, value in metrics.items():

            normalized_key = re.sub(
                r"\s+",
                "_",
                str(key).strip().lower()
            )

            result[normalized_key] = value

        return result

    # ========================================================
    #
    # SAFE NUMBER
    #
    # ========================================================

    def _number(
        self,
        value,
        default=0.0
    ):

        try:
            return float(value)

        except (
            TypeError,
            ValueError
        ):
            return float(default)

    # ========================================================
    #
    # CLAMP
    #
    # ========================================================

    def _clamp(
        self,
        value,
        minimum=0,
        maximum=100
    ):

        value = self._number(
            value,
            minimum
        )

        return max(
            minimum,
            min(
                maximum,
                value
            )
        )

    # ========================================================
    #
    # DETECT WEAKNESSES
    #
    # ========================================================

    def detect_weaknesses(
        self,
        metrics
    ):
        """
        Detect system weaknesses from available metrics.
        """

        metrics = self.normalize_metrics(
            metrics
        )

        weaknesses = []

        accuracy = self._clamp(
            metrics.get(
                "accuracy",
                0
            )
        )

        errors = max(
            0,
            self._number(
                metrics.get(
                    "errors",
                    0
                )
            )
        )

        performance = self._clamp(
            metrics.get(
                "performance",
                metrics.get(
                    "speed",
                    100
                )
            )
        )

        confidence = self._clamp(
            metrics.get(
                "confidence",
                100
            )
        )

        latency = max(
            0,
            self._number(
                metrics.get(
                    "latency",
                    0
                )
            )
        )

        memory_usage = self._clamp(
            metrics.get(
                "memory_usage",
                0
            )
        )

        # ----------------------------------------------------
        # ACCURACY
        # ----------------------------------------------------

        if accuracy < self.ACCURACY_CRITICAL:

            weaknesses.append({
                "type": "accuracy",
                "severity": "CRITICAL",
                "score": 100 - accuracy,
                "value": accuracy
            })

        elif accuracy < self.ACCURACY_WARNING:

            weaknesses.append({
                "type": "accuracy",
                "severity": "HIGH",
                "score": 100 - accuracy,
                "value": accuracy
            })

        # ----------------------------------------------------
        # ERROR RATE
        # ----------------------------------------------------

        if errors >= self.ERROR_CRITICAL:

            weaknesses.append({
                "type": "errors",
                "severity": "CRITICAL",
                "score": min(
                    100,
                    errors * 3
                ),
                "value": errors
            })

        elif errors > self.ERROR_WARNING:

            weaknesses.append({
                "type": "errors",
                "severity": "HIGH",
                "score": min(
                    100,
                    errors * 3
                ),
                "value": errors
            })

        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        if performance < self.PERFORMANCE_CRITICAL:

            weaknesses.append({
                "type": "performance",
                "severity": "CRITICAL",
                "score": 100 - performance,
                "value": performance
            })

        elif performance < self.PERFORMANCE_WARNING:

            weaknesses.append({
                "type": "performance",
                "severity": "HIGH",
                "score": 100 - performance,
                "value": performance
            })

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        if confidence < self.CONFIDENCE_WARNING:

            weaknesses.append({
                "type": "confidence",
                "severity": "MEDIUM",
                "score": 100 - confidence,
                "value": confidence
            })

        # ----------------------------------------------------
        # LATENCY
        # ----------------------------------------------------

        if latency > 1000:

            weaknesses.append({
                "type": "latency",
                "severity": "HIGH",
                "score": min(
                    100,
                    latency / 10
                ),
                "value": latency
            })

        elif latency > 500:

            weaknesses.append({
                "type": "latency",
                "severity": "MEDIUM",
                "score": min(
                    100,
                    latency / 10
                ),
                "value": latency
            })

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        if memory_usage >= 90:

            weaknesses.append({
                "type": "memory_usage",
                "severity": "CRITICAL",
                "score": memory_usage,
                "value": memory_usage
            })

        elif memory_usage >= 75:

            weaknesses.append({
                "type": "memory_usage",
                "severity": "HIGH",
                "score": memory_usage,
                "value": memory_usage
            })

        weaknesses.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return weaknesses

    # ========================================================
    #
    # GENERATE RECOMMENDATIONS
    #
    # ========================================================

    def generate_recommendations(
        self,
        weaknesses
    ):
        """
        Generate actionable recommendations.
        """

        recommendations = []

        recommendation_map = {

            "accuracy": (
                "Review prediction features, "
                "training data and decision thresholds."
            ),

            "errors": (
                "Improve validation, exception handling "
                "and input safety."
            ),

            "performance": (
                "Optimize processing pipeline, "
                "parallel execution and expensive operations."
            ),

            "confidence": (
                "Improve evidence quality, "
                "multi-factor validation and confidence calibration."
            ),

            "latency": (
                "Reduce unnecessary computation, "
                "optimize I/O and improve asynchronous execution."
            ),

            "memory_usage": (
                "Optimize memory retention, "
                "cleanup stale objects and limit historical data."
            )
        }

        priority_map = {
            "CRITICAL": 100,
            "HIGH": 80,
            "MEDIUM": 60,
            "LOW": 30
        }

        for weakness in weaknesses:

            weakness_type = weakness.get(
                "type"
            )

            severity = weakness.get(
                "severity",
                "LOW"
            )

            recommendation = recommendation_map.get(
                weakness_type,
                "Investigate the detected system weakness."
            )

            recommendations.append({

                "type":
                    weakness_type,

                "severity":
                    severity,

                "priority":
                    priority_map.get(
                        severity,
                        20
                    ),

                "score":
                    round(
                        self._number(
                            weakness.get(
                                "score",
                                0
                            )
                        ),
                        2
                    ),

                "recommendation":
                    recommendation

            })

        recommendations.sort(
            key=lambda item: item["priority"],
            reverse=True
        )

        return recommendations

    # ========================================================
    #
    # ANALYZE SYSTEM PERFORMANCE
    #
    # ========================================================

    def analyze(
        self,
        metrics
    ):
        """
        Analyze system performance and produce
        improvement opportunities.
        """

        try:

            metrics = self.normalize_metrics(
                metrics
            )

            weaknesses = self.detect_weaknesses(
                metrics
            )

            recommendations = (
                self.generate_recommendations(
                    weaknesses
                )
            )

            result = {

                "id":
                    self._create_id(
                        "analysis"
                    ),

                "time":
                    utc_now(),

                "metrics":
                    deepcopy(
                        metrics
                    ),

                "weaknesses":
                    weaknesses,

                "recommendations":
                    recommendations,

                "weakness_count":
                    len(
                        weaknesses
                    ),

                "recommendation_count":
                    len(
                        recommendations
                    ),

                "overall_status":
                    self._overall_status(
                        weaknesses
                    )

            }

            self.last_analysis = result

            self.suggestions.append(
                result
            )

            self._trim_history()

            return result

        except Exception as exc:

            logger.exception(
                "Improvement analysis failed: %s",
                exc
            )

            return {

                "time":
                    utc_now(),

                "status":
                    "failed",

                "error":
                    str(exc)

            }

    # ========================================================
    #
    # OVERALL STATUS
    #
    # ========================================================

    def _overall_status(
        self,
        weaknesses
    ):

        if any(
            item.get("severity") == "CRITICAL"
            for item in weaknesses
        ):
            return "CRITICAL"

        if any(
            item.get("severity") == "HIGH"
            for item in weaknesses
        ):
            return "NEEDS_IMPROVEMENT"

        if weaknesses:
            return "MONITOR"

        return "HEALTHY"

    # ========================================================
    #
    # CREATE IMPROVEMENT PLAN
    #
    # ========================================================

    def create_plan(
        self,
        title,
        description="",
        recommendations=None,
        priority="NORMAL",
        goal_id=None,
        target_metric=None
    ):
        """
        Create a structured improvement plan.
        """

        priority = str(
            priority
        ).upper()

        if priority not in {
            "LOW",
            "NORMAL",
            "HIGH",
            "CRITICAL"
        }:
            priority = "NORMAL"

        plan = {

            "id":
                self._create_id(
                    "plan"
                ),

            "created":
                utc_now(),

            "title":
                str(
                    title
                ),

            "description":
                str(
                    description
                ),

            "priority":
                priority,

            "goal_id":
                goal_id,

            "target_metric":
                target_metric,

            "recommendations":
                deepcopy(
                    recommendations
                    if recommendations
                    else []
                ),

            "status":
                "ACTIVE",

            "progress":
                0,

            "changes":
                [],

            "completed_at":
                None

        }

        self.plans.append(
            plan
        )

        self.last_plan = plan

        self._trim_history()

        return plan

    # ========================================================
    #
    # UPDATE PLAN
    #
    # ========================================================

    def update_plan(
        self,
        plan_id,
        progress=None,
        status=None
    ):

        for plan in self.plans:

            if plan.get("id") != plan_id:
                continue

            if progress is not None:

                plan["progress"] = self._clamp(
                    progress
                )

            if status is not None:

                status = str(
                    status
                ).upper()

                allowed = {
                    "ACTIVE",
                    "PAUSED",
                    "COMPLETED",
                    "FAILED",
                    "CANCELLED"
                }

                if status in allowed:

                    plan["status"] = status

                    if status == "COMPLETED":

                        plan["progress"] = 100

                        plan["completed_at"] = (
                            utc_now()
                        )

            return plan

        return None

    # ========================================================
    #
    # RECORD PERFORMANCE
    #
    # ========================================================

    def record_performance(
        self,
        metrics,
        source="system",
        context=None
    ):

        record = {

            "id":
                self._create_id(
                    "performance"
                ),

            "time":
                utc_now(),

            "source":
                source,

            "metrics":
                deepcopy(
                    self.normalize_metrics(
                        metrics
                    )
                ),

            "context":
                deepcopy(
                    context
                ) if isinstance(
                    context,
                    dict
                ) else {}

        }

        self.performance_history.append(
            record
        )

        if len(
            self.performance_history
        ) > self.max_performance_history:

            del self.performance_history[
                :-self.max_performance_history
            ]

        return record

    # ========================================================
    #
    # APPLY CHANGE
    #
    # ========================================================

    def apply_change(
        self,
        component,
        old_value,
        new_value,
        reason,
        plan_id=None,
        goal_id=None,
        expected_metric=None,
        rollback_value=None,
        metadata=None
    ):
        """
        Record an improvement change.

        The engine does not directly mutate external modules.
        It records the change and evaluates its result later.
        """

        change = {

            "id":
                self._create_id(
                    "change"
                ),

            "time":
                utc_now(),

            "component":
                str(
                    component
                ),

            "before":
                deepcopy(
                    old_value
                ),

            "after":
                deepcopy(
                    new_value
                ),

            "reason":
                str(
                    reason
                ),

            "plan_id":
                plan_id,

            "goal_id":
                goal_id,

            "expected_metric":
                expected_metric,

            "rollback_value":
                deepcopy(
                    rollback_value
                ),

            "metadata":
                deepcopy(
                    metadata
                ) if isinstance(
                    metadata,
                    dict
                ) else {},

            "result":
                "pending",

            "evaluated_at":
                None,

            "evaluation":
                None

        }

        self.changes.append(
            change
        )

        self.improvement_count += 1

        self.pending_changes += 1

        self.last_change = change

        if plan_id:

            plan = self._find_plan(
                plan_id
            )

            if plan is not None:

                plan.setdefault(
                    "changes",
                    []
                ).append(
                    change["id"]
                )

        self._trim_history()

        logger.info(
            "Improvement change recorded: %s",
            component
        )

        return change

    # ========================================================
    #
    # EVALUATE CHANGE RESULT
    #
    # ========================================================

    def evaluate_change(
        self,
        change_id,
        success,
        before_metric=None,
        after_metric=None,
        note="",
        metrics=None
    ):
        """
        Evaluate whether an improvement succeeded.
        """

        change = self._find_change(
            change_id
        )

        # Backward compatibility:
        # allow numeric list index.
        if change is None:

            try:

                index = int(
                    change_id
                )

                if (
                    0 <= index
                    < len(self.changes)
                ):

                    change = self.changes[
                        index
                    ]

            except (
                TypeError,
                ValueError
            ):
                pass

        if change is None:

            return False

        success = bool(
            success
        )

        change["result"] = (
            "success"
            if success
            else
            "failed"
        )

        change["evaluated_at"] = (
            utc_now()
        )

        change["evaluation"] = {

            "before_metric":
                before_metric,

            "after_metric":
                after_metric,

            "difference":
                self._difference(
                    before_metric,
                    after_metric
                ),

            "note":
                note,

            "metrics":
                deepcopy(
                    metrics
                ) if isinstance(
                    metrics,
                    dict
                ) else {}

        }

        if self.pending_changes > 0:

            self.pending_changes -= 1

        if success:

            self.successful_changes += 1

        else:

            self.failed_changes += 1

        self._generate_change_lesson(
            change
        )

        return True

    # ========================================================
    #
    # FIND CHANGE
    #
    # ========================================================

    def _find_change(
        self,
        change_id
    ):

        for change in self.changes:

            if change.get(
                "id"
            ) == change_id:

                return change

        return None

    # ========================================================
    #
    # FIND PLAN
    #
    # ========================================================

    def _find_plan(
        self,
        plan_id
    ):

        for plan in self.plans:

            if plan.get(
                "id"
            ) == plan_id:

                return plan

        return None

    # ========================================================
    #
    # COMPARE PERFORMANCE
    #
    # ========================================================

    def compare(
        self,
        before,
        after
    ):
        """
        Compare two numeric performance values.
        """

        before = self._number(
            before
        )

        after = self._number(
            after
        )

        improvement = (
            after - before
        )

        return {

            "before":
                before,

            "after":
                after,

            "difference":
                round(
                    improvement,
                    6
                ),

            "percentage_change":
                round(
                    (
                        improvement
                        / before
                        * 100
                    )
                    if before != 0
                    else 0,
                    3
                ),

            "better":
                improvement > 0,

            "worse":
                improvement < 0,

            "unchanged":
                improvement == 0

        }

    # ========================================================
    #
    # COMPARE METRICS
    #
    # ========================================================

    def compare_metrics(
        self,
        before,
        after
    ):
        """
        Compare multiple performance metrics.
        """

        before = self.normalize_metrics(
            before
        )

        after = self.normalize_metrics(
            after
        )

        keys = set(
            before
        ) | set(
            after
        )

        result = {}

        for key in keys:

            old = self._number(
                before.get(
                    key,
                    0
                )
            )

            new = self._number(
                after.get(
                    key,
                    0
                )
            )

            result[key] = self.compare(
                old,
                new
            )

        return result

    # ========================================================
    #
    # TREND
    #
    # ========================================================

    def trend(
        self,
        metric,
        limit=5
    ):
        """
        Detect whether a metric is improving,
        declining or stable.
        """

        metric = str(
            metric
        ).lower()

        records = self.performance_history[
            -max(
                2,
                int(limit)
            ):
        ]

        values = []

        for record in records:

            value = record.get(
                "metrics",
                {}
            ).get(
                metric
            )

            if value is not None:

                values.append(
                    self._number(
                        value
                    )
                )

        if len(values) < 2:

            return {

                "metric":
                    metric,

                "trend":
                    "unknown",

                "values":
                    values

            }

        first = values[0]

        last = values[-1]

        difference = last - first

        tolerance = max(
            0.01,
            abs(first) * 0.01
        )

        if difference > tolerance:

            direction = "improving"

        elif difference < -tolerance:

            direction = "declining"

        else:

            direction = "stable"

        return {

            "metric":
                metric,

            "trend":
                direction,

            "first":
                first,

            "latest":
                last,

            "difference":
                difference,

            "samples":
                len(values)

        }

    # ========================================================
    #
    # FEEDBACK
    #
    # ========================================================

    def feedback(
        self
    ):
        """
        Generate adaptive feedback from historical changes.
        """

        successful = [
            item
            for item in self.changes
            if item.get(
                "result"
            ) == "success"
        ]

        failed = [
            item
            for item in self.changes
            if item.get(
                "result"
            ) == "failed"
        ]

        pending = [
            item
            for item in self.changes
            if item.get(
                "result"
            ) == "pending"
        ]

        lesson = self.generate_lesson(
            successful,
            failed
        )

        result = {

            "time":
                utc_now(),

            "successful_changes":
                len(successful),

            "failed_changes":
                len(failed),

            "pending_changes":
                len(pending),

            "success_rate":
                round(
                    (
                        len(successful)
                        /
                        (
                            len(successful)
                            +
                            len(failed)
                        )
                        * 100
                    )
                    if (
                        len(successful)
                        +
                        len(failed)
                    ) > 0
                    else 0,
                    2
                ),

            "lesson":
                lesson

        }

        self.feedback_history.append(
            result
        )

        self.last_feedback = result

        return result

    # ========================================================
    #
    # GENERATE LESSON
    #
    # ========================================================

    def generate_lesson(
        self,
        successful,
        failed
    ):
        """
        Generate adaptive learning lesson.
        """

        successful = successful or []

        failed = failed or []

        if (
            not successful
            and not failed
        ):

            return (
                "Insufficient improvement history "
                "for a reliable conclusion."
            )

        if len(successful) > len(failed):

            return (
                "Recent improvements generally "
                "increased system performance. "
                "Continue validating successful changes "
                "and prioritize evidence-based optimization."
            )

        if len(failed) > len(successful):

            return (
                "Recent changes show a higher failure rate. "
                "Future improvements should use smaller changes, "
                "stronger validation and rollback protection."
            )

        return (
            "Improvement results are balanced. "
            "Additional observations are required "
            "before changing optimization strategy."
        )

    # ========================================================
    #
    # CHANGE LESSON
    #
    # ========================================================

    def _generate_change_lesson(
        self,
        change
    ):

        result = change.get(
            "result"
        )

        if result == "success":

            lesson = (
                "Change produced a successful outcome."
            )

        elif result == "failed":

            lesson = (
                "Change failed validation and "
                "should be reviewed before reuse."
            )

        else:

            return None

        item = {

            "time":
                utc_now(),

            "change_id":
                change.get(
                    "id"
                ),

            "component":
                change.get(
                    "component"
                ),

            "result":
                result,

            "lesson":
                lesson

        }

        self.lessons.append(
            item
        )

        return item

    # ========================================================
    #
    # HISTORY
    #
    # ========================================================

    def history(
        self,
        limit=50
    ):

        try:

            limit = int(
                limit
            )

        except (
            TypeError,
            ValueError
        ):

            limit = 50

        if limit <= 0:

            return []

        return self.changes[
            -limit:
        ]

    # ========================================================
    #
    # SEARCH
    #
    # ========================================================

    def search(
        self,
        keyword
    ):

        if keyword is None:

            return []

        keyword = str(
            keyword
        ).lower()

        return [

            item

            for item in self.changes

            if keyword in str(
                item
            ).lower()

        ]

    # ========================================================
    #
    # ACTIVE PLANS
    #
    # ========================================================

    def active_plans(
        self
    ):

        return [

            plan

            for plan in self.plans

            if plan.get(
                "status"
            ) == "ACTIVE"

        ]

    # ========================================================
    #
    # LATEST
    #
    # ========================================================

    def latest(
        self
    ):

        return self.last_analysis

    # ========================================================
    #
    # LATEST CHANGE
    #
    # ========================================================

    def latest_change(
        self
    ):

        return self.last_change

    # ========================================================
    #
    # LATEST PLAN
    #
    # ========================================================

    def latest_plan(
        self
    ):

        return self.last_plan

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ):

        total_evaluated = (
            self.successful_changes
            +
            self.failed_changes
        )

        success_rate = (

            self.successful_changes
            /
            total_evaluated
            * 100

            if total_evaluated > 0

            else 0

        )

        return {

            "version":
                VERSION,

            "improvements":
                self.improvement_count,

            "changes":
                len(
                    self.changes
                ),

            "successful":
                self.successful_changes,

            "failed":
                self.failed_changes,

            "pending":
                self.pending_changes,

            "success_rate":
                round(
                    success_rate,
                    2
                ),

            "suggestions":
                len(
                    self.suggestions
                ),

            "performance_records":
                len(
                    self.performance_history
                ),

            "plans":
                len(
                    self.plans
                ),

            "active_plans":
                len(
                    self.active_plans()
                ),

            "lessons":
                len(
                    self.lessons
                )

        }

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        clear_history=True
    ):

        if clear_history:

            self.changes.clear()

            self.performance_history.clear()

            self.suggestions.clear()

            self.plans.clear()

            self.feedback_history.clear()

            self.lessons.clear()

        self.improvement_count = 0

        self.successful_changes = 0

        self.failed_changes = 0

        self.pending_changes = 0

        self.last_analysis = None

        self.last_change = None

        self.last_plan = None

        self.last_feedback = None

        return True

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ):

        stats = self.statistics()

        return {

            "module":
                "improvement_engine",

            "version":
                VERSION,

            "status":
                "ONLINE",

            "improvements":
                stats["improvements"],

            "changes":
                stats["changes"],

            "successful":
                stats["successful"],

            "failed":
                stats["failed"],

            "pending":
                stats["pending"],

            "success_rate":
                stats["success_rate"],

            "suggestions":
                stats["suggestions"],

            "performance_records":
                stats["performance_records"],

            "plans":
                stats["plans"],

            "active_plans":
                stats["active_plans"],

            "lessons":
                stats["lessons"],

            "has_analysis":
                self.last_analysis is not None,

            "has_latest_change":
                self.last_change is not None,

            "has_latest_plan":
                self.last_plan is not None,

            "has_feedback":
                self.last_feedback is not None

        }

    # ========================================================
    #
    # INTERNAL DIFFERENCE
    #
    # ========================================================

    def _difference(
        self,
        before,
        after
    ):

        if (
            before is None
            or
            after is None
        ):

            return None

        try:

            return (
                float(after)
                -
                float(before)
            )

        except (
            TypeError,
            ValueError
        ):

            return None

    # ========================================================
    #
    # INTERNAL ID
    #
    # ========================================================

    def _create_id(
        self,
        prefix
    ):

        import uuid

        return (
            f"{prefix}_"
            f"{uuid.uuid4().hex}"
        )

    # ========================================================
    #
    # HISTORY CONTROL
    #
    # ========================================================

    def _trim_history(
        self
    ):

        if len(
            self.changes
        ) > self.max_changes:

            del self.changes[
                :-self.max_changes
            ]

        if len(
            self.suggestions
        ) > self.max_suggestions:

            del self.suggestions[
                :-self.max_suggestions
            ]

        if len(
            self.plans
        ) > self.max_plans:

            del self.plans[
                :-self.max_plans
            ]


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

improvement = ImprovementEngine()


# ============================================================
#
# OPTIONAL ALIAS
#
# ============================================================

improvement_engine = improvement


# ============================================================
#
# SELF TEST
#
# ============================================================

def test_improvement_engine():

    engine = ImprovementEngine()

    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    performance = engine.record_performance({

        "accuracy": 52,

        "errors": 15,

        "performance": 45,

        "confidence": 48,

        "latency": 700

    })

    assert performance is not None

    # --------------------------------------------------------
    # Analysis
    # --------------------------------------------------------

    analysis = engine.analyze({

        "accuracy": 52,

        "errors": 15,

        "performance": 45,

        "confidence": 48,

        "latency": 700

    })

    assert analysis["weakness_count"] > 0

    assert (
        analysis["overall_status"]
        in {
            "CRITICAL",
            "NEEDS_IMPROVEMENT",
            "MONITOR",
            "HEALTHY"
        }
    )

    # --------------------------------------------------------
    # Plan
    # --------------------------------------------------------

    plan = engine.create_plan(

        title="Improve prediction quality",

        description=(
            "Improve prediction accuracy "
            "and confidence."
        ),

        recommendations=
            analysis["recommendations"],

        priority="HIGH"

    )

    assert plan["status"] == "ACTIVE"

    # --------------------------------------------------------
    # Change
    # --------------------------------------------------------

    change = engine.apply_change(

        component="prediction_threshold",

        old_value=55,

        new_value=60,

        reason="Improve signal quality",

        plan_id=plan["id"]

    )

    assert change["result"] == "pending"

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    assert engine.evaluate_change(

        change["id"],

        True,

        before_metric=52,

        after_metric=68,

        note="Accuracy improved."

    )

    # --------------------------------------------------------
    # Feedback
    # --------------------------------------------------------

    feedback = engine.feedback()

    assert (
        feedback["successful_changes"]
        == 1
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    stats = engine.statistics()

    assert stats["improvements"] == 1

    assert stats["successful"] == 1

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    status = engine.status()

    assert status["status"] == "ONLINE"

    return {

        "status":
            "PASS",

        "analysis":
            analysis,

        "plan":
            plan,

        "change":
            change,

        "feedback":
            feedback,

        "statistics":
            stats,

        "engine_status":
            status

    }


# ============================================================
#
# MANUAL TEST
#
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(

        level=logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )

    )

    print()
    print("=" * 70)
    print("INKSIDE INTELLIGENCE OS")
    print("IMPROVEMENT ENGINE v2.0")
    print("=" * 70)
    print()

    try:

        result = test_improvement_engine()

        print(
            "TEST STATUS:",
            result["status"]
        )

        print(
            "ANALYSIS STATUS:",
            result[
                "analysis"
            ].get(
                "overall_status"
            )
        )

        print(
            "IMPROVEMENTS:",
            result[
                "statistics"
            ]["improvements"]
        )

        print(
            "SUCCESS RATE:",
            result[
                "statistics"
            ]["success_rate"]
        )

        print(
            "ACTIVE PLANS:",
            result[
                "statistics"
            ]["active_plans"]
        )

        print()
        print("=" * 70)
        print("IMPROVEMENT ENGINE TEST COMPLETE")
        print("=" * 70)

    except Exception as exc:

        logger.exception(
            "Improvement Engine self-test failed."
        )

        print(
            "TEST STATUS: FAIL"
        )

        print(
            "ERROR:",
            exc
        )

