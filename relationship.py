from models import BaseRelationship
from mongoHandler import MongoHandler


def insert_all_relationships(handler, output_collection, include_losers):
    nominees = handler.get_all()
    for nominee in nominees:
        if len(nominee['nobel']) >= 1 or include_losers:
            for nominator_id, nominations in nominee['nominations'].items(
            ):
                nominator = handler.get_person_by_id(nominator_id)
                min_year, max_year = get_min_max_year_from(nominations)
                relationship = BaseRelationship(
                    nominator_id, nominator['name'],
                    nominator['prizes'], nominee['id'], nominee['name'],
                    len(nominations), min_year, max_year,
                    nominee['prizes']).__dict__
                handler.db[output_collection].insert_one(relationship)


def get_min_max_year_from(nominations):
    min_year = max_year = int(nominations[0]['year'])
    for nomination in nominations:
        nomination_year = int(nomination['year'])
        if nomination_year < min_year:
            min_year = nomination_year
        elif nomination_year > max_year:
            max_year = nomination_year
    return [min_year, max_year]

def yearly_relationship(handler, csvFileName, include_losers):
    nominees = handler.get_all()
    file = open(csvFileName, mode="w", errors="replace")
    file.write("nominee_id,nominee_name,nominator_id,nominator_name")
    for i in range(1901,1972):
        file.write(","+str(i))
    file.write("\n")
    for nominee in nominees:
        if len(nominee['nobel']) >= 1 or include_losers:
            for nominator_id, nominations in nominee['nominations'].items(
            ):
                nominator = handler.get_person_by_id(nominator_id)
                nomination_years = set(int(item["year"]) for item in nominations)
                file.write(nominee['id']+",")
                file.write(nominee['name']+",")
                file.write(nominator_id+",")
                file.write(nominator['name'])
                for i in range(1901,1972):
                    file.write(","+str(i in nomination_years))
                file.write("\n")
    file.close()

def main():
    handler = MongoHandler("people")
    insert_all_relationships(handler, "all_ch_people", True)
    #yearly_relationship(handler, "relation_by_year.csv", True)


if __name__ == "__main__":
    main()
