# -*- coding: utf-8 -*
from plants_libs.timeit import timeit

class Plant(object):
    def __init__(self, plant=None):
        if plant:
            self.name = plant.get('name')
            self.common_name = plant.get('common_name')
            self.photo = plant.get('photo')
            self.wiki = plant.get('wiki')
            self.descriptors = plant.get('descriptors')
            self.distance = plant.get('distance',0)

    def save(self, db):
        db.execute("INSERT INTO leaves(name,common_name,photo,wiki, descriptors) values (%(name)s,%(common_name)s,%(photo)s,%(wiki)s,%(descriptors)s);",
        {'name':self.name,'common_name':self.common_name, 'photo':self.photo,'wiki':self.wiki,'descriptors':self.descriptors})

    @staticmethod
    def _db_to_plant(plant_result):
        if plant_result:
            plant = {'name':plant_result[0], 'common_name': plant_result[1],'photo':plant_result[2],'wiki':plant_result[3],'descriptors':plant_result[4]}
            if len(plant_result)>5:
                plant['distance'] = plant_result[5]
            return plant
            # return Plant(plant)
        return None

    @staticmethod
    def retrieve(db, name):
        db.execute("SELECT name,common_name,photo,wiki,descriptors FROM Leaves WHERE name=%s LIMIT 1",(name,))
        plants = []
        for plant in db.fetchall():
            plants.append(Plant._db_to_plant(plant))
        return plants

    @timeit
    @staticmethod
    def search(db, descriptors):
        db.execute('''SELECT name, common_name, photo, wiki, descriptors, vdistance(descriptors ,cast(%s as double precision[])) as distance
                      FROM Leaves
                      ORDER BY distance ASC
                      LIMIT 2''', (descriptors,))
        plants = []
        for plant in db.fetchall():
            plants.append(Plant._db_to_plant(plant))
        return plants
