from pypinyin import lazy_pinyin
import re

class CitationAPA:
    def __init__(self, authors, year, title):
        self.authors = authors
        self.year = year
        self.title = title

class JournalCitation(CitationAPA):
    def __init__(self, authors, year, title, journal, volume, issue, pages):
        super().__init__(authors, year, title)
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.pages = pages

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. {self.journal}, {self.volume}({self.issue}), {self.pages}."
        return citation

class JournalCitationWithDOI(JournalCitation):
    def __init__(self, authors, year, title, journal, volume, issue, pages, doi):
        super().__init__(authors, year, title, journal, volume, issue, pages)
        self.doi = doi

    def generate_citation(self):
        citation = super().generate_citation() + f" https://doi.org/{self.doi}"
        return citation

class OnlineJournalCitation(CitationAPA):
    def __init__(self, authors, year, title, journal, volume, doi):
        super().__init__(authors, year, title)
        self.journal = journal
        self.volume = volume
        self.doi = doi

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. {self.journal}. {self.volume} Advance online publication. https://doi.org/{self.doi}"
        return citation

class ElectronicJournalCitation(JournalCitationWithDOI):
    def __init__(self, authors, year, title, journal, volume, issue, article_number, doi):
        super().__init__(authors, year, title, journal, volume, issue, article_number, doi)

    def generate_citation(self):
        citation = super().generate_citation().replace(f", {self.pages}", f", Article {self.pages}")
        return citation

class NewspaperCitation(CitationAPA):
    def __init__(self, authors, year, title, newspaper, url, date):
        super().__init__(authors, year, title)
        self.newspaper = newspaper
        self.url = url
        self.date = date

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}, {self.date}). {self.title}. {self.newspaper}. {self.url}"
        return citation

class BookCitation(CitationAPA):
    def __init__(self, authors, year, title, publisher):
        super().__init__(authors, year, title)
        self.publisher = publisher

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. {self.publisher}."
        return citation

class BookChapterCitation(CitationAPA):
    def __init__(self, authors, year, title, book_title, editors, edition, pages, publisher):
        super().__init__(authors, year, title)
        self.book_title = book_title
        self.editors = editors
        self.edition = edition
        self.pages = pages
        self.publisher = publisher

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. In {self.editors} (Eds.), {self.book_title} ({self.edition}, pp. {self.pages}). {self.publisher}."
        return citation

class OnlineFirstChapterCitation(CitationAPA):
    def __init__(self, authors, year, title, book_title, doi):
        super().__init__(authors, year, title)
        self.book_title = book_title
        self.doi = doi

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. {self.book_title}. Advance online publication. https://doi.org/{self.doi}"
        return citation

class TranslatedBookCitation(BookCitation):
    def __init__(self, authors, year, title, translator, location, publisher, original_year):
        super().__init__(authors, year, title, publisher)
        self.translator = translator
        self.location = location
        self.original_year = original_year

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title} ({self.translator}, Trans.). {self.location}: {self.publisher}. (Original work published {self.original_year})"
        return citation

class PreprintCitation(CitationAPA):
    def __init__(self, authors, year, title, url):
        super().__init__(authors, year, title)
        self.url = url

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. Preprint retrieved from {self.url}"
        return citation

class OnlineDocumentCitation(CitationAPA):
    def __init__(self, authors, year, title, publisher, date_retrieved, url):
        super().__init__(authors, year, title)
        self.publisher = publisher
        self.date_retrieved = date_retrieved
        self.url = url

    def generate_citation(self):
        citation = f"{self.authors} ({self.year}). {self.title}. {self.publisher}. Retrieved {self.date_retrieved}, from {self.url}"
        return citation

class OnlineDatabaseCitation(OnlineDocumentCitation):
    def generate_citation(self):
        citation = super().generate_citation()
        return citation

