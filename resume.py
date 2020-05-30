from subprocess import run
from shlex import split
from pathlib import Path
from textwrap import dedent


def main():
    resume = current_resume()
    resume.to_pdf('resumedev')
    #resume.to_html('resume')


class Resume:

    __slots__ = 'head', 'sections'

    def __init__(self, head, *sections):
        self.head = head
        self.sections = sections

    def to_pdf(self, filename='resume'):
        "given filename (no extension) try to create .tex file and .pdf file"
        tex_filename = filename + '.tex'
        Path(tex_filename).write_text(self.to_latex())
        run(split(f'pdflatex {tex_filename}'))

    def to_latex(self):
        return (f'\n{self.head.to_latex()}\n\\begin{{document}}\n'
                + '\n'.join([s.to_latex() for s in self.sections])
                + '\n\\end{document}')


class ResumeHead:
    __slots__ = 'name', 'street_address', 'city_state_zip', 'email', 'phone'
    def __init__(self, name, street_address, city_state_zip, email, phone):
        self.name = name
        self.street_address = street_address
        self.city_state_zip = city_state_zip
        self.email = email
        self.phone = phone

    def to_latex(self):
        return latex_heading(name=self.name,
          street_address=self.street_address, city_state_zip=self.city_state_zip,
          email=self.email, phone=self.phone)


class ResumeSection:
    __slots__ = 'name', 'subsections'
    def __init__(self, name, *subsections):
        self.name = el(name)
        self.subsections = subsections

    def to_latex(self):
        if len(self.subsections) == 1 and isinstance(self.subsections[0], str):
            return md_to_latex(el(self.subsections[0]))
        return f'\\cvsection{{{self.name}}}\n\n' + '\n\n'.join(
          [ss for ss in 
            (ss if isinstance(ss, str) else ss.to_latex() 
                for ss in self.subsections)])


class FirmSubSection:
    __slots__ = 'firm title location dates items'.split()
    def __init__(self, firm='', title='', location='', dates='', items=None):
        self.firm = firm
        self.title = title
        self.location = location
        self.dates = dates
        self.items = items or Items()

    def to_latex(self):
        sb = r'\sbullet' if self.firm and self.title else ''
        return (f'\\cvsubsection{{{el(self.firm)} {sb} '
                + f'\emph{{{el(self.title)}}}}}'
                + f'{{{el(self.location)}}}'
                + f'{{{el(self.dates)}}}'
               ) + self.items.to_latex()


class PlainSubSection:
    __slots__ = 'name', 'items' 
    def __init__(self, name, *items):
        self.name = name
        self.items = Items(*items)

    def to_latex(self):
        return f'\n\\cvsubsection{{{self.name}}}{{}}{{}}\n{self.items.to_latex()}'


class Items:
    __slots__ = 'items'
    def __init__(self, *items):
        self.items = items
    def to_latex(self):
        items = (i.to_latex() if isinstance(i, SubItems) else i 
                     for i in self.items)
        items = '\n'.join([f'  \\item {el(item)}' for item in items])
        return f'\\begin{{itemize}}\n{items}\n\\end{{itemize}}' if items else ''


class SubItems:
    "list of elements joined by small glyphs or bullets"
    __slots__ = 'items'
    def __init__(self, *items):
        self.items = items
    def to_latex(self):
        return ' \\sbullet '.join([md_to_latex(i).strip() for i in self.items])


def md_to_latex(text):
    if '*' in text:
        print(text)
    b = bytes(text, 'utf-8')
    proc = run(split('pandoc --to=latex'), input=b, capture_output=True)
    return str(proc.stdout, 'utf-8') 


def escape_latex(s):
    "md_to_latex should also cover this, but this (probably) is faster"
    return s.translate(str.maketrans({'&': r'\&', '$': r'\$'}))


el = escape_latex # alias for usage


NYNY = 'New York, NY'
PCOLA = 'Pensacola, FL'
TALLY = 'Tallahassee, FL'
FSU = 'Florida State University'


