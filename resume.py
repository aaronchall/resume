from subprocess import run
from shlex import split
from pathlib import Path
from textwrap import dedent
from datetime import date


def main():
    resume = current_resume()
    resume.to_pdf('resumedev')
    #resume.to_html('resume')


def current_resume():
    return Resume(
        ResumeHead(
            'Aaron Hall, MBA, MSCS', '5224 Rowe Trail', 
            'Pace, FL  32571', 'aaronchallmba@gmail.com',
            '+001 (850) 529-9078', 'aaronchall'
        ),
        summary(),
        professional_section(),
        education_section(),
        knowledge_section(),
        #interests()
    )


class Resume:

    __slots__ = 'head', 'sections'

    def __init__(self, head, *sections):
        self.head = head
        self.sections = sections

    def to_pdf(self, filename='resume'):
        "given filename (no extension) try to create .tex file and .pdf file"
        tex_filename = filename + '.tex'
        Path(tex_filename).write_text(self.to_latex())
        run(['pdflatex', tex_filename])

    def to_latex(self):
        return (self.head.to_latex() + '\n'
                + '\n'.join([s.to_latex() for s in self.sections])
                + '\n' + r'\end{document}' + '\n')


class ResumeHead:
    __slots__ = 'name', 'street_address', 'city_state_zip', 'email', 'phone', 'linkedin'
    def __init__(self, name, street_address, city_state_zip, email, phone, linkedin):
        self.name = name
        self.street_address = street_address
        self.city_state_zip = city_state_zip
        self.email = email
        self.phone = phone
        self.linkedin = linkedin

    def to_latex(self):
        return latex_heading(name=self.name,
          street_address=self.street_address, city_state_zip=self.city_state_zip,
          email=self.email, phone=self.phone, linkedin=self.linkedin)


class ResumeSection:
    __slots__ = 'name', 'subsections'
    def __init__(self, name, *subsections):
        self.name = el(name)
        self.subsections = subsections

    def to_latex(self):
        if len(self.subsections) == 1 and isinstance(self.subsections[0], str):
            return f'\\cvsection{{{self.name}}}\n\n' + md_to_latex(el(self.subsections[0]))
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
                + f'\\emph{{{el(self.title)}}}}}'
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
    b = bytes(text, 'utf-8')
    proc = run(split('pandoc --to=latex'), input=b, capture_output=True)
    return str(proc.stdout, 'utf-8') 


def escape_latex(s):
    "md_to_latex should also cover this, but this (probably) is faster"
    return s.translate(str.maketrans({'&': r'\&', '$': r'\$'}))


el = escape_latex # alias for very repetitive usage


NYNY = 'New York, NY'
PCOLA = 'Pensacola, FL'
TALLY = 'Tallahassee, FL'
FSU = 'Florida State University'
UWF = 'University of West Florida'


def summary():
    return ResumeSection(
        "Professional Summary",
        nix_mls("""
            Seeking an engineering management or staff technical lead role
            to formalize the leadership I've exercised throughout my career. 
            De facto technical leader, senior software architect, 
            and Python expert with 12 years building large-scale distributed
            systems in financial services — consistently the go-to authority 
            on code quality, best practices, and knowledge transfer. 
            MS in Computer Science (Data Science), researching Large Language 
            Models for Data Analytic Model Selection. 
            Track record of improving system reliability from 50% to nearly 
            100% and training hundreds of engineers. 
            Former educator at Columbia, NYU, and Yeshiva; PyCon speaker; 
            Free Open Source Software contributor;
            ranked 110 all-time on Stack Overflow with over 200 million developers reached.
        """))


