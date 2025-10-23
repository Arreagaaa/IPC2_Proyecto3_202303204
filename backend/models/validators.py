import re
from typing import Optional, Tuple


def validate_nit(nit: str) -> bool:
    # Validar formato NIT: numeros-guion-digito o K
    if not nit:
        return False
    pattern = r'^\d+-[0-9K]$'
    return bool(re.match(pattern, nit, re.IGNORECASE))


def extract_first_date(text: str) -> Optional[str]:
    # Retorna la primera fecha valida en formato dd/mm/yyyy o None
    if not text:
        return None
    # Patron para dd/mm/yyyy
    pattern = r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(\d{4})'
    match = re.search(pattern, text)
    if match:
        day, month, year = match.groups()
        # Validacion basica
        day_int = int(day)
        month_int = int(month)
        year_int = int(year)

        # Verificar mes
        if month_int < 1 or month_int > 12:
            return None

        # Verificar rangos de dias por mes (simplificado)
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if day_int < 1 or day_int > days_in_month[month_int - 1]:
            return None

        return match.group(0)
    return None


def extract_first_datetime(text: str) -> Optional[Tuple[str, str]]:
    # Retorna la primera fecha y hora valida en formato (dd/mm/yyyy, hh:mm) o None
    if not text:
        return None
    # Patron para dd/mm/yyyy hh:mm (formato 24 horas)
    pattern = r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(\d{4})\s+([01]?\d|2[0-3]):([0-5]\d)'
    match = re.search(pattern, text)
    if match:
        date_part = f"{match.group(1)}/{match.group(2)}/{match.group(3)}"
        time_part = f"{match.group(4)}:{match.group(5)}"
        return (date_part, time_part)

    # Intentar extraer al menos la fecha
    date_only = extract_first_date(text)
    if date_only:
        return (date_only, "00:00")

    return None