def current_resume():
    return Resume(
  ResumeHead('Aaron Hall, MBA', '80 Dekalb Ave 14N', 'Brooklyn, NY  11201',
             'aaronchallmba@gmail.com', '+001 (850) 529 9078',
  ),

  ResumeSection('Relevant Domain Knowledge & Experience',

    PlainSubSection('Talks and Community Involvement',
      SubItems('Conference talks: *Slot or Not* at PyCon 2017', '*Linear Models with Python*',
           '*The Python Datamodel: When and how to write objects*', '*Best Practices for Writing Reusable Python*'),
      'Stack Overflow Moderator and top Answerer, top 200 users by Reputation Points All Time, over 120 million reached',
      'FOSS contributions: CPython code and documentation, Jupyter documentation, NixOps types', 
      "Contributed to Documentation on Installing NixOS on Linode's server as a service platform",
      'Organized and Tutored Python Office Hours Sundays for a solid year from 2014 to 2015 - still an event organizer',
      SubItems('Meetup Talks and Lectures: *Learning Python with Best Practices*', 
           '*Python Best Practices*', '*Functional Programming with Python*', 'N-Languages meetup: *Python*')
    ),
    PlainSubSection('Programming Languages, Libraries, and Environments',
      SubItems(*'Python, R, Nix, NixOS, Ubuntu, RHEL, Haskell, OODBs, BASH, HTML, RST, Emacs, Orgmode, Rmarkdown'.split(', ')),
      SubItems(*'MyPy, Matplotlib, Numpy, Scipy, Statsmodels, Scikit-learn, Pandas, Flask, Requests, Jupyter'.split(', ')),
      SubItems(*'Vim, Waf, Scala, Clojure, SAS, SPSS, Stata, Prolog, C, Ruby, Lisps, Fortran, COBOL, SQL, JS, \\LaTeX'.split(', ')),
    ),
    PlainSubSection('Finance/Business Background',
      'Organizer of NYCFinance meetup, host for CFA Study Groups',
      'Have passed CFA Level I, Series 7 & 66, Florida Insurance and Real Estate Licensure Courses and Tests',
      'Answered over 150 Accounting and Tax Questions on Investments Pro-bono for All-Experts.com, highly rated',
    ) 
  ),
  ResumeSection('Professional Experience',
  
    FirmSubSection('Bank of America', 'Software Engineer & Architect', NYNY, 'April 2014 - February 2020', 
      Items(
        'Wrote and Delivered Training to Hundreds of Engineers on Python 2-3 migration, Statistics and Machine Learning',
        'Lead Developer Integrated Jupyter Notebook/Lab with OODB backend for saving notebooks',
        'Technical Subject Matter Expert on various applications for the purpose of auditing',
        'Wrote Documentation and Training on Access Control, Proprietary OODB, Python, IDE, Sphinx, and Batch Jobs',
        'Reviewed Projects for Best Practices & Edited Scripts for Performance, Maintainability, and Readability',
        'Instructed Developers in Best Practices with Weekly Webinars and Regular Code Review',
        'Developed GUI for Continuous Integration and Release Management Tool with Pretty Urls',
        'Developed Extension to Python Logging API',
        'Developed Library to Export Data from native Python to Tableau',
      )
    ),
    # kwargs because no firm listed:
    FirmSubSection(title='Adjunct Professor', location=NYNY, dates='April 2016 - April 2019, Various dates',
      items=Items(
        'Columbia Masters in Operations Research Program, Python course',
        'NYU, Python Certificate Program',
        'Yeshiva, Computational Math and Statistics with Python',
      )
    ),
    FirmSubSection('Rose International', 'Software Engineer, Contractor', NYNY, 'October 2012 - April 2014',
      Items(
        'At BofA, Developed Tool to Document Filesets, Provide Statistics, Push to Environments, and Raise Review Requests',
        'Lead Developer on Portal for Delivering Documentation, Information, Statistics, and Reports',
        'Led Team to use Core Technology, Idiomatic Python, Maintainable Style, Proper Unittesting, and Proper SDLC',
      )
    ),
    FirmSubSection('Simplify IT', 'Technician', NYNY, 'March, 2012 - May, 2012',
      Items(
        'Troubleshot Computers and Networks, Punched Ethernet Panels and Jacks, and Audited and Installed Software',
        'Uploaded and Managed Inventory in an Amazon Web Store, Working With CSV and Flat Files',
      )
    ),
    FirmSubSection('Thornhill Community Supportive Services Inc.', 'Assistant Director', NYNY, 'August, 2011 - February, 2012',
      Items(
        'Operation Planning, Risk Management, and Network, Computer, Accounting, and Electronic Document Administration',
        'Led Team of 17 in Providing Computer Literacy and Coat, Toy, Book, and Media Community Distribution Programs',
      )
    ),
    FirmSubSection('Pvt. Invest. Advisor/Sol Strategies', 'Investment/Strategic Planning', NYNY, 'April, 2007 - October, 2012',
      Items(
        'Advised Sol Strategies on Firm Strategy, Business Development, Cash-Flow Management, and Billing Policy',
        'Consulted on Strategy and Wrote Financial, Investment, and Business Plans and Grant Applications',
      )
    ),
    FirmSubSection(FSU, 'Research Assistant', TALLY, 'August, 2007 - April, 2008',
      Items(
        'Teaching Fellow, Graded for Mergers and Acquisitions, Assisted in Data Collection, Research, and Proctoring Exams',
        'Programmed in SAS, Stata, SPSS, and R and Performed Regressions on Econometric Data',
      )
    ),
    FirmSubSection('Merrill Lynch', 'Financial Advisor', PCOLA, 'May, 2006 - April, 2007', 
      Items(
        'Hosted Speakers, Brought in $3 Million in Accounts, and Serviced More Than 100 House Accounts',
        'Executed Trades and Limit Orders on Exchange Traded Funds, Stocks, Options, and Auction Rate Securities',
      )
    ),
    FirmSubSection('Ameriprise Financial Services', 'Financial Advisor', PCOLA, 'January, 2004 - August, 2005',
      Items(
        'Gave Seminars, Sold Financial Plans, Met Sales Goals, and Applied Monte Carlo Simulation & Modern Portfolio Theory',
        'Series 7 Securities, Series 66 Investment Advisor, Life Insurance, Health Insurance, and Variable Annuity Licensed'
      )
    )
  ),
  ResumeSection('Education',
    
    FirmSubSection('University Of West Florida', 'Master of Business Administration', PCOLA, 'August 2010',
      Items(
        '730 GMAT, 3.6 GPA, 486 Item Bibliographic Database, and International Business Strategy Championship winner',
        'Notable Papers: Predictors of Stock Market Values (Time Series) and Marketing Financial Services (Best in Class)',
        SubItems('Statistics Courses: Econometrics', 'Applied Regression', 'Probability and Statistics', 
                 'Special Topics', 'Quantitative Methods'),
        SubItems('Finance: Financial Management', 'Accounting Aspects', 'Advanced Managerial Economics', 'Static Optimization',
        )
      )
    ),
    FirmSubSection(FSU, 'Bachelor of Science, Political Science & Real Estate', TALLY, 'April 2002',
      Items(
        "National Merit Scholar, Dean's List, and Graduated with 169 credit hours, 3.4 GPA, Boards, Clubs, SGA",
      )
    )
  ),
  ResumeSection('Interests & Miscellany',
    "Big Data, Databases, Statistics, Finance, Economics, Machine Learning, Operating Systems",
    "Extensive Bibliographies: User Experience, Software Design, Finance Classics, Knowledge, and Management"
  )
)


