
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SELF DIAGNOSTIC ENGINE
# Version 2.0
#
# ============================================================
#
# RESPONSIBILITIES
# ------------------------------------------------------------
#
# - System health checking
# - Memory diagnostics
# - Error diagnostics
# - Accuracy diagnostics
# - Performance diagnostics
# - Learning diagnostics
# - Context diagnostics
# - Event / handler diagnostics
# - Goal diagnostics
# - Health scoring
# - Severity classification
# - Issue detection
# - Recommendation generation
# - Diagnostic history
# - Latest report
# - Trend analysis
# - Summary statistics
# - Configurable thresholds
# - Safe diagnostic execution
#
# ============================================================

import logging
import uuid
import time

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

DIAGNOSTIC_VERSION = "2.0"


# ============================================================
#
# SEVERITY
#
# ============================================================

SEVERITY_INFO = "INFO"
SEVERITY_WARNING = "WARNING"
SEVERITY_CRITICAL = "CRITICAL"


# ============================================================
#
# HEALTH STATUS
#
# ============================================================

STATUS_HEALTHY = "healthy"
STATUS_NEEDS_ATTENTION = "needs_attention"
STATUS_CRITICAL = "critical"


# ============================================================
#
# DEFAULT THRESHOLDS
#
# ============================================================

DEFAULT_THRESHOLDS = {

    # Memory
    "memory_minimum": 1,

    # Errors
    "errors_warning": 5,
    "errors_critical": 10,

    # Accuracy
    "accuracy_warning": 70,
    "accuracy_critical": 50,

    # Performance
    "performance_warning": 70,
    "performance_critical": 50,

    # Learning
    "learning_minimum": 1,

    # Context
    "context_minimum": 1,

    # Goals
    "goal_warning": 0,

    # Event handlers
    "handler_errors_warning": 3,
    "handler_errors_critical": 10,

}


# ============================================================
#
# TIME HELPER
#
# ============================================================

def utc_now() -> str:
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
# SELF DIAGNOSTIC ENGINE
#
# ============================================================

