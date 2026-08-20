# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# LONG TERM MEMORY ENGINE
#
# Version: 2.0
#
# Production Cognitive Memory
#
# ============================================================
#
# Features:
#
# - Persistent SQLite Memory
# - Observation Storage
# - Experience Learning
# - Pattern Memory
# - Decision History
# - Semantic Memory
# - Knowledge Storage
# - Recall System
# - Thread Safe
#
# ============================================================


import sqlite3
import json
import logging
import threading
import shutil
import time

from pathlib import Path
from datetime import datetime


logger = logging.getLogger(__name__)





# ============================================================
#
# DATABASE PATH
#
# ============================================================


BASE_DIR = Path(__file__).resolve().parent.parent


DATABASE_DIR = (

    BASE_DIR /
    "database"

)


DATABASE_DIR.mkdir(
    exist_ok=True
)



MEMORY_DB = (

    DATABASE_DIR /
    "memory.db"

)



BACKUP_DIR = (

    DATABASE_DIR /
    "backup"

)


BACKUP_DIR.mkdir(
    exist_ok=True
)








# ============================================================
#
# MEMORY ENGINE
#
# ============================================================


class MemoryEngine:



    def __init__(self):


        self.db_path = str(

            MEMORY_DB

        )



        self.lock = threading.RLock()



        self.initialize()



        logger.info(

            "Long Term Memory Engine v2.0 initialized."

        )









    # ========================================================
    #
    # DATABASE CONNECTION
    #
    # ========================================================


    def connect(
        self
    ):


        return sqlite3.connect(

            self.db_path,

            check_same_thread=False

        )









    # ========================================================
    #
    # INITIAL DATABASE
    #
    # ========================================================


    def initialize(
        self
    ):


        try:


            with self.connect() as conn:



                cursor = conn.cursor()



                # ============================================
                #
                # OBSERVATION MEMORY
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS observations

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    source TEXT,


                    data TEXT,


                    result TEXT


                )

                """
                )





                # ============================================
                #
                # KNOWLEDGE MEMORY
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS knowledge

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    category TEXT,


                    content TEXT


                )

                """
                )






                # ============================================
                #
                # PATTERN MEMORY
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS patterns

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    name TEXT,


                    confidence REAL,


                    data TEXT


                )

                """
                )







                # ============================================
                #
                # DECISION MEMORY
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS decisions

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    decision TEXT,


                    reason TEXT,


                    confidence REAL


                )

                """
                )







                # ============================================
                #
                # EXPERIENCE MEMORY
                #
                # Trading feedback
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS experiences

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    symbol TEXT,


                    action TEXT,


                    entry REAL,


                    exit REAL,


                    profit REAL,


                    result TEXT,


                    data TEXT


                )

                """
                )







                # ============================================
                #
                # SEMANTIC MEMORY
                #
                # ============================================


                cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS semantic_memory

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,


                    timestamp TEXT,


                    concept TEXT,


                    relation TEXT,


                    data TEXT


                )

                """
                )






                # ============================================
                #
                # INDEX
                #
                # ============================================


                cursor.execute(
                """

                CREATE INDEX IF NOT EXISTS idx_obs_time

                ON observations(timestamp)

                """
                )



                cursor.execute(
                """

                CREATE INDEX IF NOT EXISTS idx_pattern_name

                ON patterns(name)

                """
                )




                conn.commit()



        except Exception as e:


            logger.exception(

                "Memory initialization failed: %s",

                e

            )
                # ========================================================
    #
    # REMEMBER
    #
    # Universal Memory Entry
    #
    # Dipanggil oleh Brain
    #
    # ========================================================


    def remember(
        self,
        data,
        result=None,
        source="brain"
    ):


        return self.save_observation(

            data,

            result,

            source

        )









    # ========================================================
    #
    # SAVE OBSERVATION
    #
    # Brain perception storage
    #
    # ========================================================


    def save_observation(
        self,
        data,
        result=None,
        source="brain"
    ):


        try:


            with self.lock:


                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO observations

                    (

                        timestamp,

                        source,

                        data,

                        result

                    )


                    VALUES

                    (?,?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        source,



                        json.dumps(

                            data,

                            default=str

                        ),



                        json.dumps(

                            result,

                            default=str

                        )

                    )

                    )


                    conn.commit()



            return True




        except Exception as e:


            logger.exception(

                "Save observation failed: %s",

                e

            )


            return False










    # ========================================================
    #
    # SAVE KNOWLEDGE
    #
    # Knowledge Builder
    #
    # ========================================================


    def save_knowledge(
        self,
        content,
        category="general"
    ):


        try:



            with self.lock:



                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO knowledge

                    (

                        timestamp,

                        category,

                        content

                    )


                    VALUES

                    (?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        category,



                        json.dumps(

                            content,

                            default=str

                        )

                    )

                    )



                    conn.commit()



            return True





        except Exception as e:



            logger.exception(

                "Save knowledge failed: %s",

                e

            )



            return False











    # ========================================================
    #
    # SAVE PATTERN
    #
    # Pattern Recognition Memory
    #
    # ========================================================


    def save_pattern(
        self,
        name,
        confidence,
        data=None
    ):


        try:



            with self.lock:



                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO patterns

                    (

                        timestamp,

                        name,

                        confidence,

                        data

                    )


                    VALUES

                    (?,?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        name,



                        float(

                            confidence

                        ),



                        json.dumps(

                            data,

                            default=str

                        )

                    )

                    )



                    conn.commit()



            return True





        except Exception as e:



            logger.exception(

                "Save pattern failed: %s",

                e

            )



            return False











    # ========================================================
    #
    # SAVE DECISION
    #
    # Trading decision history
    #
    # ========================================================


    def save_decision(
        self,
        decision,
        reason,
        confidence=0
    ):


        try:



            with self.lock:



                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO decisions

                    (

                        timestamp,

                        decision,

                        reason,

                        confidence

                    )


                    VALUES

                    (?,?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        str(

                            decision

                        ),



                        str(

                            reason

                        ),



                        float(

                            confidence

                        )

                    )

                    )


                    conn.commit()



            return True





        except Exception as e:



            logger.exception(

                "Save decision failed: %s",

                e

            )


            return False










    # ========================================================
    #
    # SAVE EXPERIENCE
    #
    # Trading result feedback
    #
    # ========================================================


    def save_experience(
        self,
        data
    ):


        try:


            symbol = data.get(

                "symbol",

                ""

            )


            action = data.get(

                "action",

                ""

            )


            entry = data.get(

                "entry",

                0

            )


            exit_price = data.get(

                "exit",

                0

            )


            profit = data.get(

                "profit",

                0

            )


            result = data.get(

                "result",

                ""

            )




            with self.lock:



                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO experiences

                    (

                        timestamp,

                        symbol,

                        action,

                        entry,

                        exit,

                        profit,

                        result,

                        data

                    )


                    VALUES

                    (?,?,?,?,?,?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        symbol,



                        action,



                        float(entry),



                        float(exit_price),



                        float(profit),



                        result,



                        json.dumps(

                            data,

                            default=str

                        )

                    )

                    )


                    conn.commit()



            return True




        except Exception as e:



            logger.exception(

                "Save experience failed: %s",

                e

            )


            return False










    # ========================================================
    #
    # SAVE SEMANTIC MEMORY
    #
    # Semantic Processor
    #
    # ========================================================


    def save_semantic(
        self,
        concept,
        relation,
        data=None
    ):


        try:



            with self.lock:



                with self.connect() as conn:


                    conn.execute(

                    """

                    INSERT INTO semantic_memory

                    (

                        timestamp,

                        concept,

                        relation,

                        data

                    )


                    VALUES

                    (?,?,?,?)

                    """,

                    (

                        datetime.now()

                        .isoformat(),



                        concept,



                        relation,



                        json.dumps(

                            data,

                            default=str

                        )

                    )

                    )


                    conn.commit()



            return True




        except Exception as e:



            logger.exception(

                "Save semantic failed: %s",

                e

            )


            return False
                # ========================================================
    #
    # RECALL SYSTEM
    #
    # Mengambil seluruh pengalaman masa lalu
    #
    # Dipakai oleh:
    #
    # - Learning Engine
    # - Reasoning Engine
    # - Reflection
    #
    # ========================================================


    def recall(
        self,
        limit=100
    ):


        return {


            "observations":

                self.get_observations(
                    limit
                ),



            "knowledge":

                self.get_knowledge(
                    limit
                ),



            "patterns":

                self.get_patterns(
                    limit
                ),



            "decisions":

                self.get_decisions(
                    limit
                ),



            "experiences":

                self.get_experiences(
                    limit
                ),



            "semantic":

                self.get_semantic(
                    limit
                )

        }









    # ========================================================
    #
    # GENERIC FETCH ENGINE
    #
    # ========================================================


    def _fetch(
        self,
        table,
        limit=100
    ):


        try:


            allowed = [

                "observations",

                "knowledge",

                "patterns",

                "decisions",

                "experiences",

                "semantic_memory"

            ]



            if table not in allowed:


                return []




            with self.connect() as conn:


                cursor = conn.cursor()



                cursor.execute(

                f"""

                SELECT *

                FROM {table}

                ORDER BY id DESC

                LIMIT ?

                """,

                (

                    limit,

                )

                )



                return cursor.fetchall()





        except Exception as e:


            logger.exception(

                "Fetch failed %s: %s",

                table,

                e

            )


            return []









    # ========================================================
    #
    # GET OBSERVATIONS
    #
    # ========================================================


    def get_observations(
        self,
        limit=100
    ):


        return self._fetch(

            "observations",

            limit

        )









    # ========================================================
    #
    # GET KNOWLEDGE
    #
    # ========================================================


    def get_knowledge(
        self,
        limit=100
    ):


        return self._fetch(

            "knowledge",

            limit

        )









    # ========================================================
    #
    # GET PATTERNS
    #
    # ========================================================


    def get_patterns(
        self,
        limit=100
    ):


        return self._fetch(

            "patterns",

            limit

        )









    # ========================================================
    #
    # GET DECISIONS
    #
    # ========================================================


    def get_decisions(
        self,
        limit=100
    ):


        return self._fetch(

            "decisions",

            limit

        )









    # ========================================================
    #
    # GET EXPERIENCES
    #
    # Trading Learning History
    #
    # ========================================================


    def get_experiences(
        self,
        limit=100
    ):


        return self._fetch(

            "experiences",

            limit

        )









    # ========================================================
    #
    # GET SEMANTIC MEMORY
    #
    # ========================================================


    def get_semantic(
        self,
        limit=100
    ):


        return self._fetch(

            "semantic_memory",

            limit

        )









    # ========================================================
    #
    # SEARCH MEMORY
    #
    # Basic Semantic Search
    #
    # Nanti bisa diganti embedding AI
    #
    # ========================================================


    def search(
        self,
        keyword,
        limit=50
    ):


        results = []



        try:


            keyword = str(
                keyword
            )



            with self.connect() as conn:


                cursor = conn.cursor()



                # Knowledge search

                cursor.execute(

                """

                SELECT *

                FROM knowledge

                WHERE content LIKE ?

                ORDER BY id DESC

                LIMIT ?

                """,

                (

                    f"%{keyword}%",

                    limit

                )

                )



                results.extend(

                    cursor.fetchall()

                )






                # Pattern search


                cursor.execute(

                """

                SELECT *

                FROM patterns

                WHERE name LIKE ?

                ORDER BY id DESC

                LIMIT ?

                """,

                (

                    f"%{keyword}%",

                    limit

                )

                )



                results.extend(

                    cursor.fetchall()

                )






                # Experience search


                cursor.execute(

                """

                SELECT *

                FROM experiences

                WHERE data LIKE ?

                ORDER BY id DESC

                LIMIT ?

                """,

                (

                    f"%{keyword}%",

                    limit

                )

                )


                results.extend(

                    cursor.fetchall()

                )





        except Exception as e:


            logger.exception(

                "Memory search failed: %s",

                e

            )




        return results










    # ========================================================
    #
    # FIND SIMILAR EXPERIENCE
    #
    # Untuk adaptive learning
    #
    # ========================================================


    def find_similar(
        self,
        keyword,
        limit=20
    ):


        matches = []



        try:



            data = self.search(

                keyword,

                limit

            )



            for item in data:


                matches.append(

                    {

                    "memory":

                        item,


                    "similarity":

                        1.0

                    }

                )





        except Exception as e:



            logger.exception(

                "Similarity search failed: %s",

                e

            )



        return matches
            # ========================================================
    #
    # MEMORY STATISTICS
    #
    # Monitoring jumlah memory
    #
    # ========================================================


    def stats(
        self
    ):


        result = {}



        tables = [

            "observations",

            "knowledge",

            "patterns",

            "decisions",

            "experiences",

            "semantic_memory"

        ]



        try:



            with self.connect() as conn:



                cursor = conn.cursor()



                for table in tables:



                    cursor.execute(

                    f"""

                    SELECT COUNT(*)

                    FROM {table}

                    """

                    )



                    count = cursor.fetchone()[0]



                    result[table] = count






            result["database"] = {


                "size_mb":

                    round(

                        Path(

                            self.db_path

                        ).stat()

                        .st_size

                        /

                        1024

                        /

                        1024,

                        3

                    )

            }




        except Exception as e:



            logger.exception(

                "Memory stats error: %s",

                e

            )




        return result











    # ========================================================
    #
    # HEALTH CHECK
    #
    # Dipakai Module Manager
    #
    # ========================================================


    def health(
        self
    ):


        try:



            with self.connect() as conn:



                conn.execute(

                    "SELECT 1"

                )



            return {


                "status":

                    "ONLINE",


                "database":

                    self.db_path,


                "time":

                    datetime.now()

                    .isoformat()


            }




        except Exception as e:



            return {


                "status":

                    "ERROR",


                "error":

                    str(e)

            }












    # ========================================================
    #
    # MEMORY OPTIMIZATION
    #
    # Membersihkan memory lama
    #
    # ========================================================


    def cleanup(
        self,
        days=180
    ):


        try:


            with self.lock:



                with self.connect() as conn:



                    cursor = conn.cursor()



                    tables = [

                        "observations",

                        "experiences",

                        "decisions"

                    ]



                    for table in tables:



                        cursor.execute(

                        f"""

                        DELETE FROM {table}

                        WHERE timestamp < datetime(

                            'now',

                            '-{days} days'

                        )

                        """

                        )




                    conn.commit()




            return True





        except Exception as e:



            logger.exception(

                "Cleanup failed: %s",

                e

            )


            return False











    # ========================================================
    #
    # DATABASE OPTIMIZATION
    #
    # ========================================================


    def optimize(
        self
    ):


        try:



            with self.lock:



                with self.connect() as conn:



                    conn.execute(

                        "VACUUM"

                    )



                    conn.execute(

                        "ANALYZE"

                    )




            return True





        except Exception as e:



            logger.exception(

                "Optimize failed: %s",

                e

            )



            return False










    # ========================================================
    #
    # BACKUP MEMORY
    #
    # ========================================================


    def backup(
        self
    ):


        try:



            filename = (


                "memory_backup_"

                +

                datetime.now()

                .strftime(

                    "%Y%m%d_%H%M%S"

                )

                +

                ".db"


            )



            destination = (

                BACKUP_DIR /

                filename

            )



            shutil.copy2(

                self.db_path,

                destination

            )



            return str(

                destination

            )





        except Exception as e:



            logger.exception(

                "Backup failed: %s",

                e

            )


            return None










    # ========================================================
    #
    # RESTORE MEMORY
    #
    # ========================================================


    def restore(
        self,
        backup_file
    ):


        try:



            source = Path(

                backup_file

            )



            if not source.exists():

                return False




            shutil.copy2(

                source,

                self.db_path

            )




            return True





        except Exception as e:



            logger.exception(

                "Restore failed: %s",

                e

            )



            return False










    # ========================================================
    #
    # EXPORT SNAPSHOT
    #
    # GUI / Dashboard
    #
    # ========================================================


    def snapshot(
        self
    ):


        return {


            "status":

                self.health(),



            "statistics":

                self.stats(),



            "timestamp":

                datetime.now()

                .isoformat()


        }









    # ========================================================
    #
    # RESET MEMORY
    #
    # Development Only
    #
    # ========================================================


    def reset(
        self
    ):


        try:



            with self.lock:



                with self.connect() as conn:



                    tables = [

                        "observations",

                        "knowledge",

                        "patterns",

                        "decisions",

                        "experiences",

                        "semantic_memory"

                    ]



                    for table in tables:



                        conn.execute(

                        f"""

                        DELETE FROM {table}

                        """

                        )




                    conn.commit()



            return True




        except Exception as e:



            logger.exception(

                "Reset memory failed: %s",

                e

            )



            return False
                # ========================================================
    #
    # AUTO BACKUP SYSTEM
    #
    # Memory protection layer
    #
    # ========================================================


    def auto_backup(
        self,
        interval_hours=24
    ):


        try:


            import threading



            def backup_loop():


                while True:



                    try:



                        result = self.backup()



                        if result:



                            logger.info(

                                "Automatic memory backup created: %s",

                                result

                            )




                    except Exception as e:



                        logger.exception(

                            "Auto backup error: %s",

                            e

                        )




                    time.sleep(

                        interval_hours *

                        3600

                    )





            thread = threading.Thread(


                target=backup_loop,


                daemon=True


            )



            thread.start()



            return True





        except Exception as e:



            logger.exception(

                "Auto backup start failed: %s",

                e

            )


            return False











    # ========================================================
    #
    # LEARNING ENGINE COMPATIBILITY API
    #
    # ========================================================


    def get_memory_for_learning(
        self,
        limit=200
    ):


        return {


            "observations":

                self.get_observations(

                    limit

                ),



            "patterns":

                self.get_patterns(

                    limit

                ),



            "knowledge":

                self.get_knowledge(

                    limit

                ),



            "experiences":

                self.get_experiences(

                    limit

                ),



            "decisions":

                self.get_decisions(

                    limit

                )


        }









    # ========================================================
    #
    # BRAIN COMPATIBILITY
    #
    # core.brain.py interface
    #
    # ========================================================


    def observe(
        self,
        data,
        result=None
    ):


        return self.save_observation(

            data,

            result,

            "brain"

        )







    def learn(
        self,
        knowledge
    ):


        return self.save_knowledge(

            knowledge,

            "learning"

        )







    def remember_pattern(
        self,
        name,
        confidence,
        data=None
    ):


        return self.save_pattern(

            name,

            confidence,

            data

        )











    # ========================================================
    #
    # MEMORY STATUS FOR DASHBOARD
    #
    # ========================================================


    def status(
        self
    ):


        return {


            "engine":

                "LONG_TERM_MEMORY",



            "status":

                self.health(),



            "records":

                self.stats(),



            "database":

                self.db_path



        }









# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================


memory = MemoryEngine()



# ============================================================
#
# STARTUP MEMORY SERVICES
#
# ============================================================


try:


    memory.auto_backup(

        interval_hours=24

    )



except Exception as e:



    logger.warning(

        "Auto backup disabled: %s",

        e

    )



# ============================================================
#
# END
#
# INKSIDE INTELLIGENCE OS
#
# LONG TERM MEMORY ENGINE v2.0
#
# ============================================================