def knowledge_section():
    return ResumeSection('Relevant Domain Knowledge & Experience',
    PlainSubSection('Programming Languages, Libraries, and Environments',
      SubItems(*'Python, Rust, R, Nix, NixOS, Ubuntu, RHEL, Haskell, OODBs, BASH, HTML, Emacs, Orgmode, Rmarkdown'.split(', ')),
      SubItems(*'Oracle SQL, MyPy, Matplotlib, Numpy, Scipy, Statsmodels, Scikit-learn, Pandas, Flask, Requests, Jupyter, Spark'.split(', ')),
      SubItems(*'Vim, Waf, Scala, Clojure, SAS, SPSS, Prolog, C, C++, Java, Lisp, Typescript, \\LaTeX'.split(', ')),
    ),
    PlainSubSection('Workshops and Talks Given',
      SubItems('Meetup Talks and Lectures: *Learning Python with Best Practices*',
      '*Python Best Practices*', '*Functional Programming with Python*',
      'N-Languages meetup: *Python*'),
      SubItems('UWF Workshops for the *CS Department C++ Pointers, Memory, and Valgrind* and *C++ File I/O*'), 
      SubItems('UWF ACM: *Python in Industry*', '*Intro to Python*', '*Rust*', '*NixOS*',),
      SubItems('UWF AI and Data Analytics Club: *Eliza in Emacs*', 
               '*AI*', '*NLP*', '*LLMs*', '*Python versus R*'),
      SubItems('Workshops at Emerald Coast Linux User Group: *NixOS*', '*Rust*', '*Python*', '*VPNs*', '*LLMs*'),
      SubItems('Conference talks: *Slot or Not* at PyCon 2017', '*Linear Models with Python*',
      '*The Python Datamodel: When and How to Write Objects*', '*Best Practices for Writing Reusable Python*'),
    ),
    PlainSubSection('Other Community Involvement',
      'Stack Overflow moderator and top answerer, ranked 110 all-time by reputation points, over 200 million reached',
      'FOSS contributions: CPython code and documentation, Jupyter documentation, NixOps types',
      "Contributed to documentation on installing NixOS on Linode's server as a service platform",
      'Organized and tutored Python Office Hours Sundays for a solid year from 2014 to 2015 - still an event organizer',
      'UWF club volunteering: Argopalooza tabling, ACM International Collegiate Programming Contest, Math Club tutoring',
      'Moderator and trusted user roles in various discords and online chat rooms',
    ),
    PlainSubSection('Awards',
      'HackerRank Python Gold Badge',
      'Stack Overflow Python Gold Badge',
      SubItems('Github: Mars 2020 Contributor', 'Arctic Code Vault Contributor'),
    ),
    PlainSubSection('Finance/Business Background',
      'Organizer of NYCFinance meetup, host for CFA Study Groups',
      'Have passed CFA Level I, Series 7 & 66, Florida insurance and real estate licensure courses and tests',
      'Answered over 150 accounting and tax questions on investments pro-bono for All-Experts.com, highly rated',
    )
  )

