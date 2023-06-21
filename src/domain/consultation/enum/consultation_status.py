from enum import Enum


class ConsultationStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    CANCELED = "CANCELED"
    IN_PROCESS = "IN_PROCESS"
    FINISHED = "FINISHED"



