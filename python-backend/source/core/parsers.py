import re
import uuid
from typing import List, Optional

from fastapi import Query


def parse_call_id_list(
    call_ids: Optional[str] = Query(
        None,
        description="comma-separated list of int call ids")
) -> List[str]:
    """parse a string of (comma-separated) call ids"""
    if not call_ids:
        return None
    parsed_call_ids = [int(cid.strip())
                       for cid in re.split(r"[^0-9]+", call_ids)]
    if len(parsed_call_ids) < 1:
        return []
    return parsed_call_ids


def parse_comma_separated_str_list(lst: str) -> List[str]:
    return [str(elem).strip() for elem in lst.split(",")]


def parse_field_list(
    fields: Optional[str] = Query(
        None,
        description="comma-separated list of field ('key') names. if empty, search all")
) -> List[str]:
    """parse a string of (comma-separated) field names"""
    if not fields:
        return None
    field_names = parse_comma_separated_str_list(fields)
    if len(field_names) < 1:
        return []
    return field_names


def parse_id_list(
    ids: Optional[str] = Query(
        None,
        description="comma-separated list of id names. if empty, search all")
) -> List[str]:
    """parse a string of (comma-separated) field names"""
    if not ids:
        return None
    id_elements = parse_comma_separated_str_list(ids)
    if len(id_elements) < 1:
        return []
    return id_elements


def parse_title_list(
    titles: Optional[str] = Query(
        None,
        description="comma-separated list of titles. if empty, search all")
) -> List[str]:
    """parse a string of (comma-separated) field names"""
    if not titles:
        return None
    title_elements = parse_comma_separated_str_list(titles)
    if len(title_elements) < 1:
        return []
    return title_elements


def parse_origins_list(
    origins: Optional[str]
) -> List[str]:
    """parse a string of (comma-separated) field names"""
    if not origins:
        return [""]
    origins_list = parse_comma_separated_str_list(origins)
    if len(origins_list) < 1:
        return [""]
    return origins_list


def parse_sections(prompt):
    pattern = r'\[(.*?)\]'
    sections = re.findall(pattern, prompt)
    return sections


def parse_report(report: str, sections: list) -> dict:
    report_dict = {}

    for i in range(len(sections)):
        section = sections[i].lower()
        try:
            if i < len(sections) - 1:
                match = re.search(
                    f'\[{section}\](.*)\[{sections[i+1]}\]', report, re.DOTALL | re.IGNORECASE)
            else:
                match = re.search(f'\[{section}\](.*)',
                                  report, re.DOTALL | re.IGNORECASE)

            if match:
                lines = [re.sub('^[0-9\-\.]+\s+', '', line).strip()
                         for line in match.group(1).strip().split('\n') if line.strip()]
                if section == 'summary':
                    report_dict[section] = '\n'.join(lines)
                else:
                    report_dict[section] = lines

        except Exception as e:
            report_dict[section] = None

    return report_dict
