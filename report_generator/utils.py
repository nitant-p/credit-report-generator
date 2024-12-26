import difflib
from datetime import datetime


def find_closest_company_by_name(company_name, company_names_list):
    from report_generator.models.CompanyModel import Company

    closest_match = difflib.get_close_matches(company_name, company_names_list, n=1)
    matched_company_name = closest_match[0]
    company = Company.objects.get(name=matched_company_name)
    return company

def get_case_insensitive_closest_names(target, target_list, n):
    target = target.lower()
    case_mapping = {}
    lowercase_list = []
    for item in target_list:
        lowercase = item.lower()
        case_mapping[lowercase] = item
        lowercase_list.append(lowercase)

    close_matches = difflib.get_close_matches(target, lowercase_list, n=n)

    result = []

    for match in close_matches:
        result.append(case_mapping[match])

    return result

def convert_datetimes(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, datetime):
                obj[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                convert_datetimes(value)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            if isinstance(item, datetime):
                obj[index] = item.isoformat()
            elif isinstance(item, (dict, list)):
                convert_datetimes(item)
    return obj