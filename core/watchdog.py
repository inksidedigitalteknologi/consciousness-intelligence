# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SYSTEM WATCHDOG
#
# Version: 1.0
#
# Functions:
#
# - Runtime Monitoring
# - Thread Monitoring
# - Component Health Check
# - Warning Detection
# - Self Recovery Hook
#
# ============================================================


import logging
import threading
import time
from datetime import datetime


logger = logging.getLogger(__name__)




# ============================================================
#
# OPTIONAL CONNECTION
#
# ============================================================


try:

    from core.health import set_status

except Exception:


    def set_status(*args, **kwargs):
        pass





# ============================================================
#
# WATCHDOG ENGINE
#
# ============================================================


class SystemWatchdog:



    def __init__(
        self,
        interval=60
    ):


        self.interval = interval


        self.running = False


        self.thread = None


        self.targets = {}



        self.history = []


        self.errors = 0



        logger.info(
            "System Watchdog initialized."
        )





    # ========================================================
    #
    # REGISTER COMPONENT
    #
    # ========================================================


    def register(
        self,
        name,
        component
    ):


        self.targets[name] = component


        logger.info(

            "Watchdog registered: %s",

            name

        )





    # ========================================================
    #
    # CHECK COMPONENT
    #
    # ========================================================


    def check_component(
        self,
        name,
        component
    ):


        result = {


            "name":

                name,


            "status":

                "UNKNOWN",


            "time":

                datetime.now()
                .isoformat()

        }



        try:



            if component is None:


                result["status"] = "OFFLINE"

                return result





            # common health method


            if hasattr(
                component,
                "health_check"
            ):


                health = component.health_check()



                result["details"] = health



                result["status"] = (

                    "ONLINE"

                    if health

                    else

                    "WARNING"

                )


            elif hasattr(
                component,
                "running"
            ):


                result["status"] = (

                    "ONLINE"

                    if component.running

                    else

                    "IDLE"

                )


            else:


                result["status"] = "AVAILABLE"





        except Exception as e:


            self.errors += 1


            result["status"] = "ERROR"


            result["error"] = str(e)



            logger.exception(

                "Watchdog check failed %s",

                name

            )



        return result





    # ========================================================
    #
    # FULL SYSTEM CHECK
    #
    # ========================================================


    def scan(
        self
    ):


        report = {


            "timestamp":

                datetime.now()
                .isoformat(),


            "components":[]

        }




        for name,component in self.targets.items():


            report["components"].append(

                self.check_component(

                    name,

                    component

                )

            )




        self.history.append(
            report
        )



        # limit memory


        if len(
            self.history
        ) > 500:


            self.history.pop(0)



        return report





    # ========================================================
    #
    # MONITOR LOOP
    #
    # ========================================================


    def loop(
        self
    ):


        logger.info(
            "Watchdog monitoring started."
        )



        set_status(
            "watchdog",
            "ONLINE"
        )



        while self.running:


            try:


                report = self.scan()



                self.analyze(
                    report
                )



            except Exception as e:


                self.errors += 1


                logger.exception(

                    "Watchdog loop error: %s",

                    e

                )




            for _ in range(
                self.interval
            ):


                if not self.running:

                    break


                time.sleep(1)






    # ========================================================
    #
    # ANALYZE REPORT
    #
    # ========================================================


    def analyze(
        self,
        report
    ):


        for item in report["components"]:


            status = item.get(
                "status"
            )



            if status in (

                "ERROR",

                "OFFLINE"

            ):


                logger.warning(

                    "Watchdog warning: %s",

                    item

                )






    # ========================================================
    #
    # START
    #
    # ========================================================


    def start(
        self
    ):


        if self.running:

            return False



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )



        self.thread.start()



        return True





    # ========================================================
    #
    # STOP
    #
    # ========================================================


    def stop(
        self
    ):


        self.running = False



        if self.thread:


            self.thread.join(
                timeout=5
            )


            self.thread = None



        logger.info(
            "Watchdog stopped."
        )



        return True





    # ========================================================
    #
    # STATUS
    #
    # ========================================================


    def status(
        self
    ):


        return {


            "running":

                self.running,


            "targets":

                len(
                    self.targets
                ),


            "checks":

                len(
                    self.history
                ),


            "errors":

                self.errors

        }





    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================


    def snapshot(
        self
    ):


        return {


            "status":

                self.status(),


            "latest":

                self.history[-1]

                if self.history

                else None

        }





# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================


watchdog = SystemWatchdog()



# ============================================================
#
# END
#
# ============================================================