import copy

def getBanksList():
    OschadBankUSD = {"name": "OschadBank",
                  "link": "https://www.oschadbank.ua/rates-archive",
                  "currency": "USD",
                  "selectors":
                      {"table": ".rate-table__table tbody",
                       "buy": "tr td:nth-child(3) span",
                       "sale": "tr td:nth-child(4) span",
                       "date": "tr td:nth-child(1) span",
                       "actions": [".rates-archive .tabs__wrap div:nth-child(2)",
                                   ".rates-archive__content .tabs__wrap div:nth-child(2)",
                                   ".rate-toolbar__filter-period .rate-toolbar__filter-list li:nth-child(2)"],
                       "showMore": ".rate-table__section-buttons button",
                       "tr": ".rate-table__table tbody tr"
                       }
                  }

    PrivateBankUSD = {"name": "PrivateBank",
                   "link": "https://privatbank.ua/obmin-valiut",
                   "currency": "USD",
                   "selectors":
                       {"table": "#table-archive tbody",
                        "buy": "tr td:nth-child(4)",
                        "sale": "tr td:nth-child(5)",
                        "date": "tr td:nth-child(1)",
                        "actions": ["#archive-block",
                                    "#table-currency",
                                    "#one_month_by_table"],
                        "showMore": "div.download-more",
                        "tr": "#table-archive tbody tr"
                        }
                   }
    PrivateBankEUR = copy.deepcopy(PrivateBankUSD)
    PrivateBankEUR["currency"] = "EUR"
    PrivateBankEUR["selectors"]["actions"].append("#bs-select-2-2")

    OschadBankEUR = copy.deepcopy(OschadBankUSD)
    OschadBankEUR["currency"] = "EUR"
    OschadBankEUR["selectors"]["actions"].append(".rate-toolbar__currencies-select div.base-select__field")
    OschadBankEUR["selectors"]["actions"].append(".rate-toolbar__currencies-select .base-select__list ul li:nth-child(2)")
    banksList = [PrivateBankUSD, OschadBankUSD, PrivateBankEUR, OschadBankEUR]
    return banksList

if __name__ == "__main__":
    print("It's util file, to save selectors")
    print("Contains of such methods:")
    print("getBanksList -> return list with dictionaries of banks selectors")