class SelfDiagnostic:

    """
    Comprehensive health and diagnostic engine.

    The engine receives a system state dictionary and produces
    a normalized diagnostic report.

    Compatible with the original API:

        check()
        latest()
        history()
        status()

    Additional API:

        diagnose()
        summary()
        statistics()
        issues()
        critical_issues()
        warnings()
        trend()
        reset()
        configure_thresholds()
    """

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(
        self,
        max_history: int = 500,
        thresholds: Optional[Dict[str, Any]] = None
    ):

        self.max_history = max(
            1,
            int(max_history)
        )

        self.reports: List[
            Dict[str, Any]
        ] = []

        self.total_checks = 0

        self.total_healthy = 0

        self.total_attention = 0

        self.total_critical = 0

        self.total_issues = 0

        self.total_warnings = 0

        self.total_critical_issues = 0

        self.last_check = None

        self.started_at = utc_now()

        self.enabled = True

        self.thresholds = deepcopy(
            DEFAULT_THRESHOLDS
        )

        if isinstance(
            thresholds,
            dict
        ):

            self.configure_thresholds(
                thresholds
            )

        logger.info(
            "Self Diagnostic Engine v%s initialized.",
            DIAGNOSTIC_VERSION
        )

    # ========================================================
    #
    # CONFIGURE THRESHOLDS
    #
    # ========================================================

    def configure_thresholds(
        self,
        thresholds: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update diagnostic thresholds.
        """

        if not isinstance(
            thresholds,
            dict
        ):

            return deepcopy(
                self.thresholds
            )

        for key, value in thresholds.items():

            if key not in self.thresholds:
                continue

            try:

                self.thresholds[key] = float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                logger.warning(
                    "Invalid diagnostic threshold: %s=%r",
                    key,
                    value
                )

        return deepcopy(
            self.thresholds
        )

    # ========================================================
    #
    # NORMALIZE NUMBER
    #
    # ========================================================

    def _number(
        self,
        value,
        default=0.0
    ) -> float:

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return float(
                default
            )

    # ========================================================
    #
    # NORMALIZE SYSTEM STATE
    #
    # ========================================================

    def _normalize_state(
        self,
        system_state
    ) -> Dict[str, Any]:

        if not isinstance(
            system_state,
            dict
        ):

            return {}

        return system_state

    # ========================================================
    #
    # ADD ISSUE
    #
    # ========================================================

    def _add_issue(
        self,
        report: Dict[str, Any],
        code: str,
        message: str,
        severity: str,
        recommendation: str,
        component: str = "system"
    ) -> None:

        issue = {

            "code":
                code,

            "message":
                message,

            "severity":
                severity,

            "component":
                component,

            "recommendation":
                recommendation,

            "time":
                utc_now()

        }

        report["issues"].append(
            issue
        )

        report["recommendations"].append(
            recommendation
        )

    # ========================================================
    #
    # CHECK MEMORY
    #
    # ========================================================

    def _check_memory(
        self,
        state,
        report
    ):

        memory = self._number(
            state.get(
                "memory",
                state.get(
                    "semantic_memory_items",
                    0
                )
            )
        )

        report["metrics"]["memory"] = memory

        if memory < self.thresholds[
            "memory_minimum"
        ]:

            self._add_issue(

                report,

                "MEMORY_EMPTY",

                "Memory contains no usable records.",

                SEVERITY_WARNING,

                "Store validated observations, knowledge, or experiences.",

                "memory"

            )

    # ========================================================
    #
    # CHECK ERRORS
    #
    # ========================================================

    def _check_errors(
        self,
        state,
        report
    ):

        errors = self._number(
            state.get(
                "errors",
                0
            )
        )

        report["metrics"]["errors"] = errors

        if errors >= self.thresholds[
            "errors_critical"
        ]:

            self._add_issue(

                report,

                "ERROR_RATE_CRITICAL",

                "System error frequency is critically high.",

                SEVERITY_CRITICAL,

                "Inspect recent exceptions, failing modules, and recovery logic.",

                "system"

            )

        elif errors >= self.thresholds[
            "errors_warning"
        ]:

            self._add_issue(

                report,

                "ERROR_RATE_HIGH",

                "System error frequency is elevated.",

                SEVERITY_WARNING,

                "Review recent errors and identify recurring failure patterns.",

                "system"

            )

    # ========================================================
    #
    # CHECK ACCURACY
    #
    # ========================================================

    def _check_accuracy(
        self,
        state,
        report
    ):

        accuracy = self._number(
            state.get(
                "accuracy",
                0
            )
        )

        report["metrics"]["accuracy"] = accuracy

        if accuracy <= 0:

            return

        if accuracy < self.thresholds[
            "accuracy_critical"
        ]:

            self._add_issue(

                report,

                "ACCURACY_CRITICAL",

                "Prediction or evaluation accuracy is critically low.",

                SEVERITY_CRITICAL,

                "Review training data, feature quality, strategy parameters, and evaluation logic.",

                "learning"

            )

        elif accuracy < self.thresholds[
            "accuracy_warning"
        ]:

            self._add_issue(

                report,

                "ACCURACY_LOW",

                "Prediction or evaluation accuracy is below the desired level.",

                SEVERITY_WARNING,

                "Increase learning quality and review recent prediction failures.",

                "learning"

            )

    # ========================================================
    #
    # CHECK PERFORMANCE
    #
    # ========================================================

    def _check_performance(
        self,
        state,
        report
    ):

        performance = self._number(
            state.get(
                "performance",
                state.get(
                    "speed",
                    100
                )
            )
        )

        report["metrics"]["performance"] = performance

        if performance < self.thresholds[
            "performance_critical"
        ]:

            self._add_issue(

                report,

                "PERFORMANCE_CRITICAL",

                "System processing performance is critically degraded.",

                SEVERITY_CRITICAL,

                "Inspect slow modules, blocking operations, network calls, and excessive processing.",

                "performance"

            )

        elif performance < self.thresholds[
            "performance_warning"
        ]:

            self._add_issue(

                report,

                "PERFORMANCE_LOW",

                "System processing performance is below the preferred level.",

                SEVERITY_WARNING,

                "Optimize expensive operations and review processing bottlenecks.",

                "performance"

            )

    # ========================================================
    #
    # CHECK LEARNING
    #
    # ========================================================

    def _check_learning(
        self,
        state,
        report
    ):

        learning = self._number(
            state.get(
                "learning",
                state.get(
                    "learning_events",
                    0
                )
            )
        )

        report["metrics"]["learning"] = learning

        if learning < self.thresholds[
            "learning_minimum"
        ]:

            self._add_issue(

                report,

                "LEARNING_INACTIVE",

                "No learning activity has been detected.",

                SEVERITY_WARNING,

                "Feed validated observations, outcomes, experiences, or knowledge into the learning pipeline.",

                "learning"

            )

    # ========================================================
    #
    # CHECK CONTEXT
    #
    # ========================================================

    def _check_context(
        self,
        state,
        report
    ):

        context = self._number(
            state.get(
                "context",
                state.get(
                    "context_events",
                    0
                )
            )
        )

        report["metrics"]["context"] = context

        if context < self.thresholds[
            "context_minimum"
        ]:

            self._add_issue(

                report,

                "CONTEXT_EMPTY",

                "Context manager contains insufficient context information.",

                SEVERITY_WARNING,

                "Record observations, market states, signals, predictions, decisions, and outcomes.",

                "context"

            )

    # ========================================================
    #
    # CHECK GOALS
    #
    # ========================================================

    def _check_goals(
        self,
        state,
        report
    ):

        goals = self._number(
            state.get(
                "goals",
                0
            )
        )

        active_goals = self._number(
            state.get(
                "active_goals",
                goals
            )
        )

        report["metrics"]["goals"] = goals

        report["metrics"][
            "active_goals"
        ] = active_goals

        if (
            goals <= self.thresholds[
                "goal_warning"
            ]
        ):

            self._add_issue(

                report,

                "NO_GOALS",

                "No active learning or improvement goals are configured.",

                SEVERITY_INFO,

                "Create measurable goals for learning and system improvement.",

                "goal_manager"

            )

    # ========================================================
    #
    # CHECK HANDLER ERRORS
    #
    # ========================================================

    def _check_handlers(
        self,
        state,
        report
    ):

        handler_errors = self._number(
            state.get(
                "handler_errors",
                0
            )
        )

        report["metrics"][
            "handler_errors"
        ] = handler_errors

        if handler_errors >= self.thresholds[
            "handler_errors_critical"
        ]:

            self._add_issue(

                report,

                "HANDLER_ERRORS_CRITICAL",

                "Event handler errors are critically high.",

                SEVERITY_CRITICAL,

                "Inspect event handlers, callbacks, and event payload compatibility.",

                "event_system"

            )

        elif handler_errors >= self.thresholds[
            "handler_errors_warning"
        ]:

            self._add_issue(

                report,

                "HANDLER_ERRORS_HIGH",

                "Event handler errors are elevated.",

                SEVERITY_WARNING,

                "Review failed event handlers and callback exceptions.",

                "event_system"

            )

    # ========================================================
    #
    # CALCULATE HEALTH SCORE
    #
    # ========================================================

    def _calculate_health_score(
        self,
        report
    ) -> float:

        score = 100.0

        for issue in report["issues"]:

            severity = issue.get(
                "severity"
            )

            if severity == SEVERITY_CRITICAL:

                score -= 25

            elif severity == SEVERITY_WARNING:

                score -= 10

            elif severity == SEVERITY_INFO:

                score -= 2

        return round(
            max(
                0.0,
                min(
                    100.0,
                    score
                )
            ),
            2
        )

    # ========================================================
    #
    # CLASSIFY HEALTH
    #
    # ========================================================

    def _classify(
        self,
        report
    ) -> str:

        has_critical = any(

            issue.get(
                "severity"
            ) == SEVERITY_CRITICAL

            for issue
            in report["issues"]

        )

        if has_critical:

            return STATUS_CRITICAL

        if report["health_score"] < 80:

            return STATUS_NEEDS_ATTENTION

        return STATUS_HEALTHY

    # ========================================================
    #
    # CHECK
    # ========================================================

    def check(
        self,
        system_state
    ) -> Dict[str, Any]:
        """
        Run complete system diagnostic.
        """

        start = time.perf_counter()

        report = {

            "id":
                str(
                    uuid.uuid4()
                ),

            "time":
                utc_now(),

            "version":
                DIAGNOSTIC_VERSION,

            "status":
                STATUS_HEALTHY,

            "health_score":
                100.0,

            "issues":
                [],

            "recommendations":
                [],

            "metrics":
                {},

            "checks":
                {},

            "duration":
                0.0,

        }

        if not self.enabled:

            report["status"] = (
                "disabled"
            )

            return report

        try:

            state = self._normalize_state(
                system_state
            )

            # ------------------------------------------------
            # Execute diagnostics
            # ------------------------------------------------

            checks = [

                (
                    "memory",
                    self._check_memory
                ),

                (
                    "errors",
                    self._check_errors
                ),

                (
                    "accuracy",
                    self._check_accuracy
                ),

                (
                    "performance",
                    self._check_performance
                ),

                (
                    "learning",
                    self._check_learning
                ),

                (
                    "context",
                    self._check_context
                ),

                (
                    "goals",
                    self._check_goals
                ),

                (
                    "handlers",
                    self._check_handlers
                ),

            ]

            for check_name, check_function in checks:

                try:

                    before = len(
                        report["issues"]
                    )

                    check_function(
                        state,
                        report
                    )

                    report["checks"][
                        check_name
                    ] = {

                        "status":
                            "PASS"
                            if len(
                                report["issues"]
                            ) == before
                            else
                            "ISSUES_FOUND"

                    }

                except Exception as exc:

                    report["checks"][
                        check_name
                    ] = {

                        "status":
                            "ERROR",

                        "error":
                            str(exc)

                    }

                    self._add_issue(

                        report,

                        "DIAGNOSTIC_CHECK_ERROR",

                        f"Diagnostic check failed: {check_name}",

                        SEVERITY_CRITICAL,

                        f"Repair diagnostic subsystem: {check_name}.",

                        "diagnostic"

                    )

            # ------------------------------------------------
            # Health
            # ------------------------------------------------

            report["health_score"] = (
                self._calculate_health_score(
                    report
                )
            )

            report["status"] = (
                self._classify(
                    report
                )
            )

            # ------------------------------------------------
            # Statistics
            # ------------------------------------------------

            report["issue_count"] = len(
                report["issues"]
            )

            report["warning_count"] = sum(

                1

                for issue
                in report["issues"]

                if issue.get(
                    "severity"
                ) == SEVERITY_WARNING

            )

            report["critical_count"] = sum(

                1

                for issue
                in report["issues"]

                if issue.get(
                    "severity"
                ) == SEVERITY_CRITICAL

            )

            report["info_count"] = sum(

                1

                for issue
                in report["issues"]

                if issue.get(
                    "severity"
                ) == SEVERITY_INFO

            )

            report["duration"] = round(

                time.perf_counter()
                - start,

                6

            )

            # ------------------------------------------------
            # Store report
            # ------------------------------------------------

            self.reports.append(
                report
            )

            if len(
                self.reports
            ) > self.max_history:

                del self.reports[
                    :-self.max_history
                ]

            self.total_checks += 1

            self.total_issues += report[
                "issue_count"
            ]

            self.total_warnings += report[
                "warning_count"
            ]

            self.total_critical_issues += report[
                "critical_count"
            ]

            if report["status"] == STATUS_HEALTHY:

                self.total_healthy += 1

            elif report["status"] == STATUS_CRITICAL:

                self.total_critical += 1

            else:

                self.total_attention += 1

            self.last_check = report

            logger.info(

                "Diagnostic completed: "
                "%s | score=%.2f | issues=%s",

                report["status"],

                report["health_score"],

                report["issue_count"]

            )

            return report

        except Exception as exc:

            logger.exception(
                "Self diagnostic failed: %s",
                exc
            )

            report["status"] = (
                STATUS_CRITICAL
            )

            report["health_score"] = 0.0

            report["issues"].append({

                "code":
                    "DIAGNOSTIC_FAILURE",

                "message":
                    str(exc),

                "severity":
                    SEVERITY_CRITICAL,

                "component":
                    "diagnostic",

                "recommendation":
                    "Inspect the diagnostic engine and supplied system state.",

                "time":
                    utc_now()

            })

            report["issue_count"] = 1

            report["critical_count"] = 1

            report["duration"] = round(

                time.perf_counter()
                - start,

                6

            )

            self.reports.append(
                report
            )

            self.total_checks += 1

            self.total_critical += 1

            self.total_issues += 1

            self.total_critical_issues += 1

            self.last_check = report

            return report

    # ========================================================
    #
    # DIAGNOSE ALIAS
    #
    # ========================================================

    def diagnose(
        self,
        system_state
    ) -> Dict[str, Any]:

        return self.check(
            system_state
        )

    # ========================================================
    #
    # LATEST REPORT
    #
    # ========================================================

    def latest(
        self
    ) -> Optional[Dict[str, Any]]:

        if not self.reports:

            return None

        return self.reports[-1]

    # ========================================================
    #
    # HISTORY
    #
    # ========================================================

    def history(
        self,
        limit=20
    ) -> List[Dict[str, Any]]:

        try:

            limit = int(
                limit
            )

        except (
            TypeError,
            ValueError
        ):

            limit = 20

        if limit <= 0:

            return []

        return self.reports[
            -limit:
        ]

    # ========================================================
    #
    # ISSUES
    #
    # ========================================================

    def issues(
        self,
        severity: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Return issues from latest diagnostic.
        """

        latest = self.latest()

        if not latest:

            return []

        result = list(
            latest.get(
                "issues",
                []
            )
        )

        if severity:

            severity = str(
                severity
            ).upper()

            result = [

                issue

                for issue in result

                if issue.get(
                    "severity"
                ) == severity

            ]

        if limit is not None:

            try:

                limit = int(
                    limit
                )

            except (
                TypeError,
                ValueError
            ):

                limit = len(
                    result
                )

            result = result[
                :max(
                    0,
                    limit
                )
            ]

        return result

    # ========================================================
    #
    # CRITICAL ISSUES
    #
    # ========================================================

    def critical_issues(
        self
    ) -> List[Dict[str, Any]]:

        return self.issues(
            SEVERITY_CRITICAL
        )

    # ========================================================
    #
    # WARNINGS
    #
    # ========================================================

    def warnings(
        self
    ) -> List[Dict[str, Any]]:

        return self.issues(
            SEVERITY_WARNING
        )

    # ========================================================
    #
    # TREND
    #
    # ========================================================

    def trend(
        self,
        limit=10
    ) -> Dict[str, Any]:
        """
        Analyze health-score trend.
        """

        reports = self.history(
            limit
        )

        if not reports:

            return {

                "status":
                    "NO_DATA",

                "scores":
                    [],

                "direction":
                    "unknown"

            }

        scores = [

            self._number(
                report.get(
                    "health_score",
                    0
                )
            )

            for report
            in reports

        ]

        if len(scores) < 2:

            direction = "stable"

        else:

            difference = (
                scores[-1]
                -
                scores[0]
            )

            if difference > 2:

                direction = "improving"

            elif difference < -2:

                direction = "declining"

            else:

                direction = "stable"

        return {

            "status":
                "AVAILABLE",

            "scores":
                scores,

            "latest":
                scores[-1],

            "oldest":
                scores[0],

            "change":
                round(
                    scores[-1]
                    -
                    scores[0],
                    2
                ),

            "direction":
                direction

        }

    # ========================================================
    #
    # SUMMARY
    #
    # ========================================================

    def summary(
        self
    ) -> Dict[str, Any]:

        latest = self.latest()

        if latest is None:

            return {

                "status":
                    "NO_DATA",

                "health_score":
                    None,

                "issues":
                    0,

                "warnings":
                    0,

                "critical":
                    0

            }

        return {

            "status":
                latest.get(
                    "status"
                ),

            "health_score":
                latest.get(
                    "health_score"
                ),

            "issues":
                latest.get(
                    "issue_count",
                    0
                ),

            "warnings":
                latest.get(
                    "warning_count",
                    0
                ),

            "critical":
                latest.get(
                    "critical_count",
                    0
                ),

            "info":
                latest.get(
                    "info_count",
                    0
                ),

            "duration":
                latest.get(
                    "duration",
                    0
                ),

            "trend":
                self.trend(
                    10
                )

        }

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ) -> Dict[str, Any]:

        scores = [

            self._number(
                report.get(
                    "health_score",
                    0
                )
            )

            for report
            in self.reports

        ]

        average_score = (

            sum(scores)
            /
            len(scores)

            if scores

            else 0

        )

        return {

            "checks":
                self.total_checks,

            "healthy":
                self.total_healthy,

            "needs_attention":
                self.total_attention,

            "critical":
                self.total_critical,

            "issues":
                self.total_issues,

            "warnings":
                self.total_warnings,

            "critical_issues":
                self.total_critical_issues,

            "average_health_score":
                round(
                    average_score,
                    2
                ),

            "latest_health_score":
                (
                    scores[-1]
                    if scores
                    else None
                ),

            "history":
                len(
                    self.reports
                )

        }

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        latest = self.latest()

        return {

            "module":
                "self_diagnostic",

            "version":
                DIAGNOSTIC_VERSION,

            "status":
                (
                    latest.get(
                        "status"
                    )
                    if latest
                    else "NO_DATA"
                ),

            "health_score":
                (
                    latest.get(
                        "health_score"
                    )
                    if latest
                    else None
                ),

            "reports":
                len(
                    self.reports
                ),

            "checks":
                self.total_checks,

            "healthy":
                self.total_healthy,

            "needs_attention":
                self.total_attention,

            "critical":
                self.total_critical,

            "issues":
                self.total_issues,

            "warnings":
                self.total_warnings,

            "critical_issues":
                self.total_critical_issues,

            "max_history":
                self.max_history,

            "enabled":
                self.enabled,

            "started_at":
                self.started_at

        }

    # ========================================================
    #
    # ENABLE
    #
    # ========================================================

    def enable(
        self
    ) -> bool:

        self.enabled = True

        logger.info(
            "Self Diagnostic enabled."
        )

        return True

    # ========================================================
    #
    # DISABLE
    #
    # ========================================================

    def disable(
        self
    ) -> bool:

        self.enabled = False

        logger.info(
            "Self Diagnostic disabled."
        )

        return True

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self
    ) -> bool:

        self.reports.clear()

        self.total_checks = 0

        self.total_healthy = 0

        self.total_attention = 0

        self.total_critical = 0

        self.total_issues = 0

        self.total_warnings = 0

        self.total_critical_issues = 0

        self.last_check = None

        logger.info(
            "Self Diagnostic reset."
        )

        return True


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