def professional_section():
    return ResumeSection('Professional Experience',
      FirmSubSection('Icon Consultants', 'Software Architect, Contractor', PCOLA, 'June 2023 - June 2025',
        Items(
          'Assigned to BofA Glass (Distributed compute spreadsheet killer with Tickers, Pricing, Visualization, and Signals)',
          'Declarative infrastructure, OpenShift/Kubernetes Docker containers serve PlayWright running views for report capture',
          'Solved nightly bounce on OpenShift to guarantee fresh services daily supporting hundreds of users',
          'Rewrite of Python backend to expand functionality for Glass Reports, objects and scheduler',
          'Improved reliability to nearly 100\\% from below 50\\% of the Glass Reports system by implementing a new REST API',
          'Added a REST API to track the Glass report log for a user accessible frontend',
          'Added a REST API for Glass profile data leveraging existing websocket API, performance comparison analysis',
          "Served as Glass's Quartz/Python Expert, assisting more junior team members as a force multiplier",
        )
      ),
      FirmSubSection('Icon Consultants', 'Software Engineer, Contractor', PCOLA, 'October 2020 - October 2022',
        Items(
          'BofA Glass: onboarded and wrote ticking data functions for new cryptocurrency data providers',
          'Rewrote application documentation Markdown and CSS for web-based presentation',
          'Wrote new development documentation to get new developers up to speed',
          'Reproducible build pipeline of OpenShift/Kubernetes Docker containers to serve documentation',
          'Recorded instructional videos for users, videos released weekly on internal video channel',
          'Implemented application usage tracking and user functions for data viewing and visualization',
          'Modified user interface functionality in React/JS',
          'Added autocomplete/documentation display feature for a separate class of Glass functions',
          "Served as Glass's Quartz/Python Expert, fixed legacy bugs in the Python",
          'Automated Venafi certificate generation and SAN assignment for hundreds of hosts',
        )
      ),
      FirmSubSection('Bank of America', 'Software Engineer & Architect', NYNY, 'April 2014 - February 2020',
        Items(
          'Contributed to Quartz Academy user interface, an application for training, code execution, and testing',
          'Wrote Quartz Academy training material, content, tests, and direction for other trainers',
          'Wrote and delivered training to hundreds of engineers on Python 2-3 migration, statistics and machine learning',
          'Lead Developer integrating Jupyter Notebook/Lab with OODB backend for notebook management',
          'Technical subject matter expert on various applications for the purpose of auditing',
          'Wrote documentation and training on access control, proprietary OODB, Python, IDE, Sphinx, and batch jobs',
          'Reviewed projects for best practices & edited scripts for performance, maintainability, and readability',
          'Instructed developers in best practices with weekly webinars and regular code review',
          'Developed GUI for continuous integration and release management with pretty urls',
          'Developed extension to Python logging library API',
          'Developed library to export data from native Python to Tableau',
        )
      ),
      # kwargs because no firm listed:
      FirmSubSection(title='Adjunct Professor', location=NYNY, dates='April 2016 - April 2019, Various dates',
        items=Items(
          'Columbia Masters in Operations Research Program, Python course',
          'NYU, Python Certificate Program',
          'Yeshiva, Computational Math and Statistics with Python',)
      ),
      FirmSubSection('Rose International', 'Software Engineer, Contractor', NYNY, 'October 2012 - April 2014',
        Items(
          'At BofA, developed tool to document filesets, provide statistics, push to environments, and raise review requests',
          'Lead developer on portal for delivering documentation, information, statistics, and reports',
          'Led team to use core technology, idiomatic Python, maintainable style, proper unittesting, and proper SDLC',
        )
      ),
      FirmSubSection('Simplify IT', 'Technician', NYNY, 'March 2012 - May 2012',
        Items(
          'Troubleshot computers and networks, punched ethernet panels, and audited and installed software',
          'Uploaded and managed inventory in an Amazon web store, working with CSV and flat files',
        )
      ),
      FirmSubSection('Thornhill Community Supportive Services Inc.', 'Assistant Director', NYNY, 'August 2011 - February 2012',
        Items(
          'Operation planning, risk management, and network, computer, accounting, and electronic document administration',
          'Led team of 17 in providing computer literacy and coat, toy, book, and media community distribution programs',
        )
      ),
      FirmSubSection('Pvt. Invest. Advisor/Sol Strategies', 'Investment/Strategic Planning', NYNY, 'April 2007 - October 2012',
        Items(
          'Advised Sol Strategies on strategy, business development, cashflow management, and billing policy',
          'Consulted on strategy and wrote financial, investment, and business plans and grant applications',
        )
      ),
      FirmSubSection(FSU, 'Research Assistant', TALLY, 'August 2007 - April 2008',
        Items(
          'Teaching fellow, graded for Mergers and Acquisitions, assisted in data collection, research, and proctoring exams',
          'Programmed in SAS, Stata, SPSS, and R and performed regressions on econometric data',
        )
      ),
      FirmSubSection('Merrill Lynch', 'Financial Advisor', PCOLA, 'May 2006 - April 2007',
        Items(
          'Hosted speakers, serviced $3 Million and more than 100 house accounts',
          'Executed trades and limit orders on exchange traded funds, stocks, options, and auction rate securities',
        )
      ),
      FirmSubSection('Ameriprise Financial Services', 'Financial Advisor', PCOLA, 'January 2004 - August 2005',
        Items(
          'Gave seminars, sold financial plans, met sales goals, and applied Monte Carlo simulation & modern portfolio theory',
          'Series 7 securities, Series 66 investment advisor, life insurance, health insurance, and variable annuity licensed'
        )
      )
    )

