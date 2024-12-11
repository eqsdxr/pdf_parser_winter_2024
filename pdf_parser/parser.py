from fitz import Document, Page # type: ignore # PyMuPDF alias
from dataclasses import dataclass

import pprint

class Parser:
    def __init__(self, file) -> None:
        self.file = file
        self.data = []

    def extract_tables_from_pdf(self) -> list[list]:
        for page in self.file:
            tabs: Page.TableFinder = page.find_tables()
            for i in tabs:
                self.data.append(i.extract())
                # pprint.pprint(i.extract()) 
            # print('='*100)
        return self.data

    def get_results_tables(self) -> list[list[list[str]]]:
        cond1 = not self.data
        cond2 = len(self.data) < 4
        if cond1 or cond2:
            raise Exception(f'Data is empty or corrupted. \n {self.data}')
    
        results = []

        for t in self.data:
            if len(t[0]) == 6: # getting results table
                cond1 = t[0][1] == "Наименование поставщика"
                cond2 = t[0][1] == "Өнім берушінің атауы"
                if not cond1 and not cond2:
                    results.append(t) # skipping first row of the result table
                else:
                    if len(t) > 1:
                        results.append(t[1:])
                        
                cond1 = False
                cond2 = False
                continue


        return results