self_diagnostic = SelfDiagnostic()


# ============================================================
#
# SELF TEST
#
# ============================================================

def test_self_diagnostic() -> Dict[str, Any]:
    """
    Internal validation for the diagnostic engine.
    """

    engine = SelfDiagnostic(
        max_history=20
    )

    healthy_state = {

        "memory":
            100,

        "errors":
            1,

        "accuracy":
            85,

        "performance":
            90,

        "learning":
            20,

        "context":
            30,

        "goals":
            3,

        "active_goals":
            2,

        "handler_errors":
            0

    }

    unhealthy_state = {

        "memory":
            0,

        "errors":
            15,

        "accuracy":
            40,

        "performance":
            30,

        "learning":
            0,

        "context":
            0,

        "goals":
            0,

        "handler_errors":
            15

    }

    healthy = engine.check(
        healthy_state
    )

    unhealthy = engine.check(
        unhealthy_state
    )

    success = (

        healthy["status"]
        ==
        STATUS_HEALTHY

        and

        unhealthy["status"]
        ==
        STATUS_CRITICAL

        and

        unhealthy["critical_count"]
        >
        0

        and

        len(
            engine.history()
        )
        ==
        2

    )

    return {

        "status":
            "PASS"
            if success
            else
            "FAIL",

        "healthy_report":
            healthy,

        "critical_report":
            unhealthy,

        "summary":
            engine.summary(),

        "statistics":
            engine.statistics(),

        "trend":
            engine.trend()

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

    print(
        "INKSIDE INTELLIGENCE OS"
    )

    print(
        "SELF DIAGNOSTIC ENGINE v%s"
        % DIAGNOSTIC_VERSION
    )

    print("=" * 70)

    print()

    result = test_self_diagnostic()

    print(
        "TEST STATUS:",
        result["status"]
    )

    print(
        "SUMMARY:",
        result["summary"]
    )

    print(
        "STATISTICS:",
        result["statistics"]
    )

    print(
        "TREND:",
        result["trend"]
    )

    print()

    print("=" * 70)

    print(
        "SELF DIAGNOSTIC TEST COMPLETE"
    )

    print("=" * 70)

