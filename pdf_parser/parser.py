import fitz # type: ignore # PyMuPDF alias
import datetime
import pprint

from pdf_parser import utils

from pdf_parser.data import ResultsRow, LotDataTable, DeniedSuppliersRow

from typing import Any

class Parser:
    """
    Class for all parser logic.

    The main logic of parsing table functions is built on
    the trait of table in pdf documents that specific
    types of tables can only be of specific length.

    We can only proceed the list of all data at once.
    """
    def __init__(self) -> None:
        self.tabs = [] # tables
        self.data = [] # dataclasses

    def open_pdf(self, pdf_path: str) -> fitz.Document:
        pdf = fitz.open(pdf_path)
        self.pdf = pdf
        return pdf

    def extract_tables_from_pdf(self) -> list[list]:
        """It is possible to only find all tables at once and then sort them"""
        for page in self.pdf:
            tabs: fitz.Page.TableFinder = page.find_tables()
            for i in tabs:
                self.tabs.append(i.extract())
        return self.tabs

    def results_table(self, tab) -> list[ResultsRow]:
        """
        Function that fetches all tables with results from a pdf file and
        stores them as a list of ResultsRow dataclass instances.

        Results table is a table where potential suppliers and one winner are
        represented. Make sure that you extracted all tables from a pdf.
        """
    
        results = []

        for row in tab:
            if (row[1] == "Наименование поставщика" or
                row[1] == "Өнім берушінің атауы"):
                continue

            # Parse date_time assuming the fifth column in a table row
            # is the date string. If not then it will raise an exception.
            date_time = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S.%f')
            results.append(ResultsRow(
                serial_number=int(row[0]),
                supplier_name=row[1],
                bin_iin_inn_unp=row[2],
                unit_price=int(row[3]),
                total_price=int(row[4]),
                date_time=date_time
            ))

        return results
    
    def lot_table(self, tab: list) -> list[LotDataTable]:
        """
        Function fetches data from a table with information about lots.

        Sometimes a table can be dissected by a page break so it hard to
        fetch everything corectly, so I decided to use match-case
        statement to handle this.

        EXAMPLE OF A tab (argument):

        [
            ['Лот №', '69106193-ЗЦП1'],
            ['Наименование лота', 'Услуги по технической поддержке сайтов'],
            ['Наименование заказчика',
            'КГУ "Централизованная библиотечная система "Отырар" Отырарского района" '
            'отдела культуры, развития языков,\n'
            'физической культуры и спорта Отырарского района"'],
            ['Адрес заказчика',
            '614830100, 160700, Казахстан, г. Ш?УІЛДІР АУЫЛЫ, ул. НУРТАС ОНДАСЫНОВ, д. '
            '2, оф.'],
            ['Запланированная цена за\nединицу, тенге', '250000'],
            ['Запланированная сумма, тенге', '250000'],
            ['Единица измерения', 'Одна услуга'],
            ['Количество', '1']
        ]

        """

        lot = LotDataTable()

        for i in tab:
            print(i[0])
            match i[0]:
                # kz
                case 'Лоттың №':
                    # see the example about to understand why it is i[1]
                    lot.lot_number = i[1]
                case 'Лоттың атауы':
                    lot.lot_name = i[1]
                case 'Тапсырыс берушінің атауы':
                    lot.customer_name = i[1]
                case 'Тапсырыс берушінің мекенжайы':
                    lot.customer_address = i[1]
                case 'Бірлік, теңге үшін жоспарланған баға':
                    lot.planned_unit_price = int(i[1])
                case 'Жоспарланған сома, теңге':
                    lot.planned_total_price = i[1]
                case 'Өлшем бірлігі':
                    lot.measurment_unit = i[1]
                case 'Саны':
                    lot.amount = int(i[1])
                # ru
                case 'Лот №':
                    lot.lot_number = i[1]
                case 'Наименование лота':
                    lot.lot_name = i[1]
                case 'Наименование заказчика':
                    lot.customer_name = i[1]
                case 'Адрес заказчика ':
                    lot.customer_address = i[1]
                case 'Запланированная цена за единицу, тенге':
                    lot.planned_unit_price = i[1]
                case 'Запланированная сумма, тенге':
                    lot.planned_total_price = i[1]
                case 'Единица измерения':
                    lot.measurment_unit = i[1]
                case 'Количество':
                    lot.amount = i[1]

        return lot
    
    def denied_table(self, tab: list[list]) -> DeniedSuppliersRow:
        """
        It works because every row is a independed data unit.
        """
        denied = []
        if (tab[0][1] == 'Наименование поставщика' or
            tab[0][1] == 'Өнім берушінің атауы'):
            tab = tab[1:]
        for row in tab:
            denied.append(
                DeniedSuppliersRow(
                    serial_number = int(row[0]),
                    supplier_name = row[1],
                    bin_iin_unp = int(row[2]),
                    reason_for_deviation = row[3]
                )
            )
        return denied

    def get_all_data(self) -> list[list[Any]]:

        utils.check_data(self.tabs)
        
        lot = denied = result = None

        for tab in self.tabs:
            if len(tab[0]) == 2:
                lot = self.lot_table(tab)
            elif len(tab[0]) == 4:
                denied = self.denied_table(tab)
            elif len(tab[0]) == 6:
                result = self.results_table(tab)

            if lot and denied and result:
                self.data.append([lot, denied, result])
                lot = denied = result = None
        return self.data


    
