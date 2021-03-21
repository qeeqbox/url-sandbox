'''
    __G__ = "(G)bd249ce4"
    backend -> report
'''

from os import path
from json import loads, dumps, JSONEncoder
from pickle import load as pload
from base64 import b64encode
from datetime import datetime
from tinydb import TinyDB, Query
from binascii import unhexlify
from jinja2 import Template, Environment, FileSystemLoader
from shared.logger import log_string, ignore_excpetion
from shared.settings import defaultdb
from shared.mongodbconn import add_item_fs, find_item


class ComplexEncoder(JSONEncoder):
    '''
    this will be used to encode objects
    '''

    def default(self, obj):
        '''
        override default
        '''
        if not isinstance(obj, str):
            return str(obj)
        return JSONEncoder.default(self, obj)


def pretty_json(value):
    '''
    object to json
    '''
    return dumps(value, indent=4)


def make_json_table(env, data, header) -> str:
    '''
    render json html table
    '''
    parsed_header = header.replace(' ', '_')
    temp = """
    <div class="tablewrapper">
    <table>
        <thead>
            <tr>
                <th colspan="1" onclick=toggle_class(".table-{{ parsed_header }}")>{{ header }}</th>
            </tr>
        </thead>
        <tbody class="table-{{ parsed_header }}" style="display:none";>
           {%- for row in data -%}
               <tr>
                <td><pre>{{ row | pretty_json }}</pre></td>
               </tr>
           {%- endfor -%}
        </tbody>
    </table>
    </div>"""

    result = env.from_string(temp).render(header=header, parsed_header=parsed_header, data=data)
    return result


def make_json_table_no_loop(env, data, header) -> str:
    '''
    render json html table
    '''
    parsed_header = header.replace(' ', '_')
    temp = """
    <div class="tablewrapper">
    <table>
        <thead>
            <tr>
                <th colspan="1" onclick=toggle_class(".table-{{ parsed_header }}")>{{ header }}</th>
            </tr>
        </thead>
        <tbody class="table-{{ parsed_header }}" style="display:none";>
               <tr>
                <td><pre>{{ data | pretty_json }}</pre></td>
               </tr>
        </tbody>
    </table>
    </div>"""

    result = env.from_string(temp).render(header=header, parsed_header=parsed_header, data=data)
    return result


def make_text_table(env, data, header) -> str:
    '''
    render text html table
    '''
    parsed_header = header.replace(' ', '_')
    temp = """
    <div class="tablewrapper">
    <table>
        <thead>
            <tr>
                <th colspan="1" onclick=toggle_class(".table-{{ parsed_header }}")>{{ header }}</th>
            </tr>
        </thead>
        <tbody class="table-{{ parsed_header }}" style="display:none";>
           {%- for row in data -%}
               <tr>
                <td>{{ row }}</td>
               </tr>
           {%- endfor -%}
        </tbody>
    </table>
    </div>"""

    result = env.from_string(temp).render(header=header, parsed_header=parsed_header, data=data)
    return result


def make_image_table_base64(env, data, header) -> str:
    '''
    render image inside html table
    '''
    parsed_header = header.replace(' ', '_')
    temp = """
    <div class="tablewrapper">
    <table>
        <thead>
            <tr>
                <th colspan="1" onclick=toggle_class(".table-{{ parsed_header }}")>{{ header }}</th>
            </tr>
        </thead>
        <tbody class="table-{{ parsed_header }}" style="display:none";>
               <tr>
                    <td><img class="fullsize" src="{{ data }}" /></td>
                </tr>
        </tbody>
    </table>
    </div>"""
    result = env.from_string(temp).render(header=header, parsed_header=parsed_header, data=data)
    return result


ENV_JINJA2 = Environment(autoescape=True, loader=FileSystemLoader('/tmp'), trim_blocks=True, lstrip_blocks=True)
ENV_JINJA2.filters['pretty_json'] = pretty_json


