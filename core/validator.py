# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MODULE VALIDATOR
#
# Version: 1.0
#
# Functions:
#
# - Validate Module Structure
# - Check Required Methods
# - Detect Broken Module
# - Generate Validation Report
#
# ============================================================

import logging
from datetime import datetime


logger = logging.getLogger(__name__)


# ============================================================
#
# VALIDATOR ENGINE
#
# ============================================================


class ModuleValidator:


    def __init__(self):


        self.results = []

        self.errors = []


        logger.info(
            "Module Validator initialized."
        )



    # ========================================================
    #
    # CHECK BASIC MODULE
    #
    # ========================================================


    def validate(
        self,
        name,
        module
    ):


        report = {


            "name":
                name,


            "status":
                "UNKNOWN",


            "methods":
                [],


            "errors":
                [],


            "time":
                datetime.now()
                .isoformat()

        }



        try:


            # --------------------------------------------
            # Module existence
            # --------------------------------------------


            if module is None:


                report["status"] = "MISSING"


                report["errors"].append(
                    "Module not loaded"
                )


                self.results.append(
                    report
                )


                return report





            # --------------------------------------------
            # Check methods
            # --------------------------------------------


            supported = [


                "initialize",

                "process",

                "run",

                "analyze",

                "detect",

                "predict",

                "update",

                "generate",

                "status"

            ]



            found = []



            for method in supported:


                if hasattr(
                    module,
                    method
                ):


                    found.append(
                        method
                    )



            report["methods"] = found





            # --------------------------------------------
            # Minimum requirement
            # --------------------------------------------


            if (

                "process" in found

                or

                "run" in found

                or

                "analyze" in found

            ):


                report["status"] = "READY"



            else:


                report["status"] = "DEGRADED"


                report["errors"].append(

                    "No execution method found"

                )







        except Exception as e:


            report["status"] = "FAILED"


            report["errors"].append(

                str(e)

            )


            logger.exception(
                "Validation failed: %s",
                e
            )



        self.results.append(
            report
        )


        return report





    # ========================================================
    #
    # VALIDATE MULTIPLE MODULE
    #
    # ========================================================


    def validate_all(
        self,
        modules
    ):


        self.results.clear()



        reports = []



        for name,module in modules.items():


            reports.append(

                self.validate(

                    name,

                    module

                )

            )



        return reports





    # ========================================================
    #
    # SYSTEM SCORE
    #
    # ========================================================


    def score(
        self
    ):


        total = len(
            self.results
        )


        ready = 0


        degraded = 0


        failed = 0



        for item in self.results:


            if item["status"] == "READY":

                ready += 1


            elif item["status"] == "DEGRADED":

                degraded += 1


            else:

                failed += 1





        if total == 0:


            percentage = 0



        else:


            percentage = round(

                ready /

                total *

                100,

                2

            )





        return {


            "total":

                total,


            "ready":

                ready,


            "degraded":

                degraded,


            "failed":

                failed,


            "health_score":

                percentage

        }





    # ========================================================
    #
    # QUICK CHECK
    #
    # ========================================================


    def is_ready(
        self,
        module
    ):


        result = self.validate(

            "temporary",

            module

        )


        return (

            result["status"]

            ==

            "READY"

        )





    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================


    def snapshot(
        self
    ):


        return {


            "score":

                self.score(),


            "results":

                self.results

        }




# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================


validator = ModuleValidator()


# ============================================================
#
# END
#
# ============================================================