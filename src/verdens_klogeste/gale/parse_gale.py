#!/usr/bin/env python3

import gzip
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def get_id(doc, namespaces):
    docids = doc.findall("./gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids", namespaces)
    for docid in docids:
        _id = docid.find('./meta:id', namespaces)
        _type = _id.attrib['type']
        if _type == 'zzNumber':
            #print(ET.tostring(_id))
            val_el = _id.find('./meta:value', namespaces)
            pre_el = _id.find('./meta:prefix', namespaces)
            value = val_el.text if val_el != None else ''
            prefix = pre_el.text if pre_el != None else ''
            #if val_el and pre_el and val_el.text and pre_el.text:
            if value and prefix:
                identifier = f'{prefix}{value}'
                #print(f'ID: {identifier}')
                return identifier
            else:
                return ''
    return ''


def get_title(doc, namespaces):
    title_node =  doc.find("./gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/gift-doc:document-titles/meta:title-display", namespaces)
    title_with_tags =ET.tostring(title_node, 'unicode')
    title = BeautifulSoup(title_with_tags, "lxml").text
    title = title.strip()
    title = title.replace('/', '_')
    #print(title)
    return title

def parse_document(doc, namespaces):
    doc_id = get_id(doc, namespaces)
    if not doc_id:
        return '', '', ''
    try:
        title = get_title(doc, namespaces)
    except AttributeError as e:
        return '', '', ''
    essay_divs = doc.findall("./gift-doc:document/gift-doc:body/essay:div", namespaces)
    text = []
    for essay_div in essay_divs:
        for node in essay_div:
            if node.tag.startswith(f'{{{namespaces["essay"]}}}'):
                if node.text:
                    text.append(node.text.strip())
    return doc_id, title, ' '.join(text).strip()


def fetch_documents_from_file(filename):
    docs = []
    with gzip.open(filename, 'rb') as f:
        file_content = f.read()
        root = ET.fromstring(file_content)
        namespaces = {
            'gold': 'http://www.gale.com/gold',
            'meta': 'http://www.gale.com/goldschema/metadata',
            'gift-doc': 'http://www.gale.com/goldschema/gift-doc',
            'essay': 'http://www.gale.com/goldschema/essay',
        }
        for doc in root.findall('gold:document-instance', namespaces):
            doc_id, title, text = parse_document(doc, namespaces)
            if doc_id and text:
                res = {
                    'docid': doc_id,
                    'title': title,
                    'text': text,
                    'filename': filename
                }
                docs.append(res)
    return docs

                
if __name__ == '__main__':
    import glob
    import json
    
    outfile = '/data/verdens_klogeste_gale/vk_gale_data.json'
    filenames = glob.glob('/data/verdens_klogeste_gale/*/*.xml.gz')
    #outfile = 'vk_gale_data.json'
    #filenames = ['/data/verdens_klogeste_gale/Student/NREF-P10-0.xml.gz']
    #print(filenames)
    with open(outfile, 'w') as of:
        for i, filename in enumerate(filenames):
            print(f'{filename} - {i+1}/{len(filenames)}')
            docs = fetch_documents_from_file(filename)
            for doc in docs:
                json.dump(doc, of)
                of.write('\n')
        