def education_section():
    return ResumeSection('Education',
    FirmSubSection(UWF, 'M.S. Computer Science (Data Science)', PCOLA, 'December 2025',
      Items(
        '4.0 program GPA', 'President of AI and Data Analytics Club two years running',
        'Working Paper in AI: Large Language Models for Data Analytic Model Selection',
        SubItems('Computing Essentials (Operating Systems and Networking)', 'Parallel and Distributed Programming', 'Data Structures and Algorithms',
                 'Advanced Algorithms', 'Database Systems',
                 'Agile Software Engineering', 'Data Mining', 'Advanced Big Data Analytics'),
      )
    ),
    FirmSubSection(UWF, 'Master of Business Administration', PCOLA, 'August 2010',
      Items(
        '730 GMAT, 3.6 GPA, 486 Item Bibliographic Database, and International Business Strategy Championship winner',
        'Notable Papers: Predictors of Stock Market Values (Time Series) and Marketing Financial Services (Best in Class)',
        SubItems('Statistics Courses: Econometrics', 'Applied Regression', 'Modern Regression Analysis', 'Probability and Statistics',
                 'Special Topics', 'Quantitative Methods', 'Basic Software Tools for Statistics'),
        SubItems('Finance: Financial Management', 'Accounting Aspects', 'Advanced Managerial Economics', 'Static Optimization',
        )
      )
    ),
    FirmSubSection(FSU, 'Bachelor of Science, Political Science & Real Estate', TALLY, 'April 2002',
      Items(
        "National Merit Scholar, Dean's List, and graduated with 169 credit hours, 3.4 GPA, Boards, Clubs, SGA",
      )
    )
  )


def interests():
    return ResumeSection('Interests & Miscellany',
    "Big Data, Databases, Statistics, Finance, Economics, Machine Learning, Operating Systems",
    "Extensive Bibliographies: User Experience, Software Design, Finance Classics, Knowledge, and Management"
  )


def latex_heading(name, street_address, city_state_zip, email, phone, linkedin):
    """return template joined with +'s - """
    return nix_mls(r"""
        \documentclass[letterpaper,10pt]{article}
        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage{lmodern}
        \usepackage[english]{babel}
        \usepackage[margin=0.5in]{geometry}
        \usepackage{lastpage}
        \usepackage{enumitem}
        \usepackage{titlesec}
        \usepackage[hidelinks]{hyperref}
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
        \titlespacing{\section}{0pt}{3pt}{3pt}
        \titlespacing{\subsection}{0pt}{3pt}{0pt}
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
        \date{""" + date.today().isoformat() + r"""}
        \pagestyle{empty}
        \begin{document}
        \raisebox{10pt}[0pt][0pt]{%
        \begin{minipage}[t]{0.23\textwidth}
        """ + street_address + r"\\" + city_state_zip + r"""
        \end{minipage}
        }
        \hfill
        \begin{minipage}[t]{0.5\textwidth}
        \centering
        {\huge \textbf{""" + name + r"""}}
        \end{minipage}
        \hfill
        \raisebox{10pt}[0pt][0pt]{%
        \begin{minipage}[t]{0.23\textwidth}
        \raggedleft
        """ + email + r"\\" + phone + r"\\" +
        r"\href{https://linkedin.com/in/" + linkedin +
                r"}{linkedin.com/in/" + linkedin + r"""}
        \end{minipage}
        }
        """)


def nix_mls(s):
    """
    Given a python multiline string, 
    dedent it and strip one potential leading newline, a'la Nix.
    This makes it possible to have
    - text indented with the rest of the code
    - use the triple quotes as delimiters like regular parens and brackets
    - text start on the next line after the leading triple quotes
    - thus embed documents that look like the way they'll look in a written file.
    i.e. eat your cake and have it too.
    """
    ds = dedent(s)
    if ds[:1] == '\n': # if we start with a newline (it usually looks better)
        return ds[1:]  # then only remove that newline, not other whitespace.
    else:
        return ds

if __name__ == '__main__':
    main()
