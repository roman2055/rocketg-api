import calendar
import datetime
import requests

from django.db.models import Q, Sum

from apis.api_view import constants
from apis.models import Industry_locales, Country_locales, Images, Countries, Expenses, Users, ExpenseFile
from apis.serializers import ImageSerializer, ExpenseFileSerializer


def getExpenseData(expenseList, half):
    expenses_data = []
    for expense in expenseList:
        user = Users.objects.get(id=expense.user_id)
        image = Images.objects.filter(user_id=expense.user_id)[0]
        expense_data = {
            "id": expense.id,
            "merchant_name": expense.merchant_name,
            "receipt_date": expense.receipt_date,
            "description": expense.description,
            "total_amount": expense.total_amount,
            "converted_amount": 0,
            "category": expense.category,
            "assignees": expense.assignees,
            "file_urls": expense.file_urls,
            "file_names": expense.file_names,
            "user_id": expense.user_id,
            "company_id": expense.company_id,
            "currency_type": expense.currency_type,
            "status": expense.status,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,
            "user": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "avatar_url": image.avatar.name,
                "job_title": user.job_title,
            },
            "half": half,
        }
        expenses_data.append(expense_data)

    return expenses_data


def getIndustryData(industryList):
    industries_data = []

    for industry in industryList:
        industry_data = {
            "id": industry.industry_id,
            "name": industry.name,
        }
        industries_data.append(industry_data)

    return industries_data


def getCountryData(countryList):
    countries_data = []

    for country in countryList:
        countryCode = Countries.objects.get(id=country.country_id)
        if countryCode is None:
            code = ''
        else:
            code = countryCode.code
        country_data = {
            "id": country.country_id,
            "code": code,
            "name": country.name,
        }
        countries_data.append(country_data)

    return countries_data


def getUserData(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency,
        }
        users_data.append(user_data)

    return users_data


def getUserDataWithPW(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": user.reset_password_token,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency,
        }
        users_data.append(user_data)

    return users_data


def getExpenseDetail(expenses):
    expenses_data = []

    for expense in expenses:
        expense_data = {
            "id": expense.id,
            "merchant_name": expense.merchant_name,
            "receipt_date": expense.receipt_date,
            "description": expense.description,
            "total_amount": expense.total_amount,
            "category": expense.category,
            "assignees": expense.assignees,
            "file_urls": expense.file_urls,
            "file_names": expense.file_names,
            "user_id": expense.user_id,
            "company_id": expense.company_id,
            "status": expense.status,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,
        }
        expenses_data.append(expense_data)

    return expenses_data


def getCompanyData(companies, lang):
    companies_data = []

    for company in companies:
        industryLocal = Industry_locales.objects.filter(language__startswith=lang,
                                                        industry_id=company.industry.id).first()
        countryLocal = Country_locales.objects.filter(language__startswith=lang, country_id=company.country.id).first()

        company_data = {
            "id": company.id,
            "name": company.name,
            "active_employees": company.active_employees,
            "total_expenses": company.total_expenses,
            "manage": company.manage,
            "website": company.website,
            "employee_count_index": company.employee_count_index,
            "created_at": company.created_at,
            "industry_id": company.industry_id,
            "country_id": company.country_id,
            "user_id": company.user_id,
            "industry": {
                "id": company.industry.id,
                "name": industryLocal.name
            },
            "country": {
                "id": company.country.id,
                "name": countryLocal.name
            }
        }
        companies_data.append(company_data)

    return companies_data


def uploadImage(userId, imageInfo):
    try:
        image = Images.objects.get(user_id=userId)
        image_serializer = ImageSerializer(image, data=imageInfo)
    except Images.DoesNotExist:
        image_serializer = ImageSerializer(data=imageInfo)

    if image_serializer.is_valid():
        image_serializer.save()

    return image_serializer


def uploadExpenseFile(expenseId, expenseInfo):
    try:
        file = ExpenseFile.objects.get(expense_id=expenseId)
        file_serializer = ExpenseFileSerializer(file, data=expenseInfo)
    except ExpenseFile.DoesNotExist:
        file_serializer = ExpenseFileSerializer(data=expenseInfo)

    if file_serializer.is_valid():
        file_serializer.save()

    return file_serializer


