# -*- coding: utf-8 -*-

import sqlite3, os, shutil
import plistlib
import logging

log = logging.getLogger(__name__)

########################################
# util
########################################

DEFAULT_DOCSET_PATH = os.path.expanduser("~/Library/Application Support/Dash/DocSets/")

def create_anchor(dash_type, name):
    return "<a name='//apple_ref/cpp/%s/%s' class='dashAnchor' />" % (dash_type, name)
 
########################################
# DocsetGenerator
########################################

class DocsetGenerator:

    def __init__(self, docset_name, docset_path, orig_doc_path, orig_icon_path=None):
        self.docset_name = docset_name
        self.docset_path = docset_path
        self.orig_doc_path = orig_doc_path
        self.orig_icon_path = orig_icon_path
        self.contents_path = os.path.join(self.docset_path, "Contents")
        self.resources_path = os.path.join(self.contents_path, "Resources")
        self.documents_path = os.path.join(self.resources_path, "Documents")
        self.db_path = os.path.join(self.resources_path, "docSet.dsidx")
        self.plist_path = os.path.join(self.contents_path, "Info.plist")
        self.icon_path = os.path.join(self.docset_path, "icon.png")

        self.plist = DocsetPlist(docset_name, docset_name, docset_name.lower())

        self.db = None
        self.cursor = None

    def create_project(self):
        log.info("create docset")
        os.makedirs(self.contents_path)

        log.info("copying documents...")
        shutil.copytree(self.orig_doc_path, self.documents_path)

        if not self.orig_icon_path is None:
            shutil.copy2(self.orig_icon_path, self.icon_path)

        self.plist.writePlist(self.plist_path)
        self.db, self.cursor = self._init_DB(self.db_path)

    def _init_DB(self, dbPath):
        log.info("create database")
        db = sqlite3.connect(dbPath)
        cur = db.cursor()

        try:
            cur.execute('DROP TABLE searchIndex;')
        except:
            pass

        cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

        db.commit()

        return db, cur

    def add_docset_index(self, name, type, path):
        log.debug("addIndex....\nname:%s\ntype:%s\npath:%s" % (name, type, path))
        self.cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, type, path))

    def finish(self):
        log.debug("close database")
        self.db.commit()
        self.db.close()

########################################
# DocsetPlist
########################################

class DocsetPlist:

    def __init__(self,
            CFBundleIdentifier,
            CFBundleName,
            DocSetPlatformFamily,
            DashDocSetFamily="dashtoc",
            dashIndexFilePath=None,
            isDashDocset=True,
            isJavaScriptEnabled=True
            ):

        self.CFBundleIdentifier = CFBundleIdentifier
        self.CFBundleName = CFBundleName
        self.DocSetPlatformFamily = DocSetPlatformFamily
        self.DashDocSetFamily = DashDocSetFamily
        self.isDashDocset = isDashDocset
        self.isJavaScriptEnabled = isJavaScriptEnabled
        self.dashIndexFilePath = dashIndexFilePath

    def writePlist(self, path):

        plist = {
                'CFBundleIdentifier': self.CFBundleIdentifier,
                'CFBundleName': self.CFBundleName,
                'DocSetPlatformFamily': self.DocSetPlatformFamily,
                'DashDocSetFamily': self.DashDocSetFamily,
                'isDashDocset': self.isDashDocset,
                'isJavaScriptEnabled': self.isJavaScriptEnabled
                }

        if self.dashIndexFilePath:
            plist['dashIndexFilePath'] = self.dashIndexFilePath

        log.debug("write plist file.\n" + str(plist))
        plistlib.writePlist(plist, path)

########################################
# DashType
########################################

class DashType:
    ATTRIBUTE = "Attribute"
    BINDING = "Binding"
    CATEGORY = "Category"
    CLASS = "Class"
    COMMAND = "Command"
    CONSTANT = "Constant"
    CONSTRUCTOR = "Constructor"
    DEFINE = "Define"
    DIRECTIVE = "Directive"
    ELEMENT = "Element"
    ENTRY = "Entry"
    ENUM = "Enum"
    ERROR = "Error"
    EVENT = "Event"
    EXCEPTION = "Exception"
    FIELD = "Field"
    FILE = "File"
    FILTER = "Filter"
    FRAMEWORK = "Framework"
    FUNCTION = "Function"
    GLOBAL = "Global"
    GUIDE = "Guide"
    INSTANCE = "Instance"
    INTERFACE = "Interface"
    LIBRARY = "Library"
    MACRO = "Macro"
    METHOD = "Method"
    MIXIN = "Mixin"
    MODULE = "Module"
    NAMESPACE = "Namespace"
    NOTATION = "Notation"
    OBJECT = "Object"
    OPERATOR = "Operator"
    OPTION = "Option"
    PACKAGE = "Package"
    PARAMETER = "Parameter"
    PROPERTY = "Property"
    PROTOCOL = "Protocol"
    RECORD = "Record"
    SAMPLE = "Sample"
    SECTION = "Section"
    SERVICE = "Service"
    STRUCT = "Struct"
    STYLE = "Style"
    TAG = "Tag"
    TRAIT = "Trait"
    TYPE = "Type"
    UNION = "Union"
    VALUE = "Value"
    VARIABLE = "Variable"

