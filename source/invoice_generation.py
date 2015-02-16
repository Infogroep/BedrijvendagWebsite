from bedrijvendagboek import latexify
import os
from shutil import copyfile

def generate_invoice(company, representative, address1, address2, address3, edition, displaytype, displaycost):
    """Generate a new invoice for a company using the provided information"""

    company = latexify(company)
    representative = latexify(representative)
    address1 = latexify(address1)
    address2 = latexify(address2)
    address3 = latexify(address3)
    edition = edition
    displaytype = latexify(displaytype)
    displaycost = displaycost

    read_file = open('''invoices/invoice_template.tex''', 'r')
    texstring = read_file.read()
    read_file.close()

    texstring = texstring.replace('[[COMPANY]]', company)
    texstring = texstring.replace('[[REPRESENTATIVE]]', representative)
    texstring = texstring.replace('[[COMPANYADDRESS1]]', address1)
    texstring = texstring.replace('[[COMPANYADDRESS2]]', address2)
    texstring = texstring.replace('[[COMPANYADDRESS3]]', address3)
    texstring = texstring.replace('[[EDITION]]', str(edition))
    texstring = texstring.replace('[[DISPLAYTYPE]]', displaytype)
    texstring = texstring.replace('[[DISPLAYCOST]]', str(displaycost))

    tex_file_name = '''invoices/%s/%s.tex''' % (company, company)
    if not os.path.exists('invoices/%s/' % company):
        os.makedirs('invoices/%s/' % company)
    tex_file = open(tex_file_name, 'w')
    tex_file.write(texstring)
    tex_file.close()

def compile_latex(company):
    '''compiles the tex file to pdf'''
    os.system('''/usr/texbin/pdflatex -interaction=nonstopmode -output-directory="invoices/%s"  "invoices/%s/%s.tex"''' % (company, company, company))
    os.system('''rm -rf invoices/%s/*.aux''' % company)
    os.system('''rm -rf invoices/%s/*.log''' % company)