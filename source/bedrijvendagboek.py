import os
from os.path import dirname, abspath
from database import *
import logging, config

path = dirname(abspath(__file__)) + '/bedrijvendagboek'

def latexify(text):
    '''escapes certain characters to latex standards'''
    if not(text is None):
        text.replace("%", "\\%")
        text.replace("&", "\\&")
        return text
    else:
        return ''

def stringvalue(boolean):
    '''Changes boolean to string value as it should appear on the page'''
    if boolean:
        return "ja"
    else:
        return "nee"

def bedrijvendagboek_path(name):
    '''returns the path where the file should be saved'''
    return '''%s/%s.pdf''' % (path, name)

def bedrijvendagboek_path_free_page(name, number):
    return '''%s/%s/%s.pdf''' % (path, name, number)

def local_path(name):
    return '''/bedrijvendagboek/%s.pdf''' % (name,)

def local_path_free_page(name, number):
    return '''/bedrijvendagboek/%s/%s.pdf''' % (name, number)

def has_page(name):
    return os.path.exists(bedrijvendagboek_path(name))

def has_free_page(name, number):
    return os.path.exists(bedrijvendagboek_path_free_page(name, number))

def compile_tex(name):
    '''compiles the tex file to pdf'''
    os.system('''pdflatex -interaction=nonstopmode  %s''' % (name))
    os.system('''rm -rf *.aux''')

def create_tex_file(name, location, slogan, why, NL, ENG, FR, DE, jobs, stage, sjobs, field, develop, fy, ch, wi, bio, cw, bio_ing, geo):
    '''generates the tex file and calls the compile function in the end'''
    website = get_website(name)
    name = latexify(name)
    location = latexify(location)
    why = latexify(why)
    slogan = latexify(slogan)
    website = latexify(website)
    field = latexify(field)
    develop = latexify(develop)
    logo = get_logo(name)

    
    read_file = open('''%s/bbentry.tex''' % path, 'r')
    texstring = read_file.read()
    read_file.close()

    texstring = texstring.replace('[NAAM]', name)
    texstring = texstring.replace('[QUOTE]', slogan)
    texstring = texstring.replace('[LOCATIE]', location)
    texstring = texstring.replace('[WEBSITE]', website)
    texstring = texstring.replace('[WAAROM]', why)
    texstring = texstring.replace('[NL]', stringvalue(NL))
    texstring = texstring.replace('[EN]', stringvalue(ENG))
    texstring = texstring.replace('[FR]', stringvalue(FR))
    texstring = texstring.replace('[DE]', stringvalue(DE))
    texstring = texstring.replace('[JOBS]', stringvalue(jobs))
    texstring = texstring.replace('[SJOBS]', stringvalue(sjobs))
    texstring = texstring.replace('[STAGE]', stringvalue(stage))
    texstring = texstring.replace('[FY]', stringvalue(fy))
    texstring = texstring.replace('[CH]', stringvalue(ch))
    texstring = texstring.replace('[WI]', stringvalue(wi))
    texstring = texstring.replace('[BIO]', stringvalue(bio))
    texstring = texstring.replace('[CW]', stringvalue(cw))
    texstring = texstring.replace('[BIN]', stringvalue(bio_ing))
    texstring = texstring.replace('[GEO]', stringvalue(geo))
    texstring = texstring.replace('[OPL]', field)
    texstring =  texstring.replace('[DOORGR]', develop)
    
    tex_file_name = '''%s/%s.tex''' % (path, name)
    tex_file = open(tex_file_name, 'w')
    
    tex_file.write(texstring)
    
    tex_file.close()

    compile_tex(tex_file_name)

def free_page_upload(name, index, raw):

    filename = bedrijvendagboek_path_free_page(name, index)

    if not(os.path.isdir('%s/%s' % (path, name))):
        os.mkdir(path + '/' + name)

    output_file = open(filename, 'w')

    output_file.write(raw)
    output_file.close()