def make_report(parsed):
    '''
    make the html table
    '''
    table = ""
    full_table = ""

    analyzer_db = None
    sniffer_db = None

    analyzer_path = "{}{}{}".format(parsed['locations']['box_output'], parsed['task'], parsed['locations']['analyzer_logs'])
    sniffer_path = "{}{}{}".format(parsed['locations']['box_output'], parsed['task'], parsed['locations']['sniffer_logs'])

    analyzer_db = TinyDB(analyzer_path)
    sniffer_db = TinyDB(sniffer_path)

    with open(analyzer_path) as file:
        temp_id = add_item_fs(defaultdb["dbname"], defaultdb["reportscoll"], file.read(), parsed['task'], None, parsed['task'], "application/json", datetime.now())

    with ignore_excpetion():
        screenshot_table = analyzer_db.table('screenshot_table')
        item = screenshot_table.search(lambda x: x if 'normal_image' in x else 0)
        if item:
            bimage = b64encode(unhexlify(item[0]['normal_image'].encode('utf-8')))
            img_base64 = "data:image/jpeg;base64, {}".format(bimage.decode("utf-8", errors="ignore"))
            table += make_image_table_base64(ENV_JINJA2, img_base64, "Screenshot")
            log_string("Parsed normal screenshot", task=parsed['task'])

    with ignore_excpetion():
        screenshot_table = analyzer_db.table('screenshot_table')
        item = screenshot_table.search(lambda x: x if 'full_image' in x else 0)
        if item:
            bimage = b64encode(unhexlify(item[0]['full_image'].encode('utf-8')))
            img_base64 = "data:image/jpeg;base64, {}".format(bimage.decode("utf-8", errors="ignore"))
            table += make_image_table_base64(ENV_JINJA2, img_base64, "Full Screenshot")
            log_string("Parsed full screenshot", task=parsed['task'])

    with ignore_excpetion():
        network_table = analyzer_db.table('network_table')
        item = network_table.search(lambda x: x if 'circular_layout' in x else 0)
        if item:
            bimage = b64encode(unhexlify(item[0]['circular_layout'].encode('utf-8')))
            img_base64 = "data:image/jpeg;base64, {}".format(bimage.decode("utf-8", errors="ignore"))
            table += make_image_table_base64(ENV_JINJA2, img_base64, "Network Graph")
            log_string("Parsed Network Graph", task=parsed['task'])

    with ignore_excpetion():
        words_table = analyzer_db.table('extracted_table')
        item = words_table.search(lambda x: x if 'dns_records' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["dns_records"], "DNS Records")

    with ignore_excpetion():
        words_table = analyzer_db.table('extracted_table')
        item = words_table.search(lambda x: x if 'Request_Headers' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["Request_Headers"], "Request Headers")

    with ignore_excpetion():
        words_table = analyzer_db.table('extracted_table')
        item = words_table.search(lambda x: x if 'Response_Headers' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["Response_Headers"], "Response Headers")

    with ignore_excpetion():
        words_table = analyzer_db.table('extracted_table')
        item = words_table.search(lambda x: x if 'Certificate' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["Certificate"], "Certificate")

    with ignore_excpetion():
        words_table = analyzer_db.table('words_table')
        item = words_table.search(lambda x: x if 'all_words' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item, "OCR Words")

    with ignore_excpetion():
        extracted_table = analyzer_db.table('extracted_table')
        item = extracted_table.search(lambda x: x if 'extracted_links' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["extracted_links"], "Extracted links")

    with ignore_excpetion():
        extracted_table = analyzer_db.table('extracted_table')
        item = extracted_table.search(lambda x: x if 'extracted_scripts' in x else 0)
        if item:
            table += make_json_table_no_loop(ENV_JINJA2, item[0]["extracted_scripts"], "Extracted scripts")

    with ignore_excpetion():
        analyzer_table = analyzer_db.table('analyzer_table')
        if len(analyzer_table.all()) > 0:
            table += make_json_table(ENV_JINJA2, analyzer_table.all(), "Browser")

    with ignore_excpetion():
        sniffer_table = sniffer_db.table('sniffer_table')
        if len(sniffer_table.all()) > 0:
            table += make_json_table_no_loop(ENV_JINJA2, sniffer_table.all(), "Sniffer")

    all_logs = find_item(defaultdb["dbname"], defaultdb["taskdblogscoll"], {'task': parsed['task']})
    if all_logs:
        full_table = make_text_table(ENV_JINJA2, all_logs['logs'], "Logs")
        log_string("Adding logs", task=parsed['task'])

    full_table += table
    if len(full_table) == 0:
        full_table = "Error"

    with open("template.html") as file:
        rendered = Template(file.read()).render(title=parsed['task'], content=full_table)
        temp_id = add_item_fs(defaultdb["dbname"], defaultdb["reportscoll"], rendered, parsed['task'], None, parsed['task'], "text/html", datetime.now())

    temp_id = add_item_fs(defaultdb["dbname"], defaultdb["taskfileslogscoll"], "\n".join(all_logs['logs']), "log", None, parsed['task'], "text/plain", datetime.now())
