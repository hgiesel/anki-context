#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki Add-on: Anki Context

Please do not edit this file unless you know what you are doing.

Copyright: (c) 2019 Henrik Giesel <https://github.com/hgiesel>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import importlib.util
aqt_spec = importlib.util.find_spec('aqt')


if aqt_spec is not None:
    from .lib import context

else:
    from lib.parser import setup_parser

    from lib.identifier import Identifier, Printer
    from lib.util import decloze, stdlib
    from lib.srs_connection import AnkiConnection

    ARGV, printer = setup_parser()

    if ARGV.cmd is not None:

        result = None

        if ARGV.cmd == 'paths':
            addr = Identifier(ARGV.uri, printer=printer)
            result = getattr(addr, ARGV.cmd)()

            if ARGV.paths == 'rel':
                result = [(Identifier.to_rel_path(path[0]),path[1]) for path in result]
            elif ARGV.paths == 'id':
                result = [(Identifier.to_identifier(path[0]),path[1]) for path in result]
            elif ARGV.paths == 'shortid':
                result = [(Identifier.to_identifier(path[0], omit_section=True),path[1]) for path in result]
            elif ARGV.paths == 'none':
                result = []

            if ARGV.delimiter == 'default':
                result = [(path[0]+':'+str(path[1])+':',) if path[1] is not None else (path[0],) for path in result]

            Printer.print_stats(result, delimiter=ARGV.delimiter)

        elif ARGV.cmd == 'stats':
            addr = Identifier(ARGV.uri, printer=printer)

            result = getattr(addr, ARGV.cmd)()

            if ARGV.paths == 'default':
                pass

            if ARGV.paths == 'full':
                pass
            elif ARGV.paths == 'rel':
                result = [(Identifier.to_rel_path(e[0]),) + e[1:] for e in result]
            elif ARGV.paths == 'id':
                result = [(Identifier.to_identifier(e[0]),) + e[1:] for e in result]
            elif ARGV.paths == 'shortid':
                result = [(Identifier.to_identifier(e[0], omit_section=True),) + e[1:] for e in result]
            elif ARGV.paths == 'none':
                result = [e[1:] for e in result]

            Printer.print_stats(result, delimiter=ARGV.delimiter)


        elif ARGV.cmd == 'headings':
            addr = Identifier(ARGV.uri, printer=printer)

            result = getattr(addr, ARGV.cmd)()
            lines = [(val['fileName'],heading[0],heading[1]) for val in result for heading in val['headings']]

            if ARGV.paths == 'default':
                pass
            elif ARGV.paths == 'rel':
                lines = [(Identifier.to_rel_path(line[0]),) + line[1:] for line in lines]
            elif ARGV.paths == 'id':
                lines = [(Identifier.to_identifier(line[0]),) + line[1:] for line in lines]
            elif ARGV.paths == 'shortid':
                lines = [(Identifier.to_identifier(line[0], omit_section=True),) + line[1:] for line in lines]
            elif ARGV.paths == 'none':
                lines = [line[1:] for line in lines]

            Printer.print_stats(lines, ARGV.delimiter if not ARGV.delimiter == 'default' else '\t')

        elif ARGV.cmd == 'query':
            addr = Identifier(ARGV.uri, printer=printer)
            result = getattr(addr, ARGV.cmd)(ARGV.validate)
            print(' '.join(result))


        elif ARGV.cmd == 'verify':
            addr = Identifier(ARGV.uri, printer=printer)

            result = getattr(addr, ARGV.cmd)()
            lines = [(entry['fileName'],error['type'],error['info'],error['lineno']) for entry in result for error in entry['errors']]

            if ARGV.paths == 'default':
                lines = [(entry['fileName'],error['type'],error['info'],error['lineno']) for entry in result for error in entry['errors']]
            elif ARGV.paths == 'rel':
                lines = [(Identifier.to_rel_path(entry['fileName']), error['type'],error['info'], error['lineno']) for entry in result for error in entry['errors']]
            elif ARGV.paths == 'id':
                lines = [(Identifier.to_identifier(entry['fileName']), error['type'],error['info'],error['lineno']) for entry in result for error in entry['errors']]
            elif ARGV.paths == 'shortid':
                lines = [(Identifier.to_identifier(entry['fileName'], omit_section=True), error['type'],error['info'],error['lineno']) for entry in result for error in entry['errors']]
            elif ARGV.paths == 'none':
                lines = [(error['type'],error['info'],error['lineno']) for entry in result for error in entry['errors']]

            Printer.print_stats(lines, delimiter=ARGV.delimiter)

        elif ARGV.cmd == 'match':
            anki_connection = AnkiConnection(
                    deck_name='misc::head',
                    model_name='Cloze (overlapping)',
                    quest_field_name='Quest',
                    content_field_name='Quest',
                    quest_id_regex=r':([0-9]+)\a*:')

            addr = Identifier(ARGV.uri, printer=printer)
            result = getattr(addr, ARGV.cmd)(anki_connection)

            Printer.print_stats(result)

        elif ARGV.cmd == 'add':
            anki_connection = AnkiConnection(
                    deck_name='misc::head',
                    model_name='Cloze (overlapping)',
                    quest_field_name='Quest',
                    content_field_name='Quest',
                    quest_id_regex=r':([0-9]+)\a*:')

            tag, qid = Identifier(ARGV.uri, printer=printer).paths(usequest=True)


            result = anki_connection.anki_add(addr[0].replace(':', '::'), addr[1], ARGV.content.read())
            print(result)

        elif ARGV.cmd == 'browse':
            anki_connection = AnkiConnection(
                    deck_name='misc::head',
                    model_name='Cloze (overlapping)',
                    quest_field_name='Quest',
                    content_field_name='Quest',
                    quest_id_regex=r':([0-9]+)\a*:')

            addr = Identifier(ARGV.uri, printer=printer).query()
            result = anki_connection.anki_browse(addr)

            print(result)


        elif ARGV.cmd == 'decloze':
            text = ARGV.infile.read()
            text_declozed = decloze(text)
            print(text_declozed, file=ARGV.outfile)


        elif ARGV.cmd == 'stdlib':
            stdlib()

        else:
            getattr(Identifier(ARGV.uri, printer=printer), ARGV.cmd)()
