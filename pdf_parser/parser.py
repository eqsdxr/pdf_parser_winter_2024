import datetime

import fitz # type: ignore # PyMuPDF alias

from pdf_parser import utils, data


class Parser:
    """
    Class for all parser logic.

    The main logic of parsing table functions is built on
    the trait of table in pdf documents that specific
    types of tables can only be of specific length.

    We can only proceed the list of all data at once.
    """
    
    def __init__(self) -> None:
        pass
    
    def process_pdf_from_path(self, pdf_path: str) -> fitz.Document:
        pdf = fitz.open(pdf_path)
        return pdf
    
    def process_pdf_from_bytes(self, pdf_bytes) -> fitz.Document:    
        pdf_document = fitz.open("pdf", pdf_bytes)
        return pdf_document

    # the most time consuming function (~99% of time)
    def extract_tables_from_pdf(self, pdf: fitz.Document) -> list[list]:
        """
        It is possible to only find all tables at once and then sort them
        """
        document_tabs = []
        for page in pdf:
            page_tabs: fitz.Page.TableFinder = page.find_tables()
            for i in page_tabs:
                document_tabs.append(i.extract())
        return document_tabs

    def fetch_lot_table(self, tab: list[list[str]]) -> list[data.LotDataTable]:
        """
        Fetches data from a table with information about lots.

        Sometimes a table can be dissected by a page break so it hard to
        fetch everything corectly, so I decided to use match-case
        statement to handle this.

        EXAMPLE OF A tab:

        [
            ["Лот №", "69106193-ЗЦП1"],
            ["Наименование лота", "Услуги по технической поддержке сайтов"],
            ["Наименование заказчика",
            "КГУ "Централизованная библиотечная система "Отырар" 
            Отырарского района" ""отдела культуры, развития языков,\n"
            "физической культуры и спорта Отырарского района""],
            ["Адрес заказчика",
            "614830100, 160700, Казахстан, 
            г. Ш?УІЛДІР АУЫЛЫ, ул. НУРТАС ОНДАСЫНОВ, д. ""2, оф."],
            ["Запланированная цена за\nединицу, тенге", "250000"],
            ["Запланированная сумма, тенге", "250000"],
            ["Единица измерения", "Одна услуга"],
            ["Количество", "1"]
        ]

        """

        lot = data.LotDataTable()

        for i in tab:
            match i[0]:
                # all values that can be converted, are converted here, others cannot
                # kz
                case "Лоттың №":
                    # see the docstring about to understand why it is i[1]
                    lot.lot_number = i[1]
                case "Лоттың атауы":
                    lot.lot_name = i[1]
                case "Тапсырыс берушінің атауы":
                    lot.customer_name = i[1]
                case "Тапсырыс берушінің мекенжайы":
                    lot.customer_address = i[1]

                # checking for a field with word wrapping
                case "Бірлік, теңге үшін жоспарланған баға":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Бірлік, теңге үшін жоспарланған \nбаға":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Бірлік, теңге үшін жоспарланған\nбаға":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Бірлік, теңге үшін жоспарланған\n баға":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                # end of checking for a field with word wrapping

                case "Жоспарланған сома, теңге":
                    lot.planned_total_price = utils.cast_to_int_float(i[1])
                case "Өлшем бірлігі":
                    lot.measurment_unit = i[1]
                case "Саны":
                    lot.amount = utils.cast_to_int_float(i[1])
                # ru
                case "Лот №":
                    lot.lot_number = i[1]
                case "Наименование лота":
                    lot.lot_name = i[1]
                case "Наименование заказчика":
                    lot.customer_name = i[1]
                case "Адрес заказчика":
                    lot.customer_address = i[1]
                    
                # checking for a field with word wrapping
                case "Запланированная цена за единицу, тенге":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Запланированная цена за \nединицу, тенге":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Запланированная цена за\nединицу, тенге":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                case "Запланированная цена за\n единицу, тенге":
                    lot.planned_unit_price = utils.cast_to_int_float(i[1])
                # end of checking for a field with word wrapping

                case "Запланированная сумма, тенге":
                    lot.planned_total_price = utils.cast_to_int_float(i[1])
                case "Единица измерения":
                    lot.measurment_unit = i[1]
                case "Количество":
                    lot.amount = utils.cast_to_int_float(i[1])

        return lot

    def fetch_denied_table(
            self,
            tab: list[list]
        ) -> list[data.DeniedSuppliersRow]:
        """
        It works because every row is a independed data unit.
        """
        denied = []
        if (tab[0][1] == "Наименование поставщика" or
            tab[0][1] == "Өнім берушінің атауы"):
            tab = tab[1:]
        for row in tab:
            denied.append(
                data.DeniedSuppliersRow(
                    serial_number = utils.cast_to_int_float(row[0]),
                    supplier_name = row[1],
                    bin_iin_unp = utils.cast_to_int_float(row[2]),
                    reason_for_deviation = row[3]
                )
            )
        return denied

    def fetch_results_table(
            self, 
            tab: list[list[str]]
        ) -> list[data.ResultsRow]:
        """
        Fetches all tables with results from a pdf file and
        stores them as a list of ResultsTable dataclass instances.

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
            date_time = datetime.datetime.strptime(
                row[5], 
                "%Y-%m-%d %H:%M:%S.%f"
            )
            results.append(data.ResultsRow(
                serial_number=utils.cast_to_int_float(row[0]),
                supplier_name=row[1],
                bin_iin_inn_unp=utils.cast_to_int_float(row[2]),
                unit_price=utils.cast_to_int_float(row[3]),
                total_price=utils.cast_to_int_float(row[4]),
                date_time=date_time
            ))

        return results

    def fetch_all_data(
            self, 
            tabs: list[list[list[str]]]
        ) -> list[data.ThreeTablesLDR]:
        """
        Uses all fetch functions and gathers information from the files.
        This function was mainly written by ChatGPT after I gave them my 
        initial function.
        """
        utils.check_data(tabs)

        output = []
        # Separately initialize lists to avoid shared references
        lot, denied, result = [], [], []  

        last_table_len = 0

        for tab in tabs:
            if len(tab[0]) == 2:
                if last_table_len == 6:
                    output.append(
                        data.ThreeTablesLDR(
                            lot_data_table=lot,
                            denied_suppliers_table=denied,
                            results_table=result
                        )
                    )
                    # Clear lists after appending to output
                    lot, denied, result = [], [], []  
                lot = self.fetch_lot_table(tab)
                last_table_len = 2

            elif len(tab[0]) == 4:
                denied = (self.fetch_denied_table(tab) if last_table_len != 4 
                          else denied + self.fetch_denied_table(tab))
                last_table_len = 4

            elif len(tab[0]) == 6:
                result = (self.fetch_results_table(tab) if last_table_len != 6
                           else result + self.fetch_results_table(tab))
                last_table_len = 6
 
        if lot or denied or result:
            output.append(
                data.ThreeTablesLDR(
                    lot_data_table=lot,
                    denied_suppliers_table=denied,
                    results_table=result
                )
            )

        return output
    
    def proceed_pdf(self, pdf: str | bytes) -> list[data.ThreeTablesLDR]:

        if isinstance(pdf, str) and "http" not in pdf:
            pdf_obj = self.process_pdf_from_path(pdf)
        elif isinstance(pdf, bytes):
            pdf_obj = self.process_pdf_from_bytes(pdf)
        else:
            raise TypeError(
                "Provide pdf in bytes or provide local path to pdf."
            )

        tabs = self.extract_tables_from_pdf(pdf_obj)
        data = self.fetch_all_data(tabs)
        return data


    