def latex_heading(name, street_address, city_state_zip, email, phone):
    """return template joined with +'s"""
    return r"""
\documentclass[letterpaper,10pt]{article}
\usepackage[margin=.5in, includehead, headsep=0mm, headheight=30pt]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{color}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\definecolor{darkblue}{rgb}{0.0,0.0,0.3}
\hypersetup{colorlinks, breaklinks, linkcolor=darkblue, urlcolor=darkblue, anchorcolor=darkblue,
            citecolor=darkblue}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{""" + el(street_address) + r'\\' + el(city_state_zip) + r"""}
\fancyhead[C]{\Huge \textbf{""" + el(name) + r"""}}
\fancyhead[R]{""" + el(email) + r'\\' + el(phone) + r"""}
\renewcommand{\headrulewidth}{0pt}
% sections
\titleformat{\section}
  {\normalfont\normalsize\scshape}
  {}% no number
  {0pt}% no space
  {}% title
  [\titlerule]
\titleformat{\subsection}
  {\normalfont\normalsize}
  {}
  {0pt}
  {}
\titlespacing{\section}{0pt}{*2}{*1}
\titlespacing{\subsection}{0pt}{*1}{0pt}
\setlist[itemize, 1]{nosep, leftmargin=*}
\newcommand{\sbullet}{%
  \texorpdfstring{\textsbullet}{\textbullet}%
}
\DeclareRobustCommand{\textsbullet}{%
  \unskip~\,\begin{picture}(1,1)(0,-3)\circle*{3}\end{picture}\ %
}
\newcommand{\cvsection}[1]{\section{#1}}
\newcommand{\cvsubsection}[3]{%
  \subsection{\textbf{#1} #2\texorpdfstring{\hfill}{ }#3}%
}
\AtBeginDocument{\setlength{\parindent}{0pt}}
\date{05/27/2020}
"""


if __name__ == '__main__':
    main()