class InteractiveCitationGenerator:
    def __init__(self):
        self.attributes = {}
        self.journal_order = {
            1: ["authors", "year", "title", "journal", "volume", "issue", "pages"],
            2: ["authors", "year", "title", "journal", "volume", "issue", "pages", "doi"],
            3: ["authors", "year", "title", "journal", "volume", "doi"],
            4: ["authors", "year", "title", "journal", "volume", "issue", "article_number", "doi"],
            5: ["authors", "year", "title", "newspaper", "url", "date"],
        }
        self.book_order = {
            1: ["authors", "year", "title", "publisher"],
            2: ["authors", "year", "title", "book_title", "editors", "edition", "pages", "publisher"],
            3: ["authors", "year", "title", "book_title", "doi"],
            4: ["authors", "year", "title", "translator", "location", "publisher", "original_year"],
            5: ["authors", "year", "title", "url"],
            6: ["authors", "year", "title", "url", "date_retrieved", "publisher"],
            7: ["authors", "year", "title", "url", "date_retrieved", "publisher"],
        }
        self.journal_types = {
            1: "Journal Article",
            2: "Journal Article with DOI",
            3: "Journal Article by DOI (advance online publication, no page numbers)",
            4: "Article in electronic journal by DOI (no paginated version)",
            5: "Newspaper Article",
        }
        self.book_types = {
            1: "Book",
            2: "Book Chapter",
            3: "OnlineFirst chapter in a series",
            4: "Translated Book",
            5: "Publicly available preprint",
            6: "Online document",
            7: "Online database",
        }
        self.citation_classes = {
        "Journal Article": JournalCitation,
        "Journal Article with DOI": JournalCitationWithDOI,
        "Journal Article by DOI (advance online publication, no page numbers)": OnlineJournalCitation,
        "Article in electronic journal by DOI (no paginated version)": ElectronicJournalCitation,
        "Newspaper Article": NewspaperCitation,
        "Book": BookCitation,
        "Book Chapter": BookChapterCitation,
        "OnlineFirst chapter in a series": OnlineFirstChapterCitation,
        "Translated Book": TranslatedBookCitation,
        "Publicly available preprint": PreprintCitation,
        "Online document": OnlineDocumentCitation,
        "Online database": OnlineDatabaseCitation,
        }

    def get_attribute(self, attr_name):
        while True:
            response = input(f"Please enter the {attr_name} (type 'back' to go back or leave empty to skip): ")
            if response.lower() == "back":
                return "back"
            else:
                return response or None

    def generate_interactive_citation(self):
        with open('/Users/sunluyi/Desktop/APA_Citations.txt', 'a') as f:
            while True:
                form = input("Please enter the citation form (journal or book) or type 'quit' to exit: ")
                if form.lower() == 'quit':
                    break
                elif form.lower() == "journal":
                    print("Please select a journal citation type:")
                    self.print_types(self.journal_types)
                    type_number = self.get_type_number(len(self.journal_types), self.journal_types)
                    self.collect_attributes(self.journal_order[type_number])
                elif form.lower() == "book":
                    print("Please select a book citation type:")
                    self.print_types(self.book_types)
                    type_number = self.get_type_number(len(self.book_types), self.book_types)
                    self.collect_attributes(self.book_order[type_number])
                else:
                    print("Invalid form. Please enter either 'journal' or 'book'.")
                try:
                    citation = self.create_citation()
                    if citation:
                        print("Generated Citation: ")
                        print(citation)
                        f.write(citation + '\n')
                    else:
                        print("Please type in the sufficient attributes!")
                except Exception as e:
                    print(f"An error occurred during citation generation: {e}")
                self.reset()

    def print_types(self, types):
        for num, name in types.items():
            print(f"{num}. {name}")
            
    def get_type_number(self, max_number, types_dict):
        while True:
            try:
                type_number = int(input("Enter the citation type number: "))
                if 1 <= type_number <= max_number:
                    self.attributes["type"] = types_dict[type_number]
                    return type_number
                else:
                    print(f"Invalid number. Please enter a number between 1 and {max_number}.")
            except ValueError:
                print("Invalid input. Please enter a number.")


    def collect_attributes(self, order):
        for attr in order:
            while True:
                response = self.get_attribute(attr)
                if response == "back":
                    if not self.attributes:
                        print("No previous attribute to go back to.")
                    else:
                        self.attributes.popitem()
                        break
                else:
                    self.attributes[attr] = response
                    break

    def create_citation(self):
        citation_class = self.citation_classes.get(self.attributes.get("type"))
        if not citation_class:
            return None
        citation_attributes = self.attributes.copy()  # Copy attributes
        citation_attributes.pop("type", None)  # Remove 'type' key
        citation_instance = citation_class(**citation_attributes)
        return citation_instance.generate_citation()

    def reset(self):
        self.attributes = {}

def reference_order():
    with open('/Users/sunluyi/Desktop/APA_Citations.txt', 'r') as read_obj:
        lines = read_obj.readlines()
    lines.sort(key=lambda x: x.lower())


    with open('/Users/sunluyi/Desktop/APA_Citations.txt', 'w') as write_obj:
        for line in lines:
            write_obj.write(line)

def clean_text(text):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    return pattern.sub('', text)

def get_author_initials(text):
    # Extract author's name and convert to pinyin initials
    author_name = text.split(".")[0]
    pinyin = lazy_pinyin(clean_text(author_name))
    initials = [word[0] for word in pinyin]
    return "".join(initials)

def reference_order_Chinese():
    with open('/Users/sunluyi/Desktop/APA_Citations.txt', 'r') as read_obj:
        lines = read_obj.readlines()
    lines.sort(key=get_author_initials)

    with open('/Users/sunluyi/Desktop/APA_Citations.txt', 'w') as write_obj:
        for line in lines:
            write_obj.write(line)





citation_generator = InteractiveCitationGenerator()
citation_generator.generate_interactive_citation()
reference_order()
reference_order_Chinese()
