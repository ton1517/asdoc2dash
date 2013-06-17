# -*- coding: utf-8 -*-

import os
from pyquery import PyQuery as pq
from dash import *

log = logging.getLogger(__name__)

########################################
# util 
########################################

def _read(path):
    f = open(path, "r")
    page = f.read()
    f.close()
    return page

def _write(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()

_typelabel_map  = {
        "classes" : DashType.CLASS,
        "class" : DashType.CLASS,
        u"クラス" : DashType.CLASS,
        "interfaces" : DashType.INTERFACE,
        "interface" : DashType.INTERFACE,
        u"インターフェイス" : DashType.INTERFACE,
        "functions" : DashType.FUNCTION,
        "function" : DashType.FUNCTION,
        u"関数" : DashType.FUNCTION,
        "methods" : DashType.METHOD,
        "method" : DashType.METHOD,
        u"メソッド" : DashType.METHOD,
        "constants" : DashType.CONSTANT,
        "constant" : DashType.CONSTANT,
        u"定数" : DashType.CONSTANT,
        "property" : DashType.PROPERTY,
        "properties" : DashType.PROPERTY,
        u"プロパティ" : DashType.PROPERTY,
        "event" : DashType.EVENT,
        "events" : DashType.EVENT
}

def _get_type_by_label(label):
    search_label = label.lower()
    dash_type = None

    try:
        dash_type = _typelabel_map[search_label]
    except KeyError:
        for key in _typelabel_map.keys():
            if key in search_label:
                dash_type = _typelabel_map[key]
                break

    return dash_type

########################################
# ASDocParser
########################################

class ASDocParser:

    _packages_html = "package-summary.html"
    _package_html = "package.html"
    _index_html = "index.html"

    def __init__(self, docsetGenerator):
        self.generator = docsetGenerator
        self.generator.plist.dashIndexFilePath = ASDocParser._index_html

        self._doc_path = self.generator.documents_path

    def parse(self):
        log.info("parsing asdoc...")
        self._parse_package_summary()

    def _parse_package_summary(self):
        log.debug("parse package summary")
        file_path = os.path.join(self._doc_path, self._packages_html)
        page = _read(file_path)
        pqpage = pq(page)

        for a in pqpage("table.summaryTable").find("a"):
            pqa = pq(a)
            package_path = pqa.attr.href
            package_name = pqa.text()

            self.generator.add_docset_index(package_name, DashType.PACKAGE, package_path)
            pqa.before(create_anchor(DashType.PACKAGE, package_name))

            self._parse_package(package_name, package_path)

        _write(file_path, str(pqpage))

    def _parse_package(self, package_name, package_path):
        log.debug("parse package")
        file_path = os.path.join(self._doc_path, package_path)
        page = _read(file_path)
        pqpage = pq(page)
        package_dir = os.path.dirname(package_path)

        exists_package_html = False

        for index, table in enumerate(pqpage.find("table.summaryTable")):
            typelabel = pqpage("div.summaryTableTitle").eq(index).text()

            dash_type = _get_type_by_label(typelabel)
            if dash_type is None: continue

            for a in pq(table).find("a"):
                href = pq(a).attr.href
                name = pq(a).text()
                path = os.path.join(package_dir, href)

                if dash_type in {DashType.METHOD, DashType.FUNCTION}:
                    name = name + "()"

                pq(a).before(create_anchor(dash_type, name))

                if dash_type in {DashType.CLASS, DashType.INTERFACE}:
                    self.generator.add_docset_index(name, dash_type, path)
                    self._parse_class(package_name, name, path)
                else:
                    exists_package_html = True

        if exists_package_html:
            self._parse_class(package_name, None, os.path.join(package_dir, ASDocParser._package_html))
        
        _write(file_path, str(pqpage))


    def _parse_class(self, package_name, class_name, class_path):
        log.debug("parse class")
        file_path = os.path.join(self._doc_path, class_path)
        page = _read(file_path)
        pqpage = pq(page)

        for section in pqpage.find("div.summarySection"):
            pqsection = pq(section)
            typelabel = pqsection("div.summaryTableTitle").text()
            dash_type = _get_type_by_label(typelabel)
            if dash_type is None: continue

            pqsection.find("[class^='hideInherited']").remove()

            for a in pqsection.find("a.signatureLink"):
                pqa = pq(a)
                name = pqa.text()
                href = pqa.attr.href
                path = class_path + href
                tmp_type = dash_type

                if name == class_name:
                    tmp_type = DashType.CONSTRUCTOR

                if dash_type in {DashType.METHOD, DashType.FUNCTION}:
                    name = name + "()"

                self.generator.add_docset_index(name, tmp_type, path)

                anchor_name = href.split("#")[1]
                anchor_tag = pqpage.find("[name='%s']"%anchor_name)[0]
                pq(anchor_tag).before(create_anchor(tmp_type, name))

        _write(file_path, str(pqpage))

