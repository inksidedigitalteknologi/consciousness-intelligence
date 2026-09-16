# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MODULE MANAGER v2.0
#
# PRODUCTION CORE SYSTEM
#
# ============================================================
#
# FEATURES:
#
# - Dynamic Module Loader
# - Auto Discovery
# - Dependency Tracking
# - Thread Safe Execution
# - Lifecycle Management
# - Health Monitoring
# - Safe Reload
# - Self Healing Support
# - GUI Snapshot
#
# ============================================================


import logging
import importlib
import inspect
import threading
import traceback
import pkgutil

from datetime import datetime


logger = logging.getLogger(__name__)





# ============================================================
#
# MODULE MANAGER
#
# ============================================================


class ModuleManager:



    def __init__(self):


        # loaded module object

        self.modules = {}



        # module status

        self.status = {}



        # errors

        self.errors = {}



        # load timestamp

        self.loaded_time = {}



        # versions

        self.versions = {}



        # dependencies

        self.dependencies = {}



        # lifecycle state

        self.lifecycle = {}



        # thread safety

        self.lock = threading.RLock()



        logger.info(
            "Module Manager v2.0 initialized."
        )






    # ========================================================
    #
    # SAFE IMPORT
    #
    # ========================================================


    def load_module(
        self,
        name,
        path
    ):


        with self.lock:


            try:


                module = importlib.import_module(
                    path
                )



                self.modules[name] = module



                self.status[name] = "ONLINE"



                self.loaded_time[name] = (
                    datetime.now()
                    .isoformat()
                )



                self.lifecycle[name] = {

                    "loaded": True,

                    "initialized": False,

                    "running": False

                }



                self.versions[name] = getattr(

                    module,

                    "VERSION",

                    "unknown"

                )



                self.dependencies[name] = (

                    self.detect_dependencies(

                        module

                    )

                )



                logger.info(

                    "Module loaded: %s v%s",

                    name,

                    self.versions[name]

                )



                return module




            except Exception as e:



                self.modules[name] = None


                self.status[name] = "FAILED"


                self.errors[name] = str(e)



                logger.error(

                    "Module load failed %s : %s",

                    name,

                    e

                )



                return None







    # ========================================================
    #
    # REGISTER EXISTING MODULE
    #
    # ========================================================


    def register(
        self,
        name,
        module
    ):


        with self.lock:


            try:



                if module:



                    self.modules[name] = module


                    self.status[name] = "ONLINE"


                    self.versions[name] = getattr(

                        module,

                        "VERSION",

                        "unknown"

                    )


                    self.dependencies[name] = (

                        self.detect_dependencies(

                            module

                        )

                    )



                else:



                    self.modules[name] = None


                    self.status[name] = "FAILED"



            except Exception as e:


                logger.exception(

                    "Register failed: %s",

                    e

                )



    # ========================================================
    #
    # DEPENDENCY DETECTOR
    #
    # ========================================================


    def detect_dependencies(
        self,
        module
    ):


        deps = []


        try:


            source = inspect.getsource(
                module
            )



            for line in source.splitlines():


                if line.startswith(
                    "import "
                ):


                    deps.append(
                        line
                    )



                elif line.startswith(
                    "from "
                ):


                    deps.append(
                        line
                    )



        except Exception:


            pass



        return deps
            # ========================================================
    #
    # AUTO DISCOVERY
    #
    # Mencari module otomatis dalam package
    #
    # ========================================================


    def discover(
        self,
        package_name
    ):


        discovered = []


        try:


            package = importlib.import_module(
                package_name
            )


            for item in pkgutil.walk_packages(
                package.__path__,
                package.__name__ + "."
            ):


                module_name = item.name



                short_name = (

                    module_name
                    .split(".")[-1]

                )



                module = self.load_module(

                    short_name,

                    module_name

                )



                if module:


                    discovered.append(

                        short_name

                    )



            logger.info(

                "Discovery completed: %s modules",

                len(discovered)

            )



        except Exception as e:


            logger.exception(

                "Discovery failed: %s",

                e

            )



        return discovered







    # ========================================================
    #
    # INITIALIZE MODULE
    #
    # Jika module punya initialize()
    #
    # ========================================================


    def initialize_module(
        self,
        name
    ):


        with self.lock:


            module = self.modules.get(
                name
            )



            if not module:


                return False





            try:



                if hasattr(

                    module,

                    "initialize"

                ):


                    module.initialize()



                self.lifecycle[name]["initialized"] = True



                logger.info(

                    "Module initialized: %s",

                    name

                )



                return True




            except Exception as e:


                self.status[name] = "DEGRADED"


                self.errors[name] = str(e)



                logger.exception(

                    "Initialize failed %s",

                    name

                )


                return False







    # ========================================================
    #
    # INITIALIZE ALL
    #
    # ========================================================


    def initialize_all(
        self
    ):


        result = {}



        for name in self.modules:


            result[name] = (

                self.initialize_module(

                    name

                )

            )



        return result








    # ========================================================
    #
    # START MODULE
    #
    # ========================================================


    def start_module(
        self,
        name
    ):


        with self.lock:


            module = self.modules.get(
                name
            )



            if not module:


                return False





            try:



                if hasattr(

                    module,

                    "start"

                ):


                    module.start()



                self.lifecycle[name]["running"] = True



                logger.info(

                    "Module started: %s",

                    name

                )



                return True




            except Exception as e:



                self.status[name] = "DEGRADED"


                self.errors[name] = str(e)



                return False








    # ========================================================
    #
    # START ALL MODULES
    #
    # ========================================================


    def start_all(
        self
    ):


        result = {}



        for name in self.modules:


            result[name] = (

                self.start_module(

                    name

                )

            )



        return result








    # ========================================================
    #
    # STOP MODULE
    #
    # ========================================================


    def stop_module(
        self,
        name
    ):


        with self.lock:


            module = self.modules.get(
                name
            )



            if not module:


                return False



            try:



                if hasattr(

                    module,

                    "stop"

                ):


                    module.stop()



                self.lifecycle[name]["running"] = False



                logger.info(

                    "Module stopped: %s",

                    name

                )


                return True



            except Exception as e:



                self.errors[name] = str(e)



                return False







    # ========================================================
    #
    # STOP ALL
    #
    # ========================================================


    def stop_all(
        self
    ):


        result = {}



        for name in self.modules:


            result[name] = (

                self.stop_module(

                    name

                )

            )



        return result
            # ========================================================
    #
    # SAFE EXECUTION ENGINE
    #
    # Menjalankan fungsi module tanpa crash OS
    #
    # ========================================================


    def execute(
        self,
        name,
        method,
        *args,
        **kwargs
    ):


        with self.lock:


            module = self.modules.get(
                name
            )



            if module is None:


                logger.warning(

                    "Execute skipped, module offline: %s",

                    name

                )

                return None





            try:



                if hasattr(

                    module,

                    method

                ):


                    func = getattr(

                        module,

                        method

                    )



                    result = func(

                        *args,

                        **kwargs

                    )



                    return result





                logger.debug(

                    "Method not found %s.%s",

                    name,

                    method

                )



                return None




            except Exception as e:


                self.errors[name] = str(e)


                self.status[name] = "DEGRADED"



                logger.exception(

                    "Module execution error %s.%s : %s",

                    name,

                    method,

                    e

                )



                return None







    # ========================================================
    #
    # RELOAD MODULE
    #
    # Untuk self healing
    #
    # ========================================================


    def reload_module(
        self,
        name
    ):


        with self.lock:


            module = self.modules.get(
                name
            )



            if module is None:


                return False





            try:



                new_module = importlib.reload(

                    module

                )



                self.modules[name] = new_module



                self.status[name] = "ONLINE"



                self.errors.pop(

                    name,

                    None

                )



                self.loaded_time[name] = (

                    datetime.now()

                    .isoformat()

                )



                logger.info(

                    "Module reloaded: %s",

                    name

                )



                return True




            except Exception as e:


                self.status[name] = "FAILED"


                self.errors[name] = str(e)



                logger.exception(

                    "Reload failed %s",

                    name

                )



                return False







    # ========================================================
    #
    # UNLOAD MODULE
    #
    #
    # ========================================================


    def unload_module(
        self,
        name
    ):


        with self.lock:



            try:



                self.stop_module(

                    name

                )



                self.modules.pop(

                    name,

                    None

                )



                self.status.pop(

                    name,

                    None

                )


                self.lifecycle.pop(

                    name,

                    None

                )


                logger.info(

                    "Module unloaded: %s",

                    name

                )



                return True




            except Exception as e:


                logger.exception(

                    "Unload failed: %s",

                    e

                )



                return False








    # ========================================================
    #
    # DEPENDENCY CHECK
    #
    # ========================================================


    def dependency_check(
        self,
        name
    ):


        missing = []



        deps = self.dependencies.get(

            name,

            []

        )



        for dep in deps:



            if "core." in dep:



                parts = dep.split()



                for part in parts:



                    if part.startswith(

                        "core."

                    ):


                        module_name = (

                            part

                            .replace(

                                "core.",

                                ""

                            )

                            .split(".")[0]

                        )



                        if module_name not in self.modules:



                            missing.append(

                                module_name

                            )




        return {


            "module":

                name,


            "missing":

                list(

                    set(

                        missing

                    )

                ),


            "healthy":

                len(missing) == 0

        }









    # ========================================================
    #
    # HEALTH CHECK
    #
    # ========================================================


    def health_check(
        self
    ):


        report = []



        for name,module in self.modules.items():



            state = {


                "name":

                    name,


                "status":

                    self.status.get(

                        name,

                        "UNKNOWN"

                    ),



                "version":

                    self.versions.get(

                        name,

                        "unknown"

                    ),



                "lifecycle":

                    self.lifecycle.get(

                        name,

                        {}

                    ),



                "dependencies":

                    self.dependency_check(

                        name

                    )

            }




            if module:


                methods = []



                for method in (

                    "process",

                    "run",

                    "analyze",

                    "update",

                    "predict",

                    "generate",

                    "start",

                    "stop"

                ):


                    if hasattr(

                        module,

                        method

                    ):


                        methods.append(

                            method

                        )



                state["methods"] = methods




            report.append(

                state

            )



        return report
            # ========================================================
    #
    # MODULE SUMMARY
    #
    # Ringkasan sistem
    #
    # ========================================================


    def summary(
        self
    ):


        online = 0

        offline = 0

        degraded = 0

        failed = 0



        for state in self.status.values():


            if state == "ONLINE":

                online += 1


            elif state == "DEGRADED":

                degraded += 1


            elif state == "FAILED":

                failed += 1


            else:

                offline += 1





        return {


            "total":

                len(

                    self.modules

                ),


            "online":

                online,


            "offline":

                offline,


            "degraded":

                degraded,


            "failed":

                failed,


            "errors":

                len(

                    self.errors

                ),


            "timestamp":

                datetime.now()

                .isoformat()

        }









    # ========================================================
    #
    # SYSTEM REPORT
    #
    # Untuk Dashboard / AI Brain
    #
    # ========================================================


    def system_report(
        self
    ):


        return {


            "manager":

            {


                "status":

                    "ONLINE",



                "version":

                    "2.0"

            },



            "summary":

                self.summary(),




            "modules":

                self.health_check(),




            "errors":

                self.errors,




            "dependencies":

                {


                    name:

                    self.dependency_check(

                        name

                    )

                    for name in self.modules

                }

        }









    # ========================================================
    #
    # SNAPSHOT
    #
    # Mobile Mirror / GUI
    #
    # ========================================================


    def snapshot(
        self
    ):


        return {


            "time":

                datetime.now()

                .isoformat(),



            "system":

                self.summary(),




            "modules":

                [

                    {

                        "name":

                            item.get(

                                "name"

                            ),


                        "status":

                            item.get(

                                "status"

                            )

                    }


                    for item in self.health_check()

                ],




            "errors":

                len(

                    self.errors

                )

        }









    # ========================================================
    #
    # RESET ERROR
    #
    # ========================================================


    def clear_errors(
        self
    ):


        self.errors.clear()



        for name in self.status:


            if self.modules.get(name):


                self.status[name] = "ONLINE"



        logger.info(

            "Module errors cleared."

        )



        return True









    # ========================================================
    #
    # AUTO RECOVERY
    #
    # Memperbaiki module gagal
    #
    # ========================================================


    def auto_recover(
        self
    ):


        recovered = []

        failed = []



        for name,state in list(

            self.status.items()

        ):



            if state in (

                "FAILED",

                "DEGRADED",

                "OFFLINE"

            ):



                result = self.reload_module(

                    name

                )



                if result:


                    recovered.append(

                        name

                    )


                else:


                    failed.append(

                        name

                    )





        return {


            "recovered":

                recovered,


            "failed":

                failed,


            "timestamp":

                datetime.now()

                .isoformat()

        }









    # ========================================================
    #
    # WATCHDOG CHECK
    #
    # Dipanggil berkala oleh Brain
    #
    # ========================================================


    def watchdog(
        self
    ):


        issues = []



        for name,state in self.status.items():



            if state != "ONLINE":


                issues.append(

                    {

                        "module":

                            name,


                        "status":

                            state,


                        "error":

                            self.errors.get(

                                name

                            )

                    }

                )




        return {


            "healthy":

                len(issues) == 0,


            "issues":

                issues,


            "time":

                datetime.now()

                .isoformat()

        }










# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================


module_manager = ModuleManager()