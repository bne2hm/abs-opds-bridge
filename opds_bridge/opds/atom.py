import datetime as dt
from lxml import etree

def atom_root(title: str, href_self: str, kind: str = "acquisition"):
    nsmap = {None: "http://www.w3.org/2005/Atom",
             "opds": "http://opds-spec.org/2010/catalog"}
    feed = etree.Element("feed", nsmap=nsmap)
    etree.SubElement(feed, "id").text = href_self
    etree.SubElement(feed, "title").text = title
    etree.SubElement(feed, "updated").text = dt.datetime.utcnow().isoformat() + "Z"

    link_self = etree.SubElement(feed, "link")
    link_self.set("rel", "self")
    link_self.set("href", href_self)
    link_self.set("type", f"application/atom+xml;profile=opds-catalog;kind={kind}")
    return feed

def add_nav_entry(feed, title: str, href: str):
    entry = etree.SubElement(feed, "entry")
    etree.SubElement(entry, "id").text = href
    etree.SubElement(entry, "title").text = title
    etree.SubElement(entry, "updated").text = dt.datetime.utcnow().isoformat() + "Z"
    link = etree.SubElement(entry, "link")
    link.set("rel", "subsection")
    link.set("type", "application/atom+xml;profile=opds-catalog;kind=acquisition")
    link.set("href", href)
    return entry
