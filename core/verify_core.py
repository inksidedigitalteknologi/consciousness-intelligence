# ============================================================
# verify_core.py
# CORE MODULE VERIFICATION SCRIPT
# ============================================================

import sys
import traceback
from datetime import datetime

print()
print("=" * 70)
print("  INKSIDE CORE MODULE VERIFICATION")
print("  " + datetime.now().isoformat())
print("=" * 70)
print()

modules_to_test = [
    # Core modules
    ("core.consciousness", "Consciousness"),
    ("core.brain", "Brain"),
    ("core.bot", "TradingBot"),
    
    # Learning modules
    ("core.learning.engine", "LearningEngine"),
    ("core.learning.pattern", "PatternEngine"),
    ("core.learning.market_learning", "MarketLearning"),
    ("core.learning.semantic_memory", "SemanticMemory"),
    ("core.learning.learning_memory", "LearningMemory"),
    ("core.learning.entity_recognition", "EntityRecognition"),
    ("core.learning.semantic_processor", "SemanticProcessor"),
    ("core.learning.context_manager", "ContextManager"),
    ("core.learning.reflection", "ReflectionEngine"),
    ("core.learning.insight", "InsightEngine"),
    ("core.learning.behavior", "BehaviorEngine"),
    ("core.learning.association", "AssociationEngine"),
    ("core.learning.archive_manager", "ArchiveManager"),
    ("core.learning.evaluator", "EvaluatorEngine"),
    ("core.learning.adaptive", "AdaptiveEngine"),
    ("core.learning.strategy", "StrategyEngine"),
    ("core.learning.simulation", "SimulationEngine"),
    ("core.learning.memory_optimizer", "MemoryOptimizer"),
    ("core.learning.analyzer", "LearningAnalyzer"),
    
    # System modules
    ("core.memory", "MemoryEngine"),
    ("core.knowledge", "KnowledgeEngine"),
    ("core.health", "HealthMonitor"),
    ("core.scheduler", "Scheduler"),
    ("core.runtime", "RuntimeManager"),
    ("core.watchdog", "SystemWatchdog"),
    ("core.diagnostics", "SystemDiagnostics"),
    ("core.bootstrap", "Bootstrap"),
]

passed = 0
failed = 0
results = []

for module_path, class_name in modules_to_test:
    try:
        # Import module
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name, None)
        
        if cls is None:
            results.append({
                "module": module_path,
                "status": "FAIL",
                "error": f"Class {class_name} not found"
            })
            failed += 1
            continue
        
        # Try to instantiate
        try:
            instance = cls()
            status = "PASS"
            error = None
        except Exception as e:
            status = "WARN"
            error = str(e)
        
        # Try to call methods if available
        methods = ["status", "get_state", "health", "snapshot"]
        method_results = []
        
        for method in methods:
            if hasattr(instance, method):
                try:
                    getattr(instance, method)()
                    method_results.append(f"{method}: OK")
                except Exception as e:
                    method_results.append(f"{method}: ERROR ({e})")
        
        results.append({
            "module": module_path,
            "class": class_name,
            "status": status,
            "error": error,
            "methods": method_results
        })
        
        if status == "PASS":
            passed += 1
        else:
            failed += 1
            
    except Exception as e:
        results.append({
            "module": module_path,
            "status": "FAIL",
            "error": str(e)
        })
        failed += 1

# Print results
print("=" * 70)
print("  RESULTS")
print("=" * 70)
print()

for result in results:
    status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
    print(f"{status_icon} {result['module']}")
    
    if result.get("error"):
        print(f"     Error: {result['error']}")
    
    if result.get("methods"):
        print(f"     Methods: {', '.join(result['methods'])}")
    
    print()

print("=" * 70)
print(f"  SUMMARY: {passed} PASSED, {failed} FAILED")
print(f"  TOTAL:   {passed + failed} MODULES")
print("=" * 70)
print()

if failed == 0:
    print("✅ ALL CORE MODULES VERIFIED!")
else:
    print("❌ SOME MODULES FAILED VERIFICATION!")
    print("   Please check the errors above.")

sys.exit(0 if failed == 0 else 1)