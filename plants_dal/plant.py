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
        db.execute("INSERT INTO leaves(name,common_name,photo,wiki) values (%(name)s,%(common_name)s,%(photo)s,%(wiki)s);",
        {'name':self.name,'common_name':self.common_name, 'photo':self.photo,'wiki':self.wiki})
        Plant.add_sample(db, self.name, self.descriptors)

    @staticmethod
    def add_sample(db, name, descriptors):
        db.execute("INSERT INTO descriptors(name, descriptors) values (%(name)s,%(descriptors)s);",
                    {'name':name,'descriptors':descriptors})

    @staticmethod
    def _db_to_plant(plant_result):
        if plant_result:
            plant = {'name':plant_result[0], }
            if len(plant_result)>5:
                plant['distance'] = plant_result[5]
            return plant
            # return Plant(plant)
        return None

    @staticmethod
    def retrieve(db, name):
        db.execute("SELECT name,common_name,photo,wiki FROM Leaves WHERE name=%s LIMIT 1",(name,))
        plants = []
        for plant in db.fetchall():
            plants.append(Plant._db_to_plant(plant))
        return plants

    @staticmethod
    @timeit
    def search(db, descriptors):
        db.execute('''SELECT distinct Leaves.name as name 
                      FROM Leaves, (SELECT name, vdistance(descriptors ,cast(%s as double precision[])) as distance
                                    FROM descriptors
                                    ORDER BY distance ASC
                                    LIMIT 10) as descr
                      WHERE Leaves.name = descr.name;''', (descriptors,))
        plants = []
        for plant in db.fetchall():
            plants.append(Plant._db_to_plant(plant))
        return plants