def first_day_in_month(year, month, type):
    if type == 2:
        return datetime.datetime(year, month, 16)
    else:
        return datetime.datetime(year, month, 1)


def last_day_in_month(year, month, type):
    lastDay = calendar.monthrange(year, month)[1]  # last day of month
    if type == 1:
        return datetime.datetime(year, month, 15)
    else:
        return datetime.datetime(year, month, lastDay)


def getExpenseByMonth(startDate, endDate, userId, assignerId):
    if userId:
        dataByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                              Q(receipt_date__lte=endDate), Q(status__gt=0))
    elif assignerId:
        dataByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                              Q(receipt_date__lte=endDate), Q(status__gt=0), (
                                                      Q(assignees=assignerId) | Q(
                                                  assignees__startswith=assignerId) | Q(
                                                  assignees__contains=assignerId) | Q(
                                                  assignees__endswith=assignerId)))

    return dataByMonth


def getMonthInfoForExpenses(startDate, endDate, userId, assignerId):
    if userId:
        expensesByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                                  Q(receipt_date__lte=endDate), Q(status__gt=0)).values(
            'currency_type').annotate(total_amount=Sum('total_amount'))
    elif assignerId:
        expensesByMonth = Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate),
                                                  Q(receipt_date__lte=endDate), Q(status__gt=0), (
                                                              Q(assignees=assignerId) | Q(
                                                          assignees__startswith=assignerId) | Q(
                                                          assignees__contains=assignerId) | Q(
                                                          assignees__endswith=assignerId))).values(
            'currency_type').annotate(total_amount=Sum('total_amount'))

    return expensesByMonth


def getMonthInfoCountForExpenses(startDate, endDate, userId, assignerId):
    if userId:
        expensesCountByMonth = list(
            Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate), Q(receipt_date__lte=endDate)))
    elif assignerId:
        expensesCountByMonth = list(
            Expenses.objects.filter(Q(user_id=userId), Q(receipt_date__gte=startDate), Q(receipt_date__lte=endDate), (
                        Q(assignees=assignerId) | Q(assignees__startswith=assignerId) | Q(
                    assignees__contains=assignerId) | Q(assignees__endswith=assignerId))))
    count = len(expensesCountByMonth)
    return count


def getMonthTotalPrice(expensesByMonth, wants_currency):
    total = 0
    for expense in expensesByMonth:
        total += exchangeMoney(expense['total_amount'], expense['currency_type'], wants_currency)
    return total


def exchangeMoney(money, fromNum, toNum):
    today = datetime.date.today()
    if constants.g_today != today:
        constants.g_utc = RealTimeCurrencyExchangeRate("USD", "CNY", constants.api_key)
        constants.g_etc = RealTimeCurrencyExchangeRate("EUR", "CNY", constants.api_key)
        constants.g_ctu = RealTimeCurrencyExchangeRate("CNY", "USD", constants.api_key)
        constants.g_etu = RealTimeCurrencyExchangeRate("EUR", "USD", constants.api_key)
        constants.g_ute = RealTimeCurrencyExchangeRate("USD", "EUR", constants.api_key)
        constants.g_cte = RealTimeCurrencyExchangeRate("CNY", "EUR", constants.api_key)
        constants.g_today = today

    if fromNum == toNum:
        money = money
    elif fromNum == 1 and toNum == 2:
        money = money / constants.g_ute
    elif fromNum == 1 and toNum == 3:
        money = money / constants.g_utc
    elif fromNum == 2 and toNum == 1:
        money = money / constants.g_etu
    elif fromNum == 2 and toNum == 3:
        money = money / constants.g_etc
    elif fromNum == 3 and toNum == 1:
        money = money / constants.g_ctu
    elif fromNum == 3 and toNum == 2:
        money = money / constants.g_cte

    return money


def RealTimeCurrencyExchangeRate(from_currency, to_currency, api_key):

    # base_url variable store base url
    base_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"

    # main_url variable store complete url
    main_url = base_url + "&from_currency=" + from_currency + "&to_currency=" + to_currency + "&apikey=" + api_key

    # get method of requests module
    # return response object
    req_ob = requests.get(main_url)

    # json method return json format
    # data into python dictionary data type.

    # result contains list of nested dictionaries
    result = req_ob.json()
    return float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])