import datetime

nq_contracts = {
    "ENQH7": "2017-03-17",
    "ENQM7": "2017-06-16",
    "ENQU7": "2017-09-15",
    "ENQZ7": "2017-12-15",
    "ENQH18": "2018-03-16",
    "ENQM18": "2018-06-15",
    "ENQU18": "2018-09-21",
    "ENQZ18": "2018-12-21",
    "ENQH19": "2019-03-15",
    "ENQM19": "2019-06-21",
    "ENQU19": "2019-09-20",
    "ENQZ19": "2019-12-20",
    "ENQH20": "2020-03-20",
    "ENQM20": "2020-06-19",
    "ENQU20": "2020-09-18",
    "ENQZ20": "2020-12-18",
    "ENQH21": "2021-03-19",
    "ENQM21": "2021-06-18",
    "ENQU21": "2021-09-17",
    "ENQZ21": "2021-12-17",
    "ENQH22": "2022-03-18",
    "ENQM22": "2022-06-17",
    "ENQU22": "2022-09-16",
    "ENQZ22": "2022-12-16",
    "ENQH23": "2023-03-17",
    "ENQM23": "2023-06-16",
    "ENQU23": "2023-09-15",
    "ENQZ23": "2023-12-15",
}


def get_contract(date):
    for contract, expiration_date in nq_contracts.items():
        if (
            date.date()
            <= datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
        ):
            return contract, expiration_date
    return None
