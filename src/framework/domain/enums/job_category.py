from enum import Enum


class JobCategoryEnum(str, Enum):
    TECHNOLOGY = "Technology"
    OPERATIONS = "Operations"
    SALES = "Sales"
    MARKETING = "Marketing"
    ADMINISTRATION = "Administration"
    HR = "Human Resources"
    FINANCE = "Finance"
    CUSTOMER_SERVICE = "Customer Service"
    OTHER = "Other"
