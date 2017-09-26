#!/usr/bin/python3

import csv
import sys

import bs4

from challonge2csv.utils import fetch, normalize

tournament_results = []
tournament_names = []

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            url = line.strip() + "/standings/"
            tournament_names.append(url)
            html_data = fetch(url)
            html = bs4.BeautifulSoup(html_data, "html.parser")
            rows = html.select('.standings-container tr')

            results = {}
            for row in filter(lambda row: row.select('td.rank'), rows):
                add_row(results, row)

            tournament_results.append(results)

    players = set()
    for t in tournament_results:
        players.update(t.keys())
    players = sorted(players)

    print_results(players, tournament_results)

def add_row(results, row):
    # TODO: Input sanity checking
    rank = int(row.select('td.rank')[0].text)
    name = row.select('td.display_name')[0].text.strip()
    results[normalize(name)] = rank

def print_results(players, tournaments):
    writer = csv.writer(sys.stdout)
    writer.writerow([None] + tournament_names)
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournaments))
        writer.writerow(row)

if __name__ == '__main__':
    main()