#! /usr/local/bin/python3

import sys, re

def convert_line(line):
    ''' convert a line of html to latex '''
    # html precess
    new_line = line
    new_line = convert_a(new_line)
    new_line = convert_em(new_line)
    new_line = convert_p(new_line)
    new_line = convert_ul(new_line)
    # new_line = convert_numbered_ul(new_line)
    new_line = convert_ol(new_line)
    new_line = convert_b(new_line)
    new_line = convert_blockquote(new_line)
    new_line = convert_span(new_line)
    new_line = convert_img_tex(new_line)
    new_line = remove_redundant_code(new_line)
    new_line = noindent_thm(new_line)



    return new_line


def convert_p(line):
    ''' remove p tags '''

    new_line = re.sub(r'(<p.*?>|</p>)', '\n', line)
    return new_line


def remove_redundant_code(line):


    redundant_code = ["&nbsp;"]
    for w in redundant_code:
        new_line = re.sub(w, '', line)

    return new_line


def convert_em(line):
    new_line = line
    new_line = re.sub(r'<em>', '\emph{', new_line)
    new_line = re.sub(r'</em>', '}', new_line)
    return new_line

def convert_a(line):
    new_line = line
    new_line = re.sub(r'<a(.*?)>', '', new_line)
    new_line = re.sub(r'</a>', '', new_line)
    return new_line

def convert_img_tex(line):
    new_line = line

    # extract the title field in the img tags
    title_fields = re.findall(r'<img.*?title="(.*?)".*?scale="2">', new_line)

    # replace the whole img tag by the latex code of title field
    repl_list = [texify(title) for title in title_fields]

    for repl in repl_list:
        # cannot use repl as string since escape sequence such as '\f' will get intepreted
        new_line = re.sub(r'<img.*?scale="2">', lambda x: repl, new_line, count = 1)


    return new_line

def texify(s):
    ''' convert a string s from title of img tag to tex code '''

    if is_displaymode(s):
        return re.sub(r'^\\displaystyle', r'\[', s) + r'\]'

    # then it must be inline math
    else:
        return '$' + s + '$'


def convert_b(line):
    new_line = line
    new_line = re.sub(r'<b>', r'\\textbf{', new_line)
    new_line = re.sub(r'</b>', '}', new_line)
    return new_line


def convert_span(line):
    new_line = line
    new_line = re.sub(r'<span.*?>|</span>', '', new_line)
    return new_line


def convert_blockquote(line):
    # tentative
    new_line = line
    new_line = re.sub(r'<blockquote>|</blockquote>', '', new_line)
    return new_line

def convert_numbered_ul(line):
    new_line = line
    new_line = re.sub(r'<ul>', r'\\begin{enumerate}[(i)]', new_line)
    new_line = re.sub(r'</ul>', r'\\end{enumerate}', new_line)
    new_line = re.sub(r'<li>\([ivx]+\)', r'\\item', new_line)
    new_line = re.sub(r'</li>', '', new_line)
    return new_line


def convert_ul(line):
    new_line = line
    new_line = re.sub(r'<ul>', r'\\begin{itemize}', new_line)
    new_line = re.sub(r'</ul>', r'\\end{itemize}', new_line)
    new_line = re.sub(r'<li>', r'\\item', new_line)
    new_line = re.sub(r'</li>', '', new_line)
    return new_line

def convert_ol(line):
    new_line = line
    new_line = re.sub(r'<ol>', r'\\begin{enumerate}[(i)]', new_line)
    new_line = re.sub(r'</ol>', r'\\end{enumerate}', new_line)
    new_line = re.sub(r'<li>', r'\\item', new_line)
    new_line = re.sub(r'</li>', '', new_line)
    return new_line

def noindent_thm(line):
    new_line = line

    if re.search(r'(\\textbf{Exercise|\\textbf{Example|\\textbf{Theorem|\\textbf{Definition|\\textbf{Remark|\\textbf{Corollary)', new_line):
        # print("This is new line:"+new_line)
        return '\\noindent' + new_line
    return new_line



def is_displaymode(s):
    return "\\displaystyle" in s















PREAMBLE = r'''\documentclass{article}
\usepackage{amsthm, amsmath, enumerate}

\pretolerance=1000
\linespread{1.15}
\setlength{\parskip}{0.2em}


\def\Box{\qed}

\begin{document}'''





# main
input_file = open(sys.argv[-2], 'r')
output_file = open(sys.argv[-1], 'w')

output_file.write(PREAMBLE)

for line in input_file:
    output_file.write(convert_line(line))

output_file.write("\\end{document}")

input_file.close()
output_file.close()
